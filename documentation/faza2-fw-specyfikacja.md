# Faza 2-FW — Specyfikacja funkcjonalna firmware

| | |
|---|---|
| **Identyfikator** | DOC-004 |
| **Wersja** | **1.7** |
| **Status** | roboczy — punkt A zamknięty, punkty B–J do opracowania |
| **Właściciel** | Paweł |
| **Opracowanie** | Claude |
| **Data wersji** | 2026-09-20 |
| **Dokument nadrzędny** | `proces-rozwoju-ecu.md` (DOC-001) |

**Historia zmian**

| Wersja | Data | Zakres zmiany |
|---|---|---|
| 0.1 | 2026-08-31 | Utworzenie: maszyna stanów (A.1–A.4), decyzje A.1–A.8, źródła wybudzenia; szkice punktów B–J |
| 0.2 | 2026-09-12 | Korekta A.3b (sterowanie rozrusznikiem — audyt F-006); korekta opisu uśpienia: wyłączana jest wyłącznie przetwornica 5 V |
| 0.3 | 2026-09-20 | Aktualizacja oznaczeń komponentów (BMI088 → BMI090L); metryka dokumentu |
| 0.4 | 2026-09-20 | Punkt B: klasyfikacja usterek K0–K4, zamknięta lista zdarzeń odcinających, macierz grup 1 i 2, ustalenia o wyjściu C.F. w VBG08H-E, sufit czasu ładowania w rejestrze okresu HRTIM, zatrzask i odblokowanie |
| **0.5** | **2026-09-20** | Korekta opisu uśpienia (obie przetwornice pracują, odcinany jest przełącznik obciążenia); **macierz usterek grupa 3** — komunikacja i zasilanie, 11 kodów DTC; decyzje o niezgodności wersji protokołu i kolejności diagnozowania przy awarii szyny 5 V |
| 0.6 | 2026-09-20 | **Wycofanie propozycji zasilania MAX9926 poza przełącznikiem obciążenia** po sprawdzeniu karty katalogowej (brak wejścia shutdown, pobór 4,7 mA typ.); zagrożenie przeniesione na ECU-PWR-010 / DTC-PWR-10 |
| 0.7 | 2026-09-22 | **Macierz usterek grupa 4** — bezpieczeństwo, autotest i pamięć, 15 kodów DTC; **macierz kompletna (40 DTC), F-023 domknięte**. Decyzje: trzypoziomowe rozpoznanie kill switcha z bramkowaniem komparatorem zewnętrznym, blokada startu przy uszkodzonych mapach sterowania z rozdzieleniem od konfiguracji użytkownika, migawka stanu przy resecie watchdoga, próg wywrotki 65°/3 s. Domknięty zakres autotestu skróconego (ECU-PWR-003a); doprecyzowane zachowanie licznika resetów w B.4 |
| 0.8 | 2026-09-22 | **B.3 tryb pracy zastępczej** (trzy grupy deratingu wg utraconej informacji, mapa awaryjna na pełne obciążenie, zjazd limitu w 3 s, czterostopniowa prezentacja usterek) i **B.5 interlocki live tuningu** (zakres dozwolonych zmian, blokada przy obrotach i obciążeniu łącznie, limity szybkości, automatyczne przerwanie sesji). Rozdzielenie DTC-PWR-08 na 08a/08b po uwadze Pawła o zasilaniu MAX9926; rozdzielenie DTC-SEN-04 na warianty [A] i [B/C]. Odtworzone B.4, usunięte odniesienie do wycofanego zdarzenia 8 |
| 0.9 | 2026-09-29 | **B.6 quickshifter** — zamknięcie pozycji P0 z rozdz. 14.11. Zmiana decyzji 2.6: gotowy czujnik prętowy 0–5 V zamiast surowego tensometru ze wzmacniaczem w G474. Czas odcięcia zależny od obrotów z sufitem sprzętowym 150 ms, samoczynne wyłączenie przy zablokowanej dźwigni, warunek otwarcia przepustnicy 20% jako główny filtr fałszywych wyzwoleń. Nowe DTC-SEN-11 i DTC-SEN-12. Blipper formalnie poza zakresem |
| **1.0** | **2026-09-29** | **B.6.8 czujnik sprzęgła** — luka wykryta przez Pawła: warunki dopuszczenia nie sprawdzały intencji kierowcy. Mikroprzełącznik w klamce blokuje cięcie przy wciśniętym sprzęgle; kontrola wiarygodności stanu (DTC-SEN-13). Decyzja L2 utrzymana — brak blokady rozrusznika; w zamian wskazanie informacyjne włączonego biegu na HMI z czujnika bębna, bez zapisu do logu. Wykryty warunek konieczny: wybudzenie ECU musi pociągać wybudzenie HMI (SYS-COM-007). Pin zwolniony w B.6.2 przypadł czujnikowi sprzęgła, luka L33 odłożona |
| **1.1** | **2026-09-29** | Korekta wskazania włączonego biegu (HMI-UI-009): dodany **trzeci warunek — sprzęgło nie wciśnięte**. Wcześniejszy zapis pomijał go i błędnie twierdził, że czujnik sprzęgła nie jest do tego potrzebny |
| **1.2** | **2026-09-29** | **Poprawione kryterium DTC-SEN-13** po uwadze Pawła: kryterium czasowe (60 s przy prędkości powyżej 10 km/h) dawało fałszywy alarm przy zjeździe z góry na wciśniętym sprzęgle. Nowe kryterium — 3 potwierdzone zmiany biegu bez ani jednego odczytu stanu puszczonego. Dopisana jawna informacja, że awaria przeciwna (przełącznik rozwarty) jest niewykrywalna |
| 1.3 | 2026-09-29 | **Wycofane drugie kryterium DTC-SEN-13** — Paweł wskazał, że podczas zjazdu z góry na wciśniętym sprzęgle wykonuje się wiele redukcji bez puszczania klamki (5→1, potem 1→2). Kryterium oparte na liczbie zdarzeń zawodzi tak samo jak czasowe. Pozycja **otwarta**, trzy warianty przedstawione do decyzji; kryterium nie będzie zapisane bez zatwierdzenia (nowa zasada procesu #15) |
| 1.4 | 2026-09-29 | **Quickshifter i czujnik sprzęgła usunięte z produktu** decyzją Pawła. Sekcja B.6 zastąpiona zapisem zmiany zakresu z powodami i konsekwencjami; usunięte DTC-SEN-11/12/13; skorygowane stan PRACA, lista zabroniona w B.5, zakres kalibracji w punkcie G i podsumowanie w B.7. Zwolnione dwa piny złącza |
| 1.5 | 2026-09-29 | **Diagram bezpieczeństwa gotowy** (DOC-008 i DOC-009). **Punkt B zamknięty** — wszystkie podpunkty B.1–B.7 domknięte |
| 1.6 | 2026-10-11 | **C.1 trigger i synchronizacja** na podstawie pomiarów koła impulsowego (1 wypust, 30°, krawedź spływu w GMP, pick-up 95,7 Ω, szczelina 0,18 mm). Ciągły model kąta, estymata z interwału wypustu z korektą przyspieszenia, **bramkowanie kątowe odrzucające fałszywe zbocza**, dwa limity wyprzedzenia (28° geometryczny + termodynamiczny w mapie), iskra od drugiego przejścia wypustu. **Przebudowane DTC-IGN-02 i 03** — dawny zapis opisywał wzór zębów koła 60-2, którego ten silnik nie ma; dodane DTC-IGN-03a. Przemianowane zdarzenie 6 w B.1.1. Domyka F-013 |
| **1.7** | **2026-10-11** | **Skutki obalenia założenia Z1 — Beta 300 RR nie ma TPS.** Usunięte DTC-SEN-04 [A]; skorygowane grupa G3 w B.3.1, tabela wariantów w B.3.2, zakres kalibracji w punkcie G. **Interlock live tuningu dla MVP-A pozostawiony jako pozycja otwarta** — bez TPS nie da się ocenić warunku obciążenia |

---

## A. Maszyna stanów ECU

Firmware w każdej chwili znajduje się w dokładnie jednym zdefiniowanym stanie. Stan określa, które wyjścia są aktywne, jakie zadania są wykonywane i jakie zdarzenia mogą go zmienić.

### A.1 Stany

| Stan | Opis | Wyjścia mocy | Pobór |
|---|---|---|---|
| **UŚPIENIE** | **Poprawione 20.09.2026 — opis nie nadążał za przeprojektowaniem zasilania (F-002/F-003).** Obie przetwornice pozostają włączone w trybie oszczędnym: **3,3 V** zasila MCU w trybie Stop, flash, IMU i VIO transceivera; **5,0 V** zasila wyłącznie **VCC transceivera TJA1043** — musi zostać pod napięciem, bo przy zaniku VCC układ samoczynnie przechodzi w Sleep i przestaje nasłuchiwać magistrali. Odcinany jest **przełącznik obciążenia 5 V**: bez zasilania zostają czujniki zewnętrzne, MAX9926 i MLX90316. TJA1043 w trybie Standby, MCU w trybie Stop z aktywnymi przerwaniami EXTI | Wszystkie wyłączone | ~70-135 µA |
| **WYBUDZANIE** | Stan przejściowy. Wyjście MCU z trybu Stop, **załączenie przełącznika obciążenia 5 V** (przetwornica już pracuje), odczekanie na start czujników i ustalenie się progu adaptacyjnego MAX9926 (~1-2 ms), reinicjalizacja peryferiów (FDCAN, ADC, timery), wczytanie konfiguracji i map z flash, uruchomienie watchdoga, zapis przyczyny wybudzenia do logu | Wszystkie wyłączone | — |
| **GOTOWOŚĆ** | Silnik nie pracuje, system czuwa. HMI aktywne. Prime pompy paliwa. Oczekiwanie na obroty lub przycisk startu | Pompa (prime), światła wg ustawień | ~320 mA |
| **ROZRUCH** | Wał się kręci, obroty poniżej progu pracy samodzielnej. Osobna strategia: wzbogacenie, inne wyprzedzenie zapłonu. **Rozrusznik pracuje równolegle z tym stanem** (jeśli rozruch elektryczny), nie przed nim — ECU generuje iskrę w trakcie kręcenia | Zapłon, wtrysk (mapa rozruchowa), pompa, rozrusznik (warunkowo) | — |
| **PRACA** | Silnik pracuje samodzielnie. Pełna funkcjonalność: mapy, korekty, rev limiter, wentylator, logowanie | Wszystkie wg logiki | — |
| **ZATRZYMYWANIE** | Kontrolowane wyłączenie: odcięcie zapłonu i wtrysku, wyłączenie pompy, dokończenie zapisu logów | Wygaszane sekwencyjnie | — |
| **AWARIA** | Wykryto błąd krytyczny. Zachowanie zależne od rodzaju błędu (patrz punkt B) | Wg strategii awaryjnej | — |

### A.2 Decyzje (2026-08-31)

| # | Decyzja | Ustalenie |
|---|---|---|
| A.1 | **Timeout uśpienia ECU** | 30 minut bez pracy silnika i bez interakcji użytkownika |
| A.2 | **Timeout wyświetlacza HMI** | 3 minuty bez interakcji i bez pracy silnika — podświetlenie gaszone, HMI w trybie niskiego poboru. Wciśnięcie przycisku natychmiast przywraca ekran bez restartu systemu. Powód: podświetlenie to ~250 z 430 mA poboru HMI; dwustopniowy timeout obniża zużycie w czuwaniu z ~160 mAh do ~75 mAh na cykl (akumulator enduro ma 2-4 Ah) |
| A.3 | **Prime pompy paliwa** | 2 s przy przejściu w stan GOTOWOŚĆ (po wybudzeniu). Bezwarunkowy — zgodnie z praktyką fabryczną. Dotyczy wyłącznie konfiguracji TPI/TBI |
| A.4 | **Czujnik ciśnienia paliwa** | **Odrzucony.** Fabryczne systemy TPI/TBI go nie mają (regulator mechaniczny, założenie stałego ciśnienia). Dawałby przewagę diagnostyczną (zużyta pompa, zapchany filtr, wykrycie zubożenia mieszanki), ale kosztem ostatniego wolnego pinu złącza i ~150-350 PLN. Do ewentualnego powrotu w przyszłej wersji |
| A.5 | **Wejście w stan AWARIA** | Tylko usterki krytyczne. Pozostałe → praca kontynuowana z ostrzeżeniem na HMI i wpisem do logu diagnostycznego. Klasyfikacja usterek — punkt E |
| A.6 | **Próg ROZRUCH → PRACA** | 600-800 obr/min (wartość robocza, do korekty podczas testów na finalnym motocyklu — Faza 8) |
| A.7 | **Zachowanie po resecie watchdoga** | **ZMIENIONE 12.09.2026 po audycie (F-005).** Pełny reset ECU, wyjścia w stan bezpieczny, a następnie **ZATRZASK** — wyjścia pozostają zablokowane do zatrzymania wału **i świadomego odblokowania przez kierowcę**. Wcześniejszy zapis dopuszczał samoczynne złapanie silnika z rozpędu, co audyt słusznie zakwestionował. Zatrzask obejmuje też brown-out i wykrycie wywrotki. Szczegóły: `plan-naprawczy-audyt.md` rozdz. 9.2 |
| A.8 | **Zabezpieczenie przed pętlą resetów** | Licznik resetów watchdoga w pamięci nieulotnej. **3 resety w krótkim czasie → stan AWARIA z komunikatem na HMI, koniec prób startu.** Zapobiega cyklowi reset→start→zawieszenie→reset przy trwałej przyczynie awarii. Okno czasowe i sposób kasowania licznika — do doprecyzowania przy rozpisywaniu punktu B |

### A.3 Tabela przejść między stanami

| Ze stanu | Zdarzenie | Do stanu |
|---|---|---|
| UŚPIENIE | Trigger / przycisk startu / aktywność CAN / podłączenie USB | WYBUDZANIE |
| WYBUDZANIE | Inicjalizacja zakończona pomyślnie | GOTOWOŚĆ |
| WYBUDZANIE | Licznik resetów ≥ 3 lub błąd krytyczny przy starcie | AWARIA |
| GOTOWOŚĆ | **Naciśnięcie przycisku startu** → ECU załącza przekaźnik rozrusznika (kanał PROFET) | ROZRUCH (rozrusznik aktywny) |
| GOTOWOŚĆ | **Wykryto obroty bez naciśniętego przycisku** (kopnięcie) | ROZRUCH (bez rozrusznika) |
| GOTOWOŚĆ | 30 min bez pracy silnika i bez interakcji | UŚPIENIE |
| GOTOWOŚĆ | 3 min bez interakcji (tylko HMI — ECU pozostaje w GOTOWOŚĆ) | *wygaszenie ekranu* |
| ROZRUCH | Obroty > próg (600-800 obr/min) i stabilne → **ECU automatycznie wyłącza rozrusznik** | PRACA |
| ROZRUCH | Zwolnienie przycisku startu | Rozrusznik wyłączony; jeśli wał się zatrzyma → GOTOWOŚĆ |
| ROZRUCH | **Przekroczenie 5 s ciągłego kręcenia** | Rozrusznik wyłączony, komunikat na HMI |
| ROZRUCH | Zanik obrotów | GOTOWOŚĆ |
| ROZRUCH / PRACA | Kill switch / wykrycie wywrotki (IMU) / zanik obrotów | ZATRZYMYWANIE |
| ROZRUCH / PRACA | Usterka krytyczna | AWARIA |
| ZATRZYMYWANIE | Zapis logów zakończony, wyjścia wygaszone | GOTOWOŚĆ |
| AWARIA | **Zatrzask** (decyzja 1.2 planu naprawczego): wyjście wymaga zatrzymania wału **i świadomego odblokowania przez kierowcę**. Nie ma automatycznego powrotu | GOTOWOŚĆ (po odblokowaniu) |

### A.3b Sterowanie rozrusznikiem (poprawka 12.09.2026, audyt F-006)

**Wykryty błąd:** pierwotna maszyna stanów przechodziła z GOTOWOŚCI do ROZRUCHU „po wykryciu obrotów wału", ale żadne zdarzenie nie załączało rozrusznika. W tej postaci silnik nie mógł zostać uruchomiony elektrycznie.

**Dwie drogi do stanu ROZRUCH:**

| Droga | Przebieg |
|---|---|
| **Rozrusznik elektryczny** | Przycisk startu → ECU załącza przekaźnik (kanał PROFET) → wał się kręci → wykrycie triggera → iskra i wtrysk **przy pracującym rozruszniku** → obroty > próg → ECU wyłącza rozrusznik → PRACA |
| **Kopnięcie** | Wykrycie triggera bez naciśniętego przycisku → ROZRUCH bez rozrusznika → PRACA |

**Blokady i limity:**

| Warunek | Zachowanie | Decyzja |
|---|---|---|
| Silnik już pracuje (obroty > 0) | Rozrusznik nie załącza się | Ochrona zębatki i bendiksa |
| Ciągłe kręcenie > **5 s** | Rozrusznik wyłączony, komunikat na HMI | Ochrona termiczna rozrusznika |
| Przerwa między próbami | **Brak wymuszonej przerwy** | Decyzja 12.09.2026: odpowiedzialność kierowcy |
| Stan AWARIA / zatrzask | Rozrusznik zablokowany | Decyzja 1.2 |
| Zwolnienie przycisku | Natychmiastowe wyłączenie rozrusznika | Kontrola kierowcy |
| Kill switch rozwarty | Blokada sprzętowa (pin EN drivera) | Rozdz. 9.1 planu naprawczego |
| Obroty > próg (600-800 obr/min) | **Automatyczne wyłączenie rozrusznika** | Decyzja 12.09.2026 |

⚠️ **Udokumentowane ryzyko resztkowe:** limit 5 s bez wymuszonej przerwy chroni przed jednorazowym zablokowaniem przycisku, ale nie przed uporczywym odpalaniem — po zwolnieniu i ponownym naciśnięciu licznik startuje od zera. Przyjęte świadomie.

### A.4 Źródła wybudzenia z UŚPIENIA

**Architektura: MCU zarządza uśpieniem** (nie transceiver). STM32G474 pozostaje zasilany w trybie Stop i sam nasłuchuje wejść; po wybudzeniu włącza regulator 5 V dla czujników zewnętrznych. Szczegóły sprzętowe — rozdz. 6.4 dokumentu procesu.

| # | Źródło | Mechanizm | Uwagi dla FW |
|---|---|---|---|
| 1 | **Ramka CAN z HMI** | TJA1043 w Standby nasłuchuje magistrali, reaguje na filtrowany wzorzec wybudzenia → zmiana RXD → przerwanie EXTI | Po wybudzeniu MCU reinicjalizuje peryferium FDCAN. Wzorzec wybudzenia do zdefiniowania w protokole (Faza 2-Desktop) |
| 2 | **Przycisk startu** | GPIO z EXTI, rezystor podciągający | Filtrowanie drgań styku; opcjonalnie wymóg przytrzymania |
| 3 | **Przyciski na kierownicy** | Budzą HMI lokalnie → HMI wysyła ramkę CAN → budzi ECU (przez źródło 1) | — |
| 4 | **Podłączenie USB** | Wykrycie 5 V przez dzielnik → GPIO z EXTI | — |

**Wybudzanie sygnałem obrotów wału — świadomie odrzucone** (decyzja 2026-08-31, uzasadnienie w rozdz. 6.4 dok. procesu). Sygnał obrotów ma jedną ścieżkę: cewka VR → MAX9926 → MCU, a MAX9926 jest w uśpieniu bez zasilania.

**Konsekwencja dla FW i instrukcji:** jeśli ECU śpi, kopnięcie samo w sobie go nie obudzi — użytkownik musi najpierw nacisnąć przycisk. Dotyczy to zarówno czujników VR, jak i Halla.

**Wymagania FW przy zasypianiu:**
- Wyłączenie przełącznika obciążenia 5 V przez GPIO (odcina czujniki zewnętrzne, MAX9926, MLX90316)
- **Wprowadzenie w tryb niskiego poboru układów na szynie 3,3 V, która pozostaje włączona:**
  - **BMI090L (IMU)** → tryb suspend. W normalnym trybie pobiera ~5 mA, czyli ~50× cały budżet uśpienia — bez tego oszczędzanie energii nie ma sensu
  - **W25Q64 (flash)** → deep power-down (~1 µA zamiast ~15 mA przy odczycie)
  - **TJA1043** → tryb Standby (nasłuch magistrali)
- Wysłanie polecenia uśpienia do HMI po CAN, odczekanie na potwierdzenie, dopiero potem zaśnięcie własne
- Przejście MCU w tryb Stop z aktywnymi przerwaniami EXTI

**Wymagania FW przy wybudzaniu:**
- **Zapis przyczyny wybudzenia do logu diagnostycznego** — istotne przy diagnozowaniu rozładowania akumulatora
- Włączenie regulatora 5 V, odczekanie na start MAX9926 i pozostałych czujników (~1-2 ms)
- Wyprowadzenie BMI090L i W25Q64 z trybów niskiego poboru
- Reinicjalizacja peryferiów (FDCAN, ADC, timery)

### A.5 Pozostaje do doprecyzowania (przy punktach B, E)

- Czasy i warunki szczegółowe przejść (histerezy, opóźnienia)
- Maksymalny czas trwania stanu ZATRZYMYWANIE (ile na dokończenie zapisu logów)
- Okno czasowe licznika resetów watchdoga i sposób jego kasowania
- Które usterki są krytyczne (klasyfikacja — punkt E)

---

## B. Bezpieczeństwo i tryby awaryjne

*Opracowywane od 2026-09-20. Domyka pozycje audytu F-023 (macierz usterek) i część F-011.*

**Wymaganie wiążące (z decyzji L1):** okno watchdoga TPS3430-Q1 rzędu ~100 ms. Kill switch jest równolegle wejściem GPIO i sygnałem bramkującym drivery sprzętowo (rozdz. 9.1 planu naprawczego), więc jego działanie nie zależy od stanu firmware.

---

### B.1 Klasyfikacja usterek (decyzja 2026-09-20)

Klasa usterki określa **reakcję bazową** firmware. Macierz usterek (B.2) przypisuje każdej usterce dokładnie jedną klasę.

| Klasa | Nazwa | Reakcja | Ustępuje samoczynnie |
|---|---|---|---|
| **K0** | informacyjna | Zapis do logu. Bez sygnalizacji dla kierowcy | tak |
| **K1** | ostrzegawcza | Log + ostrzeżenie na HMI. Praca silnika bez zmian | tak, z histerezą |
| **K2** | zastępcza | Log + ostrzeżenie + **wartość zastępcza** podstawiana za uszkodzony czujnik | tak, z histerezą |
| **K3** | ograniczająca | Log + ostrzeżenie + **ograniczenie obrotów lub zubożenie mapy** | tak, z histerezą |
| **K4** | odcinająca | Log + ostrzeżenie + **odcięcie zapłonu i wtrysku + zatrzask** | **nie** |

**Reguła rozdzielająca:** klasy K0–K3 ustępują samoczynnie, gdy warunek zniknie (z histerezą przeciw migotaniu). Klasa K4 nie ustępuje nigdy — wymaga zatrzymania wału i świadomego odblokowania przez kierowcę (B.4). Dzięki tej regule nie trzeba przy każdej usterce z osobna rozstrzygać, czy wolno jej się „odkleić".

#### B.1.1 Uprawnienie ECU do zatrzymania silnika (decyzja 2026-09-20)

**Decyzja: ECU gasi pracujący silnik wyłącznie w przypadkach z zamkniętej listy poniżej.** Każda inna usterka skutkuje najwyżej ograniczeniem (K3) i ostrzeżeniem — decyzję o zatrzymaniu motocykla podejmuje kierowca, który ma kill switch pod kciukiem i widzi sytuację, której ECU nie widzi.

Uzasadnienie: w enduro silnik pełni również funkcję hamulca silnikowego i stabilizacji. Zgaszenie go w brodzie, na stromym podjeździe lub w koleinie kończy się przewróceniem. ECU gaszące silnik „na wszelki wypadek" jest w terenie groźniejsze niż ECU, które ogranicza moc i wyraźnie ostrzega.

**Lista zamknięta — zdarzenia powodujące odcięcie:**

| # | Zdarzenie | Podstawa | Uzasadnienie |
|---|---|---|---|
| 1 | Rozwarcie kill switcha | Funkcja podstawowa, ECU-SAF-001 | Świadoma decyzja kierowcy; realizowane także sprzętowo, niezależnie od firmware |
| 2 | Potwierdzona wywrotka (IMU) | ECU-SAF-005 | Motocykl leży — silnik nie powinien pracować |
| 3 | Reset watchdoga | ECU-SAF-003 | Przyczyna nieznana, stan sterowania nieokreślony |
| 4 | Zapaść napięcia (brown-out) | ECU-SAF-004 | Stan rejestrów i przebieg przerwanej operacji nieokreślone |
| 5 | Przekroczenie progu ogranicznika obrotów | ECU-IGN-006 | Odcięcie **chwilowe, bez zatrzasku** — funkcja normalna, nie usterka |
| 6 | **Utrata wiarygodnego sygnału obrotów przy pracującym silniku** *(przemianowane 2026-10-11 — patrz C.1.7)* | K4, decyzja 2026-09-20 | Bez sygnału obrotów nie ma bazy czasu — nie da się wyznaczyć momentu zapłonu. Alternatywą byłoby wyzwalanie w losowej fazie. Odcięcie jest tu jawnym zachowaniem zamiast stanu nieokreślonego |
| 7 | **Wtryskiwacz zablokowany otwarty** | K4, decyzja 2026-09-20 | Zwarcie kanału zgłoszone przez TLE9104SH. Zalanie cylindra: uderzenie hydrauliczne w 4T, spłukanie filmu olejowego z gładzi w 2T |
| ~~8~~ | ~~Driver zapłonu zablokowany w stanie załączonym~~ | **Wycofane 2026-09-20** | Po lekturze karty katalogowej VBG08H-E: **firmware nie ma czym tego wykryć**. Wyjście diagnostyczne C.F. odnosi się wyłącznie do stanu wejścia sterującego, więc zwarty tranzystor wyjściowy nie daje sygnału zwrotnego. Zapisanie reakcji na niewykrywalną usterkę byłoby ochroną pozorną. Zagrożenie pokrywają: ograniczenie prądu i miękkie wyłączenie w samym układzie, sprzętowy sufit czasu ładowania (B.2.3) oraz okno watchdoga — analiza w B.2.3 |

**Lista jest zamknięta.** Dopisanie do niej kolejnej pozycji wymaga osobnej decyzji zapisanej w tym dokumencie, z uzasadnieniem — inaczej lista rozrośnie się przez drobne kroki do wariantu, który odrzuciliśmy. Pozycja 8 została **wycofana tego samego dnia**, gdy okazało się, że nie da się jej wykryć — to samo kryterium, którym odrzuciliśmy zablokowany rozrusznik (B.2.2).

**Rozstrzygnięcie odrzucone — przegrzanie cieczy chłodzącej:** rozważane jako kandydat do K4, **pozostaje w K3** (ograniczenie obrotów + ostrzeżenie). Trzy powody: (a) czujnik temperatury cieczy jest jednym z najczęściej zawodzących elementów, a przerwa w przewodzie daje odczyt skrajny — fałszywe zgaszenie na podjeździe jest groźniejsze niż zagrożenie, przed którym miało chronić; (b) zgaszenie silnika zatrzymuje pompę cieczy i **pogarsza** przegrzanie lokalnie; (c) podtrzymuje wcześniejszą decyzję L5. Zmiana tej decyzji wymaga wpisu w historii zmian dokumentu.

---

### B.2 Macierz usterek

*Wszystkie cztery grupy zamknięte: 1 i 2 — 2026-09-20, 3 — 2026-09-20, 4 — 2026-09-22. **Macierz usterek jest kompletna** — 40 kodów DTC. Domyka pozycję audytu F-023.*

**Schemat kodu usterki:** `DTC-[OBSZAR]-[NUMER]`, obszary jak w `wymagania.md` (SEN, IGN, INJ, PWR, COM, SAF, SYS).

**Zasada wykrywania dla wejść analogowych:** czujnik pracuje z rezystorem podciągającym do szyny 5 V. Przerwa w przewodzie wypycha napięcie do górnej granicy, zwarcie do masy ściąga do zera — obie awarie dają odczyt poza fizycznie możliwym zakresem. Progi: **< 3% i > 97% zakresu przetwornika**, liczone względem rzeczywistego napięcia szyny 5 V (kompensacja ratiometryczna, ECU-SEN-011). Margines 3% pokrywa tolerancję czujnika i spadki na złączach, a żaden realny odczyt tam nie sięga. **Domyka wartości `[DO USTALENIA]` w ECU-SEN-007.**

#### B.2.1 Grupa 1 — czujniki (decyzja 2026-09-20)

| DTC | Usterka | Wykrycie | Czas potwierdzenia | Klasa | Reakcja firmware | Wskazanie na HMI |
|---|---|---|---|---|---|---|
| DTC-SEN-01 | Temperatura cieczy — przerwa | napięcie > 97% zakresu | 500 ms | **K2** | Wartość zastępcza (niżej) + **wentylator załączony na stałe** | Kreski `---` + komunikat „CZUJNIK TEMP. — AWARIA" |
| DTC-SEN-02 | Temperatura cieczy — zwarcie do masy | napięcie < 3% zakresu | 500 ms | **K2** | jw. | jw. |
| DTC-SEN-03 | Temperatura powietrza — przerwa lub zwarcie | jw. | 500 ms | **K2** | Wartość zastępcza 20 °C | Kreski + komunikat |
| DTC-SEN-04 **[B/C]** | Położenie przepustnicy — poza zakresem, **warianty z wtryskiem** *(MVP-A nie ma TPS — założenie Z1 obalone 11.10.2026)* | napięcie < 3% lub > 97% | **100 ms** | **K3** | **Mapa awaryjna liczona na pełne obciążenie** (bogata w całym zakresie) + ograniczenie do **3500 obr/min**. Szczegóły i uzasadnienie: B.3.2 | Poziom P2 — komunikat musi wyjaśniać, że silnik pracuje na bogato celowo |
| DTC-SEN-05 | Napięcie akumulatora — odczyt niemożliwy | poza 5–20 V (uszkodzenie dzielnika lub ADC) | 1000 ms | **K1** | Korekty napięciowe na wartościach nominalnych | Kreski + komunikat |
| DTC-SEN-06 | Prędkość koła — brak sygnału | brak impulsów przy obrotach silnika > 2000 obr/min | 3 s | **K1** | Bez wpływu na sterowanie silnikiem | Wskazanie wygaszone + komunikat |
| DTC-SEN-07 | Pozycja biegu — odczyt poza zakresem lub brak odpowiedzi | błąd transmisji SPI lub kąt poza zakresem kalibracji | 200 ms | **K1** | Bez wpływu na sterowanie silnikiem | Wskazanie biegu wygaszone |
| DTC-SEN-08 | Ciśnienie barometryczne — brak komunikacji | 3 kolejne nieudane odczyty I²C | 3 próby | **K2** | Wartość zastępcza 1013 hPa (poziom morza — mieszanka bogatsza, kierunek bezpieczny) | Komunikat |
| DTC-SEN-09 | IMU — brak komunikacji | 3 kolejne nieudane odczyty SPI | 3 próby | **K1** | Wykrywanie wywrotki nieczynne | Komunikat „WYKRYWANIE WYWROTKI NIECZYNNE" |



**Czasy potwierdzenia są celowo różne.** Czujniki wolnozmienne (temperatury, ciśnienie) mogą czekać pół sekundy — tyle i tak zajmuje im zmiana o cokolwiek istotnego, a dłuższy filtr odsiewa zakłócenia od instalacji zapłonowej. Przepustnica dostaje 100 ms, bo jest sygnałem szybkozmiennym i sterującym: czekanie pół sekundy oznaczałoby pół sekundy jazdy na błędnym odczycie.

##### Wartość zastępcza temperatury cieczy (decyzja 2026-09-20)

**Rozdzielenie wartości wyświetlanej i wartości używanej przez sterowanie — rozstrzygnięcie zasadnicze dla całej grupy K2.**

| Przeznaczenie | Wartość |
|---|---|
| Mapy wtrysku i zapłonu, logika wentylatora | **Model narastający: 20 °C na starcie, liniowo do 90 °C w ciągu 120 s pracy silnika.** Wentylator załączony na stałe |
| Wskazanie na wyświetlaczu | Kreski `---` + komunikat awarii. **Żadna liczba się nie pojawia** |

Uzasadnienie modelu narastającego: stała wartość jest zawsze błędna w jednym z dwóch momentów — podstawienie ciepłego silnika utrudnia rozruch na zimno, podstawienie zimnego wzbogaca mieszankę na ciepłym silniku i zanieczyszcza świecę. Model odwzorowuje to, co silnik realnie robi.

**Odrzucone: podstawianie wartości skrajnej (−40 °C) do sterowania.** Rozważane, ponieważ skrajne wskazanie jest dla kierowcy jednoznaczne. Odrzucone, bo myli dwa różne zadania: −40 °C podane do map oznacza dla ECU zamarznięty silnik, czyli maksymalne wzbogacenie — zalewanie, zanieczyszczenie świecy, spadek mocy w 2T — a logika wentylatora przy takiej wartości nigdy by go nie załączyła. Czytelność wskazania osiągamy po stronie wyświetlacza, nie przez psucie sterowania.

**Zasada ogólna wynikająca z tego rozstrzygnięcia:** dla każdej usterki klasy K2 macierz podaje osobno **wartość dla sterowania** (kierunek bezpieczny dla silnika) i **sposób wskazania dla kierowcy** (jednoznaczny, nigdy mylący się z pomiarem). Te dwie rzeczy nie muszą i zwykle nie powinny być tym samym.

---

#### B.2.2 Grupa 2 — sygnał obrotów, drivery, wyjścia mocy (decyzja 2026-09-20)

| DTC | Usterka | Wykrycie | Potwierdzenie | Klasa | Reakcja |
|---|---|---|---|---|---|
| DTC-IGN-01 | Brak sygnału obrotów przy pracującym silniku | brak zbocza przez 3× ostatni okres zęba, nie mniej niż 100 ms | — | **K4** | Odcięcie + zatrzask |
| DTC-IGN-02 | **Sygnał obrotów niewiarygodny** — powtarzalne naruszenie kryteriów z C.1.7 | długość wypustu poza ±25% kalibracji, zbocze poza oknem kątowym, stosunek okresów poza 0,5–2,0 | **2 kolejne obroty wału** | **K4** | Odcięcie + zatrzask |
| DTC-IGN-03 | **Odrzucone zbocze pojedyncze** | zbocze poza oknem kątowym (C.1.6) | — | **K0** | **Zbocze ignorowane**, zapłon bez zmian z modelu kąta. Wyłącznie licznik |
| DTC-IGN-03a | **Podwyższona liczba odrzuceń** — jakość sygnału | > 5 odrzuceń na 100 obrotów | 100 obrotów | **K1** | Ostrzeżenie o jakości sygnału; wskazuje na zakłócenia lub luźny czujnik |
| DTC-IGN-04 | Cewka — brak osiągnięcia progu prądu | C.F. nie wraca w stan wysoki do końca ładowania | 3 kolejne zapłony | **K3** | Wydłużenie ładowania do limitu + ograniczenie obrotów |
| DTC-IGN-05 | Cewka — próg prądu osiągany zbyt wcześnie | C.F. wraca poniżej 30% oczekiwanego czasu | 3 kolejne zapłony | **K3** | Skrócenie ładowania + ograniczenie obrotów |
| DTC-INJ-01 | Wtryskiwacz zablokowany otwarty | diagnostyka SPI TLE9104SH — zwarcie do masy | natychmiast | **K4** | Odcięcie + zatrzask |
| DTC-INJ-02 | Wtryskiwacz — przerwa obciążenia | diagnostyka SPI | 3 kolejne wtryski | **K3** | Ograniczenie obrotów — w wariancie dwuwtryskiwaczowym praca na jednym daje ubogą mieszankę |
| DTC-INJ-03 | Driver wtrysku — przegrzanie | diagnostyka SPI | natychmiast | **K3** | Ograniczenie obrotów |
| DTC-PWR-01 | Kanał pompy paliwa — zwarcie lub przeciążenie | diagnostyka BTS7008-2EPA | 3 próby ponownego załączenia | **K3** | Ograniczenie; silnik i tak zgaśnie z braku paliwa |
| DTC-PWR-02 | Kanał wentylatora — zwarcie lub przeciążenie | jw. | 3 próby | **K3** | Obniżony próg ograniczenia obrotów od temperatury |
| DTC-PWR-03 | Kanał świateł — zwarcie lub przeciążenie | jw. | 3 próby | **K1** | Kanał wyłączony |
| DTC-PWR-04 | Kanał rozrusznika zablokowany załączony | prąd mimo wyłączonego sterowania — *możliwość wykrycia do potwierdzenia w Fazie 4* | 200 ms | **K1** | Komunikat „ODŁĄCZ AKUMULATOR" |
| DTC-SYS-01 | Przegrzanie ECU | czujnik temperatury w mikrokontrolerze | 5 s | **K3** | Skrócenie ładowania cewki + ograniczenie obrotów |

**Przebudowa DTC-IGN-02 i 03 — korekta 2026-10-11 po pomiarach koła impulsowego.** Dotychczasowe brzmienie mówiło o wzorze zębów i zgubionym zębie, czyli opisywało detekcję właściwą dla koła 60-2. **Beta 300 RR ma jeden wypust na obrót**, więc nie ma wzoru zębów ani zgubionego zęba — oba zapisy opisywały mechanizm, którego nie da się zrealizować.

W dwusuwie nie występuje też **utrata synchronizacji** w sensie czterosuwowym: silnik pali co obrót, jeden wypust to jedna iskra, nie ma dwuznaczności suwu do rozstrzygnięcia. Realnym zagrożeniem nie jest utrata fazy, tylko **fałszywe zbocze od instalacji zapłonowej**, które przesunęłoby iskrę w przypadkowy kąt.

**Dlaczego DTC-IGN-03 jest klasy K0 i nie powoduje żadnej reakcji poza zliczeniem:** zbocze rozpoznane jako fałszywe jest **ignorowane**, a zapłon przebiega normalnie na podstawie ciągłego modelu kąta (C.1.3). Nie traci się iskry i nie gasi silnika. Dopiero powtarzalne naruszenie kryteriów przechodzi w DTC-IGN-02, a podwyższona liczba odrzuceń w DTC-IGN-03a jako ostrzeżenie o jakości instalacji. Mechanizm bramkowania kątowego — C.1.6.

**Dlaczego zablokowany rozrusznik nie trafia do K4**, mimo że niszczy mechanikę: odcięcie zapłonu nic tu nie daje. Zwarty kanał wysokiego napięcia pozostaje zwarty niezależnie od tego, czy silnik pracuje, a zgaszenie silnika nie przerywa pracy rozrusznika. Jedyne skuteczne działanie jest po stronie kierowcy — odłączenie zasilania. Wpisanie tego do K4 dawałoby złudzenie ochrony.

---

#### B.2.3 Wyjście diagnostyczne VBG08H-E i sprzętowy limit czasu ładowania (ustalenia 2026-09-20)

**Wyjście C.F.** VBG08H-E (pin 6, otwarty dren) przechodzi w stan niski, gdy wejście sterujące idzie w stan wysoki, i wraca w stan wysoki, **gdy prąd cewki osiągnie stały próg 6,5 A** (wartość zależna od temperatury). Ogranicznik prądu układu działa dopiero przy 8,5–10,5 A, klamra przepięciowa przy 320–400 V, miękkie wyłączenie przy temperaturze złącza 150–175 °C.

**Zastosowanie: wyłącznie diagnostyka** (DTC-IGN-04, DTC-IGN-05). Czas od podania sterowania do powrotu C.F. to zmierzony czas dojścia cewki do 6,5 A: brak powrotu oznacza przerwę w obwodzie, powrót zbyt szybki — zwarcie zwojów.

**Odrzucone: sterowanie czasem ładowania w pętli zamkniętej na podstawie C.F.** Propozycja rozważana 2026-09-20 i **wycofana po sprawdzeniu karty katalogowej**: ST opisuje C.F. wyłącznie jako wyjście diagnostyczne, bez żadnej wzmianki o wykorzystaniu do regulacji. Dodatkowo próg 6,5 A należy do układu, nie do cewki, i dryfuje z temperaturą — regulowalibyśmy do wielkości, która nie jest parametrem sterowanego obiektu. ECU-IGN-003 (korekta w funkcji napięcia) pozostaje bez zmian. Temat może wrócić po pomiarach na stanowisku w Fazie 6 jako świadomy eksperyment z własną walidacją.

**Ograniczenie konstrukcyjne wynikające z progu C.F.:** czas ładowania musi być na tyle długi, by prąd cewki przekroczył 6,5 A — inaczej C.F. nigdy nie zmieni stanu i diagnostyka odczyta sprawną cewkę jako przerwaną. **Do sprawdzenia przy doborze cewki w Fazie 4.**

##### Decyzja architektoniczna: impuls zapłonu generuje peryferium, nie program

**Decyzja 2026-09-20.** Impuls sterujący driverem zapłonu powstaje w peryferium HRTIM mikrokontrolera, a nie przez zapis do rejestru portu z poziomu zadania.

Uzasadnienie liczbowe: przy 6000 obr/min jeden stopień obrotu wału trwa 27,8 µs, przy 10 000 obr/min — 16,7 µs. Wymaganie ECU-IGN-002 dopuszcza błąd ≤ 1,0° w 99,9 percentylu. Wyjście przełączane z poziomu zadania podlega opóźnieniom obsługi przerwań i szeregowania rzędu dziesiątek mikrosekund, czyli rzędu całego budżetu błędu — **wymaganie byłoby niespełnialne niezależnie od jakości kodu**. Układ porównania w timerze wystawia zbocze z jitterem rzędu nanosekund.

To jest standard branżowy, nie rozwiązanie autorskie: NXP eTPU to osobny procesor z własnym rdzeniem i pamięcią, z gotowymi funkcjami *Spark and Dwell Time*, sterowania wtryskiem i trybem kątowym; Infineon AURIX ma GTM, Renesas RH850 ma ATU. Decyzja porządkuje też wybór STM32G474 — układ wybrano właśnie za HRTIM, a przy sterowaniu programowym HRTIM byłby zbędny.

##### Sprzętowy sufit czasu ładowania — domknięcie ECU-IGN-005

**Zweryfikowane 2026-09-20 bezpośrednio w STM32CubeMX na STM32G474VETx.** Parametr `Reset Source Selection` wyjścia HRTIM przyjmuje **liczbę aktywnych źródeł kasowania od 0 do 32**; po jej wpisaniu pojawiają się osobne pozycje „1st Reset Source", „2nd Reset Source" itd. Lista źródeł zawiera między innymi:

- *Timer counter reset event coming solely from software*
- **Timer period event forces the output to its inactive state**
- *Timer compare 1 / 2 / 3 / 4 event forces the output to its inactive state*
- *The master timer period event forces the output to its inactive state*

Zdarzenie końca okresu i zdarzenie porównania można więc przypisać **jednocześnie** jako niezależne źródła kasowania.

**Konfiguracja wynikająca z tego ustalenia:**

| Rejestr | Kto zapisuje | Rola |
|---|---|---|
| Okres (PER) | ustawiany **raz przy inicjalizacji**, jako stała konfiguracyjna | **Maksymalny dopuszczalny czas ładowania — sufit sprzętowy** |
| Porównanie (CMP) | zapisywany przez zadanie zapłonu **w każdym cyklu** | Rzeczywisty czas ładowania z mapy |
| Źródła kasowania wyjścia | ustawiane raz | **Zdarzenie porównania ORAZ zdarzenie końca okresu** |

Skutek: utknięte zadanie zapłonu nie przedłuży impulsu, bo licznik dojdzie do okresu i zdejmie wyjście. **Błędna wartość porównania — nawet większa od okresu — również go nie wydłuży**, bo zdarzenie końca okresu kasuje wyjście niezależnie. Zadanie zapłonu nie ma drogi, żeby ten sufit podnieść, bo nie dotyka rejestru okresu.

**To domyka ECU-IGN-005 i pozycję otwartą z rozdz. 9.1 planu naprawczego — bez ani jednego dodatkowego elementu.** Weryfikacja: T-IGN-005 (wstrzyknięcie usterki z zawieszonym firmware, pomiar długości impulsu).

**Analiza uzupełniająca — ile realnie grozi przy zawieszonym firmware.** Prąd jest ograniczony przez układ do 8,5–10,5 A. Przy rezystancji uzwojenia pierwotnego rzędu 0,4 Ω daje to około 40 W traconych w cewce plus 15–20 W na tranzystorze. Okno watchdoga wynosi 100 ms, po którym następuje reset, a rezystory ściągające zdejmują sterowanie. Cewka przyjmuje w tym czasie **około 6 J**, co przy jej masie rzędu 0,3 kg oznacza przyrost temperatury poniżej jednej dziesiątej stopnia. Sufit z rejestru okresu skraca to jeszcze o rząd wielkości. Sprzętowy układ monostabilny byłby więc wydatkiem bez pokrycia w zagrożeniu.

**Pozostaje do zweryfikowania w Fazie 5:** tryb pracy licznika (single shot retriggerable / non-retriggerable / continuous) właściwy dla sterowania kątowego. Nie wpływa na samą zasadę sufitu, bo zdarzenie końca okresu występuje w każdym z tych trybów.

---

#### B.2.4 Grupa 3 — komunikacja i zasilanie (decyzja 2026-09-20)

| DTC | Usterka | Wykrycie | Potwierdzenie | Klasa | Reakcja |
|---|---|---|---|---|---|
| DTC-COM-01 | Zanik komunikacji z HMI | brak poprawnej ramki od HMI | 1000 ms (ECU-DIA-003) | **K1** | Log + praca silnika bez zmian |
| DTC-COM-02 | Ramka odrzucona — suma kontrolna lub licznik sekwencyjny | pojedyncze odrzucenie | — | **K0** | Tylko licznik odrzuceń |
| DTC-COM-02a | Seria odrzuceń — pogorszona jakość magistrali | > 10 odrzuceń w 1 s | — | **K1** | Komunikat „ZAKŁÓCENIA MAGISTRALI" |
| DTC-COM-03 | Kontroler CAN w stanie bus-off | flaga peryferium FDCAN | — | **K1** | Automatyczne odzyskiwanie; 3 wystąpienia w 10 s → komunikat |
| DTC-COM-04 | Niezgodność wersji protokołu ECU↔HMI | wymiana numerów wersji przy nawiązaniu połączenia (SYS-COM-005) | natychmiast | **K1** | **HMI wygasza wszystkie dane i wyświetla wyłącznie komunikat o niezgodności** — patrz decyzja niżej |
| DTC-PWR-05 | Napięcie akumulatora niskie przy pracującym silniku | < 11,0 V **przy obrotach > 2000 obr/min** | 5 s | **K1** | Ostrzeżenie „ŁADOWANIE — AWARIA" |
| DTC-PWR-06 | Napięcie krytycznie niskie | < 9,0 V | 2 s | **K1** | Ostrzeżenie krytyczne; poniżej 9,0 V wychodzimy poza SYS-ENV-001 |
| DTC-PWR-07 | Przepięcie | > 16,5 V | 200 ms | **K1** | Ostrzeżenie + **załączenie wentylatora jako obciążenia**; wyłączenie po spadku poniżej 15,5 V |
| DTC-PWR-08a | **Szyna 5 V poza tolerancją, w zakresie pracy MAX9926** | ADC w przedziale 4,50–4,75 V lub 5,25–5,50 V | 100 ms | **K3** | Odczyty czujników niewiarygodne mimo kompensacji ratiometrycznej — strategia jak przy utracie TPS (grupa G3, B.3.1) |
| DTC-PWR-08b | **Szyna 5 V poniżej zakresu pracy lub Power Good nieaktywny** | ADC < 4,50 V albo > 5,50 V, albo PG nieaktywny | 100 ms | **K4** | MAX9926 przestaje pracować, sygnał obrotów zanika i silnik gaśnie przez DTC-IGN-01. **Przyczyna źródłowa dla zatrzasku** — patrz decyzja niżej |
| DTC-PWR-09 | Szyna 3,3 V poza zakresem | ADC poza 3,15–3,45 V | 100 ms | **K1** | Ostrzeżenie + wymuszony zapis logu; przy dalszym spadku sprawę przejmuje brown-out (DTC-SAF, grupa 4) |
| DTC-PWR-10 | Przełącznik obciążenia 5 V nie załączył się | brak napięcia na szynie czujników po 5 ms od załączenia | 3 próby | **K3** | Blokada wyjścia ze stanu GOTOWOŚĆ — bez tej szyny nie ma odczytów czujników |

**Warunek obrotów przy DTC-PWR-05 jest konieczny.** Przy rozruchu zapad napięcia do 9 V jest normalny — rozrusznik pobiera kilkadziesiąt amperów. Bez warunku `obroty > 2000` ECU zgłaszałoby awarię ładowania przy każdym odpaleniu i kierowca przestałby zwracać uwagę na ten komunikat, co jest gorsze niż jego brak.

**Rozdzielenie DTC-PWR-08 — korekta wprowadzona 2026-09-22 po uwadze Pawła.** Pierwotnie awaria szyny 5 V miała jedną klasę K3 z ograniczeniem obrotów. To było niepełne: **MAX9926 jest zasilany z tej szyny**, więc przy jej zaniku nie ma czego ograniczać — silnik gaśnie z braku sygnału obrotów. Ograniczenie ma sens wyłącznie w paśmie, w którym szyna jest poza tolerancją, a układ dalej pracuje (4,50–5,50 V wg karty katalogowej MAX9926, przy progu wykrycia 4,75–5,25 V). Stąd dwie pozycje zamiast jednej.

Klasa K4 dla DTC-PWR-08b nie narusza zamkniętej listy zdarzeń odcinających z B.1.1 — odcięcie następuje przez zdarzenie 6 (utrata sygnału synchronizacji), które na tej liście jest. DTC-PWR-08b wskazuje przyczynę źródłową, nie tworzy nowego zdarzenia odcinającego.

##### Decyzja — niezgodność wersji protokołu (2026-09-20)

**Przyjęte: każda niezgodność wersji wygasza dane na HMI.** Wyświetlacz pokazuje wyłącznie komunikat o niezgodności wraz z obiema wersjami; żadna wartość pomiarowa się nie pojawia.

Rozważany był podział na niezgodność `major` (dane wygaszone) i `minor` (dane pokazywane z ostrzeżeniem). **Odrzucony na rzecz jednej reguły.** Uzasadnienie wyboru: jedna ścieżka w kodzie i jeden przypadek testowy zamiast dwóch, brak klasy błędów polegających na złej ocenie, które pole jeszcze wolno zinterpretować. Przy wskazaniach, od których zależy prowadzenie motocykla, brak wskazania jest jednoznaczny, a wskazanie możliwie fałszywe — nie.

**Koszt tej decyzji i jak go usuwamy.** Skutkiem ubocznym jest to, że aktualizacja samego ECU zostawia kierowcę bez wskazań do czasu aktualizacji HMI. **Rozwiązanie przenoszone do punktu H (bootloader): pakiet aktualizacyjny zawiera obrazy firmware ECU i HMI razem, a aktualizacja jest jedną transakcją** — ECU jest nadrzędne na magistrali i potrafi przeprogramować HMI (SYS-COM-001a), więc rozdzielenie tych dwóch aktualizacji nie jest nikomu potrzebne. Przy takim pakiecie niezgodność wersji przestaje występować w normalnej eksploatacji i zostaje wyłącznie jako zabezpieczenie na wypadek podmiany jednego z modułów.

##### Decyzja — kolejność diagnozowania przy awarii szyny 5 V (2026-09-20)

**Przyjęte: przy jednoczesnym wystąpieniu DTC-PWR-08 i DTC-IGN-01 firmware zapisuje obie usterki, ale jako przyczynę zatrzasku podaje awarię zasilania.**

Powód wynika z topologii, nie z preferencji: MAX9926 pracuje na szynie 5 V, więc jej awaria zabiera sygnał obrotów i silnik gaśnie przez DTC-IGN-01 (K4, zatrzask). Bez reguły pierwszeństwa w logu zostałby „brak sygnału obrotów", co poprowadziłoby diagnostykę do cewki VR i okablowania czujnika — czyli w miejsce, gdzie nic nie jest uszkodzone.

**Zasada ogólna:** gdy jedna usterka jest fizyczną przyczyną drugiej, macierz wskazuje przyczynę źródłową jako powód przejścia w stan awarii. Pozostałe zapisywane są jako towarzyszące. Druga para tego rodzaju to DTC-PWR-10 i usterki odczytu czujników.

##### Odrzucone — MAX9926 poza przełącznikiem obciążenia (2026-09-20)

**Propozycja postawiona i wycofana tego samego dnia, po sprawdzeniu karty katalogowej.**

Propozycja brzmiała: zasilić MAX9926 bezpośrednio z przetwornicy 5 V i usypiać go własnym wejściem SHDN, żeby usunąć jeden z dwóch szeregowych punktów awarii w torze sygnału obrotów (dziś są to przetwornica **i** przełącznik obciążenia).

**Powód wycofania — karta katalogowa MAX9926:**

| Parametr | Wartość |
|---|---|
| Wejście shutdown lub standby | **nie istnieje** — układ ma tryby pracy A1, A2, B, C, żaden nie redukuje poboru |
| Prąd zasilania ICC | **4,7 mA typowo, 10 mA maksymalnie** |

Propozycja opierała się na założeniu, że układ ma wejście SHDN. Nie ma. Nawet gdyby miało to być odcięcie samym EN przetwornicy, 4,7 mA to ponad trzydziestokrotność całego budżetu uśpienia ECU (150 µA, ECU-PWR-001) i około 3400 mAh miesięcznie — więcej niż pojemność akumulatora. **Odcięcie zasilania jest jedyną drogą, a przełącznik obciążenia jest do tego właściwym miejscem.**

Zapis ten zostaje w dokumencie jako ostrzeżenie: rozdz. 6.4 dokumentu procesu **już zawierał** ten wniosek przy odrzucaniu wybudzania sygnałem obrotów, a propozycja i tak powstała. Przy okazji poprawiono tam oszacowanie poboru z „2 mA" na rzeczywiste 4,7 mA.

**Zagrożenie, które propozycja miała usunąć, pozostaje realne i jest adresowane inaczej:** awaria przełącznika obciążenia oznacza brak sygnału obrotów przy sprawnej reszcie toru. Odpowiedzią jest **ECU-PWR-010 i DTC-PWR-10** — wykrycie braku napięcia na szynie czujników po 5 ms od załączenia i zablokowanie wyjścia ze stanu GOTOWOŚĆ z jawnym komunikatem. Cicha awaria staje się awarią zdiagnozowaną, zanim kierowca zacznie kopać.

---

#### B.2.5 Grupa 4 — bezpieczeństwo, autotest i pamięć (decyzja 2026-09-22)

| DTC | Usterka | Wykrycie | Potwierdzenie | Klasa | Reakcja |
|---|---|---|---|---|---|
| DTC-SAF-01 | **Przerwa w przewodzie kill switcha lub rozłączona wtyczka** | napięcie na wejściu w górnym oknie (powyżej poziomu STOP) | 50 ms | **K4** | Odcięcie sprzętowe (komparator) + zatrzask + komunikat „PRZERWA W PRZEWODZIE KILL SWITCHA" |
| DTC-SAF-01a | Kill switch naciśnięty | napięcie w oknie środkowym | 50 ms | — | Normalne gaszenie silnika, **bez zatrzasku**, bez usterki |
| DTC-SAF-02 | Reset watchdoga | rejestr przyczyny resetu w STM32G474 | natychmiast | **K4** | Zatrzask + zapis migawki (B.2.5.3) + inkrementacja licznika |
| DTC-SAF-03 | Trzeci reset watchdoga | licznik ≥ 3, zerowany po 60 s bezawaryjnej pracy silnika (ECU-SAF-006) | — | **K4** | Stan AWARIA trwały, koniec prób startu, kasowanie wyłącznie aplikacją desktop |
| DTC-SAF-04 | Zapaść napięcia (brown-out) | flaga BOR w STM32G474 | natychmiast | **K4** | Zatrzask + zapis migawki |
| DTC-SAF-05 | **Potwierdzona wywrotka** | kąt przechyłu **> 65°** z BMI090L | **3 s nieprzerwanie** | **K4** | Odcięcie + zatrzask |
| DTC-SYS-02 | Błędna suma kontrolna firmware | autotest pełny przy starcie | — | — | **Brak startu**, komunikat, wejście w tryb bootloadera |
| DTC-SYS-03a | **Błędna suma kontrolna map sterowania** (zapłon, wtrysk, korekty, progi wentylatora, próg ogranicznika) | autotest pełny przy starcie | — | — | **Blokada startu silnika** + komunikat „MAPY USZKODZONE — WGRAJ PONOWNIE" |
| DTC-SYS-03b | **Błędna suma kontrolna konfiguracji użytkownika** (obwód koła, jednostki, wygląd HMI, jasność) | autotest pełny przy starcie | — | **K1** | Podstawienie wartości domyślnych + ostrzeżenie. **Silnik pracuje normalnie** |
| DTC-SYS-04 | Błąd testu RAM | autotest pełny przy starcie | — | — | Brak startu, komunikat |
| DTC-SYS-05 | Brak komunikacji z pamięcią W25Q64 | 3 nieudane odczyty SPI | 3 próby | **K1** | Logowanie i czarna skrzynka nieczynne, silnik pracuje |
| DTC-SYS-06 | Błąd zapisu do pamięci | weryfikacja odczytem po zapisie | 3 próby na różnych sektorach | **K1** | Po wyczerpaniu prób jak DTC-SYS-05 |
| DTC-SYS-07 | Brak wolnych sektorów lub zużycie pamięci | licznik cykli kasowania sektora | — | **K0** | Nadpisywanie najstarszych wpisów, zapis zdarzenia |
| DTC-SYS-08 | Zegar utracił czas | superkondensator rozładowany, rejestr zegara niezainicjalizowany | — | **K0** | Znaczniki czasu względne od startu, **oznaczone w logu jako niepewne** |
| DTC-SYS-09 | Driver wtrysku zgłasza utratę konfiguracji | rejestr stanu SPI TLE9104SH | 3 próby ponownej konfiguracji | **K3** | Po wyczerpaniu prób ograniczenie obrotów |
| DTC-SYS-10 | Niespójny licznik motogodzin | suma kontrolna rekordu | — | **K1** | Odtworzenie z ostatniego spójnego zapisu, zdarzenie w logu |

**Zakres autotestu pełnego:** DTC-SYS-02, 03a, 03b, 04. Wykonywany po podłączeniu akumulatora i po aktualizacji firmware.

**Zakres autotestu skróconego przy zwykłym wybudzeniu — domyka ECU-PWR-003a:** suma kontrolna map sterowania (DTC-SYS-03a) **oraz** odczyt identyfikatora pamięci W25Q64 (DTC-SYS-05). Pominięte: suma kontrolna firmware i test RAM. Uzasadnienie: firmware i RAM nie zmieniają się między uśpieniem a wybudzeniem — od ostatniego pełnego testu nikt ich nie dotykał. Mapy natomiast mogły zostać nadpisane przez aplikację desktop tuż przed uśpieniem, a to jedyna rzecz w tym zestawie, która potrafi się zmienić bez restartu. Suma kontrolna map to pojedyncze przejście przez kilkadziesiąt kilobajtów — mieści się w budżecie 200 ms (ECU-PWR-003) z zapasem.

---

##### B.2.5.1 Kill switch — rozpoznanie trzech stanów (decyzja 2026-09-22)

**Przyjęte: układ trzypoziomowy z bramkowaniem komparatorem.**

Problem: przy zwykłym okablowaniu normalnie zamkniętym przerwa w przewodzie i naciśnięcie przycisku dają ten sam stan elektryczny. Kierunek jest bezpieczny w obu przypadkach, ale ECU-SAF-002 wymaga **zapisania usterki przerwania przewodu**, czego dwa stany nie umożliwiają.

**Rozwiązanie:**

```
        5 V
         │
        R_pull (w ECU)
         │
         ├──────────────► wejście ADC mikrokontrolera (rozpoznanie 3 stanów)
         │
         ├──────────────► komparator ──► bramkowanie EN driverów (niezależne od FW)
         │
      ─ ─┼─ ─ ─ ─ ─ ─ ─ ─ ─ złącze ─ ─ ─ ─ ─ ─ ─ ─ ─
         │
        R_ser (w wiązce, przy przycisku)
         │
         ├── styk kill switcha ──► masa      (zwarty = RUN)
         │
        R_par (w wiązce, równolegle do styku)
         │
        masa
```

| Stan | Droga do masy | Napięcie na wejściu | Bramkowanie |
|---|---|---|---|
| **RUN** — styk zwarty | R_ser | **dolne** | przepuszcza |
| **STOP** — styk rozwarty | R_ser + R_par | **środkowe** | odcina |
| **Przerwa lub rozłączona wtyczka** | brak | **górne (pełne podciągnięcie)** | odcina |

**Bramkowanie sprzętowe wymaga jednego komparatora, nie dwóch.** Próg ustawiony pomiędzy poziomem RUN a poziomem STOP odcina zarówno przy naciśnięciu, jak i przy przerwie — obie sytuacje leżą powyżej progu. Rozróżnieniem zajmuje się mikrokontroler, czytając ten sam punkt przetwornikiem, i robi to wyłącznie na potrzeby logu i komunikatu. **Funkcja bezpieczeństwa nie zależy od tego odczytu.**

**Bilans pinów bez zmian.** Wejście kill switcha już istnieje; wymaga jedynie przypisania do pinu z dostępem do przetwornika ADC. Wyjście komparatora prowadzi do wejść EN driverów po stronie płytki i nie zajmuje pinu złącza.

**Zachowanie przy zwykłym przycisku bez rezystorów w wiązce** (ktoś podłączy fabryczny kill switch): styk zwarty daje poziom dolny, czyli RUN — poprawnie; styk rozwarty daje poziom górny, czyli odcięcie — również poprawnie, ale zgłoszone jako przerwa w przewodzie. **Degradacja jest bezpieczna**: funkcja działa, myli się wyłącznie komunikat. Wymóg zastosowania wiązki z rezystorami trafia do wymagań instalacyjnych (rozdz. 6.7 dok. procesu).

**Do domknięcia w Fazie 4:** wartości R_pull, R_ser i R_par wraz z analizą najgorszego przypadku (tolerancje rezystorów, rezystancja przejścia styku, spadki na złączach i wiązce) oraz dobór komparatora. **Komparatora świadomie nie wskazuję teraz** — zgodnie z zasadą przyjętą 20.09.2026 propozycja komponentu powstaje dopiero po sprawdzeniu karty katalogowej i dostępności w TME.

**Rozważone i odrzucone: wykorzystanie komparatora wbudowanego w STM32G474.** Układ ma sprzętowe komparatory z bezpośrednim połączeniem do HRTIM, więc kusi, żeby nie dokładać elementu. Odrzucone, bo komparator wewnętrzny jest konfigurowany przez firmware, a błąd firmware może go przekonfigurować lub wyłączyć — to dokładnie ta zależność, którą audyt zakwestionował w pozycji F-004. Zewnętrzny komparator działa od chwili podania zasilania i firmware nie ma do niego dostępu.

---

##### B.2.5.2 Uszkodzone mapy — blokada startu, z rozdzieleniem na dwa zakresy (decyzja 2026-09-22)

**Przyjęte: uszkodzenie map sterowania blokuje start silnika.** Odrzucone warianty: start na mapach awaryjnych zaszytych w firmware oraz start na drugiej kopii map. Uzasadnienie wyboru: praca silnika na czymkolwiek niezweryfikowanym to ryzyko po stronie silnika, a nie po stronie wygody.

**Doprecyzowanie wprowadzone przy zapisie decyzji — rozdzielenie DTC-SYS-03 na dwie pozycje.** Pierwotny zapis obejmował jedną sumą kontrolną „mapy lub konfigurację", co oznaczałoby, że uszkodzony bajt w ustawieniu jednostek prędkości albo w wyglądzie ekranu HMI unieruchamia motocykl. To nie jest to, co decyzja miała osiągnąć.

| Zakres | Zawartość | Reakcja na uszkodzenie |
|---|---|---|
| **Mapy sterowania** (DTC-SYS-03a) | Mapa zapłonu, mapa wtrysku, korekty (temperatura, ciśnienie, napięcie), progi wentylatora, próg i histereza ogranicznika obrotów, czasy ładowania cewki | **Blokada startu** |
| **Konfiguracja użytkownika** (DTC-SYS-03b) | Obwód koła, jednostki, układ i wygląd ekranów HMI, jasność podświetlenia, wybrany profil wyglądu | **Wartości domyślne + ostrzeżenie, silnik pracuje** |

Kryterium podziału: **czy wartość wpływa na to, co ECU robi z silnikiem.** Progi wentylatora i ogranicznika są po stronie map mimo że wyglądają na ustawienia użytkownika, bo ich uszkodzenie może doprowadzić do przegrzania lub przekroczenia obrotów.

**Ryzyko przyjęte świadomie:** uszkodzenie map unieruchamia motocykl tam, gdzie nie ma laptopa. Ograniczają je dwie rzeczy już obecne w projekcie — zapis transakcyjny map (APP-COM-006), który eliminuje przerwaną aktualizację jako przyczynę, oraz weryfikacja odczytem po zapisie (DTC-SYS-06). Pozostaje awaria samej pamięci, a przy uszkodzonej pamięci jazda na zawartości tej pamięci nie jest bezpieczniejsza od postoju.

---

##### B.2.5.3 Migawka stanu przy resecie watchdoga (decyzja 2026-09-22)

**Przyjęte: licznik resetów w pamięci nieulotnej, a wraz z nim zapis kontekstu — co się działo w chwili, gdy watchdog musiał zadziałać.** Sam licznik mówi, że coś zawiodło; nie mówi co, a to jest informacja o największej wartości diagnostycznej w całym systemie.

**Mechanizm dwustopniowy — rozwiązuje problem zużycia pamięci Flash:**

| Etap | Gdzie | Kiedy zapis |
|---|---|---|
| **Ślad bieżący** | rejestry domeny podtrzymywanej w STM32 (superkondensator) | **w trakcie pracy**, przy każdym punkcie kontrolnym — zero zapisów do Flash |
| **Migawka** | W25Q64 | **raz, po resecie**, w trakcie startu — ślad bieżący przepisywany do pamięci trwałej razem z licznikiem |

Zużycie Flash jest z definicji ograniczone: zapis następuje wyłącznie po resecie watchdoga, a trzeci reset przenosi ECU w trwały stan awarii i kończy dalsze próby. **Scenariusz pętli resetów, który licznik ma wykrywać, daje najwyżej trzy zapisy.**

**Zawartość migawki:**

| Pole | Po co |
|---|---|
| Przyczyna resetu z rejestru MCU | Rozróżnienie: watchdog niezależny, watchdog okienkowy, brown-out, reset programowy, reset pinem |
| **Ostatni osiągnięty punkt kontrolny** | Wskazuje miejsce w przebiegu programu, w którym wykonanie się zatrzymało — bez tego licznik jest bezużyteczny diagnostycznie |
| Stan maszyny stanów | GOTOWOŚĆ, ROZRUCH, PRACA, ZATRZYMYWANIE |
| Obroty silnika | Czy awaria wiąże się z zakresem obrotów |
| Napięcie akumulatora i obu szyn | Odróżnienie awarii firmware od zapadu zasilania |
| Temperatura mikrokontrolera | Odróżnienie awarii od przegrzania |
| Czas od startu i licznik motogodzin | Czy awaria występuje cyklicznie |
| Wersja firmware i suma kontrolna map | Powiązanie awarii z konkretną wersją |
| Aktywne kody usterek | Kontekst — co było już zgłoszone przed resetem |

**Punkt kontrolny jest kluczem.** Żeby po resecie wiedzieć, gdzie wykonanie utknęło, firmware musi zostawić ślad **zanim** się zawiesi. Realizacja: każde zadanie czasu rzeczywistego przy wejściu zapisuje swój identyfikator do rejestru podtrzymywanego. Zapis to jedna instrukcja, więc narzut jest pomijalny, a po resecie rejestr trzyma identyfikator zadania, które nie zdążyło się zakończyć. **Lista identyfikatorów powstaje w punkcie I (architektura zadań czasu rzeczywistego)** i musi pokrywać wszystkie zadania — zadanie bez identyfikatora jest luką w diagnostyce.

**Odczyt migawek:** aplikacja desktop, zakładka diagnostyki. Przechowywane są **trzy ostatnie migawki**, nie tylko najnowsza — przy usterce występującej cyklicznie porównanie kolejnych wystąpień jest tym, co pokazuje wzorzec.

---

##### B.2.5.4 Wywrotka — próg i czas potwierdzenia (decyzja 2026-09-22)

**Przyjęte: kąt przechyłu powyżej 65° utrzymany nieprzerwanie przez 3 s.** Jeden warunek, jeden próg, bez sprzężenia z innymi czujnikami.

Odrzucono wariant z dodatkowym warunkiem prędkości koła poniżej 5 km/h. Powód jest konkretny: po wywrotce koło często kręci się dalej napędzane silnikiem, więc warunek prędkości potrafi **zablokować** wykrycie dokładnie w sytuacji, do której został pomyślany. Odrzucono też próg 80° przy 1 s — wywrotka zatrzymana na drzewie, skale lub w koleinie zatrzymuje się pod mniejszym kątem, a to w terenie przypadek częsty.

**Wartości są wstępne.** Do skorygowania pomiarem w Fazie 8: rejestracja kąta przechyłu podczas normalnej jazdy w terenie i sprawdzenie, jak blisko 65° dochodzi jazda, która wywrotką nie jest. Kryterium korekty: **zero fałszywych zadziałań podczas sesji testowej**, przy zachowaniu wykrycia rzeczywistego przewrócenia.

**Warunek uzupełniający:** wykrywanie działa wyłącznie w stanie PRACA. W stanie GOTOWOŚĆ motocykl stojący na podpórce bocznej ma przechył rzędu 25–30° i nie ma czego odcinać.

---

### B.3 Tryb pracy zastępczej (limp-home)

*Opracowany 2026-09-22. Domyka lukę L4 i ryzyko związane z pracą przy niepełnych danych.*

**Tryb zastępczy nie jest osobnym stanem maszyny stanów.** Stan AWARIA obsługuje klasę K4. Klasa K3 pozostaje w stanie PRACA z nałożonymi ograniczeniami — bo silnik ma dalej jechać.

#### B.3.1 Podział deratingu według tego, czego ECU nie wie (decyzja 2026-09-22)

Kryterium ograniczenia nie jest „jak poważna wydaje się usterka", tylko **jakiej informacji ECU zostało pozbawione i czy da się ją czymś zastąpić**.

| Grupa | Czego ECU nie wie | Reakcja | Usterki |
|---|---|---|---|
| **G1 — wartość zastępcza wystarcza** | Temperatura powietrza, ciśnienie atmosferyczne. Wpływ na dawkę rzędu kilku procent | **Bez ograniczeń, pełny zakres obrotów.** Wartość zastępcza + ostrzeżenie | DTC-SEN-03, DTC-SEN-08 (klasa K2) |
| **G2 — ochrona termiczna lub elektryczna** | Nic — dane są poprawne, problem jest po stronie sprzętu | **Limit obrotów 5000 obr/min, mapy bez zmian.** Cel: zdjęcie obciążenia z przegrzanego lub uszkodzonego elementu | DTC-INJ-03, DTC-PWR-01, DTC-PWR-02, DTC-SYS-01, DTC-SYS-09 |
| **G3 — utrata sygnału obciążenia** | Położenie przepustnicy (warianty B/C) albo szyna 5 V. **W MVP-A zostaje wyłącznie przypadek szyny 5 V — TPS w tym wariancie nie istnieje** | **Osobna strategia (B.3.2)** — mapa awaryjna + limit 3500 obr/min | DTC-SEN-04, DTC-PWR-08a |

Grupa G1 nie ogranicza niczego celowo. Podstawienie 20 °C za temperaturę powietrza albo 1013 hPa za ciśnienie zmienia dawkę o kilka procent — to mniej niż różnica między porankiem a popołudniem tego samego dnia. Ograniczanie obrotów z tego powodu byłoby karą bez przyczyny.

**Łączenie wielu jednoczesnych usterek: nie sumują się.** Obowiązuje najniższy limit obrotów i największe cofnięcie zapłonu spośród aktywnych. Sumowanie dałoby przy dwóch drobnych usterkach ograniczenie ostrzejsze niż przy jednej poważnej.

**Wyjście z trybu:** gdy wszystkie usterki ustąpią z histerezą, limit wraca narastająco — tym samym mechanizmem co zjazd (B.3.3), w drugą stronę.

#### B.3.2 Utrata sygnału przepustnicy — mapa awaryjna liczona na pełne obciążenie (decyzja 2026-09-22)

**Problem postawiony przez Pawła:** bez sygnału przepustnicy ECU nie wie, ile paliwa podać. Jeżeli utrzyma dawkę z biegu jałowego, to po otwarciu przepustnicy mieszanka stanie się skrajnie uboga.

**Doprecyzowanie skutku:** silnik wtedy nie zgaśnie, tylko **się zatrze**. Zgaśnięcie z ubogiej mieszanki to wariant szczęśliwy. W dwusuwie uboga mieszanka pod obciążeniem oznacza przegrzany tłok, a przy dużym otwarciu przepustnicy obciążenie jest realne niezależnie od tego, czy ECU o nim wie.

**Rozwiązanie odwraca intuicję: mapa awaryjna jest liczona na pełne obciążenie, nie na bieg jałowy.** Bogata w całym zakresie obrotów.

| Warunek pracy | Skutek mapy bogatej |
|---|---|
| Bieg jałowy i małe otwarcie | Przelewanie, nierówna praca, możliwe zalanie świecy. Kierowca podtrzymuje gazem |
| Duże otwarcie, realne obciążenie | **Bezpiecznie** — chłodniej, bez detonacji, bez zatarcia |

Kosztem jest kiepska jazda, zyskiem silnik, który dojedzie o własnych siłach. Razem z limitem 3500 obr/min daje to strategię wyjścia z terenu, a nie strategię jazdy.

**Zależność od wariantu — istotna:**

| Wariant | Skutek utraty TPS | Reakcja |
|---|---|---|
| **[A] MVP-A, Beta 300RR, gaźnik** | **Nie dotyczy — motocykl nie ma TPS** (założenie Z1 obalone 11.10.2026). Mapa zapłonu jest jednowymiarowa z definicji (ECU-IGN-020) | Zejście na mapę zapłonu jednowymiarową, liczoną z samych obrotów — dokładnie to, co robiły zapłony CDI. Limit 5000 obr/min, bez mapy bogatej |
| **[B/C] TPI, TBI** | Utrata jedynego sygnału obciążenia | Mapa awaryjna na pełne obciążenie + limit 3500 obr/min |

**Pozycja otwarta dla wariantów B/C — niezależny sygnał obciążenia.** Fabryczny system KTM TPI ma **czujnik ciśnienia w skrzyni korbowej**; w modelach 2018–2019 służył jednocześnie za odniesienie ciśnienia otoczenia, i właśnie dlatego od 2020 dołożono osobny czujnik barometryczny — sygnał ze skrzyni okazał się niewiarygodny jako odniesienie przy pewnych obrotach i obciążeniach. Wniosek pośredni, ale mocny: skoro zmienia się z obciążeniem na tyle, że psuł pomiar ciśnienia otoczenia, to **niesie informację o obciążeniu** i mógłby zastąpić TPS.

Świadomie **nie wprowadzany teraz**: kosztowałby ostatni wolny pin złącza — ten sam, o który rozbiła się decyzja A.4 o czujniku ciśnienia paliwa — i dotyczy wariantów, których jeszcze nie projektujemy. Do rozstrzygnięcia przy wariancie TPI/TBI, razem z ponownym bilansem pinów. Zapisane jako luka **L33**.

*Źródła ustalenia o czujniku KTM: Transmoto, „Explainer: The TPI System's New Ambient Air Pressure Sensor"; katalog Slavens Racing, pozycja Crankcase Pressure Sensor dla modeli TPI/TBI. Sprawdzone 2026-09-22.*

#### B.3.3 Wejście w ograniczenie — zjazd w 3 s (decyzja 2026-09-22)

Limit obrotów schodzi z wartości bieżącej do docelowej **liniowo przez 3 s**, zamiast obowiązywać skokowo.

Powód: nagłe odcięcie z 8000 do 3500 obr/min w trakcie pokonywania przeszkody albo na pochyłym trawersie to szarpnięcie, które samo w sobie może doprowadzić do wywrotki. Trzy sekundy wystarczą, żeby kierowca poczuł spadek mocy i zdążył zareagować — dokończyć manewr, zjechać z linii, wyjść z zakrętu.

Przyjęte ryzyko: przez te 3 s silnik pracuje powyżej limitu mimo potwierdzonej usterki. Przy usterkach grupy G2 (ochrona termiczna) trzy sekundy nie zmieniają niczego — element grzeje się w skali dziesiątek sekund. Przy grupie G3 mieszanka jest już wtedy bogata, czyli w kierunku bezpiecznym.

#### B.3.4 Prezentacja usterek kierowcy (decyzja 2026-09-22)

**Luka wykryta przy opracowywaniu B.3:** macierz definiuje 40 kodów usterek, ale do tej pory żadna reguła nie mówiła, **jak** trafiają one na wyświetlacz. Bez tego mapa awaryjna z B.3.2 jest wręcz niebezpieczna — motocykl jeździ tak źle, że kierowca bez wyjaśnienia uzna silnik za zepsuty i będzie go dalej męczył, zamiast dojechać i wyłączyć.

Cztery poziomy prezentacji, przypisane wprost do klas usterek:

| Poziom | Klasa | Co widzi kierowca | Czy da się schować |
|---|---|---|---|
| **P0 — zapis** | K0 | Nic. Wyłącznie wpis do logu | — |
| **P1 — ostrzeżenie** | K1, K2 | Symbol usterki + krótki komunikat. Uszkodzony odczyt zastąpiony kreskami `---`, **nigdy liczbą** | Komunikat po potwierdzeniu przyciskiem; **symbol zostaje** do ustąpienia usterki |
| **P2 — ograniczenie** | K3 | Symbol + **trwały pas z informacją o ograniczeniu mocy i jego przyczyną** | **Nie.** Pas jest widoczny przez cały czas obowiązywania ograniczenia |
| **P3 — awaria** | K4 | Pełnoekranowy komunikat: przyczyna zatrzasku + instrukcja odblokowania | Tylko przez odblokowanie zatrzasku |

**Treść komunikatu poziomu P2 musi zawierać trzy elementy:** co wysiadło, że moc jest ograniczona **celowo**, oraz co robić. Przykład dla DTC-SEN-04 w wariancie z wtryskiem: *czujnik przepustnicy — awaria; moc ograniczona; silnik pracuje na bogato, dojedź do serwisu*. Sam komunikat „awaria czujnika przepustnicy" nie spełnia tego wymagania, bo nie tłumaczy, dlaczego motocykl zachowuje się nienormalnie.

**Pierwszeństwo przy wielu jednoczesnych usterkach:** ekran zajmuje usterka o najwyższej klasie. Pozostałe dostępne z listy pod przyciskiem, z licznikiem aktywnych usterek przy symbolu.

**Zachowanie przy zaniku komunikacji z HMI** (DTC-COM-01): ograniczenia obowiązują dalej — są po stronie ECU. Kierowca traci informację o przyczynie, nie ochronę. Jest to argument za tym, żeby ograniczenie było wyczuwalne także bez wyświetlacza, co limit obrotów z definicji jest.

Realizacja graficzna — punkt J. Reguły pierwszeństwa i trwałości należą do punktu B, bo wynikają z klasyfikacji usterek, nie z wyglądu ekranu.

---

### B.4 Zatrzask i odblokowanie

**Warunki wejścia w zatrzask:** zdarzenia **2, 3, 4, 6 i 7** z listy B.1.1 — potwierdzona wywrotka, reset watchdoga, zapaść napięcia, utrata synchronizacji przy pracującym silniku, wtryskiwacz zablokowany otwarty. Dodatkowo **przerwa w przewodzie kill switcha** (DTC-SAF-01, grupa 4).

Poza zatrzaskiem pozostają: zdarzenie 1 — naciśnięcie kill switcha, bo jest normalnym sposobem gaszenia silnika; zdarzenie 5 — ogranicznik obrotów, który odcina chwilowo. *(Zdarzenie 8 zostało wycofane 2026-09-20 jako niewykrywalne — patrz B.1.1.)*

**Odblokowanie (decyzja 2026-09-20): dwie równoważne drogi.**

| Droga | Warunek | Uwaga |
|---|---|---|
| Kill switch STOP → RUN | Przełączenie w pozycję stop i z powrotem | Pod kciukiem, działa przy uszkodzonym lub odłączonym HMI |
| Potwierdzenie na HMI | Naciśnięcie przycisku potwierdzenia przy wyświetlonym komunikacie o przyczynie | Czytelna informacja o powodzie zatrzasku |

**Warunek wspólny, wymagany dla obu dróg:** wał zatrzymany (brak sygnału obrotów przez zdefiniowany czas, z histerezą). Odblokowanie przy obracającym się wale jest niedopuszczalne.

**Konsekwencja testowa:** wymaganie ECU-SAF-003 weryfikuje się **dwoma wariantami testu** — T-SAF-003a (odblokowanie kill switchem) i T-SAF-003b (odblokowanie z HMI). To dwie różne ścieżki w kodzie i obie muszą przechodzić przez ten sam warunek zatrzymania wału.

**Zachowanie licznika resetów — doprecyzowane 2026-09-22:** licznik i migawka stanu w pamięci nieulotnej W25Q64, mechanizm dwustopniowy opisany w B.2.5.3. Licznik zerowany po 60 s bezawaryjnej pracy silnika (ECU-SAF-006); po trzecim resecie stan AWARIA trwały, kasowany wyłącznie aplikacją desktop.

*Do doprecyzowania: czas braku sygnału obrotów uznawany za zatrzymanie wału, treść komunikatów.*

---

### B.5 Interlocki live tuningu

*Opracowane 2026-09-22. Domyka ECU-SAF-011 i ryzyko R1.*

**Zasada nadrzędna: ECU weryfikuje każdą zmianę ponownie po odebraniu.** Aplikacja desktop odrzuca wartości niedozwolone przed wysłaniem, ale aplikacja może mieć błąd, a protokół jest otwarty na tyle, że ktoś napisze własne narzędzie. Ta sama zasada obowiązuje już przy histerezie ogranicznika (ECU-IGN-006a).

#### B.5.1 Zakres dozwolonych zmian przy pracującym silniku

| Dozwolone | Zabronione zawsze przy pracującym silniku |
|---|---|
| Komórki mapy zapłonu | Konfiguracja sprzętowa: typ czujnika obrotów, liczba cylindrów, wariant silnika, obwód koła |
| Komórki mapy wtrysku | Progi bezpieczeństwa: blokada i wyłączenie rozrusznika (stałe w firmware — ECU-SAF-008, ECU-SAF-010) |
| Globalne przesunięcie paliwa | Parametry rozruchu i mapa rozruchowa |
| Globalne przesunięcie zapłonu | Próg i histereza ogranicznika obrotów |
| Progi wentylatora | — |

Kryterium podziału: **czy błędna wartość ujawni się natychmiast, czy dopiero przy następnym zdarzeniu.** Zmiana komórki mapy zapłonu daje skutek od razu i kierowca go usłyszy. Zmiana progu blokady rozrusznika nie zrobi nic, dopóki ktoś nie użyje rozrusznika przy pracującym silniku — i dopiero wtedy urwie bendiks. Parametry drugiego rodzaju zmienia się przy zgaszonym silniku, świadomie.

#### B.5.2 Blokada w obszarze wysokiego obciążenia (decyzja 2026-09-22)

**Zmiany map zablokowane, gdy jednocześnie: obroty > 5000 obr/min oraz otwarcie przepustnicy > 60%** — w wariantach wyposażonych w TPS.

> **POZYCJA OTWARTA (11.10.2026):** MVP-A nie ma czujnika przepustnicy, więc warunku obciążenia nie da się ocenić. Sposób blokady dla tego wariantu wymaga decyzji — warianty i ich koszty opisane w DOC-001 rozdz. 11.3. Do rozstrzygnięcia przed zamknięciem punktu C.

To obszar najwyższego obciążenia cieplnego, w którym zubożenie mieszanki albo przestawienie zapłonu grozi detonacją. Poza nim strojenie pozostaje możliwe — w tym na niskich obrotach i przy częściowym otwarciu, czyli tam, gdzie stroi się najczęściej.

**Warunek jest koniunkcją, nie alternatywą.** Sam próg obrotów blokowałby strojenie na wysokich obrotach przy zamkniętej przepustnicy, gdzie nic nie grozi, a jednocześnie przepuszczał zmiany przy pełnym otwarciu na 4500 obr/min — czyli w warunkach realnie groźnych dla dwusuwu.

Próba zapisu w obszarze zablokowanym: **zmiana odrzucona**, aplikacja dostaje odpowiedź z przyczyną odmowy, zdarzenie zapisane do logu. Bez kolejkowania — zapis odłożony w czasie wykonałby się w momencie, którego strojący już nie kontroluje.

#### B.5.3 Limity szybkości zmiany

| Parametr | Limit pojedynczego zapisu | Odstęp między zapisami tej samej komórki |
|---|---|---|
| Kąt wyprzedzenia zapłonu | **2°** | **500 ms** |
| Dawka paliwa | **5%** | **500 ms** |
| Przesunięcie globalne zapłonu | 2° | 500 ms |
| Przesunięcie globalne paliwa | 5% | 500 ms |

Limity dotyczą **skoku wartości**, nie wartości bezwzględnej. Przestawienie komórki o 10° jest możliwe — pięcioma zapisami w ciągu 2,5 s, z których każdy kierowca lub strojący usłyszy. Chodzi o to, żeby nie dało się przestawić mapy jedną pomyłką w oknie aplikacji.

#### B.5.4 Automatyczne przerwanie sesji strojenia

Sesja live tuningu kończy się natychmiast, a mapy wracają do wartości zapisanych trwale, gdy wystąpi którekolwiek z:

| Zdarzenie | Powód |
|---|---|
| Usterka klasy K3 lub K4 | Silnik przestał pracować w warunkach, w których strojenie ma sens |
| Zanik komunikacji USB | Nie wiadomo, czy strojący widzi, co się dzieje |
| Przekroczenie progu temperatury cieczy | Strojenie na przegrzewającym się silniku to strojenie do stanu przejściowego |
| Przejście w stan inny niż PRACA | Zatrzymanie, rozruch i awaria mają własne strategie |

**Zmiany niezatwierdzone przepadają.** Zapis trwały wymaga osobnego, świadomego polecenia i odbywa się transakcyjnie (APP-COM-006). Sesja strojenia operuje na kopii roboczej w pamięci RAM — przerwanie sesji nie może zostawić w pamięci nieulotnej mapy w stanie pośrednim.

---

### B.6 Quickshifter — USUNIĘTY Z ZAKRESU (29.09.2026)

**Funkcja usunięta z produktu decyzją Pawła 29.09.2026.** Specyfikacja była opracowana w całości (podpunkty B.6.1–B.6.8) i została usunięta wraz z wymaganiami ECU-SEN-012/013/014/015, ECU-IGN-009/010/011, ECU-SAF-015 i HMI-UI-009 oraz kodami DTC-SEN-11/12/13.

**Powody decyzji:**

| Powód | Szczegół |
|---|---|
| Najgorszy stosunek złożoności do wartości | 9 wymagań, 3 kody usterek, 2 komponenty do doboru, 2 piny złącza, sprzężenia z TPS, czujnikiem bębna, przepustnicą i trybem zastępczym |
| Jedyna funkcja wnioskująca o **intencji kierowcy** | Wszystkie pozostałe funkcje ECU reagują na mierzalny stan fizyczny. Stąd trzy kolejne błędy specyfikacji, każdy przechodzący testy pozytywne i zawodzący w normalnej jazdzie: cięcie przy użyciu sprzęgła, wskazanie biegu bez warunku sprzęgła, dwa błędne kryteria wykrycia zwartego czujnika |
| Niska wartość w zastosowaniu docelowym | W technicznym terenie kierowca używa sprzęgła nieustannie — do kontroli trakcji, dozowania mocy, pokonywania przeszkód. Warunek „gaz powyżej 20% i obroty powyżej 3000" spełniałby się rzadziej, niż wyglądało na papierze |
| Najgroźniejszy tryb awarii w ECU | Odcięcie zapłonu w niewłaściwym momencie |

**Konsekwencje:** zwolnione **dwa piny złącza** — luka L33 (niezależny sygnał obciążenia dla wariantów TPI/TBI) dostaje miejsce, jeden pin zostaje w zapasie. Luka L3 (czujnik sprzęgła) wraca do stanu zamkniętego jako niepotrzebna. Wbudowany wzmacniacz operacyjny STM32G474 pozostaje wolny. Decyzja 2.6 z Fazy 2-ECU przestaje obowiązywać.

**Zapis pozostaje w dokumencie zgodnie z zasadą procesu #4** (zmiana zakresu jest świadomą decyzją w rejestrze, nie cichym usunięciem) — tak samo jak przy zawężeniu zakresu logowania (F-027). Pełna treść usuniętej specyfikacji jest dostępna w historii wersji dokumentu (wersje 0.9–1.3).

---

### B.7 Pozostały zakres punktu B

**Zamknięte 2026-09-22:** tryb pracy zastępczej (B.3, luka L4), interlocki live tuningu (B.5, ECU-SAF-011 i ryzyko R1), reakcja na niskie napięcie (DTC-PWR-05 i 06, decyzja L12), zakres skróconego autotestu (ECU-PWR-003a), progi i czas potwierdzenia wywrotki (ECU-SAF-005), prezentacja usterek kierowcy (B.3.4).

**Zmiana zakresu 2026-09-29:** quickshifter i czujnik sprzęgła **usunięte z produktu** (B.6). Pozycja P0 quickshiftera z rozdz. 14.11 przestała istnieć wraz z funkcją — nie wymaga już wymagań.

**Zamknięte 2026-09-29:** **diagram bezpieczeństwa** — dwa arkusze: `diagram-bezpieczenstwa.mermaid` (DOC-008, łańcuch odcięcia z podziałem na ścieżki sprzętowe i programowe) oraz `diagram-zatrzask.mermaid` (DOC-009, cykl zatrzasku, odblokowania i licznika resetów). Jeden arkusz byłby nieczytelny — pierwszy odpowiada na pytanie *co odcina i czy działa bez firmware*, drugi na *jak się z tego wychodzi*.

> ## PUNKT B ZAMKNIĘTY (2026-09-29)
>
> Wszystkie pozycje punktu B są domknięte. Pozycja audytu **F-023 zamknięta** (macierz usterek), pozycja **F-031 częściowo** — diagram bezpieczeństwa gotowy, pozostają funkcjonalny i elektryczny.

**Wartości do wystrojenia w Fazie 8, nieblokujące bramki G0** (mają zapisaną wartość wstępną, metodę i kryterium): próg i czas potwierdzenia wywrotki, próg ROZRUCH → PRACA.

**Decyzje podtrzymane:** brak blokady rozrusznika na biegu (L2) — ostrzeżenie w instrukcji użytkownika zamiast blokady.

---

## C. Strategie sterowania silnikiem

### C.1 Trigger i synchronizacja

*Opracowany 2026-10-11 na podstawie pomiarów wykonanych przez Pawła na Becie 300 RR 2015. Domyka pozycję audytu **F-013**.*

#### C.1.1 Zmierzona geometria koła impulsowego

| Parametr | Wartość | Źródło |
|---|---|---|
| Liczba wypustów na kole magnesowym | **1** | pomiar, potwierdzony pełnym obrotem wału |
| Długość kątowa wypustu | **30° wału** | pomiar tarczą kątową |
| Krawędź natarcia | **30° przed GMP** | pomiar |
| Krawędź spływu | **dokładnie w GMP (0°)** | pomiar |
| Rezystancja pick-upu | **95,7 Ω** | pomiar; mieści się w fabrycznej specyfikacji 100 Ω ±20% |
| Szczelina czujnik–wypust | **0,18 mm** | pomiar |

**Konsekwencja nadrzędna: punkt zapłonu leży wewnątrz wypustu.** Dwusuw tej klasy pali w zakresie od okolic GMP przy rozruchu do ok. 25° przed GMP w pracy, a cały ten zakres mieści się między krawędziami. Krawędź natarcia jest więc punktem odniesienia **tuż przed** iskrą, nie na przeciwnym końcu obrotu.

**Dwusuw nie wymaga rozpoznania fazy.** Silnik pali co obrót, więc jeden wypust na obrót to jedna iskra na obrót. Nie ma dwuznaczności suwu, nie ma czujnika wałka rozrządu i **nie istnieje pojęcie utraty synchronizacji** w sensie, w jakim występuje w silnikach czterosuwowych. Ma to bezpośrednie konsekwencje dla macierzy usterek — patrz C.1.7.

#### C.1.2 Dlaczego ta geometria jest korzystna — rachunek

Dokładność zależy od **odległości kątowej między punktem odniesienia a iskrą**, bo na tym odcinku estymata prędkości zdąży się zestarzeć.

| Obroty | Przyspieszenie | Prognoza od krawędzi natarcia | Prognoza od poprzedniego GMP |
|---|---|---|---|
| 1500 obr/min | 2000 obr/min/s | 0,80° | — |
| 3000 obr/min | 3000 obr/min/s | **0,20°** | 6,80° |
| 6000 obr/min | 3000 obr/min/s | **0,05°** | 1,70° |
| 8000 obr/min | 2000 obr/min/s | **0,03°** | — |
| 10 000 obr/min | 1500 obr/min/s | **0,02°** | — |

Budżet ECU-IGN-002 wynosi 1,0° w 99,9 percentylu. **Powyżej 3000 obr/min zapas jest co najmniej pięciokrotny.**

**Najtrudniejszy jest zakres niskich obrotów, nie wysokich** — odwrotnie niż przy kole wielozębnym. Przy 1500 obr/min estymata starzeje się o 5,3% w ciągu obrotu. Dlatego korekta przyspieszenia (C.1.4) nie jest ulepszeniem, tylko warunkiem spełnienia wymagania w dolnym zakresie.

#### C.1.3 Ciągły model kąta wału

Firmware utrzymuje **ciągły model położenia wału**, a nie wyłącznie reakcję na zbocza. Model jest korygowany przy każdej ważnej krawędzi natarcia i ekstrapolowany między nimi.

Model jest konieczny z dwóch powodów:

| Powód | Wyjaśnienie |
|---|---|
| **Start ładowania cewki wypada poza wypustem** | Patrz tabela w C.1.5 — powyżej ok. 1000 obr/min ładowanie musi ruszyć zanim wypust się pojawi |
| **Bramkowanie kątowe wejścia** | Bez wiedzy, gdzie jest wał, nie da się stwierdzić, że zbocze przyszło w złym miejscu (C.1.6) |

**Rozdzielenie dokładności — kluczowe dla zrozumienia całości:**

| Zdarzenie | Źródło wyznaczenia | Wymagana dokładność | Skutek błędu |
|---|---|---|---|
| **Start ładowania** | ciągły model kąta | niska | ciepło w driverze — prąd i tak ograniczy VBG08H-E |
| **Iskra** | krawędź natarcia + wyliczona zwłoka | **1,0° (ECU-IGN-002)** | moc, detonacja, uszkodzenie silnika |

Wypust **nie jest oknem ładowania cewki**. Jest punktem odniesienia dla kąta.

#### C.1.4 Estymata prędkości i korekta przyspieszenia

**Baza: interwał między krawędziami wypustu z poprzedniego obrotu.**

Wypust zajmuje te same 30° wału w każdym obrocie, więc czas jego przejścia daje prędkość chwilową **w dokładnie tej fazie wału, w której nastąpi iskra**. W jednocylindrowym dwusuwie prędkość w obrębie obrotu faluje — sprężanie hamuje wał, rozprężanie przyspiesza — więc średnia z pełnego obrotu jest wobec okolic GMP **systematycznie przesunięta**. Pomiar w tej samej fazie znosi ten błąd, bo powtarza się w tych samych warunkach.

**Korekta: przyspieszenie z dwóch kolejnych okresów obrotu.** Estymata z poprzedniego obrotu jest stara o jeden obrót; korekta liniowa redukuje błąd starzenia do drugiego rzędu. To ona ratuje przypadek 1500 obr/min z tabeli C.1.2.

**Odrzucone: średnia z pełnego obrotu jako baza.** Prostsze i niezależne od kalibracji długości wypustu, ale obarczone błędem **systematycznym** od tętnienia prędkości — a błąd systematyczny nie uśrednia się i wchodzi wprost w kąt zapłonu.

#### C.1.5 Ładowanie cewki

| Obroty | Czas obrotu | Ładowanie 3 ms jako kąt | Wyprzedzenie typ. | Start ładowania | W wypuście? |
|---|---|---|---|---|---|
| 400 | 150 ms | 7,2° | 2° | 9,2° przed GMP | tak |
| 600 | 100 ms | 10,8° | 5° | 15,8° przed GMP | tak |
| 1000 | 60 ms | 18,0° | 10° | 28,0° przed GMP | na styk |
| 1500 | 40 ms | 27,0° | 15° | 42,0° przed GMP | nie |
| 3000 | 20 ms | 54,0° | 20° | 74,0° przed GMP | nie |
| 6000 | 10 ms | 108,0° | 20° | 128° przed GMP | nie |
| 10 000 | 6 ms | 180,0° | 12° | 192° przed GMP | nie |

Powyżej ok. 1000 obr/min start ładowania przypada w obszarze między wypustami i jest wyznaczany **wyłącznie z modelu kąta**. Nie wpływa to na dokładność iskry, bo iskra kończy ładowanie przez rejestr porównania HRTIM, aktualizowany po korekcie modelu na krawędzi natarcia.

Sufit sprzętowy czasu ładowania z B.2.3 (rejestr okresu HRTIM) obowiązuje niezmiennie.

#### C.1.6 Bramkowanie kątowe wejścia — odrzucanie fałszywych zboczy (wymaganie Pawła, 2026-10-11)

**Zasada: zbocze, które przyszło w miejscu, w którym wypust nie może wystąpić, jest odrzucane, a nie przetwarzane.**

Instalacja zapłonowa generuje impulsy zdolne udawać krawędź wypustu. Bez bramkowania takie zbocze skorygowałoby model kąta w złym miejscu i przesunęło iskrę w przypadkowy punkt — przy pełnym obciążeniu groźny dla silnika.

| Stan | Zachowanie wejścia |
|---|---|
| Model kąta ważny | Przyjmowane są wyłącznie zbocza w **oknie spodziewanego położenia** krawędzi natarcia. Pozostałe odrzucane bez wpływu na model |
| Zbocze odrzucone | Zliczane; **zapłon przebiega normalnie** na podstawie modelu kąta — nie traci się iskry |
| Brak ważnego zbocza w oknie | Model pracuje dalej przez ograniczony czas; brak kolejnych zboczy prowadzi do DTC-IGN-01 |
| Model nieważny (rozruch, po resecie) | Bramkowanie nieaktywne — nie ma względem czego bramkować. Walidacja opiera się wtedy wyłącznie na długości wypustu |

**Szerokość okna — wartości wstępne, do wystrojenia w Fazie 8:**

| Zakres | Okno wokół spodziewanej pozycji |
|---|---|
| Rozruch, poniżej 2000 obr/min | ±20° |
| Powyżej 2000 obr/min | ±10° |

Przy niskich obrotach prędkość zmienia się szybciej między obrotami, więc okno musi być szersze — zbyt wąskie odrzucałoby ważne zbocza.

**Wsparcie sprzętowe, nie tylko programowe:** filtr cyfrowy wejścia przechwytującego w STM32G474 oraz adaptacyjny próg MAX9926 odsiewają część zakłóceń zanim dotrą do firmware. Bramkowanie kątowe jest warstwą trzecią, obejmującą to, co przeszło przez dwie pierwsze.

#### C.1.7 Wykrywanie nieprawidłowości sygnału — zastępuje dawne DTC-IGN-02 i DTC-IGN-03

**Korekta zapisu, decyzja 2026-10-11.** Dotychczasowe DTC-IGN-02 („wzór zębów niezgodny z oczekiwanym", „analiza wzoru zgubionego zęba") i DTC-IGN-03 („pojedyncze zakłócenie wzoru") opisywały mechanizm właściwy dla koła wielozębnego typu 60-2. **Na kole z jednym wypustem nie ma wzoru zębów ani zgubionego zęba**, więc oba zapisy opisywały detekcję, której nie da się zrealizować.

W zamian trzy kryteria, każde odnoszące się do zmierzonej geometrii:

| Kryterium | Próg wstępny | Co wykrywa |
|---|---|---|
| Długość wypustu niezgodna z kalibracją | odchyłka > **±25%** od 30° | zakłócenie wewnątrz wypustu, luźny czujnik, uszkodzenie koła |
| Zbocze poza oknem kątowym | wg C.1.6 | zakłócenie od instalacji zapłonowej |
| Stosunek kolejnych okresów obrotu | poza zakresem **0,5–2,0** | zgubione lub podwojone zdarzenie |

**Klasyfikacja i reakcja:**

| Kod | Zdarzenie | Klasa | Reakcja |
|---|---|---|---|
| **DTC-IGN-02** | Sygnał obrotów niewiarygodny — kryterium spełnione powtarzalnie | **K4** | Odcięcie + zatrzask |
| **DTC-IGN-03** | Odrzucone zbocze pojedyncze | **K0** | Wyłącznie licznik. Zapłon bez zmian |
| **DTC-IGN-03a** | Podwyższona liczba odrzuceń — **> 5 na 100 obrotów** | **K1** | Ostrzeżenie o jakości sygnału; wskazuje na zakłócenia lub luźny czujnik |

Licznik odrzuceń jest wskaźnikiem jakości instalacji o dużej wartości diagnostycznej przy uruchamianiu i warto go udostępnić w aplikacji desktop.

#### C.1.8 Sekwencja rozruchu

**Iskra od drugiego przejścia wypustu.** Pierwsze przejście służy wyłącznie do pomiaru: krawędź natarcia startuje pomiar, krawędź spływu go kończy, z czego powstaje pierwsza estymata prędkości i model kąta.

Uzasadnienie: kickstarter obraca wał kilkakrotnie w jednym ruchu nogi, więc wypust przechodzi pod czujnikiem wielokrotnie w trakcie tego samego kopnięcia. **Strata pierwszego obrotu nie kosztuje kopnięcia.** W zamian cały układ ma jedną ścieżkę w kodzie zamiast dwóch i żadnego przypadku szczególnego.

**Rozważone i odrzucone: iskra na pierwszym przejściu**, z ładowaniem na krawędzi natarcia i iskrą na krawędzi spływu, czyli w GMP przy zerowym wyprzedzeniu. Działało bez znajomości prędkości, ale wprowadzało drugą, zupełnie inną ścieżkę wyzwalania, używaną wyłącznie przez jeden obrót w całym cyklu życia uruchomienia.

**Przypadek szczególny do obsłużenia:** restart w ruchu, gdy silnik zgasł na biegu, a motocykl jedzie. Model kąta i estymata prędkości są wtedy **nadal ważne**, więc iskra musi pójść natychmiast z mapy, bez przechodzenia przez sekwencję rozruchową.

**Ograniczenie znane:** bardzo słabe lub krótkie kopnięcie dające tylko jeden obrót nie wywoła iskry. Wymaga powtórzenia kopnięcia.

#### C.1.9 Dwa limity wyprzedzenia

Rozróżnienie istotne dla bezpieczeństwa silnika — jeden limit nie zastępuje drugiego.

| Limit | Wartość | Charakter | Gdzie egzekwowany |
|---|---|---|---|
| **Geometryczny** | **28° przed GMP** | stały, niekonfigurowalny | firmware odrzuca każdą wyższą wartość z mapy i zgłasza zdarzenie |
| **Termodynamiczny** | niższy, zależny od punktu pracy | wynik strojenia | mapa, ustalany w Fazie 8 z obserwacją detonacji |

**Skąd 28°:** iskra musi wypaść **po** krawędzi natarcia (30° przed GMP), żeby można ją było odnieść do świeżego punktu. Dwa stopnie marginesu zapewniają, że zwłoka jest zawsze dodatnia, więc tolerancja mechaniczna wypustu i opóźnienie detekcji nie przesuną iskry przed krawędź — czyli w obszar, którego algorytm nie obsługuje.

**Limit geometryczny nie chroni silnika.** Chroni przed błędem mapy zadającym absurdalną wartość. Detonacja przy dużym obciążeniu może wystąpić znacznie poniżej 28°, i przed nią chroni wyłącznie limit termodynamiczny w mapie.

**Potwierdzenie, że 28° wystarcza:** fabryczne CDI pracuje na tym samym kole, więc jego mapa również musi mieścić się w tej geometrii.

#### C.1.10 Wymagania kalibracyjne — do punktu G

| Parametr | Pochodzenie | Uwaga |
|---|---|---|
| Długość kątowa wypustu | pomiar, domyślnie 30° | Baza estymaty prędkości — błąd przechodzi wprost do kąta |
| Położenie krawędzi natarcia względem GMP | pomiar, domyślnie 30° | Offset całej mapy |
| Opóźnienie detekcji w torze VR | pomiar na stanowisku | Stała czasowa MAX9926 i filtra wejściowego; wchodzi jako offset |
| Szerokość okna bramkowania | Faza 8 | Wartości wstępne w C.1.6 |
| Próg odchyłki długości wypustu | Faza 8 | Wartość wstępna ±25% |

**Kalibracja musi być przechowywana jako dane, nie jako stałe w kodzie** — platforma ma obsługiwać różne silniki, a każdy ma inną geometrię koła.

#### C.1.11 Pozycja otwarta — amplituda sygnału VR

Szczelina 0,18 mm jest wyraźnie mniejsza niż typowe 0,3–1,0 mm, co daje mocny sygnał przy rozruchu, ale **przy 10 000 obr/min amplituda może przekroczyć 100 V**, czyli górną granicę przyjętą w ECU-SEN-001.

Do zweryfikowania oscyloskopem na pracującym silniku i do uwzględnienia przy projektowaniu obwodu wejściowego MAX9926 w Fazie 4 — rezystor szeregowy ograniczający prąd wejściowy i klamra. Nie blokuje C.1, bo nie zmienia algorytmu.

---
### C.2 Pozostały zakres punktu C

*Do opracowania.* Mapa rozruchowa, wzbogacenie przy rozgrzewaniu, mapy zapłonu i wtrysku, korekty (temperatura powietrza i cieczy, ciśnienie atmosferyczne, napięcie akumulatora), odcięcie paliwa przy zamkniętej przepustnicy, ogranicznik obrotów, mapa awaryjna przy utracie TPS (B.3.2).

**Wymaganie z analizy termicznej (rozdz. 6.8 dok. procesu):** czas ładowania cewki musi być skracany przy wysokich obrotach — ładowanie tylko do osiągnięcia prądu nasycenia, nie stałe 3 ms. Przy 8000 obr/min i stałym dwell wypełnienie sięga 40%, co daje 4,8 z 5,5 W wszystkich strat cieplnych ECU.

---

## D. Struktura danych i map

*Do opracowania*

Zakres: wymiarowość map, interpolacja, parametry konfiguracyjne, profile per model motocykla (L10), organizacja pamięci flash z uwzględnieniem zużycia komórek.

---

## E. Diagnostyka

*Do opracowania*

Zakres: lista błędów i kodów, klasyfikacja krytyczne/niekrytyczne (potrzebna dla decyzji A.5), przechowywanie z znacznikami czasu RTC, sygnalizacja na HMI i w aplikacji desktop. Monitorowanie heartbeat HMI (decyzja L22).

---

## F. Czarna skrzynka

*Do opracowania*

Zakres: progi wyzwolenia z IMU, zakres danych, okno czasowe przed/po zdarzeniu, zapewnienie dokończenia zapisu.

---

## G. Kalibracja

*Do opracowania*

Zakres: czujnik biegu (pozycje, z uwzględnieniem układu 1-N-2-3-4-5-6 i filtra czasowego), koło impulsowe (długość wypustu, położenie krawędzi natarcia względem GMP, opóźnienie detekcji w torze VR), a w wariantach z TPS także TPS (min/max).

---

## H. Bootloader i aktualizacja

*Do opracowania*

**Ustalone (zasada #10 procesu):** dwubankowy, automatyczny powrót do poprzedniej wersji przy nieudanej aktualizacji. STM32G474 i STM32G0B1 mają sprzętowe wsparcie dwubankowej pamięci Flash.

Zakres do rozpisania: procedura aktualizacji ECU i HMI (HMI przez ECU jako gateway), weryfikacja integralności, kontrola zgodności wersji (zasada #7).

---

## I. Architektura zadań czasu rzeczywistego

*Do opracowania*

Zakres: priorytety przerwań, budżet czasowy, obsługa watchdoga okienkowego, rozdział rdzeń real-time / zadania tła.

---

## J. Firmware HMI

*Do opracowania*

**Ustalone:**
- Przy utracie komunikacji z ECU — komunikat o błędzie i **wygaszenie danych** (decyzja L11). Żadna wartość nie jest wyświetlana, żeby nie wprowadzać w błąd zamrożonym odczytem
- Po resecie MCU wymagana poprawna **reinicjalizacja koprocesora EVE4** (decyzja L22)
- **Timeout wyświetlacza 3 min** bez interakcji (decyzja A.2)
- **Uśpienie na polecenie ECU po CAN** (rozdz. 7.1 dok. procesu). ECU dyryguje; HMI ma **własny timeout awaryjny** na wypadek zaginięcia polecenia
- **Wybudzanie przyciskiem:** linia drabinki rezystorowej podpięta równolegle do wejścia EXTI obok wejścia ADC — naciśnięcie dowolnego przycisku daje zbocze wybudzające. Dopiero po wybudzeniu ADC określa, który przycisk. Konieczne, bo **ADC nie działa w trybie Stop**
- **Zarządzanie jasnością wg temperatury** (decyzja H.13, analiza w rozdz. 7.2): panel LCD czernieje powyżej ~70°C, a na słońcu potrzeba maksymalnej jasności — firmware musi wyważyć czytelność i ochronę wyświetlacza. Progi i charakterystyka do ustalenia
- Przy zasypianiu: odłączenie wyświetlacza i EVE4, flash SPI w deep power-down, TJA1043 w Standby

Zakres do rozpisania: maszyna stanów HMI, struktura menu, format konfiguracji wyglądu z aplikacji desktop, obsługa heartbeat z ECU.
