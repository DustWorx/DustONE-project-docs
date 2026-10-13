# Plan naprawczy po audycie zewnętrznym

*Źródło: `audyt-dokumentacji-ecu-hmi-fw.pdf`, wersja 1.0, 12.09.2026*
*Werdykt audytu: NO-GO do implementacji produkcyjnego FW i zamrożenia PCB*

| | |
|---|---|
| **Identyfikator** | DOC-006 |
| **Wersja** | **1.7** |
| **Status** | roboczy — wszystkie pozycje P0 zamknięte |
| **Właściciel** | Paweł |
| **Opracowanie** | Claude |
| **Data wersji** | 2026-09-20 |
| **Dokument nadrzędny** | `proces-rozwoju-ecu.md` (DOC-001) |

**Historia zmian**

| Wersja | Data | Zakres zmiany |
|---|---|---|
| 1.0 | 2026-09-12 | Utworzenie: stanowisko wobec audytu, podział 36 pozycji na naprawę i proces, etapy 1–3, bramki |
| 1.1 | 2026-09-12 | Rozdz. 8–12: karta MVP, koncepcja bezpieczeństwa, ponowny dobór drivera wtryskiwaczy, przeprojektowanie zasilania, bilans pinów |
| 1.2 | 2026-09-20 | Zamknięcie F-011 (wartości wymagań), F-012 (tabela pokrycia), F-029 (rejestr ryzyk), F-033 (wersjonowanie dokumentów); aktualizacja bilansu w rozdz. 7.3 |
| 1.4 | 2026-09-22 | **F-023 zamknięte** — macierz usterek kompletna (40 DTC). Pozycja przeniesiona z listy procesowej do zamkniętych |
| 1.5 | 2026-09-29 | Usunięcie quickshiftera z zakresu: karta MVP-A, bilans pinów analogowych i zakres pozycji F-011 |
| 1.6 | 2026-09-29 | F-031 w części diagramu bezpieczeństwa zamknięte — DOC-008 i DOC-009 |
| **1.7** | **2026-10-11** | **F-013 zamknięte** — specyfikacja triggera i synchronizacji (C.1) |

---

## 1. Stanowisko wobec audytu

Audyt oceniony jako **rzetelny i w zdecydowanej większości trafny**. Przyjęty w całości jako podstawa działań naprawczych.

### 1.1 Błędy potwierdzone jako własne

| ID | Błąd | Charakter |
|---|---|---|
| F-001 | L9960 opisany jako 2-kanałowy driver wtryskiwaczy peak-and-hold. Producent określa go jako mostek H do silników DC (przepustnice, EGR, pompy). **Zweryfikowane u ST — audyt ma rację** | Nieuprawniona ekstrapolacja z kategorii „automotive driver" bez sprawdzenia funkcji w datasheecie |
| F-002 | LDO 5 V (TLE4276) zasilany z 5 V z przetwornicy. Regulator liniowy wymaga zapasu napięcia — wystawi ~4,5 V zamiast 5,0 V | Błąd elementarny, przeoczony mimo kilkukrotnego rysowania drzewa zasilania. Rujnuje dokładność czujników ratiometrycznych |
| F-006 | Maszyna stanów przechodzi GOTOWOŚĆ → ROZRUCH „po wykryciu obrotów", ale nic tych obrotów nie wywołuje. Brak stanu żądania startu i załączenia rozrusznika | Błąd logiczny — w tej formie maszyna stanów nie odpali silnika |

### 1.2 Trafne ustalenia, które nie były błędami, lecz przeoczeniami

- **F-003** — domeny zasilania TJA1043 (VBAT/VCC/VIO) nieprzeanalizowane. Wyłączamy szynę 5 V, czyli VCC transceivera — zmienia to jego tryb pracy, co unieważnia opisaną koncepcję wybudzania
- **F-005** — automatyczny powrót do pracy po resecie watchdoga. Zauważony i opisany, ale bez wyciągnięcia wniosku o konieczności zatrzasku
- **F-004** — argument liczbowy, którego nie podano wcześniej: okno watchdoga 100 ms przy 10 000 obr/min to ~17 obrotów wału
- **F-007, F-009, F-010** — sprzeczność MVP z bramką Fazy 8, brak macierzy pinów, brak protokołów
- **Statusy faz** — oznaczenie 2-ECU i 2-HMI jako ZAMKNIĘTE sugerowało kompletność, której nie osiągnęły. **Błąd w prowadzeniu procesu**

### 1.3 Ustalenia opisujące artefakty z faz jeszcze nierozpoczętych

F-016, F-030, F-032 (schematy, netlista, BOM z pełnymi OPN, projekt wiązki) dotyczą Fazy 4. Sam audyt zaznacza to w rozdziale o ograniczeniach. **Nie podważa to werdyktu** — sedno zarzutu (przedwczesne zamknięcie faz) pozostaje słuszne.

---

## 2. Działania wykonane natychmiast (12.09.2026)

| Działanie | Status |
|---|---|
| Cofnięcie statusu Fazy 2-ECU na COFNIĘTA | ✅ |
| Cofnięcie statusów Faz 0, 1, 2-HMI na WARUNKOWO | ✅ |
| Oznaczenie L9960 jako do ponownego doboru | ✅ |
| Oznaczenie TLE4276/drzewa zasilania jako do przeprojektowania | ✅ |
| Utworzenie niniejszego planu naprawczego | ✅ |

---

## 3. Etap 1 — decyzje blokujące (P0)

**Przedefiniowany 12.09.2026:** po podziale na naprawę i pracę procesową (rozdz. 7) etap obejmuje wyłącznie błędy w fazach zamkniętych. Pozycje F-008 (specyfikacja FW) i F-010 (protokoły) przeszły do normalnej pracy w Fazach 2-FW i 2-Desktop, gdzie uwagi audytu są kryteriami akceptacji. Zabezpieczeniem są bramki G0-G5.

Kolejność wymuszona zależnościami: zakres → bezpieczeństwo → sprzęt → interfejsy.

| # | Zadanie | Pozycje audytu | Zależność | Status |
|---|---|---|---|---|
| 1.1 | **Zamrożenie zakresu MVP** — karta wariantów, obiekty walidacyjne, kryteria wydania | F-007 | — | ✅ **rozdz. 8** |
| 1.2 | **Koncepcja bezpieczeństwa** — kill switch fail-safe, zatrzask po awarii | F-004, F-005 | 1.1 | ✅ **rozdz. 9** (analiza zagrożeń do uzupełnienia w punkcie B) |
| 1.3 | **Maszyna stanów — poprawka rozrusznika** | F-006 | 1.2 | ✅ specyfikacja FW rozdz. A.3b |
| 1.4 | **Ponowny dobór drivera wtryskiwaczy** | F-001, F-014 | — | ✅ **rozdz. 10** — TLE8104E na podstawie danych 11,7 Ω |
| 1.5 | **Przeprojektowanie drzewa zasilania** | F-002, F-003, F-018 | — | ✅ topologia (proces rozdz. 6.2b); ⬜ analiza najgorszego przypadku i dobór konkretnych przetwornic |
| 1.6 | **Macierz pinów i peryferiów** | F-009 | 1.5 | ✅ bilans i zmiana obudowy (rozdz. 12); ⬜ przypisanie pinów w CubeMX przy schemacie |
| ~~1.7~~ | ~~Protokoły CAN i USB~~ | F-010 | — | ➡️ **przeniesione do Fazy 2-Desktop** jako kryterium akceptacji (bramka G1) |
| ~~1.8~~ | ~~Dokończenie specyfikacji FW B-J~~ | F-008 | — | ➡️ **przeniesione do Fazy 2-FW** jako kryterium akceptacji (bramka G3) |

---

## 4. Etap 2 — specyfikacje wykonawcze (P1)

Uruchamiany po zamknięciu Etapu 1.

- Przepisanie wymagań MVP do formy: identyfikator + treść + wartość + tolerancja + metoda weryfikacji (F-011)
- Przebudowa tabeli pokrycia: wymaganie → projekt → moduł → identyfikator testu → dowód (F-012)
- Specyfikacja triggera i synchronizacji: koło, offset TDC, zbocze, blanking, dropout, resync, jitter (F-013)
- Tory czujnikowe: schemat i analiza najgorszego przypadku dla każdego typu wejścia (F-015)
- Profil transjentów i weryfikacja energetyczna zabezpieczeń (F-017)
- Model termiczny złącze→otoczenie, weryfikacja klasy temperaturowej MCU (F-019)
- Bilans pamięci: przepustowość, partycje, zużycie komórek, zapis atomowy (F-020)
- Pełna strategia aktualizacji: manifest, podpis, liczba prób, wycofanie (F-021)
- Budżety czasu rzeczywistego: zadania, WCET, NVIC/DMA, przeciążenie (F-022)
- Macierz usterek i praca awaryjna (F-023)
- Domknięcie termiki i czytelności HMI (F-024)
- Analiza najgorszego przypadku drabinki przycisków (F-025)
- Podprojekt mechaniczny czujnika biegu (F-026)
- Formalna zmiana zakresu logowania (F-027)
- Wstępna macierz regulacyjna przed layoutem (F-028)
- Właściciele i dowody zamknięcia ryzyk (F-029)
- Trzy diagramy: funkcjonalny, elektryczny, bezpieczeństwa (F-031)

---

## 5. Etap 3 — weryfikacja przed PCB

- Symulacja triggera, stanów i usterek
- Stanowisko z driverem cewki i docelowym obciążeniem wtrysku
- Stanowisko zasilania: rozruch, brown-out, odwrotna polaryzacja, transjenty, uśpienie, zanik zasilania
- Testy obciążeniowe CAN/USB z przerywaniem transakcji
- Wstępne badania termiczne ECU i HMI, czytelność HMI na słońcu
- Przegląd pokrycia: każde wymaganie ma przypisany test

---

## 6. Zmiana bramek procesu

Struktura faz zostaje, ale dochodzą twarde kryteria przejścia (za audytem, rozdz. 12.4):

| Bramka | Warunek GO |
|---|---|
| G0 — Wymagania | MVP zamrożony, identyfikatory wymagań, kryteria akceptacji, założenia zgodności |
| G1 — Architektura | Zasilanie, bezpieczeństwo, wejścia/wyjścia, protokoły i warianty spójne |
| G2 — Projekt szczegółowy | Schemat, macierz pinów/DMA, BOM z OPN, analiza najgorszego przypadku, wiązka, przegląd FMEA |
| G3 — Implementacja FW | Sekcje A-J kompletne, interfejsy zamrożone, testy zdefiniowane |
| G4 — Wydanie PCB | ERC, przegląd projektu, testowalność, termika, lista kontrolna EMC zamknięte |
| G5 — Pojazd | Testy wstrzykiwania usterek i stanu bezpiecznego zaliczone |

**Zasada:** jedna otwarta pozycja P0 lub jedna otwarta pozycja bezpieczeństwa = bramka pozostaje NO-GO.

---

## 7. Rejestr pozycji audytu — podział na naprawę i pracę procesową

**Kryterium podziału (decyzja 12.09.2026):**
- **NAPRAWA** — audyt wskazuje coś, co **zrobiliśmy źle**: zapis nieprawdziwy, sprzeczny albo błędny wybór w fazie oznaczonej jako zamknięta. Wymaga korekty teraz, bo dokumentacja wprowadza w błąd
- **PROCES** — audyt wskazuje coś, czego **jeszcze nie zrobiliśmy**: pusty rozdział w fazie, do której nie doszliśmy. Realizowane normalnym trybem, z uwagami audytu jako kryteriami akceptacji fazy

**Co to zabezpiecza:** bramki G0–G5 (rozdz. 6). Każda pozycja audytu jest przypisana do bramki. Bramka pozostaje NO-GO, dopóki wszystkie przypisane pozycje nie są zamknięte — niezależnie od tego, czy nazywają się naprawą, czy pracą procesową.

### 7.1 NAPRAWA — błędy w fazach zamkniętych

| ID | Prio | Skrót | Status |
|---|---|---|---|
| F-001 | P0 | Driver wtrysku — błędna klasa układu | ✅ TLE9104SH, rozdz. 10 |
| F-002 | P0 | LDO 5 V zasilany z 5 V | ✅ dwie przetwornice, rozdz. 11 |
| F-003 | P0 | Domeny i tryby TJA1043 opisane nieprawdziwie | ✅ VCC zawsze zasilane, rozdz. 11.1 |
| F-004 | P0 | Kill switch bez niezależnego fail-safe | ✅ NC + bramkowanie sprzętowe, rozdz. 9.1 |
| F-005 | P0 | Automatyczny restart po watchdogu | ✅ zatrzask + świadome odblokowanie, rozdz. 9.2 |
| F-006 | P0 | Cykliczna logika rozrusznika | ✅ dwie drogi do ROZRUCH, spec. FW A.3b |
| F-007 | P0 | MVP sprzeczny z bramką Fazy 8 | ✅ macierz wariantów, rozdz. 8 |
| F-009 | P0 | Brak macierzy pinów przy „zamkniętej" Fazie 2-ECU | ✅ ZAMKNIĘTE — bilans wykazał niewystarczalność LQFP64, zmiana na LQFP100, rozdz. 12 |
| F-011 | P1 | Wymagania Fazy 0 nie są mierzalne | 🔶 `wymagania.md` v0.2 — 70 wymagań z ID, 37 wartości ustalonych 20.09.2026. **Otwarte: 23 pozycje `[DO USTALENIA]` + brak wymagań dla quickshiftera i bootloadera (rozdz. 14.11 dokumentu głównego). Wszystko blokuje G0** |
| F-012 | P1 | Tabela pokrycia wskazuje fazy zamiast testów, część mapowań błędna | ✅ **ZAMKNIĘTE 20.09.2026** — tabela przebudowana (DOC-001 rozdz. 14.1–14.11): wymaganie → sprzęt → moduł FW → ID testu → dowód. 70/70 wymagań pokrytych, 70 identyfikatorów testów. Przebudowa ujawniła 10 funkcji bez wymagania (rozdz. 14.11) |
| F-019 | P1 | Błędne twierdzenie o klasie temperaturowej komponentów | ✅ STM32G474RE**T3**, przegląd komponentów |
| F-027 | P1 | Niespójny zakres logowania | ✅ ZAMKNIĘTE — wymaganie ECU-LOG-005 + formalna zmiana zakresu w `wymagania.md` rozdz. 8 |
| F-029 | P1 | Ryzyka bez właściciela i dowodu zamknięcia | ✅ **ZAMKNIĘTE 20.09.2026** — rejestr przebudowany (DOC-001 rozdz. 11): właściciel, działanie ograniczające, dowód zamknięcia i bramka dla każdej pozycji. Dopisane R16 (wyposażenie stanowiska), R17 (jedno źródło MAX9926), R18 (funkcje bez wymagań) |
| F-031 | P1 | Diagram pomija ścieżki zasilania, safety i interfejsy | 🔶 **1 z 3 gotowy (29.09.2026):** diagram bezpieczeństwa — DOC-008 (łańcuch odcięcia, podział sprzęt/firmware) i DOC-009 (zatrzask i odblokowanie). Pozostają: **funkcjonalny** — przegląd DOC-003 względem kryteriów audytu; **elektryczny** — powstaje w Fazie 4 przy schemacie |
| F-032 | P2 | Brak pełnych numerów katalogowych i statusu cyklu życia | 🔶 zasada #10 wprowadzona; przegląd częściowo wykonany |
| F-033 | P2 | Brak zarządzania wersjami dokumentów | ✅ **ZAMKNIĘTE 20.09.2026** — zasada procesu #13 + metryka i historia zmian we wszystkich siedmiu dokumentach (DOC-001…DOC-007), spis w DOC-001 rozdz. 0.2 |

### 7.2 PROCES — praca w fazach, do których nie doszliśmy

Uwagi audytu stają się **kryteriami akceptacji** tych faz.

| ID | Prio | Zakres | Faza | Bramka |
|---|---|---|---|---|
| F-008 | P0 | Specyfikacja FW, sekcje B-J | 2-FW (w toku) | G3 |
| F-010 | P0 | Protokoły CAN i USB | 2-Desktop | G1 |
| ~~F-013~~ | P1 | Specyfikacja triggera i synchronizacji | 2-FW, punkt C | G3 | ✅ **ZAMKNIĘTE 11.10.2026** — punkt C.1 na podstawie pomiarów koła impulsowego; ECU-IGN-012…019 |
| F-014 | P1 | Dane elektryczne wtryskiwaczy (pomiar) | 2-ECU / stanowisko | G2 |
| F-015 | P1 | Tory czujnikowe — schemat i analiza najgorszego przypadku | 4 (schemat) | G2 |
| F-016 | P1 | Wiązka, bezpiecznik, przekroje, masy | 4 | G2 |
| F-017 | P1 | Profil transjentów i weryfikacja energetyczna | 4 | G2 |
| F-018 | P1 | Budżet prądu spoczynkowego z tolerancjami | 4 / pomiar w 6 | G2 |
| F-020 | P1 | Bilans pamięci, partycje, zapis atomowy | 2-FW, punkt D | G3 |
| F-021 | P1 | Pełna strategia aktualizacji | 2-FW, punkt H | G3 |
| F-022 | P1 | Budżety czasu rzeczywistego | 2-FW, punkt I | G3 |
| ~~F-023~~ | P1 | Macierz usterek i praca awaryjna | 2-FW, punkt B | G3 | ✅ **ZAMKNIĘTE 22.09.2026** — macierz kompletna, 40 kodów DTC w 4 grupach (spec. FW B.2.1–B.2.5) |
| F-024 | P1 | Domknięcie termiki i czytelności HMI | 4 / test w 6 i 9 | G4 |
| F-025 | P1 | Analiza najgorszego przypadku drabinki przycisków | 4 | G2 |
| F-026 | P1 | Podprojekt mechaniczny czujnika biegu | osobny podprojekt | G2 |
| F-028 | P1 | Wstępna macierz regulacyjna | **przed layoutem** (nie Faza 11) | G2 |
| F-030 | P1 | Schematy, netlista, BOM z pełnymi numerami | 4 | G2 |
| F-034 | P2 | Słownik danych i jednostek | 2-Desktop | G1 |
| F-035 | P2 | Testowalność, punkty testowe, serializacja | 4 | G4 |
| F-036 | P2 | Kalibracja — obsługa i odzysk | 2-FW, punkt G | G3 |

### 7.3 Bilans

*Zaktualizowany 20.09.2026. Poprzednia wersja zawierała błąd rachunkowy — sumy nie zgadzały się z liczbą wierszy w tabelach 7.1 i 7.2 (podawała 15 i 22 zamiast 16 i 20). Obecne liczby zgadzają się z audytem: 36 pozycji, w tym 10×P0, 21×P1, 5×P2.*

| | P0 | P1 | P2 | Razem |
|---|---|---|---|---|
| Naprawa — **zamknięte** | 8 | 4 | 1 | **13** |
| Naprawa — otwarte | **0** | 2 | 1 | **3** |
| Proces — do realizacji w fazach | 2 | 15 | 3 | **20** |
| **Razem** | **10** | **21** | **5** | **36** |

**Wszystkie pozycje P0 w części naprawczej są zamknięte.** Dwie pozostałe pozycje P0 (F-008 — specyfikacja FW B–J, F-010 — protokoły CAN i USB) przeszły do pracy procesowej; ich zamknięcie jest warunkiem bramek G3 i G1.

**Otwarte pozycje naprawcze (3):**

| ID | Prio | Co pozostaje | Kiedy |
|---|---|---|---|
| F-011 | P1 | pozycje `[DO USTALENIA]` + wymagania dla bootloadera (quickshifter usunięty z zakresu 29.09.2026) | Domykane przy punktach B i C specyfikacji FW oraz w Fazie 2-Desktop; **wszystkie przed G0** |
| F-031 | P1 | Trzy diagramy: funkcjonalny, elektryczny, bezpieczeństwa | Razem z punktem B — diagram bezpieczeństwa powstaje z koncepcji bezpieczeństwa, nie przed nią |
| F-032 | P2 | Potwierdzenie stanów magazynowych i pełnych OPN dla całego BOM | Faza 4 (BOM), właściciel: Paweł |

**Wniosek procesowy:** etap naprawczy jest zamknięty w zakresie, jaki dało się zamknąć przed punktem B. F-031 i pozostała część F-011 są świadomie przeniesione do punktu B — nie dlatego, że są mniej ważne, lecz dlatego, że ich treść **wynika** z koncepcji bezpieczeństwa, a nie odwrotnie. Wykonanie ich wcześniej oznaczałoby zgadywanie, czyli dokładnie ten błąd, który wytknął audyt.

---

## 8. Zadanie 1.1 — Karta zamrożenia zakresu MVP (12.09.2026)

Odpowiedź na F-007. Zamiast jednej deklaracji „obsługujemy gaźnik, TPI, TBI i 4T" wprowadzamy **rozdzielone warianty, każdy z własnym obiektem walidacyjnym i własnym raportem**.

### 8.1 Macierz wariantów

| Wariant | Obiekt walidacyjny | Zakres funkcji | Kryterium wydania |
|---|---|---|---|
| **MVP-A** — gaźnik | **Beta 300RR 2015** (posiadany, motocykl) | Zapłon, rev limiter, wskaźnik biegu, prędkość/przebieg, motogodziny, wentylator, rozrusznik, światła, IMU/czarna skrzynka, HMI, aplikacja desktop, uśpienie | Pełna walidacja na pojeździe: stanowisko + jazda + teren |
| **Zdolność sprzętowa — wtrysk** | **Stanowisko HIL** (bez pojazdu) | Kanały wtrysku, pompa paliwa, TPS, korekta baro/temp — potwierdzone na obciążeniu zastępczym i rzeczywistym wtryskiwaczu | Dowód działania toru sprzętowego. **Nie jest deklaracją walidacji produktu na pojeździe** |
| **MVP-B** — TPI | Rzeczywisty silnik TPI (do pozyskania) | MVP-A + wtrysk 2-kanałowy do kanałów przepłukujących + pompa paliwa | Osobny raport walidacyjny, osobne mapy |
| **MVP-C** — TBI | Rzeczywisty silnik TBI (do pozyskania) | MVP-A + wtrysk 1-kanałowy w gardzieli + pompa paliwa | Osobny raport walidacyjny, osobne mapy |
| **Wariant 4T** | Silnik 4T (do pozyskania) | Inna synchronizacja, tryb batch lub wejście fazy | Osobny raport; zakres i termin nieustalone |

### 8.2 Konsekwencje dla procesu

- **Bramka Fazy 8 rozdzielona per wariant.** „Silnik pracuje pod kontrolą ECU" dotyczy MVP-A na Becie. Pozostałe warianty mają własne bramki i nie blokują wydania MVP-A.
- **Materiały produktowe nie mogą deklarować obsługi TPI/TBI/4T** przed zamknięciem odpowiedniego raportu walidacyjnego. Do czasu walidacji na silniku obowiązuje sformułowanie „tor sprzętowy potwierdzony na stanowisku".
- **Stanowisko HIL staje się osobnym deliverable** — pozwala testować kanały wtrysku bez posiadania silnika TPI/TBI. Do zaplanowania w Etapie 3.

### 8.3 Zadanie 1.4 — dane wtryskiwaczy: status

Producent (KTM/Husqvarna/GasGas) **nie publikuje danych elektrycznych wtryskiwaczy TPI/TBI**. Potwierdzono jedynie, że TPI stosuje dwa wtryskiwacze wtryskujące do tylnych kanałów przepłukujących — zgodne z założeniem dwóch kanałów.

**Ścieżka postępowania:**
1. Poszukiwanie danych w dokumentacji serwisowej producenta
2. Jeśli bezskutecznie — **zakup wtryskiwacza TPI i pomiar własny**

**Parametry do zmierzenia przed doborem drivera:**

| Parametr | Po co |
|---|---|
| Rezystancja uzwojenia | Rozróżnienie nisko-/wysokoimpedancyjny; decyduje o trybie sterowania |
| Indukcyjność | Czas narastania prądu, dobór obwodu gaszenia |
| Prąd szczytowy do otwarcia | Wymagana wydajność prądowa drivera |
| Prąd podtrzymania | Straty cieplne w driverze |
| Czas otwarcia i zamknięcia | Czas martwy w modelu paliwowym (punkt C specyfikacji FW) |
| Napięcie i energia przy wyłączeniu | Dobór obwodu gaszenia i ograniczenia napięcia |

**Do czasu pomiaru dobór drivera wtryskiwaczy pozostaje otwarty.** Ponowny wybór bez danych powtórzyłby błąd F-001.

---

## 9. Zadanie 1.2 — Koncepcja bezpieczeństwa (12.09.2026)

Odpowiedź na F-004 i F-005.

### 9.1 Kill switch — wejście cyfrowe z fail-safe (F-004)

**Decyzja: okablowanie normalnie zamknięte + sprzętowe bramkowanie driverów.** Zmiana wobec wcześniejszej decyzji L1 (samo wejście GPIO), po argumencie audytu: okno watchdoga 100 ms przy 10 000 obr/min to ~17 obrotów wału z niekontrolowaną pracą.

| Warstwa | Realizacja | Co pokrywa |
|---|---|---|
| **Okablowanie NC** | Wyłącznik zwarty = praca dozwolona. Przerwanie przewodu, korozja styku, rozłączona wtyczka → stan „stop" | Najczęstsza awaria polowa: uszkodzenie okablowania |
| **Wejście cyfrowe MCU** | Odczyt stanu do logiki, diagnostyki, komunikatu na HMI, wpisu do logu | Normalna obsługa i diagnostyka |
| **Sprzętowe bramkowanie** | Ten sam sygnał przez tranzystor/bramkę logiczną ściąga wejścia sterujące drivera zapłonu (VBG08H-E) i driverów wtrysku do stanu nieaktywnego | **Zawieszenie MCU** — odcięcie działa bez udziału firmware |

Koszt: jeden tranzystor lub bramka logiczna. Kill switch pozostaje wejściem cyfrowym; dochodzi równoległa ścieżka sprzętowa.

**Do zaprojektowania w Fazie 4:** dokładny obwód bramkujący, pomiar czasu reakcji (wymóg audytu), zachowanie przy jednoczesnym rozwarciu i zawieszeniu MCU, DTC dla wykrytego przerwania przewodu.

**~~Otwarte (audyt F-004)~~ — ZAMKNIĘTE 20.09.2026:** niezależny sprzętowy limit czasu ładowania cewki. Karta katalogowa VBG08H-E potwierdza ograniczenie prądu 8,5–10,5 A i miękkie wyłączenie przy 150–175 °C złącza, ale **to jest limit prądu, nie czasu** — sama ta ochrona nie wystarcza. Rozwiązanie: **rejestr okresu HRTIM jako sufit sprzętowy** (wyjście kasowane zdarzeniem porównania oraz zdarzeniem końca okresu — zweryfikowane bezpośrednio w STM32CubeMX na STM32G474VETx). Szczegóły i analiza energetyczna: `faza2-fw-specyfikacja.md` B.2.3. Limit szerokości impulsu wtrysku — analogicznie, do potwierdzenia przy konfiguracji timera wtrysku w Fazie 5.

### 9.2 Zatrzask po awarii (F-005)

**Decyzja: po awarii wyjścia zablokowane do zatrzymania wału i świadomego odblokowania.** Zniesiona wcześniejsza decyzja A.7, zgodnie z którą ECU po resecie startowało normalną ścieżką i mogło samoczynnie złapać silnik z rozpędu.

**Zdarzenia wyzwalające zatrzask:**

| Zdarzenie | Uzasadnienie |
|---|---|
| Reset od watchdoga | Przyczyna nieznana — automatyczny powrót do sterowania silnikiem jest nieuzasadniony |
| Brown-out (zapaść napięcia) | Stan rejestrów i przebieg przerwanej operacji nieokreślone |
| Wykrycie wywrotki przez IMU | Motocykl leży; silnik nie powinien wracać do pracy sam |
| Awaria krytyczna (klasyfikacja w punkcie E) | Zależnie od typu usterki |

**Warunki wyjścia z zatrzasku:**
1. Wał zatrzymany (brak sygnału obrotów przez zdefiniowany czas, z histerezą)
2. **Świadome działanie kierowcy** — sposób do ustalenia w punkcie B specyfikacji FW (np. przełączenie kill switcha w pozycję stop i z powrotem, albo potwierdzenie na HMI)
3. Zdarzenie zapisane do logu diagnostycznego z przyczyną i znacznikiem czasu

**Zabezpieczenie przed pętlą** (decyzja A.8): 3 resety watchdoga w krótkim czasie → stan AWARIA bez możliwości odblokowania bez interwencji, komunikat na HMI.

**Konsekwencja dla użytkownika:** po zadziałaniu zabezpieczenia silnik nie wróci sam do pracy — wymagane jest zatrzymanie i świadome odblokowanie. Do zapisania w instrukcji obsługi.


---

## 10. Zadanie 1.4 — Ponowny dobór drivera wtryskiwaczy (12.09.2026)

### 10.1 Dane wejściowe

**Rezystancja wtryskiwaczy KTM EXC TPI/TBI: 11,7 Ω nominalnie, zakres 10,5–13,0 Ω przy ~20°C.**

Źródło: materiały o systemach KTM. ⚠️ **Do potwierdzenia pomiarem na fizycznym wtryskiwaczu** przed zamrożeniem schematu — dane pochodzą z internetu, nie z dokumentacji serwisowej producenta.

**Wnioski:**
- To wtryskiwacz **wysokoimpedancyjny**. Prąd: ~1,03 A przy 12 V, ~1,23 A przy 14,4 V
- **Peak-and-hold jest niepotrzebne** — wystarcza sterowanie w trybie nasyconym (zwykłe włącz/wyłącz z ograniczeniem prądu i gaszeniem)
- Wcześniejsze wymaganie peak-and-hold wynikało z błędnego założenia o wtryskiwaczach niskoimpedancyjnych. Błąd dotyczył **klasy układu**, nie tylko konkretnego numeru katalogowego

### 10.2 Wybrany układ: Infineon TLE9104SH (OPN: TLE9104SHXUMA1)

**Ścieżka doboru — dwie zmiany:**

1. **L9960** — błąd pierwotny. Mostek H do silników prądu stałego, nie driver wtryskiwaczy
2. **TLE8104E** — funkcjonalnie właściwy, ale **status NRND** (Not Recommended for New Designs). Odrzucony na etapie sprawdzania dostępności — nie wolno go stosować w produkcie przeznaczonym do produkcji. Dokładnie ten problem sygnalizowała pozycja audytu F-032 (status cyklu życia)
3. **TLE9104SH** — wybrany. Aktywny, AEC-Q100/101

Funkcja potwierdzona w datasheecie producenta: układ przeznaczony do sterowania **wtryskiwaczami**, elektrozaworami i przekaźnikami, szczególnie w systemach zarządzania silnikiem.

| Parametr | Wartość | Ocena |
|---|---|---|
| Kanały | 4 × low-side (open drain DMOS) | 2 na wtryskiwacze, 2 zapasowe |
| Prąd obciążenia | 3 A/kanał | Zapas 2,4× wobec 1,23 A |
| Kwalifikacja | AEC-Q100/101 | Automotive |
| Obciążenia indukcyjne | Aktywne ograniczanie napięcia (wbudowane) | Bez zewnętrznych diod gaszących |
| Diagnostyka | SPI 16-bit: zwarcie do masy, zwarcie do plusa, przerwa obciążenia | Pokrywa wymagania |
| Sterowanie | Bezpośrednie wejścia PWM (aktywne niskim) + SPI | Timing z HRTIM bez pośrednictwa SPI |
| **Funkcje bezpieczeństwa** | **Piny EN i RESN** | Patrz 10.5 |

### 10.5 Synergia z koncepcją bezpieczeństwa

TLE9104SH ma pin **EN**, który sprzętowo wyłącza wszystkie stopnie wyjściowe. To gotowy punkt przyłączenia bramkowania od kill switcha (rozdz. 9.1) — **nie trzeba projektować własnego obwodu bramkującego dla toru wtrysku**, wystarczy poprowadzić na ten pin sygnał z wyłącznika. Upraszcza realizację F-004.

Pin **RESN** wymusza reset rejestrów SPI do wartości domyślnych — przydatny w sekwencji startu i przy realizacji stanu bezpiecznego po resecie watchdoga (rozdz. 9.2).

⚠️ **Do sprawdzenia (kolejność TME → Mouser → Farnell → DigiKey):** stan magazynowy. Mouser ma TLE9104SHXUMA1 w katalogu; dostępność w TME niepotwierdzona.

### 10.3 Skutki uboczne korekty

- **Straty cieplne ECU spadają z 6,7 W do ~5,9 W** (drivery wtrysku: 1,0 W → 0,16 W). Wnioski o obudowie aluminiowej pozostają aktualne
- Odpada złożoność sterowania: regulacja prądu szczytowego, pomiar prądu, faza podtrzymania. Upraszcza punkt C specyfikacji FW
- 2 wolne kanały low-side to rezerwa np. pod przyszły elektrozawór power valve

### 10.4 Pozostaje otwarte (F-014)

Pomiar na fizycznym wtryskiwaczu przed zamrożeniem schematu:
- Rezystancja — weryfikacja wartości 11,7 Ω z materiałów internetowych
- **Indukcyjność** — potrzebna do obliczenia energii gaszenia
- Czas otwarcia i zamknięcia — czas martwy w modelu paliwowym (punkt C specyfikacji FW)
- **Energia gaszenia:** Infineon publikuje osobną notę aplikacyjną o ograniczeniach energii dla TLE9104SH — przy obciążeniach o większej energii wymagany zewnętrzny obwód ograniczający. Szacunek dla naszego przypadku: ~11 mJ przy założonej indukcyjności 15 mH, co powinno mieścić się z zapasem. **Do zestawienia z wartościami z datasheetu po zmierzeniu rzeczywistej indukcyjności**


---

## 11. Zadanie 1.5 — Przeprojektowanie zasilania (12.09.2026)

Odpowiedź na F-002 i F-003. Szczegóły topologii: `proces-rozwoju-ecu.md` rozdz. 6.2b.

### 11.1 F-003 — ustalenie z datasheetu TJA1043

Dokumentacja NXP: **tryb Sleep jest wymuszany automatycznie przy zaniku napięcia na VCC albo VIO**, a pin INH przechodzi wtedy w stan wysokiej impedancji. Moja wcześniejsza dokumentacja opisywała tryb Standby przy wyłączonej szynie 5 V — było to nieprawdziwe.

**Rozwiązanie:** VCC transceivera zasilane na stałe z szyny 5 V. Wyłączane są tylko czujniki zewnętrzne, MAX9926 i MLX90316 — przez przełącznik obciążenia. Transceiver pozostaje w przewidywalnym trybie Standby.

**Dodatkowe ustalenie (forum wsparcia NXP):** przy zbyt niskim napięciu na VBAT transceivera nie da się wybudzić żadną metodą. Istotne dla scenariusza słabego akumulatora — do uwzględnienia w punkcie B specyfikacji FW.

### 11.2 Zmiany wobec poprzedniej wersji

| | Było (błędne) | Jest |
|---|---|---|
| Szyna 5 V | Przetwornica 12→5 V, potem LDO 5 V z tych samych 5 V | Przetwornica 12→5 V bezpośrednio |
| Odcinanie czujników | LDO 5 V (błędnie użyty jako wyłącznik) | Przełącznik obciążenia |
| Szyna 3,3 V | LDO z 5 V | Osobna przetwornica z 12 V |
| Tryb TJA1043 w uśpieniu | Standby (opis nieprawdziwy) | Standby (VCC zasilane na stałe) |
| Straty cieplne ECU | 5,9 W | **5,5 W** (mniej ciepła z LDO) |

### 11.3 Odrzucona propozycja: regulacja napięcia szyn przez MCU

Rozważana jako sposób na „świadomość ECU o problemach z zasilaniem". Odrzucona — wprowadza zagrożenie, nie usuwa żadnego:
- MCU zasila się z regulowanych szyn: błąd w firmware może zniszczyć czujniki, transceiver, pamięć i sam mikrokontroler
- Możliwa pętla: obniżenie własnego zasilania → brown-out → reset → wartość domyślna → powtórka
- Zawieszenie MCU zostawia szynę w nieokreślonym stanie
- Regulacja nie usuwa przyczyny — spadek napięcia oznacza zwarcie, przeciążenie lub słaby akumulator; podniesienie nastawy pogłębia problem

**Zamiast tego:** pomiar obu szyn przez ADC, sygnały Power Good z przetwornic, sterowanie włączeniem szyny 5 V (kierunek bezpieczny). Reakcja: diagnostyka, ostrzeżenie, tryb awaryjny — nigdy zmiana nastawy.

### 11.4 Pozostaje otwarte

- **Dobór konkretnych przetwornic** — kryteria: niski prąd własny w trybie oszczędnym (budżet uśpienia), wejście Power Good, sterowanie EN, odporność na transjenty, AEC-Q100. Dostawca wg zasady TME → Mouser → Farnell → DigiKey
- **Dobór przełącznika obciążenia** — z ograniczaniem prądu, żeby zwarcie w okablowaniu zewnętrznym nie wpływało na resztę układu
- **Analiza najgorszego przypadku (F-018)** — napięcia min/typ/max, prądy, tolerancje, zakres temperatur
- **Zasilanie HMI** — analogicznie dwie przetwornice; do rozstrzygnięcia, czy VCC transceivera HMI zostaje zasilone w uśpieniu


---

## 12. Zadanie 1.6 — Bilans pinów i peryferiów (12.09.2026)

Odpowiedź na F-009.

### 12.1 Uwaga metodyczna

Nie przypisuję konkretnych numerów pinów (typu „PA8 = wyjście zapłonu"). Funkcje alternatywne w STM32 mają setki ograniczeń krzyżowych i jedynym wiarygodnym narzędziem jest **STM32CubeMX**, który sam wykrywa konflikty. Zgadywanie przypisań powtórzyłoby błąd, który audyt wytknął przy L9960.

**Na tym etapie ustalamy bilans zapotrzebowania i adekwatność obudowy. Przypisanie pinów następuje w CubeMX przy tworzeniu schematu (Faza 4), z wydrukiem konfiguracji jako dowodem braku konfliktów.**

### 12.2 Bilans zapotrzebowania ECU

| Grupa | Sygnały | Piny |
|---|---|---|
| **Analogowe (ADC)** | TPS, temp. cieczy, temp. powietrza, pozycja biegu, monitor szyny 5 V, monitor napięcia akumulatora, pomiar prądu z 3 układów PROFET | **11** |
| **Czasowe (timery, HRTIM)** | Trigger z MAX9926, zapłon, wtryskiwacze 1-2, prędkość koła, czujnik fazy 4T (rezerwa) | **6** |
| **Cyfrowe** | Przycisk startu, kill switch, 6× sterowanie PROFET, 3× wybór diagnostyki PROFET, włączenie przełącznika obciążenia 5 V, 2× Power Good, karmienie watchdoga, TLE9104SH (CS, EN, RESN), TJA1043 (STB_N, EN, ERR_N, WAKE) | **22** |
| **Interfejsy i system** | FDCAN (2), USB (2), SPI wspólne (3), 3× wybór układu SPI, I2C (2), SWD (2), rezonator kwarcowy (2) | **16** |
| **RAZEM** | | **55** |

### 12.3 Wynik: LQFP64 niewystarczająca

LQFP64 ma 64 wyprowadzenia, z czego ~12-14 zajmuje zasilanie, masa, zasilanie analogowe, napięcie odniesienia, podtrzymanie RTC i reset. **Zostaje ~50 pinów użytkowych wobec 55 potrzebnych.**

Bilans pinów złącza (27 z 28) niczego tu nie wykrywał — to dokładnie luka, którą wskazał audyt.

**Decyzja: STM32G474VET3 (LQFP100)** — ten sam rdzeń, ~82 piny użytkowe, zapas ~27.

**Rozważona i odrzucona alternatywa:** redukcja funkcji do zmieszczenia w LQFP64 (rezygnacja z pomiaru prądu PROFET, rezerwy pod czujnik fazy 4T, jednego Power Good) dałaby ~48 pinów — mieści się, ale kosztem funkcji diagnostycznych i bez żadnej rezerwy.

**Koszt decyzji:** większa powierzchnia na płytce, nieco wyższa cena układu.

### 12.4 Pozostaje do wykonania (Faza 4, bramka G2)

- Przypisanie pinów w STM32CubeMX z weryfikacją konfliktów funkcji alternatywnych
- Przypisanie kanałów DMA i przerwań (audyt F-022 wymaga tabeli NVIC/DMA)
- Analogiczny bilans dla **STM32G0B1 w HMI** — nie wykonany; przy wyświetlaczu SPI, drabince przycisków, CAN, flash i czujniku temperatury zapotrzebowanie jest znacznie mniejsze, ale wymaga sprawdzenia
- Pełna macierz w formacie wymaganym przez audyt: złącze → kondycjonowanie → pin MCU → funkcja alternatywna → DMA/przerwanie → częstotliwość → diagnostyka → stan po resecie
