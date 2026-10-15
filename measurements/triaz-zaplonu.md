# Triaż zapłonu — Beta 300 RR 2015

**Jedno pytanie: DC-CDI czy zapłon indukcyjny?**

Od odpowiedzi zależy, czy VBG08H-E zostaje w projekcie, czy cała architektura ładowania cewki, analiza termiczna i wybór obudowy idą do przeprojektowania. Potrzebny multimetr. 30 minut.

## Bezpieczeństwo

- Świeca **wykręcona i położona na masie silnika** albo nasadka zwarta do masy. Nigdy nie kręcić silnikiem z rozwartą nasadką — przebije izolację cewki.
- Nie trzymać przewodów cewki podczas kręcenia. **Wtórne napięcie CDI zabija.**
- Pomiary napięć przy kill switchu w pozycji RUN i bez kręcenia silnikiem, poza krokiem 5.

---

## Krok 1 — Spisz numery, zrób zdjęcia

| Co | Gdzie szukać |
|---|---|
| Numer na cewce zapłonowej | wytłoczony lub naklejka na korpusie |
| Numer na puszce zapłonu (CDI / power unit / igniter) | zwykle pod kierownicą, przy główce ramy albo pod siodłem |
| Liczba i kolory przewodów wchodzących do puszki | — |
| Czy puszka zapłonu i cewka to **dwa osobne elementy**, czy jeden moduł | — |

Prześlij zdjęcia i numery — sprawdzę je u producenta. Numer Kokusan sam w sobie rozstrzyga połowę pytania.

---

## Krok 2 — **Test decydujący: czy cewka ma stałe zasilanie +12 V**

Kill switch w RUN, silnik nie pracuje. Multimetr na napięcie stałe, czarna sonda na masę silnika lub ramy.

Dotykaj kolejno **każdego zacisku uzwojenia pierwotnego cewki** (nie puszki zapłonu — **pomiar musi być na cewce**).

| Wynik | Wniosek |
|---|---|
| Na jednym z zacisków **~12 V** | **Zapłon indukcyjny.** Cewka jest zasilana z akumulatora, a sterownik zwiera drugi zacisk do masy. VBG08H-E zostaje w projekcie |
| Na obu zaciskach **~0 V** | **DC-CDI.** Cewka nie ma zasilania — dostaje gotowy impuls wysokiego napięcia z puszki. **VBG08H-E nie nadaje się** |

To jest sedno triażu. Uwaga na jedną pułapkę: w układzie DC-CDI **puszka** jest zasilana z 12 V, więc na niej napięcie znajdziesz. Na samej cewce go nie ma.

---

## Krok 3 — Potwierdzenie: rezystancja zacisków pierwotnych do masy

Multimetr na rezystancję, silnik wyłączony, **odłącz złącze cewki** od wiązki.

| Wynik | Wniosek |
|---|---|
| Jeden zacisk pierwotny **zwarty do masy** (0–1 Ω) | Przesłanka za **CDI** |
| Oba zaciski **nie mają połączenia z masą** | Przesłanka za **indukcyjnym** |

---

## Krok 4 — Rezystancje cewki (potrzebne tak czy inaczej)

Zapisz, niezależnie od wyniku — będą potrzebne w pełnej sesji pomiarowej.

| Pomiar | Wartość |
|---|---|
| Pierwotne, między zaciskami | …… Ω |
| Wtórne, od zacisku do końcówki świecy | …… kΩ |
| Temperatura otoczenia przy pomiarze | …… °C |

**Sama rezystancja pierwotna nie rozstrzyga** — zakresy CDI i indukcyjnych nachodzą na siebie. Dlatego decyduje krok 2, a nie ta tabela.

---

## Krok 5 — Jeśli masz miernik z zakresem indukcyjności (opcjonalny, ale rozstrzygający)

Cewka odłączona od wiązki, pomiar na uzwojeniu pierwotnym.

| Indukcyjność pierwotna | Wniosek |
|---|---|
| poniżej ~0,5 mH (setki µH i mniej) | **CDI** |
| powyżej ~1,5 mH (jednostki mH) | **Indukcyjny** |

Różnica jest kilkudziesięciokrotna, więc wynik jest jednoznaczny. Jeśli miernik nie ma tego zakresu — pomiń, krok 2 wystarcza.

---

## Przy okazji, bez przyrządów

Skoro jesteś przy motocyklu, trzy rzeczy, które i tak będą potrzebne:

1. **Rozrusznik** — czy jest przekaźnik rozrusznika i gdzie? Przewód od przycisku idzie wprost do silnika rozrusznika, czy do cewki przekaźnika? *(Decyduje, czy nasz kanał mocy steruje silnikiem 7,5 A, czy cewką przekaźnika 0,2 A — zupełnie inne obciążenia.)*
2. **Bęben zmiany biegów** — czy czop bębna jest dostępny z zewnątrz pokrywy, czy wymagałby ingerencji w pokrywę? Zdjęcie pokrywy sprzęgła i pokrywy zmiany biegów.
3. **Stator** — ile przewodów wychodzi z silnika do regulatora i czy regulator jest osobnym elementem?

---

## Co zrobię z wynikiem

| Wynik kroku 2 | Co się dzieje |
|---|---|
| **Indukcyjny** | Założenie Z12 potwierdzone. VBG08H-E zostaje. Przechodzimy do pełnej sesji pomiarowej: parametry cewki, krzywa wyprzedzenia, VR względem GMP |
| **DC-CDI** | Założenie Z12 obalone. Zatrzymuję wszystko, co dotyczy ładowania cewki, i wracamy do decyzji: zachować topologię CDI i zaprojektować pod nią tor energii, albo przejść na zapłon indukcyjny z inną cewką. To decyzja produktowa, nie zapis do poprawienia |
