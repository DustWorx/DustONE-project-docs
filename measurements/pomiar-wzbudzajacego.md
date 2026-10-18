# Pomiar uzwojenia wzbudzającego, iskry i pick-upu — Beta 300 RR 2015

**Jedna sesja, trzy odpowiedzi:**

1. Amplituda i faza uzwojenia wzbudzającego względem obrotu — kiedy kondensator jest naładowany (założenie Z14, O-001)
2. Rzeczywisty moment iskry z fabrycznego CDI — **fabryczna krzywa wyprzedzenia**
3. Zbocze pick-upu względem iskry (O-005)

Pomiar na pracującym silniku z **fabrycznym CDI**, przez wkłucia w złącza. Nic nie jest rozłączane.

## Sprzęt

| Element | Uwagi |
|---|---|
| Rigol DHO804 | 4 kanały |
| 3× sonda FNIRSI P4100 (100:1, 2 kV) | CH1, CH2, CH3 |
| 1× standardowa sonda ×10 | CH4 |
| Igły do wkłuwania w złącza od tyłu, izolowane | Albo cienkie szpilki w koszulce termokurczliwej |
| Opaski zaciskowe | Do unieruchomienia przewodów sond |
| Multimetr | Krok 2 |

## Bezpieczeństwo

- **Na uzwojeniu wzbudzającym i na cewce są setki woltów.** Nie dotykać igieł, sond ani przewodów, gdy silnik pracuje. Podłączać i odłączać wyłącznie przy zgaszonym silniku.
- **Wszystkie krokodylki masy w jednym punkcie masy silnika.** Jeśli zasilacz Rigola ma bolec uziemienia, motocykl zostaje uziemiony przez ten punkt — dlatego **żadna ładowarka ani inne urządzenie z sieci nie może być podłączone do motocykla w trakcie pomiaru.**
- Oscyloskop jest uziemiony (zasilacz z bolcem + przewód uziemiający na zacisku obudowy) — **tak ma zostać**, nie odłączać uziemienia, żeby „odpłynąć” oscyloskop.
- Przed wpięciem pierwszego krokodylka: multimetr na napięcie (AC i DC) między masą silnika a zaciskiem uziemienia oscyloskopu — **ma być ~0 V**. Inny wynik oznacza, że motocykl ma jakieś połączenie z siecią; nie podłączać, najpierw znaleźć przyczynę.
- Kanały CH1–CH3 ustawione na **100X przed** podłączeniem.
- Przewody sond z dala od przewodu WN świecy i od wydechu, unieruchomione opaskami.
- Wysokie obroty: krótko, na rozgrzanym silniku, na luzie, według własnej oceny.

---

## Krok 1 — Sprawdzenie sond (przed wyjściem do motocykla)

1. Każdą P4100 podłączyć do wyjścia kalibracyjnego Rigola, kanał na 100X, wyregulować kompensację trymerem do prostokąta bez przerostów i zaokrągleń.
2. Każdą P4100 przyłożyć do zacisków akumulatora: odczyt **12–13 V**. Inny wynik = zła nastawa 100X albo uszkodzona sonda. **Nie przechodzić dalej bez tego.**

## Krok 2 — Identyfikacja przewodów (silnik zgaszony)

Na złączach między silnikiem a sterownikiem zapłonu zapisz **kolory** i zmierz rezystancje (złącze rozłączone tylko na czas tego kroku):

| Para | Rezystancja | Kolory |
|---|---|---|
| Uzwojenie wzbudzające (2 przewody statora do sterownika) | …… Ω | …… |
| Pick-up (osobna wtyczka) | …… Ω | …… |
| Każdy z przewodów powyżej względem masy silnika | …… (zwarty / izolowany) | — |

Ostatni wiersz rozstrzyga, czy uzwojenie wzbudzające i pick-up są pływające, czy mają jeden koniec na masie. Potrzebne do projektu wejść ECU.

Złącza z powrotem połączyć.

## Krok 3 — Podłączenie (silnik zgaszony)

| Kanał | Sonda | Punkt | Nastawa |
|---|---|---|---|
| CH1 | P4100, 100X | Przewód wzbudzającego A | 50 V/dz, DC |
| CH2 | P4100, 100X | Przewód wzbudzającego B | 50 V/dz, DC |
| CH3 | P4100, 100X | Zacisk uzwojenia pierwotnego cewki | 100 V/dz, DC |
| CH4 | ×10, 10X | Przewód pick-upu (ten, który nie jest na masie; jeśli oba izolowane — dowolny) | 2 V/dz, DC |
| MATH | CH1 − CH2 | Napięcie na uzwojeniu wzbudzającym | — |

**Wyzwalanie:** CH3, zbocze narastające, poziom ~50 V, tryb **Normal**. Impuls na cewce = moment iskry.

**Pamięć:** najdłuższa dostępna, tak żeby na ekranie były **co najmniej dwa pełne obroty**.

## Krok 4 — Punkty pomiarowe

W każdym punkcie: **zapisz przebieg do pliku CSV oraz zrzut ekranu.** Nazwa pliku = punkt pomiarowy.

| # | Stan | Podstawa czasu (orientacyjnie) | Uwagi |
|---|---|---|---|
| 1 | **Kopnięcie** | 50 ms/dz, tryb Single | Najważniejszy punkt. Jeśli silnik odpali — dobrze, zapis i tak się złapie |
| 2 | Kopnięcie, drugie podejście | jw. | Powtarzalność |
| 3 | Bieg jałowy, rozgrzany | 10 ms/dz | |
| 4 | ~3000 obr/min | 5 ms/dz | Obroty odczytasz z okresu impulsów na CH3 |
| 5 | ~5000 obr/min | 2 ms/dz | |
| 6 | ~7000 obr/min | 2 ms/dz | Krótko |
| 7 | Najwyższe, jakie uznasz za bezpieczne na luzie | 1 ms/dz | Krótko. Podaj, ile osiągnąłeś |

Jeśli wysokie napięcie wychodzi poza ekran — zwiększ V/dz na CH1–CH3 i powtórz zapis.

## Krok 5 — Instalacja ładowania (dodane 18.10.2026, obwiednia napięciowa)

**5a. Napięcie i tętnienia na akumulatorze.** Sonda ×10 na zacisku plus akumulatora, masa na minusie. Sprzężenie DC, potem AC. Zapis przy biegu jałowym, ~3000, ~5000, ~7000 obr/min, ze światłami włączonymi i wyłączonymi: napięcie średnie i tętnienia międzyszczytowe.

**5b. Napięcie jałowe uzwojenia ładującego — najgorszy przypadek awarii regulatora.** Silnik zgaszony: **odpiąć złącze regulatora od statora**. Sondy P4100 (100X) na obu przewodach uzwojenia ładującego względem masy, MATH = różnica. Krótko na biegu jałowym, ~5000 i najwyższych bezpiecznych obrotach. **Napięcie może przekroczyć 100 V** — te same zasady co przy uzwojeniu wzbudzającym. Motocykl pracuje wtedy na samym akumulatorze — krótko. Po pomiarze złącze regulatora z powrotem.

## Co z tego wyliczę

| Wielkość | Z czego | Do czego |
|---|---|---|
| Amplituda wzbudzającego w funkcji obrotów, szczególnie przy kopnięciu | MATH | Napięcie kondensatora, dobór elementów bloku CDI, Z14 |
| Okno kątowe ładowania kondensatora względem pick-upu | MATH vs CH4 | Czy nasza mapa wyprzedzenia mieści się w oknie, w którym kondensator jest naładowany |
| Kąt iskry względem pick-upu w funkcji obrotów | CH3 vs CH4 | **Fabryczna krzywa wyprzedzenia** — punkt startowy naszej mapy |
| Kształt i biegunowość sygnału pick-upu | CH4 | Weryfikacja ustawień MAX9926, O-005 |
| Kształt impulsu na pierwotnym cewki | CH3 | Napięcie i czas impulsu — wymagania dla tyrystora |
| Napięcie i tętnienia akumulatora | Krok 5a | Wymaganie odporności na tętnienia (×2 zmierzonych) |
| Napięcie jałowe uzwojenia ładującego | Krok 5b | Korekta wartości 35 V w SYS-ENV-009, dobór TVS |

**Prześlij:** pliki CSV, zrzuty ekranu, tabelę z kroku 2 i zdjęcie miejsca wpięcia sond.
