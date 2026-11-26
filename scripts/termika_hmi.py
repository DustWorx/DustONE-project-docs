#!/usr/bin/env python3
"""Bilans cieplny HMI na sloncu (O-034) - siec cieplna 4 wezlow, stan ustalony.

Wezly: P - szklo LCD z polaryzatorami (tu siedzi ciekly krysztal),
       B - podswietlenie + PCB modulu + ramka, W - szybka ochronna,
       E - obudowa HMI (z plytka procesora). Otoczenie = T_ot.
Wszystkie parametry geometryczne i optyczne to zalozenia (Z30) - do
zastapienia pomiarem na makiecie (T-ENV-003a). Model sluzy do porownania
rozwiazan, nie do potwierdzenia temperatury.

Uzycie: python3 scripts/termika_hmi.py  -> tabela przypadkow, kod wyjscia 0.
"""
import numpy as np

SIGMA = 5.67e-8
G_SUN = 1000.0          # W/m2, naslonecznienie prostopadle do ekranu (najgorszy przypadek)
A_W = 0.0045            # m2, okno nad panelem (pole aktywne 70,08 x 52,56 mm + margines)
A_E = 0.025             # m2, zewnetrzna powierzchnia obudowy oddajaca cieplo
A_ES = 0.005            # m2, naslonecznione rzutowane pole obudowy poza oknem
T_OP_MAX, T_ST_MAX = 70.0, 80.0   # karta RVT35HHBNWN00 Rev 1.3 s. 6

# podzial widma slonca: UV ~5 %, widzialne ~45 %, podczerwien ~50 %
A_P = 0.05 + 0.45 * 0.85   # pochlanianie w panelu: UV + widzialne w polaryzatorach
A_B = 0.50 * 0.60          # podczerwien przechodzi przez polaryzatory, ~60 % pochlania tyl modulu
H_PB = 50.0                # W/m2K, szklo LCD -> podswietlenie (szczelina + folie + swiatlowod)
P_MOD_LOGIKA = 0.6         # W, modul: 3,3 V x 180 mA (karta s. 6)
P_PODSW = 0.75             # W, podswietlenie 5 V x 150 mA przy 100 % (karta s. 7)
P_PLYTKA = 0.86            # W, STM32G474RE 170 MHz (~+0,11 W wobec STM32G0B1, 26.11.2026), CAN, straty przetwornic 5/3,3 V, LED przyciskow (razem z modulem ~2,1 W, zgodnie z produkt.md 9.1)


def h_zewn(v):
    """Wspolczynnik wymiany ciepla na zewnatrz [W/m2K]: konwekcja + promieniowanie."""
    h_rad = 4 * 0.9 * SIGMA * (330.0 ** 3)          # ~7,3; promieniowanie do otoczenia (bez zimnego nieba)
    if v <= 0:
        h_conv = 6.0                                  # konwekcja swobodna, plyta ~7 cm, dT ~30 K
    else:
        L, nu, k = 0.08, 1.7e-5, 0.028
        re = v * L / nu
        h_conv = 0.664 * re ** 0.5 * 0.7 ** (1 / 3) * k / L   # plyta, przeplyw laminarny
    return h_conv + h_rad


def okno(rodzaj):
    """(odbicie, pochlanianie, przepuszczanie slonca, przewodnosc szczeliny panel-okno W/m2K)."""
    if rodzaj == 'PC':           # poliweglan 2 mm, szczelina powietrzna 2 mm
        gap = 0.028 / 0.002 + 7.0
        return 0.09, 0.06, 0.85, 1 / (1 / gap + 0.002 / 0.2)
    if rodzaj == 'PC+IR':        # j.w. z powloka odbijajaca podczerwien (hot mirror)
        gap = 0.028 / 0.002 + 7.0
        return 0.45, 0.07, 0.48, 1 / (1 / gap + 0.002 / 0.2)
    if rodzaj == 'szklo-klej':   # szklo 1,1 mm klejone optycznie do panelu (OCA 0,2 mm)
        return 0.06, 0.04, 0.90, 1 / (0.0002 / 0.2 + 0.0011 / 1.0)
    if rodzaj == 'szklo-klej+IR':
        return 0.45, 0.05, 0.50, 1 / (0.0002 / 0.2 + 0.0011 / 1.0)
    raise ValueError(rodzaj)


def licz(T_ot=40.0, v=0.0, okno_r='PC', obud='Al-kontakt', alfa_e=0.9, cien=0.0,
         podsw=1.0, zasilanie=True, g_be=None):
    """Zwraca temperatury [P, B, W, E] w degC."""
    refl, a_w, tau, g_pw_m2 = okno(okno_r)
    G = G_SUN * (1 - cien)                 # daszek zaslania okno
    G_e = G_SUN * (1 - 0.5 * cien)         # i polowe obudowy
    h = h_zewn(v)
    if g_be is None:
        g_be = {'Al-kontakt': 2.0, 'Al-luzno': 0.12, 'tworzywo': 0.12}[obud]
    eta = {'Al-kontakt': 1.0, 'Al-luzno': 1.0, 'tworzywo': 0.5}[obud]   # rozplyw ciepla po obudowie
    G_PW = A_W * g_pw_m2
    G_PB = A_W * H_PB
    G_WA = A_W * h
    G_EA = A_E * h * eta
    el = 1.0 if zasilanie else 0.0
    q = np.array([
        G * A_W * tau * A_P,                                            # P
        G * A_W * tau * A_B + el * (P_MOD_LOGIKA + podsw * P_PODSW),     # B
        G * A_W * a_w,                                                  # W
        alfa_e * G_e * A_ES + el * P_PLYTKA,                            # E
    ])
    # macierz przewodnosci (wezly P, B, W, E), otoczenie jako odniesienie
    K = np.zeros((4, 4))
    def lacz(i, j, g):
        K[i, i] += g; K[j, j] += g; K[i, j] -= g; K[j, i] -= g
    lacz(0, 2, G_PW); lacz(0, 1, G_PB); lacz(1, 3, g_be)
    K[2, 2] += G_WA; K[3, 3] += G_EA
    return T_ot + np.linalg.solve(K, q)


PRZYPADKI = [
    ('A  postoj, Al+kontakt, czarna, PC',                dict()),
    ('B  jw., obudowa jasna',                             dict(alfa_e=0.3)),
    ('C  jw., tworzywo czarne bez kontaktu',              dict(obud='tworzywo')),
    ('D  jw. A, podswietlenie 30 %',                      dict(podsw=0.3)),
    ('E  jw. A, szyba z filtrem IR',                      dict(okno_r='PC+IR')),
    ('F  jw. A, szklo klejone optycznie',                 dict(okno_r='szklo-klej')),
    ('G  jw. A, klejone + filtr IR',                      dict(okno_r='szklo-klej+IR')),
    ('H  jw. A, daszek zaslania ekran',                   dict(cien=1.0)),
    ('I  jazda 3 m/s (11 km/h), wariant A',               dict(v=3.0)),
    ('J  jazda 8 m/s (29 km/h), wariant A',               dict(v=8.0)),
    ('K  postoj, zaplon wylaczony, wariant A',            dict(zasilanie=False)),
    ('L  postoj, zaplon wylaczony, klejone + IR',         dict(zasilanie=False, okno_r='szklo-klej+IR')),
    ('M  jasna + filtr IR',                               dict(alfa_e=0.3, okno_r='PC+IR')),
    ('N  jasna + klejone + filtr IR',                     dict(alfa_e=0.3, okno_r='szklo-klej+IR')),
    ('O  jasna + daszek',                                 dict(alfa_e=0.3, cien=1.0)),
    ('P  czarna Al bez kontaktu',                         dict(obud='Al-luzno')),
    ('R  tworzywo czarne, zaplon wylaczony',              dict(obud='tworzywo', zasilanie=False)),
]


def kontrast(R_lustr, tau, L_nieba=6000.0, E=80000.0, R_rozpr=0.005, L_pan=1000.0, CR_pan=1000.0):
    """Kontrast ekranu w sloncu: (L_wl + L_odb) / (L_wyl + L_odb).
    L_odb = odbicie lustrzane nieba + odbicie rozproszone oswietlenia E (HMI-UI-005: 80 klx)."""
    L_wl = L_pan * tau
    L_odb = R_lustr * L_nieba + R_rozpr * E / np.pi
    return (L_wl + L_odb) / (L_wl / CR_pan + L_odb)


CZYTELNOSC = [  # (opis, suma odbic lustrzanych, przepuszczanie swiatla)
    ('szyba PC ze szczelina, bez AR (3 powierzchnie x ~5 %)', 0.15, 0.85),
    ('szyba ze szczelina, AR obustronnie + panel 4 %',        0.05, 0.90),
    ('szklo klejone optycznie, bez AR',                       0.04, 0.92),
    ('szklo klejone optycznie + AR na zewnatrz',              0.005, 0.95),
]


def main():
    for T_ot in (40.0, 45.0):
        print(f'\nOtoczenie {T_ot:.0f} degC, slonce {G_SUN:.0f} W/m2 prostopadle; '
              f'granice panelu: praca {T_OP_MAX:.0f}, przechowywanie {T_ST_MAX:.0f} degC')
        print(f'{"przypadek":46s} {"panel":>6s} {"tyl":>6s} {"okno":>6s} {"obud":>6s}  ocena')
        for nazwa, kw in PRZYPADKI:
            P, B, W, E = licz(T_ot=T_ot, **kw)
            lim = T_OP_MAX if kw.get('zasilanie', True) else T_ST_MAX
            ocena = 'OK' if max(P, B) <= lim - 5 else ('GRANICA' if max(P, B) <= lim else 'PRZEKROCZONE')
            print(f'{nazwa:46s} {P:6.1f} {B:6.1f} {W:6.1f} {E:6.1f}  {ocena}')
    # wymagana przewodnosc modul -> obudowa (aluminium), zeby panel <= 65 degC
    print('\nWymagany kontakt cieplny modul -> obudowa [W/K] dla panelu <= 65 degC (postoj, bezwietrznie):')
    for nazwa, kw in (('jasna', dict(alfa_e=0.3)), ('jasna + filtr IR', dict(alfa_e=0.3, okno_r='PC+IR')),
                      ('jasna + daszek', dict(alfa_e=0.3, cien=1.0)), ('czarna', dict())):
        wyn = []
        for T_ot in (40.0, 45.0):
            g = next((g for g in np.arange(0.05, 10.0, 0.05) if licz(T_ot=T_ot, g_be=g, **kw)[0] <= 65.0), None)
            wyn.append('nieosiagalne' if g is None else f'>= {g:.2f}')
        print(f'  {nazwa:18s} 40 degC: {wyn[0]:>13s}   45 degC: {wyn[1]:>13s}')
    # wrazliwosc na zalozenia optyczne (wariant A, 40 degC)
    global A_P, A_B
    print('\nWrazliwosc wariantu A (40 degC) na pochlanianie w module:')
    for ap, ab in ((0.35, 0.20), (0.43, 0.30), (0.50, 0.45)):
        A_P, A_B = ap, ab
        P, B, _, _ = licz()
        print(f'  panel {ap:.2f} / tyl {ab:.2f}  ->  panel {P:5.1f}  tyl {B:5.1f} degC')
    print('\nKontrast w sloncu (niebo 6000 cd/m2 odbite lustrzanie, 80 klx rozproszone 0,5 %, panel 1000 cd/m2):')
    for opis, R, tau in CZYTELNOSC:
        print(f'  {opis:56s} {kontrast(R, tau):4.1f} : 1')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
