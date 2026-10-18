# Wynik triażu zapłonu — Beta 300 RR 2015

**Pomiar wykonany przez Pawła 15.10.2026.** Temperatura otoczenia 14 °C.

## Dane zmierzone

| Pozycja | Wartość |
|---|---|
| Przewody we wtyczce sterownika zapłonu | **8** |
| Uzwojenie pierwotne cewki, koniec 1 | **na stałe na masie/ramie** oraz do sterownika |
| Uzwojenie pierwotne cewki, koniec 2 | wprost do sterownika, przewód 0,5 mm² |
| Zasilanie na uzwojeniu pierwotnym bez kręcenia | **brak** |
| Rezystancja uzwojenia pierwotnego | **0,4 Ω** (zacisk cewki — masa) |
| Rezystancja uzwojenia wtórnego | **10,82 kΩ** (masa cewki — zacisk świecy) |
| Przewody wychodzące ze statora | **4**: dwa do regulatora z prostownikiem, dwa opisane jako „od cewki dla zapłonu" |

## Wniosek pewny: zapłon NIE jest indukcyjny

Decyduje sposób wpięcia, nie rezystancje. W układzie indukcyjnym uzwojenie pierwotne jest zasilane z akumulatora, a sterownik zwiera jego drugi koniec do masy. Tutaj **jeden koniec jest na stałe na masie**, drugi idzie wprost do sterownika, a zasilania nie ma nigdzie. To wpięcie kondensatorowe: cewka pracuje jako transformator impulsowy, nie jako magazyn energii.

Rezystancje są z tym zgodne — 0,4 Ω pierwotnego leży na samym dole zakresu, 10,82 kΩ wtórnego mieści się w typowym dla cewek CDI — ale same nie rozstrzygałyby, bo zakresy obu rodzin nachodzą na siebie.

**Skutki:** założenia **Z2** (czas ładowania 3 ms) i **Z12** (zapłon indukcyjny) **obalone**. Driver VBG08H-E wypada z projektu razem z architekturą czasu ładowania cewki, sufitem w rejestrze okresu HRTIM, pozycją 4,8 W w analizie termicznej i wnioskiem o konieczności obudowy aluminiowej.

## Rozstrzygnięcie: AC-CDI

| Pozycja | Dane |
|---|---|
| Sterownik zapłonu | Kokusan **026400001-000**, model **CU7542**, oznaczenie Beta **026400038 300** |
| Cewka zapłonowa | **RC01 IG5128**, data 14-08-22. Jeden zacisk uzwojenia pierwotnego, korpus na masie |
| Zasilanie sterownika | Również **+12 V z akumulatora** — logika sterownika, nie energia iskry |
| Przewody z silnika po stronie statora | **6**, na dwóch wtyczkach: **4 ze statora** (2 uzwojenie ładujące → regulator, 2 uzwojenie wzbudzające → sterownik zapłonu) oraz **2 pick-up** na osobnej wtyczce |
| 8 przewodów sterownika (rozkład wnioskowany, nie zmierzony pinami) | 2 uzwojenie wzbudzające, 2 pick-up, 1 cewka, 1 masa, 1 +12 V, 1 kill switch |

Trzy niezależne przesłanki za AC-CDI: wpięcie cewki (koniec na masie, impuls ze sterownika), **osobne uzwojenie w statorze** niezależne od ładującego i od pick-upu, oraz opis tego uzwojenia jako *source coil* przez firmy przewijające statory do Bety 250/300 RR 2015–2019.

Pomiary A, B i C z wcześniejszej wersji tego dokumentu nie są już potrzebne do rozstrzygnięcia topologii — rozstrzyga ją okablowanie.

**Decyzja 18.10.2026: MVP-A zachowuje topologię AC-CDI** z fabryczną cewką. Uzasadnienie i odrzucone alternatywy: `otwarte.md` O-001, `produkt.md` decyzja 2.9.

## Następny pomiar: uzwojenie wzbudzające względem GMP

Potrzebny do projektu bloku CDI i do potwierdzenia założenia Z14: kiedy w obrocie kondensator jest naładowany, jaką amplitudę daje uzwojenie przy kopnięciu i przy wysokich obrotach. Procedura: [`pomiar-wzbudzajacego.md`](pomiar-wzbudzajacego.md). Ta sama sesja daje fabryczną krzywą wyprzedzenia i położenie zbocza pick-upu względem iskry.
