# Proces — ECU „Dust ONE"

Fazy, bramki i kryteria odbioru wyrobu. Nic więcej.

**Zasady dyscypliny projektowej nie są już dokumentem.** Arkusz kwalifikacji komponentu, trzy pytania o mechanizm ochronny, analiza scenariuszy rzeczywistej jazdy, rejestracja założeń i wniosków oraz status trójstanowy stanowią instrukcję roboczą stosowaną automatycznie przy każdej propozycji. Paweł widzi **wynik** — wypełniony arkusz przy propozycji komponentu — a nie regułę do utrzymywania.

---

## 1. Podział ról

| Rola | Kto |
|---|---|
| Decyzje produktowe i techniczne, zatwierdzanie komponentów, pomiary na sprzęcie, projekt PCB i obudów | **Paweł** |
| Analiza, specyfikacja, dokumentacja, schematy i netlisty, kod, przygotowanie decyzji do zatwierdzenia | **Claude** |
| Niezależny przegląd funkcji krytycznych | **nieobsadzona — pozycja O-057** |

Analiza wspierana modelem językowym nie jest niezależnym przeglądem ludzkim. Dotyczy to także obu dotychczasowych audytów.

---

## 2. Fazy

| Faza | Zakres | Status |
|---|---|---|
| 0 | Wymagania (ECU + HMI + aplikacja) | ⬜ **otwarta** — bramka G0 zablokowana |
| 1 | Architektura systemu | ⚠️ warunkowo — brak diagramu elektrycznego |
| 2-ECU | Projekt szczegółowy sprzętu ECU | ⚠️ warunkowo — elementy wokół PMIC (przyjęty 1.11.2026), komparator i próg tranzystorowy, potwierdzenie BOM |
| 2-HMI | Projekt szczegółowy sprzętu HMI | ⚠️ warunkowo — drzewo zasilania, drabinka przycisków, pełny numer pamięci |
| **2-FW** | **Specyfikacja funkcjonalna firmware** | 🔶 **w toku** — A i B zamknięte, C.1 do ponownego przeglądu, C.2–J otwarte |
| 2-Desktop | Aplikacja desktop i protokoły komunikacji | ⬜ |
| 3 | Prototyp funkcjonalny — **wyłącznie płytki dev, sygnały symulowane** | ⬜ |
| 4 | Projekt PCB i wytyczne EMI | ⬜ |
| 5 | Firmware produkcyjny | ⬜ |
| 6 | Montaż na docelowym PCB, bring-up, testy elektryczne | ⬜ |
| 7 | Aplikacja desktop — implementacja finalna | ⬜ |
| 8 | Integracja i pierwsze testy na motocyklu | ⬜ |
| 9 | Walidacja terenowa | ⬜ |
| 10 | Iteracja (rev B) | ⬜ |
| 11 | Przygotowanie do produkcji małoseryjnej i dokumentacja użytkownika | ⬜ |
| 12 | Pilotaż, mała seria | ⬜ |
| 13 | Sprzedaż i wsparcie | ⬜ |

**Rozgraniczenie Fazy 3 i 5:** Faza 3 dowodzi, że **logika sterowania jest poprawna** — to można zrobić na płytce dev. Faza 5 dokłada wszystko, czego na płytce dev sprawdzić się nie da: drivery mocy, zarządzanie zasilaniem, bootloader. Kod z Fazy 3 nie jest wyrzucany, jest rozszerzany.

**Zasada kolejności:** pełny dobór sprzętu i projekt aplikacji **przed** prototypowaniem. Płytki deweloperskie nie mają zabezpieczeń przepięciowych, więc podłączenie do pracującego silnika grozi uszkodzeniem.

⚠️ **Korekta po drugim audycie:** zasada późnej integracji **nie zabrania pasywnej charakterystyki fabrycznego motocykla**. Pomiary na motocyklu sterowanym fabrycznym układem są dopuszczone od razu i są dziś pozycją o najwyższym priorytecie (O-001) — poprzedni plan odkładał dane wejściowe za decyzje, które od nich zależą.

---

## 3. Bramki jakości

Nadrzędne wobec bramek poszczególnych faz.

> **Reguła nadrzędna: jedna otwarta pozycja P0 albo jedna otwarta pozycja bezpieczeństwa oznacza NO-GO.**

| Bramka | Warunek GO |
|---|---|
| **G0 — Wymagania** | Zakres MVP zamrożony, wymagania z identyfikatorami, wartościami i metodą weryfikacji, zatwierdzone kryteria odbioru wyrobu, obwiednia środowiskowa i elektryczna, budżet wykonalności |
| **G1 — Architektura** | Zasilanie, bezpieczeństwo, wejścia i wyjścia, protokoły i warianty spójne. Stan bezpieczny zdefiniowany per wyjście, analiza niezależności mechanizmów ochronnych wykonana |
| **G2 — Projekt szczegółowy** | Schemat, macierz pinów i DMA, BOM z pełnymi numerami i arkuszami kwalifikacji, analiza najgorszego przypadku, wiązka, FMEA. **Przed wydaniem PCB: niezależny przegląd ludzki toru energii, odcięcia i synchronizacji** |
| **G3 — Implementacja firmware** | Punkty A–J kompletne w zakresie MVP, interfejsy zamrożone, testy zdefiniowane i wykonane na stanowisku, standard kodowania i analiza statyczna wdrożone, build odtwarzalny |
| **G4 — Wydanie PCB i integracja z silnikiem** | Kontrola elektryczna, przegląd projektu, testowalność, termika, lista kontrolna EMC. Aktywna integracja nowego ECU dopuszczona dopiero tutaj |
| **G5 — Walidacja w pojazdzie** | Testy wstrzykiwania usterek i stanu bezpiecznego zaliczone, środowisko i czytelność potwierdzone w rzeczywistym enduro |

**Żadna bramka nie służy do pierwszego ustalania podstawowych parametrów bezpieczeństwa.** Próby terenowe potwierdzają wymagania, nie ustalają ich.

---

## 4. Kryteria odbioru wyrobu MVP-A

**Status: zatwierdzone przez Pawła 25.10.2026, kryterium po kryterium (O-050).** Bramki opisują fazy, a te kryteria opisują wyrób. A4 uzupełnione o granicę bezwzględną 25.10.2026 (O-007).

Wyrób uznaje się za gotowy, gdy **wszystkie** poniższe są spełnione i udokumentowane:

| # | Kryterium | Wartość | Dowód |
|---|---|---|---|
| A1 | Rozruch kickstarterem na zimnym silniku | ≤ 3 kopnięcia, 10 prób z rzędu | Protokół z Fazy 8 |
| A2 | Rozruch kickstarterem na rozgrzanym silniku | ≤ 2 kopnięcia, 10 prób | jw. |
| A3 | Praca ciągła w całym zakresie obrotów bez przerw w zapłonie | 800–10 000 obr/min | Rejestracja przerw |
| A4 | Dokładność momentu zapłonu | wg ECU-IGN-002 (≤ 1,0° w 99,9 %) **oraz ECU-IGN-022: w 100 % zapłonów wcześniej ≤ 1°, później ≤ 2°**; w rozruchu iskra w GMP (ECU-IGN-019) | T-IGN-002, T-IGN-019, T-IGN-022 |
| A5 | Każdy mechanizm klasy K4 zweryfikowany wstrzykiwaniem usterki | 100% pozycji | Protokoły T-SAF-* |
| A6 | Pobór prądu w uśpieniu | ECU ≤ 150 µA, zestaw ≤ 250 µA (bilans: ≤ 63 / ≤ 123 µA) | T-PWR-001, T-PWR-002 |
| A7 | Przejazd terenowy bez usterki krytycznej i bez fałszywego odcięcia | **10 godzin** pracy silnika w terenie | Log czarnej skrzynki |
| A8 | Temperatura wewnątrz obudów w granicach klas komponentów z marginesem SYS-ENV-003b | **Komora klimatyczna +50 °C otoczenia** (SYS-ENV-003, zmiana 1.11.2026) oraz **dane z czujników temperatury ECU z przejazdu A7**; w miejscu akcelerometru **≤ 100 °C** (Z17); żadne zadziałanie progu T3 (ECU-SAF-020) | Protokół z komory + log |
| A9 | Czytelność wyświetlacza w pełnym słońcu | wg HMI-UI-005 | T-UI-005 |
| A10 | Pełny cykl: strojenie mapy, zapis, aktualizacja firmware ECU i HMI, powrót do pracy, **w tym przerwanie aktualizacji w losowym momencie** | bez utraty spójności danych; ECU zawsze startuje | T-COM-005b, T-COM-006, T-BTL-003 |
| A11 | Pozycje P0 otwarte | **zero** | `otwarte.md` |
| A12 | Ryzyka o wpływie wysokim | zamknięte dowodem albo **świadomie zaakceptowane na piśmie** | `otwarte.md` |
| **A14** | **Rozruch kopnięciem przy bardzo słabym akumulatorze** — zasilacz 7 V na złączu ECU zamiast akumulatora (ECU-IGN-021) | **≤ 5 kopnięć**, 10 prób | Protokół z Fazy 8 |
| **A15** | **Zero fałszywych wywrotek, w tym na hopach** (ECU-SAF-005) | przejazd A7 zawiera hopy; zero zadziałań | Log kąta i przyspieszenia z czarnej skrzynki |
| **A13** | **Brak nieplanowanej iskry** w żadnym scenariuszu: reset, zanik zasilania, kill switch, utrata synchronizacji, aktualizacja firmware, ruch wsteczny wału | zero zdarzeń | Protokoły T-AUD-03, T-AUD-05, T-AUD-10 |

**A7 jest kryterium najtrudniejszym i celowo takim pozostaje.** Dziesięć godzin realnej jazdy wyłapie to, czego nie wyłapie żadne stanowisko: zakłócenia, wibracje, błoto, temperaturę, zachowanie kierowcy. Jeśli któregokolwiek z pozostałych kryteriów nie da się zmierzyć przed A7, znaczy to, że A7 przyszło za wcześnie.

**A13 dopisane po drugim audycie.** Nieplanowana iskra pod przypadkowym kątem jest skutkiem kilku niezależnych mechanizmów awarii i żadne z pozostałych kryteriów jej nie obejmuje.

---

## 5. Plan prac

Kolejność wynika z jednej reguły: **dane wejściowe przed decyzjami, które od nich zależą.**

| Etap | Zakres | Co rozstrzyga |
|---|---|---|
| **0** | Repozytorium i baseline, uczciwe statusy, korekta potwierdzonych błędów zapisu | Utrwalenie stanu — **wykonane 13.10.2026** |
| **1** | **Triaż zapłonu i oględziny na motocyklu** (`measurements/triaz-zaplonu.md`) | Czy driver zapłonu i cała architektura ładowania cewki zostają w projekcie — **wykonane 15.10.2026: zapłon nie jest indukcyjny, przyjęte AC-CDI** |
| **2** | Pełna sesja pomiarowa i naprawa założeń fizycznych | Topologia zapłonu, kąt odniesienia, budżet latencji, przebieg uzwojenia wzbudzającego względem GMP (AC-CDI) |
| **3** | Zamknięcie G0 | Obwiednia środowiskowa, granica błędu kąta, polityka live tuningu, wymagania bootloadera i wybudzania, budżet wykonalności, zamiennik IMU (**wybrany 25.10.2026: AIS2IH**, warunek Z17) |
| **4** | Architektura, schemat, G1 i G2 | Tor energii AC-CDI, logika odcięcia, niezależne ograniczenie wyzwalania tyrystora (ECU-IGN-005), wiązka, EMC, termika. **Niezależny przegląd ludzki przed PCB** |
| **5** | Dokończenie punktu C, punkt D, punkt H, protokoły | Rozruch i synchronizacja, struktura map, bootloader, komunikacja |
| **6** | Stanowisko i G3 | Wstrzykiwanie usterek, standard kodowania, odtwarzalny build |

---

### 5.1 Wyposażenie pomiarowe i założenia budżetowe (O-051, decyzje Pawła 25.10.2026)

**Budżet i zakupy prowadzi Paweł.** Ten rozdział zapisuje tylko skutki techniczne.

| Przyrząd | Do czego | Stan |
|---|---|---|
| Rigol DHO804 (4 kanały, 70 MHz) | Oscylogramy zapłonu, VR, zasilania | jest |
| 3× sonda P4100 100:1 / 2 kV | Uzwojenie wzbudzające, pierwotne cewki, uzwojenie ładujące | do kupienia |
| Multimetr, miernik µA | Rezystancje, pobór w uśpieniu (T-PWR-001/002) | jest |
| ST-LINK na płytce Nucleo | Programowanie i debugowanie przez SWD | jest |
| Zasilacz laboratoryjny 0–30 V / 5 A | 7 V (A14), 18 V, −14 V (zamiana przewodów), zapady | do kupienia |
| **Symulator VR na Nucleo z DAC** | Testy zapłonu na stanowisku: obroty, hamowanie wału, zakłócenia, **wyjście cyfrowe „prawdziwego kąta” jako niezależne odniesienie** | do zbudowania |
| Adapter USB-CAN (typu CANable) | Podgląd i wstrzykiwanie ramek — **niezależny od ECU** | do kupienia |
| STEVAL-MKI218V1 + STEVAL-MKI109D | Drgania w miejscu montażu (O-047) | do kupienia |
| Własna komora grzewcza (+50 °C, SYS-ENV-003 od 1.11.2026) | A8, SYS-ENV-003 strona gorąca, progi ECU-SAF-020 | do zbudowania |
| Termopary z rejestratorem, luksomierz | A8, A9 | do kupienia |

**Pomiar kąta zapłonu (wymóg O-051):** na stanowisku odniesieniem jest **wyjście kąta z symulatora VR**, które nie przechodzi przez kondycjoner ECU. Przy 10 000 obr/min 1° to 16,7 µs, a oscyloskop i timery dają rozdzielczość w nanosekundach, więc niepewność toru jest o rzędy wielkości mniejsza od granicy ECU-IGN-022. **Na silniku** niezależne odniesienie to lampa stroboskopowa z tarczą kątową (niepewność rzędu 0,5–1°). Wystarcza do porównania z fabrycznym CDI, **nie** do dowodu granicy 1°. Granicę dowodzi stanowisko.

**Świadomie przyjęte luki w dowodach:**
- **−40 °C (SYS-ENV-003) bez pomiaru.** Zamrażarka daje ok. −20…−30 °C. Dolna granica wykazywana analizą klas temperaturowych elementów (SYS-ENV-003b)
- **EMC bez laboratorium akredytowanego** (decyzja 18.10.2026, SYS-ENV-010)
- **Jedna iteracja PCB.** Warunek: pełny przegląd schematu i płytki przed zamówieniem, w tym niezależny przegląd ludzki toru zapłonu i odcięcia (O-057)

## 6. Dokumenty

| Plik | Zawartość |
|---|---|
| `produkt.md` | Co budujemy i jak: zakres, warianty, decyzje sprzętowe z uzasadnieniami, komponenty, zasilanie, złącze, uśpienie, HMI, budżety, obudowy, obwiednia |
| `wymagania.md` | Wymagania z wartościami i metodą weryfikacji + tabela pokrycia od wymagania do dowodu |
| `firmware.md` | Specyfikacja funkcjonalna firmware, punkty A–J |
| `otwarte.md` | **Jedyny rejestr pozycji otwartych** — jedna przestrzeń identyfikatorów, trzy statusy, założenia, ryzyka zaakceptowane świadomie |
| `proces.md` | Ten plik |
| `diagrams/` | Architektura systemu, łańcuch odcięcia, zatrzask K4 |
| `measurements/` | Procedury pomiarowe i wyniki |
| `audit/` | Otrzymane raporty audytowe w formie dostarczonej |
| `scripts/kontrola.py` | Kontrola spójności i generowanie liczników |
| — | Dokumentacja przed konsolidacją (odpowiedzi na oba audyty, dawny dokument główny, nieaktualna specyfikacja Fazy 3) została na gałęzi `Old-docs` tego repozytorium i nie jest rozwijana |

**Historii zmian nie prowadzimy w treści dokumentów — nosi ją repozytorium.** Baseline przy bramce jest znacznikiem w repozytorium, nie wpisem w tabeli.
