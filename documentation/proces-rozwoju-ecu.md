# Proces rozwoju produktu — ECU + HMI + Aplikacja Desktop (Offroad Motorsport)

## 0. Metryka dokumentu

| | |
|---|---|
| **Identyfikator** | DOC-001 |
| **Wersja** | **3.9** |
| **Status** | roboczy (przed bramką G0) |
| **Właściciel** | Paweł |
| **Opracowanie** | Claude |
| **Data wersji** | 2026-09-20 |
| **Dokument nadrzędny** | — (dokument główny projektu) |
| **Baseline** | brak — pierwszy baseline powstanie przy zamknięciu bramki G0 |

### 0.1 Historia zmian

| Wersja | Data | Zakres zmiany | Powód |
|---|---|---|---|
| 1.0 | ≤ 2026-08-30 | Struktura fazowa, Faza 0, Faza 1, pierwsza wersja Fazy 2-ECU i 2-HMI | Budowa procesu od zera. **Uwaga: zmiany z tego okresu nie były rejestrowane — historia odtworzona z dat w treści dokumentu** |
| 2.0 | 2026-08-31 | Architektura uśpienia B, budżet energetyczny i analiza termiczna (6.8, 7.2), wnioski o obudowie aluminiowej, wskaźnik biegu, okablowanie start/kill, rejestr luk L1–L29, Faza 2-FW jako osobna faza | Przegląd całości projektu, wykrycie luk funkcjonalnych i braku fazy specyfikacji firmware |
| 2.1 | 2026-09-12 | Bramki jakości G0–G5 (3.0), przeprojektowanie zasilania (6.2b), korekta drivera wtryskiwaczy na TLE9104SH, MCU na STM32G474VET3 (LQFP100), IMU na BMI090L, zasady procesu #10 i #11 | **Audyt zewnętrzny — werdykt NO-GO.** Realizacja planu naprawczego (`plan-naprawczy-audyt.md`), 36 pozycji |
| 2.3 | 2026-09-20 | Aktualizacja tabeli pokrycia po ustaleniach punktu B: ECU-IGN-005 domknięte sufitem sprzętowym z rejestru okresu HRTIM (zweryfikowane w CubeMX), ECU-IGN-002 z warunkiem generowania impulsu przez peryferium, ECU-SEN-007 z progami 3%/97%, T-SAF-003 rozbity na dwa warianty odblokowania | Praca nad punktem B specyfikacji firmware — klasyfikacja usterek i macierz usterek, grupy 1 i 2 |
| **2.2** | **2026-09-20** | Przebudowa tabeli pokrycia wymagań (rozdz. 14, z rozbiciem na 14.1–14.11), przebudowa rejestru ryzyk z właścicielami i dowodami zamknięcia (rozdz. 11), metryka i historia zmian (rozdz. 0), zasada procesu #13, luki L30–L32, korekta strat cieplnych 6,7 → 5,5 W w L16, usunięcie nieaktualnych odniesień do L9960 i BMI088 | Domknięcie pozycji audytu **F-012, F-029, F-033** — ostatnie pozycje naprawcze przed przejściem do punktu B specyfikacji firmware |

| 2.4 | 2026-09-20 | Nowe wiersze pokrycia dla ECU-PWR-009/010 i SYS-COM-005a/005b; aktualizacja bilansu (74 wymagania, 74 testy) | Macierz usterek grupa 3 — komunikacja i zasilanie; decyzje Pawła z 20.09.2026 |
| 2.5 | 2026-09-20 | **Wycofanie zmiany topologii zasilania MAX9926** w rozdz. 6.2b i 6.4 — powrót do zasilania przez przełącznik obciążenia; uściślenie poboru w rozdz. 6.4 z 2 mA na 4,7 mA typ. wg karty katalogowej | Karta katalogowa MAX9926: brak wejścia shutdown, pobór 4,7 mA typ. Propozycja była sprzeczna z ustaleniem już zapisanym w rozdz. 6.4 |

| 2.6 | 2026-09-22 | Komparator kill switcha w liście komponentów (6.2); wymóg wiązki z rezystorami w wymaganiach instalacyjnych (6.7); 6 nowych wierszy pokrycia i aktualizacja 3 istniejących; bilans 79 wymagań | Macierz usterek grupa 4 — bezpieczeństwo, autotest i pamięć; decyzje Pawła z 22.09.2026 |

| 2.7 | 2026-09-22 | Korekta bilansu pokrycia (94 zamiast zaniżonych 85 — skrypt kontrolny pomijał obszar UI); 10 nowych wierszy pokrycia (ECU-INJ-007, ECU-IGN-008, ECU-PWR-008a, ECU-SAF-011a/013/014, HMI-UI-006/007/008) i aktualizacja ECU-SAF-011; bilans 85 wymagań; nowa luka L33 — niezależny sygnał obciążenia dla wariantów TPI/TBI | Punkty B.3 i B.5 specyfikacji firmware; uwaga Pawła o zasilaniu MAX9926 z szyny 5 V |

| 2.8 | 2026-09-29 | **Zmiana decyzji 2.6** — czujnik quickshiftera z prętowego 0–5 V zamiast surowego tensometru; 6 nowych wierszy pokrycia (ECU-SEN-012/013, ECU-IGN-009/010/011, ECU-SAF-015); bilans 100 wymagań; **zamknięcie pozycji P0 quickshiftera w rozdz. 14.11** | Punkt B.6 specyfikacji firmware — wymagania quickshiftera |

| 2.9 | 2026-09-29 | Wejście czujnika sprzęgła: 4 nowe wiersze pokrycia (ECU-SEN-014/015, HMI-UI-009, SYS-COM-007); bilans 104 wymagania; dopisek do L2 (decyzja podtrzymana) i do L33 (pin przypadł czujnikowi sprzęgła); ostrzeżenie o przeliczeniu bilansu pinów w rozdz. 6.3 | Luka w warunkach dopuszczenia quickshiftera wykryta przez Pawła — żaden warunek nie sprawdzał intencji kierowcy |

| 3.0 | 2026-09-29 | Korekta HMI-UI-009 w tabeli pokrycia — wskazanie włączonego biegu wymaga także warunku puszczonego sprzęgła, więc realizacja obejmuje oba czujniki | Doprecyzowanie Pawła: ostrzegamy wyłącznie o stanie, w którym motocykl realnie może szarpnąć |

| 3.1 | 2026-09-29 | Poprawiony test T-SEN-015 — kryterium oparte na zmianach biegu; **dodany obowiązkowy test negatywny** (zjazd na wciśniętym sprzęgle bez zmiany biegu nie może zgłaszać usterki) | Fałszywy alarm wykryty przez Pawła: kryterium czasowe nie odróżniało kierowcy trzymającego sprzęgło od zwartego przełącznika |

| 3.2 | 2026-09-29 | **Nowe zasady procesu #14 i #15** — obowiązkowa analiza scenariuszy rzeczywistej jazdy i test negatywny dla każdego progu i automatycznego zadziałania; kryteria automatycznego zadziałania wymagają zatwierdzenia przez Pawła. Test T-SEN-015 sprowadzony do dwóch testów negatywnych, test pozytywny do zdefiniowania po wyborze wariantu | Trzy kolejne błędy w B.6 wykryte przez Pawła oraz zapisanie kryterium bez jego zgody |

| 3.3 | 2026-09-29 | **Quickshifter i czujnik sprzęgła usunięte z zakresu produktu.** Unieważniona decyzja 2.6; usuniętych 9 wierszy pokrycia; zapis zmiany zakresu w rozdz. 8; zaktualizowane L3, L31, L33, R18 i rozdz. 14.11; skorygowane listy funkcji, zakres kalibracji, ochrona wejść i lista sygnałów; bilans 95 wymagań. **Zwolnione dwa piny — luka L33 dostaje miejsce** | Decyzja Pawła: najgorszy stosunek złożoności do wartości, trzy kolejne błędy specyfikacji, niska realna wartość funkcji w terenie |

| 3.4 | 2026-09-29 | Zarejestrowane DOC-008 i DOC-009 — diagram bezpieczeństwa w dwóch arkuszach. **Punkt B specyfikacji firmware zamknięty** | Ostatnia pozycja punktu B; częściowe domknięcie pozycji audytu F-031 |

| 3.5 | 2026-09-29 | Dopisane ECU-SAF-016 i ECU-SAF-016a wraz z wierszami pokrycia; uzupełnione zasilanie komparatora w liście komponentów; DOC-008 pokazuje mechanizm wykrycia szyny 5 V i linię bramkującą | Pytanie Pawła o monitoring szyny 5 V ujawniło, że linia bramkująca EN nie była objęta żadnym wymaganiem stanu bezpiecznego |

| 3.6 | 2026-10-11 | 8 nowych wierszy pokrycia (ECU-IGN-012…019); bilans 105 wymagań | Punkt C.1 — trigger i synchronizacja na podstawie pomiarów koła impulsowego wykonanych przez Pawła |

| 3.7 | 2026-10-11 | **Aktualizacja statusów faz w rozdz. 3** — były nieaktualne w obie strony: Fazy 0 i 2-ECU nadal opisane jako „w naprawie” mimo zamknięcia wszystkich pozycji P0, Faza 1 bez uwzględnienia gotowego diagramu bezpieczeństwa, Faza 2-FW oznaczona jako „następna” mimo że punkty A, B i C.1 są zamknięte | Uwaga Pawła 11.10.2026 |

| 3.8 | 2026-10-11 | Zarejestrowany DOC-010 (dossier audytowe); **nowe luki L34–L40** wykryte przy przygotowaniu pakietu do audytu: brak repozytorium i kontroli wersji, rejestru założeń, standardu kodowania, kryteriów akceptacji wyrobu, oszacowania kosztu BOM, przypadków użycia oraz specyfikacji wariantów B/C | Przegląd całości projektu zlecony przez Pawła przed drugim audytem |

| **3.9** | **2026-10-11** | **Uzupełnienie luk przed drugim audytem.** Zasady procesu **#16** (repozytorium i kontrola wersji) i **#17** (standard kodowania, analiza statyczna, walidacja narzędzi); **rejestr założeń (rozdz. 11.2, 10 pozycji)**; **kryteria akceptacji wyrobu MVP-A (rozdz. 3.0a, A1–A12)**; **rozdz. 11.3 — skutki obalenia założenia Z1**. Korekta decyzji 2.7, usunięty wiersz pokrycia ECU-IGN-008, dodany ECU-IGN-020. L34–L37 rozwiązane, L38–L40 przeklasyfikowane na zaplanowane | Decyzja Pawła: uzupełnić realne braki przed audytem, resztę jawnie opisać jako pracę zaplanowaną |

### 0.2 Dokumenty projektu

| ID | Dokument | Wersja | Status | Właściciel |
|---|---|---|---|---|
| DOC-001 | `proces-rozwoju-ecu.md` — dokument główny | 3.9 | roboczy | Paweł |
| DOC-002 | `wymagania.md` — specyfikacja wymagań | 1.5 | roboczy | Paweł |
| DOC-003 | `architektura-systemu.mermaid` — diagram blokowy | 1.2 | roboczy | Claude |
| DOC-004 | `faza2-fw-specyfikacja.md` — specyfikacja firmware | 1.7 | roboczy (punkt A gotowy, B w toku — grupy 1–3 macierzy zamknięte, C–J otwarte) | Claude |
| DOC-005 | `przeglad-komponentow.md` — cykl życia i dostępność | 1.6 | roboczy | Paweł |
| DOC-006 | `plan-naprawczy-audyt.md` — plan naprawczy po pierwszym audycie | 1.7 | roboczy | Claude |
| **DOC-011** | `plan-naprawczy-audyt2.md` — plan naprawczy po audycie AUD-ECU-002, diagnoza wzorców pomijania, zakres zapożyczeń z automotive | **1.0** | roboczy — do realizacji | Paweł |
| **DOC-010** | `dossier-audytowe.md` — pakiet wejściowy do audytu zewnętrznego | **1.1** | wydany | Paweł |
| **DOC-008** | `diagram-bezpieczenstwa.mermaid` — łańcuch odcięcia zapłonu i wtrysku | 1.2 | roboczy | Claude |
| **DOC-009** | `diagram-zatrzask.mermaid` — zatrzask, odblokowanie, licznik resetów | 1.0 | roboczy | Claude |
| DOC-007 | `faza3-specyfikacja-fw.md` | 0.1 | **nieaktualny** — do napisania od nowa po zamknięciu Fazy 2-FW | Claude |

Zasady wersjonowania i statusów — zasada procesu #13 (rozdz. 2).

---

## 1. Zespół i podział ról

| Rola | Kto | Zakres |
|---|---|---|
| Inżynier-pomysłodawca / integrator HW | Paweł | Decyzje produktowe, budowa fizyczna, montaż, testy, dostawcy, budżet |
| Inżynier produktu / architekt | Chat (Claude) | Wymagania, architektura, specyfikacje, przegląd decyzji, dokumentacja |
| Inżynier firmware/software | Claude Code | Implementacja FW (ECU, HMI) i aplikacji desktop wg zatwierdzonych specyfikacji |

---

## 2. Zasady procesu

1. Pracujemy fazami. Każda faza ma **deliverable** i **bramkę wyjścia** — nie przechodzimy dalej, dopóki bramka nie jest zamknięta.
2. Każda istotna decyzja trafia do rejestru decyzji danej fazy.
3. ECU jest komponentem wiodącym — HMI i aplikacja desktop projektowane względem interfejsów ECU.
4. Zmiana zakresu = świadoma decyzja zapisana w rejestrze, nie przypadkowy dryf.
5. **Dobór komponentów:** każdy istotny komponent (MCU, układy scalone, czujniki, złącza, pamięci) jest konsultowany — Claude proponuje z uzasadnieniem i alternatywą, Paweł decyduje. Samodzielnie dobierane są wyłącznie elementy bierne (R, C).
6. Nic nie trafia do implementacji (Claude Code) bez zatwierdzonej specyfikacji.
7. **Wersjonowanie i zgodność (dodane 2026-08-31):** firmware ECU, firmware HMI i aplikacja desktop mają numery wersji w schemacie `major.minor.patch`. Zmiana protokołu komunikacji lub formatu danych = zmiana `major`. ECU przy starcie sprawdza zgodność wersji z HMI i sygnalizuje niezgodność; aplikacja desktop weryfikuje zgodność przed połączeniem. Szczegóły mechanizmu — Faza 2-FW (punkt H).
8. **Śledzenie pokrycia wymagań (dodane 2026-08-31):** każde wymaganie funkcjonalne z Fazy 0 musi mieć przypisaną implementację (specyfikacja FW / komponent HW) i test weryfikujący (plan testów z Fazy 3). Tabela pokrycia — rozdz. 14.
9. **Plan testów (decyzja 2026-08-31):** powstaje w Fazie 3, przed pierwszymi testami logiki, i jest rozszerzany w każdej kolejnej fazie o zakres właściwy dla tej fazy (6 — bring-up, 8 — integracja na silniku, 9 — teren).
10. **Dostawcy i status komponentów (decyzja 12.09.2026):** dostępność sprawdzana w kolejności **TME → Mouser → Farnell → DigiKey**, ze wskazaniem źródła przy każdej rekomendacji. Każdy komponent musi mieć **pełny numer katalogowy (OPN)** i **potwierdzony aktywny status cyklu życia** — komponenty oznaczone NRND (Not Recommended for New Designs) są odrzucane niezależnie od dopasowania funkcjonalnego. Zasada wprowadzona po odrzuceniu TLE8104E z tego powodu (pozycja audytu F-032).
11. **Kryteria audytowe w fazach (decyzja 12.09.2026):** uwagi audytu zewnętrznego dotyczące faz jeszcze nierozpoczętych nie są traktowane jako osobna lista naprawcza, lecz **wchodzą jako kryteria akceptacji tych faz**. Podział: pozycja opisująca zapis nieprawdziwy lub błędny wybór = naprawa teraz; pozycja opisująca brak w fazie, do której nie doszliśmy = normalna praca z kryteriami audytu. Egzekwowane bramkami G0-G5 (rozdz. 3.0).
12. **Bootloader i odzysk (decyzja 2026-08-31):** dwubankowy — jedna kopia firmware aktywna, druga jako obszar aktualizacji. Przełączenie na nową wersję dopiero po weryfikacji poprawności; przerwana lub uszkodzona aktualizacja skutkuje automatycznym powrotem do poprzedniej działającej wersji. Dotyczy ECU i HMI. Realizowalne bez dodatkowego sprzętu — STM32G474 (512 KB) i STM32G0B1 (512 KB) mają sprzętowe wsparcie dwubankowej pamięci Flash.
13. **Zarządzanie wersjami dokumentów (decyzja 20.09.2026, audyt F-033):** każdy dokument projektu ma **metrykę** (identyfikator, wersja, właściciel, status, data) i **historię zmian**. Wersjonowanie `major.minor`: `minor` — uzupełnienie lub korekta bez zmiany ustaleń; `major` — zmiana ustalenia, zakresu lub decyzji technicznej. **Baseline** to wersja zamrożona w chwili przejścia bramki — od tego momentu zmiana treści wymaga wpisu w historii zmian z podaniem powodu. Status dokumentu: `roboczy` · `w przeglądzie` · `baseline Gx` · `nieaktualny`.

14. **Analiza scenariuszy rzeczywistej jazdy (decyzja 29.09.2026):** każde wymaganie zawierające **próg czasowy, warunek automatycznego zadziałania lub kryterium wykrycia usterki** wymaga, **przed zapisaniem**, wypisania scenariuszy rzeczywistej jazdy i pracy, w których warunek może zostać spełniony bez faktycznej usterki. Minimalny zakres do przejścia: zjazd i podjazd, jazda z wciśniętym sprzęgłem, przerwy w jeździe, postój z włączonym biegiem, pokonywanie przeszkód, seria szybkich zmian biegów, jazda w skrajnych temperaturach, rozruch i gaszenie. **Każde takie wymaganie dostaje test negatywny** — dowód, że nie zadziała fałszywie — obok testu pozytywnego. Zasada wprowadzona po trzech kolejnych błędach w punkcie B.6, w których kryterium przechodziło każdy test pozytywny i zawodziło w normalnej jazdzie: quickshifter cinający przy użyciu sprzęgła, wskazanie biegu bez warunku sprzęgła, dwa kolejne błędne kryteria wykrycia zwartego czujnika sprzęgła. **Wspólny mianownik wszystkich trzech: sprawdzałem, czy mechanizm działa, a nie czy nie działa wtedy, kiedy nie powinien.**

15. **Kryteria automatycznego zadziałania wymagają zatwierdzenia (decyzja 29.09.2026):** próg, czas i warunek każdego automatycznego działania ECU są **przedstawiane jako propozycja z uzasadnieniem i scenariuszami negatywnymi**, nie zapisywane jako ustalenie. Zasada doprecyzowuje zasadę #5, która dotyczyła doboru komponentów — ta sama reguła obowiązuje dla nastaw i kryteriów w firmware. Wprowadzona po tym, jak kryterium wykrycia zwartego czujnika sprzęgła zostało wpisane do dokumentów bez zgody Pawła.

16. **Repozytorium i kontrola wersji (decyzja 11.10.2026, luka L34):** wszystkie dokumenty projektu i cały kod są przechowywane w repozytorium z historią zmian. Metryka w dokumencie opisuje **co** się zmieniło, repozytorium zapewnia **możliwość odtworzenia** dowolnej wcześniejszej wersji — zasada #13 bez tego mechanizmu była zasadą bez pokrycia. **Baseline przy bramce jest znacznikiem w repozytorium**, nie tylko wpisem w tabeli. Zasada wprowadzona po tym, jak część pracy przepadła przy awarii środowiska i trzeba było odtwarzać ją z logu sesji.

17. **Standard kodowania i kontrola jakości kodu (decyzja 11.10.2026, luka L36):** przed rozpoczęciem implementacji ustalane są: standard kodowania, narzędzie analizy statycznej uruchamiane przy każdej zmianie, minimalne pokrycie testami jednostkowymi dla modułów sterujących zapłonem i wtryskiem oraz dla warstwy bezpieczeństwa, a także wersje i konfiguracja narzędzi budowania. **Firmware sterujący zapłonem silnika spalinowego nie powstaje bez tych ustaleń.** Konkretne wybory należą do Fazy 2-FW punkt I lub do osobnego dokumentu przed Fazą 5.

---

## 3. Struktura fazowa i status

| Faza | Zakres | Status |
|---|---|---|
| 0 | Wymagania (ECU + HMI + Desktop) | ⬜ **OTWARTA** — naprawa po audycie zakończona (`wymagania.md`, 105 wymagań z pełnym pokryciem). **Bramka G0 zablokowana** pozycjami `[DO USTALENIA]` oraz brakiem wymagań bootloadera (rozdz. 14.11) |
| 1 | Architektura systemu | ⚠️ **WARUNKOWO** — diagram bezpieczeństwa gotowy 29.09.2026 (DOC-008, DOC-009). Pozostaje **diagram elektryczny** (Faza 4) i przegląd diagramu funkcjonalnego względem kryteriów audytu |
| 2-ECU | Projekt szczegółowy HW: ECU | ⚠️ **WARUNKOWO** — wszystkie błędy P0 z audytu usunięte. Pozostaje dobór konkretnych przetwornic, komparatora kill switcha i potwierdzenie dostępności BOM (Faza 4, pozycja F-032) |
| 2-HMI | Projekt szczegółowy HW: HMI | ⚠️ **WARUNKOWO** — bez zmian: brak drzewa zasilania, analizy najgorszego przypadku drabinki przycisków i pełnego OPN pamięci flash |
| **2-FW** | **Specyfikacja funkcjonalna firmware** (stany, tryby awaryjne, mapy, diagnostyka, bezpieczeństwo) | 🔶 **W TOKU** — punkt A zamknięty, **punkt B zamknięty** (42 kody DTC), **C.1 zamknięty** (trigger i synchronizacja). Otwarte: reszta C, D–J |
| 2-Desktop | Projekt szczegółowy: aplikacja desktop + protokół komunikacji | ⬜ |
| 3 | Prototyp funkcjonalny — **wyłącznie płytki dev, sygnały symulowane, bez motocykla** | ⬜ |
| 4 | Projekt PCB (ECU + HMI) + wytyczne EMI | ⬜ |
| 5 | Firmware finalny (pełen zakres) | ⬜ |
| 6 | Montaż fizyczny ECU i HMI na realnym PCB, bring-up | ⬜ |
| 7 | Aplikacja desktop — implementacja finalna | ⬜ |
| 8 | Integracja + **pierwsze testy na motocyklu (Beta 300RR)** | ⬜ |
| 9 | Walidacja terenowa | ⬜ |
| 10 | Iteracja (rev B) | ⬜ |
| 11 | Przygotowanie do małoseryjnej produkcji (DFM) | ⬜ |
| 12 | Pilotaż / mała seria | ⬜ |
| 13 | Sprzedaż i wsparcie posprzedażowe | ⬜ |

### 3.0 Bramki jakości (wprowadzone 12.09.2026 po audycie zewnętrznym)

Nadrzędne wobec bramek poszczególnych faz. **Jedna otwarta pozycja P0 lub jedna otwarta pozycja bezpieczeństwa oznacza NO-GO**, niezależnie od tego, czy pochodzi z listy naprawczej, czy z normalnej pracy w fazie.

| Bramka | Warunek GO | Powiązane pozycje audytu |
|---|---|---|
| **G0 — Wymagania** | MVP zamrożony, wymagania z identyfikatorami i kryteriami akceptacji, założenia zgodności regulacyjnej | F-007 ✅, F-011, F-012, F-027 |
| **G1 — Architektura** | Zasilanie, bezpieczeństwo, wejścia/wyjścia, protokoły i warianty spójne | F-002 ✅, F-003 ✅, F-004 ✅, F-005 ✅, F-006 ✅, F-010, F-031, F-034 |
| **G2 — Projekt szczegółowy** | Schemat, macierz pinów i DMA, BOM z pełnymi numerami, analiza najgorszego przypadku, wiązka, przegląd FMEA | F-001 ✅, F-009, F-014…F-018, F-025, F-026, F-028, F-030, F-032 |
| **G3 — Implementacja FW** | Sekcje A-J kompletne, interfejsy zamrożone, testy zdefiniowane | F-008, F-013, F-020, F-021, F-022, F-023, F-036 |
| **G4 — Wydanie PCB** | ERC, przegląd projektu, testowalność, termika, lista kontrolna EMC | F-024, F-035 |
| **G5 — Pojazd** | Testy wstrzykiwania usterek i stanu bezpiecznego zaliczone | — |

Pełny rejestr i podział na naprawę/pracę procesową: `plan-naprawczy-audyt.md` rozdz. 7.

### 3.0a Kryteria akceptacji wyrobu MVP-A (propozycja, 11.10.2026, luka L37)

**Bramki G0–G5 opisują fazy, nie wyrób.** Dotąd nie było zapisane, co znaczy „MVP-A gotowe". Poniższe kryteria są **propozycją do zatwierdzenia przez Pawła** — dopóki nie zostaną zatwierdzone, pozostają wskazówką, nie zobowiązaniem.

Wyrób uznaje się za gotowy, gdy **wszystkie** poniższe są spełnione i udokumentowane:

| # | Kryterium | Wartość | Dowód |
|---|---|---|---|
| A1 | Rozruch kickstarterem na zimnym silniku | ≤ 3 kopnięcia, 10 prób z rzędu | Protokół z Fazy 8 |
| A2 | Rozruch kickstarterem na rozgrzanym silniku | ≤ 2 kopnięcia, 10 prób | jw. |
| A3 | Praca ciągła w całym zakresie obrotów bez przerw w zapłonie | 800–10 000 obr/min | Rejestracja przerw w zapłonie |
| A4 | Dokładność momentu zapłonu | wg ECU-IGN-002 | **T-IGN-002** |
| A5 | Każdy mechanizm klasy K4 zweryfikowany wstrzykiwaniem usterki | 100% pozycji | Protokoły T-SAF-* |
| A6 | Pobór prądu w uśpieniu | ECU ≤ 150 µA, zestaw ≤ 250 µA | T-PWR-001, T-PWR-002 |
| A7 | Przejazd terenowy bez usterki krytycznej i bez fałszywego odcięcia | **10 godzin** pracy silnika w terenie | Log czarnej skrzynki + rejestr zdarzeń |
| A8 | Temperatura wewnątrz obudów w granicach klas komponentów | pomiar w warunkach letnich | Protokół termiczny Fazy 9 |
| A9 | Czytelność wyświetlacza w pełnym słońcu | wg HMI-UI-005 | T-UI-005 |
| A10 | Pełny cykl: strojenie mapy, zapis, aktualizacja firmware ECU i HMI, powrót do pracy | bez utraty spójności danych | T-COM-005b, T-COM-006 |
| A11 | Pozycje P0 otwarte | **zero** | Rejestr pozycji audytu |
| A12 | Ryzyka o wpływie wysokim | zamknięte dowodem albo **świadomie zaakceptowane na piśmie** | Rejestr ryzyk rozdz. 11 |

**A7 jest kryterium najtrudniejszym i celowo takim pozostaje.** Dziesięć godzin realnej jazdy w terenie wyłapie to, czego nie wyłapie żadne stanowisko: zakłócenia, wibracje, błoto, temperaturę, zachowanie kierowcy. Jeśli któregokolwiek z pozostałych kryteriów nie da się zmierzyć przed A7, znaczy to, że A7 przyszło za wcześnie.

---

### 3.1 Deliverable i bramki wyjścia

| Faza | Deliverable | Bramka wyjścia |
|---|---|---|
| 2-FW | **Specyfikacja funkcjonalna firmware** (rozdz. 3.2). **Kryteria z audytu:** macierz usterek z reakcją, wartością zastępczą i testem (F-023); specyfikacja triggera — geometria koła, offset TDC, blanking, dropout, resync, jitter (F-013); bilans pamięci i zapis atomowy (F-020); pełna strategia aktualizacji z manifestem, podpisem i wycofaniem (F-021); budżety czasu rzeczywistego — WCET, deadline, NVIC/DMA, przeciążenie (F-022); kalibracja z obsługą i odzyskiem (F-036) | Sekcje A-J bez zapisów „do opracowania" w zakresie MVP; każda z kryteriami testu. **Bramka G3** |
| 2-Desktop | Architektura aplikacji (.NET/WPF), model danych, **specyfikacja protokołu komunikacji** (F-010), słownik danych z jednostkami i zakresami (F-034). **Kryteria z audytu:** dla CAN — bitrate, lista identyfikatorów, kierunek, skalowanie, okresy, timeouty, licznik sekwencyjny, suma kontrolna, heartbeat, obsługa bus-off, sekwencja wybudzania, wersja protokołu. Dla USB — klasa, endpointy, framing, transakcyjny zapis (rozpocznij→zweryfikuj→zatwierdź/odrzuć), whitelist parametrów live tuningu, format logów, aktualizacja z odzyskiem po zaniku zasilania, diagnostyka DTC | Zatwierdzona architektura, protokół i słownik danych. **Bramka G1** |
| 3 | **Weryfikacja logiki sterowania** na płytkach dev (NUCLEO-G474RE + stanowisko HMI): timing zapłonu/wtrysku, odczyt czujników, komunikacja CAN, wyświetlanie na HMI. **Wyłącznie sygnały symulowane**. Dodatkowo: **plan testów** (co i jak weryfikujemy w fazach 3, 6, 8, 9) | Logika potwierdzona oscyloskopem/analizatorem; zatwierdzony plan testów |
| 4 | Schemat + netlista + BOM z pełnymi numerami i statusem cyklu życia (F-030, F-032) + layout PCB, wytyczne EMI, punkty testowe i serializacja (F-035). **Kryteria z audytu:** tory czujnikowe z analizą najgorszego przypadku (F-015); wiązka — bezpiecznik przy akumulatorze, przekroje, masy, ekranowanie (F-016); profil transjentów i weryfikacja energetyczna zabezpieczeń (F-017); budżet prądu spoczynkowego z tolerancjami (F-018); analiza drabinki przycisków (F-025); **wstępna macierz regulacyjna EMC/RoHS/WEEE/GPSR przed layoutem** (F-028) | Płytki wyprodukowane. **Bramki G2 i G4** |
| 5 | **Firmware produkcyjny** — rozszerzenie kodu z Fazy 3 o funkcje niedostępne na płytkach dev: sterowanie PROFET, IMU/czarna skrzynka, tryb uśpienia z wybudzaniem, bootloader USB, diagnostyka, RTC/motogodziny, przełączanie map, interlocki live tuningu | Firmware kompletny, przetestowany na stanowisku |
| 6 | Zmontowane (obsadzone) płytki ECU i HMI, bring-up, wgrany FW z Fazy 5, testy elektryczne bez motocykla | Obie płytki uruchomione, FW działa na realnym sprzęcie |
| 7 | Pełna aplikacja desktop połączona z realnym ECU | Wszystkie funkcje aplikacji działają z fizycznym ECU |
| 8 | Montaż na Becie 300RR, raport testów ECU-HMI-Desktop na silniku | Silnik pracuje pod kontrolą ECU, wszystkie funkcje zweryfikowane |
| 9 | Testy terenowe (offroad, warunki docelowe), lista usterek | Raport z jazd + priorytetyzowana lista poprawek |
| 10 | Poprawiony HW/FW/SW (rev B) | Poprawki wdrożone i zweryfikowane |
| 11 | Dokumentacja produkcyjna (DFM), wybrani dostawcy i montaż kontraktowy, **weryfikacja obowiązków CE/EMC/RoHS/WEEE**, **dokumentacja użytkownika** (instrukcja montażu, instrukcja obsługi, schemat wiązki, wymagania instalacyjne, **ostrzeżenie o braku blokady rozrusznika na biegu — decyzja L2**) | Gotowość do zamówienia serii |
| 12 | Pierwsza partia, testy jakościowe serii | Partia wyprodukowana i przetestowana |
| 13 | Kanał dystrybucji, wsparcie techniczne, proces aktualizacji FW, obsługa gwarancji | Produkt w sprzedaży z działającym wsparciem |

**Rozgraniczenie Faza 3 vs Faza 5:** Faza 3 dowodzi, że **logika sterowania jest poprawna** (można to zrobić na płytce dev). Faza 5 dokłada wszystko, czego na płytce dev sprawdzić się nie da, bo wymaga docelowego sprzętu (drivery mocy, zarządzanie zasilaniem, bootloader). Kod z Fazy 3 nie jest wyrzucany — jest rozszerzany.

**Kluczowa zasada kolejności (decyzja 2026-08-31):** pełny dobór HW dla ECU i HMI oraz projekt aplikacji desktop następują **przed** jakimkolwiek prototypowaniem. Testy na prawdziwym motocyklu dopiero od Fazy 8, na wyprodukowanym PCB. Powód: (a) całościowe planowanie ogranicza przeróbki, (b) płytki deweloperskie nie mają zabezpieczeń przepięciowych — podłączenie do pracującego silnika grozi uszkodzeniem.

### 3.2 Faza 2-FW — Specyfikacja funkcjonalna firmware (NOWA, dodana 2026-08-31)

Faza dodana po audycie: proces wymagał zatwierdzonej specyfikacji przed implementacją (zasada #6), ale nie zawierał fazy, która by ją tworzyła. Bez tego Claude Code implementowałby na podstawie rozproszonych notatek.

**Zakres do ustalenia w tej fazie:**

**A. Maszyna stanów ECU**
- Stany: uśpienie → wybudzanie → gotowość → rozruch (cranking) → praca → zatrzymywanie → awaria
- Warunki i czasy przejść między stanami
- Zachowanie wyjść w każdym stanie

**B. Bezpieczeństwo i tryby awaryjne**
- Sprzętowe i programowe odcięcie zapłonu (kill switch, IMU/wywrotka, rev limiter)
- Limp-home: wartości zastępcze przy uszkodzonym czujniku, ograniczona praca
- Reakcja na przegrzanie: progi, ostrzeżenie, ewentualna redukcja mocy
- Reakcja na niskie napięcie akumulatora
- Interlocki live tuningu (ryzyko R1)
- Zachowanie po resecie watchdoga

**C. Strategie sterowania silnikiem**
- Rozruch: osobna mapa/strategia dla niskich obrotów przy kręceniu
- Rozgrzewanie: wzbogacenie mieszanki wg temperatury
- Praca normalna: mapa zapłonu (RPM × TPS), mapa wtrysku, korekty (temperatura powietrza/cieczy, ciśnienie atmosferyczne, napięcie akumulatora)
- Odcięcie paliwa przy zamkniętej przepustnicy (overrun)
- Rev limiter: metoda (odcięcie zapłonu / paliwa / opóźnienie), histereza

**D. Struktura danych i map**
- Wymiarowość map, liczba punktów, metoda interpolacji
- Zestaw parametrów konfiguracyjnych (per model motocykla)
- Profile: ile map przełączanych z HMI, co dokładnie zmieniają
- Organizacja pamięci flash: mapy, konfiguracja, logi, motogodziny — z uwzględnieniem zużycia komórek (wear leveling)

**E. Diagnostyka**
- Lista wykrywanych błędów i ich kody
- Sposób przechowywania (historia, znaczniki czasu z RTC)
- Sygnalizacja: HMI, ewentualna dioda na ECU, aplikacja desktop

**F. Czarna skrzynka**
- Warunki wyzwolenia (progi IMU)
- Zakres zapisywanych danych i okno czasowe (przed/po zdarzeniu)
- Zapewnienie dokończenia zapisu

**G. Kalibracja**
- Procedury: TPS (min/max), czujnik biegu (pozycje), koło impulsowe (offset względem TDC)
- Gdzie inicjowane (aplikacja desktop / HMI) i jak przechowywane

**H. Bootloader i aktualizacja**
- Mechanizm aktualizacji ECU i HMI (przez USB, HMI przez ECU jako gateway)
- Odporność na przerwanie: recovery, weryfikacja integralności
- Kontrola zgodności wersji FW ECU ↔ FW HMI ↔ aplikacja desktop

**I. Architektura zadań czasu rzeczywistego**
- Priorytety przerwań, budżet czasowy, obsługa watchdoga okienkowego
- Rozdział zadań: rdzeń real-time vs. zadania tła

**J. Firmware HMI**
- Maszyna stanów, struktura menu, obsługa drabinki przycisków
- Zachowanie przy utracie komunikacji z ECU
- Format konfiguracji wyglądu z aplikacji desktop

**Bramka wyjścia:** zatwierdzony dokument specyfikacji FW, wystarczający do przekazania Claude Code bez dopytywania o decyzje projektowe.

---

## 4. Faza 0 — Wymagania (ZAMKNIĘTA)

### 4.1 Zakres produktu

**ECU:** uniwersalna platforma. **Zakres docelowy: wyłącznie silniki 1-cylindrowe (2T i 4T) motocykli enduro.** MVP = 1 cyl. 2T.

Obsługiwane układy paliwowe (KTM / Husqvarna / GasGas — wspólna platforma silnikowa — oraz Beta):
- **Gaźnik** — ECU steruje zapłonem i rev limiterem (bez sterowania mieszanką)
- **TPI** (Transfer Port Injection) — zapłon + 2 wtryskiwacze do kanałów przepłukujących
- **TBI** (Throttle Body Injection) — zapłon + 1 wtryskiwacz w gardzieli

Funkcje: zapłon, wtrysk, rev limiter, wskaźnik biegu, **prędkościomierz i licznik kilometrów** (fabryczny czujnik prędkości koła), **licznik motogodzin** (interwały serwisowe), **przełączanie map z HMI** (np. mokro/sucho/ekonomiczna), **zegar czasu rzeczywistego** (znaczniki czasu w logach), detekcja wypadku + czarna skrzynka, sterowanie wentylatorem / rozrusznikiem / światłami / pompą paliwa, korekta na wysokość n.p.m., **tryb uśpienia z wybudzaniem** (motocykle enduro nie mają stacyjki — ECU stale zasilane).

**HMI:** wyświetlacz z animacjami, 4 przyciski fizyczne na kierownicy, obudowa IP67+, wygląd konfigurowalny z aplikacji desktop.

**Aplikacja desktop (Windows):** edycja map offline, live tuning, data logging, aktualizacja FW (ECU + HMI), diagnostyka/kody błędów, konfigurator wyglądu HMI. Połączenie USB.

### 4.2 Rejestr decyzji Fazy 0

| # | Decyzja | Wybór | Uzasadnienie |
|---|---|---|---|
| 0.1 | Model produktu | Uniwersalna platforma dla wielu modeli | Rynek: entuzjaści, zawodnicy, zespoły motorsport |
| 0.2 | Zakres silników | **Wyłącznie 1-cylindrowe (2T i 4T) enduro.** Silniki 2-cylindrowe i ride-by-wire odrzucone | Redukcja ryzyka — RBW to osobna kategoria inżynierska (redundantne czujniki, failsafe) |
| 0.3 | MVP | 1 cyl., 2T | 2T i 4T wymagają różnej synchronizacji; zawężenie skraca drogę do prototypu |
| 0.4 | Sterowanie HMI | Przyciski fizyczne (nie dotyk) | Rękawice, błoto |
| 0.5 | Obudowy | IP67+ | Błoto, przeprawy wodne, wibracje |
| 0.6 | Power valve | Nie w MVP; zarezerwowany kanał aux | Silniki enduro (w odróżnieniu od MX) mają power valve mechaniczny, nie elektroniczny |
| 0.7 | Połączenie desktop↔ECU | USB przewodowo | Stabilność, brak problemów z parowaniem/zasięgiem |
| 0.8 | Smarowanie TPI/TBI | Fabryczna pompka olejowa usuwana, silnik na premiksie | Uproszczenie instalacji |
| 0.9 | Budżet BOM | ECU ~100–150 USD; **HMI zrewidowany na ~90–120 USD** (pierwotnie 40–65, zmiana po wyborze wyświetlacza EVE) | Benchmark konkurencji (Vortex, Ignitech, Athena GET) |
| 0.10 | Detekcja wypadku | Pełne IMU + czarna skrzynka (log zdarzeń) | Precyzja > prosty przełącznik przechyłowy |
| 0.11 | Wskaźnik biegu | Czujnik kąta na bębnie zmiany biegów (koncepcja z OEM KTM, własna implementacja) | Prawdziwa pozycja biegu zamiast wyliczania z prędkości |

**Flaga ryzyka (do Fazy 5):** live tuning na pracującym silniku wymaga interlocków w FW (limit skoku parametru, blokada zmian krytycznych powyżej progu RPM) — inaczej ryzyko uszkodzenia silnika.

---

## 5. Faza 1 — Architektura systemu (ZAMKNIĘTA)

Diagram blokowy: `architektura-systemu.mermaid`

| # | Decyzja | Wybór | Uzasadnienie |
|---|---|---|---|
| 1.1 | MCU ECU | STM32G474 | HRTIM <1ns, wbudowany FDCAN, dobre ADC, zapas na rozbudowę |
| 1.2 | Magistrala ECU↔HMI | CAN bus | Odporność na EMI/wibracje, standard motorsportowy |
| 1.3 | Topologia | Desktop →USB→ ECU (gateway) →CAN→ HMI | Jeden kabel do całego systemu |
| 1.4 | Logowanie | On-board (teren) + live przez USB (stanowisko) | Rider nie ma laptopa w trakcie jazdy |
| 1.5 | Nośnik logów | Wlutowana flash SPI NOR (bez karty microSD) | Slot karty = punkt awarii (błoto, wibracje) |
| 1.6 | Architektura FW | Rdzeń real-time na przerwaniach timerów (zapłon/wtrysk) odseparowany od reszty (komunikacja, logi, tuning) | Priorytet precyzji timingu niezależnie od obciążenia |
| 1.7 | Platforma desktop | Windows only | Największy udział w garażach motorsport |
| 1.8 | Framework desktop | .NET (C#) / WPF | Wydajne wykresy real-time, prosty instalator |

---

## 6. Faza 2-ECU — Projekt szczegółowy HW

### 6.1 Decyzje architektoniczne

| # | Decyzja | Wybór | Uzasadnienie |
|---|---|---|---|
| 2.1 | Zasilanie | Tylko motocykle z akumulatorem 12V | Eliminuje obsługę surowego AC ze statora (klasyczne CDI) |
| 2.2 | Standalone | Tak — bez fabrycznej wiązki | Uniwersalność między markami |
| 2.3 | Architektura PCB | Jedna uniwersalna płytka, tryb pracy wybierany programowo | Jeden BOM, jedna płytka zamiast wariantów |
| 2.4 | Wejście trigger | **Dwie ścieżki wybierane zworką na PCB:** (a) VR → MAX9926 → MCU, (b) Hall → ochrona + konfigurowalny rezystor podciągający → bezpośrednio wejście cyfrowe MCU. **Doprecyzowanie 2026-08-31:** MAX9926 obsługuje wyłącznie czujniki VR; Hall daje gotowy sygnał cyfrowy i nie wymaga kondycjonowania. Zworka ustawiana raz przy instalacji; dostęp wewnątrz obudowy (tej samej, która musi być otwieralna dla złącza SWD). Zasilanie czujnika Halla z linii +5 V ref, masa z masy analogowej - bez dodatkowych pinów |
| 2.5 | Synchronizacja fazy (4T) | Domyślnie batch (tylko wał korbowy); opcjonalne wejście czujnika fazy | Nie wszystkie 1-cyl. 4T mają dostępny czujnik fazy |
| ~~2.6~~ | ~~Quickshifter~~ | **DECYZJA UNIEWAŻNIONA 29.09.2026 — funkcja usunięta z produktu** | **Zmiana 29.09.2026 (spec. FW B.6.2).** Pierwotnie: surowy tensometr wzmacniany wbudowanym wzmacniaczem operacyjnym G474. Powód zmiany: sygnał miliwoltowy musiałby przejść kilkadziesiąt centymetrów wiązki obok instalacji zapłonowej, w miejscu zalewanym błotem i poddanym wibracjom. Czujnik prętowy wzmacnia sygnał przy źródle. Skutki: wzmacniacz w G474 zostaje wolny, prawdopodobnie zwalnia się jeden pin złącza (jedna linia sygnałowa zamiast dwóch różnicowych) — do potwierdzenia przy bilansie pinów w Fazie 4, wraz z luką L33 |
| 2.7 | Motocykl referencyjny | Beta 300RR (2015), 1-cyl. 2T, **gaźnik, bez TPS** | Dostępny fizycznie. **Korekta 11.10.2026:** pierwotny zapis mówił „gaźnik + TPS” — motocykl nie ma czujnika przepustnicy i nie będzie dokładany. Założenie Z1 obalone, skutki w rozdz. 11.3 |
| 2.8 | Narzędzie PCB | Claude dostarcza schemat + netlistę + wytyczne; Paweł przerysowuje w Fusion 360 Electronics | Dokumentacja transferowalna |

### 6.2 Lista komponentów ECU (numery katalogowe zweryfikowane)

| Funkcja | Układ | Producent | Uwagi |
|---|---|---|---|
| Mikrokontroler | **STM32G474VET3** | ST | **Dwie zmiany 12.09.2026 po audycie.** (1) F-019: wariant T6 ma zakres tylko -40…+85°C przy analizie dającej do 84°C — sufiks **T3** daje -40…+125°C. (2) F-009: bilans pinów wykazał **55 potrzebnych sygnałów wobec ~50 użytkowych w LQFP64** — przejście na **LQFP100** (litera V zamiast R), ~82 piny użytkowe, zapas ~27. Ten sam rdzeń: 512 KB Flash, 128 KB RAM, 170 MHz, HRTIM, FDCAN, USB |
| Driver zapłonu | VBG08H-E | ST | Smart igniter, wbudowany IGBT, ogranicznik prądu, ochrona termiczna, diagnostyka |
| Driver wtryskiwaczy | **TLE9104SH** (OPN: TLE9104SHXUMA1) | Infineon | **Korekta 12.09.2026 po audycie (F-001), zmiana 2 z 2.** Historia: L9960 (błąd - mostek H do silników DC) → TLE8104E (funkcjonalnie OK, ale **status NRND**, zakaz dla nowych projektów) → **TLE9104SH**. Dobór na podstawie danych wtryskiwaczy KTM TPI/TBI: 11,7 Ω nom. (10,5-13,0 Ω @20°C) = wysokoimpedancyjne, prąd ~1,23 A przy 14,4 V, **peak-and-hold niepotrzebne, wystarcza tryb nasycony**. Datasheet Infineona wprost: driver do wtryskiwaczy, elektrozaworów i przekaźników w systemach zarządzania silnikiem. 4 kanały low-side (2 na wtryskiwacze, 2 zapas), 3 A/kanał, AEC-Q100/101, aktywne ograniczanie napięcia dla obciążeń indukcyjnych, SPI 16-bit z diagnostyką (zwarcie do masy/plusa, przerwa obciążenia), bezpośrednie wejścia PWM. **Piny EN i RESN** - EN wykorzystany jako punkt sprzętowego bramkowania od kill switcha (rozdz. 9.1 planu naprawczego) |
| Transceiver CAN | **TJA1043** | NXP | **Korekta 2026-08-31 (TJA1051T/3 odrzucony — nie ma wybudzania przez magistralę).** W architekturze B pracuje w **trybie Standby**: nasłuchuje magistrali i sygnalizuje MCU wykrycie wzorca wybudzenia zmianą stanu linii RXD. Pin INH **nie jest używany** do sterowania regulatorami — regulator 5 V wyłącza GPIO mikrokontrolera (patrz rozdz. 6.4). Ten sam układ w ECU i HMI |
| IMU | **BMI090L** | Bosch | **Zmiana 12.09.2026:** BMI088 nie jest kwalifikowany AEC-Q100 (Bosch pozycjonuje go do dronów i robotyki) — mój wcześniejszy opis „automotive-grade" był nieuprawniony. BMI090L to odpowiednik z kwalifikacją motoryzacyjną. 6-osiowy, odporność na wibracje |
| Pamięć logów | **W25Q64** (8 MB, SPI NOR) | Winbond | Zakres logowania: zdarzenia krytyczne (czarna skrzynka), 8 MB z zapasem; wlutowana, bez slotu |
| Wyjścia pomocnicze | BTS7008-2EPA ×3 (6 kanałów) | Infineon | PROFET+2, 7.5A/kanał, diagnostyka, ochrona zwarciowa i odwrotnej polaryzacji, AEC-Q100 |
| Ochrona wejścia zasilania | TVS, ochrona odwrotnej polaryzacji, filtr LC, PTC | — | Przed przetwornicami. LM5164-Q1 rozważany jako kandydat na przetwornicę 5 V (wejście 6-100 V, AEC-Q100) — do potwierdzenia przy doborze |
| Kondycjoner VR/Hall | MAX9926 (OPN: MAX9926UAEE/V+) | Analog Devices | Obsługa VR i Hall, odporność na "skipped tooth". **Pobór 4,7 mA typ. / 10 mA maks., brak trybu shutdown** — zasilany przez przełącznik obciążenia, odcinany na czas uśpienia |
| Ciśnienie atmosferyczne | BMP390 | Bosch | Na PCB (I2C/SPI); wymaga membrany odpowietrzającej IP67 w obudowie |
| Pozycja biegu | MLX90316 | Melexis | Triaxis®, bezstykowy, kąt magnesu 0-360°, wyjście analogowe |
| **Przetwornica 5,0 V** | do doboru | — | Nastawa stała (dzielnik rezystorowy), wejście EN sterowane z MCU, wyjście Power Good. Zasila TJA1043 VCC oraz — przez przełącznik obciążenia — czujniki zewnętrzne, MAX9926 i MLX90316. **Uwaga: wejście EN nie służy do usypiania** — przetwornica pozostaje włączona także w uśpieniu (w trybie oszczędnym), bo VCC transceivera musi być pod napięciem; EN jest rezerwą na wyłączenie awaryjne przy wykrytym zwarciu w okablowaniu zewnętrznym. Odcięcie na czas uśpienia realizuje wyłącznie przełącznik obciążenia. **Zastępuje błędne rozwiązanie TLE4276 zasilany z 5 V (audyt F-002)** |
| **Przetwornica 3,3 V** | do doboru | — | Nastawa stała, zawsze włączona (zasila MCU w trybie Stop), wyjście Power Good, **niski prąd własny** (kluczowe dla budżetu uśpienia). Wymaga filtru LC dla VDDA mikrokontrolera |
| **Komparator kill switcha** | do doboru | — | **Nowy 22.09.2026 (decyzja B.2.5.1).** Bramkuje wejścia EN driverów sygnałem kill switcha, niezależnie od firmware. Jeden próg, ustawiony między poziomem RUN a poziomem STOP układu trzypoziomowego — odcina i przy naciśnięciu przycisku, i przy przerwie w przewodzie. **Zasilany z szyny 5 V za przełącznikiem obciążenia** (decyzja 29.09.2026, ECU-SAF-016a) — w uśpieniu bez napięcia, więc nie obciąża budżetu prądu spoczynkowego; bramkowanie nie jest wtedy potrzebne, bo drivery trzymają rezystory ściągające. **Komparator wewnętrzny STM32G474 świadomie odrzucony**: jest konfigurowany przez firmware, a to dokładnie ta zależność, którą zakwestionował audyt (F-004). Dobór po sprawdzeniu karty katalogowej i dostępności w TME (Faza 4) |
| **Przełącznik obciążenia 5 V** | do doboru | — | Odcina czujniki zewnętrzne, MAX9926 i MLX90316 w uśpieniu; sterowany GPIO. **MAX9926 musi przez niego przechodzić** — nie ma wejścia shutdown i pobiera 4,7 mA typowo (karta katalogowa, potwierdzone 20.09.2026), więc jedynym sposobem sprowadzenia jego poboru do zera jest odcięcie zasilania. Powinien mieć ograniczanie prądu — izoluje zwarcie w okablowaniu zewnętrznym od reszty układu |

| **Rezonator kwarcowy (HSE)** | 8 MHz, AEC-Q200, -40…+125°C (np. Abracon ABM8AIG-8.000MHz lub NDK NX3225GD) | — | Model doprecyzowany przy schemacie |
| **Watchdog zewnętrzny** | TPS3430-Q1 | Texas Instruments | **Okienkowy** (nie zwykły timeout) — wykrywa też kod działający w złym tempie (uszkodzony PLL), nie tylko zawieszenie. AEC-Q100, -40…+125°C, ±2,5% @25°C, okno programowane kondensatorem (63ms–77s), osobne opóźnienie resetu, wyłączalny na czas debugowania, 3×3mm, functional-safety-capable |
| **Podtrzymanie RTC** | Superkondensator (0,1–0,47F) + rezystor ograniczający + dioda separująca, na pinie VBAT | — | STM32G474 ma **wbudowany RTC** — zewnętrzny układ niepotrzebny. Podtrzymanie działa tylko przy odłączonym akumulatorze motocykla (serwis, zimowanie); superkondensator zamiast baterii CR2032 — brak wymiany po latach. **Uwaga projektowa:** rozładowany superkondensator przy starcie zachowuje się jak zwarcie — wymagany rezystor ograniczający prąd ładowania. Prąd upływu superkondensatora dolicza się do budżetu uśpienia (do uwzględnienia przy doborze) |
| Złącze główne | **Molex CMC, 28-obwodowy (hybrydowy)** | Molex | **Korekta 2026-08-31 (NTSEAL 26 odrzucony — zero rezerwy pinów).** Hybrydowe styki: 18× 0,635mm (2,5A, sygnały) + 5× 1,50mm (12A) + 5× 2,80mm (21A, zasilanie/moc) — więcej obwodów w mniejszej obudowie niż złącze z jednakowymi stykami. Istnieje jako header do wlutowania w PCB **i** receptacle na wiązkę. IP6K7/IP6K9K, -40…+125°C, wibracje do 25G. Molex wymienia sterowniki silnika motocyklowego jako docelowe zastosowanie. Wymiary do potwierdzenia datasheetem w Fazie 4 |
| Złącze USB | **USB-C**, wykonanie uszczelnione lub gniazdo standardowe z zaślepką IP67 | — | Wymaga rezystorów 5,1 kΩ na liniach CC (tryb urządzenia). Konkretny model przy projekcie PCB |

**6 kanałów PROFET:** wentylator, przekaźnik rozrusznika, światła, pompa paliwa, aux ×2 (rezerwa).

### 6.2b Architektura zasilania (przeprojektowana 12.09.2026 po audycie, F-002/F-003)

**Poprzednia wersja zawierała błąd blokujący:** regulator liniowy 5 V (TLE4276) był zasilany z 5 V z przetwornicy. Regulator liniowy wymaga zapasu napięcia na wejściu, więc wystawiłby ~4,5 V zamiast 5,0 V — rujnując dokładność czujników ratiometrycznych i MAX9926.

**Nowa topologia — dwie niezależne przetwornice:**

```
12V B+ ─► bezpiecznik/PTC ─► ochrona (TVS, odwrotna polaryzacja, filtr LC)
              │
              ├─► Przetwornica 5,0 V ──┬─► TJA1043 VCC (zawsze wł.)
              │   nastawa stała        │
              │   EN = rezerwa         └─► przełącznik obciążenia (GPIO) ─► TPS, MLX90316,
              │   awaryjna                                                  MAX9926, czujniki
              │
              └─► Przetwornica 3,3 V ──┬─► MCU (VDD), flash, IMU, TJA1043 VIO
                  nastawa stała        │   (zawsze włączona — zasila MCU w trybie Stop)
                  zawsze włączona      │
                                       └─► filtr LC (koralik + kondensatory) ─► VDDA/VREF+ MCU
```

**Dlaczego dwie przetwornice zamiast przetwornicy + LDO:** regulator liniowy z 5 V na 3,3 V traci ~1/3 mocy w cieple (~0,3 W przy naszym poborze). Przy napiętym budżecie termicznym w szczelnej obudowie to istotne.

**Koszt tej decyzji:** przetwornica daje napięcie z tętnieniem od przełączania, gorsze dla przetwornika ADC niż gładkie napięcie z regulatora liniowego. Kompensacja: filtr LC na zasilaniu części analogowej mikrokontrolera (VDDA) plus uśrednianie sprzętowe w ADC.

**Nastawy szyn są stałe (dzielniki rezystorowe). Mikrokontroler monitoruje, nie reguluje.**

Rozważana i **odrzucona** propozycja regulacji napięcia szyn przez MCU:
- MCU zasila się z tych samych szyn — błąd w firmware mógłby zniszczyć czujniki, transceiver, pamięć i sam mikrokontroler
- Możliwa pętla samopodtrzymująca: obniżenie własnego zasilania → brown-out → reset → wartość domyślna → powtórka
- Zawieszenie MCU zostawia szynę w nieokreślonym stanie
- **Regulacja niczego nie naprawia** — spadek napięcia oznacza zwarcie, przeciążenie lub słaby akumulator; podniesienie nastawy pogłębia problem

**Mechanizmy nadzoru (realizują cel, dla którego rozważano regulację):**

| Mechanizm | Działanie |
|---|---|
| Pomiar obu szyn przez ADC | Wykrywanie spadków i dryftu, kompensacja pomiarów ratiometrycznych |
| Sygnał Power Good z przetwornic | Wyjście cyfrowe „szyna w tolerancji"; działa niezależnie od firmware, dostępne przed startem ADC |
| Sterowanie włączeniem szyny 5 V | Wyłączenie przy uśpieniu lub wykryciu zwarcia w okablowaniu zewnętrznym. Bezpieczny kierunek sterowania |

Reakcja na wykryty problem: wpis do diagnostyki, ostrzeżenie na HMI, ewentualne przejście w tryb awaryjny — **nigdy zmiana nastawy**.

**Dokładność pomiarów — decyzja: filtr LC, bez zewnętrznego źródła odniesienia.**
- Pomiary ratiometryczne (TPS, MLX90316, temperatury) kompensują się same: mierząc tym samym ADC sygnał czujnika i szynę 5 V, błąd napięcia odniesienia skraca się w stosunku tych wartości
- Jedyny pomiar bezwzględny (napięcie akumulatora) korygowany przez fabrycznie skalibrowane wewnętrzne źródło odniesienia STM32 (kanał VREFINT)
- Tętnienie z przetwornicy tłumione filtrem LC i uśrednianiem sprzętowym w ADC

**Nowy wymóg:** jeden kanał ADC na pomiar szyny 5 V (przez dzielnik) — do kompensacji ratiometrycznej. Nie zajmuje pinu złącza.

**Zegar:** kwarc HSE 8 MHz zamiast TCXO. Przy 10000 obr/min (obrót = 6 ms) błąd kwarcu ±50 ppm to ~0,3 µs ≈ **0,002° kąta wału** — kilkaset razy mniej niż mechaniczne tolerancje koła impulsowego (0,5-1°).

### 6.2c Terminacja CAN (przygotowana pod rozbudowę)

Magistrala CAN wymaga dokładnie **dwóch** rezystorów 120Ω — na fizycznych końcach, nie przy każdym module.

- **ECU:** 120Ω na stałe (ECU jako gateway zawsze pozostaje jednym końcem)
- **HMI i każdy przyszły moduł:** terminacja przełączana zworką — dziś HMI jest drugim końcem (zworka założona); po dołożeniu modułu za HMI zdejmujemy zworkę, terminacja przechodzi na nowy ostatni moduł
- **Terminacja dzielona (split):** 2×60Ω szeregowo z kondensatorem ~4,7nF ze środka do masy zamiast pojedynczego 120Ω — tłumi zakłócenia wspólne (common-mode), standard automotive, koszt marginalny

### 6.2d Ochrona przed przepięciami, ESD i EMI

**Warstwa 1 — zasilanie:**
- TVS 24V unidirectional (np. SMBJ24A) na wejściu B+ — load dump, przepięcia rozrusznika
- Ochrona odwrotnej polaryzacji (dioda szeregowa lub ideal-diode MOSFET)
- Filtr LC (dławik + kondensatory) — blokuje szum wchodzący z instalacji i wychodzący z przetwornicy
- **PTC (500mA–1A) tylko na gałęzi logiki** (przed LM5164-Q1). **Nie na całym B+** — gałąź mocy (wentylator/pompa/światła) ciągnie kilka amperów, PTC o takim prądzie ma zauważalną rezystancję szeregową i wolną reakcję, a obwody te są już chronione indywidualnie przez PROFET-y

**Warstwa 2 — linie sygnałowe wychodzące z obudowy:**
- Czujniki (TPS, temperatury, bieg): TVS niskopojemnościowy + filtr RC na każdej linii
- CAN: dedykowany dwukanałowy TVS do CAN (np. NUP2105L)
- USB: TVS o bardzo niskiej pojemności (nie zniekształcić pary różnicowej)
- Trigger (VR/Hall): TVS + filtr — najbardziej narażona linia, biegnie przy cewce zapłonowej

**Warstwa 3 — wyjścia mocy:**
- Diody gaszące (flyback) na obciążeniach indukcyjnych (przekaźnik, wentylator, pompa) — PROFET ma wbudowane ograniczanie, zewnętrzne diody odciążają układ
- Cewka zapłonowa: VBG08H-E ma wbudowany clamp; linia odseparowana na PCB

**Warstwa 4 — konstrukcja PCB (do wytycznych Fazy 4):**
- Ciągła płaszczyzna masy, rozdzielona na sekcję analogową i mocy z jednym punktem połączenia
- Fizyczne oddzielenie sekcji zapłonu/PROFET od analogowej/MCU
- Kondensatory odsprzęgające przy każdym IC
- Sygnały analogowe z dala od ścieżek przełączających duże prądy
- Rozważyć ekran metalowy nad sekcją analogową

### 6.3 Lista sygnałów na złączu Molex CMC 28-obwodowym

> **Do aktualizacji w Fazie 4 (29.09.2026).** Usunięcie quickshiftera i czujnika sprzęgła z zakresu produktu **zwalnia dwa piny** (dwie linie różnicowe czujnika siły oraz wejście sprzęgła). Luka L33 — niezależny sygnał obciążenia dla wariantów TPI/TBI — **dostaje miejsce**, jeden pin zostaje w zapasie. Lista wymaga przeliczenia przy schemacie.

| Grupa | Sygnały | Piny | Typ styku |
|---|---|---|---|
| Zasilanie | B+ (12V, **stałe z akumulatora**), GND | 2 | duży (2,80mm) |
| Trigger | Sygnał+, Sygnał− | 2 | sygnałowy |
| Czujniki analogowe | TPS, temp. cieczy, temp. powietrza, pozycja biegu | 4 | sygnałowy |
| Wspólne czujników | +5V ref, masa analogowa | 2 | sygnałowy |
| Wejścia cyfrowe | Start (przycisk rozrusznika na kierownicy), kill switch, czujnik prędkości koła, **czujnik fazy wałka rozrządu (rezerwa dla 4T)** | 4 | sygnałowy |
| Wyjścia mocy silnika | Zapłon, wtryskiwacz 1, wtryskiwacz 2 | 3 | średni (1,50mm) |
| Wyjścia pomocnicze | Wentylator, rozrusznik, światła, pompa paliwa, aux ×2 | 6 | średni/duży |
| CAN | CAN H, CAN L | 2 | sygnałowy |
| **Razem** | | **27 / 28** (1 zapasowy) | |

**Przyciski start i kill switch** idą bezpośrednio z kierownicy do ECU przez główne złącze — niezależnie od kabla przycisków HMI (DTM04-3P), który obsługuje wyłącznie nawigację po menu. Podział: 4 przyciski HMI = obsługa systemu; start/kill = sterowanie silnikiem.

**Czujnik fazy wałka rozrządu (4T):** nie znaleziono potwierdzenia, że jednocylindrowe silniki enduro 4T (KTM/Husqvarna EXC-F) go posiadają — dokumentacja diagnostyczna wymienia tylko czujnik pozycji wału korbowego. Zgodne z praktyką dla jednocylindrowców (zapłon "zmarnowaną iskrą" + wtrysk batch — decyzja 2.5). **Pin zarezerwowany mimo to** — koszt jednego pinu vs. przeprojektowanie płytki, gdyby okazał się potrzebny (nieznane silniki, przyszły wtrysk sekwencyjny). Do weryfikacji schematem serwisowym konkretnego modelu 4T.

**Czujnik prędkości koła:** wykorzystujemy fabryczny czujnik z motocykla — pasywny (kontaktron lub Hall z otwartym kolektorem), 2 przewody. Masa wspólna z GND (sygnał cyfrowy, niska częstotliwość — brak ryzyka zakłóceń analogowych). ECU dostarcza konfigurowalny programowo rezystor podciągający do 3,3V. **Do weryfikacji przez Pawła:** pomiar rezystancji między przewodami czujnika przy powolnym obracaniu koła — powinna skakać między przerwą a zwarciem. Jeśli czujnik wymaga własnego zasilania, temat wraca do analizy.

### 6.4 Zarządzanie zasilaniem — tryb uśpienia (architektura B, decyzja 2026-08-31)

**Motocykle enduro nie mają stacyjki** — ECU jest stale zasilane z akumulatora. Wymaga to trybu uśpienia o niskim poborze.

**Wybrana architektura: MCU zarządza uśpieniem** (nie transceiver). Rozważana i odrzucona alternatywa — architektura A, w której TJA1043 pinem INH wyłącza wszystkie regulatory, a MCU jest całkowicie bez zasilania. Architektura A daje niższy pobór (~20-40 µA vs ~60-115 µA), ale jest stosowana w samochodach, gdzie kilkadziesiąt sterowników dzieli budżet prądu spoczynkowego. W motocyklu z jednym sterownikiem to ograniczenie nie występuje: nawet 115 µA to ~83 mAh miesięcznie, czyli <3% akumulatora 3 Ah.

**Co pozostaje zasilane w uśpieniu:**

| Element | Stan | Szacunkowy pobór |
|---|---|---|
| Przetwornica 3,3 V (tryb oszczędny) | włączona | ~10-25 µA |
| Przetwornica 5,0 V (tryb oszczędny, zasila tylko VCC transceivera) | włączona | ~10-25 µA |
| STM32G474 w trybie Stop | zegar zatrzymany, EXTI aktywne | ~10-20 µA |
| TJA1043 | tryb **Standby** (nasłuch magistrali). VCC zasilane na stałe — inaczej układ przeszedłby samoczynnie w Sleep, bo **datasheet wymusza Sleep przy zaniku VCC lub VIO** | ~30-50 µA |
| **Przełącznik obciążenia 5 V** → czujniki zewnętrzne, MAX9926, MLX90316 | **wyłączony przez GPIO mikrokontrolera** | ~1-10 µA |
| PROFET-y, drivery zapłonu/wtrysku | wyłączone | ~µA |
| **RAZEM (szacunek)** | | **~70-135 µA** |

**Źródła wybudzenia (decyzja 2026-08-31 — opcja B):**

| Źródło | Mechanizm |
|---|---|
| **Ramka CAN z HMI** | TJA1043 w trybie Standby nasłuchuje magistrali i reaguje na **filtrowany wzorzec wybudzenia** (nie na dowolną aktywność — odporność na zakłócenia z zapłonu). Sygnalizuje MCU zmianą stanu linii RXD → przerwanie EXTI wybudza procesor |
| **Przycisk startu** | Wejście GPIO z przerwaniem EXTI, rezystor podciągający, przycisk zwiera do masy |
| **Przyciski na kierownicy (przez HMI)** | Naciśnięcie budzi HMI lokalnie, HMI wysyła ramkę CAN, ta budzi ECU |
| **Podłączenie USB** | Wykrycie 5 V z laptopa przez dzielnik → wejście GPIO z przerwaniem |

**Świadomie odrzucone: wybudzanie sygnałem obrotów wału.** Rozważane były trzy warianty:

| Wariant | Powód odrzucenia |
|---|---|
| Dedykowany komparator nanomocowy (TLV7031-Q1) na równoległej ścieżce VR | Dublowanie ścieżki sygnału (dwa układy, dwie drogi na PCB, możliwa rozbieżność wskazań). Dodatkowo **marginalna czułość przy kopnięciu**: sygnał VR przy obrotach rozruchowych ma 50-300 mV międzyszczytowo, a zwykły komparator ze stałym progiem i napięciem niezrównoważenia rzędu miliwoltów działałby na granicy — ryzyko fałszywych wybudzeń lub przegapienia słabego kopnięcia. MAX9926 radzi sobie dzięki adaptacyjnemu progowi i czułości od 20 mV |
| Utrzymanie MAX9926 pod napięciem w uśpieniu | Precyzyjny front-end analogowy pobiera miliampery, nie nanoampery. **Potwierdzone kartą katalogową 20.09.2026: 4,7 mA typowo, 10 mA maksymalnie, brak jakiegokolwiek trybu shutdown.** To ~3400 mAh miesięcznie po stronie szyny 5 V — więcej niż cały akumulator 3 Ah. Układ musi być odcinany zasilaniem, innej drogi nie ma |
| Okresowe próbkowanie (RTC budzi MCU, MAX9926 włączany na krótko) | Złożone, a przy krótkim oknie próbkowania łatwo przegapić kopnięcie — zawodne dokładnie w scenariuszu, dla którego się to robi |

**Konsekwencja dla użytkownika:** jeśli ECU śpi, przed kopnięciem trzeba nacisnąć przycisk (startu lub dowolny na kierownicy). **Do zapisania w instrukcji obsługi.** Uzasadnienie praktyczne: kopnięcie stosuje się zwykle przy zbyt słabym akumulatorze dla rozrusznika — ale ECU i tak wymaga akumulatora do pracy, więc naciśnięcie przycisku to jeden ruch więcej, nie utrata funkcji.

**Zysk:** jedna ścieżka sygnału obrotów (cewka VR → MAX9926 → MCU), jeden komponent mniej, brak problemu czułości i rozbieżności między dwoma torami.

**Dzielnik pomiaru napięcia akumulatora:** typowy dzielnik 100 kΩ/10 kΩ pobiera z 12 V ~110 µA, czyli sam przekroczyłby cały budżet uśpienia. **Wymagany dzielnik wysokoomowy lub odłączany tranzystorem** — do rozstrzygnięcia przy schemacie.

**Warunki zaśnięcia:** 30 min bez pracy silnika i bez interakcji użytkownika (patrz specyfikacja FW, punkt A). Wyświetlacz HMI gaszony wcześniej, po 3 min.

### 6.5 Nadzór nad poprawnym działaniem (watchdog) i stan bezpieczny

**Trzy poziomy zabezpieczenia:**

1. **IWDG (wewnętrzny watchdog STM32G474)** — taktowany własnym oscylatorem LSI, niezależnym od zegara głównego. Wykrywa zawieszenie oprogramowania. Firmware cyklicznie go "karmi"; brak sygnału = reset MCU.
2. **TPS3430-Q1 (watchdog okienkowy zewnętrzny)** — całkowicie niezależny od MCU, działa nawet przy awarii zasilania rdzenia, uszkodzeniu kwarcu lub zawieszeniu sprzętowym. **Okienkowy**, nie prosty timeout: sygnał musi przyjść w zdefiniowanym oknie czasowym — za wcześnie lub za późno oznacza reset. Wykrywa kod działający w złym tempie (uszkodzona konfiguracja PLL), co przy sterowniku zapłonu jest realnym zagrożeniem, a zwykły watchdog by tego nie zauważył.
3. **Stan bezpieczny przy resecie** — sam reset nie wystarczy, jeśli wyjścia zostaną w przypadkowym stanie. **Wymagane rezystory ściągające** na wejściach sterujących: drivera zapłonu (VBG08H-E), driverów wtryskiwaczy (TLE9104SH) i wszystkich PROFET-ów. Przy resecie i podczas startu MCU wszystkie wyjścia mocy muszą być domyślnie **wyłączone** — inaczej reset przy pracującym silniku mógłby zostawić cewkę pod napięciem (przegrzanie) lub wtryskiwacz otwarty.

**Do doprecyzowania w Fazie 5:** okno czasowe watchdoga (kondensator programujący) dobierane po ustaleniu częstotliwości pętli głównej firmware.

**Rozważony i odrzucony wariant konsolidacji:** układy SBC (System Basis Chip, np. NXP UJA1169A) integrują transceiver CAN + regulator + watchdog + zarządzanie uśpieniem w jednej obudowie, zastępując 4 komponenty. Odrzucone: regulator w SBC jest liniowy i pracuje bezpośrednio z 12V — wraca problem termiczny rozwiązany architekturą dwustopniową (rozdz. 6.2b). Dodatkowo warianty z regulatorem 3,3V nie mają wyjścia 5V dla czujników zewnętrznych, a warianty z tym wyjściem mają regulator 5V — nie da się mieć obu naraz.

### 6.6 Przyciski start i kill switch — okablowanie (decyzja 2026-08-31)

**Oba przewodowo, bezpośrednio do ECU** przez główne złącze — nie przez HMI/CAN.

Rozważana alternatywa (obsługa przez HMI, żądanie wysyłane po CAN) odrzucona:

- **Kill switch to funkcja bezpieczeństwa.** Awaria oznaczałaby "nie mogę zatrzymać pracującego silnika" — scenariusze użycia to zablokowana przepustnica, upadek z przygniecionym motocyklem, silnik w rozbiegu. Przepuszczenie przez trzy dodatkowe punkty awarii (FW HMI, magistrala CAN, FW ECU) tworzy sytuację, w której zawieszenie oprogramowania HMI odbiera możliwość zgaszenia silnika. Standardowe rozwiązanie motocyklowe działa **fail-safe**: obwód normalnie zamknięty, przerwanie przewodu = silnik gaśnie. Przez CAN tej właściwości nie da się odtworzyć.
- **Przycisk startu — opóźnienie.** Przy uśpionym ECU łańcuch to: naciśnięcie → wybudzenie HMI → ramka CAN → wybudzenie ECU → rozrusznik. Setki milisekund zwłoki przy funkcji, która ma reagować natychmiast.

**Podział ról:** 4 przyciski HMI (kabel DTM04-3P) = wyłącznie nawigacja po menu i obsługa systemu. Start i kill switch (główne złącze ECU) = sterowanie silnikiem.

### 6.7 Wymagania instalacyjne (do dokumentacji użytkownika, Faza 11)

**Elementy fabrycznej instalacji, które MUSZĄ pozostać** mimo że ECU jest standalone:

| Element | Dlaczego |
|---|---|
| **Stator (uzwojenie ładowania)** | Jedyne źródło energii ładującej akumulator — bez niego akumulator rozładuje się w kilka godzin jazdy |
| **Regulator napięcia / prostownik** | Zamienia napięcie przemienne ze statora na stałe i ogranicza je do bezpiecznego poziomu. Bez niego napięcie rośnie z obrotami i zniszczy akumulator oraz odbiorniki |
| **Akumulator** | ECU zasilane wyłącznie z akumulatora (decyzja 2.1); dodatkowo bufor wygładzający tętnienia z prostownika |
| **Czujnik prędkości koła** | Wykorzystywany przez ECU (prędkościomierz, licznik km) |
| **Cewka zapłonowa** | Sterowana przez ECU |

**Elementy usuwane:** fabryczny sterownik CDI/ECU, fabryczna wiązka sygnałowa, licznik, pompka olejowa w silnikach TPI/TBI (przejście na premiks — decyzja 0.8).

**Wiązka kill switcha — wymóg szczególny (decyzja 22.09.2026):** przycisk musi być podłączony wiązką zawierającą **dwa rezystory umieszczone przy przycisku** — szeregowy i równoległy do styku. Dają one trzy rozróżnialne poziomy napięcia, dzięki czemu ECU odróżnia naciśnięcie przycisku od przerwania przewodu lub rozłączenia wtyczki i potrafi to wskazać kierowcy. Wartości rezystorów — Faza 4.

Podłączenie zwykłego przycisku bez rezystorów **nie jest niebezpieczne**: funkcja odcięcia działa poprawnie w obu stanach, ale każde naciśnięcie przycisku zostanie zgłoszone jako przerwa w przewodzie. Wiązka z rezystorami wchodzi w zakres dostawy.

**Kondensator buforowy na wejściu zasilania ECU:** wymagany, żeby ECU pracowało stabilnie przy tętniącym napięciu z prostownika w sytuacji uszkodzonego/odłączonego akumulatora (patrz L6). Pojemność do obliczenia przy projekcie zasilania, weryfikacja pomiarem w Fazie 6.

### 6.8 Budżet energetyczny i analiza termiczna (2026-08-31)

Szacunki na podstawie wartości typowych z datasheetów. **Do weryfikacji pomiarem w Fazie 6.**

**Pobór prądu (przeliczony na stronę 12 V):**

| Pozycja | Prąd @12V | Moc |
|---|---|---|
| ECU — logika i czujniki | ~120 mA | ~1,3 W |
| HMI — MCU, EVE4, podświetlenie 1000 cd/m², LED przycisków | ~200 mA | ~2,2 W |
| **System sterujący razem** | **~320 mA** | **~3,8 W** |
| Wentylator chłodnicy | ~6 A | 72 W |
| Pompa paliwa (TPI/TBI) | ~4 A | 48 W |
| Oświetlenie LED | ~2 A | 24 W |
| Przekaźnik rozrusznika (cewka) | ~0,3 A | 4 W |
| **Szczyt (wszystko naraz)** | **~12,6 A** | **~151 W** |
| Typowa jazda (światła, wentylator sporadycznie) | ~2,3 A | ~28 W |

**Wniosek:** stator w enduro tej klasy oddaje typowo 150–200 W. Bilans się domyka; szczyt występuje rzadko i przy wysokich obrotach, gdy stator daje pełną moc. Samo ECU+HMI to <4 W — margines, nie problem.

**Straty cieplne wewnątrz obudowy ECU** *(zaktualizowane 12.09.2026 po korekcie drivera wtrysku)*:

| Źródło | Straty |
|---|---|
| **Driver zapłonu VBG08H-E** (8000 obr/min, dwell 3 ms → wypełnienie ~40%) | **4,8 W** |
| Drivery wtryskiwaczy TLE9104SH (2 kan., 1,23 A, wypełnienie ~10%) | ~0,16 W |
| Przetwornica 3,3 V (sprawność ~90%, 200 mA) | 0,07 W |
| PROFET ×3 (Rds_on, 3 A/kanał) | 0,27 W |
| Przetwornica 5,0 V (sprawność ~90%) | 0,17 W |
| Przełącznik obciążenia 5 V | 0,05 W |
| **RAZEM** | **~5,5 W** |

| Wykonanie obudowy | Przyrost | Temp. wewnątrz przy otoczeniu 40°C |
|---|---|---|
| Aluminium + dobry kontakt termiczny (Rth≈3 K/W) | +17°C | **57°C** ✅ |
| Aluminium bez past/padów (Rth≈8 K/W) | +44°C | **84°C** ⚠️ (na granicy zakresu STM32G474RE**T6**; wybrany wariant **T3** ma zapas do 125°C) |
| Tworzywo sztuczne (Rth≈20 K/W) | +110°C | **150°C** ❌ |

⚠️ **Ograniczenie modelu (audyt F-019):** powyższe używa uproszczonej rezystancji cieplnej obudowy. Wymagany pełny łańcuch złącze→pad/PCB→interfejs termiczny→obudowa→otoczenie oraz weryfikacja klasy temperaturowej komponentów. **STM32G474RET6 w wersji przemysłowej ma zakres do 85°C otoczenia** — twierdzenie, że wszystkie komponenty pracują do 125°C, było nieuprawnione bez rozróżnienia temperatury złącza i klasy. Do domknięcia w Etapie 2.

**Wnioski:**
1. **Obudowa aluminiowa z kontaktem termicznym jest wymagana**, nie zalecana. Tworzywo wykluczone.
2. **Do Fazy 2-FW:** czas ładowania cewki powinien być skracany przy wysokich obrotach (ładowanie tylko do osiągnięcia prądu nasycenia, nie stałe 3 ms). Realnie obniży to dominujące źródło strat.

---

## 7. Faza 2-HMI — Projekt szczegółowy HW

| # | Decyzja | Wybór | Uzasadnienie |
|---|---|---|---|
| H.1 | Własny MCU | Tak | Obsługa CAN, przycisków, wyświetlacza, lokalnej konfiguracji |
| H.2 | MCU | STM32G0B1 | Jedyna linia G0 z FDCAN (G071 go nie ma); ten sam producent co ECU |
| H.3 | Wyświetlacz | Riverdi **RVT35HHBFWN00** — 3.5", 320×240, IPS, EVE4 (BT817Q), SPI/QSPI, 1000 cd/m², bez dotyku, metalowa ramka | Koprocesor graficzny = animacje bez obciążania RAM-u MCU; polski producent |
| H.4 | Przyciski | 4 szt. (GÓRA/DÓŁ/WYBÓR/WSTECZ), IP67, rodzina APEM IP-momentary lub E-Switch 16mm | Automotive-grade, 1M cykli, złocone styki |
| H.5 | Lokalizacja przycisków | **Na kierownicy**, nie w obudowie HMI | Ergonomia obsługi w jeździe |
| H.6 | Okablowanie przycisków | Drabinka rezystorowa — 4 przyciski na 1 wejściu analogowym | Ogranicza liczbę żył; brak detekcji jednoczesnego wciśnięcia nieistotny |
| H.7 | Podświetlenie przycisków | Sterowane — ECU wysyła stan świateł po CAN, HMI włącza podświetlenie | Bez dodatkowego okablowania |
| H.8 | Złącze główne HMI | Deutsch DTM04-4P: CAN H, CAN L, **+12V stałe z akumulatora**, GND | Seria DTM = miniaturowa wersja DT, 13A/pin. **Uwaga:** motocykle enduro nie mają stacyjki, więc HMI jest zasilane stale i wymaga własnego trybu uśpienia (rozdz. 7.1) |
| H.9 | Złącze przycisków | Osobne: Deutsch DTM04-3P (sygnał drabinki, zasilanie LED, masa) | Serwisowalność — kierownice wymieniane po upadkach bez ruszania wiązki głównej |
| H.10 | Transceiver CAN HMI | **TJA1043** (ten sam co w ECU) | Spójność — jeden numer katalogowy na oba urządzenia; wybudzanie przez magistralę potrzebne także w HMI (tryb uśpienia, budzenie przyciskiem) |
| H.11 | Zasilanie HMI | **Dwie przetwornice: 5 V (wyświetlacz + EVE4, wyłączana w uśpieniu) i 3,3 V (MCU, flash, TJA1043 VIO, zawsze włączona)** — analogicznie do ECU po przeprojektowaniu z 12.09.2026. Nastawy stałe, Power Good do MCU, filtr LC dla VDDA. TJA1043 VCC z szyny 5 V — **do rozstrzygnięcia przy schemacie:** czy VCC HMI zostaje zasilone w uśpieniu (tryb Standby) czy wyłączane (tryb Sleep) |
| H.13 | **Czujnik temperatury** | Cyfrowy czujnik temperatury na PCB HMI, blisko wyświetlacza (I2C, np. TMP112-Q1 lub równoważny; model przy schemacie) | Analiza termiczna (rozdz. 7.2) wykazała ryzyko przekroczenia 70°C na słońcu, przy którym panel LCD czernieje. Czujnik umożliwia automatyczne ograniczanie jasności podświetlenia przy przegrzaniu |
| H.12 | **Pamięć zasobów graficznych i konfiguracji** | Zewnętrzna flash SPI NOR, rodzina W25Q (ta sama co w ECU; pojemność do ustalenia po oszacowaniu rozmiaru zasobów) | EVE4 wymaga trwałego przechowywania bitmap, czcionek i animacji; dwubankowy bootloader zostawia ~256 KB na bank w STM32G0B1 — za mało na firmware + zasoby graficzne. Ta sama rodzina co w ECU upraszcza zaopatrzenie i kod obsługi |

### 7.1 Zarządzanie uśpieniem HMI (decyzja 2026-08-31)

HMI, tak jak ECU, jest zasilane stale z akumulatora (brak stacyjki) i wymaga trybu uśpienia.

**Kto decyduje o zaśnięciu:** ECU, poleceniem wysłanym po CAN. ECU dyryguje całym systemem - zna stan silnika i czas bezczynności, więc to ono wyznacza moment uśpienia (wyświetlacz gaszony po 3 min, pełne uśpienie przy zasypianiu ECU po 30 min).

**Zabezpieczenie przed utratą polecenia:** gdyby ramka z poleceniem uśpienia zaginęła (zakłócenie, awaria magistrali), HMI zostałoby wybudzone na stałe i rozładowywało akumulator. Dlatego **HMI ma własny timeout awaryjny** - brak jakiejkolwiek ramki z ECU przez określony czas (rząd kilku minut, do ustalenia w Fazie 2-FW) skutkuje samodzielnym zaśnięciem.

**Stan uśpienia HMI:**

| Element | Stan |
|---|---|
| STM32G0B1 | tryb Stop, aktywne przerwania EXTI |
| Przetwornica 3,3 V | włączona - zasila MCU |
| Wyświetlacz RVT35 + koprocesor EVE4 | **odłączone** (podświetlenie ~250 mA - główny konsument) |
| Podświetlenie LED przycisków | wyłączone |
| Flash SPI (zasoby graficzne) | tryb deep power-down |
| TJA1043 | tryb Standby, nasłuch magistrali |

**Źródła wybudzenia HMI** (niezależne od tego, kto je usypia):

| Źródło | Mechanizm |
|---|---|
| **Naciśnięcie dowolnego przycisku** | Linia drabinki rezystorowej podpięta **równolegle do wejścia z przerwaniem zewnętrznym (EXTI)** obok wejścia ADC. Naciśnięcie dowolnego przycisku ściąga linię w dół, zbocze wybudza MCU. Dopiero po wybudzeniu ADC określa, **który** przycisk. Konieczne, bo **przetwornik ADC nie działa w trybie Stop** |
| **Ramka CAN z ECU** | TJA1043 w Standby wykrywa wzorzec wybudzenia, sygnalizuje przez RXD, EXTI wybudza MCU |

**Kolejność zasypiania:** ECU wysyła polecenie uśpienia do HMI, odczekuje na potwierdzenie (lub krótki czas), dopiero potem zasypia samo. Inaczej HMI mogłoby zostać wybudzone.

### 7.2 Analiza termiczna HMI (2026-08-31)

**Straty wewnętrzne: ~2,4 W**

| Źródło | Straty |
|---|---|
| Podświetlenie wyświetlacza (1000 cd/m²) | 1,25 W |
| Driver LED przycisków | 0,30 W |
| Przetwornica 12→5 V | 0,26 W |
| TJA1043 + flash SPI | 0,20 W |
| Koprocesor EVE4 (BT817Q) | 0,17 W |
| LDO 3,3 V | 0,17 W |
| STM32G0B1 | 0,10 W |

**Obciążenie zewnętrzne — nasłonecznienie.** HMI to jedyny element systemu wystawiony bezpośrednio na słońce. Ekran 3,5" (~0,005 m²) w ciemnej obudowie może pochłonąć do ~4 W promieniowania - więcej niż generuje sam.

| Wykonanie obudowy | Temp. wewnątrz przy 40°C otoczenia + nasłonecznieniu |
|---|---|
| Tworzywo, ciasna obudowa | ~151°C ❌ |
| Tworzywo, obudowa z zapasem | ~107°C ❌ |
| Aluminium z odprowadzeniem ciepła | ~76°C ⚠️ |

**Zagrożenie jest realne:** panele LCD mają typowy zakres pracy do 70°C - powyżej tej granicy ciekły kryształ przechodzi w fazę izotropową i **ekran czernieje**. To znany problem jasnych wyświetlaczy na słońcu: im mocniejsze podświetlenie, tym więcej ciepła.

**Wymagania wynikające z analizy:**
1. **Obudowa HMI aluminiowa** z kontaktem termicznym - tak samo jak ECU
2. **Jasny lub odblaskowy kolor obudowy** zamiast czarnego - redukuje pochłanianie z ~4 W do ułamka
3. **Czujnik temperatury + zarządzanie jasnością w FW** (decyzja H.13). Paradoks do rozwiązania w Fazie 2-FW: na słońcu potrzeba maksymalnej jasności, a właśnie wtedy grozi przegrzanie
4. **Daszek przeciwsłoneczny** - do rozważenia przy projekcie obudowy; chroni przed nagrzewaniem i poprawia czytelność pod kątem

*Wartości szacunkowe, do weryfikacji pomiarem w Fazie 6.*

---

## 8. Poza zakresem — świadomie odrzucone

- **Silniki 2-cylindrowe i ride-by-wire** (np. KTM 890 Adventure) — osobna kategoria ryzyka, wymagałaby dedykowanego projektu
- **Closed-loop lambda (czujnik O2)** — poza zakresem MVP
- **EGT, czujnik spalania stukowego (knock)** — zaawansowane funkcje tuningowe, poza MVP
- **Sterowanie pompką olejową** — pompka usuwana, premiks
- **Launch control** — nie wybrany w Fazie 0. Sprzętowo możliwy do dodania później w firmware (wymaga tylko istniejących wejść: RPM, TPS, bieg) — brak przeszkód konstrukcyjnych
- **Kontrola trakcji** — nieomawiana. Po dodaniu czujnika prędkości koła stała się technicznie możliwa (porównanie RPM silnika z prędkością koła), ale poza zakresem MVP — do rozważenia w przyszłej wersji firmware

---

**Quickshifter i czujnik sprzęgła — usunięte 29.09.2026 (decyzja Pawła).** Funkcja była w zakresie od Fazy 0 i miała opracowaną pełną specyfikację (punkt B.6). Powody usunięcia: najgorszy stosunek złożoności do wartości w projekcie (9 wymagań, 3 kody usterek, 2 komponenty, 2 piny); jedyna funkcja wymagająca wnioskowania o **intencji kierowcy** zamiast o mierzalnym stanie — stąd trzy kolejne błędy specyfikacji; niska realna wartość w technicznym terenie, gdzie sprzęgło jest w ciągłym użyciu; najgroźniejszy tryb awarii w ECU. **Zwolnione dwa piny przechodzą do bilansu — luka L33 dostaje miejsce.** Zapis usuniętej specyfikacji: `faza2-fw-specyfikacja.md` rozdz. B.6. Blipper (zmiana w dół bez sprzęgła) był poza zakresem już wcześniej.
## 9. Rejestr luk otwartych (audyt 2026-08-31)

### 9.1 Bezpieczeństwo

| # | Luka | Status |
|---|---|---|
| L1 | **Kill switch fail-safe** — **DECYZJA ZMIENIONA 12.09.2026 po audycie zewnętrznym (F-004).** Wcześniejsza akceptacja samego wejścia GPIO cofnięta: okno watchdoga 100 ms przy 10 000 obr/min to ~17 obrotów wału z niekontrolowaną pracą. Nowe rozwiązanie: okablowanie normalnie zamknięte + **sprzętowe bramkowanie** wejść sterujących driverów zapłonu i wtrysku (tranzystor/bramka logiczna), niezależne od MCU. Szczegóły: `plan-naprawczy-audyt.md` rozdz. 9.1 | ✅ Rozwiązane |
| L2 | **Brak blokady rozrusznika na biegu** — **decyzja 2026-08-31: brak blokady, odpowiedzialność po stronie kierowcy** (jak w części motocykli sportowych). Wymaga wyraźnego ostrzeżenia w instrukcji obsługi. **Podtrzymane 29.09.2026** przy okazji wprowadzenia czujnika sprzęgła: czujnik świadomie **nie** jest warunkiem załączenia rozrusznika, bo awaria przełącznika w klamce mogłaby unieruchomić motocykl. W zamian wskazanie informacyjne włączonego biegu na HMI przy zgaszonym silniku (HMI-UI-009), bez blokady i bez zapisu do logu | ⚠️ Zaakceptowane |
| L3 | **Czujnik sprzęgła** — **niepotrzebny** wobec decyzji L2. Rozważany ponownie 29.09.2026 na potrzeby quickshiftera i **odrzucony razem z nim**; pin pozostaje wolny | ✅ Zamknięte |
| L4 | **Strategia limp-home** przy uszkodzeniu czujnika — **przeniesione do Fazy 2-FW, punkt B** | ➡️ Faza 2-FW |
| L5 | **Reakcja na przegrzanie silnika** — **decyzja 2026-08-31: tylko ostrzeżenie na HMI**, bez automatycznego ograniczania mocy. Decyzja o zatrzymaniu należy do kierowcy (świadomy wybór — w zawodach automatyczna redukcja mocy mogłaby być groźniejsza niż przegrzanie). Progi do ustalenia w Fazie 2-FW | ✅ Zamknięte |

### 9.2 Funkcjonalne

| # | Luka | Status |
|---|---|---|
| L6 | **Kickstart przy rozładowanym akumulatorze** — **rewizja oceny 2026-08-31: problem znacznie węższy niż pierwotnie oszacowano.** Granica działania ECU to ~7 V na złączu (LM5164-Q1 pracuje od 6 V + spadki na ochronie) — akumulator przy 7 V jest już zniszczony, nie tylko rozładowany. Ładowanie cewki przy niskim napięciu wymaga ~1,7× dłuższego czasu, co przy obrotach kopnięcia (300-500 obr/min) nie stanowi problemu, a energia iskry pozostaje pełna. Ścieżka stator → prostownik → ECU już istnieje; bez akumulatora jako bufora napięcie jest tętniące, ale przetwornica znosi 6-100 V. **Rozwiązanie: odpowiednio duży kondensator buforowy na wejściu zasilania + kompensacja czasu ładowania cewki wg napięcia w FW.** Nie jest potrzebne osobne wejście AC ze statora ani dodatkowe piny. Nierozwiązywalny pozostaje wyłącznie akumulator ze zwartym ogniwem (dotyczy tak samo fabrycznej instalacji) | ✅ Zamknięte |
| L7 | **Układ ładowania (stator + regulator/prostownik) musi pozostać** przy instalacji standalone — **rozwiązane 2026-08-31: dopisane jako wymaganie instalacyjne (rozdz. 6.7), trafia do dokumentacji użytkownika w Fazie 11** | ✅ Zamknięte |
| L8 | **Prime pompy paliwa** (~2s po wybudzeniu przed rozruchem, TPI/TBI) — **przeniesione do Fazy 2-FW, punkt A/B** (maszyna stanów: stan gotowości) | ➡️ Faza 2-FW |
| L9 | **Sygnalizacja stanu bez HMI** — **decyzja 2026-08-31: brak diody na ECU.** Diagnostyka wyłącznie przez HMI i aplikację desktop | ✅ Zamknięte |
| L10 | **Profile konfiguracyjne per model motocykla** — **przeniesione do Fazy 2-FW, punkt D** | ➡️ Faza 2-FW |
| L11 | **Zachowanie HMI przy utracie komunikacji z ECU** — **decyzja 2026-08-31: komunikat o błędzie i wygaszenie danych.** Żadna wartość nie jest wyświetlana, żeby nie wprowadzać w błąd zamrożonym odczytem | ✅ Zamknięte |
| L12 | **Reakcja na niskie napięcie akumulatora** — **decyzja 2026-08-31: ostrzeżenie na HMI + zapis do logu diagnostycznego.** ECU nie wyłącza odbiorników samodzielnie. Próg do ustalenia w Fazie 2-FW | ✅ Zamknięte |

### 9.3 Sprzętowe — DO USTALENIA

| # | Luka | Waga |
|---|---|---|
| L13 | Złącze USB — **decyzja 2026-08-31: USB-C** (uszczelnione lub z zaślepką IP67; rezystory CC 5,1 kΩ) | ✅ |
| L14 | Driver LED podświetlenia przycisków — **decyzja 2026-08-31: umieszczony w HMI** (bliżej przycisków, krótsza ścieżka zasilania). Driver ze stałym prądem + wejście PWM; model przy schemacie HMI | ✅ |
| L15 | **Budżet energetyczny** — **policzony 2026-08-31 (rozdz. 6.8): bez zastrzeżeń.** System sterujący ~320 mA / 3,8 W; szczyt całkowity ~12,6 A / 151 W przy wydajności statora 150–200 W | ✅ |
| L16 | **Analiza termiczna** — **policzona 2026-08-31, zaktualizowana 12.09.2026 po korekcie drivera wtrysku (rozdz. 6.8): ~5,5 W strat, dominuje driver zapłonu (4,8 W @8000 obr/min).** Wniosek: obudowa aluminiowa z kontaktem termicznym **wymagana**, tworzywo wykluczone | ✅ |
| L17 | Liczba warstw PCB — nieustalona (wpływa na koszt i EMI) | 🟡 |
| L18 | **Powłoka ochronna (conformal coating)** na PCB — do rozważenia mimo obudowy IP67 (kondensacja) | 🟡 |
| L19 | **Punkty testowe** na PCB do diagnostyki produkcyjnej | 🟢 |
| L20 | **Serializacja/znakowanie płytek** — numer seryjny do obsługi gwarancyjnej | 🟢 |
| L21 | **Stanowisko testowe HMI** — **decyzja 2026-08-31: moduł ewaluacyjny Riverdi (docelowy RVT35HHBFWN00) + NUCLEO-G0B1RE.** Stanowisko odpowiada docelowemu sprzętowi — kod z Fazy 3 przenosi się na PCB bez przepisywania | ✅ |
| L22 | **Watchdog w HMI** — **decyzja 2026-08-31: wystarczy wewnętrzny IWDG**, bez zewnętrznego układu. Dominujący tryb awarii (zawieszenie FW) jest przez niego pokryty; HMI nie steruje silnikiem. Uzupełnienia: (a) ECU monitoruje heartbeat HMI na CAN i loguje zanik jako zdarzenie diagnostyczne, (b) po resecie HMI musi poprawnie reinicjalizować koprocesor EVE4 | ✅ |

### 9.4 Procesowe — DO UZUPEŁNIENIA

| # | Luka | Waga |
|---|---|---|
| L23 | **Brak fazy specyfikacji firmware** — zasada #6 mówi "nic do implementacji bez zatwierdzonej specyfikacji", a proces nie zawierał fazy, która ją tworzy. **Rozwiązane: dodana Faza 2-FW (rozdz. 3.2)** | ✅ |
| L24 | **Brak śledzenia pokrycia wymagań** (traceability) — **rozwiązane: zasada #8 + tabela w rozdz. 14** | ✅ |
| L25 | **Brak planu testów** — **rozwiązane: zasada #9, plan powstaje w Fazie 3, rozszerzany w kolejnych** | ✅ |
| L26 | **Brak wersjonowania i zarządzania konfiguracją** — **rozwiązane: zasada #7 (major.minor.patch, kontrola zgodności ECU↔HMI↔desktop)** | ✅ |
| L27 | **Brak dokumentacji użytkownika** — **rozwiązane: dopisana do deliverables Fazy 11** | ✅ |
| L28 | **Strategia bootloadera/recovery** — **rozwiązane: zasada #10, dwubankowy z automatycznym powrotem do poprzedniej wersji** | ✅ |
| L29 | **HMI: brak pamięci na zasoby graficzne i konfigurację wyglądu** — **rozwiązane: zewnętrzna flash SPI NOR (rodzina W25Q), decyzja H.12. Pojemność do ustalenia po oszacowaniu rozmiaru zasobów w Fazie 2-FW** | ✅ |
| **L30** | **Brak planu wyposażenia stanowiska pomiarowego** — 57 z 70 testów przypada na Fazę 6, część wymaga sprzętu, którego nie ma (komora klimatyczna, wstrząsarka, automatyczny zbiór 10⁵ pomiarów kąta, miernik z zakresem µA). Do zestawienia w Fazie 3 razem z planem testów. Prowadzone jako **ryzyko R16** | 🔴 |
| **L31** | **Funkcje w zakresie bez wymagania** — zestawione w rozdz. 14.11. **Aktualizacja 29.09.2026:** quickshifter usunięty z zakresu, więc pozostała **jedna pozycja P0 — bootloader** (punkt H specyfikacji FW). Nadal blokuje bramkę G0. Prowadzone jako **ryzyko R18** | 🔴 |
| **L34** | ~~Brak repozytorium i kontroli wersji~~ — **ROZWIĄZANE 11.10.2026: zasada procesu #16.** Pierwotny zapis: dokumenty istnieją jako pliki nadpisywane w miejscu; historia zmian jest w treści, ale nie da się odtworzyć wcześniejszej wersji; baseline przy bramce jest zasadą bez mechanizmu. **Zmaterializowało się już raz** — część pracy przepadła przy awarii środowiska | ✅ |
| **L35** | ~~Brak rejestru założeń~~ — **ROZWIĄZANE 11.10.2026: rozdz. 11.2.** Pierwsza wpisana pozycja (Z1 — obecność TPS w MVP-A) okazała się fałszywa tego samego dnia; skutki w rozdz. 11.3. Pierwotny zapis: założenia siedzą w prozie (czas ładowania cewki ~3 ms, typowe kąty wyprzedzenia dwusuwu, liczba obrotów wału na kopnięcie, obecność TPS na gaźniku) i żadne nie jest oznaczone jako wymagające potwierdzenia | ✅ |
| **L36** | ~~Brak standardu kodowania, planu analizy statycznej i walidacji narzędzi~~ — **ROZWIĄZANE 11.10.2026: zasada procesu #17** (decyzja o konieczności i zakresie; konkretne wybory przed Fazą 5). Pierwotny zapis: implementacja firmware sterującego zapłonem ma ruszyć, a nie ustalono ani standardu, ani narzędzi, ani kryteriów pokrycia testami jednostkowymi | ✅ |
| **L37** | ~~Brak kryteriów akceptacji wyrobu~~ — **ROZWIĄZANE 11.10.2026: rozdz. 3.0a, 12 kryteriów A1–A12.** Status 🟡 do chwili zatwierdzenia listy przez Pawła. Pierwotny zapis: bramki opisują fazy, nie wyrób; nie zdefiniowano, co znaczy „MVP-A gotowe” | 🟡 |
| **L38** | **ZAPLANOWANE, nie przeoczenie — Faza 4.** Oszacowanie kosztu BOM wymaga istniejącego BOM z pełnymi numerami katalogowymi, który powstaje w Fazie 4. Pierwotny zapis: Faza 0 wymagała, by system był „budżetowo rozsądny i uargumentowany”; nie przeliczono tego ani razu | 🟡 |
| **L39** | **ZAPLANOWANE, nie przeoczenie — Faza 2-Desktop.** Przypadki użycia i wymagania niefunkcjonalne aplikacji powstają razem z jej projektem; napisane wcześniej i pospiesznie byłyby dokumentacją pod audytora, nie pod produkt. Pierwotny zapis: brak przypadków użycia i wymagań niefunkcjonalnych aplikacji desktop — nie opisano żadnego scenariusza użytkownika, ekranów HMI ani przepływów w aplikacji; jedyne wymaganie APP dotyczy transakcyjności zapisu | 🟡 |
| **L40** | **ZAPLANOWANE, nie przeoczenie — po zamknięciu MVP-A.** Warianty B i C mają zarezerwowane zdolności sprzętowe; ich zakres powstanie, gdy MVP-A będzie działać. Pierwotny zapis: wymagania oznaczone `[B/C]` odwołują się do wariantów bez własnego zakresu i odbiorcy | 🟡 |
| **L33** | **Niezależny sygnał obciążenia dla wariantów TPI/TBI** — przy utracie TPS ECU zostaje bez jakiejkolwiek informacji o obciążeniu. Fabryczny system KTM ma czujnik ciśnienia w skrzyni korbowej, który taką informację niesie. Wprowadzenie kosztowałoby **ostatni wolny pin złącza** (ten sam, o który rozbiła się decyzja A.4 o czujniku ciśnienia paliwa). Do rozstrzygnięcia przy projektowaniu wariantu B/C, razem z ponownym bilansem pinów. Nie dotyczy MVP-A. **Aktualizacja 29.09.2026:** po usunięciu quickshiftera i czujnika sprzęgła z zakresu **luka dostaje miejsce** — zwolnione dwa piny, jeden dla tego czujnika, jeden w zapasie. Do rozstrzygnięcia merytorycznego przy projektowaniu wariantu B/C | 🟡 |
| **L32** | **Brak zarządzania wersjami dokumentów** (audyt F-033) — **rozwiązane 20.09.2026: rozdz. 0 (metryka i historia zmian) + zasada procesu #13** | ✅ |

### 9.5 Zamknięte w audycie HW (2026-08-31)

Transceiver CAN dla HMI (TJA1043) · regulatory napięcia (architektura dwustopniowa) · rezonator HSE · terminacja CAN · ochrona nadprądowa · ochrona ESD/TVS · złącze SWD · driver LED (koncepcja) · model transceivera · pojemność pamięci · watchdog (TPS3430-Q1) · okablowanie start/kill

⚠️ **Zawężenie zakresu logowania:** logowanie on-board ograniczone do zdarzeń krytycznych (czarna skrzynka) — pierwotna decyzja 1.4 zakładała pełne logowanie sesji. Ograniczenie jest w firmware, nie w sprzęcie (8 MB daje zapas).


## 10. Wymagania dla obudów (projekt: Paweł)

### ECU

| Parametr | Wymaganie |
|---|---|
| Szczelność | IP67 minimum (zanurzenie, przeprawy wodne, mycie ciśnieniowe) |
| Wyrównanie ciśnienia | **Membrana odpowietrzająca (Gore-Tex vent lub odpowiednik)** — obowiązkowa: BMP390 mierzy ciśnienie atmosferyczne (korekta na wysokość n.p.m.), w hermetycznej obudowie byłby bezużyteczny. Membrana zapobiega też kondensacji przy zmianach temperatury |
| Odprowadzanie ciepła | **WYMAGANE: obudowa aluminiowa z zapewnionym kontaktem termicznym** (pady lub pasta) między ścianką a driverem zapłonu, PROFET-ami i przetwornicą. Tworzywo **wykluczone** — analiza (rozdz. 6.8) daje +134°C przyrostu, czyli 174°C wewnątrz przy otoczeniu 40°C |
| Przepusty | Złącze Molex CMC 28-obwodowe (header wlutowany w PCB) + gniazdo **USB-C** — uszczelnione lub standardowe z zaślepką gumową/gwintowaną. Uszczelnienie na poziomie IP67 |
| Wibracje | Mocowanie PCB w kilku punktach (nie tylko na złączu), silikonowe tuleje/gumowe podkładki w punktach montażu do ramy |
| Temperatura | Praca -20…+85°C otoczenia; komponenty dobrane do 125°C, ale obudowa nie może kumulować ciepła |
| Dostęp serwisowy | Możliwość otwarcia bez niszczenia uszczelnienia (uszczelka wymienna, nie klejona na stałe) — dostęp do złącza SWD |
| Montaż | Odporny na uderzenia/upadki; ECU umieszczone z dala od bezpośredniego strumienia błota i gorąca wydechu |

### HMI

| Parametr | Wymaganie |
|---|---|
| Szczelność | IP67 minimum |
| Widoczność | Ekran chroniony przed zarysowaniem (osobna szybka poliwęglanowa/szklana nad panelem — wyświetlacz nie ma własnej) |
| Odblaski | Matowa/antyrefleksyjna warstwa lub daszek — inaczej 1000 cd/m² nie wystarczy przy słońcu pod kątem |
| Przepusty | 2 złącza: DTM04-4P (główne) + DTM04-3P (przyciski) |
| Wibracje | Mocowanie do kierownicy/mostka przez elementy tłumiące — wyświetlacz LCD jest wrażliwy na wibracje |
| Temperatura | **WYMAGANE: obudowa aluminiowa z kontaktem termicznym + jasny/odblaskowy kolor.** Analiza (rozdz. 7.2): tworzywo daje 107-151°C wewnątrz na słońcu, panel LCD czernieje powyżej ~70°C. Czujnik temperatury steruje jasnością podświetlenia. Daszek przeciwsłoneczny do rozważenia |
| Widoczność nocna | Regulowana jasność podświetlenia (sterowana z HMI) |

---

## 11. Rejestr ryzyk i założeń

**Przebudowany 20.09.2026** (audyt F-029). Poprzednia wersja nie wskazywała, kto ryzyko prowadzi ani co uznajemy za dowód jego zamknięcia — ryzyko mogło więc zostać „zamknięte" dowolnym stwierdzeniem.

Zasady rejestru:
- **Właściciel** — osoba, która doprowadza ryzyko do zamknięcia. W dwuosobowym zespole podział jest prosty: **Paweł** prowadzi wszystko, co wymaga pomiaru, zakupu, dostępu do motocykla lub decyzji biznesowej; **Claude** prowadzi analizy, specyfikacje i dokumentację. Właściciel nie zawsze wykonuje pracę sam, ale odpowiada za domknięcie.
- **Dowód zamknięcia** — konkretny artefakt (protokół, pomiar, zapis decyzji). Bez niego ryzyko pozostaje otwarte, niezależnie od przekonania, że „powinno być dobrze".
- **Bramka** — najpóźniejszy moment, w którym ryzyko musi być zamknięte lub świadomie zaakceptowane na piśmie.
- Status: **Otwarte** · **W trakcie** · **Zaakceptowane** (świadomie, z uzasadnieniem) · **Zamknięte** (dowodem).

| # | Ryzyko | Wpływ | Właściciel | Działanie ograniczające | Dowód zamknięcia | Bramka | Status |
|---|---|---|---|---|---|---|---|
| R1 | **Live tuning na pracującym silniku** — błędna lub zbyt gwałtowna zmiana mapy może uszkodzić silnik | Wysoki (zniszczenie silnika) | Claude (specyfikacja) → Paweł (weryfikacja) | Interlocki w FW: lista dozwolonych parametrów, limit szybkości zmiany, blokada powyżej progu obrotów (ECU-SAF-011) | Protokół T-SAF-011: udokumentowana próba zmiany parametru spoza listy i powyżej progu, obie odrzucone | G3 (Faza 7) | Otwarte |
| R2 | **Zakłócenia EMI z instalacji zapłonowej** — błędne odczyty czujników lub reset MCU | Wysoki (nieprzewidywalne działanie) | Claude (projekt ochrony) → Paweł (pomiar) | Czterowarstwowa strategia ochrony (rozdz. 6.2d); separacja obwodów mocy i sygnałowych w layoucie | Protokół T-COM-001 (stopa błędów CAN przy pracującym zapłonie) + protokół T-SEN-001 na pracującym silniku (Faza 8) | G4 (Faza 8) | Otwarte |
| R3 | **Wymiary złącza Molex CMC 28** — nie potwierdzone kartą katalogową, czy zmieści się w planowanej obudowie | Średni (przeprojektowanie obudowy) | Paweł | Weryfikacja wymiarów z karty katalogowej i modelu 3D **przed** rozpoczęciem layoutu | Zapis w dokumentacji: wymiary z karty katalogowej + rysunek obudowy z zachowanymi odstępami | G2 (Faza 4) | Otwarte |
| R4 | **Typ czujnika prędkości koła** — założono pasywny (kontaktron lub Hall z otwartym kolektorem); jeśli wymaga zasilania, potrzebny dodatkowy pin | Niski (zapas pinów w LQFP100) | Paweł | Pomiar na fabrycznym czujniku Bety 300RR | Protokół pomiarowy: typ sygnału, poziomy, zapotrzebowanie na zasilanie | G2 (Faza 4) | Otwarte |
| R5 | **Parametry sterowania wtryskiwaczami TPI/TBI** — rezystancja znana (11,7 Ω nom., 10,5–13,0 Ω), ale czas martwy i prąd podtrzymania nie zostały zmierzone na fizycznym egzemplarzu | Niski (korekta tabeli w FW, bez zmian sprzętowych) | Paweł | Pomiar na fizycznym wtryskiwaczu (F-014); driver TLE9104SH ma zapas prądowy 3 A/kanał wobec ~1,23 A wymaganych | Protokół T-INJ-004: tabela czasu martwego w funkcji napięcia | G3 (Faza 6) | W trakcie — rezystancja ustalona 12.09.2026, pomiar pozostaje |
| R6 | **Dostępność czopu bębna zmiany biegów w silnikach 2T** — potwierdzone dla 4T (KTM 500 EXC-F), nieznane dla 2T | Średni (brak wskaźnika biegu na części silników) | Paweł | Oględziny fizyczne Bety 300RR; wariant zapasowy: rezygnacja ze wskaźnika biegu w MVP-A | Zdjęcie lub pomiar z demontażu + zapis decyzji o zakresie funkcji | G1 (Faza 2-ECU) | Otwarte |
| R7 | **Testy z prawdziwym silnikiem dopiero w Fazie 8** — problemy widoczne tylko przy realnych zakłóceniach wyjdą późno | Średni (koszt iteracji rev B) | Paweł | Świadomie zaakceptowane; Faza 10 (rev B) jest siatką bezpieczeństwa. Ograniczenie: maksymalnie dużo weryfikacji przeniesione na stanowisko (57 testów w Fazie 6) | Zapis decyzji z uzasadnieniem — obecny akapit | — | Zaakceptowane 2026-08-31 |
| R8 | **Czytelność wyświetlacza w pełnym słońcu** — 1000 cd/m² deklarowane, nie zweryfikowane w warunkach docelowych | Średni (użyteczność produktu) | Paweł | Panel o wysokiej jasności + obudowa aluminiowa w jasnym kolorze; daszek przeciwsłoneczny do rozważenia | Protokół T-UI-005: test na słońcu wg kryterium przyjętego w Fazie 3 | G5 (Faza 9) | Otwarte |
| R9 | **Pobór prądu w trybie uśpienia** — ECU stale podłączone do akumulatora; zbyt wysoki pobór rozładuje akumulator przy postoju | Wysoki (motocykl nie odpali po tygodniu) | Claude (architektura) → Paweł (pomiar) | Architektura uśpienia B (rozdz. 6.4); szacunek analityczny 70–135 µA dla ECU+HMI wobec limitu 250 µA (SYS-PWR-002) | Protokoły T-PWR-001 i T-PWR-002: pomiar prądu miernikiem z zakresem µA | G3 (Faza 6) | Otwarte |
| R10 | **Czujnik fazy wałka rozrządu w 4T** — brak potwierdzenia, czy występuje w jednocylindrowych enduro; wniosek z rozumowania inżynierskiego, nie z dokumentacji serwisowej | Niski (pin zarezerwowany, tryb batch działa bez niego) | Paweł | Weryfikacja schematem serwisowym konkretnego modelu 4T | Wyciąg ze schematu serwisowego lub zapis decyzji o rezygnacji z wariantu 4T w MVP | G4 (przed Fazą 8) | Otwarte |
| R11 | ~~Utrata funkcji kickstartu przy rozładowanym akumulatorze~~ | — | Claude | Ponowna analiza: ECU pracuje do ~7 V, ścieżka stator→prostownik już istnieje, wystarcza kondensator buforowy + kompensacja czasu ładowania cewki | Analiza zapisana w rozdz. 6.4 i pozycji L6; weryfikacja pomiarowa wchodzi w T-ENV-002 | — | **Zamknięte 2026-08-31** (analizą; pomiar potwierdzający w T-ENV-002) |
| R12 | **Kill switch zależny od firmware** — pierwotnie nie był sprzętowym fail-safe | Wysoki (bezpieczeństwo) | Claude (projekt) → Paweł (weryfikacja) | **Zmiana po audycie:** wprowadzono sprzętowe bramkowanie wejść EN driverów sygnałem kill switcha (ECU-SAF-001), niezależne od stanu firmware. Okno watchdoga ~100 ms jako druga warstwa | Protokół T-SAF-001: odcięcie przy zawieszonym firmware, z pomiarem czasu. **Dopóki ten protokół nie istnieje, ryzyko pozostaje otwarte** | G2 (schemat), G3 (pomiar) | Otwarte — zmieniony charakter: z „zaakceptowane warunkowo" na „rozwiązane w projekcie, do potwierdzenia pomiarem" |
| R13 | ~~Budżet energetyczny nieprzeanalizowany~~ | — | Claude | Analiza w rozdz. 6.8: ECU+HMI <4 W przy statorze 150–200 W | Analiza w rozdz. 6.8; pomiar weryfikacyjny w Fazie 6 | — | **Zamknięte 2026-08-31** (analizą) |
| R14 | **Odprowadzanie ciepła z ECU** — 5,5 W strat w szczelnej obudowie; przy niedostatecznym kontakcie termicznym temperatura wewnątrz przekracza 84 °C | Średni (skrócenie żywotności komponentów) | Claude (analiza) → Paweł (wykonanie obudowy) | Obudowa aluminiowa z padami lub pastą (wymóg, rozdz. 10); skracanie czasu ładowania cewki przy wysokich obrotach (ECU-IGN-004) — dominujące źródło strat | Protokół T-IGN-004 + pomiar termiczny wnętrza obudowy w Fazie 6; pełny łańcuch termiczny złącze→PCB→obudowa→otoczenie do udokumentowania | G3 (Faza 6) | Otwarte |
| R15 | **Przegrzanie wyświetlacza HMI na słońcu** — panel czernieje powyżej ~70 °C; analiza (rozdz. 7.2) daje 76 °C nawet przy obudowie aluminiowej | Wysoki (utrata funkcji HMI) | Claude (analiza) → Paweł (obudowa, pomiar) | Obudowa aluminiowa + jasny kolor (wymóg, rozdz. 10); czujnik temperatury + ograniczanie jasności (HMI-UI-004); daszek do rozważenia | Protokół T-UI-004 (charakterystyka ograniczania) + pomiar temperatury panelu na słońcu w Fazie 9 | G3 (pomiar), G5 (słońce) | Otwarte |
| **R16** | **Brak planu wyposażenia stanowiska pomiarowego** — 57 z 70 testów przypada na Fazę 6, a część wymaga sprzętu, którego nie ma: komora klimatyczna (T-ENV-003), wstrząsarka (T-ENV-006), automatyczne zbieranie 10⁵ pomiarów kąta (T-IGN-002), miernik z zakresem µA (T-PWR-001) | Wysoki (Faza 6 zatrzyma się na braku sprzętu, wykryte dopiero w jej trakcie) | Paweł | Zestawienie potrzebnego wyposażenia z kosztem i wariantem zastępczym (usługa zewnętrzna, wypożyczenie, uproszczony test) — **do wykonania w Fazie 3 razem z planem testów** | Zestawienie wyposażenia z decyzją zakup/usługa/rezygnacja dla każdej pozycji | G2 (przed Fazą 4) | **Otwarte — nowe 20.09.2026**, wykryte przy przebudowie tabeli pokrycia |
| **R17** | **Jedno źródło zaopatrzenia dla MAX9926UAEE/V+** — układ niedostępny w TME, wyłącznie Mouser/Farnell/DigiKey, czyli import spoza UE | Średni (czas dostawy, cło, ryzyko przy produkcji serii) | Paweł | Sprawdzenie dostępności i minimalnej partii u dystrybutorów; rozważenie zapasu magazynowego na serię pilotażową | Potwierdzona dostępność i cena przy zakładanej wielkości serii, zapisane w przeglądzie komponentów | G2 (Faza 4, BOM) | **Otwarte — nowe 20.09.2026** |
| **R18** | **Zakres funkcji bez wymagań** — **zredukowane 29.09.2026 do bootloadera** (quickshifter usunięty z zakresu). Bootloader jest w zakresie produktu, ale nie ma żadnego sprawdzalnego wymagania (rozdz. 14.11); oba dotykają bezpieczeństwa lub użyteczności podstawowej | Wysoki (funkcja zaprojektowana „z głowy", bez kryterium odbioru) | Claude | Uzupełnienie wymagań przed bramką G0, razem z domykaniem pozycji `[DO USTALENIA]` | Wymagania z wartościami i metodą weryfikacji w `wymagania.md` + wiersze w tabeli pokrycia | **G0** | **Otwarte — nowe 20.09.2026** |

### 11.1 Bilans rejestru ryzyk

| Status | Liczba |
|---|---|
| Otwarte | 14 |
| W trakcie | 1 (R5) |
| Zaakceptowane świadomie | 1 (R7) |
| Zamknięte dowodem | 2 (R11, R13) |
| **Razem** | **18** |

Ryzyka o wpływie wysokim: R1, R2, R9, R12, R15, R16, R18 — **żadne nie jest zamknięte**. Wszystkie mają przypisany dowód zamknięcia i bramkę, więc żadne nie przejdzie niezauważone przez kolejne fazy.


### 11.2 Rejestr założeń (wprowadzony 11.10.2026, luka L35)

**Po co osobny rejestr.** Luki opisują to, czego nie wiemy i wiemy, że nie wiemy. Ryzyka opisują to, co może pójść źle. **Założenie to twierdzenie przyjęte za prawdziwe bez weryfikacji, na którym zbudowano inne ustalenia** — najgroźniejsza z trzech kategorii, bo nie wygląda na pozycję otwartą.

Rejestr powstał po stwierdzeniu, że założenia projektu siedziały wyłącznie w prozie i żadne nie było oznaczone jako wymagające potwierdzenia. **Pierwsza wpisana pozycja okazała się fałszywa w dniu utworzenia rejestru.**

Zasady:
- Każde założenie ma **właściciela**, **sposób potwierdzenia** i **wskazanie, co się zawali, jeśli jest fałszywe**
- Status: **Niepotwierdzone** · **Potwierdzone** (z dowodem) · **Obalone** (z zakresem skutków)
- Założenie obalone **nie jest usuwane** — zostaje razem z listą rzeczy, które przez nie trzeba było poprawić

| # | Założenie | Na czym stoi | Co się zawali, jeśli fałszywe | Właściciel | Sposób potwierdzenia | Status |
|---|---|---|---|---|---|---|
| **Z1** | ~~Beta 300 RR 2015 ma czujnik położenia przepustnicy~~ | Decyzja 2.7 zapisana jako fakt, nigdy nieweryfikowana | Mapa zapłonu 2D dla MVP-A, strategia zastępcza przy utracie TPS, interlock live tuningu oparty na obciążeniu, pin w złączu | Paweł | Oględziny motocykla | ❌ **OBALONE 11.10.2026** — motocykl nie ma TPS i nie będzie dokładany. Skutki w rozdz. 11.3 |
| **Z2** | Czas ładowania cewki wynosi ok. 3 ms | Wartość typowa dla cewek motocyklowych, przyjęta do wszystkich rachunków wypełnienia i strat cieplnych | Analiza termiczna (rozdz. 6.8), tabela startu ładowania w C.1.5, wniosek o obudowie aluminiowej | Paweł | Pomiar na docelowej cewce, Faza 6 | 🟡 Niepotwierdzone |
| **Z3** | Kickstarter obraca wał kilkakrotnie w jednym ruchu nogi | Rozumowanie o przełożeniu mechanizmu, bez pomiaru | ECU-IGN-019 — iskra od drugiego przejścia wypustu. Jeśli kopnięcie daje jeden obrót, silnik nie odpali | Paweł | Policzenie obrotów koła magnesowego przy kopnięciu | 🟡 Niepotwierdzone |
| **Z4** | Typowe wyprzedzenie zapłonu dwusuwu 300 mieści się w zakresie 0–25° przed GMP | Wiedza ogólna o silnikach tej klasy, bez danych dla tego silnika | Limit geometryczny 28° (ECU-IGN-015). Jeśli silnik potrzebuje więcej, geometria koła nie pozwala na dokładne wyzwalanie | Paweł | Strojenie w Fazie 8; wniosek pośredni: fabryczne CDI pracuje na tym samym kole | 🟡 Niepotwierdzone |
| **Z5** | Szczelina 0,18 mm jest wartością fabryczną, nie stanem tego egzemplarza | Pomiar jednego motocykla | Oszacowanie amplitudy sygnału VR i dobór obwodu wejściowego MAX9926 | Paweł | Instrukcja serwisowa Beta albo pomiar drugiego egzemplarza | 🟡 Niepotwierdzone |
| **Z6** | Wtryskiwacze KTM TPI/TBI mają 11,7 Ω nominalnie | Dane z internetu, nie z pomiaru | Dobór TLE9104SH i decyzja o trybie nasyconym zamiast peak-and-hold | Paweł | Pomiar na fizycznym wtryskiwaczu (pozycja audytu F-014) | 🟡 Niepotwierdzone |
| **Z7** | Stator Bety oddaje 150–200 W | Wartość typowa dla klasy, nie z dokumentacji tego motocykla | Budżet energetyczny (rozdz. 6.8) i wniosek, że szczyt 151 W się domyka | Paweł | Instrukcja serwisowa albo pomiar | 🟡 Niepotwierdzone |
| **Z8** | Czujnik prędkości koła jest pasywny i nie wymaga zasilania | Założenie przy bilansie pinów | Bilans pinów złącza; przy czujniku aktywnym potrzebny dodatkowy pin | Paweł | Pomiar na motocyklu (ryzyko R4) | 🟡 Niepotwierdzone |
| **Z9** | Czop bębna zmiany biegów jest dostępny w silniku 2T tak jak w 4T | Potwierdzone dla KTM 500 EXC-F, przeniesione na Betę bez weryfikacji | Wskaźnik biegu, adaptacja czasu cięcia, wykrywanie zablokowanej dźwigni — **ostatnie dwa odpadły razem z quickshifterem** | Paweł | Oględziny Bety (ryzyko R6) | 🟡 Niepotwierdzone |
| **Z10** | Dwusuw pali co obrót, więc jeden wypust na obrót wystarcza i nie trzeba rozpoznawać fazy | Zasada działania silnika dwusuwowego | Cała architektura triggera C.1; brak czujnika wałka rozrządu | Claude | Potwierdzenie przy pierwszym uruchomieniu na stanowisku | 🟢 Potwierdzone rozumowaniem — zasada działania silnika, nie dane |

**Zasada na przyszłość:** każde twierdzenie o motocyklu, komponencie lub zjawisku fizycznym, którego nie potwierdza pomiar, karta katalogowa ani dokumentacja serwisowa, trafia do tego rejestru **w chwili, gdy zostaje użyte jako podstawa decyzji**.

---

### 11.3 Skutki obalenia założenia Z1 — brak TPS w MVP-A

Beta 300 RR 2015 nie ma czujnika położenia przepustnicy, a fabryczny układ zapłonowy pracuje wyłącznie z sygnału obrotów. **Decyzja Pawła z 11.10.2026: TPS nie będzie dokładany.**

Wbrew pierwszemu wrażeniu szkody są ograniczone, bo wymaganie podstawowe ECU-IGN-001 od początku mówiło o mapie kąta **w funkcji obrotów**. Dwuwymiarowość weszła bokiem, przez wymagania opisujące zachowanie przy utracie sygnału, którego w tym wariancie nigdy nie było.

| Zapis | Było | Jest |
|---|---|---|
| Decyzja 2.7 | „Beta 300RR (2015), 1-cyl. 2T, gaźnik **+ TPS**" | „gaźnik, **bez TPS**" |
| ECU-IGN-008 **[A]** | Strategia zastępcza przy utracie sygnału przepustnicy w wariancie gaźnikowym | **Usunięte** — nie ma sygnału, który można utracić |
| **ECU-IGN-020** | — | **Nowe:** mapa zapłonu MVP-A jest jednowymiarowa, kąt wyłącznie w funkcji obrotów |
| DTC-SEN-04 **[A]** | Usterka przepustnicy, wariant gaźnikowy | **Usunięte** |
| ECU-SEN-003 | Błąd pomiaru TPS — bez oznaczenia wariantu | Przeniesione do **[HW]** — zdolność sprzętowa dla wariantów B/C |
| B.3.1, grupa G3 | Utrata sygnału obciążenia: przepustnica lub szyna 5 V | W MVP-A zostaje **wyłącznie przypadek szyny 5 V** |
| Punkt G, kalibracja | „TPS (min/max)" w zakresie kalibracji | Dotyczy wyłącznie wariantów z TPS |
| SYS-COM-002a | Dane szybkozmienne: obroty, **przepustnica**, prędkość | W MVP-A przepustnica nie jest nadawana |

**Jedna konsekwencja wymaga osobnej decyzji i jest pozostawiona otwarta.** Interlock live tuningu (ECU-SAF-011, B.5.2) blokuje zmiany map przy jednoczesnym spełnieniu warunku obrotów **i** otwarcia przepustnicy powyżej 60%. **W MVP-A drugiego warunku nie da się ocenić.** Możliwe drogi: blokada wyłącznie od obrotów (mniej precyzyjna, blokuje też tam, gdzie nic nie grozi), blokada każdej zmiany przy pracującym silniku w wariancie bez TPS (najbezpieczniejsza, odbiera funkcję strojenia na żywo), albo pozostawienie samego limitu szybkości zmiany (ryzyko R1 wraca). **Pozycja do rozstrzygnięcia przed zamknięciem punktu C.**

**Wniosek procesowy:** założenie Z1 przetrwało w dokumentacji od Fazy 0 do dziś i zdążyło zrodzić cztery zapisy. Rejestr założeń wyłapał je w pierwszej godzinie istnienia — to jest argument za tym, żeby prowadzić go od początku następnego projektu, a nie po pierwszym audycie.


---

## 12. Kwestia regulacyjna

Homologacja pojazdu nie dotyczy (produkt offroad/motorsport, nie do ruchu drogowego). Sprzedaż urządzenia elektronicznego w UE może jednak wiązać się z obowiązkami niezależnymi od homologacji (CE/EMC, RoHS, WEEE). **Do sprawdzenia z kimś kompetentnym przed Fazą 12 (produkcja/sprzedaż)** — nie blokuje obecnych prac. Claude nie jest prawnikiem ani rzeczoznawcą.

---

## 13. Dokumenty powiązane

Pełny spis dokumentów projektu z wersjami, statusami i właścicielami — **rozdz. 0.2**. Utrzymywany jest jeden spis, żeby dwie listy nie zaczęły się rozjeżdżać.

Hierarchia:
- `proces-rozwoju-ecu.md` (DOC-001) — dokument główny; w razie sprzeczności rozstrzyga on, z jednym wyjątkiem niżej
- `plan-naprawczy-audyt.md` (DOC-006) — **nadrzędny w zakresie pozycji audytu do czasu zamknięcia wszystkich pozycji P0 i P1 z części naprawczej**
- pozostałe dokumenty są podrzędne wobec DOC-001

---

## 14. Tabela pokrycia wymagań (traceability)

**Przebudowana 20.09.2026** (audyt F-012). Poprzednia wersja wychodziła od nazw funkcji i wskazywała fazy zamiast testów — nie dało się z niej odczytać, czy konkretne wymaganie jest pokryte ani czym zostanie udowodnione.

Łańcuch: **wymaganie → realizacja sprzętowa → moduł firmware → identyfikator testu → dowód**.

Zasady:
- Punktem wyjścia jest identyfikator wymagania z `wymagania.md`. Funkcja, która nie ma wymagania, nie może być prześledzona — takie przypadki zebrano w rozdz. 14.11.
- **ID testu**: `T-[OBSZAR]-[NUMER]`, numeracja odpowiada wymaganiu (ECU-IGN-002 → T-IGN-002). Jeden test może pokrywać kilka wymagań; wtedy ten sam identyfikator powtarza się w wierszach. Treść testów powstaje w Fazie 3 (plan testów).
- **Moduł FW**: punkt specyfikacji `faza2-fw-specyfikacja.md` (A–J). Kreska oznacza wymaganie realizowane wyłącznie sprzętowo lub poza firmware ECU.
- **Dowód**: konkretny artefakt zamykający wymaganie. Dopóki nie istnieje, wiersz pozostaje otwarty.
- **Faza**: faza, w której test jest wykonywany. Wypełnienie kolumny „Dowód" dla wszystkich wierszy przypisanych do danej fazy jest warunkiem wyjścia z jej bramki (rozdz. 3.0).

Status: ⬜ niewykonane · 🔶 częściowo · ✅ zamknięte dowodem.

### 14.1 Warunki pracy

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| SYS-ENV-001 | Przetwornice 5,0 V i 3,3 V (6.2b), ochrona wejścia (6.2d) | — | T-ENV-001 | Protokół pomiarowy: przemiatanie 9→16 V z zasilacza laboratoryjnego, kontrola pełnego zestawu funkcji | 6 | ⬜ |
| SYS-ENV-002 | Jw. + kondensator buforowy | B (degradacja) | T-ENV-002 | Protokół: 7→18 V, potwierdzenie zachowania sterowania silnikiem i zapisu usterki | 6 | ⬜ |
| SYS-ENV-003 | Komponenty w klasie −40…+125 °C, obudowa aluminiowa | — | T-ENV-003 | Protokół z komory klimatycznej — **sprzęt niedostępny, do zaplanowania (luka L30)** | 6 | ⬜ |
| SYS-ENV-004 | Dobór komponentów | — | T-ENV-004 | Zestawienie zakresów temperatur z kart katalogowych całego BOM (analiza) | 4 | ⬜ |
| SYS-ENV-005 | Obudowa + Molex CMC 28 + Deutsch DTM | — | T-ENV-005 | Protokół próby zanurzeniowej 1 m / 30 min wg IP67 | 6 | ⬜ |
| SYS-ENV-006 | Mocowanie PCB, podparcie elementów ciężkich | — | T-ENV-006 | Profil wibracji przyjęty w Fazie 3 + protokół testu na wstrząsarce lub przejazd pomiarowy | 3 (profil), 9 (test) | ⬜ |
| SYS-ENV-007 | MAX9926UAEE/V+ + HRTIM w STM32G474VET3 | C | T-ENV-007 | Protokół: generator sygnału VR, 200–10 000 obr/min, zliczanie zgubionych zębów | 6 | ⬜ |

### 14.2 Zapłon

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| ECU-IGN-001 | VBG08H-E, HRTIM | C | T-IGN-001 | Protokół: kąt zadany z mapy vs zmierzony na wyjściu drivera | 6 | ⬜ |
| **ECU-IGN-002** | VBG08H-E, HRTIM (**impuls generowany przez peryferium, nie przez program** — spec. FW B.2.3), MAX9926, STM32G474VET3 | C + I (priorytety przerwań) | **T-IGN-002** | **Histogram błędu z min. 10⁵ zapłonów, oscyloskop, przy jednoczesnej pracy logowania, CAN i USB. Test krytyczny dla bramki G2** | 6 | ⬜ |
| ECU-IGN-003 | Pomiar VBAT (dzielnik + ADC + VREFINT) | C | T-IGN-003 | Protokół: prąd cewki w funkcji napięcia 7–16 V | 6 | ⬜ |
| ECU-IGN-004 | VBG08H-E (ograniczenie prądu, diagnostyka termiczna) | C | T-IGN-004 | Pomiar temperatury drivera przy maksymalnych obrotach i najwyższym napięciu | 6 | ⬜ |
| ECU-IGN-005 | **Rejestr okresu HRTIM jako sufit sprzętowy** (kasowanie wyjścia zdarzeniem porównania oraz końcem okresu) + ograniczenie prądu w VBG08H-E | — (niezależne od FW) | T-IGN-005 | Test wstrzykiwania usterki: zawieszenie firmware z wyjściem w stanie aktywnym oraz zapis błędnej wartości porównania; pomiar długości impulsu w obu przypadkach | 6 | ⬜ |
| ECU-IGN-006 | — | C | T-IGN-006 | Protokół: odcięcie i powrót przy zadanym progu, stanowisko + silnik | 6, 8 | ⬜ |
| ECU-IGN-006a | — | C + D (walidacja zakresu) + aplikacja | T-IGN-006a | Protokół: odrzucenie wartości spoza 50–500 obr/min po stronie aplikacji **i** po stronie ECU | 7 | ⬜ |
| **ECU-IGN-020** | — (brak TPS w MVP-A) | C + D | T-IGN-020 | Przegląd struktury mapy: jedna oś, obroty (inspekcja) + protokół na stanowisku potwierdzający, że kąt zależy wyłącznie od obrotów | 5, 6 | ⬜ |
| **ECU-IGN-012** | **Koło magnesowe Beta 300 RR: 1 wypust, 30°, krawędź spływu w GMP** (zmierzone) + MAX9926 | C.1.1 + G (kalibracja) | T-IGN-012 | Przegląd struktur danych: geometria jako parametr kalibracyjny, nie stała (inspekcja) + test z podmienioną geometrią na stanowisku | 5, 6 | ⬜ |
| **ECU-IGN-013** | HRTIM + wejście przechwytujące w STM32G474VET3 | C.1.3 | T-IGN-013 | Protokół: generator sygnału VR z wymuszonym przyspieszaniem i zwalnianiem; porównanie modelu kąta z sygnałem odniesienia | 6 | ⬜ |
| **ECU-IGN-014** | MAX9926 + przechwytywanie obu krawędzi wypustu | C.1.4 | T-IGN-014 | Protokół: porównanie estymaty z interwału wypustu i ze średniej z obrotu wobec sygnału odniesienia, przy niskich obrotach z tętnieniem | 6 | ⬜ |
| **ECU-IGN-015** | — (niezależne od mapy) | C.1.9 + D (walidacja) | T-IGN-015 | Protokół: mapa zadająca 35° — potwierdzenie ograniczenia do 28° i zapisu zdarzenia | 6 | ⬜ |
| **ECU-IGN-016** | — | C.2 + D | T-IGN-016 | Protokół strojenia z obserwacją detonacji; kryterium: brak detonacji przy pełnym obciążeniu w całym zakresie | 8 | ⬜ |
| **ECU-IGN-017** | Filtr cyfrowy wejścia + adaptacyjny próg MAX9926 + bramkowanie programowe | C.1.6 | T-IGN-017 | **Protokół wstrzykiwania zakłóceń:** impulsy imitujące zbocze w fazie, w której wypust nie może wystąpić — potwierdzenie, że są odrzucone **i że iskra nie została utracona**. Osobno test negatywny: brak odrzucania ważnych zboczy przy gwałtownym przyspieszaniu | 6, 8 | ⬜ |
| **ECU-IGN-018** | Jw. | C.1.7 | T-IGN-018 | Protokół: naruszenie każdego z trzech kryteriów osobno; kontrola klasy reakcji (K0 pojedyncze, K4 powtarzalne) | 6 | ⬜ |
| **ECU-IGN-019** | — | C.1.8 | T-IGN-019 | Protokół: rozruch z pomiarem, która iskra jest pierwsza; osobno **restart w ruchu** z potwierdzeniem natychmiastowej iskry z mapy | 6, 8 | ⬜ |
| ECU-IGN-007 | — | D | T-IGN-007 | Przegląd formatu mapy w specyfikacji struktur danych (inspekcja) | 3 | ⬜ |

### 14.3 Wtrysk

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| ECU-INJ-001 | TLE9104SHXUMA1 (2 z 4 kanałów) | C | T-INJ-001 | Protokół obciążeniowy: prąd ciągły 1,5 A/kanał, temperatura układu | 6 | ⬜ |
| ECU-INJ-002 | TLE9104SHXUMA1 | C | T-INJ-002 | Oscylogram prądu na wtryskiwaczu wzorcowym 11,7 Ω oraz skrajnych 10,5 i 13,0 Ω | 6 | ⬜ |
| ECU-INJ-003 | Timer w STM32G474VET3 | C | T-INJ-003 | Pomiar szerokości impulsu na wyjściu drivera: rozdzielczość i powtarzalność | 6 | ⬜ |
| ECU-INJ-004 | Pomiar VBAT | C + D (tabela korekt) | T-INJ-004 | Pomiar czasu martwego na fizycznym wtryskiwaczu w funkcji napięcia (F-014) | 6 | ⬜ |
| **ECU-INJ-007** | — | C + B (B.3.2) | T-INJ-007 | Protokół: wymuszona usterka TPS na stanowisku, pomiar składu mieszanki analizatorem spalin przy otwartej przepustnicy; potwierdzenie, że mieszanka jest bogata, nie uboga | 6, 8 | ⬜ |
| ECU-INJ-005 | BTS7008-2EPA (kanał pompy) | A.3 | T-INJ-005 | Oscylogram załączenia pompy przy wejściu w stan GOTOWOŚĆ | 6 | ⬜ |
| ECU-INJ-006 | BTS7008-2EPA | B | T-INJ-006 | Protokół: brak obrotów → wyłączenie pompy w zadanym czasie | 6 | ⬜ |

### 14.4 Czujniki

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| ECU-SEN-001 | MAX9926UAEE/V+ + ochrona wejścia | C | T-SEN-001 | Protokół: generator + cewka VR, od 50 mV do 100 V szczytowo, zliczanie błędów detekcji | 6 | ⬜ |
| ECU-SEN-002 | Osobna ścieżka Hall (zworka), z pominięciem MAX9926 | C + D | T-SEN-002 | Protokół: praca z czujnikiem Halla, weryfikacja przełączenia zworką | 6 | ⬜ |
| ECU-SEN-003 | ADC + szyna 5,00 V ±2% | C + G (kalibracja) | T-SEN-003 | Protokół: potencjometr wzorcowy, błąd po kalibracji w całym zakresie | 6 | ⬜ |
| ECU-SEN-004 | ADC + rezystor podciągający | C | T-SEN-004 | Protokół: rezystory wzorcowe odwzorowujące 0–120 °C, porównanie z tabelą czujnika | 6 | ⬜ |
| ECU-SEN-005 | ADC + rezystor podciągający | C | T-SEN-005 | Jw. dla zakresu −20…+80 °C | 6 | ⬜ |
| ECU-SEN-006 | Dzielnik + ADC + VREFINT | C | T-SEN-006 | Protokół: porównanie z miernikiem wzorcowym w zakresie 7–16 V | 6 | ⬜ |
| ECU-SEN-007 | Podciągnięcia/ściągnięcia na wejściach czujnikowych; progi < 3% i > 97% zakresu (spec. FW B.2.1) | E | T-SEN-007 | Protokół wstrzykiwania usterek: rozwarcie i zwarcie każdego wejścia, kontrola zgłoszonego kodu | 6 | ⬜ |
| ECU-SEN-008 | MLX90316 na bębnie zmiany biegów | G + D | T-SEN-008 | Protokół: 200 zmian biegu na silniku, licznik błędów rozpoznania | 8 | ⬜ |
| ECU-SEN-009 | MLX90316 | C/G | T-SEN-009 | Oscylogram + log: zmiana 1↔2 z pomiarem czasu, brak zgłoszenia pozycji neutralnej | 8 | ⬜ |
| ECU-SEN-010 | Wejście z podciągnięciem | C | T-SEN-010 | Protokół: porównanie z odcinkiem pomiarowym o znanej długości | 8 | ⬜ |
| ECU-SEN-011 | Pomiar szyny 5 V przez ADC | C | T-SEN-011 | Protokół: wymuszona zmiana napięcia szyny, potwierdzenie stałości wskazania TPS | 6 | ⬜ |

### 14.5 Zasilanie i tryb uśpienia

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| ECU-PWR-001 | Architektura uśpienia (6.4): przełącznik obciążenia 5 V, TJA1043 w Standby, W25Q64 w deep power-down | A | T-PWR-001 | Protokół pomiaru prądu (miernik z zakresem µA) przy 12,0 V i +25 °C | 6 | ⬜ |
| SYS-PWR-002 | Jw. + uśpienie HMI (7.1) | A + J | T-PWR-002 | Protokół pomiaru prądu całego zestawu | 6 | ⬜ |
| ECU-PWR-003 | — | A + A.4 | T-PWR-003 | Oscylogram: zbocze źródła wybudzenia → pierwszy impuls na wyjściu drivera zapłonu | 6 | ⬜ |
| ECU-PWR-003a | — | A + B (B.2.5) | T-PWR-003a | Protokół: czas i zakres autotestu pełnego vs skróconego, log przyczyny wyboru; pomiar czasu sumy kontrolnej map | 6 | ⬜ |
| ECU-PWR-004 | — | A | T-PWR-004 | Protokół: pomiar czasu do zaśnięcia, 10 powtórzeń | 6 | ⬜ |
| HMI-PWR-005 | Sterowanie podświetleniem przez BT817Q | J | T-PWR-005 | Protokół: pomiar czasu wygaszenia | 6 | ⬜ |
| ECU-PWR-006 | Dzielnik rezystorowy nastawy przetwornic (brak DAC i potencjometru cyfrowego) | — | T-PWR-006 | Przegląd schematu: potwierdzenie braku ścieżki sterowania nastawą z MCU (inspekcja) | 4 | ⬜ |
| ECU-PWR-007 | ADC na obu szynach + sygnały Power Good | B | T-PWR-007 | Protokół: wymuszone zaniki i przeciążenia szyn, kontrola reakcji | 6 | ⬜ |
| ECU-PWR-008 | Przetwornica 5,0 V o stałej nastawie | — | T-PWR-008 | Protokół: pomiar napięcia przy skrajnym obciążeniu i w skrajnych temperaturach | 6 | ⬜ |
| **ECU-PWR-008a** | ADC szyny 5 V + Power Good | B (B.2.4) | T-PWR-008a | Protokół: regulowane zasilanie szyny czujników w zakresie 4,3–5,7 V; potwierdzenie granic obu reakcji i **poprawnej przyczyny w logu** przy zaniku | 6 | ⬜ |
| **ECU-PWR-009** | Pomiar VBAT + BTS7008-2EPA (kanał wentylatora) | B (DTC-PWR-07) | T-PWR-009 | Protokół: podanie 17 V z zasilacza laboratoryjnego, potwierdzenie ostrzeżenia i załączenia wentylatora; kontrola histerezy przy zejściu poniżej 15,5 V | 6 | ⬜ |
| **ECU-PWR-010** | Przełącznik obciążenia 5 V + ADC szyny czujników | B (DTC-PWR-10) | T-PWR-010 | Protokół: wymuszone rozwarcie przełącznika, potwierdzenie blokady wyjścia ze stanu GOTOWOŚĆ po 3 próbach | 6 | ⬜ |

### 14.6 Bezpieczeństwo

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| **ECU-SAF-001** | Sprzętowe bramkowanie wejść EN driverów (TLE9104 EN/RESN, VBG08H-E) sygnałem kill switcha | B | **T-SAF-001** | **Test wstrzykiwania usterki: zawieszony firmware z aktywnymi wyjściami, rozwarcie kill switcha, pomiar czasu do odcięcia. Test krytyczny dla bramki G2** | 6 | ⬜ |
| ECU-SAF-002 | **Układ trzypoziomowy: rezystory w wiązce przy przycisku + podciągnięcie w ECU + komparator bramkujący** | B (B.2.5.1) + E | T-SAF-002 | Protokół: trzy przypadki — naciśnięcie przycisku, przecięcie przewodu, rozłączenie wtyczki. W każdym kontrola odcięcia **oraz** poprawności rozróżnienia w logu i komunikacie | 6 | ⬜ |
| **ECU-SAF-002a** | Jw. | B | T-SAF-002a | Protokół: pomiar czasu od zmiany stanu do zgłoszenia usterki, kontrola odporności na drgania styku | 6 | ⬜ |
| ECU-SAF-003 | TPS3430-Q1 + rezystory ściągające | B | T-SAF-003a / T-SAF-003b | Protokół: wymuszony reset watchdoga przy pracującym silniku, potwierdzenie braku samoczynnego startu. **Dwa warianty** — odblokowanie kill switchem (a) i odblokowanie z HMI (b); obie drogi muszą przechodzić przez ten sam warunek zatrzymania wału | 6 | ⬜ |
| ECU-SAF-004 | Detektor brown-out w MCU + Power Good | B | T-SAF-004 | Protokół: zapad napięcia poniżej progu, ten sam zatrzask co T-SAF-003 | 6 | ⬜ |
| ECU-SAF-005 | BMI090L | B (B.2.5.4) | T-SAF-005 | Protokół: obrót zestawu na stanowisku (próg 65°, czas 3 s) + **rejestracja kąta przechyłu podczas sesji jazdy w terenie**; kryterium zaliczenia: zero fałszywych zadziałań | 6, 8 | ⬜ |
| ECU-SAF-006 | Licznik w pamięci nieulotnej (W25Q64) | B | T-SAF-006 | Protokół: 3 wymuszone resety → stan awarii; weryfikacja zerowania dopiero po 60 s pracy silnika | 6 | ⬜ |
| **ECU-SAF-006a** | W25Q64 + rejestry domeny podtrzymywanej (superkondensator) | B (B.2.5.3) | T-SAF-006a | Protokół: wymuszony reset watchdoga, odczyt migawki aplikacją desktop, kontrola kompletu pól; powtórzenie 3× i kontrola, czy zachowane są 3 ostatnie migawki | 6 | ⬜ |
| **ECU-SAF-006b** | Rejestr domeny podtrzymywanej | I (lista zadań) + B | T-SAF-006b | Przegląd kodu: każde zadanie czasu rzeczywistego zapisuje identyfikator przy wejściu (inspekcja) + test: zawieszenie wybranego zadania i kontrola, czy migawka wskazuje właśnie je | 5, 6 | ⬜ |
| **ECU-SAF-012** | W25Q64 (suma kontrolna map) | B (B.2.5.2) | T-SAF-012 | Protokół: celowe uszkodzenie bajtu w mapach, kontrola blokady startu i treści komunikatu | 6 | ⬜ |
| **ECU-SAF-012a** | W25Q64 (suma kontrolna konfiguracji) | B (B.2.5.2) | T-SAF-012a | Protokół: celowe uszkodzenie bajtu w konfiguracji użytkownika, potwierdzenie **uruchomienia silnika** na wartościach domyślnych z ostrzeżeniem | 6 | ⬜ |
| ECU-SAF-007 | Rezystory ściągające na wszystkich wyjściach mocy | — | T-SAF-007 | Oscylogram stanu wyjść od chwili podania zasilania do końca startu MCU | 6 | ⬜ |
| **ECU-SAF-016** | **Rezystory ściągające na linii bramkującej EN** driverów | — (niezależne od FW) | T-SAF-016 | Protokół wstrzykiwania usterki: odłączenie zasilania komparatora przy pracującym silniku — potwierdzenie odcięcia, nie załączenia. Osobno: oscylogram stanu linii EN od chwili podania zasilania | 6 | ⬜ |
| **ECU-SAF-016a** | Komparator zasilany z szyny 5 V za przełącznikiem obciążenia | — | T-SAF-016a | Przegląd schematu (inspekcja) + pomiar prądu spoczynkowego w T-PWR-001 potwierdzający brak wpływu komparatora | 4, 6 | ⬜ |
| ECU-SAF-008 | BTS7008-2EPA (kanał rozrusznika) | B + A.3b | T-SAF-008 | Protokół: próba załączenia rozrusznika przy obrotach > 400 obr/min, potwierdzenie blokady | 8 | ⬜ |
| ECU-SAF-009 | BTS7008-2EPA | A.3b | T-SAF-009 | Protokół: pomiar czasu ciągłej pracy rozrusznika | 6 | ⬜ |
| ECU-SAF-010 | BTS7008-2EPA | A.3b | T-SAF-010 | Protokół: pomiar obrotów w chwili wyłączenia rozrusznika | 8 | ⬜ |
| ECU-SAF-010a | — | D (walidacja parametrów) | T-SAF-010a | Przegląd kodu i zestawu parametrów: potwierdzenie warunku 700 > 400 (inspekcja) | 5 | ⬜ |
| ECU-SAF-011 | — | B (B.5) + aplikacja | T-SAF-011 | Protokół: próba zmiany parametru spoza listy dozwolonych; próba zapisu w obszarze zablokowanym (> 5000 obr/min i > 60% przepustnicy jednocześnie) oraz tuż poza nim; próba przekroczenia limitu 2°/5% na zapis. **Weryfikacja odrzucenia po stronie ECU przy pominiętej aplikacji** | 7 | ⬜ |
| **ECU-SAF-011a** | — | B (B.5.4) | T-SAF-011a | Protokół: wymuszenie każdego z czterech wyzwalaczy przerwania sesji; kontrola powrotu map do wartości trwałych i spójności pamięci nieulotnej | 7 | ⬜ |
| **ECU-SAF-013** | — | B (B.3.3) | T-SAF-013 | Oscylogram: wymuszenie usterki K3 przy 8000 obr/min, pomiar przebiegu zjazdu limitu w czasie | 6 | ⬜ |
| **ECU-SAF-014** | — | B (B.3.1) | T-SAF-014 | Protokół: dwie jednoczesne usterki K3 o różnych limitach, potwierdzenie obowiązywania niższego bez sumowania | 6 | ⬜ |

### 14.7 Diagnostyka i logowanie

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| ECU-DIA-001 | W25Q64 + RTC w STM32G474VET3 | E | T-DIA-001 | Protokół: wymuszenie każdej usterki z macierzy, kontrola kompletu pól rekordu | 6 | ⬜ |
| ECU-DIA-002 | — | E | T-DIA-002 | Przegląd macierzy usterek: każda pozycja ma przypisaną klasę (inspekcja) | 5 | ⬜ |
| ECU-DIA-003 | TJA1043 | E | T-DIA-003 | Protokół: odłączenie HMI, pomiar czasu do zapisania zdarzenia | 6 | ⬜ |
| ECU-DIA-004 | — | A.4 + F | T-DIA-004 | Protokół: wybudzenie z każdego źródła, kontrola zapisanej przyczyny | 6 | ⬜ |
| ECU-LOG-005 | W25Q64 (8 MB — zapas na przyszłe rozszerzenie) | F | T-LOG-005 | Przegląd zakresu logowania względem karty MVP (inspekcja) | 5 | ⬜ |
| ECU-LOG-006 | W25Q64 + BMI090L | F | T-LOG-006 | Protokół: wyzwolenie zdarzenia, odczyt okna przed i po | 6 | ⬜ |
| ECU-LOG-007 | Kondensator buforowy na szynie 3,3 V | F | T-LOG-007 | Protokół: przerwanie zasilania w losowym momencie zapisu, min. 100 powtórzeń, brak uszkodzonego rekordu | 6 | ⬜ |
| ECU-LOG-008 | W25Q64 (zapis atomowy) | F | T-LOG-008 | Jw., kontrola licznika motogodzin po każdym przerwaniu | 6 | ⬜ |

### 14.8 Komunikacja

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| SYS-COM-001 | TJA1043 ×2, terminacja (6.2c) | A, J | T-COM-001 | Protokół: analizator CAN, jakość sygnału i stopa błędów przy pracującym zapłonie | 6 | ⬜ |
| SYS-COM-001a | — | H | T-COM-001a | Protokół: pomiar czasu aktualizacji firmware HMI przez CAN | 7 | ⬜ |
| SYS-COM-002 | — | Protokół (Faza 2-Desktop) | T-COM-002 | Przegląd definicji ramek + test odbioru ramki z błędną sumą kontrolną | 6 | ⬜ |
| SYS-COM-002a | — | I (harmonogram zadań) | T-COM-002a | Protokół: pomiar odstępów między ramkami analizatorem CAN, histogram | 6 | ⬜ |
| SYS-COM-002b | — | I | T-COM-002b | Jw. dla ramek wolnozmiennych | 6 | ⬜ |
| SYS-COM-003 | — | Protokół (Faza 2-Desktop) | T-COM-003 | Protokół wstrzykiwania błędów: ramki zgubione, powtórzone, przekłamane | 6 | ⬜ |
| SYS-COM-004 | — | Protokół (Faza 2-Desktop) | T-COM-004 | Przegląd specyfikacji protokołu: każda ramka cykliczna ma okres i timeout (inspekcja) | 2-Desktop | ⬜ |
| **SYS-COM-007** | TJA1043 ×2 | A.4 + J | T-COM-007 | Protokół: wybudzenie ECU każdym ze źródeł, kontrola czy HMI budzi się bez interakcji kierowcy z wyświetlaczem | 6 | ⬜ |
| SYS-COM-005 | — | H | T-COM-005 | Protokół: połączenie niezgodnych wersji, kontrola wykrycia i komunikatu | 7 | ⬜ |
| **SYS-COM-005a** | — | J (HMI) | T-COM-005a | Protokół: połączenie wersji różniących się o `minor` **i** o `major`; w obu przypadkach ekran bez danych pomiarowych | 7 | ⬜ |
| **SYS-COM-005b** | — | H | T-COM-005b | Protokół: aktualizacja pakietem zawierającym oba obrazy; przerwanie w losowym momencie i kontrola, czy zestaw wraca do spójnej pary wersji | 7 | ⬜ |
| APP-COM-006 | — | D + H + aplikacja | T-COM-006 | Protokół: przerwanie zapisu w losowym momencie, min. 50 powtórzeń, kontrola spójności konfiguracji | 7 | ⬜ |

### 14.9 Interfejs użytkownika

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| HMI-UI-001 | Drabinka rezystorowa + ADC w STM32G0B1 | J | T-UI-001 | Oscylogram: zbocze na przycisku vs sygnał z fotodiody przyłożonej do ekranu | 6 | ⬜ |
| HMI-UI-002 | RVT35HHBFWN00 + BT817Q | J | T-UI-002 | Pomiar częstotliwości odświeżania na sygnałach panelu | 6 | ⬜ |
| HMI-UI-002a | BT817Q | J | T-UI-002a | Demonstracja: nagranie ruchu wskazań przy skokowej zmianie danych | 6 | ⬜ |
| HMI-UI-003 | — | J | T-UI-003 | Protokół: przerwanie CAN, pomiar czasu do wygaszenia danych | 6 | ⬜ |
| **HMI-UI-006** | RVT35HHBFWN00 + BT817Q | J + B (B.3.4) | T-UI-006 | Protokół: wymuszenie usterki z każdej klasy, kontrola poziomu prezentacji; osobno kontrola, że pasa poziomu P2 nie da się schować | 6 | ⬜ |
| **HMI-UI-007** | — | J | T-UI-007 | Przegląd treści komunikatów: każdy komunikat poziomu P2 zawiera trzy wymagane elementy (inspekcja) | 5 | ⬜ |
| **HMI-UI-008** | — | J | T-UI-008 | Protokół: trzy jednoczesne usterki różnych klas, kontrola pierwszeństwa na ekranie i licznika w liście | 6 | ⬜ |
| HMI-UI-004 | TMP112-Q1 *(propozycja, niezweryfikowana)* | J | T-UI-004 | Protokół: nagrzewanie modułu, kontrola charakterystyki ograniczania jasności | 6 | ⬜ |
| HMI-UI-005 | Panel 1000 cd/m² + obudowa aluminiowa, jasny kolor | J | T-UI-005 | Protokół testu na słońcu wg kryterium przyjętego w Fazie 3 | 9 | ⬜ |

### 14.10 Bilans pokrycia

*Liczby skorygowane 22.09.2026. Wcześniejsze wersje bilansu podawały wartości zaniżone — skrypt kontrolny nie obejmował wymagań obszaru **UI**, bo jego wzorzec zakładał trzyliterowy kod obszaru, a `HMI-UI-xxx` ma dwuliterowy. Same wiersze w tabeli były obecne; błędna była kontrola, nie pokrycie.*

| Pozycja | Liczba |
|---|---|
| Wymagań w `wymagania.md` | 105 |
| Wymagań ujętych w tabeli pokrycia | 105 (100%) |
| Wymagań z przypisanym identyfikatorem testu | 105 (107 identyfikatorów testów — kilka wymagań weryfikowanych dwoma wariantami) |
| Wymagań zamkniętych dowodem | 0 |
| Testy w Fazie 3 (inspekcje formatu, przyjęcie profilu wibracji) | 2 |
| Testy w Fazie 4 (przegląd schematu i BOM) | 2 |
| Testy w Fazie 5 (przeglądy projektowe) | 5 |
| Testy w Fazie 6 (stanowisko) | 72 |
| Testy w Fazie 7 (aplikacja i aktualizacja) | 8 |
| Testy w Fazie 8 (silnik / motocykl) | 9 |
| Testy w Fazie 9 (warunki rzeczywiste) | 2 |
| Testy w Fazie 2-Desktop (przegląd protokołu) | 1 |

### 14.11 Funkcje w zakresie bez wymagania — luka wykryta przy przebudowie tabeli

Przebudowa ujawniła funkcje obecne w zakresie produktu (rozdz. 4.1) i w poprzedniej tabeli pokrycia, które **nie mają żadnego wymagania w `wymagania.md`**. Bez wymagania nie da się ich zweryfikować — nie wiadomo, co miałoby zostać udowodnione.

| Funkcja | Źródło zakresu | Brakujące wymagania | Priorytet |
|---|---|---|---|
| ~~Quickshifter~~ | Faza 0 | ❌ **USUNIĘTY Z ZAKRESU 29.09.2026** — funkcja wypadła z produktu wraz z wymaganiami i czujnikami. Pozycja przestała istnieć zamiast zostać domknięta | — |
| **Bootloader i aktualizacja firmware** | Faza 0, zasada procesu #12 | Warunki dopuszczające aktualizację, czas, zachowanie przy przerwaniu, automatyczny powrót do poprzedniej wersji | **P0** — przerwana aktualizacja unieruchamia motocykl |
| Sterowanie wentylatorem | Faza 0 | Progi załączenia i wyłączenia, histereza, reakcja na usterkę czujnika temperatury, praca po zgaszeniu silnika | P1 |
| Przełączanie map z HMI | Faza 0 | Liczba profili, warunki dopuszczające zmianę (obroty, praca silnika), czas przełączenia | P1 |
| Licznik przebiegu (km) | Faza 0 | Rozdzielczość, odporność na zanik zasilania, zakres | P1 |
| Korekta na wysokość n.p.m. | Faza 0, BMP390 | Zakres korekty, częstotliwość aktualizacji, zachowanie przy usterce czujnika | P1 |
| Aplikacja desktop (poza APP-COM-006) | Faza 0 | Cały obszar APP-*: edycja map, podgląd na żywo, odczyt kodów usterek, wymagania wydajnościowe | P1 — do ustalenia w Fazie 2-Desktop |
| Sterowanie światłami | Faza 0 | Obciążalność kanału, zachowanie przy przeciążeniu, sterowanie z HMI | P2 |
| Zegar czasu rzeczywistego | Faza 0 | Dokładność, podtrzymanie przy odłączonym akumulatorze, źródło synchronizacji | P2 |
| Konfigurator wyglądu HMI | Faza 0 | Zakres konfigurowalności, format, walidacja | P2 |

**Stan na 29.09.2026:** quickshifter usunięty z zakresu, więc jego pozycja P0 przestała istnieć. **Pozostaje jedna pozycja P0 — bootloader**, do zamknięcia w punkcie H specyfikacji firmware, przed bramką G0.

**Decyzja procesowa:** pozycje P0 muszą uzyskać wymagania **przed bramką G0**, razem z domykaniem pozycji `[DO USTALENIA]`. Pozycje P1 i P2 powstają w naturalnym miejscu procesu — przy punktach B, C, D i H specyfikacji firmware oraz w Fazie 2-Desktop — ale ich brak jest od teraz jawnie śledzony w tej tabeli, zamiast być odkrywanym na końcu.

Ta luka jest dokładnie tym, przed czym ostrzegała pozycja audytu F-012: poprzednia tabela wychodziła od nazw funkcji, więc każda funkcja „miała wiersz" i wyglądała na pokrytą, mimo że nie stało za nią żadne sprawdzalne wymaganie.
