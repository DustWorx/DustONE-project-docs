# Produkt — ECU „Dust ONE"

Co budujemy, jak to jest zbudowane i dlaczego tak. Pozycje nierozstrzygnięte są w `otwarte.md`, wymagania w `wymagania.md`, firmware w `firmware.md`.

**Uzasadnienia są częścią treści.** Przy każdej decyzji zapisane jest, co odrzucono i dlaczego — bez tego decyzja wraca co kilka tygodni jako „a może inaczej".

---

## 1. Zakres

Samodzielna, programowalna jednostka sterująca silnika do motocykli enduro i adventure, moduł wyświetlacza na kierownicę oraz aplikacja desktop do strojenia i diagnostyki. **Motorsport i entuzjaści offroadu; urządzenie nie jest i nie będzie homologowane drogowo.**

**Zakres docelowy: wyłącznie silniki 1-cylindrowe (2T i 4T) motocykli enduro** — platforma KTM / Husqvarna / GasGas oraz Beta. Warianty rozróżnia **układ paliwowy**, nie model motocykla.

| Wariant | Układ paliwowy | Zakres sterowania |
|---|---|---|
| **MVP-A** — gaźnik | Gaźnik, bez sterowania mieszanką. Motocykl rozwojowy: **Beta 300 RR 2015**, 1-cyl. 2T, **bez TPS** | Zapłon (mapa jednowymiarowa, kąt w funkcji obrotów), ogranicznik obrotów, wskaźnik biegu, prędkość i przebieg, motogodziny, wyjścia mocy, diagnostyka |
| B — TPI | **Transfer Port Injection** — 2 wtryskiwacze do kanałów przepłukujących | Dodatkowo wtrysk paliwa |
| C — TBI | **Throttle Body Injection** — 1 wtryskiwacz w gardzieli | Dodatkowo wtrysk paliwa |

⚠️ **Korekta 15.10.2026.** Wcześniejsze wydania tego dokumentu oraz dossier przekazane do audytu zewnętrznego podawały dla wariantów B i C konkretne motocykle odniesienia, w tym **KTM 890 Adventure dla wariantu C, z przepustnicą sterowaną elektronicznie**. Było to nieprawdziwe: motocykli odniesienia dla B i C nigdy nie ustalono, a KTM 890 Adventure występuje w dokumencie źródłowym **wyłącznie jako przykład konstrukcji odrzuconej** (decyzja 0.2 — silniki 2-cylindrowe i ride-by-wire poza zakresem). Audyt AUD-ECU-002 pracował na tym błędnym opisie zakresu.

**Projektowany jest wyłącznie MVP-A.** Warianty B i C mają zarezerwowane zdolności sprzętowe (wymagania `[HW]` i `[B/C]`), ale nie mają własnych specyfikacji ani odbiorcy.

### 1.1 Czego produkt nie robi

| Funkcja | Powód |
|---|---|
| **Quickshifter i czujnik sprzęgła** | Usunięte. Najgorszy stosunek złożoności do wartości: 9 wymagań, 3 kody usterek, 2 komponenty, 2 piny. **Jedyna funkcja wymagająca wnioskowania o intencji kierowcy** zamiast o mierzalnym stanie — stąd trzy kolejne błędy specyfikacji. W technicznym terenie sprzęgło jest w ciągłym użyciu, więc realna wartość jest niska. Zwolnione dwa piny przechodzą do bilansu |
| **Blokada rozrusznika na biegu** | Odpowiedzialność po stronie kierowcy, jak w części motocykli sportowych. Czujnik sprzęgła jako warunek rozruchu mógłby przy awarii przełącznika w klamce unieruchomić motocykl w terenie. Wymaga ostrzeżenia w instrukcji |
| **Automatyczne ograniczenie mocy przy przegrzaniu silnika** | Tylko ostrzeżenie na HMI. W zawodach automatyczna redukcja mocy może być groźniejsza od przegrzania — decyzja o zatrzymaniu należy do kierowcy, który widzi sytuację |
| **Regulacja napięcia szyn przez mikrokontroler** | Patrz rozdz. 4.2 — błąd firmware mógłby zniszczyć czujniki i sam procesor |
| Pełne logowanie sesji jazdy | Zawężone do czarnej skrzynki (zdarzenia krytyczne). Ograniczenie w firmware, nie w sprzęcie — 8 MB daje zapas |
| Sygnalizacja stanu na samym ECU | Brak diody. Diagnostyka wyłącznie przez HMI i aplikację |
| **Silniki 2-cylindrowe i ride-by-wire** (np. KTM 890 Adventure) | Decyzja 0.2 Fazy 0. Ride-by-wire to osobna kategoria inżynierska — redundantne czujniki i failsafe. **Żaden wariant produktu ich nie obejmuje** |
| Closed-loop lambda, EGT, czujnik spalania stukowego | Poza MVP |
| Sterowanie pompką olejową | Pompka usuwana, przejście na premiks |
| Launch control, kontrola trakcji | Poza MVP. Sprzętowo możliwe do dodania później — wymagają tylko istniejących wejść |

---

## 2. Decyzje architektoniczne

| # | Decyzja | Wybór | Uzasadnienie |
|---|---|---|---|
| 2.1 | Zasilanie | Logika ECU wyłącznie z akumulatora 12 V; **energia zapłonu w MVP-A z uzwojenia wzbudzającego statora** (decyzja 2.9) | Pierwotnie decyzja wykluczała obsługę napięcia przemiennego ze statora. Zmieniona 18.10.2026: ECU nadal nie zasila się ze statora, ale prowadzi i prostuje napięcie uzwojenia wzbudzającego do kondensatora zapłonowego |
| 2.2 | Standalone | Bez fabrycznej wiązki sygnałowej | Uniwersalność między markami |
| 2.3 | Architektura PCB | Jedna uniwersalna płytka, tryb pracy wybierany programowo | Jeden BOM, jedna płytka zamiast wariantów |
| 2.4 | Wejście triggera | **Dwie ścieżki wybierane zworką:** (a) VR → MAX9926 → MCU, (b) Hall → ochrona + konfigurowalny rezystor podciągający → wejście cyfrowe MCU | MAX9926 obsługuje wyłącznie czujniki VR; Hall daje gotowy sygnał cyfrowy i nie wymaga kondycjonowania. Zworka ustawiana raz przy instalacji, wewnątrz obudowy — tej samej, która musi być otwieralna dla złącza SWD. Zasilanie czujnika Halla z linii +5 V ref, bez dodatkowych pinów |
| 2.5 | Synchronizacja fazy (4T) | Domyślnie batch, tylko z wału korbowego; opcjonalne wejście czujnika fazy | Nie wszystkie jednocylindrowe 4T mają dostępny czujnik fazy |
| 2.7 | Motocykl referencyjny | Beta 300 RR (2015), 1-cyl. 2T, gaźnik, **bez TPS** | Dostępny fizycznie. Motocykl nie ma czujnika przepustnicy i nie będzie on dokładany |
| 2.8 | Narzędzie PCB | Claude dostarcza schemat, netlistę i wytyczne; Paweł przerysowuje w Fusion 360 Electronics | Dokumentacja transferowalna |
| 2.9 | Tor energii zapłonu MVP-A | **AC-CDI** z fabryczną cewką | Energia iskry sprawdzona fabrycznie na tym silniku w całym zakresie obrotów, także przy kopnięciu. Akumulator zasila tylko logikę, więc rozruch kopnięciem przy słabym akumulatorze ma największy zapas (ECU-IGN-021). Bez zakupu cewki, przeróbek mechanicznych i dodatkowego obciążenia ładowania. Odrzucone alternatywy i otwarte punkty: O-001 |

---

## 3. Komponenty ECU

Kolumna **Kwalifikacja** jest polem arkusza kwalifikacji komponentu. Pozycje bez potwierdzonej kwalifikacji i pełnego numeru są otwarte (O-027, O-063).

| Funkcja | Układ | Pełny numer | Kwalifikacja / zakres | Uwagi |
|---|---|---|---|---|
| Mikrokontroler | **STM32G474VET3** | STM32G474VET3 | −40…+125 °C | Wybrany za HRTIM. **Sufiks T3, nie T6** — T6 ma tylko −40…+85 °C, a analiza termiczna daje do 84 °C wewnątrz obudowy. **LQFP100, nie LQFP64** — bilans wykazał 55 potrzebnych sygnałów wobec ~50 użytkowych w LQFP64; LQFP100 daje ~82 piny, zapas ~27. 512 KB Flash, 128 KB RAM, 170 MHz, HRTIM, FDCAN, USB |
| Tor zapłonu | **AC-CDI — blok dyskretny** | ⚠️ do doboru | ⚠️ do kwalifikacji | Prostownik WN, kondensator zapłonowy, tyrystor, rozładowanie, ochrona przepięciowa. Dobór i arkusze kwalifikacji w O-001 — elementy istotne dla bezpieczeństwa, nie przechodzą do Fazy 4 jako zwykłe bierne. **VBG08H-E usunięty 15.10.2026** — zapłon nie jest indukcyjny |
| Driver wtryskiwaczy | **TLE9104SH** | TLE9104SHXUMA1 | ✅ Aktywny, AEC-Q100/101 | Historia doboru: L9960 (błąd — mostek H do silników DC) → TLE8104E (funkcjonalnie dobry, **status NRND**) → TLE9104SH. Dane wtryskiwaczy KTM TPI/TBI: 11,7 Ω nom., prąd ~1,23 A przy 14,4 V = wysokoimpedancyjne, **peak-and-hold niepotrzebne, wystarcza tryb nasycony**. 4 kanały low-side (2 na wtryskiwacze, 2 zapas), 3 A/kanał, SPI z diagnostyką. Pin EN jest punktem sprzętowego bramkowania od kill switcha |
| Transceiver CAN ×2 | **TJA1043** | ⚠️ do ustalenia | ✅ Aktywny, AEC-Q100 (strona NXP) | TJA1051T/3 odrzucony — nie ma wybudzania przez magistralę. **Od 18.10.2026 steruje zasilaniem: wyjście INH włącza obie przetwornice, w uśpieniu (Sleep) czuwa sam z pinu BAT, 18 µA typ. / 30 µA maks.** Reguły schematu: rozdz. 6.2. Ten sam układ w ECU i HMI. **NXP wskazuje TJA1443A jako następcę** — zgodność do sprawdzenia przy doborze pełnego numeru (Faza 4) |
| IMU | ~~BMI090L~~ | — | ❌ **Brak AEC-Q100, −40…+85 °C** | Zmiana z BMI088 miała usunąć brak kwalifikacji; BMI090L jej **też nie ma** — dokumenty producenta wskazują rynki przemysłowe, a karty dystrybutorów status Obsolete. **Dobór nierozstrzygnięty, pozycja O-027** |
| Pamięć logów | **W25Q64** (8 MB, SPI NOR) | ⚠️ rodzina, nie numer | ⚠️ klasa przemysłowa | Czarna skrzynka, 8 MB z zapasem; wlutowana, bez slotu. Pełny numer i klasa do ustalenia (O-063) |
| Wyjścia pomocnicze | BTS7008-2EPA ×3 | ⚠️ do ustalenia | AEC-Q100 | PROFET+2, 6 kanałów, diagnostyka, ochrona zwarciowa i odwrotnej polaryzacji. **7,5 A/kanał to wartość nominalna w określonych warunkach, nie dopuszczalny prąd roboczy dowolnego obciążenia** |
| Kondycjoner VR/Hall | **MAX9926** | MAX9926UAEE/V+ | ✅ Production, −40…+125 °C, automotive | Adaptacyjny próg 33% poprzedniego szczytu, detekcja przejścia przez zero, czułość od 20 mV, odporność na pominięty ząb. **Pobór 4,7 mA typ./10 mA max, brak trybu shutdown** — musi być odcinany przełącznikiem obciążenia. Wersja dwukanałowa; jednokanałowy MAX9924 jest mniejszy i tańszy. Jedyna pozycja niedostępna w TME (O-033) |
| Ciśnienie atmosferyczne | BMP390 | ⚠️ do ustalenia | ❌ **bez kwalifikacji automotive, −40…+85 °C** | Korekta na wysokość n.p.m. Wymaga membrany odpowietrzającej IP67. **Nowe wymaganie SYS-ENV-003b dyskwalifikuje ten układ w obecnej roli** — przy 85 °C otoczenia wnętrze obudowy przekracza jego zakres. Albo zamiennik w klasie Grade 1/2, albo zatwierdzone odstępstwo z uzasadnieniem miejsca montażu na PCB |
| Pozycja biegu | MLX90316 | ⚠️ do ustalenia | ⚠️ do potwierdzenia | Triaxis, bezstykowy, kąt magnesu 0–360°, wyjście analogowe. **Wykonalność mechaniczna na Becie niepotwierdzona (O-031)** |
| **Przetwornica 5,0 V** | do doboru | — | — | Nastawa stała (dzielnik rezystorowy), wyjście Power Good. Zasila VCC transceivera oraz — przez przełącznik obciążenia — czujniki zewnętrzne, MAX9926 i MLX90316. **Wejście EN sterowane z INH TJA1043** — musi znosić napięcie akumulatora i wyłączać przetwornicę przy INH niesterowanym. Prąd w stanie wyłączonym ≤ 5 µA (przydział, rozdz. 6.1) |
| **Przetwornica 3,3 V** | do doboru | — | — | Nastawa stała, Power Good. Zasila procesor, watchdog, pamięć, IMU i VIO transceivera. **Wejście EN sterowane z INH TJA1043** (te same wymagania co 5 V). Prąd w stanie wyłączonym ≤ 5 µA (przydział). Wymaga filtru LC dla części analogowej procesora |
| **Komparator kill switcha** | do doboru | — | — | Bramkuje wejścia EN driverów sygnałem kill switcha, niezależnie od firmware. Jeden próg między poziomem RUN a STOP układu trzypoziomowego — odcina i przy naciśnięciu, i przy przerwie w przewodzie. Zasilany z szyny 5 V za przełącznikiem obciążenia, więc w uśpieniu nie obciąża budżetu. **Komparator wewnętrzny procesora świadomie odrzucony**: jest konfigurowany przez firmware, a to dokładnie ta zależność, którą zakwestionował audyt |
| **Przełącznik obciążenia 5 V** | do doboru | — | — | Odcina czujniki zewnętrzne, MAX9926 i MLX90316 w uśpieniu. Powinien mieć ograniczanie prądu — izoluje zwarcie w okablowaniu zewnętrznym od reszty układu |
| Rezonator HSE | 8 MHz | do doboru | AEC-Q200, −40…+125 °C | Przy 10 000 obr/min błąd kwarcu ±50 ppm to ~0,3 µs ≈ **0,002° kąta wału** — kilkaset razy mniej niż tolerancje mechaniczne koła (0,5–1°). TCXO niepotrzebny |
| **Watchdog zewnętrzny** | TPS3430-Q1 | ⚠️ do ustalenia | AEC-Q100, −40…+125 °C | **Okienkowy**, nie prosty timeout — wykrywa też kod działający w złym tempie (uszkodzony PLL), czego zwykły watchdog nie zauważy. Okno programowane kondensatorem, 63 ms–77 s. **Ma wejście wyłączające nadzór — patrz O-013** |
| Podtrzymanie RTC | Superkondensator 0,1–0,47 F | — | — | Procesor ma wbudowany RTC. Podtrzymanie działa tylko przy odłączonym akumulatorze (serwis, zimowanie); superkondensator zamiast baterii — brak wymiany po latach. **Rozładowany superkondensator przy starcie zachowuje się jak zwarcie** — wymagany rezystor ograniczający. Prąd upływu dolicza się do budżetu uśpienia |
| Złącze główne | **Molex CMC 28-obwodowy** | ⚠️ wymiary do potwierdzenia | IP6K7/IP6K9K, −40…+125 °C, 25 G | NTSEAL 26 odrzucony — zero rezerwy pinów. Styki hybrydowe: 18× 0,635 mm (2,5 A, sygnały) + 5× 1,50 mm (12 A) + 5× 2,80 mm (21 A) — więcej obwodów w mniejszej obudowie niż złącze z jednakowymi stykami. Istnieje jako header do PCB i receptacle na wiązkę |
| Złącze USB | USB-C | — | — | Uszczelnione lub standardowe z zaślepką IP67. Wymaga rezystorów 5,1 kΩ na liniach CC (tryb urządzenia) |
| Ochrona wejścia | TVS, ochrona odwrotnej polaryzacji, filtr LC, PTC | do doboru | — | Patrz rozdz. 4.4 |

**6 kanałów PROFET:** wentylator, przekaźnik rozrusznika, światła, pompa paliwa, aux ×2.

---

## 4. Zasilanie

### 4.1 Topologia

```
12 V B+ ─► ochrona wejścia (TVS) ─► dioda Schottky'ego (gałąź logiki) ─► filtr LC ─┬─► 1 kΩ + 10 nF ─► TJA1043 BAT
                                                                                │       (czuwa zawsze, ~18 µA w Sleep)
                                                                                │              │ INH
                                                                                │              ▼
                                                                                ├─► Przetwornica 5,0 V ◄─ EN ─┐
                                                                                │   nastawa stała             │
                                                                                │     └─► TJA1043 VCC,        │
                                                                                │         przełącznik obciążenia (GPIO) ─► MAX9926,
                                                                                │         komparator, czujniki zewnętrzne
                                                                                │                             │
                                                                                └─► Przetwornica 3,3 V ◄─ EN ─┘
                                                                                    nastawa stała
                                                                                      └─► MCU, TPS3430-Q1, flash, IMU, TJA1043 VIO
                                                                                          └─► filtr LC ─► VDDA/VREF+

W uśpieniu: INH niesterowane → obie przetwornice wyłączone → procesor i watchdog bez zasilania (rozdz. 6)
```

**Dwie przetwornice zamiast przetwornicy i regulatora liniowego.** Regulator liniowy z 5 V na 3,3 V traci ~1/3 mocy w cieple (~0,3 W przy naszym poborze), co przy napiętym budżecie termicznym w szczelnej obudowie jest istotne.

**Koszt tej decyzji:** przetwornica daje napięcie z tętnieniem od przełączania, gorsze dla przetwornika ADC niż gładkie napięcie z regulatora liniowego. Kompensacja: filtr LC na zasilaniu części analogowej plus uśrednianie sprzętowe w ADC.

**Odrzucona konsolidacja w układ SBC** (transceiver + regulator + watchdog + zarządzanie uśpieniem w jednej obudowie, np. UJA1169A): regulator w SBC jest liniowy i pracuje bezpośrednio z 12 V, co przywraca problem termiczny rozwiązany architekturą dwustopniową. Dodatkowo warianty z regulatorem 3,3 V nie mają wyjścia 5 V dla czujników zewnętrznych, a warianty z tym wyjściem mają regulator 5 V — nie da się mieć obu naraz.

### 4.2 Mikrokontroler monitoruje, nie reguluje

**Nastawy szyn są stałe (dzielniki rezystorowe).** Regulacja napięcia szyn przez procesor została rozważona i odrzucona:

- Procesor zasila się z tych samych szyn — błąd firmware mógłby zniszczyć czujniki, transceiver, pamięć i sam procesor
- Możliwa pętla samopodtrzymująca: obniżenie własnego zasilania → brown-out → reset → wartość domyślna → powtórka
- Zawieszenie procesora zostawia szynę w nieokreślonym stanie
- **Regulacja niczego nie naprawia** — spadek napięcia oznacza zwarcie, przeciążenie albo słaby akumulator; podniesienie nastawy pogłębia problem

**Mechanizmy nadzoru, które realizują cel, dla którego rozważano regulację:**

| Mechanizm | Działanie |
|---|---|
| Pomiar obu szyn przez ADC | Wykrywanie spadków i dryftu, kompensacja pomiarów ratiometrycznych |
| Sygnał Power Good z przetwornic | Wyjście cyfrowe „szyna w tolerancji"; działa niezależnie od firmware, dostępne przed startem ADC |
| Sterowanie włączeniem szyny 5 V | Wyłączenie przy uśpieniu lub wykryciu zwarcia w okablowaniu zewnętrznym. Bezpieczny kierunek sterowania |

Reakcja na wykryty problem: wpis do diagnostyki, ostrzeżenie na HMI, ewentualne przejście w tryb awaryjny — **nigdy zmiana nastawy**.

**Dokładność pomiarów: filtr LC, bez zewnętrznego źródła odniesienia.** Pomiary ratiometryczne kompensują się same — mierząc tym samym przetwornikiem sygnał czujnika i szynę 5 V, błąd napięcia odniesienia skraca się w stosunku tych wartości. Jedyny pomiar bezwzględny (napięcie akumulatora) korygowany fabrycznie skalibrowanym wewnętrznym źródłem odniesienia procesora.

⚠️ **Ograniczenie tego rozumowania (O-025):** kompensacja ratiometryczna działa przy wspólnej referencji proporcjonalnej, a użycie uszkodzonej szyny jako odniesienia do badania jej samej może ukryć awarię. Nadzór krytycznej szyny wymaga niezależnego odniesienia.

### 4.3 Terminacja CAN

Magistrala wymaga dokładnie **dwóch** rezystorów 120 Ω — na fizycznych końcach, nie przy każdym module.

- **ECU:** 120 Ω na stałe (jako gateway zawsze pozostaje jednym końcem)
- **HMI i każdy przyszły moduł:** terminacja przełączana zworką. Dziś HMI jest drugim końcem; po dołożeniu modułu za HMI zworka schodzi i terminacja przechodzi na nowy ostatni moduł
- **Terminacja dzielona:** 2×60 Ω szeregowo z kondensatorem ~4,7 nF ze środka do masy zamiast pojedynczego 120 Ω — tłumi zakłócenia wspólne, standard automotive, koszt marginalny. Zgodne z rys. 30 noty NXP AH1014, która dodaje **ok. 100 pF z CANH i z CANL do masy**

### 4.4 Ochrona przed przepięciami, ESD i EMI

**Warstwa 1 — zasilanie:** **TVS dwukierunkowy** na wejściu B+ (zmiana 18.10.2026 — jednokierunkowy nie przetrwa odwrotnej polaryzacji; dobór wg rozdz. 13.1); ochrona odwrotnej polaryzacji **diodą Schottky'ego na gałęzi logiki** (decyzja 18.10.2026: ~120 mA × ~0,4 V ≈ 50 mW strat, **0 µA w uśpieniu**; sterownik diody idealnej odrzucony — pobiera prąd spoczynkowy albo wymaga wyłączania przez INH; zapas napięcia dla przetwornicy 5 V przy 7 V na złączu do potwierdzenia przy jej doborze); filtr LC blokujący szum w obu kierunkach; **PTC 500 mA–1 A tylko na gałęzi logiki, nie na całym B+** — gałąź mocy ciągnie kilka amperów, a PTC o takim prądzie ma zauważalną rezystancję szeregową i wolną reakcję, a te obwody są już chronione indywidualnie przez PROFET-y.

**Warstwa 2 — linie wychodzące z obudowy:** czujniki — TVS niskopojemnościowy + filtr RC na każdej linii; CAN — dedykowany dwukanałowy TVS; USB — TVS o bardzo niskiej pojemności, żeby nie zniekształcić pary różnicowej; **trigger — TVS + filtr, linia najbardziej narażona, biegnie przy cewce zapłonowej**.

**Warstwa 3 — wyjścia mocy:** diody gaszące na obciążeniach indukcyjnych (PROFET ma wbudowane ograniczanie, zewnętrzne diody go odciążają); cewka zapłonowa ma clamp w driverze, linia odseparowana na PCB.

**Warstwa 4 — konstrukcja PCB:** ciągła płaszczyzna masy rozdzielona na sekcję analogową i mocy z jednym punktem połączenia; fizyczne oddzielenie sekcji zapłonu i PROFET od analogowej; kondensatory odsprzęgające przy każdym układzie; sygnały analogowe z dala od ścieżek przełączających duże prądy; do rozważenia ekran metalowy nad sekcją analogową.

⚠️ **Architektura powrotów prądowych i ekranowania musi być ustalona przed PCB (O-039).** Późne wykrycie nieodpornego wejścia VR wymusi zmianę płytki i złączy.

---

## 5. Złącze i sygnały

> Lista wymaga przeliczenia przy schemacie. Usunięcie quickshiftera i czujnika sprzęgła **zwolniło dwa piny**; jeden przechodzi do pozycji O-060 (niezależny sygnał obciążenia dla B/C), jeden zostaje w zapasie.

| Grupa | Sygnały | Piny | Typ styku |
|---|---|---|---|
| Zasilanie | B+ (12 V, stałe z akumulatora), GND | 2 | 2,80 mm |
| Trigger | Sygnał+, Sygnał− | 2 | sygnałowy |
| Czujniki analogowe | TPS *(tylko B/C)*, temp. cieczy, temp. powietrza, pozycja biegu | 4 | sygnałowy |
| Wspólne czujników | +5 V ref, masa analogowa | 2 | sygnałowy |
| Wejścia cyfrowe | Start, kill switch, czujnik prędkości koła, czujnik fazy wałka *(rezerwa 4T)* | 4 | sygnałowy |
| Wyjścia mocy silnika | Zapłon, wtryskiwacz 1, wtryskiwacz 2 | 3 | 1,50 mm |
| Wyjścia pomocnicze | Wentylator, rozrusznik, światła, pompa paliwa, aux ×2 | 6 | średni/duży |
| CAN | CAN H, CAN L | 2 | sygnałowy |
| **Razem** | | **27 / 28** | |

⚠️ **Bilans dotyczy pinów układu, nie obwodów wiązki (O-030).** Potrzebne są osobne powroty mas, a prąd i temperatura ograniczają liczbę jednocześnie obciążonych styków.

**Przyciski start i kill switch idą bezpośrednio z kierownicy do ECU** przez główne złącze, niezależnie od kabla przycisków HMI. Podział: 4 przyciski HMI = obsługa systemu; start i kill = sterowanie silnikiem.

Rozważona i odrzucona obsługa kill switcha przez HMI i CAN:

- **Kill switch to funkcja bezpieczeństwa.** Awaria oznacza „nie mogę zatrzymać pracującego silnika" — scenariusze to zablokowana przepustnica, upadek z przygniecionym motocyklem, silnik w rozbiegu. Przepuszczenie przez trzy dodatkowe punkty awarii (firmware HMI, magistrala, firmware ECU) tworzy sytuację, w której zawieszenie oprogramowania wyświetlacza odbiera możliwość zgaszenia silnika. **Standardowe rozwiązanie motocyklowe działa fail-safe: obwód normalnie zamknięty, przerwanie przewodu gasi silnik. Przez CAN tej właściwości nie da się odtworzyć.**
- **Przycisk startu — opóźnienie.** Przy uśpionym ECU łańcuch to naciśnięcie → wybudzenie HMI → ramka CAN → wybudzenie ECU → rozrusznik. Setki milisekund zwłoki przy funkcji, która ma reagować natychmiast.

**Czujnik fazy wałka rozrządu (4T):** nie znaleziono potwierdzenia, że jednocylindrowe enduro 4T go mają — dokumentacja diagnostyczna wymienia tylko czujnik wału korbowego, co jest zgodne z praktyką dla jednocylindrowców. **Pin zarezerwowany mimo to** — koszt jednego pinu wobec przeprojektowania płytki, gdyby okazał się potrzebny.

**Czujnik prędkości koła:** wykorzystujemy fabryczny, założono pasywny (kontaktron lub Hall z otwartym kolektorem), 2 przewody, masa wspólna z GND. ECU dostarcza konfigurowalny programowo rezystor podciągający. **Jeśli czujnik wymaga własnego zasilania, potrzebny dodatkowy pin (O-032).**

---

## 6. Uśpienie i wybudzanie

**Motocykle enduro nie mają stacyjki** — ECU jest stale podłączone do akumulatora.

**Wybrana architektura (decyzja Pawła 18.10.2026): w uśpieniu szyny 3,3 V i 5 V są wyłączone przez wyjście INH transceivera TJA1043.** Procesor, watchdog i cała logika są bez zasilania; czuwa wyłącznie TJA1043 zasilany z pinu BAT. To docelowe zastosowanie układu według producenta: karta TJA1043 opisuje INH jako *„inhibit output for switching external voltage regulators”*, a nota NXP AH1014 (rozdz. 6.3, rys. 30) pokazuje obie przetwornice — w tym zasilającą mikrokontroler — sterowane z INH.

**Zastąpiona architektura:** procesor w trybie Stop przy włączonych obu przetwornicach. Odrzucona z dwóch powodów: bilans uśpienia ~117–187 µA przy limicie 150 µA (O-023) oraz sprzeczność watchdoga z uśpieniem (O-013) — zasilony watchdog resetowałby śpiący procesor, a jego programowe wyłączanie tworzyłoby stan „silnik pracuje, nadzór wyłączony”. Wcześniejsze uzasadnienie odrzucenia INH („rozwiązanie samochodowe, w motocyklu niepotrzebne”) nie wytrzymało bilansu.

| Element | Praca | Uśpienie |
|---|---|---|
| TJA1043 | Normal | **Sleep** — zasilany z BAT, nasłuch wzorca wybudzenia na magistrali i zbocza na pinie WAKE, INH niesterowane |
| Przetwornice 5,0 V i 3,3 V | włączone przez INH | **wyłączone** (INH niesterowane, wejście włączania ściągnięte w dół) |
| STM32G474, TPS3430-Q1, pamięć, IMU, czujniki | zasilane | **bez zasilania** |
| PROFET-y, driver wtrysku, blok CDI | wg stanu silnika | wyłączone |

**Skutek dla nadzoru (O-013):** watchdog jest zasilany zawsze wtedy, gdy zasilany jest procesor — nie istnieje stan „procesor pracuje, nadzór wyłączony” i nie istnieje programowy wyłącznik nadzoru (ECU-SAF-017).

**Skutek dla danych:** uśpione ECU nie ma RAM. Motogodziny, przebieg, zatrzask K4 (O-014) i stan usterek muszą być w pamięci nieulotnej przed zaśnięciem.

### 6.1 Bilans uśpienia ECU

Punkt odniesienia: **zaciski akumulatora, 12,0 V, +25 °C** (ECU-PWR-001). Dla elementów jeszcze niewybranych wartość jest **przydziałem**, który staje się kryterium doboru.

| Element zasilany z akumulatora w uśpieniu | µA maks. | Źródło |
|---|---|---|
| TJA1043, Sleep, pin BAT | 30 | karta (18 typ.) |
| Pin WAKE, prąd wejściowy | 10 | karta |
| Przetwornica 5 V, wyłączona | ≤ 5 | przydział |
| Przetwornica 3,3 V, wyłączona | ≤ 5 | przydział |
| Zabezpieczenie przed odwrotną polaryzacją — dioda Schottky'ego | 0 | konstrukcja (rozdz. 4.4) |
| TVS na wejściu, upływ przy 12 V | ≤ 5 | przydział |
| 3× PROFET, wyłączone | ≤ 3 | przydział |
| Dzielnik pomiaru akumulatora, podciągnięcia kill switcha i czujników | 0 | **reguła: zasilane wyłącznie z szyn wyłączanych** |
| **Razem** | **≤ 63** | wobec limitu 150 µA |

Do potwierdzenia pomiarem T-PWR-001 na prototypie.

### 6.2 Reguły schematu dla TJA1043 (ECU i HMI)

Z karty TJA1043 (rys. 9) i noty AH1014 (rys. 30, rozdz. 6.3–6.4), sprawdzone na schematach graficznych 18.10.2026:

| Pin / obwód | Reguła |
|---|---|
| BAT | Za diodą zabezpieczającą; **ok. 1 kΩ szeregowo + ok. 10 nF** przy pinie |
| INH → wejścia włączania obu przetwornic | Obciążenie INH **≥ 10 kΩ, ≤ ok. 1 mA** (AH1014). Przy INH niesterowanym przetwornica musi być wyłączona — wewnętrzne ściąganie wejścia albo zewnętrzny rezystor. **Wejście włączania musi znosić napięcie akumulatora** (INH ≈ VBAT) — kryterium doboru przetwornic |
| WAKE | Przełącznik do masy (przycisk startu; w HMI drabinka przycisków), **Rexbias ≤ 150 kΩ** do BAT za diodą, **RS ≥ 2,7 kΩ** szeregowo (maks. 15 mA pinu przy utracie masy, U do 40 V) |
| Linia przycisku startu do MCU | W uśpieniu przy puszczonym przycisku niesie napięcie akumulatora — dzielnik lub ogranicznik do 3,3 V |
| USB | Tranzystor zwierający węzeł WAKE do masy, sterowany napięciem z USB |
| STB_N, EN | Wprost do portów procesora, **bez zewnętrznych rezystorów** — jak w schematach NXP (decyzja Pawła 18.10.2026). Stan przy niesterowanych pinach: założenie Z16 |
| ERR_N | Do wejścia procesora z włączonym wewnętrznym podciąganiem. Diagnostyka: Pwon, źródło wybudzenia, usterka magistrali, usterka lokalna |
| VCC / VIO | Z szyny 5 V / z szyny 3,3 V procesora |
| CANH, CANL | Terminacja dzielona (rozdz. 4.3) + **ok. 100 pF** z każdej linii do masy |

### 6.3 Źródła wybudzenia

**Każda droga wybudzenia kończy się na transceiverze zasilanym z BAT, nigdy na procesorze.**

| Źródło | Droga |
|---|---|
| Przycisk startu | Pin WAKE TJA1043 w ECU |
| Podłączenie USB | Tranzystor ściąga pin WAKE w ECU |
| Przyciski na kierownicy | Pin WAKE TJA1043 w HMI → HMI wstaje i nadaje → TJA1043 w ECU wybudza się z magistrali |
| Ramka CAN | Filtrowany wzorzec wybudzenia (dominujący–recesywny–dominujący); **każda zwykła ramka go spełnia** |

**Gdy ECU nie śpi, HMI też nie śpi** — ECU po wybudzeniu zawsze budzi HMI. Trwały stan „jeden węzeł pracuje, drugi śpi” jest do uniknięcia ze względu na różne podparcie napięciowe magistrali (AH1014, rozdz. 6.2.4).

**Świadomie odrzucone: wybudzanie sygnałem obrotów wału.** Trzy warianty i powody odrzucenia:

| Wariant | Powód odrzucenia |
|---|---|
| Dedykowany komparator nanomocowy na równoległej ścieżce VR | Dublowanie ścieżki sygnału — dwa układy, dwie drogi na PCB, możliwa rozbieżność wskazań. Dodatkowo **marginalna czułość przy kopnięciu**: sygnał VR przy obrotach rozruchowych ma 50–300 mV międzyszczytowo, a komparator ze stałym progiem i napięciem niezrównoważenia rzędu miliwoltów działałby na granicy. MAX9926 radzi sobie dzięki adaptacyjnemu progowi i czułości od 20 mV |
| Utrzymanie MAX9926 pod napięciem | Precyzyjny front-end analogowy pobiera miliampery, nie nanoampery: **4,7 mA typowo, 10 mA maksymalnie, brak jakiegokolwiek trybu shutdown**. To ~3400 mAh miesięcznie — więcej niż cały akumulator 3 Ah |
| Okresowe próbkowanie (RTC budzi procesor, kondycjoner włączany na krótko) | Przy krótkim oknie łatwo przegapić kopnięcie — zawodne dokładnie w scenariuszu, dla którego się to robi. W nowej architekturze dodatkowo niemożliwe bez zasilonego procesora |

**Scenariusze startu (O-024, decyzje Pawła 18.10.2026):**

| Scenariusz | Zachowanie |
|---|---|
| Start przyciskiem, ECU śpi | Nacisk budzi; **przycisk trzymany do gotowości (≤ 200 ms, ECU-PWR-003) uruchamia rozrusznik** przy kill switchu w RUN. Puszczony wcześniej — tylko budzi (ECU-SAF-018) |
| Kopnięcie, ECU śpi | **Najpierw przycisk** (start albo dowolny na kierownicy). Przy słabym akumulatorze — przycisk na kierownicy, żeby nie kręcić rozrusznikiem |
| Start z rozpędu (popych), ECU śpi | **Najpierw przycisk** — świadome ograniczenie. Po wybudzeniu popych działa normalnie |
| Praca bez HMI | **Pełna** — start, praca i usypianie bez HMI (SYS-COM-008), kod usterki DTC-COM-01 |
| Silnik zgasł w ruchu | ECU nie śpi (30 min od ostatniej pracy silnika) — restart z mapy natychmiast (ECU-IGN-019) |

Kopnięcie i popych przy uśpionym ECU wymagają przycisku — **do zapisania w instrukcji**.

**Po podłączeniu akumulatora** ECU albo wstaje samo, albo czeka na przycisk — karta tego nie rozstrzyga (założenie Z15). Oba zachowania są bezpieczne.

⚠️ **Pełna ścieżka startu nie jest zdefiniowana (O-024):** czy nacisk budzący uruchamia rozrusznik, start z rozpędu, praca bez HMI, sekwencja wobec czasu startu zasilania i dopuszczenia iskry.

### 6.4 Sekwencja usypiania

1. ECU decyduje: **30 min bez pracy silnika i bez interakcji** (naciśnięcia przycisków HMI są zgłaszane do ECU po CAN). Ekran gaśnie wcześniej, po 3 min — to robi HMI samo, bez usypiania
2. ECU wysyła żądanie uśpienia do HMI
3. HMI kończy zapisy w toku; **naciśnięcie przycisku w tym momencie przerywa usypianie** (HMI odpowiada „zajęte”, ECU liczy 30 min od nowa)
4. HMI wysyła potwierdzenie i **czeka na zgłoszenie kontrolera CAN, że ramka wyszła na magistralę**
5. HMI ustawia transceiver w Go-to-Sleep → Sleep → INH niesterowane → szyny HMI gasną
6. ECU po potwierdzeniu czeka na **ciszę na magistrali** dłuższą niż timeout ramki HMI (SYS-COM-004) — drugie, niezależne potwierdzenie
7. ECU zapisuje stan do pamięci nieulotnej i przechodzi w Sleep tą samą drogą

**Kolejność „HMI milknie pierwsze” jest wymuszona:** każda ramka z HMI obudziłaby uśpione ECU.

| Scenariusz negatywny | Zachowanie |
|---|---|
| Potwierdzenie zginęło, HMI zasnęło | Cisza na magistrali wystarcza, ECU zasypia |
| HMI nie zasnęło | ECU ponawia kilka razy, potem zapisuje usterkę i zasypia; HMI zaśnie na swoim timeoucie |
| **Go-to-Sleep zignorowany przez równoczesne wybudzenie** (AH1014, rozdz. 6.2.5) — INH zostaje aktywne | Jeśli zasilanie nie zanikło w określonym czasie po rozkazie, firmware wraca do pracy i traktuje to jak wybudzenie |
| HMI bez ramek od ECU przez **30 s** | HMI usypia się samo (kroki 3 i 5 bez potwierdzenia) |
| Nacisk budzący HMI | **Tylko budzi**, nie wykonuje akcji w menu |
| Szyna 5 V poniżej ~3,5 V przez > 100 ms | Transceiver wymusza Sleep (karta). Wymaga akumulatora poniżej ~4 V — poza zakresem ECU-IGN-021 |

**Warunki zaśnięcia:** 30 min bez pracy silnika i bez interakcji; wyświetlacz gaszony po 3 min.

**Dzielnik pomiaru napięcia akumulatora** musi być zasilany za szyną wyłączaną albo odłączany tranzystorem — typowy dzielnik 100 kΩ/10 kΩ pobiera z 12 V ~110 µA, czyli prawie cały limit.

---

## 7. Nadzór i stan bezpieczny

**Trzy poziomy:**

1. **Watchdog wewnętrzny procesora** — taktowany własnym oscylatorem, niezależnym od zegara głównego. Wykrywa zawieszenie oprogramowania.
2. **TPS3430-Q1, watchdog okienkowy zewnętrzny** — niezależny od procesora, działa przy awarii zasilania rdzenia, uszkodzeniu kwarcu lub zawieszeniu sprzętowym. **Okienkowy**: sygnał musi przyjść w zdefiniowanym oknie, za wcześnie lub za późno oznacza reset. Wykrywa kod działający w złym tempie, co przy sterowniku zapłonu jest realnym zagrożeniem.
3. **Stan bezpieczny przy resecie** — sam reset nie wystarczy, jeśli wyjścia zostaną w przypadkowym stanie. Przy resecie i podczas startu wszystkie wyjścia mocy muszą być domyślnie wyłączone, inaczej reset przy pracującym silniku mógłby zostawić cewkę pod napięciem albo wtryskiwacz otwarty.

⚠️ **Realizacja punktu 3 jest błędna i jest pozycją otwartą (O-002, O-017).** Zapis mówił o rezystorach ściągających na wejściach sterujących wszystkich driverów. Dla driverów wtrysku i PROFET (wejścia aktywne wysokim) jest to poprawne. **Dla EN drivera zapłonu jest odwrotnie**: EN jest aktywne niskim, więc ściągnięcie go do masy **załącza** układ, a dodatkowo pokonuje wewnętrzny pull-up, który sam z siebie dawał stan bezpieczny.

⚠️ **Watchdog nie jest ochroną toru zapłonu (O-012).** Przy oknie 100 ms i 10 000 obr/min to 16,7 obrotu wału. Dla błędu kąta pojedynczego impulsu dopuszczalny czas reakcji wynosi zero — chroni wyłącznie zapobieganie i ograniczenie tego, co stopień wyjściowy jest w stanie zrobić.

**Wiązka kill switcha — wymóg szczególny:** przycisk podłączony wiązką z **dwoma rezystorami umieszczonymi przy przycisku** — szeregowym i równoległym do styku. Dają trzy rozróżnialne poziomy napięcia, dzięki czemu ECU odróżnia naciśnięcie od przerwania przewodu i potrafi to wskazać kierowcy. Podłączenie zwykłego przycisku bez rezystorów **nie jest niebezpieczne** — odcięcie działa w obu stanach, ale każde naciśnięcie zgłosi się jako przerwa. Wiązka z rezystorami wchodzi w zakres dostawy.

---

## 8. HMI

| # | Decyzja | Wybór | Uzasadnienie |
|---|---|---|---|
| H.1 | Własny procesor | Tak | Obsługa CAN, przycisków, wyświetlacza, lokalnej konfiguracji |
| H.2 | Procesor | STM32G0B1 | Jedyna linia G0 z FDCAN; ten sam producent co ECU |
| H.3 | Wyświetlacz | Riverdi **RVT35HHBFWN00** — 3,5", 320×240, IPS, koprocesor EVE4, SPI/QSPI, 1000 cd/m², bez dotyku, metalowa ramka | Koprocesor graficzny daje animacje bez obciążania pamięci procesora |
| H.4 | Przyciski | 4 szt. (góra, dół, wybór, wstecz), IP67, automotive-grade, 1 M cykli, złocone styki | — |
| H.5 | Lokalizacja | **Na kierownicy**, nie w obudowie | Ergonomia obsługi w jeździe |
| H.6 | Okablowanie przycisków | Drabinka rezystorowa — 4 przyciski na jednym wejściu analogowym | Ogranicza liczbę żył. ⚠️ **Bez analizy najgorszego przypadku (O-035)** |
| H.7 | Podświetlenie przycisków | ECU wysyła stan świateł po CAN, HMI włącza podświetlenie | Bez dodatkowego okablowania |
| H.8 | Złącze główne | Deutsch DTM04-4P: CAN H, CAN L, +12 V stałe, GND | DTM to miniaturowa wersja DT, 13 A/pin |
| H.9 | Złącze przycisków | Osobne, Deutsch DTM04-3P | Serwisowalność — kierownice wymieniane po upadkach bez ruszania wiązki głównej |
| H.10 | Transceiver | TJA1043, ten sam co w ECU | Jeden numer katalogowy na oba urządzenia; wybudzanie przez magistralę potrzebne także w HMI |
| H.11 | Zasilanie | Dwie przetwornice: 5 V (wyświetlacz i koprocesor) i 3,3 V (procesor, flash). **Obie włączane wyjściem INH transceivera HMI; w uśpieniu obie wyłączone** (zmiana 18.10.2026) | Ta sama architektura co ECU (rozdz. 6). TJA1043 HMI zasilany z +12 V stałego ze złącza DTM04 |
| H.12 | Pamięć zasobów | Zewnętrzna flash SPI NOR, rodzina W25Q | Koprocesor wymaga trwałego przechowywania bitmap, czcionek i animacji; dwubankowy bootloader zostawia ~256 KB na bank — za mało na firmware i zasoby |
| H.13 | Czujnik temperatury | Cyfrowy na PCB, blisko wyświetlacza | Analiza termiczna wykazała ryzyko przekroczenia 70 °C na słońcu, przy którym panel czernieje |

### 8.1 Uśpienie HMI

**O zaśnięciu decyduje ECU** poleceniem po CAN — zna stan silnika i czas bezczynności. Wyświetlacz gaszony po 3 min, pełne uśpienie przy zasypianiu ECU po 30 min.

**Zabezpieczenie przed utratą polecenia:** gdyby ramka zaginęła, HMI zostałoby wybudzone na stałe i rozładowało akumulator. Dlatego **HMI ma własny timeout awaryjny** — brak jakiejkolwiek ramki z ECU przez **30 s** skutkuje samodzielnym zaśnięciem.

W uśpieniu (od 18.10.2026): **obie szyny HMI wyłączone przez INH transceivera**; czuwa tylko TJA1043 zasilany z +12 V stałego. Bilans uśpienia HMI na zaciskach akumulatora: transceiver 30 µA maks., pin WAKE 10, dwie wyłączone przetwornice ≤ 10, TVS ≤ 5, dioda polaryzacji 0 — **razem ≤ 60 µA**. System ECU + HMI **≤ 123 µA** wobec SYS-PWR-002 (250 µA).

**Wybudzenie przyciskiem:** drabinka przycisków jest węzłem WAKE transceivera HMI, podciągniętym do akumulatora przez Rexbias. Naciśnięcie dowolnego przycisku ściąga węzeł w dół, transceiver włącza szyny, procesor startuje, dopiero potem ADC określa, **który** przycisk. Linia do ADC wymaga separacji od napięcia akumulatora. **Warunek dla drabinki (O-035): najwyższa rezystancja drabinki < 1,33 × Rexbias** — przy 7 V węzeł musi zejść poniżej VBAT − 3 V. Nacisk budzący tylko budzi.

**Sekwencja usypiania:** rozdz. 6.4.

**Kolejność zasypiania:** ECU wysyła polecenie, czeka na potwierdzenie, dopiero potem zasypia samo — inaczej HMI mogłoby zostać wybudzone.

### 8.2 Termika HMI

Straty wewnętrzne ~2,4 W, z czego podświetlenie 1,25 W. **HMI to jedyny element wystawiony bezpośrednio na słońce**: ekran 3,5" (~0,005 m²) w ciemnej obudowie może pochłonąć do ~4 W promieniowania, więcej niż generuje sam.

| Wykonanie obudowy | Temp. wewnątrz przy 40 °C i nasłonecznieniu |
|---|---|
| Tworzywo, ciasna obudowa | ~151 °C ❌ |
| Tworzywo z zapasem | ~107 °C ❌ |
| Aluminium z odprowadzeniem ciepła | ~76 °C ⚠️ |

**Zagrożenie jest realne:** panele LCD pracują typowo do 70 °C — powyżej ciekły kryształ przechodzi w fazę izotropową i **ekran czernieje**. To znany problem jasnych wyświetlaczy: im mocniejsze podświetlenie, tym więcej ciepła.

Wynikające wymagania: obudowa aluminiowa z kontaktem termicznym; **jasny lub odblaskowy kolor zamiast czarnego** (redukuje pochłanianie z ~4 W do ułamka); czujnik temperatury i zarządzanie jasnością w firmware; daszek przeciwsłoneczny do rozważenia.

⚠️ **Paradoks do rozwiązania:** na słońcu potrzeba maksymalnej jasności, a właśnie wtedy grozi przegrzanie. Pozycja O-034, wraz z metodą wyznaczenia 76 °C, która nie została podana.

---

## 9. Budżety

Szacunki z wartości typowych z kart katalogowych. **Do weryfikacji pomiarem.**

### 9.1 Pobór prądu, strona 12 V

| Pozycja | Prąd | Moc |
|---|---|---|
| ECU — logika i czujniki | ~120 mA | ~1,3 W |
| HMI — procesor, koprocesor, podświetlenie, LED przycisków | ~200 mA | ~2,2 W |
| **System sterujący razem** | **~320 mA** | **~3,8 W** |
| Wentylator chłodnicy | ~6 A | 72 W |
| Pompa paliwa (B/C) | ~4 A | 48 W |
| Oświetlenie LED | ~2 A | 24 W |
| Przekaźnik rozrusznika | ~0,3 A | 4 W |
| **Szczyt** | **~12,6 A** | **~151 W** |
| Typowa jazda | ~2,3 A | ~28 W |

Stator w enduro tej klasy oddaje typowo 150–200 W, więc bilans się domyka; szczyt występuje rzadko i przy wysokich obrotach, gdy stator daje pełną moc. Samo ECU z HMI to <4 W.

### 9.2 Straty cieplne w obudowie ECU

| Źródło | Straty |
|---|---|
| **Driver zapłonu** (8000 obr/min, dwell 3 ms → wypełnienie ~40%) | **4,8 W** |
| Drivery wtryskiwaczy (2 kanały, 1,23 A, wypełnienie ~10%) | ~0,16 W |
| PROFET ×3 | 0,27 W |
| Przetwornica 5,0 V | 0,17 W |
| Przetwornica 3,3 V | 0,07 W |
| Przełącznik obciążenia | 0,05 W |
| **Razem** | **~5,5 W** |

| Wykonanie obudowy | Temp. wewnątrz przy otoczeniu 40 °C |
|---|---|
| Aluminium + dobry kontakt termiczny (Rth ≈ 3 K/W) | **57 °C** ✅ |
| Aluminium bez past i padów (Rth ≈ 8 K/W) | **84 °C** ⚠️ |
| Tworzywo (Rth ≈ 20 K/W) | **150 °C** ❌ |

**Wniosek: obudowa aluminiowa z kontaktem termicznym jest wymagana, nie zalecana. Tworzywo wykluczone.**

⚠️ **Dwa ograniczenia tego bilansu.** Model używa uproszczonej rezystancji cieplnej obudowy; wymagany jest pełny łańcuch złącze→pad→interfejs termiczny→obudowa→otoczenie. Ponadto **dominująca pozycja 4,8 W opiera się na niepotwierdzonym dwell 3 ms** (założenie Z2) i na niepotwierdzonej topologii zapłonu (O-001) — jeśli silnik ma CDI, cały ten wiersz traci sens.

**Do firmware:** czas ładowania cewki powinien być skracany przy wysokich obrotach — ładowanie tylko do osiągnięcia prądu nasycenia, nie stałe. Realnie obniży to dominujące źródło strat.

---

## 10. Obudowy

### ECU

| Parametr | Wymaganie |
|---|---|
| Szczelność | IP67 minimum — zanurzenie, przeprawy wodne, mycie ciśnieniowe |
| Wyrównanie ciśnienia | **Membrana odpowietrzająca obowiązkowa** — czujnik ciśnienia atmosferycznego w hermetycznej obudowie byłby bezużyteczny. Zapobiega też kondensacji przy zmianach temperatury |
| Odprowadzanie ciepła | **Aluminium z zapewnionym kontaktem termicznym** (pady lub pasta) między ścianką a driverem zapłonu, PROFET-ami i przetwornicą. Tworzywo wykluczone |
| Przepusty | Molex CMC 28-obwodowe (header wlutowany) + USB-C uszczelnione lub z zaślepką, IP67 |
| Wibracje | Mocowanie PCB w kilku punktach, nie tylko na złączu; silikonowe tuleje w punktach montażu do ramy |
| Temperatura | **−40…+85 °C otoczenia** (SYS-ENV-003), przechowywanie −40…+105 °C (SYS-ENV-004). **Obudowa nie może kumulować ciepła**: przy 85 °C otoczenia i przyroście +17 °C (dobry kontakt termiczny) wnętrze osiąga 102 °C, co daje 23 °C marginesu do klasy Grade 1. Przy złym kontakcie (+44 °C) wnętrze osiąga **129 °C i przekracza Grade 1** — dlatego kontakt termiczny jest wymaganiem, nie zaleceniem |
| Dostęp serwisowy | Otwarcie bez niszczenia uszczelnienia (uszczelka wymienna, nie klejona) — dostęp do złącza SWD i zworki triggera |
| Montaż | Odporny na uderzenia; z dala od strumienia błota i gorąca wydechu |

### HMI

| Parametr | Wymaganie |
|---|---|
| Szczelność | IP67 minimum |
| Widoczność | Osobna szybka poliwęglanowa lub szklana nad panelem — wyświetlacz nie ma własnej |
| Odblaski | Warstwa antyrefleksyjna lub daszek — inaczej 1000 cd/m² nie wystarczy przy słońcu pod kątem |
| Przepusty | DTM04-4P (główne) + DTM04-3P (przyciski) |
| Wibracje | Mocowanie do kierownicy przez elementy tłumiące — panel LCD jest wrażliwy na wibracje |
| Temperatura | **−20…+70 °C otoczenia** (SYS-ENV-003a) — ograniczone panelem, nie wyborem. Wymaga aluminium z kontaktem termicznym **oraz jasnego lub odblaskowego koloru**; tworzywo daje 107–151 °C na słońcu. Analiza przy nasłonecznieniu daje 76 °C, czyli **6 °C powyżej granicy panelu** — pozycja O-034 |
| Widoczność nocna | Regulowana jasność podświetlenia |

---

## 11. Wymagania instalacyjne

Elementy fabrycznej instalacji, które **muszą pozostać**, mimo że ECU jest standalone:

| Element | Dlaczego |
|---|---|
| **Stator** | Uzwojenie ładujące — jedyne źródło energii ładującej akumulator. **Uzwojenie wzbudzające — źródło energii zapłonu (AC-CDI)**, prowadzone do ECU |
| **Regulator napięcia i prostownik** | Bez niego napięcie rośnie z obrotami i zniszczy akumulator oraz odbiorniki |
| **Akumulator** | ECU zasilane wyłącznie z akumulatora; dodatkowo bufor wygładzający tętnienia |
| **Czujnik prędkości koła** | Wykorzystywany przez ECU |
| **Cewka zapłonowa** | **Fabryczna RC01 IG5128 (cewka CDI), zachowana.** Uzwojenie pierwotne dostaje impuls z kondensatora w ECU |

**Elementy usuwane:** fabryczny sterownik zapłonu, fabryczna wiązka sygnałowa, licznik, pompka olejowa w silnikach TPI/TBI (przejście na premiks).

**Kondensator buforowy na wejściu zasilania ECU** jest wymagany, żeby ECU pracowało stabilnie przy tętniącym napięciu z prostownika przy uszkodzonym lub odłączonym akumulatorze. Granica działania to ~7 V na złączu; akumulator przy 7 V jest już zniszczony, nie tylko rozładowany. W AC-CDI energia iskry pochodzi z uzwojenia wzbudzającego, nie z akumulatora — przy 7 V akumulator zasila wyłącznie logikę ECU i kondycjoner VR (ECU-IGN-021).

---

## 12. Kwestia regulacyjna

Homologacja pojazdu nie dotyczy — produkt offroad i motorsport, nie do ruchu drogowego. Sprzedaż urządzenia elektronicznego w UE może jednak wiązać się z obowiązkami niezależnymi od homologacji (CE/EMC, RoHS, WEEE). **Do sprawdzenia z kimś kompetentnym przed produkcją i sprzedażą** — nie blokuje obecnych prac. Claude nie jest prawnikiem ani rzeczoznawcą.

---

## 13. Obwiednia środowiskowa i elektryczna

**Część ustalona 13.10.2026 — temperatura (SYS-ENV-003, 003a, 003b, 004). Obwiednia napięciowa ustalona 18.10.2026 (rozdz. 13.1, O-022). Otwarte: profil wibracji — O-047.** Przyjęte podejście: bierzemy **strukturę listy prób** z norm automotive i **wartości wyprowadzamy z naszego układu**, nie z norm.

| Źródło | Co z niego bierzemy |
|---|---|
| **AEC-Q100 / AEC-Q200** | Siatkę klas temperaturowych jako język doboru: Grade 1 to −40…+125 °C, Grade 2 to −40…+105 °C, Grade 3 to −40…+85 °C. Wymaganie SYS-ENV-003b odwołuje się do tych klas zamiast do luźnych wartości z kart |
| **ISO 16750-2** | Lista prób elektrycznych: przepięcie, nakładający się przebieg AC, powolny i gwałtowny spadek napięcia, zachowanie przy resecie, profil rozruchu, zrzut obciążenia, odwrotna polaryzacja, przesunięcie masy, rozwarcie, zwarcie |
| **ISO 16750-3** | Struktura profili wibracji i udarów |
| **ISO 16750-4** | Struktura wymagań temperaturowych, cykli termicznych, wilgotności i szczelności |
| **ISO 7637-2** | Zestaw impulsów testowych na linii zasilania |

**Dlaczego wartości nie pochodzą z norm.** Normy są pisane dla samochodów, a **zrzut obciążenia skaluje się z wydajnością alternatora**: stator 150–200 W daje zaburzenie o rząd wielkości mniejsze niż alternator samochodowy 1–2 kW. Przyjęcie wartości samochodowych oznaczałoby przepłacenie za ochronę wejścia zaprojektowaną pod zjawisko, które w tym motocyklu nie wystąpi.

### 13.1 Obwiednia napięciowa (decyzje Pawła 18.10.2026)

**Instalacja odniesienia:** regulator **Arrowhead AKM6000** = zamiennik **Shindengen SH721AA** (Beta 2728101000, KTM/Husqvarna 80011034000) — **jednofazowy, tyrystorowy, bocznikowy**, ten sam na całej platformie docelowej. Akumulator **kwasowy / AGM / żelowy, zawsze podłączony**. Rozruch awaryjny **wyłącznie kopniakiem**.

**Dlaczego samochodowy zrzut obciążenia 101 V tu nie występuje:** powstaje w alternatorze z uzwojeniem wzbudzenia, którego pole wygasa setki milisekund. Stator z magnesami trwałymi z regulatorem bocznikowym jest zwierany co półokres — mechanizm długiego impulsu nie istnieje. Realne zagrożenia: **awaria regulatora** i **poluzowany zacisk akumulatora**.

Wartości normowe za: Analog Devices, LT Journal v26n4 (ISO 16750-2, ISO 7637-2, instalacja 12 V).

| Zdarzenie | Norma | Nasza wartość | Wymagane zachowanie | Wymaganie |
|---|---|---|---|---|
| Zakres pracy | 6–16 V | 9–16 V pełna funkcja, 7–18 V sterowanie silnikiem, rozruch od 7 V | Bez zmian | SYS-ENV-001, -002, ECU-IGN-021 |
| Awaria regulatora — przepięcie | 18 V / 60 min | **18 V ciągle** | Praca; ostrzeżenie od 17 V i wentylator jako obciążenie | SYS-ENV-002, ECU-PWR-009 |
| Odwrotna polaryzacja | −14 V / 60 s | **−14 V / 60 s** | Przetrwać bez uszkodzenia i bez przepalenia bezpiecznika | SYS-ENV-008 |
| Zrzut obciążenia ograniczony (poluzowany zacisk) | 35 V / 400 ms | **35 V / 400 ms — wartość wstępna**, korekta po pomiarze napięcia jałowego uzwojenia ładującego | Przetrwać; praca nie wymagana | SYS-ENV-009 |
| Impulsy przewodzone | 1: −150 V/10 Ω/2 ms; 2a: +112 V/2 Ω/50 µs; 3a/3b: −220/+150 V/50 Ω/150 ns | Te same poziomy | 1, 3a, 3b: przetrwać, dopuszczalny reset; 2a: praca bez zakłóceń | SYS-ENV-010 |
| Tętnienia nałożone | 1–4 Vpp, 50 Hz–25 kHz | **Z pomiaru tętnień na akumulatorze ×2** | Praca bez zakłóceń | Pomiar w sesji |
| Zapad | 4,5 V / 100 ms | **Akceptowane ograniczenie** | ECU może zasnąć (TJA1043: VCC < ~3,5 V przez > 100 ms); ponowne naciśnięcie przycisku je budzi. Rozrusznik i tak by się zatrzymał | Instrukcja |
| Rozruch z kabli 24 V | 24 V / 60 s | **Poza zakresem** | Instrukcja: nie używać źródeł 24 V | — |

**Konsekwencje dla ochrony wejścia (rozdz. 4.4):**
- **TVS dwukierunkowy** — jednokierunkowy przy odwróconym akumulatorze przewodzi jak dioda i ginie albo przepala bezpiecznik
- Napięcie pracy TVS powyżej 18 V ciągłej pracy; napięcie ograniczania i energia dobrane pod zrzut 35 V / 400 ms oraz impulsy 1 i 2a — obliczenie energii jako dowód (SYS-ENV-010)
- **Wszystko na wejściu, przed TVS i za nim, ≥ 40 V**: przetwornice, dioda, kondensatory wejściowe. TJA1043 ma 58 V
- Odrzucony duży kondensator podtrzymujący na zapad 4,5 V: 7–23 mF, upływ elektrolitu do ~1 mA przy limicie uśpienia 150 µA, prąd udarowy, starzenie w +85 °C — przy zysku jednego naciśnięcia przycisku

**Do sesji pomiarowej** (`measurements/pomiar-wzbudzajacego.md`): napięcie i tętnienia na akumulatorze przy kilku obrotach; napięcie przemienne jałowe uzwojenia ładującego z odpiętym regulatorem — najgorszy przypadek awarii regulatora i podstawa korekty 35 V.
