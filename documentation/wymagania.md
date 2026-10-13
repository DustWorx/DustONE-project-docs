# Specyfikacja wymagań — ECU + HMI + Aplikacja desktop

| | |
|---|---|
| **Identyfikator** | DOC-002 |
| **Wersja** | **1.5** |
| **Status** | roboczy — pozycje `[DO USTALENIA]` blokują bramkę G0 |
| **Właściciel** | Paweł |
| **Opracowanie** | Claude |
| **Data wersji** | 2026-09-20 |
| **Dokument nadrzędny** | `proces-rozwoju-ecu.md` (DOC-001) |

**Historia zmian**

| Wersja | Data | Zakres zmiany |
|---|---|---|
| 0.1 | 2026-09-12 | Utworzenie dokumentu: schemat identyfikatorów, ok. 60 wymagań, odpowiedź na pozycje audytu F-011 i F-027 |
| 0.2 | 2026-09-20 | Ustalenie 14 wartości liczbowych (dokładność zapłonu, histereza ogranicznika, filtr pozycji neutralnej, czas gotowości, progi rozrusznika, licznik resetów, parametry CAN i HMI); dopisanie ECU-IGN-006a, ECU-PWR-003a, ECU-SAF-010a, SYS-COM-001a/002a/002b, HMI-UI-002a |
| 0.3 | 2026-09-20 | Domknięcie ECU-IGN-005 (sufit czasu ładowania w rejestrze okresu HRTIM) i ECU-SEN-007 (progi < 3% i > 97% zakresu) na podstawie punktu B specyfikacji FW |
| 0.4 | 2026-09-20 | Dopisane ECU-PWR-009 (reakcja na przepięcie), ECU-PWR-010 (kontrola przełącznika obciążenia), SYS-COM-005a (zachowanie HMI przy niezgodności wersji), SYS-COM-005b (wspólny pakiet aktualizacyjny) — wynik macierzy usterek grupa 3 |
| 0.5 | 2026-09-22 | Domknięte ECU-PWR-003a (zakres autotestu skróconego), ECU-SAF-005 (65°/3 s), ECU-SAF-002 (układ trzypoziomowy); dopisane ECU-SAF-002a, ECU-SAF-006a (migawka stanu), ECU-SAF-006b (punkty kontrolne), ECU-SAF-012 i 012a (rozdzielenie map sterowania od konfiguracji użytkownika) — wynik macierzy usterek grupa 4 |
| 0.6 | 2026-09-22 | Domknięte ECU-SAF-011 (interlocki live tuningu). Dopisane ECU-INJ-007 i ECU-IGN-008 (mapy awaryjne przy utracie TPS, rozdzielone na warianty), ECU-PWR-008a (rozdzielenie progów szyny 5 V), ECU-SAF-011a (przerwanie sesji strojenia), ECU-SAF-013 (zjazd limitu w 3 s), ECU-SAF-014 (łączenie ograniczeń), HMI-UI-006/007/008 (prezentacja usterek kierowcy) — wynik punktów B.3 i B.5 |
| 0.7 | 2026-09-29 | **Wymagania quickshiftera — zamknięcie pozycji P0 z rozdz. 14.11:** ECU-SEN-012 (czujnik prętowy, progi), ECU-SEN-013 (usterka czujnika), ECU-IGN-009 (warunki dopuszczenia), ECU-IGN-010 (czas odcięcia od obrotów), ECU-IGN-011 (sufit sprzętowy 150 ms), ECU-SAF-015 (zablokowana dźwignia) — wynik punktu B.6 |
| **0.8** | **2026-09-29** | Dopisane ECU-SEN-014 (wejście czujnika sprzęgła, blokada cięcia), ECU-SEN-015 (kontrola wiarygodności stanu sprzęgła), HMI-UI-009 (wskazanie włączonego biegu przy zgaszonym silniku, bez zapisu do logu), SYS-COM-007 (wybudzenie ECU pociąga wybudzenie HMI) — wynik punktu B.6.8 |
| **0.9** | **2026-09-29** | Korekta HMI-UI-009: dodany trzeci warunek **sprzęgło nie wciśnięte**; źródłem jest czujnik bębna **i** czujnik sprzęgła |
| **1.0** | **2026-09-29** | Poprawione ECU-SEN-015: kryterium wykrycia zwartego czujnika sprzęgła oparte na zmianach biegu, nie na czasie. Kryterium czasowe dawało fałszywy alarm przy zjeździe na wciśniętym sprzęgle |
| 1.1 | 2026-09-29 | ECU-SEN-015 wróciło do stanu `[DO USTALENIA]` — drugie kryterium też odrzucone (redukcje biegu podczas zjazdu bez puszczania sprzęgła). Oba odrzucone kryteria zapisane wraz z powodami |
| 1.2 | 2026-09-29 | **Formalna zmiana zakresu — quickshifter i czujnik sprzęgła usunięte z produktu** (decyzja Pawła). Usuniętych 9 wymagań: ECU-SEN-012/013/014/015, ECU-IGN-009/010/011, ECU-SAF-015, HMI-UI-009. Powody i konsekwencje zapisane w rozdz. 8 |
| 1.3 | 2026-09-29 | Dopisane ECU-SAF-016 (rezystory ściągające na linii bramkującej EN) i ECU-SAF-016a (zasilanie komparatora za przełącznikiem obciążenia). Luka wykryta przy pytaniu Pawła o monitoring szyny 5 V: linia bramkująca nie była objęta ECU-SAF-007 |
| 1.4 | 2026-10-11 | **Wymagania triggera i synchronizacji** na podstawie pomiarów koła impulsowego: ECU-IGN-012 (geometria jako kalibracja), 013 (model kąta), 014 (estymata prędkości), 015 (limit geometryczny 28°), 016 (limit termodynamiczny w mapie), 017 (bramkowanie kątowe), 018 (wiarygodność sygnału), 019 (iskra od drugiego przejścia). Wynik punktu C.1 — domyka F-013 |
| **1.5** | **2026-10-11** | **Skutki obalenia założenia Z1 — Beta 300 RR nie ma TPS.** Usunięte ECU-IGN-008 [A]; dodane **ECU-IGN-020** (mapa zapłonu MVP-A jednowymiarowa); ECU-SEN-003 przeniesione do [HW]; skorygowane SYS-COM-002a i ECU-SAF-011 (sposób blokady live tuningu w MVP-A otwarty) |

---

## 1. Zasady zapisu

Każde wymaganie zawiera: **identyfikator**, treść ze słowem „musi", **wartość liczbową z tolerancją**, **warunki pracy** oraz **metodę weryfikacji**.

**Schemat identyfikatora:** `[URZĄDZENIE]-[OBSZAR]-[NUMER]`

| Urządzenie | | Obszar | |
|---|---|---|---|
| ECU | jednostka sterująca | IGN | zapłon |
| HMI | wyświetlacz | INJ | wtrysk |
| APP | aplikacja desktop | SEN | czujniki |
| SYS | wymaganie systemowe | PWR | zasilanie |
| | | SAF | bezpieczeństwo |
| | | DIA | diagnostyka |
| | | COM | komunikacja |
| | | ENV | warunki środowiskowe |
| | | LOG | logowanie |
| | | UI | interfejs użytkownika |

**Metody weryfikacji:** A = analiza/obliczenie, I = inspekcja/przegląd, T = test, D = demonstracja.

**Oznaczenia statusu wartości:**
- Wartość liczbowa — ustalona
- `[DO USTALENIA]` — wymaga decyzji projektowej lub pomiaru; **każda taka pozycja blokuje bramkę G0**

**Warianty (za kartą MVP, plan naprawczy rozdz. 8):** wymagania oznaczone **[A]** dotyczą MVP-A (Beta 300RR, gaźnik). **[HW]** oznacza wymagania zdolności sprzętowej weryfikowane na stanowisku. **[B/C]** dotyczą wariantów TPI/TBI.

---

## 2. Warunki pracy (obowiązują dla wszystkich wymagań, o ile nie wskazano inaczej)

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| SYS-ENV-001 | Zakres napięcia zasilania, przy którym ECU musi pracować w pełnym zakresie funkcji | 9,0–16,0 V | T |
| SYS-ENV-002 | Zakres napięcia, przy którym ECU musi zachować sterowanie silnikiem (dopuszczalna ograniczona funkcjonalność) | 7,0–18,0 V | T |
| SYS-ENV-003 | Zakres temperatury otoczenia pracy ECU | -20…+60 °C | T |
| SYS-ENV-004 | Zakres temperatury przechowywania | -30…+85 °C | A |
| SYS-ENV-005 | Klasa szczelności obudowy ECU i HMI | IP67 minimum | T |
| SYS-ENV-006 | Odporność na wibracje | `[DO USTALENIA]` — profil do przyjęcia z normy lub pomiaru na motocyklu | A, T |
| SYS-ENV-007 | Zakres obrotów silnika, w którym ECU musi sterować zapłonem | 200–10 000 obr/min | T |

---

## 3. Zapłon

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| ECU-IGN-001 **[A]** | ECU musi wyznaczać moment zapłonu na podstawie mapy kąta wyprzedzenia w funkcji obrotów | — | I, T |
| ECU-IGN-002 **[A]** | Błąd momentu wyzwolenia zapłonu względem wartości zadanej, mierzony na wyjściu drivera, przy jednoczesnej pracy logowania, CAN i USB | ≤ **1,0°** kąta wału w 99,9 percentylu, w zakresie 1 000–10 000 obr/min i 7,0–16,0 V | T |
| ECU-IGN-003 **[A]** | Czas ładowania cewki musi być korygowany w funkcji napięcia zasilania | Zakres korekty `[DO USTALENIA]` | T |
| ECU-IGN-004 **[A]** | Czas ładowania cewki musi być ograniczany przy wysokich obrotach (ochrona termiczna drivera) | Maksymalne wypełnienie `[DO USTALENIA]` % | A, T |
| ECU-IGN-005 **[A]** | Niezależny od firmware limit czasu ładowania cewki | **Rejestr okresu HRTIM jako sufit sprzętowy** — wyjście kasowane zdarzeniem porównania **oraz** zdarzeniem końca okresu (zweryfikowane w CubeMX 20.09.2026, spec. FW B.2.3). Wartość sufitu do ustalenia przy doborze cewki w Fazie 4; ograniczenie prądu 8,5–10,5 A i miękkie wyłączenie 150–175 °C w VBG08H-E jako warstwa dodatkowa | A, T |
| ECU-IGN-006 **[A]** | Ogranicznik obrotów musi odcinać zapłon powyżej progu konfigurowalnego przez użytkownika | Zakres nastawy 3 000–12 000 obr/min | T |
| ECU-IGN-006a **[A]** | Histereza ogranicznika musi być **konfigurowalna z aplikacji desktop** | Domyślnie **200 obr/min**, zakres dopuszczalny **50–500 obr/min**. Aplikacja odrzuca wartości spoza zakresu przed wysłaniem; ECU weryfikuje ponownie po odebraniu | T |
| **ECU-IGN-012** | Parametry geometrii koła impulsowego muszą być **danymi kalibracyjnymi**, nie stałymi w kodzie | Beta 300 RR 2015 (pomiar 11.10.2026): **1 wypust, długość 30° wału, krawędź natarcia 30° przed GMP, krawędź spływu w GMP**. Platforma ma obsługiwać różne silniki, każdy o innej geometrii | I, T |
| **ECU-IGN-013** | ECU musi utrzymywać **ciągły model położenia wału**, korygowany przy każdej ważnej krawędzi natarcia i ekstrapolowany między nimi | Konieczny, bo powyżej ok. 1000 obr/min start ładowania cewki wypada poza wypustem, a bramkowanie kątowe wymaga wiedzy o położeniu wału | I, T |
| **ECU-IGN-014** | Estymata prędkości do wyznaczenia zwłoki iskry musi pochodzić z **interwału między krawędziami wypustu z poprzedniego obrotu**, z korektą przyspieszenia z dwóch kolejnych okresów | Interwał wypustu mierzy prędkość chwilową w tej samej fazie wału, w której nastąpi iskra, więc tętnienie prędkości w obrębie obrotu znosi się systematycznie. Średnia z pełnego obrotu daje błąd **systematyczny**, który się nie uśrednia | A, T |
| **ECU-IGN-015** | Wyprzedzenie zapłonu musi być ograniczone **twardym limitem geometrycznym**, niekonfigurowalnym, odrzucającym każdą wyższą wartość z mapy wraz z zapisem zdarzenia | **28° przed GMP.** Iskra musi wypaść po krawędzi natarcia (30°), żeby odnosić ją do świeżego punktu; 2° marginesu zapewniają dodatnią zwłokę mimo tolerancji mechanicznej i opóźnienia detekcji | I, T |
| **ECU-IGN-016** | Mapa musi zawierać **limit wyprzedzenia zależny od punktu pracy**, niższy niż geometryczny | Limit geometryczny chroni przed błędem mapy, **nie przed detonacją** — ta może wystąpić znacznie poniżej 28°. Wartości ustalane w Fazie 8 z obserwacją detonacji | T |
| **ECU-IGN-017** | ECU musi **odrzucać zbocza przychodzące poza oknem kątowym** spodziewanego położenia krawędzi natarcia, bez wpływu na model kąta i bez utraty iskry | Okno wstępnie **±20° poniżej 2000 obr/min, ±10° powyżej** — do wystrojenia w Fazie 8. Zapłon przebiega normalnie z modelu kąta. Bramkowanie nieaktywne przy nieważnym modelu (rozruch, po resecie) | T (wstrzykiwanie zakłóceń) |
| **ECU-IGN-018** | ECU musi wykrywać **niewiarygodny sygnał obrotów** według trzech kryteriów | Długość wypustu poza **±25%** kalibracji; zbocze poza oknem kątowym; stosunek kolejnych okresów poza **0,5–2,0**. Progi wstępne, do wystrojenia w Fazie 8. Pojedyncze naruszenie = odrzucenie zbocza (K0); powtarzalne = K4 | T |
| **ECU-IGN-019** | Pierwsza iskra po rozruchu może nastąpić **najwcześniej przy drugim przejściu wypustu** | Pierwsze przejście służy wyłącznie pomiarowi. Kickstarter obraca wał kilkakrotnie w jednym ruchu, więc strata pierwszego obrotu nie kosztuje kopnięcia. **Wyjątek:** przy restarcie w ruchu model kąta i estymata pozostają ważne — iskra musi pójść natychmiast z mapy | T |
| **ECU-IGN-020** **[A]** | Mapa zapłonu w wariancie gaźnikowym musi być **jednowymiarowa** — kąt wyprzedzenia wyłącznie w funkcji obrotów | **Beta 300 RR 2015 nie ma czujnika położenia przepustnicy i nie będzie dokładany** (założenie Z1 obalone 11.10.2026). Fabryczny układ zapłonowy pracuje tak samo. Wymaganie ECU-IGN-001 od początku mówiło o mapie w funkcji obrotów; dwuwymiarowość weszła bokiem przez wymagania opisujące utratę sygnału, którego w tym wariancie nie ma | I, T |
| ECU-IGN-007 **[A]** | Rozdzielczość zapisu kąta wyprzedzenia w mapie | `[DO USTALENIA]`° | I |

---

## 4. Wtrysk

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| ECU-INJ-001 **[HW]** | ECU musi sterować dwoma niezależnymi kanałami wtryskiwaczy | 2 kanały, prąd ciągły ≥ 1,5 A/kanał | T |
| ECU-INJ-002 **[HW]** | Sterowanie w trybie nasyconym dla wtryskiwaczy o rezystancji | 10,5–13,0 Ω | T |
| ECU-INJ-003 **[HW]** | Rozdzielczość czasu otwarcia wtryskiwacza | ≤ `[DO USTALENIA]` µs | T |
| ECU-INJ-004 **[HW]** | Czas martwy wtryskiwacza musi być korygowany w funkcji napięcia zasilania | Na podstawie pomiaru — `[DO USTALENIA]` | T |
| **ECU-INJ-007** **[B/C]** | Przy utracie sygnału przepustnicy ECU musi przejść na **mapę awaryjną liczoną na pełne obciążenie** (bogatą w całym zakresie obrotów), nie na dawkę z biegu jałowego | Uzasadnienie: dawka z biegu jałowego przy otwartej przepustnicy oznacza skrajnie ubogą mieszankę pod obciążeniem, czyli zatarcie. Mapa bogata daje kiepską pracę na biegu jałowym i bezpieczną pod obciążeniem. Limit obrotów **3500 obr/min** | T |
| ECU-INJ-005 **[B/C]** | Pompa paliwa musi być załączana na czas wstępnego napełnienia po wybudzeniu | 2,0 s ± 0,2 s | T |
| ECU-INJ-006 **[B/C]** | Pompa paliwa musi być wyłączana przy braku obrotów przez określony czas | `[DO USTALENIA]` s | T |

---

## 5. Czujniki

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| ECU-SEN-001 | ECU musi obsługiwać czujnik obrotów typu VR (cewka indukcyjna) | Amplituda wejściowa 0,05–100 V szczytowo | T |
| ECU-SEN-002 | ECU musi obsługiwać czujnik obrotów typu Hall, ścieżką wybieraną zworką | Poziomy logiczne `[DO USTALENIA]` | T |
| ECU-SEN-003 **[HW]** | Błąd pomiaru położenia przepustnicy (TPS) po kalibracji — **zdolność sprzętowa dla wariantów B/C; MVP-A nie ma TPS** | ≤ `[DO USTALENIA]` % zakresu | T |
| ECU-SEN-004 | Błąd pomiaru temperatury cieczy chłodzącej | ≤ ±3 °C w zakresie 0…120 °C | T |
| ECU-SEN-005 | Błąd pomiaru temperatury powietrza dolotowego | ≤ ±3 °C w zakresie -20…+80 °C | T |
| ECU-SEN-006 | Błąd pomiaru napięcia akumulatora | ≤ ±0,2 V w zakresie 7,0–16,0 V | T |
| ECU-SEN-007 | ECU musi wykrywać przerwę i zwarcie każdego wejścia czujnikowego | Progi **< 3% i > 97% zakresu przetwornika**, liczone względem rzeczywistego napięcia szyny 5 V. Czasy potwierdzenia wg macierzy usterek (spec. FW B.2.1) | T |
| ECU-SEN-008 | Rozpoznanie pozycji biegu po kalibracji | 100% poprawnych rozpoznań przy 200 zmianach biegu | T |
| ECU-SEN-009 | Chwilowe przejście przez pozycję neutralną podczas zmiany 1↔2 nie może być zgłoszone jako bieg neutralny | **Filtr wybiórczy:** wskazanie biegu zgłaszane natychmiast; wskazanie pozycji neutralnej dopiero po **80 ms** stabilnego odczytu. Uzasadnienie: zmiana biegu trwa 30–60 ms, człowiek zauważa zwłokę powyżej ~150 ms | T |
| ECU-SEN-010 | Błąd pomiaru prędkości koła | ≤ `[DO USTALENIA]` % | T |
| ECU-SEN-011 | Pomiary ratiometryczne muszą być kompensowane rzeczywistym napięciem szyny 5 V | — | I, T |

---

## 6. Zasilanie i tryb uśpienia

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| ECU-PWR-001 | Pobór prądu ECU w trybie uśpienia | ≤ 150 µA przy 12,0 V i +25 °C | T |
| SYS-PWR-002 | Łączny pobór ECU i HMI w trybie uśpienia | ≤ 250 µA przy 12,0 V i +25 °C | T |
| ECU-PWR-003 | Czas od zdarzenia wybudzenia do gotowości do generowania iskry | ≤ **200 ms**. Uzasadnienie: kierowca zawsze najpierw budzi ECU, potem kopie lub trzyma przycisk startu — zmiana czynności trwa dłużej | T |
| ECU-PWR-003a | Zakres autotestu przy starcie musi być zróżnicowany: **pełny** (suma kontrolna firmware, map sterowania i konfiguracji, test RAM) po podłączeniu akumulatora i po aktualizacji firmware; **skrócony** przy zwykłym wybudzeniu z uśpienia | **Autotest skrócony: suma kontrolna map sterowania + odczyt identyfikatora pamięci W25Q64.** Pominięte suma kontrolna firmware i test RAM — nie zmieniają się między uśpieniem a wybudzeniem, mapy mogły zostać nadpisane przez aplikację desktop. Mieści się w budżecie 200 ms (ECU-PWR-003) | I, T |
| ECU-PWR-004 | ECU musi przejść w uśpienie po braku pracy silnika i interakcji użytkownika | 30 min ± 1 min | T |
| HMI-PWR-005 | Podświetlenie wyświetlacza musi zostać wygaszone po braku interakcji | 3 min ± 10 s | T |
| ECU-PWR-006 | Nastawy szyn zasilania muszą być stałe; firmware nie może ich zmieniać | — | I |
| ECU-PWR-007 | ECU musi monitorować obie szyny zasilania i sygnały Power Good | — | I, T |
| ECU-PWR-008 | Napięcie szyny 5 V zasilającej czujniki | 5,00 V ±2% w pełnym zakresie obciążenia i temperatury | A, T |
| **ECU-PWR-008a** | Reakcja na odchylenie szyny 5 V musi być **rozdzielona według tego, czy MAX9926 dalej pracuje** | **4,50–4,75 V lub 5,25–5,50 V** — odczyty niewiarygodne, tryb zastępczy grupy G3. **Poniżej 4,50 V, powyżej 5,50 V lub brak Power Good** — MAX9926 przestaje pracować, sygnał obrotów zanika, silnik gaśnie; w logu przyczyna źródłowa „zasilanie". Zakres pracy MAX9926 wg karty katalogowej | T |
| **ECU-PWR-009** | Przy przepięciu ECU musi ostrzec kierowcę i **załączyć wentylator jako obciążenie obniżające napięcie** | Próg załączenia **> 16,5 V przez 200 ms**, wyłączenie po spadku **poniżej 15,5 V**. Uzasadnienie: regulator w motocyklu jest typu bocznikującego, więc dołożenie obciążenia realnie obniża napięcie. Światła celowo pominięte — pozostają pod kontrolą kierowcy | T |
| **ECU-PWR-010** | ECU musi wykryć niezaładowanie przełącznika obciążenia szyny 5 V i zablokować wyjście ze stanu gotowości | Brak napięcia na szynie czujników **po 5 ms** od załączenia, 3 próby | T |

---

## 7. Bezpieczeństwo

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| ECU-SAF-001 | Rozwarcie kill switcha musi odciąć zapłon i wtrysk **niezależnie od stanu firmware** (bramkowanie sprzętowe) | Czas reakcji ≤ `[DO USTALENIA]` ms | T (wstrzykiwanie usterek) |
| ECU-SAF-002 | Przerwanie przewodu kill switcha lub rozłączenie wtyczki musi skutkować odcięciem **i zostać odróżnione od naciśnięcia przycisku** w logu oraz w komunikacie dla kierowcy | **Układ trzypoziomowy:** rezystor szeregowy i równoległy w wiązce przy przycisku, podciągnięcie w ECU. RUN = poziom dolny, STOP = środkowy, przerwa = górny. Bramkowanie sprzętowe jednym komparatorem z progiem między RUN a STOP — odcina w obu przypadkach niezależnie od firmware. Rozróżnienie przez ADC, wyłącznie na potrzeby diagnostyki. Wartości rezystorów i analiza najgorszego przypadku — Faza 4 | T (wstrzykiwanie usterek) |
| **ECU-SAF-002a** | Czas potwierdzenia stanu kill switcha przed zgłoszeniem usterki | **50 ms** — filtruje drgania styku, nie opóźnia odcięcia, bo odcięcie jest sprzętowe i natychmiastowe | T |
| ECU-SAF-003 | Po resecie watchdoga wyjścia mocy muszą pozostać wyłączone do zatrzymania wału i świadomego odblokowania przez kierowcę | — | T |
| ECU-SAF-004 | Po zaniku napięcia (brown-out) obowiązuje ten sam zatrzask co po resecie watchdoga | — | T |
| ECU-SAF-005 | Wykrycie wywrotki przez IMU musi odciąć zapłon i uruchomić zatrzask | Kąt przechyłu **> 65°** utrzymany nieprzerwanie **3 s**, wyłącznie w stanie PRACA. Wartości wstępne — do korekty pomiarem w Fazie 8, kryterium: zero fałszywych zadziałań podczas sesji testowej. Świadomie bez warunku prędkości koła: po wywrotce koło często kręci się dalej i warunek zablokowałby wykrycie | T |
| ECU-SAF-006 | **3 resety watchdoga** muszą przenieść ECU w stan awarii bez możliwości automatycznego startu. Licznik zerowany dopiero **po 60 s ciągłej, bezawaryjnej pracy silnika** (nie po samym upływie czasu) | 3 resety; zerowanie po 60 s udanej pracy. Uzasadnienie: dowodem sprawności jest działanie, nie upłynięcie czasu — przy zerowaniu czasowym awaria występująca co 70 s nigdy nie zostałaby wykryta. Licznik przechowywany w pamięci nieulotnej W25Q64. Po trzecim resecie stan awarii kasowany wyłącznie aplikacją desktop | T |
| ECU-SAF-007 | Wszystkie wyjścia mocy muszą być wyłączone w stanie resetu i podczas startu mikrokontrolera (rezystory ściągające) | — | I, T |
| **ECU-SAF-016** | Linia bramkująca wejścia EN driverów musi mieć **rezystory ściągające**, tak aby zanik zasilania komparatora, zanik szyny 5 V oraz stan przed startem mikrokontrolera dawały ten sam skutek: **drivery wyłączone** | Rozszerza ECU-SAF-007, które obejmuje wyjścia mocy — **linia bramkująca nie jest wyjściem mocy i nie była nim objęta**. Bez tego zanik zasilania komparatora zostawia na linii decydującej o odcięciu stan nieokreślony | I, T |
| **ECU-SAF-016a** | Komparator kill switcha musi być zasilany z szyny 5 V **za przełącznikiem obciążenia** | Uzasadnienie: w uśpieniu komparator jest wtedy bez napięcia i nie obciąża budżetu prądu spoczynkowego (ECU-PWR-001), a bramkowanie nie jest wówczas potrzebne — drivery trzymają rezystory ściągające z ECU-SAF-016. Zasilenie z szyny 3,3 V lub wprost z 5 V wymagałoby komparatora nanomocowego albo osobnego wyłączania | I |
| ECU-SAF-008 | Rozrusznik nie może zostać załączony, gdy obroty przekraczają próg | **400 obr/min**, wartość **stała w firmware, niedostępna dla użytkownika**. Uzasadnienie: bendiks wchodzący w obracające się koło zamachowe to natychmiastowe uszkodzenie mechaniczne. Próg niższy niż obroty samodzielnej pracy daje margines na wybieg po zgaszeniu | T |
| ECU-SAF-009 | Czas ciągłej pracy rozrusznika | ≤ 5,0 s ± 0,2 s | T |
| ECU-SAF-010 | Rozrusznik musi być wyłączony automatycznie po przekroczeniu progu obrotów samodzielnej pracy | **700 obr/min**, wartość **stała w firmware** | T |
| ECU-SAF-010a | **Warunek spójności:** próg wyłączenia rozrusznika (SAF-010) musi być zawsze wyższy niż próg blokady załączenia (SAF-008) | 700 > 400. Naruszenie tej relacji tworzy stan nierozstrzygalny — ECU jednocześnie wyłączałoby rozrusznik i uznawało, że wolno go załączyć | I |
| **ECU-SAF-006a** | Przy każdym resecie watchdoga i przy brown-oucie ECU musi zapisać **migawkę stanu** do pamięci nieulotnej | Zawartość: przyczyna resetu z rejestru MCU, **ostatni osiągnięty punkt kontrolny**, stan maszyny stanów, obroty, napięcie akumulatora i obu szyn, temperatura MCU, czas od startu, motogodziny, wersja firmware, suma kontrolna map, aktywne kody usterek. Przechowywane **3 ostatnie migawki**. Ślad bieżący prowadzony w rejestrach domeny podtrzymywanej (bez zużycia Flash), przepisywany do W25Q64 raz, po resecie | T |
| **ECU-SAF-006b** | Każde zadanie czasu rzeczywistego musi zapisywać swój identyfikator jako punkt kontrolny przy wejściu | Lista identyfikatorów w punkcie I specyfikacji FW; **zadanie bez identyfikatora jest luką w diagnostyce**. Narzut: jedna instrukcja zapisu na zadanie | I, T |
| **ECU-SAF-012** | Błędna suma kontrolna **map sterowania** wykryta przy starcie musi zablokować uruchomienie silnika | Zakres: mapa zapłonu, mapa wtrysku, korekty, progi wentylatora, próg i histereza ogranicznika, czasy ładowania cewki. Komunikat o uszkodzeniu map z instrukcją ponownego wgrania | T |
| **ECU-SAF-012a** | Błędna suma kontrolna **konfiguracji użytkownika** nie może blokować uruchomienia silnika | Zakres: obwód koła, jednostki, układ i wygląd ekranów HMI, jasność. Reakcja: wartości domyślne + ostrzeżenie. Kryterium podziału względem ECU-SAF-012: czy wartość wpływa na to, co ECU robi z silnikiem | T |
| **ECU-SAF-013** | Ograniczenie obrotów w trybie zastępczym musi być wprowadzane **narastająco, nie skokowo** | Zjazd z wartości bieżącej do docelowej liniowo przez **3 s**. Uzasadnienie: nagłe odcięcie z 8000 do 3500 obr/min w trakcie pokonywania przeszkody to szarpnięcie, które może doprowadzić do wywrotki | T |
| **ECU-SAF-014** | Przy wielu jednoczesnych usterkach ograniczających obowiązuje **najniższy limit obrotów i największe cofnięcie zapłonu**; ograniczenia nie sumują się | Sumowanie dałoby przy dwóch drobnych usterkach ograniczenie ostrzejsze niż przy jednej poważnej | I, T |
| ECU-SAF-011 | Zmiana parametrów podczas pracy silnika (live tuning) musi podlegać ograniczeniom | **Blokada w wariantach z TPS:** obroty > 5000 obr/min **i jednocześnie** otwarcie przepustnicy > 60%. **W MVP-A warunku obciążenia nie da się ocenić — sposób blokady `[DO USTALENIA]`, patrz DOC-001 rozdz. 11.3.** — koniunkcja, nie alternatywa. **Limity:** 2° zapłonu i 5% dawki na pojedynczy zapis, ta sama komórka nie częściej niż co 500 ms. **Zakres dozwolony:** komórki map, przesunięcia globalne, progi wentylatora. **Zabronione przy pracującym silniku:** konfiguracja sprzętowa, progi rozrusznika, parametry rozruchu, próg ogranicznika, parametry quickshiftera. ECU weryfikuje każdą zmianę ponownie po odebraniu | I, T |
| **ECU-SAF-011a** | Sesja strojenia musi zostać przerwana automatycznie, a mapy wrócić do wartości zapisanych trwale | Wyzwalacze: usterka klasy K3 lub K4, zanik komunikacji USB, przekroczenie progu temperatury cieczy, przejście w stan inny niż PRACA. Sesja operuje na kopii roboczej w RAM — przerwanie nie może zostawić w pamięci nieulotnej mapy w stanie pośrednim | T |

---

## 8. Diagnostyka i logowanie

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| ECU-DIA-001 | Każda wykryta usterka musi mieć kod, znacznik czasu, licznik wystąpień i status (aktywna/historyczna) | — | I, T |
| ECU-DIA-002 | Usterki muszą być klasyfikowane jako krytyczne (przejście w stan awarii) lub niekrytyczne (praca z ostrzeżeniem) | Klasyfikacja w specyfikacji FW punkt E | I |
| ECU-DIA-003 | ECU musi wykrywać zanik komunikacji z HMI i zapisywać to jako zdarzenie | Timeout **1000 ms** — dłuższy niż HMI-UI-003, bo silnik pracuje dalej mimo zaniku HMI; ECU nie zgłasza usterki przy chwilowym zakłóceniu | T |
| ECU-DIA-004 | Przyczyna każdego wybudzenia musi być zapisana do logu | — | T |
| **ECU-LOG-005** | **Zakres logowania on-board ograniczony do zdarzeń krytycznych (czarna skrzynka). Pełne logowanie sesji jazdy NIE jest funkcją tej wersji** — logowanie ciągłe dostępne wyłącznie przez USB na stanowisku | — | I |
| ECU-LOG-006 | Przy wykryciu wypadku ECU musi zapisać dane z okna przed i po zdarzeniu | Okno `[DO USTALENIA]` s przed / `[DO USTALENIA]` s po | T |
| ECU-LOG-007 | Zapis czarnej skrzynki musi zostać dokończony mimo zaniku zasilania | — | T (przerwanie zasilania w trakcie zapisu) |
| ECU-LOG-008 | Licznik motogodzin musi być odporny na zanik zasilania (zapis atomowy) | — | T |

> **Formalna zmiana zakresu 29.09.2026 — quickshifter i czujnik sprzęgła usunięte z produktu.** Decyzja Pawła. Usunięte wymagania: ECU-SEN-012, ECU-SEN-013, ECU-SEN-014, ECU-SEN-015, ECU-IGN-009, ECU-IGN-010, ECU-IGN-011, ECU-SAF-015, HMI-UI-009.
>
> **Powody:** (a) najgorszy stosunek złożoności do wartości w całym projekcie — 9 wymagań, 3 kody usterek, 2 komponenty, 2 piny złącza i sprzężenia z TPS, czujnikiem bębna, przepustnicą oraz trybem zastępczym; (b) jedyna funkcja, która musi wnioskować o **intencji kierowcy**, a nie o mierzalnym stanie fizycznym — stąd trzy kolejne błędy specyfikacji, każdy przechodzący testy pozytywne i zawodzący w normalnej jazdzie; (c) w technicznym terenie kierowca używa sprzęgła nieustannie, więc warunek dopuszczenia spełniałby się rzadko; (d) najgroźniejszy tryb awarii w całym ECU — odcięcie zapłonu w niewłaściwym momencie.
>
> **Zwolnione dwa piny złącza** przechodzą do bilansu: luka L33 (niezależny sygnał obciążenia dla wariantów TPI/TBI) dostaje miejsce, jeden pin zostaje w zapasie. Luka L3 (czujnik sprzęgła) wraca do stanu zamkniętego jako niepotrzebna.
>
> **Blipper** (zmiana w dół bez sprzęgła) był poza zakresem już wcześniej i nim pozostaje.

> **F-027 — formalna zmiana zakresu:** wymaganie ECU-LOG-005 utrwala zawężenie przyjęte 2026-08-31. Pierwotna decyzja 1.4 (Faza 1) zakładała pełne logowanie sesji jazdy on-board. **Zmiana zakresu: pełne logowanie sesji usunięte z zakresu tej wersji.** Ograniczenie jest w firmware, nie w sprzęcie — pamięć 8 MB pozwala przywrócić funkcję w przyszłości. Bilans pojemności: przy 20 kanałach × 4 bajty × 100 Hz zapis ciągły to ~8 kB/s, czyli ~17 minut na 8 MB — potwierdza, że pełne logowanie sesji wymagałoby innej pojemności lub innej architektury.

---

## 9. Komunikacja

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| SYS-COM-001 | Magistrala ECU↔HMI: **klasyczny CAN, 500 kbit/s** | Standard motoryzacyjny — narzędzia diagnostyczne i analizatory domyślnie na tę prędkość. Wykorzystanie w normalnej pracy: kilka procent przepustowości. CAN FD odrzucony na rzecz prostoty i dostępności narzędzi | I |
| SYS-COM-001a | **Konsekwencja wyboru klasycznego CAN:** aktualizacja firmware HMI przez ECU jako pośrednika odbywa się ramkami 8-bajtowymi. Przepustowość efektywna ~25-30 kB/s → firmware HMI (~256 KB) ok. 10 s, zasoby graficzne z pamięci zewnętrznej odpowiednio dłużej | Czas aktualizacji do zmierzenia; akceptowalny próg `[DO USTALENIA]` | T |
| SYS-COM-002 | Każda ramka CAN istotna funkcjonalnie musi zawierać licznik sekwencyjny i sumę kontrolną | — | I, T |
| SYS-COM-003 | Odbiornik musi wykrywać ramki zgubione, powtórzone i przekłamane | — | T |
| SYS-COM-004 | Każda ramka cykliczna musi mieć zdefiniowany okres i timeout | `[DO USTALENIA]` | I |
| **SYS-COM-007** | Wybudzenie ECU musi pociągać za sobą **wybudzenie HMI** | Dotychczas opisany był wyłącznie kierunek odwrotny (HMI budzi ECU ramką CAN). Bez tego kierowca budzi ECU przyciskiem startu i nie widzi żadnego wskazania — w szczególności HMI-UI-009 traci sens | T |
| SYS-COM-005 | Wersja protokołu musi być kontrolowana; niezgodność wersji ECU/HMI/aplikacji musi być wykryta i zgłoszona | — | T |
| **SYS-COM-005a** | Przy **każdej** niezgodności wersji protokołu HMI musi wygasić wszystkie dane pomiarowe i wyświetlić wyłącznie komunikat o niezgodności wraz z obiema wersjami | Bez podziału na major/minor — jedna reguła, jedna ścieżka w kodzie. Brak wskazania jest jednoznaczny, wskazanie możliwie fałszywe nie jest | T |
| **SYS-COM-005b** | Pakiet aktualizacyjny musi zawierać firmware ECU i HMI **razem**, a aktualizacja obu musi być jedną transakcją | Usuwa w normalnej eksploatacji sytuację opisaną w SYS-COM-005a. Mechanizm — punkt H specyfikacji FW | T |
| APP-COM-006 | Zapis konfiguracji i map musi być transakcyjny (rozpoczęcie, weryfikacja, zatwierdzenie lub odrzucenie) | — | T (przerwanie w losowym momencie) |

---

## 10. Interfejs użytkownika

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| HMI-UI-001 | Czas reakcji na naciśnięcie przycisku (od naciśnięcia do widocznej zmiany na ekranie) | ≤ **100 ms**. Obejmuje filtrowanie drgań styku, odczyt ADC, rozpoznanie przycisku w drabince, przerysowanie. Powyżej tej wartości interfejs odbierany jako ociężały | T |
| HMI-UI-002 | Częstotliwość odświeżania ekranu | **60 Hz** — natywna częstotliwość panelu RVT35. Animacja realizowana sprzętowo przez koprocesor EVE4 | T |
| SYS-COM-002a | Częstotliwość nadawania danych **szybkozmiennych** po CAN (obroty, prędkość, a w wariantach z TPS także położenie przepustnicy) | ≥ **50 Hz** (nowa wartość co 20 ms) | T |
| SYS-COM-002b | Częstotliwość nadawania danych **wolnozmiennych** po CAN (temperatury, napięcie akumulatora, bieg, motogodziny) | **5–10 Hz**. Uzasadnienie: te wielkości fizycznie nie zmieniają się szybciej; nadawanie ich z częstotliwością danych szybkozmiennych kilkukrotnie zwiększałoby obciążenie magistrali bez żadnego zysku | T |
| HMI-UI-002a | Ruch wskazań musi być wygładzany lokalnie między odebranymi próbkami | Interpolacja w EVE4 — dane przychodzą z 50 Hz, ekran odświeża się z 60 Hz | D |
| HMI-UI-003 | Przy utracie komunikacji z ECU wyświetlacz musi wygasić dane i pokazać komunikat błędu | Timeout **300 ms**. Przy nadawaniu 50 Hz daje to tolerancję 15 zgubionych ramek — odporność na pojedyncze zakłócenie z zapłonu przy szybkim wygaszeniu nieaktualnych danych | T |
| **HMI-UI-006** | Usterki muszą być prezentowane kierowcy w **czterech poziomach** przypisanych wprost do klas usterek | P0 (klasa K0) — wyłącznie log. P1 (K1, K2) — symbol + komunikat do potwierdzenia, symbol zostaje; uszkodzony odczyt zastąpiony kreskami, **nigdy liczbą**. P2 (K3) — symbol + **trwały pas z informacją o ograniczeniu, niemożliwy do schowania**. P3 (K4) — pełny ekran z przyczyną i instrukcją odblokowania | I, T |
| **HMI-UI-007** | Komunikat poziomu P2 musi zawierać **trzy elementy**: co uległo awarii, że moc jest ograniczona celowo, oraz co kierowca ma zrobić | Uzasadnienie: przy mapie awaryjnej silnik pracuje na tyle źle, że bez wyjaśnienia kierowca uzna go za zepsuty i będzie go dalej męczył. Sam komunikat o awarii czujnika tego wymagania nie spełnia | I |
| **HMI-UI-008** | Przy wielu jednoczesnych usterkach ekran zajmuje usterka o **najwyższej klasie**; pozostałe dostępne z listy pod przyciskiem, z licznikiem aktywnych usterek | — | T |
| HMI-UI-004 | Jasność podświetlenia musi być ograniczana po przekroczeniu progu temperatury | Próg `[DO USTALENIA]` °C, charakterystyka `[DO USTALENIA]` | T |
| HMI-UI-005 | Wyświetlacz musi być czytelny w pełnym słońcu | Kryterium `[DO USTALENIA]` | T (test na słońcu) |

---

## 11. Pozycje blokujące bramkę G0

Wszystkie oznaczenia `[DO USTALENIA]` muszą zostać zamknięte przed przejściem bramki G0. Wymagają one:

| Grupa | Sposób ustalenia |
|---|---|
| Wartości dotyczące zapłonu i wtrysku | Decyzja projektowa + pomiar na stanowisku (punkt C specyfikacji FW) |
| Progi usterek i czasy filtrowania | Punkt B i E specyfikacji FW (macierz usterek) |
| Parametry komunikacji | Faza 2-Desktop (specyfikacja protokołu) |
| Dane wtryskiwaczy | Pomiar na fizycznym wtryskiwaczu (F-014) |
| Profil wibracji | Przyjęcie z normy lub pomiar na motocyklu |
| Kryteria czytelności wyświetlacza | Test na słońcu (Faza 6 lub 9) |
