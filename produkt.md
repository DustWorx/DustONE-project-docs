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
| Tor zapłonu | **AC-CDI — blok dyskretny** | ⚠️ do doboru | ⚠️ do kwalifikacji | Prostownik WN, kondensator zapłonowy, tyrystor, rezystor rozładowujący, ochrona przepięciowa; **bramka tyrystora sprzężona pojemnościowo** (ECU-IGN-005), **bramka AND w torze impulsu**: impuls z HRTIM × zezwolenie z komparatora kill switcha, rezystory ściągające na obu wejściach (ECU-SAF-001, -016; decyzja Pawła 1.11.2026 — zastępuje tranzystor zwierający bramkę do katody), **dzielnik napięcia uzwojenia wzbudzającego** do ADC (ECU-SAF-021); **dwa łańcuchy rezystorów na kondensatorze**: rozładowujący (ECU-IGN-026) i pomiarowy do ADC, próbkowany sprzętowo przed iskrą (ECU-IGN-028, -029; decyzja Pawła 1.11.2026). Dobór i arkusze kwalifikacji w O-001 — elementy istotne dla bezpieczeństwa. **VBG08H-E usunięty 15.10.2026** |
| Driver wtryskiwaczy | **TLE9104SH** | TLE9104SHXUMA1 | ✅ Aktywny, AEC-Q100/101 | Historia doboru: L9960 (błąd — mostek H do silników DC) → TLE8104E (funkcjonalnie dobry, **status NRND**) → TLE9104SH. Dane wtryskiwaczy KTM TPI/TBI: 11,7 Ω nom., prąd ~1,23 A przy 14,4 V = wysokoimpedancyjne, **peak-and-hold niepotrzebne, wystarcza tryb nasycony**. 4 kanały low-side (2 na wtryskiwacze, 2 zapas), 3 A/kanał, SPI z diagnostyką. Pin EN jest punktem sprzętowego bramkowania od kill switcha |
| Transceiver CAN ×2 | **TJA1043** | ⚠️ do ustalenia | ✅ Aktywny, AEC-Q100 (strona NXP) | TJA1051T/3 odrzucony — nie ma wybudzania przez magistralę. **Od 18.10.2026 steruje zasilaniem: wyjście INH włącza obie przetwornice, w uśpieniu (Sleep) czuwa sam z pinu BAT, 18 µA typ. / 30 µA maks.** Reguły schematu: rozdz. 6.2. Ten sam układ w ECU i HMI. **NXP wskazuje TJA1443A jako następcę** — zgodność do sprawdzenia przy doborze pełnego numeru (Faza 4) |
| Akcelerometr (dawniej IMU) | **ST AIS2IH** | AIS2IHTR | ✅ **AEC-Q100** (karta DS12421 rev. 4, str. 1); **−40…+115 °C** — warunkowo wobec SYS-ENV-003b (założenie Z17); aktywny, dostępność deklarowana przez ST do 01/2033 | **Decyzja Pawła 25.10.2026: sam akcelerometr, bez żyroskopu** — żyroskopy MEMS są wrażliwe na drgania (przesunięcie zera → dryf kąta), a wywrotka to kąt grawitacji w spoczynku. Zakres **±16 g** (czarna skrzynka), odporność na udar 10 000 g (0,2 ms, bez zasilania), filtr pasma ODR/2…ODR/20 jako antyaliasing, samotest, dryf zera ±0,2 mg/°C, SPI, LGA-12 2×2 mm. Zasilany z szyny 3,3 V — w uśpieniu bez zasilania. **Czego nie robi:** nie liczy kąta (robi to MCU); nie mierzy powyżej ±16 g (wypadek ponad zakres = nasycenie); nie jest elementem bezpieczeństwa funkcjonalnego (ST: zastosowania motoryzacyjne bez funkcji bezpieczeństwa). **Zapasowy:** Murata SCA3300-D01-1 (−40…+125 °C, ±6 g, bez deklaracji AEC-Q). Odrzucone: BMI090L, IAM-20381HT (Grade 2, 105 °C), ADXL317 (I²S, 5 mA), SMA130 (85 °C), AIS3624DQ (wycofany), FXLS8964/67 (105 °C) |
| Pamięć logów | **W25Q64** (8 MB, SPI NOR) | ⚠️ rodzina, nie numer | ⚠️ klasa przemysłowa | Czarna skrzynka, 8 MB z zapasem; wlutowana, bez slotu. Pełny numer i klasa do ustalenia (O-063) |
| Wyjścia pomocnicze | BTS7008-2EPA ×3 | ⚠️ do ustalenia | AEC-Q100 | PROFET+2, 6 kanałów, diagnostyka, ochrona zwarciowa i odwrotnej polaryzacji. **7,5 A/kanał to wartość nominalna w określonych warunkach, nie dopuszczalny prąd roboczy dowolnego obciążenia** |
| Kondycjoner VR/Hall | **MAX9926** | MAX9926UAEE/V+ | ✅ Production, −40…+125 °C, automotive | Adaptacyjny próg 33% poprzedniego szczytu, detekcja przejścia przez zero, czułość od 20 mV, odporność na pominięty ząb. **Pobór 4,7 mA typ./10 mA max, brak trybu shutdown** — w uśpieniu odcinany razem z VDD5 PMIC (od 1.11.2026; wcześniej przełącznikiem obciążenia). Wersja dwukanałowa; jednokanałowy MAX9924 jest mniejszy i tańszy. Jedyna pozycja niedostępna w TME (O-033) |
| Ciśnienie atmosferyczne | **Infineon KP464** | KP464XTMA1 / KP464EXTMA1 — do ustalenia przy zakupie | ✅ **AEC-Q103-002** (karta rev. 1.20, str. 1) — standard AEC dla czujników MEMS; **−40…+125 °C** | **Montowany od początku na PCB MVP-A** (decyzja Pawła 25.10.2026). W MVP-A tylko logowanie ciśnienia i wysokości; korekta dawki w B/C. Zakres 40–115 kPa, ±1,0 kPa (0…85 °C), ±1,5 kPa na krańcach; SPI 16-bit; zasilanie 3,0–5,25 V, 3,5 mA aktywnie, 10 µA w power-down; start 5–10 ms; diagnostyka toru sygnału, komórki i EEPROM. **Uwagi z karty:** czuły na światło > 1 lx (obudowa nieprzezroczysta, membrana nieprzepuszczająca światła); pin VPROG wyłącznie do programowania EEPROM — podłączenie wg angielskiej karty. **Wymaga otworu ciśnieniowego z membraną IP67 w obudowie.** ⚠️ Dostępność: Farnell — 52 tyg. i MOQ 3400 szt. dla KP464E; dostępność w małych ilościach do sprawdzenia (TME → Mouser → Farnell → DigiKey) w Fazie 4. BMP390 odrzucony (bez kwalifikacji, 85 °C) |
| Pozycja biegu | MLX90316 | ⚠️ do ustalenia | ⚠️ do potwierdzenia | Triaxis, bezstykowy, kąt magnesu 0–360°, wyjście analogowe. **Wykonalność mechaniczna na Becie niepotwierdzona (O-031)** |
| **PMIC — zasilanie, nadzór szyn, watchdog** | **TI TPS65381A-Q1** | TPS65381AQDAPRQ1 | ✅ ACTIVE, AEC-Q100 Grade 1, TA −40…+125 °C | **Decyzja Pawła 1.11.2026 (O-018)**, arkusz w rozdz. 4.5. Przetwornica wstępna 6 V → **VDD5** 5,0 V ±2 % (TJA1043 VCC, MAX9926, komparator, bramka AND), **VDD3/5** 3,3 V (procesor, pamięć, AIS2IH, TJA1043 VIO, próg tranzystorowy), **VSOUT1** 5 V ±3 % dla czujników w wiązce (ochrona przed zwarciem do masy i akumulatora, domyślnie wyłączone). Nadzór UV/OV wszystkich szyn z osobnym źródłem odniesienia, watchdog, **ENDRV** → bramka AND zapłonu, blokada PROFET rozrusznika, **(B/C) EN TLE9104 i PROFET pompy**, **NRES** → reset procesora. **Wejście IGN z INH TJA1043** przez ≥ 10 kΩ. STANDBY ≤ 75 µA. Zastępuje: przetwornice 5,0 V i 3,3 V, TPS3430-Q1, przełącznik obciążenia 5 V |
| **Czujniki temperatury wnętrza ECU** | 2× termistor NTC, AEC-Q200 | do doboru (Faza 4) | AEC-Q200 | Przy bloku CDI i w sekcji mocy (PROFET-y, PMIC). Razem z czujnikiem w MCU realizują ochronę termiczną ECU-SAF-020 (T1/T2/T3) i dane do logu z jazdy (A8, Z17). Dzielnik z szyny wyłączanej w uśpieniu — 0 µA w bilansie 6.1 (decyzja Pawła 25.10.2026) |
| **Komparator kill switcha** | do doboru | — | — | Daje **zezwolenie dla impulsu bramki tyrystora** (bramka AND, od 1.11.2026), bramkuje wejścia EN driverów i **wejście PROFET kanału rozrusznika** (ECU-SAF-019). **Klucz masy rozrusznika i zwarcie uzwojenia wzbudzającego steruje osobny próg tranzystorowy** (1.11.2026, B.1.3) sygnałem kill switcha, niezależnie od firmware (od 25.10.2026). Jeden próg między poziomem RUN a STOP układu trzypoziomowego — odcina i przy naciśnięciu, i przy przerwie w przewodzie. Zasilany z **VDD5 PMIC** — w uśpieniu wyłączony razem z PMIC (od 1.11.2026). **Komparator wewnętrzny procesora świadomie odrzucony**: jest konfigurowany przez firmware, a to dokładnie ta zależność, którą zakwestionował audyt |
| **Próg tranzystorowy kill switcha** | dyskretny, do doboru | — | elementy do kwalifikacji (próg zależy od Vbe i rezystorów — pola 4, 6 arkusza) | **Drugi, niezależny od komparatora układ czytający przewód kill switcha** (decyzja Pawła 1.11.2026). Steruje kluczem zwierającym uzwojenie wzbudzające, blokadą klucza masy rozrusznika i **(B/C) wejściem RESN TLE9104**. Utknięcie jednego z progów w RUN nie znosi wszystkich blokad. Zasilanie z innej szyny niż komparator — propozycja VDD3/5 (3,3 V), do potwierdzenia przy schemacie. Wyjście odczytywane przez procesor (ECU-SAF-021) |
| **Podciągnięcie drabinki kill switcha** | rezystor | — | — | **Z VDD5 (szyna wewnętrzna), nigdy z VSOUT1** (reguła 1.11.2026): kill switch nie może zależeć od zasilania czujników w wiązce. Wariant Hall czujnika wału (zworka, rozdz. 2.4) potrzebuje zasilania — źródło do rozstrzygnięcia przy wariancie Hall: VSOUT1 (zwarcie w wiązce innego czujnika gasi silnik) albo VDD5 (brak ochrony przed zwarciem do akumulatora) |
| **Klucz masy cewki przekaźnika rozrusznika** | do doboru | — | — | Zamknięty tylko przy **fizycznie wciśniętym przycisku START** i RUN z progu tranzystorowego (ECU-SAF-022, poprawka 1.11.2026). Sygnał przycisku idzie w trzy miejsca: wejście WAKE transceivera, wejście procesora, ten klucz |
| **Kwarc LSE** | 32,768 kHz | do doboru | AEC-Q200 | Zegar RTC — znaczniki czasu w logach, motogodziny (decyzja Pawła 3.11.2026). LSI ma rozrzut rzędu procent, a errata ES0430 (2.2.4) opisuje jego niestabilność przy taktowaniu RTC. Piny PC14/PC15; PC13 nie może się przełączać (errata 2.2.8) |
| Rezonator HSE | 8 MHz | do doboru | AEC-Q200, −40…+125 °C | Przy 10 000 obr/min błąd kwarcu ±50 ppm to ~0,3 µs ≈ **0,002° kąta wału** — kilkaset razy mniej niż tolerancje mechaniczne koła (0,5–1°). TCXO niepotrzebny |
| ~~Watchdog zewnętrzny TPS3430-Q1~~ | — | — | — | **Usunięty 1.11.2026** razem z przetwornicami i przełącznikiem obciążenia — watchdog i nadzór szyn w PMIC. TPS3430 nie nadzorował napięcia i odcinał wyjścia tylko przez reset procesora (`firmware.md` B.1.3) |
| Podtrzymanie RTC | Superkondensator 0,1–0,47 F | — | — | Procesor ma wbudowany RTC. Podtrzymanie działa tylko przy odłączonym akumulatorze (serwis, zimowanie); superkondensator zamiast baterii — brak wymiany po latach. **Rozładowany superkondensator przy starcie zachowuje się jak zwarcie** — wymagany rezystor ograniczający. Prąd upływu dolicza się do budżetu uśpienia |
| Złącze główne | **do wyboru przez Pawła — większe niż 28 obwodów** (decyzja 3.11.2026) | — | IP67, −40…+125 °C | Bilans z 3.11.2026 (rozdz. 5): **≥ 22 styki sygnałowe (≤ 2,5 A), ≥ 5 średnie (12 A), 2–3 duże (21 A)**, razem 29–30, plus zapas. Molex CMC 28 (18× 0,635 + 5× 1,50 + 5× 2,80 mm) nie mieści styków sygnałowych. NTSEAL 26 odrzucony wcześniej — zero rezerwy |
| **Złącze zapłonu** | do wyboru, 3–4 piny | — | IP67, odstępy WN (ECU-IGN-027) | **Decyzja Pawła 3.11.2026:** wysokie napięcie i impulsy prądu zapłonu fizycznie oddzielone od sygnałów. Wyjście na cewkę (CDI w A, TCI w B/C), uzwojenie wzbudzające (A, 1–2 piny), masa mocy zapłonu |
| **Przełącznik zasilania HMI** | do doboru | — | — | **Domyślnie załączony** (decyzja Pawła 3.11.2026, ECU-PWR-011): HMI zasilane także w uśpieniu, więc jego przyciski budzą system; pracujące ECU może odłączyć HMI (restart, zwarcie w kablu). Ochrona zwarciowa. Pobór w uśpieniu ≤ 5 µA (przydział, rozdz. 6.1) |
| Złącze USB | USB-C | — | — | Uszczelnione lub standardowe z zaślepką IP67. Wymaga rezystorów 5,1 kΩ na liniach CC (tryb urządzenia) |
| Ochrona wejścia | TVS, ochrona odwrotnej polaryzacji, filtr LC, PTC | do doboru | — | Patrz rozdz. 4.4 |

**6 kanałów PROFET:** wentylator, przekaźnik rozrusznika, światła, pompa paliwa, aux ×2.

### 3.1 Przydział pinów procesora STM32G474VET3 (O-028, 3.11.2026)

**Metoda:** wszystkie sygnały z dokumentacji (warianty A, B i C) przydzielone programem `scripts/piny_mcu.py` na danych pinów producenta (ST, `STM32_open_pin_data`, baza CubeMX). Wynik: **70 sygnałów na 84 użyteczne piny I/O, 14 wolnych**; wszystkie peryferia mieszczą się jednocześnie.

**Ograniczenia przyjęte w przydziale:**
- USB zajmuje PA11/PA12, więc **FDCAN1 na PD0/PD1** (trzecia opcja, PB8/PB9, koliduje z BOOT0);
- **zapłon i oba wtryskiwacze na różnych jednostkach czasowych HRTIM** (E, F, A) — niezależny licznik i okres dla każdej funkcji;
- sygnał wału na zdarzeniu zewnętrznym HRTIM z filtrem cyfrowym (EEV6–10);
- **PMIC na osobnej SPI3** (decyzja Pawła 3.11.2026) — usterka magistrali czujników nie zablokuje obsługi watchdoga;
- **PB8-BOOT0 i NRST nieużywane jako GPIO; PC13 wolny i statyczny** (errata 2.2.8 — przełączanie zaburza kwarc LSE); PB4 (NJTRST) użyty jako GPIO — debug wyłącznie przez SWD (errata 2.2.1);
- piny PROFET (IN, DEN, DSEL, IS) przyjęte dla BTS7008-2EPA — **do potwierdzenia z kartą** przy arkuszu kwalifikacji (O-063).

| Pin | Nr | Funkcja | Peryferium |
|---|---|---|---|
| PF0-OSC_IN | 12 | Kwarc 8 MHz | RCC_OSC_IN |
| PF1-OSC_OUT | 13 | Kwarc 8 MHz | RCC_OSC_OUT |
| PC14-OSC32_IN | 8 | Kwarc 32,768 kHz — RTC (decyzja 3.11.2026) | RCC_OSC32_IN |
| PC15-OSC32_OUT | 9 | Kwarc 32,768 kHz | RCC_OSC32_OUT |
| PA14 | 77 | SWD | SYS_JTCK-SWCLK |
| PA13 | 76 | SWD — programowanie bootloadera (ECU-BTL-006) | SYS_JTMS-SWDIO |
| PA11 | 72 | USB-C | USB_DM |
| PA12 | 73 | USB-C | USB_DP |
| PC6 | 65 | Sygnał wału z MAX9926 / Halla — start timera zapłonu (ECU-IGN-023); EEV z filtrem cyfrowym | HRTIM1_EEV10 |
| PC8 | 67 | Impuls bramki tyrystora (A) / sterowanie drivera TCI (B/C) — przez bramkę AND; timer E | HRTIM1_CHE1 |
| PB7 | 94 | Przechwycenie rzeczywistego wyzwolenia (ECU-IGN-024) | HRTIM1_EEV3 |
| PC7 | 66 | TLE9104 IN1 — wtryskiwacz 1 (B/C); timer F | HRTIM1_CHF2 |
| PA8 | 69 | TLE9104 IN2 — wtryskiwacz 2 (B/C); timer A | HRTIM1_CHA1 |
| PD4 | 86 | Faza wałka — rezerwa 4T | TIM2_CH2 |
| PD0 | 82 | TJA1043 RXD (FDCAN1; PA11/PA12 zajęte przez USB) | FDCAN1_RX |
| PD1 | 83 | TJA1043 TXD | FDCAN1_TX |
| PA6 | 28 | W25Q64 | SPI1_MISO |
| PA7 | 29 | W25Q64 | SPI1_MOSI |
| PA5 | 27 | W25Q64 (pamięć logów) | SPI1_SCK |
| PB14 | 53 | jw. | SPI2_MISO |
| PB15 | 54 | jw. | SPI2_MOSI |
| PF10 | 11 | AIS2IH, KP464, TLE9104 (B/C) | SPI2_SCK |
| PE1 | 98 | Prędkość koła — przechwytywanie timera | TIM17_CH1 |
| PC11 | 80 | PMIC | SPI3_MISO |
| PC12 | 81 | PMIC | SPI3_MOSI |
| PC10 | 79 | PMIC — osobna magistrala (decyzja 3.11.2026) | SPI3_SCK |
| PE12 | 43 | Temperatura powietrza | ADC3_IN16, ADC4_IN16 |
| PC0 | 15 | Napięcie kondensatora zapłonowego, próbka z HRTIM (ECU-IGN-028) | ADC1_IN6, ADC2_IN6 |
| PC1 | 16 | Temperatura cieczy | ADC1_IN7, ADC2_IN7 |
| PC4 | 30 | Napięcie uzwojenia wzbudzającego (ECU-SAF-021) | ADC2_IN5 |
| PD8 | 55 | Pozycja biegu MLX90316 | ADC4_IN12, ADC5_IN12 |
| PE13 | 44 | PROFET 1 — prąd (IS) | ADC3_IN3 |
| PD13 | 60 | PROFET 2 — prąd (IS) | ADC3_IN10, ADC4_IN10 |
| PE14 | 45 | PROFET 3 — prąd (IS) | ADC4_IN1 |
| PE7 | 38 | Drabinka kill switcha (B.2.5.1) | ADC3_IN4 |
| PE9 | 40 | NTC przy bloku CDI (ECU-SAF-020) | ADC3_IN2 |
| PE11 | 42 | NTC w sekcji mocy | ADC3_IN15, ADC4_IN15 |
| PE8 | 39 | Rezerwa B/C — czujnik ciśnienia (O-060) | ADC3_IN6, ADC4_IN6 |
| PD9 | 56 | PMIC DIAG_OUT | ADC4_IN13, ADC5_IN13 |
| PA4 | 26 | TPS (B/C) | ADC2_IN17 |
| PE15 | 46 | Napięcie akumulatora | ADC4_IN2 |
| PD14 | 61 | Szyna VDD5 (ECU-PWR-008a) | ADC3_IN11, ADC4_IN11 |
| PC2 | 17 | Zasilanie czujników VSOUT1 (ECU-PWR-008b) | ADC1_IN8, ADC2_IN8 |
| PE0 | 97 | AIS2IH — przerwanie danych | GPIO |
| PD15 | 62 | Odczyt zwrotny komparatora kill (ECU-SAF-021/024) | GPIO |
| PD7 | 89 | CS AIS2IH | GPIO |
| PD5 | 87 | CS W25Q64 | GPIO |
| PF2 | 19 | CS KP464 | GPIO |
| PD6 | 88 | CS PMIC | GPIO |
| PD2 | 84 | CS TLE9104 (B/C) | GPIO |
| PB1 | 33 | Odłączenie zasilania HMI (ECU-PWR-011) | GPIO |
| PE5 | 4 | Odczyt zwrotny ENDRV | GPIO |
| PE4 | 3 | PMIC ERROR/WDI — watchdog | GPIO |
| PB11 | 50 | PROFET 1 — DEN | GPIO |
| PB6 | 93 | PROFET 2 — DEN | GPIO |
| PA0 | 20 | PROFET 3 — DEN | GPIO |
| PB0 | 32 | PROFET — DSEL (wspólny) | GPIO |
| PF9 | 10 | PROFET — wentylator | GPIO |
| PD10 | 57 | PROFET — przekaźnik rozrusznika (× komparator × ENDRV) | GPIO |
| PD12 | 59 | PROFET — światła | GPIO |
| PE10 | 41 | PROFET — pompa (B/C, × ENDRV) | GPIO |
| PC3 | 18 | PROFET — aux 1 | GPIO |
| PC5 | 31 | PROFET — aux 2 | GPIO |
| PE3 | 2 | Przycisk START | GPIO |
| PE6 | 5 | Odczyt zwrotny progu tranzystorowego | GPIO |
| PE2 | 1 | TJA1043 EN | GPIO |
| PC9 | 68 | TJA1043 ERR_N (pull-up wewn.) | GPIO |
| PD3 | 85 | TJA1043 STB_N (bez rezystora — Z16) | GPIO |
| PD11 | 58 | TLE9104 EN — żądanie MCU (× komparator × ENDRV) | GPIO |
| PB4 | 91 | Prędkość koła — przełączany podciągacz | GPIO |

**Wolne (14):** PA1, PA10, PA15, PA2, PA3, PA9, PB10, PB12, PB13, PB2, PB3, PB5, PB9, PC13.


**Do zrobienia przy schemacie:** odtworzenie przydziału w projekcie CubeMX (konfiguracja zegarów, DMA, wyzwalaczy ADC z HRTIM) i potwierdzenie rewizji krzemu (Z, Y albo X) przy zakupie — od niej zależy lista obowiązujących obejść (`firmware.md` I).

---

## 4. Zasilanie

### 4.1 Topologia (od 1.11.2026 — PMIC TPS65381A-Q1)

```
12 V B+ ─► ochrona wejścia (TVS) ─► dioda Schottky'ego (gałąź logiki) ─► filtr LC ─┬─► 1 kΩ + 10 nF ─► TJA1043 BAT
                                                                                │       (czuwa zawsze, ~18 µA w Sleep)
                                                                                │              │ INH ─► ≥ 10 kΩ ─┐
                                                                                │                                ▼ IGN
                                                                                └─► TPS65381A-Q1: przetwornica wstępna 6 V
                                                                                      ├─► VDD5 5,0 V ─► TJA1043 VCC, MAX9926, komparator, bramka AND
                                                                                      ├─► VDD3/5 3,3 V ─► MCU, pamięć, AIS2IH, TJA1043 VIO, próg tranzystorowy
                                                                                      │                    └─► filtr LC ─► VDDA/VREF+
                                                                                      ├─► VSOUT1 5 V ─► czujniki w wiązce (ochrona zwarć, domyślnie wyłączone)
                                                                                      ├─► ENDRV ─► bramka AND zapłonu, blokada PROFET rozrusznika
                                                                                      └─► NRES ─► reset MCU

W uśpieniu: INH niesterowane → IGN niski → PMIC w STANDBY, wszystkie szyny wyłączone (rozdz. 6)
```

**PMIC zamiast dwóch przetwornic, watchdoga i przełącznika obciążenia (decyzja Pawła 1.11.2026, O-018).** Powód: w poprzedniej topologii watchdog odcinał wyjścia tylko przez reakcję procesora na reset, nic niezależnego nie nadzorowało szyny 3,3 V, a przełącznik obciążenia był wspólny dla czujników w wiązce i kondycjonera wału (`firmware.md` B.1.3). PMIC daje sprzętowe ENDRV, nadzór wszystkich szyn i osobne, chronione zasilanie czujników. Arkusz kwalifikacji: rozdz. 4.5.

**Koszt tej decyzji:** regulatory liniowe pracują z 6 V — ok. +0,2 W strat (szacunek, rozdz. 9.2); zapas bilansu uśpienia spada do 22 µA (rozdz. 6.1); firmware obsługuje PMIC przez SPI i musi przejść stan DIAGNOSTIC w 512 ms przy każdym wybudzeniu (`firmware.md` A.4). Tętnienia przetwornicy wstępnej filtrują regulatory liniowe; filtr LC dla części analogowej procesora zostaje.

**Zastąpiona topologia (18.10–1.11.2026):** dwie przetwornice z wejściami EN sterowanymi z INH, TPS3430-Q1, przełącznik obciążenia 5 V.

**Odrzucona konsolidacja w układ SBC** (transceiver + regulator + watchdog + zarządzanie uśpieniem w jednej obudowie, np. UJA1169A): regulator w SBC jest liniowy i pracuje bezpośrednio z 12 V, co przywraca problem termiczny rozwiązany architekturą dwustopniową. Dodatkowo warianty z regulatorem 3,3 V nie mają wyjścia 5 V dla czujników zewnętrznych, a warianty z tym wyjściem mają regulator 5 V — nie da się mieć obu naraz. **PMIC TPS65381A-Q1 tego problemu nie ma:** regulatory liniowe pracują z przetwornicy wstępnej 6 V, nie z 12 V, a szyny 5 V i 3,3 V są osobne.

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
| Nadzór szyn w PMIC (od 1.11.2026) | Podnapięcie i przepięcie każdej szyny, z osobnym źródłem odniesienia. **Reakcja sprzętowa**: ENDRV albo reset procesora, bez udziału firmware; stan dostępny dla firmware w rejestrach statusu |
| Włączanie zasilania czujników VSOUT1 | Bit w PMIC, domyślnie wyłączone; ograniczenie prądu i ochrona przed zwarciem do akumulatora w PMIC. Bezpieczny kierunek sterowania |

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

**Warstwa 3 — wyjścia mocy:** diody gaszące na obciążeniach indukcyjnych (PROFET ma wbudowane ograniczanie, zewnętrzne diody go odciążają); **tor AC-CDI: obwód tłumiący na tyrystorze, rezystor bramka–katoda przeciw samoczynnemu załączeniu, odstępy izolacyjne dla napięć setek woltów (ECU-IGN-027), sekcja WN odseparowana na PCB** (zmiana 25.10.2026).

**Warstwa 4 — konstrukcja PCB:** ciągła płaszczyzna masy rozdzielona na sekcję analogową i mocy z jednym punktem połączenia; fizyczne oddzielenie sekcji zapłonu i PROFET od analogowej; kondensatory odsprzęgające przy każdym układzie; sygnały analogowe z dala od ścieżek przełączających duże prądy; do rozważenia ekran metalowy nad sekcją analogową.

⚠️ **Architektura powrotów prądowych i ekranowania musi być ustalona przed PCB (O-039).** Późne wykrycie nieodpornego wejścia VR wymusi zmianę płytki i złączy.

### 4.5 Kandydat: PMIC TI TPS65381A-Q1 — arkusz kwalifikacji (1.11.2026, O-018 punkty 2–4)

**Status: arkusz kompletny z pełnej karty SLVSDJ1A (rev. A, maj 2017; strony wg numeracji PDF) i instrukcji bezpieczeństwa SLVA528D. Przyjęty — decyzja Pawła 1.11.2026 (O-018).**

| # | Pole | Wartość | Źródło |
|---|---|---|---|
| 1 | Numer zamówieniowy | **TPS65381AQDAPRQ1** (taśma), TPS65381AQDAPTQ1 (mała taśma); HTSSOP-32 PowerPAD | karta SLVSDJ1A; strona produktu TI |
| 2 | Cykl życia | **ACTIVE**, sprawdzone 1.11.2026 | strona produktu TI |
| 3 | Kwalifikacja | **AEC-Q100, Grade 1** | strona produktu TI; karta rozdz. 1 |
| 4 | Temperatura | TA −40…+125 °C, TJ ≤ 150 °C — obejmuje SYS-ENV-003 (−40…+50 °C) z dużym zapasem. RθJA 26,3 K/W (płytka JEDEC high-K) | karta, warunki zalecane i dane cieplne |
| 5 | Zasilanie i pobór | Z akumulatora: VBATP, VBAT_SAFING, VSIN. **STANDBY ≤ 75 µA maks.** (R1.5: IGN = CANWU = 0 V, 5,8–20 V, TJ < 85 °C; wartości typowej karta nie podaje). Pobór własny w ACTIVE — **karta nie podaje** (pobór = obciążenia szyn przez przetwornicę 6 V). Praca pełna od 5,8 V przy starcie; po starcie do 4,5 V (VDD3/5 w wersji 3,3 V działa dalej) | karta s. 8 |
| 6 | Piny sterujące i stan bez sterowania | **IGN:** budzenie stanem wysokim, filtr 7,5–22 ms, opcjonalne podtrzymanie (bit IGN_PWRL). **CANWU:** impuls ≥ 350 µs, zatrzaskiwany. **NRES:** otwarty dren, aktywny niski, pull-up wewn. 3–6 kΩ. **ENDRV:** otwarty dren, pull-up wewn. 4,5 kΩ do VDDIO; wysoki tylko przy WD_FAIL_CNT ≤ 4, ustawionym bicie ENABLE_DRV i braku przepięcia szyn — **wraca sam**, gdy warunki ustąpią. **RSTEXT rozwarty = układ stale w RESET** (bezpieczny kierunek) | karta s. 8, 15, 22–23, 38–39, 62; forum TI E2E |
| 7 | Zanik szyn | VDD3/5 poza UV/OV → ENDRV niski (VDD3/5 5 V: UV → RESET). VBATP < 4,2–4,5 V → wyłączenie. VBATP > 34,7–36,7 V → domyślnie RESET (maskowalne bitem MASK_VBATP_OV) | karta s. 8, 12, 26–28 |
| 8 | Limity ochron | UV/OV VDD3/5 3,3 V: 3,00–3,17 / 3,43–3,60 V; VDD5: 4,50–4,85 / 5,20–5,45 V. **VSOUT1:** ograniczenie 120–500 mA, zwarcie do −2…18 V bez uszkodzenia, wyłączenie termiczne 175–210 °C, strata ≤ 0,6 W. Maks. bezwzględne VBATP 40 V, zalecane ≤ 34 V. **Spadki napięcia:** VDD6 ≤ 0,6 V (przy 1,3 A; poniżej 7 V wypełnienie 100 %), VDD5 ≤ 0,3 V, VSOUT1 ≤ 0,75 V (przy 100 mA); VDD6 5,4–6,6 V. **Przy 7 V na złączu** (ECU-IGN-021): 7 − 0,5 (dioda) − 0,6 = 5,9 V na VDD6 w najgorszym przypadku → VDD5 5,0 V ✅, VSOUT1 5,0 V ✅ z zapasem 0,15 V. ⚠️ **VSOUT1 nastawione na 5 V nie ma gwarancji pełnego napięcia przy VDD6 = 5,4 V i obciążeniu 100 mA** (5,4 − 0,75 = 4,65 V) — przy naszym obciążeniu rzędu kilkudziesięciu mA zapas jest większy, ale pomiary ratiometryczne muszą odnosić się do zmierzonego VSOUT1 (O-025) | karta s. 7, 10, 12, 19–20 |
| 9 | Timery wobec wymagań | WD_FAIL_CNT startuje od 5; dobre zdarzenie −1, złe +1; ENDRV możliwy przy < 5, czyli po pierwszym dobrym zdarzeniu; reset przy 8. **Okna watchdoga:** okno 1 do 127 × 0,55 ms ≈ 70 ms, okno 2 do 32 × 0,55 ms ≈ 17,6 ms (krok 0,55 ms ±5 %). **ENDRV opada dopiero po 5 złych zdarzeniach netto** — przy sekwencji 20 ms to ~100 ms, czyli tyle co dzisiejsze okno TPS3430. Reset przy 8. zdarzeniu (WD_RST_EN). **Stan DIAGNOSTIC: 512 ms (typ.) na wyjście**, inaczej SAFE (ENDRV niski, procesor zasilony). Start z uśpienia: filtr IGN 7,5–22 ms + BIST 21 ms + przedłużenie resetu 1,4–4,5 ms + konfiguracja + jedno dobre zdarzenie watchdoga ≈ **45–65 ms do zezwolenia ENDRV** — mieści się w ≤ 200 ms (ECU-SAF-018) | karta s. 15, 22–23, 38–40, 66–68; SLVA528D rozdz. 5.3.1.2 |
| 10 | **Czego NIE robi** | (1) **Nie czyta kill switcha** — dwa układy progowe zostają. (2) **Nie ma transceivera CAN** — TJA1043 zostaje, INH → IGN. (3) **Nie chroni przed odwrotną polaryzacją i nie pracuje powyżej 34 V** — dioda i TVS zostają; praca w czasie zrzutu nie jest wymagana (SYS-ENV-009). (4) **ENDRV może utknąć w stanie wysokim** — instrukcja bezpieczeństwa TI sama zaleca drugą, niezależną ścieżkę odcięcia (mamy dwie). (5) Nadzór sygnału błędu MCU tylko w trybie Q&A watchdoga — więcej pracy w firmware. (6) **Nie reaguje natychmiast na zawieszenie procesora** — ENDRV opada po 5 złych sekwencjach watchdoga. (7) Każde wybudzenie wymaga obsługi stanu DIAGNOSTIC w 512 ms, inaczej SAFE | SLVA528D tab. 7-1, rozdz. 5.3.1.1; karta s. 66 |
| 11 | Dostępność | TME, Mouser, Farnell — nie potwierdzone w wyszukiwaniu 1.11.2026; DigiKey — pozycja 7244182, stan nie sprawdzony | wyszukiwanie 1.11.2026 |

**Zastępuje:** obie przetwornice, TPS3430-Q1 i przełącznik obciążenia 5 V. Rdzeń STM32G474 ma własny regulator — wyjście VDD1 niewykorzystane (karta: VDD1_G i VDD1_SENSE rozwarte, nadzór VDD1 domyślnie wyłączony).

**Co rozwiązuje w O-018:**
- **Punkt 2:** ENDRV jako trzecie wejście bramki AND i blokada rozrusznika — usterka watchdoga albo szyny odcina zapłon bez udziału procesora.
- **Punkt 3:** niezależny nadzór podnapięcia i przepięcia wszystkich szyn.
- **Punkt 4:** MAX9926, komparator i bramka AND na VDD5; czujniki w wiązce na VSOUT1, z ochroną przed zwarciem do masy i do akumulatora.

**Bilans uśpienia po zamianie (rozdz. 6.1):** 63 − 10 (dwie przetwornice) + 75 = **≤ 128 µA** wobec limitu 150 µA; z przełącznikiem zasilania HMI (3.11.2026) **≤ 133 µA**, zapas 17 µA.

**Termika — szacunek:** regulatory liniowe pracują z 6 V zamiast osobnych przetwornic — około +0,2 W względem rozdz. 9.2. Do przeliczenia z drzewa zasilania przy schemacie.

**Alternatywy:**
- **Infineon TLF35584** — przetwornica wstępna 3–40 V (lepsza przy 7 V), ale projektowany dla większych układów (LDO 600 mA, VQFN-48); poboru w uśpieniu przegląd produktu nie podaje. Odrzucony wstępnie.
- **Rozwiązanie dyskretne** — obecne przetwornice i TPS3430-Q1 z trzema poprawkami: wyjście watchdoga do bramki AND, Power Good 3,3 V do resetu procesora, kondycjoner i komparator przed przełącznikiem. Mniej pracy w firmware; nadzór szyn zależny od doboru przetwornic (Power Good zwykle tylko podnapięcie), ochrona zasilania czujników przed zwarciem do akumulatora zależna od doboru przełącznika, zwykły watchdog okienkowy.

**Do sprawdzenia przy zakupie:** dostępność TME → Mouser → Farnell (wyszukiwanie nie potwierdziło). **Do rozważenia przy schemacie:** zabezpieczenie przed odwrotną polaryzacją tranzystorem NMOS sterowanym pompą ładunku układu (karta s. 2, 19) zamiast diody Schottky'ego — mniejszy spadek przy niskim napięciu akumulatora.

---

## 5. Złącze i sygnały

**Bilans obwodów — przeliczony 3.11.2026 dla wariantów A, B i C (O-030).** Dwa złącza (decyzja Pawła): **złącze zapłonu** oddziela wysokie napięcie i impulsy prądu od sygnałów; **złącze główne** — większe niż 28 obwodów, typ do wyboru przez Pawła.

**Złącze główne:**

| Grupa | Obwody | Styki ≤ 2,5 A | Styki 12 A | Styki 21 A |
|---|---|---|---|---|
| Zasilanie ECU | B+ (szczyt ~12,6 A + aux), masa ECU | — | — | **2–3** (B+ podwójne, jeśli aux duże) |
| Zasilanie HMI (ECU-PWR-011) | +12 V przez przełącznik domyślnie załączony, masa HMI | 2 | — | — |
| Czujnik wału | VR+, VR− | 2 | — | — |
| Czujniki analogowe | temp. cieczy, temp. powietrza, bieg, TPS *(B/C)* | 4 | — | — |
| Wspólne czujników | +5 V (VSOUT1), masa czujników | 2 | — | — |
| Wejścia cyfrowe | start, kill, **wspólny powrót masy obu przycisków** (decyzja 3.11.2026), prędkość koła, faza wałka *(rezerwa 4T)* | 5 | — | — |
| Wtrysk *(B/C)* | wtryskiwacz 1, 2 (~1 A) | 2 | — | — |
| Rozrusznik | przekaźnik + (PROFET, ~0,3 A), **klucz masy przekaźnika** (ECU-SAF-022) | 2 | — | — |
| CAN | H, L | 2 | — | — |
| Rezerwa B/C | czujnik ciśnienia (O-060) | 1 | — | — |
| Wyjścia PROFET | wentylator (~6 A), pompa *(B/C, ~4 A)*, światła (~2 A), aux ×2 | — | 5 | — |
| **Razem** | **29–30** + zapas | **22** | **5** | **2–3** |

**Złącze zapłonu (3–4 piny, odstępy izolacyjne wg ECU-IGN-027):** wyjście na cewkę — wspólny pin, obsadzenie zależne od wariantu (impuls CDI w A, dolny klucz TCI ~6–8 A w B/C); uzwojenie wzbudzające (A; 1 pin, jeśli ma koniec na masie, 2 — jeśli pływające; pomiar krok 2); **masa mocy zapłonu** — wyładowanie CDI to impuls rzędu dziesiątek amperów (typowo, do potwierdzenia pomiarem), w B/C wraca nią prąd cewki; nie może iść przez masę logiki.

**Identyfikacja wariantu HMI — po CAN, bez pinu** (decyzja Pawła 3.11.2026, SYS-COM-009).

⚠️ **Bilans dotyczy obwodów, nie przekrojów** — przekroje, zabezpieczenia i obciążalność styków z deratingiem przy 50 °C (SYS-ENV-003) w O-030.

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
| PMIC TPS65381A-Q1 (od 1.11.2026) | ACTIVE, IGN wysoki z INH | **STANDBY** — IGN niski (INH niesterowane), wszystkie szyny wyłączone |
| STM32G474, pamięć, AIS2IH, czujniki | zasilane | **bez zasilania** |
| PROFET-y, driver wtrysku, blok CDI | wg stanu silnika | wyłączone |

**Skutek dla nadzoru (O-013):** watchdog jest zasilany zawsze wtedy, gdy zasilany jest procesor — nie istnieje stan „procesor pracuje, nadzór wyłączony” i nie istnieje programowy wyłącznik nadzoru (ECU-SAF-017).

**Skutek dla danych:** uśpione ECU nie ma RAM. Motogodziny, przebieg, zatrzask K4 (O-014) i stan usterek muszą być w pamięci nieulotnej przed zaśnięciem.

### 6.1 Bilans uśpienia ECU

Punkt odniesienia: **zaciski akumulatora, 12,0 V, +25 °C** (ECU-PWR-001). Dla elementów jeszcze niewybranych wartość jest **przydziałem**, który staje się kryterium doboru.

| Element zasilany z akumulatora w uśpieniu | µA maks. | Źródło |
|---|---|---|
| TJA1043, Sleep, pin BAT | 30 | karta (18 typ.) |
| Pin WAKE, prąd wejściowy | 10 | karta |
| PMIC TPS65381A-Q1, STANDBY (od 1.11.2026) | 75 | karta R1.5, maks. przy TJ < 85 °C (typowej karta nie podaje) |
| Zabezpieczenie przed odwrotną polaryzacją — dioda Schottky'ego | 0 | konstrukcja (rozdz. 4.4) |
| TVS na wejściu, upływ przy 12 V | ≤ 5 | przydział |
| 3× PROFET, wyłączone | ≤ 3 | przydział |
| Dzielnik pomiaru akumulatora, podciągnięcia kill switcha i czujników | 0 | **reguła: zasilane wyłącznie z szyn wyłączanych** |
| Przełącznik zasilania HMI, domyślnie załączony (od 3.11.2026) | ≤ 5 | przydział |
| **Razem** | **≤ 133** | wobec limitu 150 µA (zapas 17 µA; przed PMIC: ≤ 63) |

Do potwierdzenia pomiarem T-PWR-001 na prototypie.

### 6.2 Reguły schematu dla TJA1043 (ECU i HMI)

Z karty TJA1043 (rys. 9) i noty AH1014 (rys. 30, rozdz. 6.3–6.4), sprawdzone na schematach graficznych 18.10.2026:

| Pin / obwód | Reguła |
|---|---|
| BAT | Za diodą zabezpieczającą; **ok. 1 kΩ szeregowo + ok. 10 nF** przy pinie |
| INH → wejście IGN PMIC (od 1.11.2026) | Przez rezystor szeregowy **≥ 10 kΩ** (zalecenie karty PMIC; spełnia też obciążenie INH ≥ 10 kΩ wg AH1014). IGN: próg 2–3 V, wewnętrzne ściąganie, odporność −7…40 V, upływ ≤ 50 µA, filtr 7,5–22 ms. **Bit podtrzymania IGN_PWRL nieużywany** — opadnięcie INH wyłącza PMIC |
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
2. **Watchdog PMIC TPS65381A-Q1** (od 1.11.2026, zastępuje TPS3430-Q1) — własny zegar, okienkowy albo pytanie–odpowiedź. Złe sekwencje opuszczają **ENDRV**: bramka AND zapłonu i PROFET rozrusznika zablokowane **sprzętowo, bez udziału procesora**; ósme złe zdarzenie resetuje procesor. Konfiguracja sekwencji tak, by ENDRV opadało w **≤ 100 ms** od zawieszenia — tyle co dotychczasowe okno.
3. **Stan bezpieczny przy resecie** — sam reset nie wystarczy, jeśli wyjścia zostaną w przypadkowym stanie. Przy resecie i podczas startu wszystkie wyjścia mocy muszą być domyślnie wyłączone, inaczej reset przy pracującym silniku mógłby wyzwolić tyrystor w przypadkowej chwili albo (B/C) zostawić wtryskiwacz otwarty. W AC-CDI zawieszone wyjście daje najwyżej jedną iskrę (ECU-IGN-005).

**Stan bezpieczny per wyjście (O-017, 1.11.2026).** Zasada: **zanik zasilania = stan niski = wyłączone.** Każda linia sterująca wyjściem ma rezystor ściągający, więc brak zasilania komparatora, PMIC albo procesora daje ten sam skutek co świadome wyłączenie. **Od 1.11.2026 ENDRV z PMIC jest trzecim wejściem bramki AND i blokadą PROFET rozrusznika.**

| Wyjście | Stan bezpieczny | Wymuszenie sprzętowe | Uśpienie / brak zasilania logiki | Reset procesora przy pracującym silniku | Wymaganie |
|---|---|---|---|---|---|
| **Wyzwalanie tyrystora** (zapłon) | brak iskry | bramka AND: impuls z HRTIM × zezwolenie z **komparatora** × **ENDRV (PMIC)**, rezystory ściągające na obu wejściach; sprzężenie pojemnościowe (najwyżej 1 iskra); rezystor bramka–katoda | brak impulsu. Kondensator naładowany kopnięciem rozładowuje się do ≤ 60 V w ≤ 5 s | wyjście HRTIM niesterowane (rezystor ściągający na wejściu impulsu) → brak impulsów → silnik gaśnie; przy resecie z watchdoga dodatkowo ENDRV niski — blokada niezależna od procesora; ponowne uruchomienie w ruchu po starcie procesora | ECU-IGN-005, -026, ECU-SAF-001, -007, -016 |
| **Zwarcie uzwojenia wzbudzającego** (ścieżka 1 kill switcha) | zwarte w STOP | klucz sterowany **progiem tranzystorowym** (nie komparatorem — 1.11.2026) | **rozwarte** — ścieżka wymaga zasilania. Zanik zasilania pokrywa ścieżka 2 (bramka AND) | próg zasilany dalej — działa według kill switcha | ECU-SAF-001, -021 |
| **Rozrusznik** | wyłączony | PROFET: procesor × komparator × ENDRV; klucz masy: **przycisk START × próg tranzystorowy** (1.11.2026); oba z rezystorami ściągającymi | wyłączony | wyłączony | ECU-SAF-007, -019, -022 |
| **Wentylator** | wyłączony | rezystor ściągający na wejściu PROFET | wyłączony | wyłączony; silnik gaśnie, więc nie ma źródła ciepła. Strategie programowe — stałe załączenie przy usterce czujnika (DTC-SEN-01), obciążenie przy przepięciu (ECU-PWR-009) — działają tylko przy sprawnym firmware | ECU-SAF-007 |
| **Światła** | wyłączone | rezystor ściągający | wyłączone | **wyłączone** — ryzyko zaakceptowane (`otwarte.md` rozdz. 9, decyzja Pawła 1.11.2026) | ECU-SAF-007 |
| **Aux ×2** | wyłączone | rezystor ściągający | wyłączone | wyłączone | ECU-SAF-007 |
| **Zasilanie czujników VSOUT1** (PMIC) | wyłączone | domyślnie wyłączone (bit VSOUT1_EN) | wyłączone | bez zmian; kondycjoner wału i komparator są na VDD5 i od niego nie zależą | ECU-PWR-010 |
| Pompa paliwa **[B/C]** | wyłączona | rezystor ściągający; wejście PROFET × **ENDRV** (1.11.2026) | wyłączona | wyłączona | ECU-SAF-007, ECU-INJ-006 |
| Wtryskiwacze **[B/C]** | zamknięte | **EN TLE9104: komparator × ENDRV; RESN: próg tranzystorowy** (1.11.2026); rezystory ściągające | wyłączone | wyłączone | ECU-SAF-016 |

**Scenariusze negatywne bramki AND:**

| Zdarzenie | Skutek | Zabezpieczenie |
|---|---|---|
| Kill switch zwolniony (STOP → RUN) w chwili, gdy wyjście HRTIM jest w stanie wysokim | Bramka AND przepuszcza zbocze → **jedna iskra w przypadkowym kącie** | Firmware trzyma wyjście HRTIM w stanie niskim przez cały czas STOP i zezwala na zapłon dopiero po synchronizacji (spec. FW B.2.3). Impuls bramki trwa mikrosekundy, więc poza błędem firmware okno nie występuje |
| Wejście impulsu bramki AND pływa podczas resetu procesora | Zakłócenia mogłyby dać zbocza przy zezwoleniu w RUN | Rezystor ściągający na wejściu impulsu; dodatkowo przy resecie z watchdoga ENDRV blokuje bramkę |
| Bramka AND traci zasilanie | Wyjście niskie → brak impulsu | Bezpieczne z natury |
| Komparator albo próg tranzystorowy zawieszony w stanie RUN | Połowa blokad nieaktywna | Drugi układ progowy nadal odcina zapłon i rozrusznik (1.11.2026); test przy każdym STOP wykrywa usterkę (ECU-SAF-021, DTC-SAF-06) |

⚠️ **Watchdog nie jest ochroną toru zapłonu (O-012).** Przy oknie 100 ms i 10 000 obr/min to 16,7 obrotu wału. Dla błędu kąta pojedynczego impulsu dopuszczalny czas reakcji wynosi zero — chroni wyłącznie zapobieganie i ograniczenie tego, co stopień wyjściowy jest w stanie zrobić.

**Wiązka kill switcha — wymóg szczególny:** przycisk podłączony wiązką **dwuprzewodową z masą prowadzoną z ECU** (przycisk odizolowany od ramy — 1.11.2026), z **dwoma rezystorami zalanymi w module przycisku**, o niskiej rezystancji (setki Ω) — szeregowym i równoległym do styku. Dają trzy rozróżnialne poziomy napięcia, dzięki czemu ECU odróżnia naciśnięcie od przerwania przewodu i potrafi to wskazać kierowcy. Podłączenie zwykłego przycisku bez rezystorów **nie jest niebezpieczne**, ale dla przycisku normalnie otwartego (typowy fabryczny) silnik nie będzie pracował bez wciśniętego przycisku (`firmware.md` B.2.5.1). Wiązka z rezystorami wchodzi w zakres dostawy.

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
| H.8 | Złącze główne | Deutsch DTM04-4P: CAN H, CAN L, +12 V **z ECU** (przełącznik domyślnie załączony — 3.11.2026, ECU-PWR-011), GND **do osobnego pinu masy HMI w ECU** | DTM to miniaturowa wersja DT, 13 A/pin |
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

### 9.2 Straty cieplne w obudowie ECU (przebudowa 25.10.2026, MVP-A)

| Źródło | Straty |
|---|---|
| **Blok AC-CDI** (prostownik, tyrystor, rezystor rozładowujący) | **≤ 1,5 W — szacunek**, do potwierdzenia pomiarem uzwojenia wzbudzającego |
| PROFET ×3 | 0,27 W |
| PMIC TPS65381A-Q1 (przetwornica 6 V + regulatory liniowe, od 1.11.2026) | **~0,5 W — szacunek** z obciążeń wg Z18 |
| Logika (MCU, czujniki, CAN) | w PMIC |
| *Drivery wtryskiwaczy* | *0 W w MVP-A (B/C: ~0,16 W)* |
| **Razem MVP-A** | **~2,3 W** |

Dawna pozycja 4,8 W (driver cewki indukcyjnej VBG08H-E) wypadła razem z zapłonem indukcyjnym.

| Wykonanie obudowy | Przyrost temp. | Wewnątrz przy 50 °C otoczenia (SYS-ENV-003, od 1.11.2026) |
|---|---|---|
| Aluminium + dobry kontakt termiczny (Rth ≈ 3 K/W) | ~7 °C | **~57 °C** ✅ |
| Aluminium bez padów (Rth ≈ 8 K/W) | ~18 °C | **~68 °C** ✅ |
| Tworzywo (Rth ≈ 20 K/W) | ~46 °C | **~96 °C** ⚠️ w granicach Grade 1 z marginesem, ale blisko limitu akcelerometru (Z17: 100 °C) |

**Wniosek po zmianie SYS-ENV-003 na +50 °C (1.11.2026):** aluminium z kontaktem termicznym daje duży zapas; tworzywo przestaje być wykluczone, ale jest graniczne wobec akcelerometru. Wybór obudowy — Paweł. Wcześniejszy wniosek „aluminium wymagane” wynikał z +85 °C, czyli klasy automotive zamiast temperatury miejsca montażu.

⚠️ **Ograniczenia bilansu:** uproszczona rezystancja cieplna obudowy (wymagany pełny łańcuch złącze→pad→interfejs→obudowa→otoczenie); straty bloku CDI to szacunek do pomiaru.


---

## 10. Obudowy

**Decyzja Pawła 1.11.2026: jedna PCB dla wariantów A, B i C; osobna obudowa dla wariantu A i osobna dla B/C.** Ten rozdział opisuje obudowę wariantu A. Obudowa i termika B/C — przy etapie B/C (O-065). Na wspólnej PCB zostaje miejsce pod kontakt termiczny drivera zapłonu TCI z przyszłą obudową B/C.

### ECU — obudowa wariantu A

| Parametr | Wymaganie |
|---|---|
| Szczelność | IP67 minimum — zanurzenie, przeprawy wodne, mycie ciśnieniowe |
| Wyrównanie ciśnienia | **Membrana odpowietrzająca obowiązkowa** — czujnik ciśnienia atmosferycznego (KP464) w hermetycznej obudowie byłby bezużyteczny. Zapobiega też kondensacji przy zmianach temperatury. **Membrana i obudowa nieprzepuszczające światła** — KP464 jest czuły na światło powyżej 1 lx |
| Odprowadzanie ciepła | Aluminium z kontaktem termicznym (pady lub pasta) z blokiem AC-CDI, PROFET-ami i PMIC — duży zapas. Tworzywo graniczne (~96 °C wewnątrz, Z17) — rozdz. 9.2. Wybór obudowy — Paweł |
| Przepusty | Złącze główne (≥ 29–30 obwodów + zapas, typ do wyboru) i złącze zapłonu 3–4-pinowe (od 3.11.2026), header wlutowany + USB-C uszczelnione lub z zaślepką, IP67 |
| Wibracje | Mocowanie PCB w kilku punktach, nie tylko na złączu; silikonowe tuleje w punktach montażu do ramy |
| Temperatura | **−40…+50 °C otoczenia w miejscu montażu** (SYS-ENV-003, zmiana 1.11.2026 — decyzja Pawła; Z20), przechowywanie −40…+105 °C (SYS-ENV-004). Wnętrze ~57 °C (aluminium, dobry kontakt), ~68 °C (aluminium bez padów), ~96 °C (tworzywo) — rozdz. 9.2. Ochrona termiczna: ECU-SAF-020 |
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
- **Wszystko na wejściu, przed TVS i za nim, ≥ 40 V**: PMIC (VBATP maks. bezwzględne 40 V, IGN −7…40 V), dioda, kondensatory wejściowe. TJA1043 ma 58 V
- Odrzucony duży kondensator podtrzymujący na zapad 4,5 V: 7–23 mF, upływ elektrolitu do ~1 mA przy limicie uśpienia 150 µA, prąd udarowy, starzenie w +85 °C — przy zysku jednego naciśnięcia przycisku

**Do sesji pomiarowej** (`measurements/pomiar-wzbudzajacego.md`): napięcie i tętnienia na akumulatorze przy kilku obrotach; napięcie przemienne jałowe uzwojenia ładującego z odpiętym regulatorem — najgorszy przypadek awarii regulatora i podstawa korekty 35 V.
