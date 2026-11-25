#!/usr/bin/env python3
"""Model bledu prognozy kata zaplonu na kole z jednym wypustem (O-008).

Geometria (firmware.md C.1.1): krawedz natarcia wypustu = kat 0 obrotu (30 st. przed GMP),
krawedz splywu = 30 st. (GMP). Iskra zadana przy wyprzedzeniu a, czyli w kacie
dth = 30 - a od krawedzi natarcia. Zwloke liczy sie w czasie od krawedzi natarcia:
t = dth / w_est. Blad = kat, w ktorym wal faktycznie jest w chwili iskry, minus dth
(ujemny = iskra za wczesnie, dodatni = za pozno).

Estymaty predkosci (C.1.4):
  E0 - czas przejscia wypustu z poprzedniego obrotu (30 st. / t_wypustu),
  E1 - E0 x (T[n-2] / T[n-1]) - korekta przyspieszenia z dwoch ostatnich okresow obrotu.

Profile predkosci (wzgledna predkosc f od kata walu, zmiana B na obrot, liniowo w kacie):
  hamowanie      - stala predkosc, od kata th0 hamowanie B na obrot,
  odwrocenie     - przyspieszanie B na obrot od 3 obrotow, od th0 hamowanie B na obrot,
  przyspieszenie - stala predkosc, od th0 przyspieszanie B na obrot.
Najgorszy przypadek liczony po fazach poczatku zmiany wzgledem krawedzi i po kolejnych
iskrach po zmianie. Wynik w % zmiany predkosci na obrot nie zalezy od obrotow
(sprawdzane przez porownanie 1500 i 8000 obr/min).

Uzycie: python3 scripts/model_kata.py [budzet_wczesnie budzet_pozno]  (domyslnie 0.7 1.7)
"""
import sys


def profil(rodzaj, B, th0):
    def f(th):
        if rodzaj == 'hamowanie':
            return 1.0 if th < th0 else 1.0 - B * (th - th0) / 360.0
        if rodzaj == 'przyspieszenie':
            return 1.0 if th < th0 else 1.0 + B * (th - th0) / 360.0
        if rodzaj == 'odwrocenie':
            ths = th0 - 3 * 360.0
            if th < ths:
                return 1.0
            if th < th0:
                return 1.0 + B * (th - ths) / 360.0
            return 1.0 + B * (th0 - ths) / 360.0 - B * (th - th0) / 360.0
        raise ValueError(rodzaj)
    return f


def symuluj(N0, f, dth, est='E1', nev=6, krok=0.02, start_obr=5):
    """Calkuje czas po kacie; zwraca liste bledow [st.] dla nev iskier od obrotu start_obr."""
    w0 = N0 * 6.0                       # st./s
    obr = start_obr + nev + 1
    n = int(round(obr * 360.0 / krok))
    t = [0.0] * (n + 1)
    for i in range(n):
        th = (i + 0.5) * krok
        w = w0 * f(th)
        if w <= 0:
            return None                  # wal sie zatrzymal
        t[i + 1] = t[i] + krok / w
    idx = lambda th: int(round(th / krok))
    def kat_w_czasie(tt, i0):
        i = i0
        while i < n and t[i + 1] <= tt:
            i += 1
        if i >= n:
            return None
        return (i + (tt - t[i]) / (t[i + 1] - t[i])) * krok
    bledy = []
    for k in range(start_obr, start_obr + nev):
        e_k = 360.0 * k
        t_wyp = t[idx(e_k - 360.0 + 30.0)] - t[idx(e_k - 360.0)]
        w_est = 30.0 / t_wyp
        if est == 'E1':
            T1 = t[idx(e_k)] - t[idx(e_k - 360.0)]
            T2 = t[idx(e_k - 360.0)] - t[idx(e_k - 720.0)]
            w_est *= T2 / T1
        tz = t[idx(e_k)] + dth / w_est
        th = kat_w_czasie(tz, idx(e_k))
        if th is None:
            return None
        bledy.append(th - e_k - dth)
    return bledy


def najgorszy(N, rodzaj, B, dth, est="E1", fazy=24):
    """Najgorszy blad (min - za wczesnie, max - za pozno) po fazach poczatku zmiany."""
    lo, hi = 0.0, 0.0
    for j in range(fazy):
        th0 = 360.0 * 5 + j * 360.0 / fazy      # zmiana w obrocie pierwszej ocenianej iskry
        b = symuluj(N, profil(rodzaj, B, th0), dth, est)
        if b is None:
            return None
        lo, hi = min(lo, min(b)), max(hi, max(b))
    return lo, hi


def obwiednia(N, rodzaj, dth, wcz=0.7, pozn=1.7, est='E1'):
    """Najwieksza zmiana predkosci na obrot [%], przy ktorej blad miesci sie w budzecie."""
    def ok(B):
        r = najgorszy(N, rodzaj, B, dth, est)
        return r is not None and r[0] >= -wcz and r[1] <= pozn
    a, b = 0.0, 0.25
    if ok(b):
        return '>= 25'
    for _ in range(18):
        m = (a + b) / 2
        a, b = (m, b) if ok(m) else (a, m)
    return f'{100 * a:.1f}'


def main():
    wcz, pozn = (float(sys.argv[1]), float(sys.argv[2])) if len(sys.argv) > 2 else (0.7, 1.7)
    print(f'Budzet prognozy: za wczesnie <= {wcz} st., za pozno <= {pozn} st.  (estymata E1)')
    print(f'{"wyprzedzenie":>12s} {"dth":>5s} | {"hamowanie":>10s} {"odwrocenie":>10s} {"przyspieszenie":>14s}   [% zmiany predkosci na obrot]')
    for a in (2.0, 15.0):
        dth = 30.0 - a
        wyn = [obwiednia(3000, r, dth, wcz, pozn) for r in ('hamowanie', 'odwrocenie', 'przyspieszenie')]
        print(f'{a:10.0f} st {dth:5.0f} | {wyn[0]:>10s} {wyn[1]:>10s} {wyn[2]:>14s}')
    # niezaleznosc od obrotow
    r15 = najgorszy(1500, 'hamowanie', 0.04, 28.0)
    r80 = najgorszy(8000, 'hamowanie', 0.04, 28.0)
    print(f'Kontrola: hamowanie 4 %/obrot, dth 28 st.: 1500 obr/min {r15[0]:.3f} st., 8000 obr/min {r80[0]:.3f} st.')
    # E0 porownawczo
    print('Bez korekty przyspieszenia (E0), dth 28 st.: hamowanie',
          obwiednia(3000, 'hamowanie', 28.0, wcz, pozn, est='E0'), '%, przyspieszenie',
          obwiednia(3000, 'przyspieszenie', 28.0, wcz, pozn, est='E0'), '%')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
