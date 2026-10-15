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
| 2-ECU | Projekt szczegółowy sprzętu ECU | ⚠️ warunkowo — dobór przetwornic, komparatora, potwierdzenie BOM |
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

**Status: propozycja niezatwierdzona (O-050).** Bramki opisują fazy, a te kryteria opisują wyrób — dopóki nie zostaną zatwierdzone, projekt formalnie nie ma definicji gotowości.

Wyrób uznaje się za gotowy, gdy **wszystkie** poniższe są spełnione i udokumentowane:

| # | Kryterium | Wartość | Dowód |
|---|---|---|---|
| A1 | Rozruch kickstarterem na zimnym silniku | ≤ 3 kopnięcia, 10 prób z rzędu | Protokół z Fazy 8 |
| A2 | Rozruch kickstarterem na rozgrzanym silniku | ≤ 2 kopnięcia, 10 prób | jw. |
| A3 | Praca ciągła w całym zakresie obrotów bez przerw w zapłonie | 800–10 000 obr/min | Rejestracja przerw |
| A4 | Dokładność momentu zapłonu | wg ECU-IGN-002 **oraz bezwzględnej granicy błędu (O-007)** | T-IGN-002 |
| A5 | Każdy mechanizm klasy K4 zweryfikowany wstrzykiwaniem usterki | 100% pozycji | Protokoły T-SAF-* |
| A6 | Pobór prądu w uśpieniu | ECU ≤ 150 µA, zestaw ≤ 250 µA — **wartość do rewizji, patrz O-023** | T-PWR-001, T-PWR-002 |
| A7 | Przejazd terenowy bez usterki krytycznej i bez fałszywego odcięcia | **10 godzin** pracy silnika w terenie | Log czarnej skrzynki |
| A8 | Temperatura wewnątrz obudów w granicach klas komponentów | pomiar w warunkach letnich | Protokół termiczny |
| A9 | Czytelność wyświetlacza w pełnym słońcu | wg HMI-UI-005 | T-UI-005 |
| A10 | Pełny cykl: strojenie mapy, zapis, aktualizacja firmware ECU i HMI, powrót do pracy | bez utraty spójności danych | T-COM-005b, T-COM-006 |
| A11 | Pozycje P0 otwarte | **zero** | `otwarte.md` |
| A12 | Ryzyka o wpływie wysokim | zamknięte dowodem albo **świadomie zaakceptowane na piśmie** | `otwarte.md` |
| **A13** | **Brak nieplanowanej iskry** w żadnym scenariuszu: reset, zanik zasilania, kill switch, utrata synchronizacji, aktualizacja firmware, ruch wsteczny wału | zero zdarzeń | Protokoły T-AUD-03, T-AUD-05, T-AUD-10 |

**A7 jest kryterium najtrudniejszym i celowo takim pozostaje.** Dziesięć godzin realnej jazdy wyłapie to, czego nie wyłapie żadne stanowisko: zakłócenia, wibracje, błoto, temperaturę, zachowanie kierowcy. Jeśli któregokolwiek z pozostałych kryteriów nie da się zmierzyć przed A7, znaczy to, że A7 przyszło za wcześnie.

**A13 dopisane po drugim audycie.** Nieplanowana iskra pod przypadkowym kątem jest skutkiem kilku niezależnych mechanizmów awarii i żadne z pozostałych kryteriów jej nie obejmuje.

---

## 5. Plan prac

Kolejność wynika z jednej reguły: **dane wejściowe przed decyzjami, które od nich zależą.**

| Etap | Zakres | Co rozstrzyga |
|---|---|---|
| **0** | Repozytorium i baseline, uczciwe statusy, korekta potwierdzonych błędów zapisu | Utrwalenie stanu — **wykonane 13.10.2026** |
| **1** | **Triaż zapłonu i oględziny na motocyklu** (`measurements/triaz-zaplonu.md`) | Czy driver zapłonu i cała architektura ładowania cewki zostają w projekcie |
| **2** | Pełna sesja pomiarowa i naprawa założeń fizycznych | Topologia zapłonu, kąt odniesienia, budżet latencji, model usterek ogranicznika dwell |
| **3** | Zamknięcie G0 | Obwiednia środowiskowa, granica błędu kąta, polityka live tuningu, wymagania bootloadera i wybudzania, budżet wykonalności, zamiennik IMU |
| **4** | Architektura, schemat, G1 i G2 | Tor energii, logika odcięcia, niezależny sufit czasu ładowania, wiązka, EMC, termika. **Niezależny przegląd ludzki przed PCB** |
| **5** | Dokończenie punktu C, punkt D, punkt H, protokoły | Rozruch i synchronizacja, struktura map, bootloader, komunikacja |
| **6** | Stanowisko i G3 | Wstrzykiwanie usterek, standard kodowania, odtwarzalny build |

---

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
