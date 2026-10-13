# Dossier audytowe — ECU „Dust ONE"

## 0. Metryka dokumentu

| | |
|---|---|
| **Identyfikator** | DOC-010 |
| **Wersja** | 1.1 |
| **Status** | wydany do audytu zewnętrznego |
| **Właściciel** | Paweł |
| **Opracowanie** | Claude |
| **Data wydania** | 2026-10-11 |
| **Stan projektu opisany w dokumencie** | DOC-001 v3.9, DOC-002 v1.5, DOC-004 v1.7 |

### 0.1 Historia zmian

| Wersja | Data | Zmiana | Powód |
|---|---|---|---|
| 1.0 | 2026-10-11 | Pierwsze wydanie pakietu do drugiego audytu. Przegląd całości projektu wykonany przy jego przygotowaniu ujawnił **siedem braków procesowych** (luki L34–L40), opisanych w rozdz. 9.1 jako otwarte | Zlecenie Pawła: sprawdzić zgodność z procesem przed audytem |
| **1.1** | **2026-10-11** | **Wydanie po uzupełnieniu braków.** Cztery luki zamknięte przed audytem (repozytorium i kontrola wersji, rejestr założeń, standard kodowania, kryteria akceptacji wyrobu), trzy przeklasyfikowane na pracę zaplanowaną z przypisaniem do konkretnych faz. Utworzony rejestr założeń **obalił pierwszą wpisaną pozycję — motocykl MVP-A nie ma czujnika położenia przepustnicy**; wynikająca z tego korekta siedmiu zapisów opisana w rozdz. 9.0 | Decyzja Pawła: nie oddawać do audytu dokumentacji z brakami, o których już wiemy |

---

## 1. Czego oczekujemy od audytora

Ten dokument jest **pakietem wejściowym do drugiego audytu zewnętrznego**. Pierwszy audyt (12.09.2026) zakończył się werdyktem **NO-GO** i 36 pozycjami; jego realizacja opisana jest w rozdz. 7.

**O co prosimy konkretnie:**

1. **Czego nie zauważyliśmy** — braki strukturalne, nie literówki. Rozdz. 9 zawiera naszą własną samoocenę; interesuje nas przede wszystkim to, czego w niej **nie ma**.
2. **Czy decyzje techniczne z rozdz. 6 bronią się** — szczególnie te, które odbiegają od praktyki motoryzacyjnej, oraz te oparte na pojedynczym pomiarze lub rozumowaniu zamiast na danych.
3. **Czy proces jest adekwatny do ryzyka** — produkt steruje zapłonem silnika spalinowego, a zespół to jedna osoba wspierana przez model językowy.
4. **Czy kolejność prac jest poprawna** — rozdz. 10 opisuje planowane następne kroki i ich uzasadnienie.
5. **Czy korekta po obaleniu założenia o TPS jest kompletna** — rozdz. 9.0. Twierdzenie, że motocykl MVP-A ma czujnik położenia przepustnicy, przetrwało w dokumentacji od Fazy 0 i zdążyło zrodzić kilka zapisów pochodnych. Usunęliśmy te, które znaleźliśmy. **Prosimy o sprawdzenie, czy nie zostało więcej.**

**Czego nie prosimy:** oceny komercyjnej, oceny rynkowej, oceny stylu dokumentów.

**Prosimy o szczerość kosztem uprzejmości.** Pierwszy audyt był ostry i to właśnie on popchnął projekt do przodu.

---

## 2. Produkt

### 2.1 Czym jest

Programowalne ECU do motocykli enduro i adventure, **wyłącznie do zastosowań motorsportowych i dla entuzjastów offroad**. Bez homologacji drogowej, bez zamiaru jej uzyskania.

Trzy wyroby składowe:

| Wyrób | Rola |
|---|---|
| **ECU** | Jednostka sterująca — zapłon, wtrysk, wyjścia mocy, diagnostyka |
| **HMI** | Wyświetlacz na kierownicę, 3,5", komunikacja po CAN |
| **Aplikacja desktop** | Windows; strojenie map, diagnostyka, aktualizacja firmware |

### 2.2 Warianty

| Wariant | Motocykl odniesienia | Zakres sterowania |
|---|---|---|
| **MVP-A** — gaźnik | **Beta 300 RR 2015** (posiadany, dostępny fizycznie). **Bez czujnika położenia przepustnicy** — stwierdzone 11.10.2026, nie będzie dokładany | Zapłon (**mapa jednowymiarowa**, kąt wyłącznie w funkcji obrotów), ogranicznik obrotów, wskaźnik biegu, prędkość i przebieg, motogodziny, wyjścia mocy, diagnostyka |
| B — TPI | KTM EXC TPI | Dodatkowo wtrysk paliwa |
| C — TBI | KTM 890 Adventure | Dodatkowo przepustnica sterowana elektronicznie |

**Projektowany jest wyłącznie MVP-A.** Warianty B i C mają zarezerwowane zdolności sprzętowe (wymagania oznaczone `[HW]` i `[B/C]`), ale nie mają własnych specyfikacji.

### 2.3 Czego produkt świadomie nie robi

| Funkcja | Powód rezygnacji |
|---|---|
| **Quickshifter** | **Usunięty 29.09.2026.** Najgorszy stosunek złożoności do wartości w projekcie; jedyna funkcja wymagająca wnioskowania o intencji kierowcy, przez co wyprodukowała trzy kolejne błędy specyfikacji; niska realna wartość w technicznym terenie, gdzie sprzęgło jest w ciągłym użyciu |
| Czujnik sprzęgła | Usunięty razem z quickshifterem — tracił uzasadnienie |
| Pełne logowanie sesji jazdy | Zawężone do czarnej skrzynki; 8 MB daje ~17 minut zapisu ciągłego |
| Blokada rozrusznika na biegu | Świadomie, odpowiedzialność po stronie kierowcy (jak w części motocykli sportowych) |
| Blipper (redukcja bez sprzęgła) | Wymaga przepustnicy elektronicznej — tylko wariant C |
| Regulacja napięcia szyn przez MCU | Odrzucona — błąd firmware mógłby zniszczyć czujniki i sam MCU |

---

## 3. Zespół i sposób pracy — istotne dla oceny ryzyka

| Rola | Kto |
|---|---|
| Inżynier-pomysłodawca, decydent, wykonawca sprzętu i testów | **Paweł** (inżynier elektronik) |
| Inżynier produktu, architekt, dokumentacja | **Claude** (model językowy, w rozmowie) |
| Implementacja firmware i aplikacji | **Claude Code** (planowana, jeszcze nierozpoczęta) |

**Konsekwencje, o których audytor powinien wiedzieć:**

- **Nie ma drugiego inżyniera.** Żaden projekt ani decyzja nie przechodzi przez niezależny przegląd ludzki. Audyt zewnętrzny jest jedynym takim mechanizmem.
- **Część treści powstaje w modelu językowym**, co udokumentowanie wygenerowało błędy specyficzne dla tego sposobu pracy: twierdzenia o komponentach bez sprawdzenia karty katalogowej (czterokrotnie), kryteria wykrywania usterek nieodporne na realne scenariusze jazdy (trzykrotnie), twierdzenie o samym motocyklu przyjęte za fakt bez oględzin (raz, z siedmioma zapisami pochodnymi). Wszystkie trzy wzorce zostały zapisane w dokumentacji i obłożone zasadami procesu (#14, #15, rejestr założeń w DOC-001 rozdz. 11.2, zapis w DOC-005 rozdz. 5). **Prosimy o ocenę, czy te zasady faktycznie blokują wzorce, czy tylko je opisują** — rozdz. 9.3.
- **Nie ma jeszcze żadnego kodu.** Projekt jest w fazie specyfikacji.

---

## 4. Proces

### 4.1 Struktura fazowa

14 faz, od wymagań do wsparcia posprzedażowego. Faza 2 rozbita na 2-ECU, 2-HMI, **2-FW** (specyfikacja firmware) i 2-Desktop.

**Faza 2-FW została dodana po przeglądzie 31.08.2026**, gdy okazało się, że zasada „nic do implementacji bez zatwierdzonej specyfikacji" nie miała fazy, która tę specyfikację tworzy.

**Faza 3 to wyłącznie płytki ewaluacyjne i sygnały symulowane.** Kontakt z motocyklem dopuszczony dopiero w Fazie 8, na wyprodukowanym PCB.

### 4.2 Bramki jakości G0–G5

Wprowadzone 12.09.2026 **w reakcji na pierwszy audyt**, którego główny zarzut brzmiał: fazy zamykane bez spełnienia własnych kryteriów.

| Bramka | Warunek przejścia |
|---|---|
| G0 | Wymagania mierzalne, bez pozycji nierozstrzygniętych |
| G1 | Architektura, protokoły, interfejsy |
| G2 | Projekt szczegółowy: schemat, macierz pinów i DMA, BOM z pełnymi numerami, analiza najgorszego przypadku, FMEA, wiązka |
| G3 | Firmware zweryfikowany na stanowisku |
| G4 | Integracja na silniku |
| G5 | Walidacja terenowa |

**Reguła nadrzędna: bramka nie przechodzi, jeśli otwarta jest choćby jedna pozycja P0 lub pozycja dotycząca bezpieczeństwa.**

### 4.3 Zasady procesu

17 zasad w DOC-001 rozdz. 2. Istotne dla audytu:

| # | Zasada | Pochodzenie |
|---|---|---|
| 5 | Każdy istotny komponent konsultowany; samodzielnie dobierane tylko elementy bierne | od początku |
| 7 | Wersjonowanie firmware i protokołu `major.minor.patch`, kontrola zgodności ECU↔HMI↔aplikacja | 31.08.2026 |
| 8 | Każde wymaganie ma implementację i test — tabela pokrycia | 31.08.2026 |
| 10 | Dostawcy w kolejności TME → Mouser → Farnell → DigiKey; **pełny numer katalogowy i aktywny status cyklu życia**; NRND dyskwalifikuje | 12.09.2026, po odrzuceniu TLE8104E |
| 11 | Uwagi audytu do faz nierozpoczętych wchodzą jako **kryteria akceptacji tych faz**, nie jako osobna lista naprawcza | 12.09.2026 |
| 13 | Metryka i historia zmian w każdym dokumencie; baseline przy bramce | 20.09.2026, po audycie F-033 |
| **14** | **Każde wymaganie z progiem czasowym lub automatycznym zadziałaniem wymaga przed zapisaniem wypisania scenariuszy rzeczywistej jazdy, w których warunek spełnia się bez usterki. Do tego obowiązkowy test negatywny** | 29.09.2026, po trzech błędach tego typu |
| **15** | **Kryteria automatycznego zadziałania są propozycją do zatwierdzenia, nie ustaleniem** | 29.09.2026, po zapisaniu kryterium bez zgody decydenta |
| **16** | **Repozytorium z historią zmian dla dokumentów i kodu. Baseline przy bramce jest znacznikiem w repozytorium, nie wpisem w tabeli** | 11.10.2026, luka L34 — po utracie części pracy przy awarii środowiska |
| **17** | **Standard kodowania, analiza statyczna przy każdej zmianie, minimalne pokrycie testami jednostkowymi warstwy zapłonu i bezpieczeństwa, wersjonowanie narzędzi budowania — ustalane przed pierwszą linią firmware** | 11.10.2026, luka L36 |

---

## 5. Stan na 11.10.2026

### 5.1 Fazy

| Faza | Status | Co otwarte |
|---|---|---|
| 0 — Wymagania | ⬜ otwarta | **17 wymagań z wartością nierozstrzygniętą** (siedemnaste doszło 11.10.2026 — sposób blokady live tuningu bez TPS, rozdz. 9.0.1); brak wymagań bootloadera. Bramka G0 zablokowana |
| 1 — Architektura | ⚠️ warunkowo | Brak diagramu elektrycznego; diagram funkcjonalny do przeglądu wobec kryteriów audytu |
| 2-ECU — HW | ⚠️ warunkowo | Dobór przetwornic, komparatora kill switcha; potwierdzenie dostępności całego BOM |
| 2-HMI — HW | ⚠️ warunkowo | Drzewo zasilania, analiza najgorszego przypadku drabinki przycisków, pełny numer pamięci flash |
| **2-FW** | 🔶 **w toku** | **A zamknięty, B zamknięty, C.1 zamknięty.** Otwarte: reszta C, D–J |
| 2-Desktop | ⬜ | Całość. Zawiera pozycję audytu P0 (protokoły) |
| 3–13 | ⬜ | — |

### 5.2 Liczby

| Pozycja | Stan |
|---|---|
| Wymagania z identyfikatorem | **105** |
| Pokrycie w tabeli traceability | **105 / 105 (100%)** |
| Identyfikatory testów | **107** |
| Wymagania zamknięte dowodem | **0** — żaden test nie został wykonany |
| Kody usterek w macierzy | **51** |
| Luki w rejestrze | **40** — 4 zamknięte 11.10.2026, 3 przeklasyfikowane na pracę zaplanowaną |
| Ryzyka w rejestrze | 18 |
| **Założenia w rejestrze** | **10** — 1 potwierdzone rozumowaniem, **1 obalone**, 8 niepotwierdzonych |
| Zasady procesu | **17** |
| Kryteria akceptacji wyrobu MVP-A | **12 (A1–A12)** — propozycja, niezatwierdzona |
| Dokumenty projektu | 10, każdy z metryką i historią zmian |

**Zero zamkniętych dowodem** jest stanem oczekiwanym — nie zbudowano jeszcze żadnego sprzętu. Identyfikatory testów są miejscami na dowód, nie wykonanymi testami.

---

## 6. Kluczowe decyzje techniczne

Pełne uzasadnienia w dokumentach źródłowych; tu wyciąg z odwołaniami.

### 6.1 Sprzęt

| Funkcja | Wybór | Uwaga dla audytora |
|---|---|---|
| MCU ECU | **STM32G474VET3** (LQFP100, −40…+125 °C) | Wybrany za HRTIM. Obudowa zmieniona z LQFP64 po bilansie pinów — 55 sygnałów wobec ~50 dostępnych |
| MCU HMI | STM32G0B1 | |
| Driver zapłonu | **VBG08H-E** | Ograniczanie prądu 8,5–10,5 A, wyjście diagnostyczne o progu 6,5 A |
| Driver wtrysku | **TLE9104SHXUMA1** | 4 kanały low-side, tryb nasycony. Historia doboru w rozdz. 7.2 |
| Kondycjoner VR | **MAX9926UAEE/V+** | Adaptacyjny próg, detekcja względem przejścia przez zero. **Jedyne źródło spoza UE** — ryzyko R17 |
| IMU | **BMI090L** | Zmieniony z BMI088 po stwierdzeniu braku kwalifikacji AEC-Q100 |
| Transceiver CAN ×2 | TJA1043 | VCC zasilane na stałe — przy jego zaniku układ samoczynnie przechodzi w Sleep |
| Watchdog | TPS3430-Q1 | Okienkowy, okno ~100 ms |
| Czujnik biegu | MLX90316 na bębnie zmiany biegów | Rozwiązanie odwzorowane z KTM |
| Wyjścia mocy | BTS7008-2EPA ×3 (6 kanałów) | Pompa, wentylator, światła, rozrusznik, rezerwa |
| Zasilanie | **Dwie niezależne przetwornice 5,0 V i 3,3 V o stałych nastawach + przełącznik obciążenia** | Przeprojektowane po audycie |
| Komparator kill switcha | do doboru | **Nowy 22.09.2026** — bramkuje wejścia EN driverów niezależnie od firmware |
| Złącze ECU | Molex CMC 28-obwodowe | Wymiary niepotwierdzone kartą katalogową — ryzyko R3 |
| Wyświetlacz | Riverdi RVT35HHBFWN00, koprocesor EVE4 BT817Q, 1000 cd/m² | |

### 6.2 Architektura bezpieczeństwa

**Zasada: ścieżki sprzętowe działają przy zawieszonym firmware.** Diagram DOC-008.

| Mechanizm | Realizacja | Niezależny od firmware |
|---|---|---|
| Kill switch | Układ trzypoziomowy + komparator bramkujący wejścia EN driverów | **tak** |
| Rozróżnienie naciśnięcia od przerwania przewodu | Rezystory w wiązce przy przycisku, trzy poziomy napięcia, odczyt ADC | diagnostyka — nie |
| Watchdog i brown-out | Reset MCU + rezystory ściągające na wyjściach mocy i na linii bramkującej EN | **tak** |
| Sufit czasu ładowania cewki | **Rejestr okresu HRTIM** — wyjście kasowane zdarzeniem porównania *oraz* końcem okresu | **tak** |
| Wywrotka, utrata sygnału obrotów, zwarty wtryskiwacz | Zadanie klasy K4 | nie — nadzorowane watchdogiem |

**Klasyfikacja usterek K0–K4** z regułą rozdzielającą: K0–K3 ustępują samoczynnie z histerezą, **K4 nie ustępuje nigdy** i wymaga zatrzymania wału oraz świadomego odblokowania.

**Zamknięta lista zdarzeń odcinających silnik** (7 pozycji). Dopisanie kolejnej wymaga osobnej decyzji z uzasadnieniem. Jedna pozycja została **wycofana tego samego dnia**, gdy okazało się, że firmware nie ma czym jej wykryć.

**Uprawnienie ECU do zatrzymania silnika jest celowo wąskie.** Uzasadnienie: w enduro silnik pełni funkcję hamulca silnikowego i stabilizacji; zgaszenie go w brodzie lub na stromym podjeździe kończy się przewróceniem. ECU gaszące „na wszelki wypadek" jest groźniejsze od ECU, które ogranicza moc i wyraźnie ostrzega.

### 6.3 Trigger i synchronizacja — oparte na pomiarze

**Zmierzone na Becie 300 RR 2015 (11.10.2026):**

| Parametr | Wartość |
|---|---|
| Wypustów na kole magnesowym | **1** |
| Długość kątowa wypustu | **30° wału** |
| Krawędź natarcia | **30° przed GMP** |
| Krawędź spływu | **dokładnie w GMP** |
| Rezystancja pick-upu | **95,7 Ω** (specyfikacja fabryczna 100 Ω ±20%) |
| Szczelina czujnik–wypust | **0,18 mm** |

**Wniosek konstrukcyjny:** punkt zapłonu leży wewnątrz wypustu, więc krawędź natarcia jest punktem odniesienia tuż przed iskrą. Prognoza obejmuje 10–20°, nie pełny obrót.

| Obroty | Błąd prognozy od krawędzi natarcia | Od poprzedniego GMP (dla porównania) |
|---|---|---|
| 3000 | **0,20°** | 6,80° |
| 6000 | **0,05°** | 1,70° |
| 10 000 | **0,02°** | — |

Budżet z ECU-IGN-002 wynosi 1,0° w 99,9 percentylu.

**Najtrudniejszy jest zakres niskich obrotów**, nie wysokich: przy 1500 obr/min estymata starzeje się o 5,3% w ciągu obrotu (0,80° bez korekty). Dlatego korekta przyspieszenia jest warunkiem spełnienia wymagania, nie ulepszeniem.

**Dwa limity wyprzedzenia, celowo rozdzielone:** geometryczny 28° (stały w firmware, chroni przed błędem mapy) oraz termodynamiczny w mapie (niższy, chroni przed detonacją). Pierwszy nie zastępuje drugiego.

**Bramkowanie kątowe wejścia:** zbocze przychodzące w fazie, w której wypust nie może wystąpić, jest **odrzucane bez wpływu na model kąta i bez utraty iskry**. Trzy warstwy: adaptacyjny próg MAX9926, filtr cyfrowy wejścia w MCU, bramkowanie programowe.

### 6.4 Tryb zastępczy — derating według utraconej informacji

Kryterium nie brzmi „jak poważna jest usterka", tylko **jakiej informacji ECU zostało pozbawione i czy da się ją czymś zastąpić**.

| Grupa | Przykład | Reakcja |
|---|---|---|
| Wartość zastępcza wystarcza | Temperatura powietrza, ciśnienie atmosferyczne | **Bez ograniczeń**, pełny zakres obrotów |
| Ochrona termiczna lub elektryczna | Przegrzanie ECU, drivera, awaria kanału mocy | Limit obrotów, mapy bez zmian |
| Utrata sygnału obciążenia | **W MVP-A wyłącznie szyna 5 V w paśmie granicznym** (motocykl nie ma przepustnicy z czujnikiem); w wariantach B/C dodatkowo przepustnica | **Mapa awaryjna liczona na pełne obciążenie** (bogata) + limit 3500 obr/min |

**Mapa awaryjna bogata, nie oszczędna** — przy utracie sygnału obciążenia utrzymanie dawki z biegu jałowego oznacza skrajnie ubogą mieszankę pod obciążeniem, czyli zatarcie. Kosztem jest kiepska praca na biegu jałowym. **Rozumowanie dotyczy wariantów z wtryskiem**; w MVP-A, gdzie dawkę podaje gaźnik, grupa ta sprowadza się do cofnięcia zapłonu i limitu obrotów.

### 6.5 Zarządzanie zasilaniem

Motocykle enduro nie mają stacyjki — ECU jest stale podłączone do akumulatora.

| Element w uśpieniu | Stan | Pobór |
|---|---|---|
| Przetwornica 3,3 V | włączona (zasila MCU w trybie Stop) | ~10–25 µA |
| Przetwornica 5,0 V | **włączona** — zasila VCC transceivera | ~10–25 µA |
| TJA1043 | Standby, nasłuch magistrali | ~30–50 µA |
| Przełącznik obciążenia 5 V | **wyłączony** — odcina czujniki, MAX9926, MLX90316 | ~1–10 µA |
| **Razem (szacunek)** | | **~70–135 µA** |

Limit z wymagania: 150 µA dla ECU, 250 µA dla zestawu.

**Wybudzanie sygnałem obrotów świadomie odrzucone** — MAX9926 pobiera 4,7 mA i nie ma trybu uśpienia, co potwierdzono kartą katalogową.

---

## 7. Odpowiedź na pierwszy audyt (12.09.2026)

### 7.1 Werdykt i reakcja

Werdykt: **NO-GO do implementacji produkcyjnego firmware i zamrożenia PCB.** 36 pozycji: 10×P0, 21×P1, 5×P2.

**Stanowisko przyjęte:** audyt miał rację co do istoty. Część pozycji dotyczyła jednak faz jeszcze nierozpoczętych, więc wprowadzono **podział na naprawę i pracę procesową** (zasada #11): pozycja opisująca zapis nieprawdziwy lub błędny wybór = naprawa natychmiast; pozycja opisująca brak w fazie, do której nie dotarliśmy = kryterium akceptacji tej fazy.

### 7.2 Błędy własne przyznane i naprawione

| Pozycja | Błąd | Przyczyna |
|---|---|---|
| F-001 | **L9960 opisany jako dwukanałowy driver wtryskiwaczy.** Producent określa go jako mostek H do silników prądu stałego | Ekstrapolacja z kategorii „driver automotive" bez sprawdzenia funkcji w karcie katalogowej |
| F-002 | **Regulator liniowy 5 V zasilany z 5 V z przetwornicy** — wystawiłby ~4,5 V, rujnując dokładność czujników ratiometrycznych | Błąd elementarny, przeoczony mimo kilkukrotnego rysowania drzewa zasilania |
| F-003 | Domeny zasilania TJA1043 opisane nieprawdziwie — karta katalogowa wymusza Sleep przy zaniku VCC lub VIO | Opis z pamięci zamiast z karty |
| F-005 | Automatyczny restart po resecie watchdoga | Dopuszczał samoczynne złapanie silnika z rozpędu |
| F-006 | **Cykliczna logika rozrusznika** — stan przechodził w ROZRUCH „po wykryciu obrotów", a nic tych obrotów nie powodowało | Błąd logiczny w maszynie stanów |
| F-009 | Faza 2-ECU zamknięta bez macierzy pinów | Bilans wykazał niewystarczalność wybranej obudowy MCU |
| F-019 | Klasa temperaturowa MCU zawyżona (T6 = 85 °C opisane jako 125 °C) | Pomylenie temperatury złącza z klasą |

**Powtarzający się wzorzec, zapisany w DOC-005 rozdz. 5:** opisywanie komponentów jako spełniających wymaganie na podstawie producenta lub zastosowania, bez sprawdzenia karty katalogowej. Wzorzec **nawrócił 20.09.2026** przy MAX9926 (propozycja oparta na nieistniejącym wejściu shutdown) i został wtedy obłożony zasadą: żadna propozycja zmiany sprzętowej nie jest przedstawiana przed sprawdzeniem karty katalogowej parametru, na którym się opiera.

### 7.3 Bilans pozycji audytu

| Kategoria | P0 | P1 | P2 | Razem |
|---|---|---|---|---|
| Naprawa — **zamknięte** | 8 | 6 | 1 | **15** |
| Naprawa — otwarte | **0** | 1 | 1 | **2** |
| Proces — kryteria akceptacji faz | 2 | 14 | 3 | **19** |
| **Razem** | **10** | **21** | **5** | **36** |

**Wszystkie pozycje P0 części naprawczej są zamknięte.** Dwie pozostałe P0 (F-008 — specyfikacja firmware B–J, F-010 — protokoły CAN i USB) są w toku jako praca fazowa.

Zamknięte od ostatniego audytu, warte wskazania: **F-023** (macierz usterek, 51 kodów), **F-013** (trigger i synchronizacja), **F-012** (tabela pokrycia przebudowana), **F-029** (ryzyka z właścicielami i dowodami), **F-033** (wersjonowanie dokumentów), **F-031 częściowo** (diagram bezpieczeństwa gotowy).

---

## 8. Rejestry pozycji otwartych

### 8.1 Wymagania bez ustalonej wartości — 16, blokują bramkę G0

| Wymaganie | Czego brakuje | Skąd przyjdzie |
|---|---|---|
| SYS-ENV-006 | Profil odporności na wibracje | Norma lub pomiar |
| ECU-IGN-003 | Zakres korekty czasu ładowania od napięcia | Punkt C, pomiar |
| ECU-IGN-004 | Maksymalne wypełnienie ładowania | Punkt C, pomiar termiczny |
| ECU-IGN-007 | Rozdzielczość zapisu kąta w mapie | **Punkt D** |
| ECU-INJ-003, 004, 006 | Parametry wtrysku | Warianty B/C, pomiar na wtryskiwaczu |
| ECU-SEN-002 | Poziomy logiczne wejścia Halla | Faza 4 |
| ECU-SEN-003 **[HW]** | Błąd pomiaru przepustnicy po kalibracji — **dotyczy wyłącznie wariantów B/C**, w MVP-A sygnału nie ma | Pomiar, warianty B/C |
| ECU-SEN-010 | Błąd pomiaru prędkości koła | Pomiar |
| ECU-SAF-001 | Czas reakcji bramkowania sprzętowego | Faza 4, pomiar |
| **ECU-SAF-011** | **Sposób blokady live tuningu w MVP-A** — warunku obciążenia nie da się ocenić bez TPS | **Decyzja, punkt C** (rozdz. 9.0.1) |
| ECU-LOG-006 | Okno zapisu przed i po wypadku | Punkt F |
| SYS-COM-001a | Akceptowalny czas aktualizacji firmware HMI | Punkt H |
| SYS-COM-004 | Okresy i timeouty ramek | Faza 2-Desktop |
| HMI-UI-004, 005 | Próg temperaturowy jasności, kryterium czytelności | Pomiar, test na słońcu |

### 8.2 Funkcje w zakresie bez wymagania

| Funkcja | Priorytet | Status |
|---|---|---|
| **Bootloader i aktualizacja firmware** | **P0** | **Blokuje G0.** Punkt H specyfikacji firmware |
| Sterowanie wentylatorem | P1 | Punkt B/C |
| Przełączanie map z HMI | P1 | Punkt D/J |
| Licznik przebiegu | P1 | Punkt C |
| Korekta na wysokość n.p.m. | P1 | Punkt C |
| **Aplikacja desktop — cały obszar poza jednym wymaganiem** | P1 | Faza 2-Desktop |
| Sterowanie światłami, zegar RTC, konfigurator wyglądu HMI | P2 | Punkty B, F, J |

### 8.3 Ryzyka o wpływie wysokim — żadne nie jest zamknięte

| # | Ryzyko | Bramka |
|---|---|---|
| R1 | Live tuning na pracującym silniku | G3 |
| R2 | Zakłócenia EMI z instalacji zapłonowej | G4 |
| R9 | Pobór prądu w uśpieniu — ECU stale podłączone do akumulatora | G3 |
| R12 | Kill switch — do potwierdzenia pomiarem przy zawieszonym firmware | G3 |
| R15 | Przegrzanie wyświetlacza na słońcu (76 °C przy obudowie aluminiowej, panel czernieje powyżej ~70 °C) | G5 |
| **R16** | **Brak planu wyposażenia pomiarowego** — 72 z 107 testów przypada na Fazę 6, a część wymaga sprzętu, którego nie ma | **G2** |
| R18 | Zakres funkcji bez wymagań (bootloader) | **G0** |

---

## 9. Samoocena — gdzie sami podejrzewamy słabość

Ta sekcja jest celowo niewygodna. Prosimy o weryfikację i o wskazanie tego, czego tu nie ma.

### 9.0 Co zmieniło się między wersją 1.0 i 1.1 tego dokumentu

Wersja 1.0 wyszła z siedmioma brakami procesowymi opisanymi jako otwarte. **Decyzja: nie oddawać do audytu dokumentacji z brakami, o których już wiemy.** Podział przyjęty świadomie:

| Luka | Co to było | Rozstrzygnięcie |
|---|---|---|
| **L34** | Brak repozytorium i kontroli wersji | **Zamknięte** — zasada procesu #16. Baseline przy bramce jest znacznikiem w repozytorium |
| **L35** | Brak rejestru założeń | **Zamknięte** — DOC-001 rozdz. 11.2, 10 pozycji Z1–Z10 z właścicielem, sposobem potwierdzenia i wskazaniem skutków obalenia |
| **L36** | Brak standardu kodowania i planu analizy statycznej | **Zamknięte co do obowiązku** — zasada #17. Konkretne narzędzia i progi pokrycia: punkt I specyfikacji firmware, przed Fazą 5 |
| **L37** | Brak kryteriów akceptacji wyrobu | **Zamknięte co do treści** — DOC-001 rozdz. 3.0a, 12 kryteriów A1–A12. **Status: propozycja niezatwierdzona** |
| **L38** | Brak oszacowania kosztu BOM | **Przeklasyfikowane na pracę zaplanowaną — Faza 4.** Wymaga BOM z pełnymi numerami katalogowymi, którego jeszcze nie ma |
| **L39** | Brak przypadków użycia i wymagań niefunkcjonalnych aplikacji | **Przeklasyfikowane — Faza 2-Desktop.** Powstają razem z projektem aplikacji |
| **L40** | Brak specyfikacji wariantów B i C jako wyrobów | **Przeklasyfikowane — po zamknięciu MVP-A** |

**Prosimy o ocenę samego podziału.** Trzy ostatnie pozycje zostały uznane za pracę zaplanowaną, nie za przeoczenie. To wygodna dla nas interpretacja i zdajemy sobie z tego sprawę.

#### 9.0.1 Rejestr założeń obalił pierwsze wpisane założenie

Rejestr założeń powstał, bo stwierdziliśmy, że założenia projektu siedzą wyłącznie w prozie i żadne nie jest oznaczone jako wymagające potwierdzenia. **Pierwsza wpisana pozycja okazała się fałszywa w dniu utworzenia rejestru.**

Założenie Z1: *Beta 300 RR 2015 ma czujnik położenia przepustnicy*. Źródło: decyzja z Fazy 0, zapisana jako fakt i nigdy nieweryfikowana. **Motocykl nie ma TPS i nie będzie dokładany** (decyzja właściciela, 11.10.2026).

Skutki — siedem zapisów skorygowanych:

| Zapis | Było | Jest |
|---|---|---|
| Decyzja 2.7 (DOC-001) | „gaźnik **+ TPS**" | „gaźnik, **bez TPS**" |
| **ECU-IGN-008** | Strategia zastępcza przy utracie sygnału przepustnicy w wariancie gaźnikowym | **Usunięte** — nie ma sygnału, który można utracić |
| **ECU-IGN-020** | — | **Nowe:** mapa zapłonu MVP-A jest jednowymiarowa, kąt wyłącznie w funkcji obrotów |
| **DTC-SEN-04** | Usterka przepustnicy, wariant gaźnikowy | **Usunięte** |
| ECU-SEN-003 | Błąd pomiaru TPS, bez oznaczenia wariantu | Przeniesione do **[HW]** — zdolność sprzętowa dla wariantów B/C |
| B.3.1 grupa G3 (DOC-004) | Utrata sygnału obciążenia: przepustnica **lub** szyna 5 V | W MVP-A **wyłącznie** przypadek szyny 5 V |
| SYS-COM-002a | Dane szybkozmienne: obroty, **przepustnica**, prędkość | W MVP-A przepustnica nie jest nadawana |

**Jedna konsekwencja została świadomie pozostawiona otwarta.** Interlock live tuningu (ECU-SAF-011) blokuje zmiany map przy jednoczesnym spełnieniu warunku obrotów **i** otwarcia przepustnicy powyżej 60%. **W MVP-A drugiego warunku nie da się ocenić.** Trzy rozważane drogi: blokada wyłącznie od obrotów (mniej precyzyjna — blokuje też tam, gdzie nic nie grozi), blokada każdej zmiany przy pracującym silniku (najbezpieczniejsza — odbiera funkcję strojenia na żywo), pozostawienie samego limitu szybkości zmiany (ryzyko R1 wraca). **Pozycja do rozstrzygnięcia przed zamknięciem punktu C. Prosimy o rekomendację.**

**Wniosek, o którego ocenę prosimy:** założenie przetrwało w dokumentacji od Fazy 0 do pierwszego audytu wewnętrznego i zdążyło zrodzić zapisy pochodne, bo nie wyglądało na pozycję otwartą — wyglądało na fakt. Rejestr wyłapał je w pierwszej godzinie istnienia. Czy są w dokumentacji inne twierdzenia tej samej natury, których nie rozpoznaliśmy jako założenia?

### 9.1 Braki procesowe wykryte przy przygotowaniu wersji 1.0 — stan po uzupełnieniu

Rozstrzygnięcie każdej pozycji opisane jest w rozdz. 9.0. Tu zostaje to, co **nadal jest otwarte**, razem z tym, co pozycja zamknięta zostawiła po sobie:

| Pozycja | Co zostało otwarte po uzupełnieniu |
|---|---|
| Repozytorium i kontrola wersji (L34) | Zasada istnieje, **mechanizm jeszcze nie** — repozytorium nie zostało założone, dokumenty nadal są plikami nadpisywanymi w miejscu. Zasada #16 bez wdrożenia jest w tej samej sytuacji, w jakiej była zasada #13 przed nią. **Termin: przed bramką G0** |
| Standard kodowania i analiza statyczna (L36) | Ustalony jest **obowiązek**, nie treść: nie wybrano standardu, narzędzia, progów pokrycia testami ani sposobu walidacji narzędzi budowania |
| Kryteria akceptacji wyrobu (L37) | 12 kryteriów A1–A12 jest **propozycją niezatwierdzoną**. Do czasu zatwierdzenia projekt formalnie nadal nie ma definicji gotowości |
| Koszt BOM (L38) | Nieoszacowany. Przypisane do Fazy 4 — **w konsekwencji wymaganie Fazy 0 o rozsądku budżetowym przechodzi przez bramkę G0 niezweryfikowane** |
| Przypadki użycia i wymagania niefunkcjonalne aplikacji (L39) | Nieopisane. Przypisane do Fazy 2-Desktop |
| Warianty B i C jako wyroby (L40) | Bez zakresu i odbiorcy. Przypisane do okresu po zamknięciu MVP-A |

**Dwie pozycje z tej listy prosimy obejrzeć szczególnie uważnie:** brak wdrożonego repozytorium (zasada bez mechanizmu — ten sam wzorzec, który raz już kosztował utratę pracy) oraz przejście bramki G0 bez weryfikacji wymagania budżetowego.

### 9.2 Decyzje, co do których mamy wątpliwości

| Decyzja | Wątpliwość |
|---|---|
| **Usunięcie quickshiftera** | Decyzja zapadła po trzech błędach specyfikacji tej funkcji. Czy powodem była realna złożoność, czy zmęczenie tematem? |
| **Mapa awaryjna „na bogato" przy utracie sygnału obciążenia** | Rozumowanie wydaje się poprawne, ale nie zostało zweryfikowane pomiarem ani z nikim skonsultowane. **Dotyczy wariantów B/C** — w MVP-A dawkę podaje gaźnik |
| **Jednowymiarowa mapa zapłonu w MVP-A** | Wymuszona brakiem TPS, nie wybrana. Fabryczne CDI pracuje tak samo, więc rozwiązanie jest co najmniej nie gorsze od oryginału — ale **kąt wyprzedzenia zależy od obciążenia, nie tylko od obrotów**, i przy strojeniu pod moc ta zależność gdzieś musi się ujawnić. Nie wiemy, czy skończy się to kompromisem w mapie, czy realnym ograniczeniem produktu. **Pytanie do audytora: czy w silniku 2T tej klasy sterowanie zapłonem wyłącznie od obrotów jest wystarczające, czy to ściana, w którą wejdziemy w Fazie 8?** |
| **Decyzja o niedokładaniu TPS** | Dołożenie czujnika do gaźnika jest wykonalne mechanicznie i dałoby mapę dwuwymiarową. Zrezygnowano, żeby nie ingerować w motocykl. **Czy ta oszczędność nie zostanie zapłacona w strojeniu?** |
| **Limit wyprzedzenia 28°** | Oparty na założeniu, że fabryczne CDI też mieści się w tej geometrii. To wniosek pośredni, nie dowód |
| **Brak blokady rozrusznika na biegu** | Świadoma rezygnacja z ochrony, którą mają motocykle fabryczne |
| **Okno bramkowania ±10°/±20°** | Wartości przyjęte bez danych o rzeczywistych zakłóceniach |
| **Szczelina 0,18 mm** | Nietypowo mała. Nie wiemy, czy to specyfikacja fabryczna, czy stan konkretnego egzemplarza. Amplituda sygnału przy 10 000 obr/min może przekroczyć przyjęty zakres wejścia |

### 9.3 Wzorce błędów udokumentowane w projekcie

Oba wystąpiły wielokrotnie i oba zostały obłożone zasadami procesu. **Prosimy o sprawdzenie, czy zasady faktycznie je blokują, czy tylko opisują.**

| Wzorzec | Wystąpienia | Reakcja |
|---|---|---|
| Twierdzenie o komponencie bez sprawdzenia karty katalogowej | L9960, BMI088, TJA1043, MAX9926 | Zasada #10, zapis w DOC-005 rozdz. 5 |
| Kryterium wykrywania usterki nieodporne na realne scenariusze jazdy | quickshifter przy użyciu sprzęgła, wskazanie biegu bez warunku sprzęgła, dwa kolejne kryteria wykrycia zwartego czujnika sprzęgła | **Zasady #14 i #15** |
| **Twierdzenie o motocyklu przyjęte za fakt bez oględzin** | **obecność TPS w MVP-A** — zapisane w Fazie 0, wykryte 11.10.2026, zdążyło zrodzić 7 zapisów pochodnych | **Rejestr założeń, DOC-001 rozdz. 11.2** |

Wspólny mianownik drugiego wzorca: sprawdzano, czy mechanizm działa, a nie czy **nie działa wtedy, kiedy nie powinien**. Wszystkie cztery błędy przeszłyby każdy test pozytywny.

---

## 10. Planowana kolejność dalszych prac

| Krok | Zakres | Uzasadnienie kolejności |
|---|---|---|
| 1 | Reszta punktu C w zakresie MVP-A: strategia zapłonu przy rozruchu, metoda odcięcia w ograniczniku, korekta ładowania od napięcia. **Wraz z rozstrzygnięciem interlocku live tuningu bez TPS** (rozdz. 9.0.1) | Określa, czego mapa musi dostarczać. Interlock jest otwartą pozycją bezpieczeństwa, więc nie może przejść do punktu D |
| 2 | **Punkt D — struktura danych i map** (osie, rozdzielczość, interpolacja, zakresy, walidacja, podział pamięci) | Aplikacja desktop nie może powstać wcześniej, bo nie wiedziałaby, co edytuje. Zamyka F-020 |
| 3 | **Punkt H — bootloader** | **Ostatnia pozycja P0 blokująca G0.** Wymaga D ze względu na podział pamięci |
| 4 | Faza 2-Desktop — protokoły CAN i USB | Pozycja P0 (F-010). Wymaga D |
| 5 | Reszta punktu C — strategie wtrysku | Dotyczy wariantów B/C, nieprojektowanych |

**Wartości map nie powstają na żadnym z tych kroków** — pochodzą ze strojenia na silniku w Fazie 8.

---

## 11. Dokumenty źródłowe

| ID | Dokument | Wersja | Zawartość |
|---|---|---|---|
| DOC-001 | `proces-rozwoju-ecu.md` | **3.9** | **Dokument główny.** Proces, fazy, bramki, zasady, decyzje sprzętowe, budżety, rejestry luk i ryzyk, tabela pokrycia wymagań |
| DOC-002 | `wymagania.md` | **1.5** | 105 wymagań z identyfikatorami, wartościami i metodą weryfikacji |
| DOC-003 | `architektura-systemu.mermaid` | 1.2 | Diagram blokowy systemu |
| DOC-004 | `faza2-fw-specyfikacja.md` | **1.7** | **Specyfikacja firmware.** Punkt A (maszyna stanów), B (bezpieczeństwo, 51 kodów usterek), C.1 (trigger) |
| DOC-005 | `przeglad-komponentow.md` | 1.6 | Cykl życia i dostępność komponentów; **rejestr wzorców błędów** |
| DOC-006 | `plan-naprawczy-audyt.md` | 1.7 | Odpowiedź na pierwszy audyt, 36 pozycji ze statusami |
| DOC-007 | `faza3-specyfikacja-fw.md` | 0.1 | **Nieaktualny**, zachowany jako materiał źródłowy |
| DOC-008 | `diagram-bezpieczenstwa.mermaid` | 1.2 | Łańcuch odcięcia z podziałem na ścieżki sprzętowe i programowe |
| DOC-009 | `diagram-zatrzask.mermaid` | 1.0 | Zatrzask, odblokowanie, licznik resetów |
| DOC-010 | `dossier-audytowe.md` | **1.1** | Ten dokument |

**Kontrola spójności wykonana 11.10.2026 (wersja 1.1):** wersje w spisie zgodne z metrykami plików; brak wiszących odwołań do kodów usterek, luk, ryzyk i założeń; wszystkie 36 pozycji pierwszego audytu obecne w rejestrze; pokrycie wymagań **105/105** po usunięciu ECU-IGN-008 i dodaniu ECU-IGN-020; brak odwołań do usuniętych ECU-IGN-008 i DTC-SEN-04.
