# Wymagania — ECU „Dust ONE"

105 wymagań z wartościami i metodą weryfikacji, oraz tabela pokrycia (traceability) od wymagania do dowodu.

Pozycje `[DO USTALENIA]` blokują bramkę G0; ich aktualną listę generuje `scripts/kontrola.py`. Pozycje nierozstrzygnięte opisuje `otwarte.md`, sprzęt `produkt.md`, firmware `firmware.md`.

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
| | | BTL | bootloader i aktualizacja |

**Metody weryfikacji:** A = analiza/obliczenie, I = inspekcja/przegląd, T = test, D = demonstracja.

**Oznaczenia statusu wartości:**
- Wartość liczbowa — ustalona
- `[DO USTALENIA]` — wymaga decyzji projektowej lub pomiaru; **każda taka pozycja w MVP-A blokuje bramkę G0.** Wymagania **[B/C]** z `[DO USTALENIA]` blokują dopiero bramkę wariantu B/C — warianty B i C są osobną wariacją projektu, realizowaną po MVP-A (decyzja Pawła 15.10.2026)

**Warianty (za kartą MVP, plan naprawczy rozdz. 8):** wymagania oznaczone **[A]** dotyczą MVP-A (Beta 300RR, gaźnik). **[HW]** oznacza wymagania zdolności sprzętowej weryfikowane na stanowisku. **[B/C]** dotyczą wariantów TPI/TBI.

---

## 2. Warunki pracy (obowiązują dla wszystkich wymagań, o ile nie wskazano inaczej)

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| SYS-ENV-001 | Zakres napięcia zasilania, przy którym ECU musi pracować w pełnym zakresie funkcji | 9,0–16,0 V | T |
| SYS-ENV-002 | Zakres napięcia, przy którym ECU musi zachować sterowanie silnikiem (dopuszczalna ograniczona funkcjonalność) | 7,0–18,0 V | T |
| SYS-ENV-003 | Zakres temperatury otoczenia pracy **ECU** | **−40…+50 °C** w miejscu montażu (tył motocykla albo przy airboxie, z dala od silnika i wydechu). **Zmiana 1.11.2026 (decyzja Pawła):** wcześniejsze +85 °C było klasą sterowników samochodowych, a nie temperaturą miejsca montażu. Górna granica do potwierdzenia rejestratorem temperatury (Z20). Klasa komponentów — SYS-ENV-003b bez zmian | T |
| **SYS-ENV-003a** | Zakres temperatury otoczenia pracy **HMI** | **−20…+70 °C** — ograniczone panelem LCD, nie wyborem projektowym: powyżej ~70 °C ciekły kryształ przechodzi w fazę izotropową i ekran czernieje. Dolna granica z karty modułu | T |
| **SYS-ENV-003b** | Klasa temperaturowa komponentów | Każdy element czynny musi mieć zakres pokrywający **temperaturę wewnątrz obudowy w najgorszym przypadku** — maksimum z SYS-ENV-003 powiększone o przyrost w jego miejscu na PCB — z marginesem **co najmniej 15 °C**. Minimum: **AEC-Q100 Grade 1 (−40…+125 °C)** dla elementów toru mocy i zapłonu; **Grade 2 (−40…+105 °C)** dopuszczalny w sekcji analogowej po wykazaniu lokalnego przyrostu pomiarem; elementy bierne **AEC-Q200**; **czujniki MEMS — AEC-Q100 albo AEC-Q103** (standard AEC dla MEMS, dodane 25.10.2026). Element bez kwalifikacji motoryzacyjnej wymaga **odstępstwa zatwierdzonego przez właściciela projektu** z uzasadnieniem i oceną skutków | A, T |
| SYS-ENV-004 | Zakres temperatury przechowywania | **−40…+105 °C** — musi pokrywać zakres pracy oraz nagrzanie bez zasilania po zgaszeniu silnika | A |
| SYS-ENV-005 | Klasa szczelności obudowy ECU i HMI | IP67 minimum | T |
| SYS-ENV-006 | Odporność na wibracje | `[DO USTALENIA]` — profil do przyjęcia z normy lub pomiaru na motocyklu | A, T |
| SYS-ENV-007 | Zakres obrotów silnika, w którym ECU musi sterować zapłonem | 200–10 000 obr/min | T |
| **SYS-ENV-008** | ECU musi przetrwać **odwrotną polaryzację** zasilania | **−14 V przez 60 s**, bez uszkodzenia i bez przepalenia bezpiecznika (ISO 16750-2) | T |
| **SYS-ENV-009** | ECU musi przetrwać **zrzut obciążenia ograniczony** (poluzowany zacisk akumulatora przy pracy silnika) | **35 V / 400 ms** — wartość wstępna; korekta po pomiarze napięcia jałowego uzwojenia ładującego. Praca w trakcie nie jest wymagana | A, T |
| **SYS-ENV-010** | ECU musi być odporne na **impulsy przewodzone na linii zasilania** | Poziomy ISO 7637-2 dla 12 V: impuls 1 (−150 V, 10 Ω, 2 ms), 2a (+112 V, 2 Ω, 50 µs), 3a/3b (−220/+150 V, 50 Ω, 150 ns). Przy 1, 3a, 3b dopuszczalny reset; przy 2a praca bez zakłóceń. **Rozruch z kabli 24 V poza zakresem** — zapis w instrukcji | A, T |

---

## 3. Zapłon

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| ECU-IGN-001 **[A]** | ECU musi wyznaczać moment zapłonu na podstawie mapy kąta wyprzedzenia w funkcji obrotów | — | I, T |
| ECU-IGN-002 **[A]** | Błąd momentu wyzwolenia zapłonu względem wartości zadanej, mierzony na wyjściu drivera, przy jednoczesnej pracy logowania, CAN i USB | ≤ **1,0°** kąta wału w 99,9 percentylu, w zakresie 1 000–10 000 obr/min i 7,0–16,0 V | T |
| ECU-IGN-005 **[A]** | Wyzwalanie tyrystora musi być ograniczone **niezależnie od firmware i zegara**: zawieszone wyjście sterujące w dowolnym stanie może dać **najwyżej jedną iskrę** | **Zmiana 25.10.2026 (decyzja Pawła)** — zastępuje dawny limit czasu ładowania cewki indukcyjnej. Realizacja: bramka tyrystora sprzężona pojemnościowo (kondensator szeregowy, dioda rozładowująca, rezystor bramka–katoda) | T (wstrzykiwanie usterek) |
| ECU-IGN-006 **[A]** | Ogranicznik obrotów musi odcinać zapłon powyżej progu konfigurowalnego przez użytkownika | Zakres nastawy 3 000–12 000 obr/min | T |
| ECU-IGN-006a **[A]** | Histereza ogranicznika musi być **konfigurowalna z aplikacji desktop** | Domyślnie **200 obr/min**, zakres dopuszczalny **50–500 obr/min**. Aplikacja odrzuca wartości spoza zakresu przed wysłaniem; ECU weryfikuje ponownie po odebraniu | T |
| **ECU-IGN-012** | Parametry geometrii koła impulsowego muszą być **danymi kalibracyjnymi**, nie stałymi w kodzie | Beta 300 RR 2015 (pomiar 11.10.2026): **1 wypust, długość 30° wału, krawędź natarcia 30° przed GMP, krawędź spływu w GMP**. Platforma ma obsługiwać różne silniki, każdy o innej geometrii | I, T |
| **ECU-IGN-013** | ECU musi utrzymywać **ciągły model położenia wału**, korygowany przy każdej ważnej krawędzi natarcia i ekstrapolowany między nimi | Konieczny do bramkowania kątowego wejścia, rozróżniania błędu predykcji od usterki wykonania (ECU-IGN-024) i restartu w ruchu (zmiana uzasadnienia 25.10.2026 — dawny powód, start ładowania cewki, nie dotyczy AC-CDI) | I, T |
| **ECU-IGN-014** | Estymata prędkości do wyznaczenia zwłoki iskry musi pochodzić z **interwału między krawędziami wypustu z poprzedniego obrotu**, z korektą przyspieszenia z dwóch kolejnych okresów | Interwał wypustu mierzy prędkość chwilową w tej samej fazie wału, w której nastąpi iskra, więc tętnienie prędkości w obrębie obrotu znosi się systematycznie. Średnia z pełnego obrotu daje błąd **systematyczny**, który się nie uśrednia | A, T |
| **ECU-IGN-015** | Wyprzedzenie zapłonu musi być ograniczone **twardym limitem geometrycznym**, niekonfigurowalnym, odrzucającym każdą wyższą wartość z mapy wraz z zapisem zdarzenia | **28° przed GMP.** Iskra musi wypaść po krawędzi natarcia (30°), żeby odnosić ją do świeżego punktu; 2° marginesu zapewniają dodatnią zwłokę mimo tolerancji mechanicznej i opóźnienia detekcji | I, T |
| **ECU-IGN-016** | Mapa musi zawierać **limit wyprzedzenia zależny od punktu pracy**, niższy niż geometryczny | Limit geometryczny chroni przed błędem mapy, **nie przed detonacją** — ta może wystąpić znacznie poniżej 28°. Wartości ustalane w Fazie 8 z obserwacją detonacji | T |
| **ECU-IGN-017** | ECU musi **odrzucać zbocza przychodzące poza oknem kątowym** spodziewanego położenia krawędzi natarcia, bez wpływu na model kąta i bez utraty iskry | Okno wstępnie **±20° poniżej 2000 obr/min, ±10° powyżej** — do wystrojenia w Fazie 8. Zapłon przebiega normalnie z modelu kąta. Bramkowanie nieaktywne przy nieważnym modelu (rozruch, po resecie) | T (wstrzykiwanie zakłóceń) |
| **ECU-IGN-018** | ECU musi wykrywać **niewiarygodny sygnał obrotów** według trzech kryteriów | Długość wypustu poza **±25%** kalibracji; zbocze poza oknem kątowym; stosunek kolejnych okresów poza **0,5–2,0**. Progi wstępne, do wystrojenia w Fazie 8. Pojedyncze naruszenie = odrzucenie zbocza (K0); powtarzalne = K4 | T |
| **ECU-IGN-019** | W stanie ROZRUCH iskra musi być wyzwalana **bezpośrednio krawędzią spływu wypustu (GMP)**, bez prognozy czasowej, **dopiero po potwierdzeniu obrotu wału do przodu** | **Zmiana 1.11.2026 (decyzja Pawła):** iskra już przy pierwszym przejściu wypustu (25.10) groziła iskrą przy **cofnięciu wału** po nieudanym kopnięciu — symetryczny wypust daje ten sam sygnał w obie strony, a samo „drugie przejście” nie wystarcza, bo cofnięcie też jest drugim przejściem. Mechanizm potwierdzenia kierunku i parametry: `[DO USTALENIA]` po pomiarze O-009 (kandydaci: dwa przejścia z wiarygodnym czasem obrotu, asymetria sygnału czujnika, faza uzwojenia wzbudzającego). Koszt: do jednego obrotu wału opóźnienia na kopnięcie. **Bez zmian z 25.10:** iskra na krawędzi spływu zamiast prognozy (sprężanie hamuje wał); **wyjątek** — restart w ruchu z ważnym modelem kąta: iskra natychmiast z mapy. Położenie zbocza spływu względem GMP — O-005 | T |
| **ECU-IGN-021** **[A]** | Silnik musi dać się uruchomić **kickstarterem przy napięciu 7 V na złączu ECU** | Scenariusz: akumulator niezdolny do obrócenia rozrusznika. ECU uruchamia się, synchronizuje i daje iskrę przy 7 V. W AC-CDI energia iskry nie pochodzi z akumulatora — wymaganie obciąża zasilanie logiki i kondycjoner VR. Granica spójna z SYS-ENV-002. **Nie obejmuje rozruchu bez akumulatora** — decyzja Pawła 18.10.2026 | T |
| **ECU-IGN-022** **[A]** | **Bezwzględna granica błędu kąta zapłonu** poza stanem ROZRUCH, w **100 % zapłonów** (uzupełnia statystyczne ECU-IGN-002) | Iskra **wcześniej niż zadana o ≤ 1°**, **później niż zadana o ≤ 2°**, w zakresie 1 000–10 000 obr/min i 7,0–16,0 V. Decyzja Pawła 25.10.2026. Osiągalność w dolnym zakresie obrotów przy gwałtownym hamowaniu wału do wykazania modelem błędu (O-008) | A, T |
| **ECU-IGN-023** **[A]** | Iskra **nigdy przed krawędzią natarcia wypustu** — zapewnione strukturalnie **wobec błędu prognozy kąta**. **Nie** chroni przed błędnym firmware: HRTIM ma programowe wymuszenie wyjścia (poprawka brzmienia 1.11.2026, B.1.3) | Timer zapłonu **startowany sprzętowo zboczem natarcia**; minimalne opóźnienie w rejestrze = odpowiednik **2°** (spójne z limitem geometrycznym 28°, C.1.9). Błąd obliczeń nie może odpalić iskry przed zboczem | I (konfiguracja HRTIM), T |
| **ECU-IGN-024** **[A]** | Firmware musi **odczytywać rzeczywisty moment wyzwolenia tyrystora** i reagować na przekroczenia | **Wyzwolenie niezgodne ze zleceniem** (usterka wykonania) → tryb zastępczy **od pierwszego zdarzenia** (DTC-IGN-06). **Przekroczenie ECU-IGN-022 przy wyzwoleniu zgodnym ze zleceniem** (błąd prognozy — fizyka wału) → log każdego zdarzenia, tryb zastępczy przy **3 przekroczeniach w 100 obrotach** (DTC-IGN-07). **Tryb zastępczy:** iskra na krawędzi spływu (GMP) + ograniczenie obrotów, K3. Decyzja Pawła 25.10.2026 | T (wstrzykiwanie usterek) |
| **ECU-IGN-025** **[A]** | Napięcie kondensatora zapłonowego w chwili iskry nie może być niższe niż w **fabrycznym CDI** przy tych samych obrotach | Porównanie w zakresie od kopnięcia do 10 000 obr/min; odniesienie: pomiar fabrycznego układu (`measurements/pomiar-wzbudzajacego.md`). Wymaganie względne — nie wymaga wartości przed pomiarem | T |
| **ECU-IGN-026** **[A]** | Kondensator zapłonowy musi się **rozładować po zatrzymaniu wału** | Do **≤ 60 V w ≤ 5 s** (decyzja Pawła 25.10.2026; wzorzec IEC 60204-1) — **łańcuch rozładowujący spełnia to sam**; osobny łańcuch pomiarowy (ECU-IGN-028) rozładowuje dodatkowo. Bezpieczeństwo przy serwisie i rozłączaniu złącza. Rezystor rozładowujący nie może obniżyć energii iskry przy kopnięciu poniżej ECU-IGN-025 | T |
| **ECU-IGN-027** **[A]** | Odstępy izolacyjne PCB i **osobnego złącza zapłonu** (od 3.11.2026) dla obwodów uzwojenia wzbudzającego, kondensatora i pierwotnego cewki | Wyliczane ze **zmierzonego** napięcia szczytowego wg IPC-2221 z zapasem — `[DO USTALENIA]` po pomiarze (O-001, punkt 2) | I, A |
| **ECU-IGN-028** **[A]** | ECU musi **mierzyć napięcie kondensatora zapłonowego** osobnym łańcuchem pomiarowym (dzielnik → ADC), z próbką **wyzwalaną sprzętowo przed każdą zaplanowaną iskrą** | Decyzja Pawła 1.11.2026. W chwili próbki kondensator jest naładowany i napięcie stoi; pomiar trwa mikrosekundy. Służy do sprawdzania ECU-IGN-025 w eksploatacji i do diagnostyki (DTC-IGN-09). Stała czasowa wejścia dzielnika — przy schemacie | T |
| **ECU-IGN-029** **[A]** | ECU musi **wykryć przerwę w łańcuchu rozładowującym** | Po zatrzymaniu wału, przy stojącym wale: napięcie kondensatora **> 60 V po 5 s** → DTC-IGN-10 i ostrzeżenie; **na silnik bez wpływu**. Próg = ECU-IGN-026. Sprawdzenie przerywane, gdy wał się ruszy (kopnięcie, toczenie na biegu) — brak fałszywych alarmów. Decyzja Pawła 1.11.2026 | T |
| **ECU-IGN-030** **[B/C]** | Wspólna PCB musi mieć **stopień zapłonu dla cewki indukcyjnej (DC-TCI)**, sterowany z tego samego kanału HRTIM co blok AC-CDI i obsadzany zależnie od wariantu | Decyzja Pawła 1.11.2026 (Z19, O-065). Driver: kandydat VBG08H-E do ponownej kwalifikacji (arkusz 11 pól). Prąd i rezystancja uzwojenia pierwotnego cewki TPI/TBI: `[DO USTALENIA]` | I, T |
| **ECU-IGN-031** **[B/C]** | Odcięcie awaryjne w trakcie ładowania cewki — kill switch, ENDRV, reset procesora, zanik szyny — **nie może wytworzyć iskry** | W TCI przerwanie prądu cewki jest mechanizmem iskry, więc bramkowanie z wariantu A (bramka AND) nie przenosi się wprost. Wymagane **miękkie wyłączenie** drivera; czas wygaszania i dopuszczalne napięcie wtórne `[DO USTALENIA]` | T (wstrzykiwanie usterek) |
| **ECU-IGN-032** **[B/C]** | Czas ładowania cewki musi być ograniczony **sprzętowo, niezależnie od firmware i zegara procesora** | Sufit `[DO USTALENIA]` ms z charakterystyki cewki. Rejestr HRTIM nie wystarcza — dzieli zegar z chronioną funkcją (dawne O-004). Po przekroczeniu — miękkie wyłączenie (ECU-IGN-031) | T (wstrzykiwanie usterek) |
| **ECU-IGN-033** **[B/C]** | Straty drivera zapłonu muszą mieścić się w bilansie cieplnym ECU przy maksymalnej temperaturze otoczenia (SYS-ENV-003), z marginesami Z17 i progami ECU-SAF-020 | Straty `[DO USTALENIA]` W z dwell i prądu cewki TPI/TBI. Dawny szacunek 4,8 W daje przy 50 °C otoczenia i 3 K/W ~71 °C wewnątrz — w granicach (przy dawnych 85 °C byłoby ~107 °C). **Osobna obudowa B/C, projektowana przy etapie B/C (decyzja Pawła 1.11.2026)**; na wspólnej PCB — miejsce pod kontakt termiczny drivera z tą obudową | A, T |
| **ECU-IGN-020** **[A]** | Mapa zapłonu w wariancie gaźnikowym musi być **jednowymiarowa** — kąt wyprzedzenia wyłącznie w funkcji obrotów | **Beta 300 RR 2015 nie ma czujnika położenia przepustnicy i nie będzie dokładany** (założenie Z1 obalone 11.10.2026). Fabryczny układ zapłonowy pracuje tak samo. Wymaganie ECU-IGN-001 od początku mówiło o mapie w funkcji obrotów; dwuwymiarowość weszła bokiem przez wymagania opisujące utratę sygnału, którego w tym wariancie nie ma | I, T |
| ECU-IGN-007 **[A]** | Rozdzielczość zapisu kąta wyprzedzenia w mapie | **0,25°** | I |

---

## 4. Wtrysk

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| ECU-INJ-001 **[HW]** | ECU musi sterować dwoma niezależnymi kanałami wtryskiwaczy | 2 kanały, prąd ciągły ≥ 1,5 A/kanał | T |
| ECU-INJ-002 **[HW]** | Sterowanie w trybie nasyconym dla wtryskiwaczy o rezystancji | 10,5–13,0 Ω | T |
| ECU-INJ-003 **[B/C]** | Rozdzielczość czasu otwarcia wtryskiwacza | ≤ `[DO USTALENIA]` µs | T |
| ECU-INJ-004 **[B/C]** | Czas martwy wtryskiwacza musi być korygowany w funkcji napięcia zasilania | Na podstawie pomiaru — `[DO USTALENIA]` | T |
| **ECU-INJ-007** **[B/C]** | Przy utracie sygnału przepustnicy ECU musi przejść na **mapę awaryjną liczoną na pełne obciążenie** (bogatą w całym zakresie obrotów), nie na dawkę z biegu jałowego | Uzasadnienie: dawka z biegu jałowego przy otwartej przepustnicy oznacza skrajnie ubogą mieszankę pod obciążeniem, czyli zatarcie. Mapa bogata daje kiepską pracę na biegu jałowym i bezpieczną pod obciążeniem. Limit obrotów **3500 obr/min** | T |
| ECU-INJ-005 **[B/C]** | Pompa paliwa musi być załączana na czas wstępnego napełnienia po wybudzeniu | 2,0 s ± 0,2 s | T |
| ECU-INJ-006 **[B/C]** | Pompa paliwa musi być wyłączana przy braku obrotów przez określony czas | `[DO USTALENIA]` s | T |

---

## 5. Czujniki

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| ECU-SEN-001 | ECU musi obsługiwać czujnik obrotów typu VR (cewka indukcyjna) | Amplituda wejściowa 0,05–100 V szczytowo | T |
| ECU-SEN-002 | ECU musi obsługiwać czujnik obrotów typu Hall, ścieżką wybieraną zworką | Czujnik zasilany **5 V**, wyjście otwarty kolektor lub push-pull. Poziom niski **≤ 1,0 V**, wysoki **≥ 3,5 V**. Wejście znosi trwałe zwarcie do akumulatora (do 16 V) i do masy bez uszkodzenia | T |
| ECU-SEN-003 **[B/C]** | Błąd pomiaru położenia przepustnicy (TPS) po kalibracji — **zdolność sprzętowa dla wariantów B/C; MVP-A nie ma TPS** | ≤ `[DO USTALENIA]` % zakresu | T |
| ECU-SEN-004 | Błąd pomiaru temperatury cieczy chłodzącej | ≤ ±3 °C w zakresie 0…120 °C | T |
| ECU-SEN-005 | Błąd pomiaru temperatury powietrza dolotowego | ≤ ±3 °C w zakresie -20…+80 °C | T |
| ECU-SEN-006 | Błąd pomiaru napięcia akumulatora | ≤ ±0,2 V w zakresie 7,0–16,0 V | T |
| ECU-SEN-007 | ECU musi wykrywać przerwę i zwarcie każdego wejścia czujnikowego | Progi **< 3% i > 97% zakresu przetwornika**, liczone względem rzeczywistego napięcia szyny 5 V. Czasy potwierdzenia wg macierzy usterek (spec. FW B.2.1) | T |
| ECU-SEN-008 | Rozpoznanie pozycji biegu po kalibracji | 100% poprawnych rozpoznań przy 200 zmianach biegu | T |
| ECU-SEN-009 | Chwilowe przejście przez pozycję neutralną podczas zmiany 1↔2 nie może być zgłoszone jako bieg neutralny | **Filtr wybiórczy:** wskazanie biegu zgłaszane natychmiast; wskazanie pozycji neutralnej dopiero po **80 ms** stabilnego odczytu. Uzasadnienie: zmiana biegu trwa 30–60 ms, człowiek zauważa zwłokę powyżej ~150 ms | T |
| ECU-SEN-010 | Błąd pomiaru prędkości koła | **≤ 2 %** po kalibracji obwodu koła, **powyżej 10 km/h**. Poniżej 10 km/h wymaganie nie obowiązuje — za mało impulsów na obrót koła | T |
| **ECU-SEN-016** | ECU musi **mierzyć ciśnienie atmosferyczne** czujnikiem na PCB i zapisywać je w logu — **od wariantu MVP-A** | Zakres **40–115 kPa**, błąd **≤ ±1,0 kPa w 0…+85 °C** i **≤ ±1,5 kPa na krańcach −40 / +125 °C** (wartości z karty KP464); odczyt co najmniej **1 Hz**. W MVP-A wyłącznie logowanie, bez wpływu na sterowanie; w B/C wejście korekty dawki. Decyzja Pawła 25.10.2026 | T |
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
| ECU-PWR-007 | ECU musi monitorować szyny zasilania (ADC) i stan nadzoru szyn w PMIC (rejestry statusu UV/OV) | Od 1.11.2026 — PMIC zamiast sygnałów Power Good | I, T |
| ECU-PWR-008 | Napięcie **wewnętrznej** szyny 5 V (VDD5: MAX9926, komparator, bramka AND, TJA1043) | 5,00 V ±2% w pełnym zakresie obciążenia i temperatury (karta PMIC: 4,9–5,1 V) | A, T |
| **ECU-PWR-008b** | Napięcie zasilania **czujników w wiązce** (VSOUT1) | **5,00 V ±3 %**; odczyty ratiometryczne liczone względem **zmierzonego** VSOUT1 (ADC). Decyzja Pawła 1.11.2026 — VSOUT1 śledzi VDD5 z błędem ±35 mV | A, T |
| **ECU-PWR-008a** | Reakcja na odchylenie szyn 5 V musi być **rozdzielona według szyny** (zmiana 1.11.2026 po przejściu na PMIC — decyzja Pawła) | **VDD5** (MAX9926, komparator, bramka AND): przepięcie **5,20–5,45 V** → PMIC sprzętowo opuszcza ENDRV, zapłon odcięty (karta PMIC tab. 5-2, bez maskowania); **poniżej 4,50 V** → MAX9926 poza zakresem pracy, silnik gaśnie; w logu przyczyna źródłowa „zasilanie VDD5”. **VSOUT1** (czujniki w wiązce): **poza 4,50–5,50 V** (ADC) albo flaga UV/OV z PMIC → **MVP-A:** wszystkie czujniki z wiązki na wartościach zastępczych wg `firmware.md` B.2.1, kod usterki i ostrzeżenie, **bez limitu obrotów** — czujnik wału (VR) i kill switch nie zależą od VSOUT1; **B/C:** grupa G3 (czujnik przepustnicy na VSOUT1). Dawne pasmo 4,50–4,75 / 5,25–5,50 V odpada — odczyty liczone względem zmierzonego VSOUT1 (ECU-PWR-008b) | T |
| **ECU-PWR-009** | Przy przepięciu ECU musi ostrzec kierowcę i **załączyć wentylator jako obciążenie obniżające napięcie** | Próg załączenia **> 16,5 V przez 200 ms**, wyłączenie po spadku **poniżej 15,5 V**. Uzasadnienie: regulator w motocyklu jest typu bocznikującego, więc dołożenie obciążenia realnie obniża napięcie. Światła celowo pominięte — pozostają pod kontrolą kierowcy | T |
| **ECU-PWR-010** | ECU musi wykryć niezałączenie zasilania czujników (VSOUT1 PMIC, od 1.11.2026 zamiast przełącznika obciążenia) i zablokować wyjście ze stanu gotowości | Brak napięcia na szynie czujników **po 5 ms** od załączenia, 3 próby | T |
| **ECU-PWR-011** | ECU musi **zasilać HMI** z B+ przez **przełącznik domyślnie załączony**, z ochroną zwarciową | Decyzja Pawła 3.11.2026. HMI zasilane także w uśpieniu ECU, więc jego przyciski budzą system (O-024). Pracujące ECU może odłączyć HMI — restart zawieszonego HMI, zwarcie w kablu. Pobór przełącznika w uśpieniu ≤ 5 µA (przydział, `produkt.md` 6.1) | I, T |

---

## 7. Bezpieczeństwo

| ID | Wymaganie | Wartość | Weryfikacja |
|---|---|---|---|
| ECU-SAF-001 | Rozwarcie kill switcha musi odciąć zapłon i wtrysk **niezależnie od stanu firmware** (bramkowanie sprzętowe) | Czas reakcji **≤ 10 ms** od rozwarcia do ostatniej możliwej iskry. W AC-CDI oznacza to **zwarcie uzwojenia wzbudzającego oraz sprzętową blokadę wyzwalania tyrystora** — sam brak ładowania nie wystarcza, bo naładowany kondensator może dać jeszcze jedną iskrę. **Obie ścieżki sterowane osobnymi układami progowymi** (decyzja Pawła 1.11.2026): utknięcie jednego w RUN nie może wyłączyć obu. Mechanizm: O-001, analiza B.1.3 | T (wstrzykiwanie usterek) |
| ECU-SAF-002 | Przerwanie przewodu kill switcha lub rozłączenie wtyczki musi skutkować odcięciem **i zostać odróżnione od naciśnięcia przycisku** w logu oraz w komunikacie dla kierowcy | **Układ trzypoziomowy:** rezystor szeregowy i równoległy w module przycisku (zalane, drabinka niskoomowa), podciągnięcie w ECU z VDD5, **obwód dwuprzewodowy z masą prowadzoną z ECU, przycisk odizolowany od ramy** (decyzje Pawła 1.11.2026, O-015). RUN = poziom dolny, STOP = środkowy, przerwa = górny. Bramkowanie sprzętowe jednym komparatorem z progiem między RUN a STOP — odcina w obu przypadkach niezależnie od firmware. Rozróżnienie przez ADC, wyłącznie na potrzeby diagnostyki. Wartości rezystorów i analiza najgorszego przypadku — Faza 4 | T (wstrzykiwanie usterek) |
| **ECU-SAF-002a** | Czas potwierdzenia stanu kill switcha przed zgłoszeniem usterki | **50 ms** — filtruje drgania styku, nie opóźnia odcięcia, bo odcięcie jest sprzętowe i natychmiastowe | T |
| **ECU-SAF-024** | ECU musi **stale porównywać** stan kill switcha odczytany przez ADC ze stanem wyjść obu układów progowych | Niezgodność dłuższa niż ECU-SAF-002a → DTC-SAF-08 i ostrzeżenie; bez wpływu na odcięcie, które działa sprzętowo. Wykrywa usterkę progu albo wejścia ADC w trakcie jazdy, nie dopiero przy STOP. Decyzja Pawła 1.11.2026 | T (wstrzykiwanie usterek) |
| **ECU-SAF-025** | Napięcie kill switcha **poniżej poziomu RUN** (zwarcie przewodu do masy, przerwa podciągnięcia) musi dać **kod usterki i ostrzeżenie, bez odcięcia** | DTC-SAF-07; ostrzeżenie na HMI do usunięcia usterki. **Decyzja Pawła 1.11.2026** — kill w tym stanie nie działa; ryzyko zaakceptowane (`otwarte.md` rozdz. 9) | T |
| ECU-SAF-003 | Po resecie watchdoga wyjścia mocy muszą pozostać wyłączone do zatrzymania wału i świadomego odblokowania przez kierowcę | — | T |
| ECU-SAF-004 | Po zaniku napięcia (brown-out) obowiązuje ten sam zatrzask co po resecie watchdoga | — | T |
| ECU-SAF-005 | Wykrycie wywrotki przez akcelerometr musi odciąć zapłon i uruchomić zatrzask | Kąt przechyłu **> 65°** utrzymany nieprzerwanie **3 s**, wyłącznie w stanie PRACA. **Kąt liczony z kierunku grawitacji i ważny tylko przy całkowitym przyspieszeniu 0,8–1,2 g**; każda próbka z kątem nieważnym (lot po hopie, lądowanie, uderzenie) **zeruje licznik 3 s**. **Wielkość przyspieszenia nie może wywołać gaszenia** — przeciążenia trafiają wyłącznie do czarnej skrzynki (ECU-LOG-006). Decyzja Pawła 25.10.2026. Wartości wstępne — do korekty pomiarem w Fazie 8, kryterium: zero fałszywych zadziałań podczas sesji testowej, w tym na hopach. Świadomie bez warunku prędkości koła: po wywrotce koło często kręci się dalej i warunek zablokowałby wykrycie | T |
| ECU-SAF-006 | **3 resety watchdoga** muszą przenieść ECU w stan awarii bez możliwości automatycznego startu. Licznik zerowany dopiero **po 60 s ciągłej, bezawaryjnej pracy silnika** (nie po samym upływie czasu) | 3 resety; zerowanie po 60 s udanej pracy. Uzasadnienie: dowodem sprawności jest działanie, nie upłynięcie czasu — przy zerowaniu czasowym awaria występująca co 70 s nigdy nie zostałaby wykryta. Licznik przechowywany w pamięci nieulotnej W25Q64. Po trzecim resecie stan awarii kasowany wyłącznie aplikacją desktop | T |
| ECU-SAF-007 | Wszystkie wyjścia mocy muszą być wyłączone w stanie resetu i podczas startu mikrokontrolera (rezystory ściągające) | — | I, T |
| **ECU-SAF-016** | Linia bramkująca wejścia EN driverów musi mieć **rezystory ściągające**, tak aby zanik zasilania komparatora, zanik szyny 5 V oraz stan przed startem mikrokontrolera dawały ten sam skutek: **drivery wyłączone** | **Od 1.11.2026 obejmuje też oba wejścia bramki AND w torze wyzwalania tyrystora** (zezwolenie z komparatora i impuls z HRTIM) oraz ENDRV z PMIC (trzecie wejście bramki AND) — tabela stanów bezpiecznych w `produkt.md` rozdz. 7 (O-017). Rozszerza ECU-SAF-007, które obejmuje wyjścia mocy — **linia bramkująca nie jest wyjściem mocy i nie była nim objęta**. Bez tego zanik zasilania komparatora zostawia na linii decydującej o odcięciu stan nieokreślony | I, T |
| **ECU-SAF-021** | Przy **każdym przejściu kill switcha w STOP** ECU musi sprawdzić **obie** ścieżki odcięcia | Zanik napięcia uzwojenia wzbudzającego (pomiar przez dzielnik → ADC) **i** zablokowanie zezwolenia bramki AND w torze wyzwalania tyrystora (odczyt zwrotny) — oraz stan wyjść **obu układów progowych** (1.11.2026). Niedziałająca ścieżka → DTC-SAF-06, ostrzeżenie; start dozwolony przy jednej sprawnej ścieżce. Wykrywa uszkodzenia ukryte (decyzja Pawła 25.10.2026) | T (wstrzykiwanie usterek) |
| **ECU-SAF-022** | Rozrusznik musi wymagać **załączenia dwóch niezależnych kluczy, każdy z innego źródła polecenia** | **PROFET** (strona zasilania): polecenie procesora × zezwolenie komparatora. **Klucz po stronie masy cewki przekaźnika**: **fizycznie wciśnięty przycisk START** × zezwolenie progu tranzystorowego. Zwarcie dowolnego jednego klucza nie może uruchomić rozrusznika w trakcie jazdy; STOP blokuje oba. **Poprawka 1.11.2026 (decyzja Pawła):** klucz masy sterowany wcześniej samym kill switchem był zamknięty przez całą jazdę i nie chronił przed zwartym PROFET | T (wstrzykiwanie usterek) |
| **ECU-SAF-023** | Rejestry licznika zapłonu (HRTIM) — **a w B/C także liczników wtrysku** — mogą być zapisywane **wyłącznie przez moduł zapłonu i wtrysku** w trybie uprzywilejowanym; próba zapisu z innego modułu firmware musi zostać zablokowana przed wykonaniem | Jednostka ochrony pamięci (MPU) rdzenia Cortex-M4; firmware podzielone na część uprzywilejowaną (zapłon, bezpieczeństwo) i zwykłą (CAN, HMI, logi, live tuning). Naruszenie → wyjątek, DTC-SYS-11, reset z migawką jak przy resecie watchdoga. Decyzja Pawła 1.11.2026 (O-018 punkt 5) | I, T (wstrzykiwanie usterek) |
| **ECU-SAF-020** | ECU musi reagować stopniowo na **przegrzanie własnej elektroniki** | **T1 > 95 °C (5 s):** ostrzeżenie HMI + kod; **T2 > 105 °C (5 s):** wyłączenie świateł i aux; **T3 > 120 °C (10 s) na dwóch niezależnych czujnikach naraz (NTC na PCB i czujnik MCU):** zgaszenie silnika z zatrzaskiem do ostygnięcia poniżej 95 °C. Niewiarygodny czujnik (przerwa, zwarcie, rozbieżność > 20 °C) → kod usterki i **wyłączenie T3**, nigdy zgaszenie. Wartości wstępne, decyzja Pawła 25.10.2026; korekta po analizie termicznej | T (wstrzykiwanie usterek) |
| **ECU-SAF-019** | Kill switch w STOP musi **sprzętowo blokować rozrusznik** | Wejście PROFET kanału rozrusznika bramkowane **komparatorem**, klucz masy cewki przekaźnika — **progiem tranzystorowym** (ECU-SAF-022), niezależnie od firmware. STOP blokuje oba klucze, więc usterka jednego progu albo jednego klucza nie znosi blokady. Decyzja Pawła 25.10.2026, podział na dwa progi 1.11.2026 | T (wstrzykiwanie usterek) |
| **ECU-SAF-018** | Przycisk startu naciśnięty przy uśpionym ECU **budzi je i — jeśli jest trzymany nieprzerwanie — uruchamia rozrusznik** | Rozrusznik dopiero po osiągnięciu gotowości (ECU-PWR-003) i tylko przy kill switchu w RUN. Puszczenie przycisku przed gotowością = samo wybudzenie, bez rozrusznika. Przy słabym akumulatorze kierowca budzi ECU przyciskiem na kierownicy i kopie (decyzja Pawła 18.10.2026) | T |
| **ECU-SAF-017** | Zewnętrzny watchdog musi być zasilany **z tej samej szyny co mikrokontroler** i **nie może mieć programowego wyłącznika** | Nie istnieje stan „procesor zasilony, nadzór wyłączony”. Uśpienie realizowane przez odcięcie zasilania obu (O-013) | I (schemat), T |
| **ECU-SAF-016a** | Komparator kill switcha musi być zasilany z **VDD5 PMIC** | **Zmiana 1.11.2026 (O-018):** wcześniej za przełącznikiem obciążenia, który znika razem z przetwornicami. W uśpieniu komparator nadal bez zasilania (PMIC w STANDBY), więc nie obciąża budżetu (ECU-PWR-001); bramkowanie nie jest wtedy potrzebne — wyjścia trzymają rezystory ściągające (ECU-SAF-016) | I |
| ECU-SAF-008 | Rozrusznik nie może zostać załączony, gdy obroty przekraczają próg | **400 obr/min**, wartość **stała w firmware, niedostępna dla użytkownika**. Uzasadnienie: bendiks wchodzący w obracające się koło zamachowe to natychmiastowe uszkodzenie mechaniczne. Próg niższy niż obroty samodzielnej pracy daje margines na wybieg po zgaszeniu | T |
| ECU-SAF-009 | Czas ciągłej pracy rozrusznika | ≤ 5,0 s ± 0,2 s | T |
| ECU-SAF-010 | Rozrusznik musi być wyłączony automatycznie po przekroczeniu progu obrotów samodzielnej pracy | **700 obr/min**, wartość **stała w firmware** | T |
| ECU-SAF-010a | **Warunek spójności:** próg wyłączenia rozrusznika (SAF-010) musi być zawsze wyższy niż próg blokady załączenia (SAF-008) | 700 > 400. Naruszenie tej relacji tworzy stan nierozstrzygalny — ECU jednocześnie wyłączałoby rozrusznik i uznawało, że wolno go załączyć | I |
| **ECU-SAF-006a** | Przy każdym resecie watchdoga i przy brown-oucie ECU musi zapisać **migawkę stanu** do pamięci nieulotnej | Zawartość: przyczyna resetu z rejestru MCU, **ostatni osiągnięty punkt kontrolny**, stan maszyny stanów, obroty, napięcie akumulatora i obu szyn, temperatura MCU, czas od startu, motogodziny, wersja firmware, suma kontrolna map, aktywne kody usterek. Przechowywane **3 ostatnie migawki**. Ślad bieżący prowadzony w rejestrach domeny podtrzymywanej (bez zużycia Flash), przepisywany do W25Q64 raz, po resecie | T |
| **ECU-SAF-006b** | Każde zadanie czasu rzeczywistego musi zapisywać swój identyfikator jako punkt kontrolny przy wejściu | Lista identyfikatorów w punkcie I specyfikacji FW; **zadanie bez identyfikatora jest luką w diagnostyce**. Narzut: jedna instrukcja zapisu na zadanie | I, T |
| **ECU-SAF-012** | Błędna suma kontrolna **map sterowania** wykryta przy starcie musi zablokować uruchomienie silnika | Zakres: mapa zapłonu, mapa wtrysku, korekty, progi wentylatora, próg i histereza ogranicznika. Komunikat o uszkodzeniu map z instrukcją ponownego wgrania | T |
| **ECU-SAF-012a** | Błędna suma kontrolna **konfiguracji użytkownika** nie może blokować uruchomienia silnika | Zakres: obwód koła, jednostki, układ i wygląd ekranów HMI, jasność. Reakcja: wartości domyślne + ostrzeżenie. Kryterium podziału względem ECU-SAF-012: czy wartość wpływa na to, co ECU robi z silnikiem | T |
| **ECU-SAF-013** | Ograniczenie obrotów w trybie zastępczym musi być wprowadzane **narastająco, nie skokowo** | Zjazd z wartości bieżącej do docelowej liniowo przez **3 s**. Uzasadnienie: nagłe odcięcie z 8000 do 3500 obr/min w trakcie pokonywania przeszkody to szarpnięcie, które może doprowadzić do wywrotki | T |
| **ECU-SAF-014** | Przy wielu jednoczesnych usterkach ograniczających obowiązuje **najniższy limit obrotów i największe cofnięcie zapłonu**; ograniczenia nie sumują się | Sumowanie dałoby przy dwóch drobnych usterkach ograniczenie ostrzejsze niż przy jednej poważnej | I, T |
| ECU-SAF-011 | Zmiana parametrów podczas pracy silnika (live tuning) musi podlegać ograniczeniom | **Blokada w wariantach z TPS:** obroty > 5000 obr/min **i jednocześnie** otwarcie przepustnicy > 60%. **W MVP-A (bez TPS) — decyzja 12.10.2026, O-020:** zmiany przy pracującym lub uzbrojonym silniku trafiają wyłącznie do bufora edycji; **aktywacja tylko przy rozbrojonym silniku** (wał nieruchomy, zapłon rozbrojony) **i po jawnej komendzie** z aplikacji. Osobny tryb stanowiskowy z fizycznym zezwoleniem dopuszcza aktywację przy pracy na hamowni. — koniunkcja, nie alternatywa. **Limity:** 2° zapłonu i 5% dawki na pojedynczy zapis, ta sama komórka nie częściej niż co 500 ms. **Zakres dozwolony:** komórki map, przesunięcia globalne, progi wentylatora. **Zabronione przy pracującym silniku:** konfiguracja sprzętowa, progi rozrusznika, parametry rozruchu, próg ogranicznika, parametry quickshiftera. ECU weryfikuje każdą zmianę ponownie po odebraniu | I, T |
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
| ECU-LOG-006 | Przy wykryciu wypadku ECU musi zapisać dane z okna przed i po zdarzeniu | Okno **10 s przed / 5 s po**. Zapis „po” może nie powstać, jeśli zdarzenie odłączy akumulator — O-042 | T |
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
| SYS-COM-001a | **Konsekwencja wyboru klasycznego CAN:** aktualizacja firmware HMI przez ECU jako pośrednika odbywa się ramkami 8-bajtowymi. Przepustowość efektywna ~25-30 kB/s → firmware HMI (~256 KB) ok. 10 s, zasoby graficzne z pamięci zewnętrznej odpowiednio dłużej | Firmware HMI **≤ 60 s**, zasoby graficzne **≤ 5 min**. Aktualizacja w warunkach warsztatowych | T |
| SYS-COM-002 | Każda ramka CAN istotna funkcjonalnie musi zawierać licznik sekwencyjny i sumę kontrolną | — | I, T |
| SYS-COM-003 | Odbiornik musi wykrywać ramki zgubione, powtórzone i przekłamane | — | T |
| SYS-COM-004 | Każda ramka cykliczna musi mieć zdefiniowany okres i timeout | Timeout **= 3 × okres ramki, nie mniej niż 50 ms**. Pojedyncza zgubiona ramka nie może wywołać usterki (test negatywny). Okresy poszczególnych ramek — specyfikacja protokołu, Faza 2-Desktop | I, T |
| **SYS-COM-008** | ECU musi **uruchamiać i prowadzić silnik bez HMI** (odłączone, uszkodzone, zawieszone) | Brak HMI = kod usterki DTC-COM-01, nie blokada. Usypianie bez potwierdzenia — wystarcza cisza na magistrali; wybudzanie przyciskiem startu i przez USB działa bez HMI (decyzja Pawła 18.10.2026) | T |
| **SYS-COM-007** | Wybudzenie ECU musi pociągać za sobą **wybudzenie HMI** | Dotychczas opisany był wyłącznie kierunek odwrotny (HMI budzi ECU ramką CAN). Bez tego kierowca budzi ECU przyciskiem startu i nie widzi żadnego wskazania — w szczególności HMI-UI-009 traci sens | T |
| SYS-COM-005 | Wersja protokołu musi być kontrolowana; niezgodność wersji ECU/HMI/aplikacji musi być wykryta i zgłoszona | — | T |
| **SYS-COM-005a** | Przy **każdej** niezgodności wersji protokołu HMI musi wygasić wszystkie dane pomiarowe i wyświetlić wyłącznie komunikat o niezgodności wraz z obiema wersjami | Bez podziału na major/minor — jedna reguła, jedna ścieżka w kodzie. Brak wskazania jest jednoznaczny, wskazanie możliwie fałszywe nie jest | T |
| **SYS-COM-005b** | Pakiet aktualizacyjny musi zawierać firmware ECU i HMI **razem**, a aktualizacja obu musi być jedną transakcją | Usuwa w normalnej eksploatacji sytuację opisaną w SYS-COM-005a. Mechanizm — punkt H specyfikacji FW | T |
| **SYS-COM-009** | HMI musi zgłaszać ECU po CAN **model, rewizję sprzętu i wersję firmware** | Rewizja sprzętu odczytywana przez procesor HMI z rezystorów na jego płytce. ECU wie, jaki wariant HMI jest podłączony — bez osobnego przewodu HWID. Rozszerzenie SYS-COM-005. Decyzja Pawła 3.11.2026 | T |
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
| HMI-UI-004 | Jasność podświetlenia musi być ograniczana po przekroczeniu progu temperatury | Start ograniczania przy **Tmax panelu − 5 °C** (Tmax z karty wybranego panelu), liniowo do **70 %** jasności przy Tmax | T |
| HMI-UI-005 | Wyświetlacz musi być czytelny w pełnym słońcu | Przy natężeniu **≥ 80 klx** na ekranie bieg i prędkość odczytane bezbłędnie przez 3 osoby z odległości 70 cm, pod kątem do 45°. **Test przy jasności już ograniczonej przez HMI-UI-004** — ograniczenie działa właśnie w słońcu. Okulary polaryzacyjne poza kryterium (decyzja 18.10.2026) | T (test na słońcu) |

---

## 10a. Bootloader i aktualizacja (decyzje Pawła 25.10.2026, O-040, O-019)

| ID | Wymaganie | Wartość / warunki | Weryfikacja |
|---|---|---|---|
| **ECU-BTL-001** | Aktualizacja firmware ECU i HMI musi być dopuszczona **wyłącznie przy spełnieniu wszystkich warunków naraz**, sprawdzanych przez ECU, nie przez aplikację | **Kill switch w STOP** + **wał stoi** (brak impulsów VR przez ≥ 2 s **i** kill switch w STOP — sam brak impulsów nie wystarcza) + **napięcie akumulatora ≥ 12,0 V**. Utrata któregokolwiek warunku w trakcie: przerwanie zapisu, praca na dotychczasowym banku | T |
| **ECU-BTL-002** | Przez cały czas aktualizacji iskra i rozrusznik muszą być **fizycznie niemożliwe** | Zapewnione sprzętowym bramkowaniem kill switcha (ECU-SAF-001, ECU-SAF-019) — niezależnie od stanu GPIO i timerów w trakcie kasowania i zapisu Flash | T (pomiar wyjść od startu bootloadera do startu aplikacji) |
| **ECU-BTL-003** | Pamięć firmware musi mieć **dwa banki**; nowy obraz trafia do banku nieaktywnego | Przerwanie zasilania lub połączenia na dowolnym etapie zostawia ECU **w pełni sprawne na poprzedniej wersji** | T (przerwanie zasilania w losowym momencie, min. 20 prób) |
| **ECU-BTL-004** | Obraz musi być zweryfikowany **sumą kontrolną** przed aktywacją | CRC-32 całego obrazu (sprzętowy moduł CRC STM32G4) + zgodność wersji ECU/HMI/protokołu (SYS-COM-005). **Bez podpisu cyfrowego** — ryzyko zaakceptowane (`otwarte.md` rozdz. 9) | T |
| **ECU-BTL-005** | Nowa wersja musi **potwierdzić sprawność**, inaczej automatyczny powrót do poprzedniej | Potwierdzenie = dojście do stanu GOTOWOŚĆ z poprawnym autotestem. Brak potwierdzenia w **3 kolejnych startach** → powrót do poprzedniego banku i kod usterki | T |
| **ECU-BTL-006** | Bootloader musi być **zabezpieczony przed zapisem** i nieaktualizowalny w eksploatacji | Zmiana bootloadera wyłącznie przez SWD | I |

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

---

## 20. Tabela pokrycia wymagań (traceability)
Łańcuch: **wymaganie → realizacja sprzętowa → moduł firmware → identyfikator testu → dowód**.

Zasady:
- Punktem wyjścia jest identyfikator wymagania z tego dokumentu. Funkcja, która nie ma wymagania, nie może być prześledzona — takie przypadki zebrano w rozdz. 20.11.
- **ID testu**: `T-[OBSZAR]-[NUMER]`, numeracja odpowiada wymaganiu (ECU-IGN-002 → T-IGN-002). Jeden test może pokrywać kilka wymagań; wtedy ten sam identyfikator powtarza się w wierszach. Treść testów powstaje w Fazie 3 (plan testów).
- **Moduł FW**: punkt specyfikacji `firmware.md` (A–J). Kreska oznacza wymaganie realizowane wyłącznie sprzętowo lub poza firmware ECU.
- **Dowód**: konkretny artefakt zamykający wymaganie. Dopóki nie istnieje, wiersz pozostaje otwarty.
- **Faza**: faza, w której test jest wykonywany. Wypełnienie kolumny „Dowód" dla wszystkich wierszy przypisanych do danej fazy jest warunkiem wyjścia z jej bramki (`proces.md`).

Status: ⬜ niewykonane · 🔶 częściowo · ✅ zamknięte dowodem.

### 20.1 Warunki pracy

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| SYS-ENV-001 | PMIC TPS65381A-Q1, ochrona wejścia (6.2d) | — | T-ENV-001 | Protokół pomiarowy: przemiatanie 9→16 V z zasilacza laboratoryjnego, kontrola pełnego zestawu funkcji | 6 | ⬜ |
| SYS-ENV-002 | Jw. + kondensator buforowy | B (degradacja) | T-ENV-002 | Protokół: 7→18 V, potwierdzenie zachowania sterowania silnikiem i zapisu usterki | 6 | ⬜ |
| SYS-ENV-003 | Obudowa wariantu A (rozdz. 10 `produkt.md`) + rejestrator temperatury w miejscu montażu (Z20) | — | T-ENV-003 | Protokół z komory, przemiatanie −40…+50 °C otoczenia z pomiarem temperatur wewnątrz; zapis temperatury w miejscu montażu w upał, w słońcu i po postoju z gorącym silnikiem — **sprzęt O-051** | 6 | ⬜ |
| **SYS-ENV-003a** | Riverdi RVT35HHBFWN00, czujnik temperatury na PCB HMI, zarządzanie jasnością | B | T-ENV-003a | Protokół: praca przy −20 i +70 °C otoczenia + osobna próba nasłonecznienia (pozycja O-034) | 6, 9 | ⬜ |
| **SYS-ENV-003b** | Dobór komponentów, arkusze kwalifikacji | — | T-ENV-003b | Zestawienie dla całego BOM: zakres z karty, miejsce na PCB, lokalny przyrost, margines. Odstępstwa wypisane osobno z zatwierdzeniem | 4 | ⬜ |
| SYS-ENV-004 | Dobór komponentów | — | T-ENV-004 | Zestawienie zakresów przechowywania z kart katalogowych całego BOM (analiza) | 4 | ⬜ |
| SYS-ENV-005 | Obudowa + złącze główne + złącze zapłonu + Deutsch DTM (HMI) | — | T-ENV-005 | Protokół próby zanurzeniowej 1 m / 30 min wg IP67 | 6 | ⬜ |
| SYS-ENV-006 | Mocowanie PCB, podparcie elementów ciężkich | — | T-ENV-006 | Profil wibracji przyjęty w Fazie 3 + protokół testu na wstrząsarce lub przejazd pomiarowy | 3 (profil), 9 (test) | ⬜ |
| **SYS-ENV-008** | TVS dwukierunkowy, dioda Schottky'ego na gałęzi logiki, ochrona PROFET | — | T-ENV-008 | Protokół: −14 V z zasilacza przez 60 s, potem pełny test funkcji; kontrola bezpiecznika | 6 | ⬜ |
| **SYS-ENV-009** | TVS dobrany na energię zrzutu, elementy wejściowe ≥ 40 V | — | T-ENV-009 | Obliczenie energii TVS (analiza) + próba 35 V / 400 ms z zasilacza o ograniczonym prądzie | 4, 6 | ⬜ |
| **SYS-ENV-010** | TVS + filtr LC wejścia | — | T-ENV-010 | Obliczenie energii impulsów 1 i 2a wobec charakterystyki TVS (analiza) + uproszczony test: rozłączanie cewki przekaźnika na linii zasilania, oscylogram na wejściu i kontrola pracy. Bez akredytowanego laboratorium (decyzja 18.10.2026) | 4, 6 | ⬜ |
| SYS-ENV-007 | MAX9926UAEE/V+ + HRTIM w STM32G474VET3 | C | T-ENV-007 | Protokół: generator sygnału VR, 200–10 000 obr/min, zliczanie zgubionych zębów | 6 | ⬜ |

### 20.2 Zapłon

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| ECU-IGN-001 | Blok AC-CDI, HRTIM | C | T-IGN-001 | Protokół: kąt zadany z mapy vs zmierzony na wyjściu drivera | 6 | ⬜ |
| **ECU-IGN-002** | Blok AC-CDI, HRTIM (**impuls generowany przez peryferium, nie przez program** — spec. FW B.2.3), MAX9926, STM32G474VET3 | C + I (priorytety przerwań) | **T-IGN-002** | **Histogram błędu z min. 10⁵ zapłonów, oscyloskop, przy jednoczesnej pracy logowania, CAN i USB. Test krytyczny dla bramki G2** | 6 | ⬜ |
| ECU-IGN-005 | Bramka tyrystora sprzężona pojemnościowo (B.2.3) | — (niezależne od FW) | T-IGN-005 | Wstrzykiwanie: wyjście HRTIM wymuszone w stan wysoki na stałe przy pracującym silniku/symulatorze — najwyżej jedna iskra; zamrożenie zegara HRTIM — jw. | 6 | ⬜ |
| ECU-IGN-006 | — | C | T-IGN-006 | Protokół: odcięcie i powrót przy zadanym progu, stanowisko + silnik | 6, 8 | ⬜ |
| ECU-IGN-006a | — | C + D (walidacja zakresu) + aplikacja | T-IGN-006a | Protokół: odrzucenie wartości spoza 50–500 obr/min po stronie aplikacji **i** po stronie ECU | 7 | ⬜ |
| **ECU-IGN-021** | Zasilanie logiki od 7 V (SYS-ENV-002), MAX9926, blok AC-CDI | C.1.8 | T-IGN-021 | Protokół: zasilacz laboratoryjny 7 V zamiast akumulatora, 10 prób rozruchu kopnięciem na zimnym silniku | 6, 8 | ⬜ |
| **ECU-IGN-022** | Estymata prędkości z korektą przyspieszenia (C.1.4), HRTIM | C.1.9a | T-IGN-022 | Model błędu (O-008) + oscylogram z niezależnym odniesieniem kąta: maksimum błędu (nie percentyl) przy hamowaniu i przyspieszaniu wału, min. 10⁵ zapłonów | 4, 6 | ⬜ |
| **ECU-IGN-023** | HRTIM: zdarzenie zewnętrzne ze zbocza MAX9926 jako start okresu; minimalna wartość rejestru porównania | C.1.9a | T-IGN-023 | Inspekcja konfiguracji + test: firmware zleca opóźnienie 0 i ujemne — iskra nie wcześniej niż 2° po zboczu | 4, 6 | ⬜ |
| **ECU-IGN-024** | Wejście przechwytywania timera na linii wyzwalania tyrystora | C.1.9a, B (DTC-IGN-06, -07) | T-IGN-024 | Wstrzykiwanie: przesunięte wyzwolenie (usterka) — tryb zastępczy po 1 zdarzeniu; symulowane hamowanie wału na generatorze VR — tryb zastępczy dopiero po 3/100; pojedyncze przekroczenie — tylko log | 6 | ⬜ |
| **ECU-IGN-025** | Blok AC-CDI | B.2.3 | T-IGN-025 | Oscylogram napięcia kondensatora (sonda 100:1) przy kopnięciu, jałowym, 3000, 6000, 9000 obr/min — ECU wobec fabrycznego CDI | 8 | ⬜ |
| **ECU-IGN-026** | Rezystor rozładowujący kondensator | B.2.3 | T-IGN-026 | Pomiar napięcia kondensatora sondą 100:1 po zgaszeniu silnika z 10 000 obr/min (najwyższe napięcie): ≤ 60 V po 5 s | 6 | ⬜ |
| **ECU-IGN-027** | Projekt PCB i dobór złącza | — | T-IGN-027 | Inspekcja odstępów wobec wyliczeń z pomiaru | 4 | ⬜ |
| **ECU-IGN-028** | Łańcuch pomiarowy kondensatora → ADC, wyzwalanie z HRTIM | B.2.3 | T-IGN-028 | Porównanie odczytu ECU z oscylogramem sondy 100:1 przy kopnięciu, jałowym i 9000 obr/min; rozwarcie łańcucha pomiarowego → DTC-IGN-09 | 6, 8 | ⬜ |
| **ECU-IGN-029** | Pomiar napięcia po zatrzymaniu wału | B.2.3 (DTC-IGN-10) | T-IGN-029 | Wstrzykiwanie: rozwarty łańcuch rozładowujący → DTC-IGN-10 po 5 s; test negatywny: kopnięcie albo toczenie w trakcie 5 s — brak alarmu | 6 | ⬜ |
| **ECU-IGN-030** | Footprint drivera TCI + wspólny kanał HRTIM | — | T-IGN-030 | Przegląd schematu: oba stopnie (AC-CDI, TCI) na tym samym kanale, obsadzenie zależne od wariantu; próba na cewce TPI/TBI | 4, 8 | ⬜ |
| **ECU-IGN-031** | Driver z miękkim wyłączeniem | B.2.3 | T-IGN-031 | Wstrzykiwanie: kill switch, ENDRV, reset i zanik szyny w 5 fazach ładowania — brak iskry (oscylogram wtórnego) | 6 | ⬜ |
| **ECU-IGN-032** | Sprzętowy ogranicznik czasu w ścieżce sterowania drivera | — | T-IGN-032 | Wstrzykiwanie: wyjście HRTIM zawieszone w stanie aktywnym, zamrożony zegar — prąd cewki wygaszony po czasie sufitu, bez iskry | 6 | ⬜ |
| **ECU-IGN-033** | Ścieżka ciepła drivera do obudowy | — | T-IGN-033 | Komora w maksymalnej temperaturze otoczenia (SYS-ENV-003), maksymalne obroty B/C — temperatury NTC i AIS2IH | 6, 8 | ⬜ |
| **ECU-IGN-020** | — (brak TPS w MVP-A) | C + D | T-IGN-020 | Przegląd struktury mapy: jedna oś, obroty (inspekcja) + protokół na stanowisku potwierdzający, że kąt zależy wyłącznie od obrotów | 5, 6 | ⬜ |
| **ECU-IGN-012** | **Koło magnesowe Beta 300 RR: 1 wypust, 30°, krawędź spływu w GMP** (zmierzone) + MAX9926 | C.1.1 + G (kalibracja) | T-IGN-012 | Przegląd struktur danych: geometria jako parametr kalibracyjny, nie stała (inspekcja) + test z podmienioną geometrią na stanowisku | 5, 6 | ⬜ |
| **ECU-IGN-013** | HRTIM + wejście przechwytujące w STM32G474VET3 | C.1.3 | T-IGN-013 | Protokół: generator sygnału VR z wymuszonym przyspieszaniem i zwalnianiem; porównanie modelu kąta z sygnałem odniesienia | 6 | ⬜ |
| **ECU-IGN-014** | MAX9926 + przechwytywanie obu krawędzi wypustu | C.1.4 | T-IGN-014 | Protokół: porównanie estymaty z interwału wypustu i ze średniej z obrotu wobec sygnału odniesienia, przy niskich obrotach z tętnieniem | 6 | ⬜ |
| **ECU-IGN-015** | — (niezależne od mapy) | C.1.9 + D (walidacja) | T-IGN-015 | Protokół: mapa zadająca 35° — potwierdzenie ograniczenia do 28° i zapisu zdarzenia | 6 | ⬜ |
| **ECU-IGN-016** | — | C.2 + D | T-IGN-016 | Protokół strojenia z obserwacją detonacji; kryterium: brak detonacji przy pełnym obciążeniu w całym zakresie | 8 | ⬜ |
| **ECU-IGN-017** | Filtr cyfrowy wejścia + adaptacyjny próg MAX9926 + bramkowanie programowe | C.1.6 | T-IGN-017 | **Protokół wstrzykiwania zakłóceń:** impulsy imitujące zbocze w fazie, w której wypust nie może wystąpić — potwierdzenie, że są odrzucone **i że iskra nie została utracona**. Osobno test negatywny: brak odrzucania ważnych zboczy przy gwałtownym przyspieszaniu | 6, 8 | ⬜ |
| **ECU-IGN-018** | Jw. | C.1.7 | T-IGN-018 | Protokół: naruszenie każdego z trzech kryteriów osobno; kontrola klasy reakcji (K0 pojedyncze, K4 powtarzalne) | 6 | ⬜ |
| **ECU-IGN-019** | HRTIM wyzwalany zboczem spływu (MAX9926) po potwierdzeniu kierunku | C.1.8 | T-IGN-019 | Protokół: rozruch kopnięciem z oscylogramem — pierwsza iskra dopiero po potwierdzeniu obrotu do przodu, w GMP; **kopnięcie z cofnięciem wału przez wypust — brak iskry**; osobno **restart w ruchu** z potwierdzeniem natychmiastowej iskry z mapy | 6, 8 | ⬜ |
| ECU-IGN-007 | — | D | T-IGN-007 | Przegląd formatu mapy w specyfikacji struktur danych (inspekcja) | 3 | ⬜ |

### 20.3 Wtrysk

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| ECU-INJ-001 | TLE9104SHXUMA1 (2 z 4 kanałów) | C | T-INJ-001 | Protokół obciążeniowy: prąd ciągły 1,5 A/kanał, temperatura układu | 6 | ⬜ |
| ECU-INJ-002 | TLE9104SHXUMA1 | C | T-INJ-002 | Oscylogram prądu na wtryskiwaczu wzorcowym 11,7 Ω oraz skrajnych 10,5 i 13,0 Ω | 6 | ⬜ |
| ECU-INJ-003 | Timer w STM32G474VET3 | C | T-INJ-003 | Pomiar szerokości impulsu na wyjściu drivera: rozdzielczość i powtarzalność | 6 | ⬜ |
| ECU-INJ-004 | Pomiar VBAT | C + D (tabela korekt) | T-INJ-004 | Pomiar czasu martwego na fizycznym wtryskiwaczu w funkcji napięcia (F-014) | 6 | ⬜ |
| **ECU-INJ-007** | — | C + B (B.3.2) | T-INJ-007 | Protokół: wymuszona usterka TPS na stanowisku, pomiar składu mieszanki analizatorem spalin przy otwartej przepustnicy; potwierdzenie, że mieszanka jest bogata, nie uboga | 6, 8 | ⬜ |
| ECU-INJ-005 | BTS7008-2EPA (kanał pompy) | A.3 | T-INJ-005 | Oscylogram załączenia pompy przy wejściu w stan GOTOWOŚĆ | 6 | ⬜ |
| ECU-INJ-006 | BTS7008-2EPA | B | T-INJ-006 | Protokół: brak obrotów → wyłączenie pompy w zadanym czasie | 6 | ⬜ |

### 20.4 Czujniki

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
| **ECU-SEN-016** | Infineon KP464 (SPI) + membrana obudowy | E (DTC-SEN-08), F | T-SEN-016 | Protokół: porównanie z barometrem wzorcowym w temperaturze pokojowej i w komorze (−40 / +50 °C); kontrola, że ECU zamknięte z membraną mierzy to samo co otwarte | 6 | ⬜ |
| ECU-SEN-011 | Pomiar szyny 5 V przez ADC | C | T-SEN-011 | Protokół: wymuszona zmiana napięcia szyny, potwierdzenie stałości wskazania TPS | 6 | ⬜ |

### 20.5 Zasilanie i tryb uśpienia

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| ECU-PWR-001 | Architektura uśpienia (`produkt.md` rozdz. 6): szyny 3,3 V i 5 V wyłączane przez INH TJA1043, w uśpieniu czuwa tylko transceiver; bilans ≤ 63 µA (rozdz. 6.1) | A | T-PWR-001 | Protokół pomiaru prądu (miernik z zakresem µA) przy 12,0 V i +25 °C | 6 | ⬜ |
| SYS-PWR-002 | Jw. + uśpienie HMI (7.1) | A + J | T-PWR-002 | Protokół pomiaru prądu całego zestawu | 6 | ⬜ |
| ECU-PWR-003 | — | A + A.4 | T-PWR-003 | Oscylogram: zbocze źródła wybudzenia → pierwszy impuls na wyjściu drivera zapłonu | 6 | ⬜ |
| ECU-PWR-003a | — | A + B (B.2.5) | T-PWR-003a | Protokół: czas i zakres autotestu pełnego vs skróconego, log przyczyny wyboru; pomiar czasu sumy kontrolnej map | 6 | ⬜ |
| ECU-PWR-004 | — | A | T-PWR-004 | Protokół: pomiar czasu do zaśnięcia, 10 powtórzeń | 6 | ⬜ |
| HMI-PWR-005 | Sterowanie podświetleniem przez BT817Q | J | T-PWR-005 | Protokół: pomiar czasu wygaszenia | 6 | ⬜ |
| ECU-PWR-006 | PMIC: VDD5 stałe, VDD3/5 wybierane pinem SEL_VDD3/5, VSOUT1 śledzi VDD5 (brak DAC i potencjometru cyfrowego) | — | T-PWR-006 | Przegląd schematu: potwierdzenie braku ścieżki sterowania nastawą z MCU (inspekcja) | 4 | ⬜ |
| ECU-PWR-007 | ADC szyn + rejestry statusu PMIC | B | T-PWR-007 | Protokół: wymuszone zaniki i przeciążenia szyn, kontrola reakcji | 6 | ⬜ |
| ECU-PWR-008 | PMIC: VDD5 o stałej nastawie | — | T-PWR-008 | Protokół: pomiar napięcia przy skrajnym obciążeniu i w skrajnych temperaturach | 6 | ⬜ |
| **ECU-PWR-008b** | PMIC: VSOUT1 w trybie śledzenia VDD5 + ADC VSOUT1 | — | T-PWR-008b | Protokół: pomiar VSOUT1 przy obciążeniu 0 i maks. z listy czujników, w skrajnych temperaturach i przy 7 V na złączu; kontrola odczytu ratiometrycznego przy celowo zmienionym VSOUT1 | 6 | ⬜ |
| **ECU-PWR-008a** | ADC VDD5 i VSOUT1 + flagi UV/OV PMIC | B (B.2.4) | T-PWR-008a | Protokół: regulowane osobno VDD5 (4,3–5,6 V) i VSOUT1 (4,3–5,7 V); potwierdzenie reakcji i **poprawnej przyczyny w logu**; **test negatywny: skoki obciążenia VDD5 (nadawanie CAN, start MAX9926) bez fałszywego opadnięcia ENDRV** | 6 | ⬜ |
| **ECU-PWR-009** | Pomiar VBAT + BTS7008-2EPA (kanał wentylatora) | B (DTC-PWR-07) | T-PWR-009 | Protokół: podanie 17 V z zasilacza laboratoryjnego, potwierdzenie ostrzeżenia i załączenia wentylatora; kontrola histerezy przy zejściu poniżej 15,5 V | 6 | ⬜ |
| **ECU-PWR-010** | VSOUT1 PMIC + ADC szyny czujników | B (DTC-PWR-10) | T-PWR-010 | Protokół: wymuszone rozwarcie przełącznika, potwierdzenie blokady wyjścia ze stanu GOTOWOŚĆ po 3 próbach | 6 | ⬜ |
| **ECU-PWR-011** | Przełącznik zasilania HMI domyślnie załączony | A.4, J | T-PWR-011 | Protokół: uśpienie ECU — HMI zasilane, przycisk HMI budzi system; ECU odłącza i ponownie załącza HMI; zwarcie kabla HMI — ochrona, ECU pracuje dalej (SYS-COM-008); pomiar prądu przełącznika w uśpieniu | 6 | ⬜ |

### 20.6 Bezpieczeństwo

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| **ECU-SAF-001** | Sprzętowo sygnałem kill switcha, **dwa osobne układy progowe**: próg tranzystorowy → **zwarcie uzwojenia wzbudzającego**; komparator → **blokada impulsu bramką AND** (AC-CDI, 1.11.2026); **w B/C wtrysk także dwiema ścieżkami: komparator → EN TLE9104, próg tranzystorowy → RESN TLE9104** (decyzja Pawła 1.11.2026) | B | **T-SAF-001** | **Test wstrzykiwania usterki: zawieszony firmware z aktywnymi wyjściami, rozwarcie kill switcha, pomiar czasu do odcięcia. Test krytyczny dla bramki G2** | 6 | ⬜ |
| ECU-SAF-002 | **Układ trzypoziomowy: rezystory w wiązce przy przycisku + podciągnięcie w ECU + komparator bramkujący** | B (B.2.5.1) + E | T-SAF-002 | Protokół: trzy przypadki — naciśnięcie przycisku, przecięcie przewodu, rozłączenie wtyczki. W każdym kontrola odcięcia **oraz** poprawności rozróżnienia w logu i komunikacie | 6 | ⬜ |
| **ECU-SAF-002a** | Jw. | B | T-SAF-002a | Protokół: pomiar czasu od zmiany stanu do zgłoszenia usterki, kontrola odporności na drgania styku | 6 | ⬜ |
| **ECU-SAF-024** | ADC wejścia kill + odczyt zwrotny wyjść komparatora i progu tranzystorowego | B.2.5.1 (DTC-SAF-08) | T-SAF-024 | Wstrzykiwanie: wymuszenie wyjścia każdego progu w RUN przy wciśniętym przycisku i odłączenie wejścia ADC — DTC-SAF-08 w ≤ 100 ms, odcięcie sprzętowe działa | 6 | ⬜ |
| **ECU-SAF-025** | ADC wejścia kill, dolna granica poziomu RUN | B.2.5.1 (DTC-SAF-07) | T-SAF-025 | Wstrzykiwanie: zwarcie przewodu kill do masy i rozwarcie R_pull — DTC-SAF-07 i ostrzeżenie, silnik pracuje | 6 | ⬜ |
| ECU-SAF-003 | Watchdog PMIC TPS65381A-Q1 (NRES + ENDRV) + rezystory ściągające | B | T-SAF-003a / T-SAF-003b | Protokół: wymuszony reset watchdoga przy pracującym silniku, potwierdzenie braku samoczynnego startu. **Dwa warianty** — odblokowanie kill switchem (a) i odblokowanie z HMI (b); obie drogi muszą przechodzić przez ten sam warunek zatrzymania wału | 6 | ⬜ |
| ECU-SAF-004 | Detektor brown-out w MCU + nadzór UV szyn w PMIC (NRES) | B | T-SAF-004 | Protokół: zapad napięcia poniżej progu, ten sam zatrzask co T-SAF-003 | 6 | ⬜ |
| ECU-SAF-005 | AIS2IH | B (B.2.5.4) | T-SAF-005 | Protokół: obrót zestawu na stanowisku (próg 65°, czas 3 s) + **test negatywny: spadek swobodny i uderzenie przy kącie > 65° nie mogą doliczyć czasu** + **rejestracja kąta przechyłu podczas sesji jazdy w terenie, z hopami**; kryterium zaliczenia: zero fałszywych zadziałań | 6, 8 | ⬜ |
| ECU-SAF-006 | Licznik w pamięci nieulotnej (W25Q64) | B | T-SAF-006 | Protokół: 3 wymuszone resety → stan awarii; weryfikacja zerowania dopiero po 60 s pracy silnika | 6 | ⬜ |
| **ECU-SAF-006a** | W25Q64 + rejestry domeny podtrzymywanej (superkondensator) | B (B.2.5.3) | T-SAF-006a | Protokół: wymuszony reset watchdoga, odczyt migawki aplikacją desktop, kontrola kompletu pól; powtórzenie 3× i kontrola, czy zachowane są 3 ostatnie migawki | 6 | ⬜ |
| **ECU-SAF-006b** | Rejestr domeny podtrzymywanej | I (lista zadań) + B | T-SAF-006b | Przegląd kodu: każde zadanie czasu rzeczywistego zapisuje identyfikator przy wejściu (inspekcja) + test: zawieszenie wybranego zadania i kontrola, czy migawka wskazuje właśnie je | 5, 6 | ⬜ |
| **ECU-SAF-012** | W25Q64 (suma kontrolna map) | B (B.2.5.2) | T-SAF-012 | Protokół: celowe uszkodzenie bajtu w mapach, kontrola blokady startu i treści komunikatu | 6 | ⬜ |
| **ECU-SAF-012a** | W25Q64 (suma kontrolna konfiguracji) | B (B.2.5.2) | T-SAF-012a | Protokół: celowe uszkodzenie bajtu w konfiguracji użytkownika, potwierdzenie **uruchomienia silnika** na wartościach domyślnych z ostrzeżeniem | 6 | ⬜ |
| ECU-SAF-007 | Rezystory ściągające na wszystkich wyjściach mocy | — | T-SAF-007 | Oscylogram stanu wyjść od chwili podania zasilania do końca startu MCU | 6 | ⬜ |
| **ECU-SAF-016** | **Rezystory ściągające na linii bramkującej EN** driverów | — (niezależne od FW) | T-SAF-016 | Protokół wstrzykiwania usterki: odłączenie zasilania komparatora przy pracującym silniku — potwierdzenie odcięcia, nie załączenia. Osobno: oscylogram stanu linii EN od chwili podania zasilania | 6 | ⬜ |
| **ECU-SAF-021** | Dzielnik napięcia uzwojenia wzbudzającego → ADC; odczyt zwrotny wyjść **obu układów progowych** | B (DTC-SAF-06) | T-SAF-021 | Wstrzykiwanie: rozwarcie elementu zwierającego wzbudzające, zablokowanie bramki AND w stanie przepuszczania, każdy próg zablokowany w RUN osobno — w każdym przypadku DTC-SAF-06 przy najbliższym zgaszeniu, silnik i tak gaśnie | 6 | ⬜ |
| **ECU-SAF-022** | Klucz masy cewki przekaźnika: przycisk START × próg tranzystorowy; PROFET: procesor × komparator | — (niezależne od FW) | T-SAF-022 | Wstrzykiwanie: (1) zwarte wyjście PROFET — rozrusznik rusza tylko przy wciśniętym START i RUN; (2) zwarty klucz masy — rusza tylko na polecenie firmware przy RUN; (3) w STOP stoi przy każdym pojedynczym zwarciu; (4) każdy próg zablokowany w RUN osobno — STOP nadal zatrzymuje | 6 | ⬜ |
| **ECU-SAF-023** | MPU: rejestry HRTIM tylko dla modułu zapłonu | B.1.3 (DTC-SYS-11) | T-SAF-023 | Wstrzykiwanie: zapis do rejestru wymuszenia wyjścia HRTIM z zadania obsługi CAN — wyjątek przed zapisem, brak iskry na oscylogramie, DTC-SYS-11 | 4, 6 | ⬜ |
| **ECU-SAF-020** | 2× NTC (AEC-Q200) przy bloku CDI i w sekcji mocy + czujnik temperatury MCU | B (DTC-PWR-11…14) | T-SAF-020 | Protokół: podgrzewanie zestawu do T1/T2/T3 z kontrolą reakcji; **testy negatywne:** zwarcie i przerwa NTC przy pracującym silniku — brak zgaszenia; pojedynczy czujnik powyżej T3 — brak zgaszenia | 6 | ⬜ |
| **ECU-SAF-019** | Bramkowanie wejścia PROFET rozrusznika sygnałem kill switcha | — (niezależne od FW) | T-SAF-019 | Test wstrzykiwania usterki: firmware wymusza załączenie rozrusznika przy kill switchu w STOP — rozrusznik nie może ruszyć | 6 | ⬜ |
| **ECU-SAF-018** | Pin WAKE TJA1043 + wejście przycisku startu w MCU + BTS7008-2EPA (kanał rozrusznika) | A.3b, A.4 | T-SAF-018 | Protokół: start z uśpienia przyciskiem trzymanym (rozrusznik rusza po gotowości), puszczonym przed gotowością (brak rozrusznika), trzymanym przy kill switchu w STOP (brak rozrusznika) | 6 | ⬜ |
| **ECU-SAF-017** | Watchdog w PMIC — w uśpieniu bez zasilania razem z szynami (IGN z INH TJA1043), bez linii wyłączającej nadzór | A.4 | T-SAF-017 | Przegląd schematu (inspekcja) + test: w każdym stanie z zasilonym procesorem, łącznie ze startem, brak obsługi WDI powoduje reset | 4, 6 | ⬜ |
| **ECU-SAF-016a** | Komparator zasilany z VDD5 PMIC | — | T-SAF-016a | Przegląd schematu (inspekcja) + pomiar prądu spoczynkowego w T-PWR-001 potwierdzający brak wpływu komparatora | 4, 6 | ⬜ |
| ECU-SAF-008 | BTS7008-2EPA (kanał rozrusznika) | B + A.3b | T-SAF-008 | Protokół: próba załączenia rozrusznika przy obrotach > 400 obr/min, potwierdzenie blokady | 8 | ⬜ |
| ECU-SAF-009 | BTS7008-2EPA | A.3b | T-SAF-009 | Protokół: pomiar czasu ciągłej pracy rozrusznika | 6 | ⬜ |
| ECU-SAF-010 | BTS7008-2EPA | A.3b | T-SAF-010 | Protokół: pomiar obrotów w chwili wyłączenia rozrusznika | 8 | ⬜ |
| ECU-SAF-010a | — | D (walidacja parametrów) | T-SAF-010a | Przegląd kodu i zestawu parametrów: potwierdzenie warunku 700 > 400 (inspekcja) | 5 | ⬜ |
| ECU-SAF-011 | — | B (B.5) + aplikacja | T-SAF-011 | Protokół: próba zmiany parametru spoza listy dozwolonych; próba zapisu w obszarze zablokowanym (> 5000 obr/min i > 60% przepustnicy jednocześnie) oraz tuż poza nim; próba przekroczenia limitu 2°/5% na zapis. **Weryfikacja odrzucenia po stronie ECU przy pominiętej aplikacji** | 7 | ⬜ |
| **ECU-SAF-011a** | — | B (B.5.4) | T-SAF-011a | Protokół: wymuszenie każdego z czterech wyzwalaczy przerwania sesji; kontrola powrotu map do wartości trwałych i spójności pamięci nieulotnej | 7 | ⬜ |
| **ECU-SAF-013** | — | B (B.3.3) | T-SAF-013 | Oscylogram: wymuszenie usterki K3 przy 8000 obr/min, pomiar przebiegu zjazdu limitu w czasie | 6 | ⬜ |
| **ECU-SAF-014** | — | B (B.3.1) | T-SAF-014 | Protokół: dwie jednoczesne usterki K3 o różnych limitach, potwierdzenie obowiązywania niższego bez sumowania | 6 | ⬜ |

### 20.7 Diagnostyka i logowanie

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| ECU-DIA-001 | W25Q64 + RTC w STM32G474VET3 | E | T-DIA-001 | Protokół: wymuszenie każdej usterki z macierzy, kontrola kompletu pól rekordu | 6 | ⬜ |
| ECU-DIA-002 | — | E | T-DIA-002 | Przegląd macierzy usterek: każda pozycja ma przypisaną klasę (inspekcja) | 5 | ⬜ |
| ECU-DIA-003 | TJA1043 | E | T-DIA-003 | Protokół: odłączenie HMI, pomiar czasu do zapisania zdarzenia | 6 | ⬜ |
| ECU-DIA-004 | — | A.4 + F | T-DIA-004 | Protokół: wybudzenie z każdego źródła, kontrola zapisanej przyczyny | 6 | ⬜ |
| ECU-LOG-005 | W25Q64 (8 MB — zapas na przyszłe rozszerzenie) | F | T-LOG-005 | Przegląd zakresu logowania względem karty MVP (inspekcja) | 5 | ⬜ |
| ECU-LOG-006 | W25Q64 + AIS2IH (±16 g) | F | T-LOG-006 | Protokół: wyzwolenie zdarzenia, odczyt okna przed i po | 6 | ⬜ |
| ECU-LOG-007 | Kondensator buforowy na szynie 3,3 V | F | T-LOG-007 | Protokół: przerwanie zasilania w losowym momencie zapisu, min. 100 powtórzeń, brak uszkodzonego rekordu | 6 | ⬜ |
| ECU-LOG-008 | W25Q64 (zapis atomowy) | F | T-LOG-008 | Jw., kontrola licznika motogodzin po każdym przerwaniu | 6 | ⬜ |

### 20.8 Komunikacja

| Wymaganie | Realizacja sprzętowa | Moduł FW | ID testu | Dowód | Faza | Status |
|---|---|---|---|---|---|---|
| SYS-COM-001 | TJA1043 ×2, terminacja (6.2c) | A, J | T-COM-001 | Protokół: analizator CAN, jakość sygnału i stopa błędów przy pracującym zapłonie | 6 | ⬜ |
| SYS-COM-001a | — | H | T-COM-001a | Protokół: pomiar czasu aktualizacji firmware HMI przez CAN | 7 | ⬜ |
| SYS-COM-002 | — | Protokół (Faza 2-Desktop) | T-COM-002 | Przegląd definicji ramek + test odbioru ramki z błędną sumą kontrolną | 6 | ⬜ |
| SYS-COM-002a | — | I (harmonogram zadań) | T-COM-002a | Protokół: pomiar odstępów między ramkami analizatorem CAN, histogram | 6 | ⬜ |
| SYS-COM-002b | — | I | T-COM-002b | Jw. dla ramek wolnozmiennych | 6 | ⬜ |
| SYS-COM-003 | — | Protokół (Faza 2-Desktop) | T-COM-003 | Protokół wstrzykiwania błędów: ramki zgubione, powtórzone, przekłamane | 6 | ⬜ |
| SYS-COM-004 | — | Protokół (Faza 2-Desktop) | T-COM-004 | Przegląd specyfikacji protokołu: każda ramka cykliczna ma okres i timeout (inspekcja) + test negatywny: usunięcie jednej ramki z magistrali nie wywołuje usterki, usunięcie trzech kolejnych — wywołuje | 2-Desktop | ⬜ |
| **SYS-COM-008** | — | A.4, B (DTC-COM-01) | T-COM-008 | Protokół: odłączone HMI — start z uśpienia przyciskiem, praca silnika, zaśnięcie po 30 min; to samo przy HMI zawieszonym (nadaje śmieci lub nic) | 6 | ⬜ |
| **ECU-BTL-001** | Kontrola warunków w bootloaderze i aplikacji ECU | H | T-BTL-001 | Protokół: próba aktualizacji przy każdym niespełnionym warunku osobno (kill switch RUN, impulsy VR, 11,5 V) — odmowa; utrata warunku w trakcie — przerwanie i praca na starym banku | 7 | ⬜ |
| **ECU-BTL-002** | ECU-SAF-001, ECU-SAF-019 | H | T-BTL-002 | Oscylogram wyjść zapłonu i rozrusznika od startu bootloadera do startu aplikacji: brak impulsu | 7 | ⬜ |
| **ECU-BTL-003** | Dwubankowa Flash STM32G474 / STM32G0B1 | H | T-BTL-003 | Przerwanie zasilania w losowym momencie aktualizacji, min. 20 prób — ECU zawsze startuje | 7 | ⬜ |
| **ECU-BTL-004** | Sprzętowy CRC STM32G4 | H | T-BTL-004 | Obraz z jednym przekłamanym bajtem i obraz niezgodnej wersji — odrzucone | 7 | ⬜ |
| **ECU-BTL-005** | Licznik startów w pamięci nieulotnej | H | T-BTL-005 | Obraz celowo nieprzechodzący autotestu — powrót do poprzedniego banku po 3 startach | 7 | ⬜ |
| **ECU-BTL-006** | Ochrona zapisu sektorów bootloadera (option bytes) | H | T-BTL-006 | Inspekcja konfiguracji + próba zapisu sektora bootloadera z aplikacji — odrzucona | 7 | ⬜ |
| **SYS-COM-007** | TJA1043 ×2 | A.4 + J | T-COM-007 | Protokół: wybudzenie ECU każdym ze źródeł, kontrola czy HMI budzi się bez interakcji kierowcy z wyświetlaczem | 6 | ⬜ |
| SYS-COM-005 | — | H | T-COM-005 | Protokół: połączenie niezgodnych wersji, kontrola wykrycia i komunikatu | 7 | ⬜ |
| **SYS-COM-005a** | — | J (HMI) | T-COM-005a | Protokół: połączenie wersji różniących się o `minor` **i** o `major`; w obu przypadkach ekran bez danych pomiarowych | 7 | ⬜ |
| **SYS-COM-005b** | — | H | T-COM-005b | Protokół: aktualizacja pakietem zawierającym oba obrazy; przerwanie w losowym momencie i kontrola, czy zestaw wraca do spójnej pary wersji | 7 | ⬜ |
| **SYS-COM-009** | Ramka identyfikacji HMI | J | T-COM-009 | Protokół: dwa egzemplarze HMI z różnymi rezystorami rewizji — ECU zapisuje w logu i pokazuje w aplikacji poprawny model i rewizję | 7 | ⬜ |
| APP-COM-006 | — | D + H + aplikacja | T-COM-006 | Protokół: przerwanie zapisu w losowym momencie, min. 50 powtórzeń, kontrola spójności konfiguracji | 7 | ⬜ |

### 20.9 Interfejs użytkownika

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

### 20.10 Bilans pokrycia

*Liczby skorygowane 22.09.2026. Wcześniejsze wersje bilansu podawały wartości zaniżone — skrypt kontrolny nie obejmował wymagań obszaru **UI**, bo jego wzorzec zakładał trzyliterowy kod obszaru, a `HMI-UI-xxx` ma dwuliterowy. Same wiersze w tabeli były obecne; błędna była kontrola, nie pokrycie.*

| Pozycja | Liczba |
|---|---|
| Wymagań w tego dokumentu | 105 |
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

### 20.11 Funkcje w zakresie bez wymagania — luka wykryta przy przebudowie tabeli

Przebudowa ujawniła funkcje obecne w zakresie produktu (rozdz. 4.1) i w poprzedniej tabeli pokrycia, które **nie mają żadnego wymagania w tego dokumentu**. Bez wymagania nie da się ich zweryfikować — nie wiadomo, co miałoby zostać udowodnione.

| Funkcja | Źródło zakresu | Brakujące wymagania | Priorytet |
|---|---|---|---|
| ~~Quickshifter~~ | Faza 0 | ❌ **USUNIĘTY Z ZAKRESU 29.09.2026** — funkcja wypadła z produktu wraz z wymaganiami i czujnikami. Pozycja przestała istnieć zamiast zostać domknięta | — |
| ~~Bootloader i aktualizacja firmware~~ | Faza 0, zasada procesu #12 | ✅ **Wymagania zapisane 25.10.2026: ECU-BTL-001…006** (rozdz. 10a) | ~~P0~~ |
| Sterowanie wentylatorem | Faza 0 | Progi załączenia i wyłączenia, histereza, reakcja na usterkę czujnika temperatury, praca po zgaszeniu silnika | P1 |
| Przełączanie map z HMI | Faza 0 | Liczba profili, warunki dopuszczające zmianę (obroty, praca silnika), czas przełączenia | P1 |
| Licznik przebiegu (km) | Faza 0 | Rozdzielczość, odporność na zanik zasilania, zakres | P1 |
| Korekta na wysokość n.p.m. | Faza 0, KP464 (w MVP-A tylko logowanie) | Zakres korekty, częstotliwość aktualizacji, zachowanie przy usterce czujnika | P1 |
| Aplikacja desktop (poza APP-COM-006) | Faza 0 | Cały obszar APP-*: edycja map, podgląd na żywo, odczyt kodów usterek, wymagania wydajnościowe | P1 — do ustalenia w Fazie 2-Desktop |
| Sterowanie światłami | Faza 0 | Obciążalność kanału, zachowanie przy przeciążeniu, sterowanie z HMI | P2 |
| Zegar czasu rzeczywistego | Faza 0 | Dokładność, podtrzymanie przy odłączonym akumulatorze, źródło synchronizacji | P2 |
| Konfigurator wyglądu HMI | Faza 0 | Zakres konfigurowalności, format, walidacja | P2 |

**Stan na 29.09.2026:** quickshifter usunięty z zakresu, więc jego pozycja P0 przestała istnieć. **Pozostawała jedna pozycja P0 — bootloader; wymagania zapisane 25.10.2026 (ECU-BTL-001…006). Pozycji P0 bez wymagań nie ma.**

**Decyzja procesowa:** pozycje P0 muszą uzyskać wymagania **przed bramką G0**, razem z domykaniem pozycji `[DO USTALENIA]`. Pozycje P1 i P2 powstają w naturalnym miejscu procesu — przy punktach B, C, D i H specyfikacji firmware oraz w Fazie 2-Desktop — ale ich brak jest od teraz jawnie śledzony w tej tabeli, zamiast być odkrywanym na końcu.

Ta luka jest dokładnie tym, przed czym ostrzegała pozycja audytu F-012: poprzednia tabela wychodziła od nazw funkcji, więc każda funkcja „miała wiersz" i wyglądała na pokrytą, mimo że nie stało za nią żadne sprawdzalne wymaganie.
