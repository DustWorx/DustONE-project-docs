# Firmware — specyfikacja funkcjonalna

Specyfikacja zachowania firmware ECU. Punkt A (maszyna stanów) i B (bezpieczeństwo, macierz usterek) zamknięte; C.1 (trigger) zamknięty i **wymaga ponownego przeglądu** po rozstrzygnięciu pozycji O-001 i O-005. Punkty C.2–J otwarte.

Wymagania w `wymagania.md`, sprzęt w `produkt.md`, pozycje nierozstrzygnięte w `otwarte.md`.

---

## A. Maszyna stanów ECU

Firmware w każdej chwili znajduje się w dokładnie jednym zdefiniowanym stanie. Stan określa, które wyjścia są aktywne, jakie zadania są wykonywane i jakie zdarzenia mogą go zmienić.

### A.1 Stany

| Stan | Opis | Wyjścia mocy | Pobór |
|---|---|---|---|
| **UŚPIENIE** | **Zmienione 18.10.2026 — architektura INH** (`produkt.md` rozdz. 6). PMIC w STANDBY — IGN niski z INH TJA1043 (od 1.11.2026); procesor, pamięć i czujniki **bez zasilania**. Czuwa tylko TJA1043 w trybie Sleep, zasilany z akumulatora: wzorzec wybudzenia na magistrali i zbocze na pinie WAKE | Wszystkie wyłączone poza zasilaniem HMI (przełącznik domyślnie załączony, ECU-PWR-011) | ≤ 133 µA (bilans `produkt.md` 6.1) |
| **WYBUDZANIE** | Stan przejściowy. **Pełny start firmware** (RAM nie przetrwał uśpienia): uruchomienie watchdoga, odczyt flag Pwon i źródła wybudzenia z ERR_N, zapis przyczyny wybudzenia do logu, odtworzenie stanu z pamięci nieulotnej, wybudzenie HMI, **obsługa PMIC (stan DIAGNOSTIC ≤ 512 ms), załączenie zasilania czujników VSOUT1**, odczekanie na start czujników i ustalenie się progu adaptacyjnego MAX9926 (~1–2 ms), wczytanie konfiguracji i map. Szczegóły: A.4 | Wszystkie wyłączone | — |
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
| ROZRUCH | Obroty > próg (600-800 obr/min) i stabilne → **ECU automatycznie wyłącza rozrusznik**. Iskra z prognozy dopiero po spełnieniu ECU-IGN-036 (> 1000 obr/min, zmiana < 4 % na obrót przez 2 obroty) — do tego czasu na krawędzi spływu | PRACA |
| ROZRUCH | Zwolnienie przycisku startu | Rozrusznik wyłączony; jeśli wał się zatrzyma → GOTOWOŚĆ |
| ROZRUCH | **Przekroczenie 5 s ciągłego kręcenia** | Rozrusznik wyłączony, komunikat na HMI |
| ROZRUCH | Zanik obrotów | GOTOWOŚĆ |
| ROZRUCH / PRACA | Kill switch / wykrycie wywrotki (akcelerometr) / zanik obrotów | ZATRZYMYWANIE |
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
| **Reset w trakcie** | Reset nieplanowany = K4 = rozrusznik zablokowany. Po każdym resecie rozrusznik wymaga **puszczenia i ponownego naciśnięcia START** — wyjątek: wybudzenie z uśpienia (ECU-SAF-018) | ECU-SAF-031, 11.11.2026 |
| **Rozrusznik kręci bez polecenia** (sklejone styki przekaźnika) | Blokada zapłonu + komunikat „ROZRUSZNIK PRACUJE BEZ POLECENIA — ODŁĄCZ AKUMULATOR” (DTC-OUT-05) | ECU-SAF-030, decyzje Pawła 11.11.2026 |

**Sklejony przekaźnik rozrusznika (O-029, decyzje Pawła 11.11.2026).** Prąd rozrusznika (~100 A, przy starcie kilkaset A) płynie z akumulatora wprost przez styki przekaźnika — **ECU ani kill switch go nie przerwą**. Drugi przekaźnik w szeregu rozważony i odrzucony; zostaje wykrycie i blokada zapłonu, żeby silnik nie odpalił.
- **Kryterium:** obroty **100–800 obr/min przez > 3 s bez polecenia rozrusznika** i napięcie akumulatora **niższe o > 1,5 V od ostatniego napięcia spoczynkowego** (zapamiętanego przy zatrzymanym wale). Rozrusznik pobiera 60–100 A i wyraźnie obniża napięcie; toczenie na biegu nie.
- **Zadziałanie bez usterki:** odpalanie na pych przy rozładowanym akumulatorze — dlatego kryterium względne, nie próg bezwzględny (ten blokowałby zapłon w jedynej sytuacji ratunkowej). **Test negatywny:** pych przy akumulatorze 10 V i 12,6 V — bez zadziałania.
- **To blokada startu, nie zatrzymanie pracującego silnika** — przy pracy silnika ładowanie podnosi napięcie, kryterium nie jest spełnione. Lista zamknięta B.1.1 bez zmian.
- Ryzyko resztkowe: na biegu przy puszczonym sprzęgle rozrusznik pcha motocykl (rozdz. 9 `otwarte.md`).

⚠️ **Udokumentowane ryzyko resztkowe:** limit 5 s bez wymuszonej przerwy chroni przed jednorazowym zablokowaniem przycisku, ale nie przed uporczywym odpalaniem — po zwolnieniu i ponownym naciśnięciu licznik startuje od zera. Przyjęte świadomie.

### A.4 Uśpienie i wybudzanie (architektura z 18.10.2026)

**Architektura: szyny 3,3 V i 5 V wyłączane przez INH transceivera TJA1043** (`produkt.md` rozdz. 6). W uśpieniu procesor jest **bez zasilania** — nie ma trybu Stop, RAM nie przetrwa, każde wybudzenie to pełny start firmware.

| # | Źródło | Mechanizm | Uwagi dla FW |
|---|---|---|---|
| 1 | **Ramka CAN z HMI** | TJA1043 w Sleep wykrywa wzorzec wybudzenia na magistrali → INH → szyny → start MCU | Każda zwykła ramka spełnia wzorzec |
| 2 | **Przycisk startu** | Pin WAKE TJA1043 → INH → szyny → start MCU | Przycisk jest nadal wciśnięty, gdy firmware wystartuje — zachowanie rozrusznika: O-024 |
| 3 | **Przyciski na kierownicy** | Pin WAKE TJA1043 w HMI → HMI nadaje → źródło 1 | — |
| 4 | **Podłączenie USB** | Tranzystor ściąga pin WAKE w ECU | — |

**Wybudzanie sygnałem obrotów wału — świadomie odrzucone** (`produkt.md` rozdz. 6.3). **Konsekwencja:** jeśli ECU śpi, kopnięcie samo go nie obudzi — najpierw przycisk.

**Wymagania FW przy starcie (każdy start jest startem od zera):**
1. Transceiver w **Listen-only** → odczyt **Pwon** z ERR_N (zasilanie BAT zanikło — akumulator był odłączony; zegar i dane nie są ciągłe). Odczekanie ok. 8 µs po każdej zmianie trybu (jednostka do potwierdzenia w oryginale karty)
2. Transceiver w **Normal** → odczyt **źródła wybudzenia** z ERR_N przed czwartym zboczem nadawania (lokalne: przycisk lub USB; brak: magistrala). Flaga jest też ustawiana przy pierwszym zasileniu — interpretacja razem z Pwon
3. Zapis przyczyny wybudzenia do logu — diagnoza rozładowań akumulatora
4. Rozpoznanie resetu i odtworzenie zatrzasku K4 z domeny podtrzymywanej (tabela w B.4), potem ustawienie znacznika „ECU pracuje”; motogodziny, przebieg i usterki z W25Q128
5. **Wybudzenie HMI** — gdy ECU nie śpi, HMI też nie śpi
6. **PMIC (od 1.11.2026):** odczekanie końca autotestu BIST (~21 ms — w tym czasie PMIC nie odpowiada po SPI); konfiguracja watchdoga i nadzoru; wyczyszczenie flag WD_FAIL i ERROR_PIN_FAIL; **wyjście ze stanu DIAGNOSTIC w ≤ 512 ms**, inaczej PMIC przechodzi w SAFE (ENDRV niski); w ACTIVE pierwsze dobre zdarzenie watchdoga, potem ustawienie ENABLE_DRV
7. Załączenie zasilania czujników VSOUT1 (bit w PMIC), odczekanie na start czujników (~1–2 ms). MAX9926 pracuje od włączenia VDD5

**Wymagania FW przy usypianiu** (sekwencja: `produkt.md` rozdz. 6.4):
1. Żądanie uśpienia do HMI; potwierdzenie **i** cisza na magistrali dłuższa niż timeout ramki HMI
2. Zapis stanu do pamięci nieulotnej i zakończenie zapisów w toku; **ostatnia czynność przed rozkazem uśpienia: skasowanie znacznika „ECU pracuje”** (B.4)
3. Wyłączenie zasilania czujników VSOUT1
4. Transceiver w **Go-to-Sleep** (STB_N niski, EN wysoki)
5. **Jeśli zasilanie nie zanikło w określonym czasie po rozkazie** — wybudzenie przyszło równocześnie i rozkaz został zignorowany (AH1014, rozdz. 6.2.5). Firmware wraca do pracy, ustawia ponownie znacznik „ECU pracuje” i traktuje to jak wybudzenie

**Usunięte z poprzedniej wersji:** wprowadzanie IMU i pamięci flash w tryby niskiego poboru, przerwania EXTI w trybie Stop — w uśpieniu te układy są bez zasilania.

### A.5 Pozostaje do doprecyzowania (przy punktach B, E)

- Czasy i warunki szczegółowe przejść (histerezy, opóźnienia)
- Maksymalny czas trwania stanu ZATRZYMYWANIE (ile na dokończenie zapisu logów)
- Okno czasowe licznika resetów watchdoga i sposób jego kasowania
- Które usterki są krytyczne (klasyfikacja — punkt E)

---

## B. Bezpieczeństwo i tryby awaryjne

*Opracowywane od 2026-09-20. Domyka pozycje audytu F-023 (macierz usterek) i część F-011.*

**Wymaganie wiążące (z decyzji L1):** reakcja watchdoga rzędu ~100 ms — od 1.11.2026 watchdog PMIC TPS65381A-Q1: sekwencja ~20 ms, ENDRV opada po 5 złych sekwencjach. **Od 4.11.2026 tryb pytanie–odpowiedź z sygnaturą punktów kontrolnych funkcji bezpieczeństwa** (I.2, ECU-SAF-026). Kill switch jest równolegle wejściem GPIO i sygnałem bramkującym drivery sprzętowo (rozdz. 9.1 planu naprawczego), więc jego działanie nie zależy od stanu firmware.

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
| 2 | Potwierdzona wywrotka (akcelerometr) | ECU-SAF-005 | Motocykl leży — silnik nie powinien pracować |
| 3 | Reset watchdoga | ECU-SAF-003 | Przyczyna nieznana, stan sterowania nieokreślony |
| 4 | Zapaść napięcia (brown-out) | ECU-SAF-004 | Stan rejestrów i przebieg przerwanej operacji nieokreślone |
| 5 | Przekroczenie progu ogranicznika obrotów | ECU-IGN-006 | Odcięcie **chwilowe, bez zatrzasku** — funkcja normalna, nie usterka |
| 6 | **Utrata wiarygodnego sygnału obrotów przy pracującym silniku** *(przemianowane 2026-10-11 — patrz C.1.7)* | K4, decyzja 2026-09-20 | Bez sygnału obrotów nie ma bazy czasu — nie da się wyznaczyć momentu zapłonu. Alternatywą byłoby wyzwalanie w losowej fazie. Odcięcie jest tu jawnym zachowaniem zamiast stanu nieokreślonego |
| 7 | **Wtryskiwacz zablokowany otwarty** | K4, decyzja 2026-09-20 | Zwarcie kanału zgłoszone przez TLE9104SH. Zalanie cylindra: uderzenie hydrauliczne w 4T, spłukanie filmu olejowego z gładzi w 2T |
| ~~8~~ | ~~Driver zapłonu zablokowany w stanie załączonym~~ | **Wycofane 2026-09-20** | Po lekturze karty katalogowej VBG08H-E: **firmware nie ma czym tego wykryć**. Wyjście diagnostyczne C.F. odnosi się wyłącznie do stanu wejścia sterującego, więc zwarty tranzystor wyjściowy nie daje sygnału zwrotnego. Zapisanie reakcji na niewykrywalną usterkę byłoby ochroną pozorną. Zagrożenie pokrywają: ograniczenie prądu i miękkie wyłączenie w samym układzie, sprzętowy sufit czasu ładowania (B.2.3) oraz okno watchdoga — analiza w B.2.3 |
| 9 | **Przegrzanie elektroniki ECU — próg T3** *(dopisane 25.10.2026, decyzja Pawła)* | ECU-SAF-020, DTC-SYS-15 | **Ochrona sprzętu, nie bezpieczeństwo kierowcy.** Próg 120 °C wewnątrz obudowy przy projektowanej wartości ~92 °C — występuje tylko przy usterce (obudowa przy wydechu, uszkodzony blok CDI, utrata kontaktu termicznego). Warunki: zgodność dwóch niezależnych czujników przez 10 s; niewiarygodny czujnik wyłącza tę pozycję zamiast ją wyzwalać |

**Lista jest zamknięta.** Dopisanie do niej kolejnej pozycji wymaga osobnej decyzji zapisanej w tym dokumencie, z uzasadnieniem — inaczej lista rozrośnie się przez drobne kroki do wariantu, który odrzuciliśmy. Pozycja 8 została **wycofana tego samego dnia**, gdy okazało się, że nie da się jej wykryć — to samo kryterium, którym odrzuciliśmy zablokowany rozrusznik (B.2.2).

**Rozstrzygnięcie odrzucone — przegrzanie cieczy chłodzącej:** rozważane jako kandydat do K4. **Od 16.11.2026 (decyzja Pawła, O-055) wyłącznie ostrzeżenie K1 — DTC-ENG-01, ECU-DIA-005**, zgodnie z `produkt.md` 1.1; wcześniejszy zapis „pozostaje w K3 (ograniczenie obrotów + ostrzeżenie)” był sprzeczny z zakresem produktu. Trzy powody: (a) czujnik temperatury cieczy jest jednym z najczęściej zawodzących elementów, a przerwa w przewodzie daje odczyt skrajny — fałszywe zgaszenie na podjeździe jest groźniejsze niż zagrożenie, przed którym miało chronić; (b) zgaszenie silnika zatrzymuje pompę cieczy i **pogarsza** przegrzanie lokalnie; (c) podtrzymuje wcześniejszą decyzję L5. Zmiana tej decyzji wymaga wpisu w historii zmian dokumentu.

---

#### B.1.2 Analiza zagrożeń zamkniętej listy zatrzymań — MVP-A (25.10.2026, O-016)

**Zatrzymania** (nr 7 — wtryskiwacz — dotyczy wyłącznie B/C; nr 8 wycofany)

| # | Zatrzymanie | Zagrożenie | Mechanizm | Maks. czas | Fałszywe zadziałanie i ograniczenie |
|---|---|---|---|---|---|
| 1 | Kill switch | Brak możliwości zgaszenia (zablokowany gaz, upadek) | Sprzętowo: zwarcie uzwojenia wzbudzającego + blokada wyzwalania tyrystora; równolegle FW | ≤ 10 ms (ECU-SAF-001) | Przerwa w wiązce gasi silnik — celowo fail-safe; kodowanie rezystorami rozróżnia przerwę (DTC-SAF-01) |
| 2 | Wywrotka | Silnik pracuje przy leżącym motocyklu: koło na biegu, wyciek paliwa | Akcelerometr, kąt ważny przy 0,8–1,2 g | 3 s (ECU-SAF-005) | Hopy i lądowania — bramka ważności zeruje licznik; trawers < 65° |
| 3 | Reset watchdoga | Nieokreślony stan sterowania zapłonem | watchdog PMIC (ENDRV, NRES) | okno watchdoga — **nie jest ochroną pojedynczej iskry** (O-012); tę zapewniają ECU-IGN-023 i ECU-IGN-019 | Reset od zakłóceń w jeździe — EMC (O-039), log przyczyny |
| 4 | Zapaść napięcia | Przerwana operacja, nieokreślone rejestry | BOR MCU | sprzętowo | Z akumulatorem kwasowym i regulatorem nie występuje w jeździe (rozdz. 13.1 `produkt.md`) |
| 5 | Ogranicznik obrotów | Przekręcenie silnika | FW, chwilowe | jeden obrót | Błędny próg — zakres 3000–12 000 walidowany w ECU (ECU-IGN-006) |
| 6 | Utrata sygnału obrotów | Brak podstawy czasu — iskry nie da się wyznaczyć | DTC-IGN-01 | ≥ 100 ms | Wcześniejsze ostrzeżenie o jakości sygnału (DTC-IGN-03a) |
| 9 | Przegrzanie ECU (T3) | Ochrona sprzętu, nie kierowcy | 2 niezależne czujniki | 10 s (ECU-SAF-020) | Usterka czujnika wyłącza T3 zamiast go wyzwalać |

**Uszkodzenia elementów wykonawczych**

| Element | Uszkodzenie | Skutek | Ocena / środek |
|---|---|---|---|
| Tyrystor CDI | zwarcie lub przerwa | Brak iskry, silnik gaśnie | Bezpieczne — kod usterki |
| Prostownik / kondensator CDI | zwarcie | Brak iskry | Bezpieczne |
| Element zwierający uzwojenie wzbudzające | zwarcie | Silnik nie odpali | Bezpieczne |
| **Element zwierający uzwojenie wzbudzające** | **przerwa** | Kill działa tylko przez blokadę tyrystora | **Uszkodzenie ukryte → test przy każdym zgaszeniu (ECU-SAF-021)** |
| **Blokada wyzwalania tyrystora** | **nie blokuje** | Kill działa tylko przez zwarcie wzbudzającego | **Uszkodzenie ukryte → ECU-SAF-021** |
| **PROFET rozrusznika** | **zwarcie wyjścia** | Bez drugiego klucza rozrusznik kręci bez przerwy, bramkowanie wejścia nie pomaga | **Klucz masy cewki przekaźnika sterowany przyciskiem START (ECU-SAF-022, poprawka 1.11.2026)** — rozrusznik tylko przy wciśniętym przycisku, jak fabrycznie |
| **Przekaźnik rozrusznika** (fabryczny) | **sklejone styki** | Rozrusznik kręci bez polecenia; ECU i kill go nie zatrzymają; na biegu przy puszczonym sprzęgle pcha motocykl | Wykrycie i blokada zapłonu (DTC-OUT-05, ECU-SAF-030); **ryzyko zaakceptowane — decyzja Pawła 11.11.2026** (drugi przekaźnik w szeregu odrzucony) |
| **Klucz masy rozrusznika** | **zwarcie** | Rozrusznik tylko na polecenie firmware przy RUN | Bezpieczne — drugi klucz (PROFET) zostaje |
| **Komparator kill switcha** | **utknięty w RUN** | Bramka AND i PROFET rozrusznika bez blokady STOP | Próg tranzystorowy nadal zwiera wzbudzające i blokuje klucz masy rozrusznika; wykrywa test przy STOP (ECU-SAF-021) |
| **Próg tranzystorowy kill switcha** | **utknięty w RUN** | Zwarcie wzbudzającego i blokada klucza masy nieaktywne | Komparator nadal blokuje bramkę AND i PROFET; wykrywa ECU-SAF-021 |
| PROFET wentylatora / świateł | zwarcie | Odbiornik działa stale, rozładowanie na postoju | Kod usterki, akceptowalne |

**Decyzje Pawła 25.10.2026:** test obu ścieżek kill switcha przy każdym zgaszeniu, ze startem dozwolonym przy jednej sprawnej ścieżce; drugi klucz rozrusznika. **1.11.2026:** klucz masy rozrusznika sterowany przyciskiem START (poprzednia wersja, sterowana kill switchem, była zamknięta przez całą jazdę); dwa osobne układy progowe kill switcha (B.1.3). **Analiza wymaga niezależnego przeglądu ludzkiego (O-057)** — jest wynikiem pracy wspieranej modelem.

#### B.1.3 Niezależność mechanizmów „sprzętowych” — wspólne przyczyny (1.11.2026, O-018)

Dla każdego mechanizmu opisanego jako działający bez firmware: co pokrywa, czego jawnie nie pokrywa, od jakiego zasobu zależy. Mechanizm zależny od tego samego zasobu co chroniona funkcja nie jest niezależny.

**Architektura kill switcha i rozrusznika po decyzjach 1.11.2026:**

| Układ progowy | Steruje | Bez zasilania |
|---|---|---|
| **Komparator** | bramka AND toru zapłonu, blokada wejścia PROFET rozrusznika, (B/C) EN TLE9104 | wszystkie zezwolenia nieaktywne → iskra i rozrusznik zablokowane |
| **Próg tranzystorowy** | klucz zwierający uzwojenie wzbudzające, blokada klucza masy rozrusznika, (B/C) RESN TLE9104 | zwarcie wzbudzającego rozwarte (pokrywa bramka AND), klucz masy rozwarty |

Rozrusznik = **(polecenie procesora × komparator RUN)** po stronie plusa **i (przycisk START wciśnięty × próg tranzystorowy RUN)** po stronie masy.

**ENDRV z PMIC** (1.11.2026) jest dodatkowym, niezależnym od procesora warunkiem dla: bramki AND zapłonu, PROFET rozrusznika, (B/C) EN TLE9104 i PROFET pompy.

| # | Mechanizm | Pokrywa | Jawnie nie pokrywa | Zasób współdzielony | Ocena |
|---|---|---|---|---|---|
| 1 | Ścieżka 1 kill: zwarcie wzbudzającego (próg tranzystorowy) | STOP i przerwę przewodu przy dowolnym stanie firmware; odcina energię kolejnych iskier | już naładowany kondensator (jeszcze jedna iskra — pokrywa ścieżka 2); próg bez zasilania | przewód i przycisk kill (O-015) | niezależna od firmware i od komparatora |
| 2 | Ścieżka 2 kill: bramka AND (komparator) | STOP, przerwę przewodu, brak zasilania komparatora lub bramki | uszkodzenie bramki przepuszczające impuls mimo braku zezwolenia; komparator utknięty w RUN (pokrywa ścieżka 1) | przewód i przycisk kill | niezależna od firmware i od progu tranzystorowego |
| 3 | Rozrusznik: dwa klucze z różnych źródeł polecenia | pojedyncze zwarcie dowolnego klucza; polecenie firmware bez przycisku; usterkę jednego progu | zwarcie obu kluczy; przycisk START zwarty (np. woda) **i** jednocześnie polecenie firmware | przekaźnik; przycisk START (także budzenie) | niezależne parami |
| 4 | Bramka impulsowa tyrystora (ECU-IGN-005) | wyjście HRTIM zawieszone w stanie wysokim lub niskim, zamrożony zegar — najwyżej 1 iskra | wyjście, które się przełącza: każde zbocze = iskra (błędny kod, programowe wymuszenie, zakłócenie na linii) | brak — elementy bierne | niezależna, **tylko dla stanów zawieszonych** |
| 5 | Start timera zboczem natarcia (ECU-IGN-023) | błąd prognozy przy poprawnym firmware | **błędne firmware:** HRTIM ma programowe wymuszenie wyjścia (rejestr SETxR, bit SST — „Software Set trigger”, zapis 1 wymusza stan aktywny); źródło zdarzenia i opóźnienie zapisuje firmware | procesor, firmware, konfiguracja HRTIM | **nie jest niezależny od firmware** — brzmienie poprawione 1.11.2026; **MPU** (ECU-SAF-023): zapis tylko z modułu zapłonu; sprzętowe okno kątowe do oceny z O-009 |
| 6 | Watchdog (dawniej TPS3430-Q1) | zawieszenie, kod poza oknem czasowym, awarię zegara procesora | pojedynczą błędną iskrę (O-012, dopuszczalny czas 0); procesor zatrzaśnięty (latch-up) — reset go nie przywraca; pętlę, która poprawnie obsługuje watchdog (O-012) | szyna 3,3 V z procesorem; **skutek wyłącznie przez reakcję procesora na reset** | **rozwiązane 1.11.2026:** watchdog PMIC opuszcza ENDRV → bramka AND i rozrusznik zablokowane bez udziału procesora |
| 7 | BOR w STM32G474 | spadek 3,3 V poniżej progu | próg ustawiony za nisko (bajty opcji); uszkodzenie procesora | struktura chronionego procesora | **rozwiązane 1.11.2026:** niezależny nadzór UV/OV w PMIC (reset, ENDRV); BOR zostaje jako druga warstwa |
| 8 | Power Good przetwornic (do 1.11.2026) | wykrycie szyny poza tolerancją | reakcję — sygnał trafia tylko do firmware | firmware | przetwornice zastąpione PMIC — nadzór z reakcją sprzętową |
| 9 | Rezystory ściągające (ECU-SAF-007, -016) | piny zwolnione: reset, brak zasilania sterownika | pin aktywnie wysterowany (błąd firmware, latch-up); przerwa rezystora (ukryta, dopóki pin jest sterowany) | zwolnienie pinów przez procesor w resecie | niezależne od firmware, zależne od procesora |
| 10 | Przełącznik obciążenia 5 V | izolację zwarcia w wiązce czujników od reszty płytki | — | **zasila też kondycjoner wału i komparator: zwarcie w wiązce czujnika gasi silnik** | **rozwiązane 1.11.2026:** czujniki na VSOUT1 PMIC (ochrona zwarć), kondycjoner i komparator na VDD5 |
| 11 | Rezystor rozładowujący (ECU-IGN-026) | rozładowanie po zatrzymaniu | — | brak | **rozwiązane 1.11.2026:** osobny łańcuch pomiarowy; przerwa łańcucha rozładowującego wykrywana po zatrzymaniu (ECU-IGN-029), pomiarowego — w pracy (DTC-IGN-09) |
| 12 | Ochrony wewnętrzne PROFET | przeciążenie i przegrzanie kanału | zwarty klucz | zasilanie z akumulatora | niezależne |

**Wspólna przyczyna, która zostaje:** przewód i przycisk kill switcha — oba progi czytają ten sam przewód. Pełna analiza uszkodzeń przewodu w O-015.

**Analiza wspierana modelem — przed PCB wymaga niezależnego przeglądu ludzkiego (O-057).**

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
| DTC-SEN-04 **[B/C]** | Położenie przepustnicy — **kod nie został usunięty, obowiązuje wyłącznie w wariantach B/C**, w których czujnik przepustnicy istnieje; w MVP-A nie ma go czym wywołać. Pierwotnie opisany jako usunięty — to była nieścisłość zapisu *(MVP-A nie ma TPS — założenie Z1 obalone 11.10.2026)* | napięcie < 3% lub > 97% | **100 ms** | **K3** | **Mapa awaryjna liczona na pełne obciążenie** (bogata w całym zakresie) + ograniczenie do **3500 obr/min**. Szczegóły i uzasadnienie: B.3.2 | Poziom P2 — komunikat musi wyjaśniać, że silnik pracuje na bogato celowo |
| DTC-SEN-05 | Napięcie akumulatora — odczyt niemożliwy | poza 5–20 V (uszkodzenie dzielnika lub ADC) | 1000 ms | **K1** | Korekty napięciowe na wartościach nominalnych | Kreski + komunikat |
| DTC-SEN-06 | Prędkość koła — brak sygnału | brak impulsów przy obrotach silnika > 2000 obr/min **i biegu innym niż N** (od 25.11.2026); przy usterce czujnika biegu (DTC-SEN-07) kod nieaktywny | **15 s** (od 25.11.2026 — wleczenie się na sprzęgle ~1 km/h daje jeden impuls na ~8 s) | **K1** | Bez wpływu na sterowanie silnikiem | Wskazanie wygaszone + komunikat |
| DTC-SEN-07 | Pozycja biegu — odczyt poza zakresem lub brak odpowiedzi | błąd transmisji SPI lub kąt poza zakresem kalibracji | 200 ms | **K1** | Bez wpływu na sterowanie silnikiem | Wskazanie biegu wygaszone |
| DTC-SEN-08 | Ciśnienie barometryczne — brak komunikacji lub błąd diagnostyki KP464 | 3 kolejne nieudane odczyty SPI albo kod diagnostyczny czujnika (tor sygnału, komórka, EEPROM) | 3 próby | **K1 w MVP-A, K2 w B/C** | **MVP-A:** tylko kod usterki i brak wartości w logu — ciśnienie nie wpływa na sterowanie. **B/C:** wartość zastępcza 1013 hPa (poziom morza — mieszanka bogatsza, kierunek bezpieczny) | Komunikat |
| DTC-SEN-09 | Akcelerometr — brak komunikacji | 3 kolejne nieudane odczyty SPI | 3 próby | **K1** | Wykrywanie wywrotki nieczynne | Komunikat „WYKRYWANIE WYWROTKI NIECZYNNE" |
| **DTC-ENG-01** | **Przegrzanie silnika** (od 16.11.2026, O-055) | temperatura cieczy > 100 °C; ustąpienie < 95 °C | 5 s | **K1** | Ostrzeżenie „PRZEGRZANIE SILNIKA”, **bez ograniczania obrotów** (ECU-DIA-005); log z maksymalną temperaturą |



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
| DTC-IGN-02 | **Sygnał obrotów niewiarygodny** — powtarzalne naruszenie kryteriów z C.1.7 | długość wypustu poza ±25% kalibracji, zbocze poza oknem kątowym, stosunek okresów poza 0,5–2,0 | **2 kolejne obroty wału** | **K4 — wyłącznie w PRACY** (od 25.11.2026, O-009) | Odcięcie + zatrzask. W ROZRUCHU i GOTOWOŚCI — DTC-IGN-11 |
| DTC-IGN-03 | **Odrzucone zbocze pojedyncze** | zbocze poza oknem kątowym (C.1.6) | — | **K0** | **Zbocze ignorowane**, zapłon bez zmian z modelu kąta. Wyłącznie licznik |
| DTC-IGN-03a | **Podwyższona liczba odrzuceń** — jakość sygnału | > 5 odrzuceń na 100 obrotów | 100 obrotów | **K1** | Ostrzeżenie o jakości sygnału; wskazuje na zakłócenia lub luźny czujnik |
| **DTC-IGN-08** | **Brak napięcia uzwojenia wzbudzającego przy obracającym się wale** | dzielnik wzbudzającego → ADC: brak napięcia przy ważnym sygnale obrotów | 3 obroty | **K1** | Kod usterki „ZAPŁON — BRAK ZASILANIA CDI”; silnik i tak gaśnie z braku iskry. Rozróżnia przerwę w uzwojeniu/wiązce od usterki ECU (dawne DTC-IGN-04 i -05 dla cewki indukcyjnej wycofane 25.10.2026) |
| **DTC-IGN-09** | **Brak odczytu napięcia kondensatora przy pracującym silniku** | łańcuch pomiarowy (ECU-IGN-028): odczyt poniżej `[DO USTALENIA]` V przy obecnym napięciu wzbudzającego i ważnych obrotach | 10 obrotów | **K1** | Kod usterki „POMIAR CDI”; silnik pracuje dalej, jeśli iskra jest. Przerwa łańcucha pomiarowego albo usterka ładowania (wtedy silnik gaśnie z braku iskry) |
| **DTC-IGN-10** | **Kondensator CDI nie rozładowuje się** | po zatrzymaniu wału, przy stojącym wale: > 60 V po 5 s (ECU-IGN-029) | — | **K1** | Ostrzeżenie „CDI — RYZYKO PORAŻENIA PRZY SERWISIE”; na silnik bez wpływu. Sprawdzenie przerywane przy ruchu wału |
| **DTC-IGN-11** | **Sygnał obrotów niewiarygodny w rozruchu** (od 25.11.2026, O-009) | kryteria C.1.7 w ROZRUCHU albo GOTOWOŚCI | — | **K0** | Powrót do stanu synchronizacji BRAK, iskra zablokowana do ponownej synchronizacji; licznik w logu (C.1.12) |
| **DTC-IGN-06** | **Wyzwolenie tyrystora niezgodne ze zleceniem** — usterka wykonania (firmware, timer, zakłócenie) | przechwycony moment wyzwolenia różni się od zleconego o więcej niż odpowiednik granicy ECU-IGN-022 | **1 zdarzenie** | **K3** | Tryb zastępczy: iskra na krawędzi spływu (GMP) + ograniczenie obrotów; ostrzeżenie (ECU-IGN-024) |
| **DTC-IGN-07** | **Błąd prognozy kąta powyżej granicy** przy wyzwoleniu zgodnym ze zleceniem — gwałtowna zmiana prędkości wału | kąt rzeczywisty wyliczony wstecz z następnego obrotu poza +1° / −2° względem zadanego | **3 w 100 obrotach** | **K3** | Jak DTC-IGN-06. Każde pojedyncze przekroczenie zapisywane w logu (K0) |
| DTC-INJ-01 | Wtryskiwacz zablokowany otwarty | diagnostyka SPI TLE9104SH — zwarcie do masy | natychmiast | **K4** | Odcięcie + zatrzask |
| DTC-INJ-02 | Wtryskiwacz — przerwa obciążenia | diagnostyka SPI | 3 kolejne wtryski | **K3** | Ograniczenie obrotów — w wariancie dwuwtryskiwaczowym praca na jednym daje ubogą mieszankę |
| DTC-INJ-03 | Driver wtrysku — przegrzanie | diagnostyka SPI | natychmiast | **K3** | Ograniczenie obrotów |
| DTC-INJ-04 | Driver wtrysku zgłasza utratę konfiguracji | rejestr stanu SPI TLE9104SH | 3 próby ponownej konfiguracji | **K3** | Po wyczerpaniu prób ograniczenie obrotów |
| DTC-OUT-01 | Kanał pompy paliwa — zwarcie lub przeciążenie | diagnostyka BTS7008-2EPA | 3 próby ponownego załączenia | **K3** | Ograniczenie; silnik i tak zgaśnie z braku paliwa |
| DTC-OUT-02 | Kanał wentylatora — zwarcie lub przeciążenie | jw. | 3 próby | **K1** | Kanał wyłączony; ostrzeżenie „WENTYLATOR — AWARIA, KONTROLUJ TEMPERATURĘ” (od 16.11.2026 bez ograniczania obrotów — ECU-DIA-005) |
| DTC-OUT-03 | Kanał świateł — zwarcie lub przeciążenie, **osobno dla postojowych, mijania i drogowych** (od 25.11.2026, ECU-AUX-004) | jw. | 3 próby | **K1** | Wyłączony tylko uszkodzony kanał; pozostałe światła pracują. Komunikat wskazuje kanał |
| DTC-OUT-04 | Kanał rozrusznika zablokowany załączony | prąd mimo wyłączonego sterowania — *możliwość wykrycia do potwierdzenia w Fazie 4* | 200 ms | **K1** | Komunikat „ODŁĄCZ AKUMULATOR" |
| **DTC-OUT-05** | **Rozrusznik pracuje bez polecenia — sklejone styki przekaźnika** (od 11.11.2026, O-029) | obroty 100–800 obr/min > 3 s bez polecenia rozrusznika **i** napięcie akumulatora niższe o > 1,5 V od ostatniego spoczynkowego | 3 s | — | **Blokada startu (zapłon zablokowany)** + komunikat „ROZRUSZNIK PRACUJE BEZ POLECENIA — ODŁĄCZ AKUMULATOR”; ustępuje po zatrzymaniu wału |
| **DTC-OUT-06** | **Kanał aux — zwarcie lub przeciążenie, osobno dla aux 1 i aux 2** (od 25.11.2026) | diagnostyka BTS7008-2EPA | 3 próby | **K1** | Wyłączony tylko uszkodzony kanał; komunikat wskazuje kanał |

**Przebudowa DTC-IGN-02 i 03 — korekta 2026-10-11 po pomiarach koła impulsowego.** Dotychczasowe brzmienie mówiło o wzorze zębów i zgubionym zębie, czyli opisywało detekcję właściwą dla koła 60-2. **Beta 300 RR ma jeden wypust na obrót**, więc nie ma wzoru zębów ani zgubionego zęba — oba zapisy opisywały mechanizm, którego nie da się zrealizować.

W dwusuwie nie występuje też **utrata synchronizacji** w sensie czterosuwowym: silnik pali co obrót, jeden wypust to jedna iskra, nie ma dwuznaczności suwu do rozstrzygnięcia. Realnym zagrożeniem nie jest utrata fazy, tylko **fałszywe zbocze od instalacji zapłonowej**, które przesunęłoby iskrę w przypadkowy kąt.

**Dlaczego DTC-IGN-03 jest klasy K0 i nie powoduje żadnej reakcji poza zliczeniem:** zbocze rozpoznane jako fałszywe jest **ignorowane**, a zapłon przebiega normalnie na podstawie ciągłego modelu kąta (C.1.3). Nie traci się iskry i nie gasi silnika. Dopiero powtarzalne naruszenie kryteriów przechodzi w DTC-IGN-02, a podwyższona liczba odrzuceń w DTC-IGN-03a jako ostrzeżenie o jakości instalacji. Mechanizm bramkowania kątowego — C.1.6.

**Dlaczego zablokowany rozrusznik nie trafia do K4**, mimo że niszczy mechanikę: odcięcie zapłonu nic tu nie daje. Zwarty kanał wysokiego napięcia pozostaje zwarty niezależnie od tego, czy silnik pracuje, a zgaszenie silnika nie przerywa pracy rozrusznika. Jedyne skuteczne działanie jest po stronie kierowcy — odłączenie zasilania. Wpisanie tego do K4 dawałoby złudzenie ochrony.

---

#### B.2.3 Blok AC-CDI: sterowanie i diagnostyka (przebudowa 25.10.2026, O-001)

**Zastępuje rozdział o VBG08H-E** (driver usunięty 15.10.2026, zapłon nie jest indukcyjny; poprzednia treść w historii repozytorium).

| Element | Rola | Wymaganie |
|---|---|---|
| Uzwojenie wzbudzające → dioda → kondensator zapłonowy | Ładowanie **bierne**, bez udziału firmware — kondensator ładuje się przez uzwojenie pierwotne cewki przy każdym półokresie | ECU-IGN-025, Z14 |
| Tyrystor | Rozładowanie kondensatora przez uzwojenie pierwotne = iskra. Wyłącza się sam po spadku prądu poniżej prądu podtrzymania | — |
| **Bramka tyrystora sprzężona pojemnościowo** (kondensator szeregowy + dioda rozładowująca + rezystor bramka–katoda) | Zbocze z HRTIM daje jeden krótki impuls prądu bramki; **zawieszone wyjście w stanie wysokim daje najwyżej jedną iskrę** | **ECU-IGN-005** |
| **Bramka AND w torze impulsu:** impuls z HRTIM × zezwolenie z komparatora kill switcha, rezystory ściągające na obu wejściach | Druga ścieżka odcięcia (obok zwarcia uzwojenia wzbudzającego). **Komparator jest zezwoleniem, nie wetem:** zanik jego zasilania blokuje iskrę sprzętowo. Zastępuje tranzystor zwierający bramkę do katody (decyzja Pawła 1.11.2026) | ECU-SAF-001, -016 |
| **Klucz zwierający uzwojenie wzbudzające**, sterowany **progiem tranzystorowym** kill switcha (nie komparatorem — 1.11.2026) **oraz ogranicznikiem ładowania** (suma logiczna, 9.11.2026) | Pierwsza ścieżka odcięcia: odcina energię kolejnych iskier. Bez zasilania rozwiera się — zanik zasilania pokrywa bramka AND | ECU-SAF-001 |
| **Ogranicznik ładowania kondensatora** (próg WN zasilany z obwodu WN → klucz zwierający uzwojenie wzbudzające) | Zatrzymuje ładowanie, gdy napięcie kondensatora przekroczy próg; **bez firmware i bez zasilania ECU**. Szczegóły niżej | **ECU-IGN-034** |
| **Obwód tłumiący RC na tyrystorze + rezystor bramka–katoda** | Odporność na zakłócenia z przewodu cewki | **ECU-IGN-035** |
| Dzielnik napięcia uzwojenia wzbudzającego → ADC | Test obu ścieżek kill switcha przy zgaszeniu; diagnostyka utraty wzbudzającego | ECU-SAF-021, DTC-IGN-08 |
| Przechwytywanie wyzwolenia (wejście timera) | Porównanie rzeczywistego wyzwolenia ze zleconym | ECU-IGN-024 |
| Rozładowanie kondensatora po zatrzymaniu | Bezpieczeństwo serwisu | ECU-IGN-026 |

**Wymaganie dla firmware (bramka AND):** przez cały czas, gdy kill switch jest w STOP, wyjście HRTIM musi być w stanie niskim, a zapłon może wrócić dopiero po ponownej synchronizacji. Inaczej zwolnienie przycisku w chwili wysokiego stanu wyjścia przepuści zbocze i da jedną iskrę w przypadkowym kącie (`produkt.md` rozdz. 7, scenariusze negatywne).

**Czego impulsowa bramka nie robi:** nie chroni przed procesorem generującym fałszywe zbocza — każde zbocze to impuls. Przed tym chronią ECU-IGN-024 (reakcja od pierwszego zdarzenia), watchdog i obie ścieżki kill switcha.

**Pomiar napięcia kondensatora (od 1.11.2026, ECU-IGN-028):** HRTIM wyzwala przetwornik ADC sprzętowo tuż przed zaplanowanym impulsem bramki — kondensator jest wtedy naładowany, a napięcie stoi. Po zatrzymaniu wału firmware śledzi rozładowanie (ECU-IGN-029).

**MPU (od 1.11.2026, ECU-SAF-023):** rejestry HRTIM w obszarze dostępnym tylko dla modułu zapłonu w trybie uprzywilejowanym. Wymaga systemu czasu rzeczywistego z obsługą MPU (np. FreeRTOS-MPU) i podziału zadań na uprzywilejowane i zwykłe.

**Pominięta iskra przeładowuje kondensator — poprawka 9.11.2026 (O-003).** Dawny zapis („kondensator pozostaje naładowany”) był błędny: uzwojenie wzbudzające ładuje kondensator dalej w każdym półokresie, a napięcie dąży do szczytu uzwojenia, który rośnie z obrotami. Bez rozładowania przekracza 1000 V i niszczy tyrystor (opis projektanta AC-CDI, transmic.fr). Dotyczy **każdej** pominiętej iskry: ogranicznik obrotów, K4 przy toczeniu, ENDRV, komparator, zawieszony procesor, przerwa w obwodzie cewki, a także **uśpione ECU przy wale obracanym na biegu**. Kill switch tego problemu nie ma — zwiera uzwojenie.

**Ogranicznik ładowania (ECU-IGN-034, decyzja Pawła 9.11.2026):** próg wysokonapięciowy (łańcuch diod Zenera) na kondensatorze załącza **ten sam klucz, który zwiera uzwojenie wzbudzające przy kill** — suma logiczna z progiem tranzystorowym. Prąd sterujący pobiera z obwodu WN, więc **działa bez firmware i bez zasilania ECU**. Klucz w stanie zwarcia prawie nie grzeje. Odrzucony sam ogranicznik przepięć (TVS/warystor): przy długim odcięciu musiałby stale rozpraszać moc uzwojenia — szacunek z energii iskry ½·C·U² × liczba iskier: rzędu 10 W przy 10 000 obr/min.
- **Pokrywa:** wszystkie przyczyny pominiętej iskry wymienione wyżej. **Nie pokrywa:** rozwarcia klucza zwierającego (traci się wtedy też ścieżka 1 kill — wykrywa test przy zgaszeniu, ECU-SAF-021); zakłóceń szybszych niż reakcja klucza — zostaje ochrona przepięciowa na kondensatorze.
- **Próg:** powyżej najwyższego napięcia kondensatora fabrycznego CDI w całym zakresie obrotów (pomiar, krok 4), z zapasem ustalonym po pomiarze; **≤ 60 % VDRM tyrystora (720 V)** i poniżej napięcia znamionowego kondensatora. Wartość do zatwierdzenia przez Pawła po pomiarze. Reakcja w obrębie półokresu — przeładowanie narasta przez wiele obrotów.
- **Zasób współdzielony:** klucz zwierający ze ścieżką 1 kill switcha. Nie zależy od zasilania ECU, zegara ani procesora.
- **Zadziałanie bez usterki:** za niski próg przy wysokich obrotach obciąłby energię iskry (narusza ECU-IGN-025). **Test negatywny:** pełny zakres obrotów przy normalnym zapłonie — ogranicznik nie działa ani razu (zapaść napięcia uzwojenia widoczna na ADC).

**Samoczynne załączenie tyrystora przy przełączaniu odcięć — wykluczone (O-003).** Napięcie anody rośnie najwyżej z szybkością prąd uzwojenia / pojemność kondensatora, a prąd ogranicza od góry szczyt napięcia / rezystancja uzwojenia (pomiar, kroki 2 i 4; Z23). Szacunkowo pojedyncze V/µs wobec ≥ 1000 V/µs tyrystora. Realne zagrożenie to **zakłócenie z wiązki na przewodzie cewki**, które kondensator sprzęga wprost na anodę — stąd obwód RC i rezystor bramka–katoda (ECU-IGN-035). Pojedyncza iskra w złym kącie może dać odbicie kopniaka, więc chroni zapobieganie, nie wykrywanie.

**Wartości elementów bramki** — tyrystor ST TN3050H-12GY-TR (`produkt.md` 3.2): impuls ≥ 2 × IGT maks. w −40 °C, narastanie ≤ 100 ns, tranzystor wzmacniający z VDD5 przed kondensatorem sprzęgającym, rezystor bramka–katoda 100–220 Ω. Indukcyjność uzwojenia pierwotnego cewki — pomiar (Z22).

##### Decyzja architektoniczna: impuls zapłonu generuje peryferium, nie program

**Decyzja 2026-09-20.** Impuls sterujący driverem zapłonu powstaje w peryferium HRTIM mikrokontrolera, a nie przez zapis do rejestru portu z poziomu zadania.

Uzasadnienie liczbowe: przy 6000 obr/min jeden stopień obrotu wału trwa 27,8 µs, przy 10 000 obr/min — 16,7 µs. Wymaganie ECU-IGN-002 dopuszcza błąd ≤ 1,0° w 99,9 percentylu. Wyjście przełączane z poziomu zadania podlega opóźnieniom obsługi przerwań i szeregowania rzędu dziesiątek mikrosekund, czyli rzędu całego budżetu błędu — **wymaganie byłoby niespełnialne niezależnie od jakości kodu**. Układ porównania w timerze wystawia zbocze z jitterem rzędu nanosekund.

To jest standard branżowy, nie rozwiązanie autorskie: NXP eTPU to osobny procesor z własnym rdzeniem i pamięcią, z gotowymi funkcjami *Spark and Dwell Time*, sterowania wtryskiem i trybem kątowym; Infineon AURIX ma GTM, Renesas RH850 ma ATU. Decyzja porządkuje też wybór STM32G474 — układ wybrano właśnie za HRTIM, a przy sterowaniu programowym HRTIM byłby zbędny.

##### Impulsowa bramka tyrystora — domknięcie ECU-IGN-005 (25.10.2026)

Dawne domknięcie (rejestr okresu HRTIM jako sufit czasu ładowania cewki) **przestało dotyczyć** — w CDI nie ma czasu ładowania sterowanego przez firmware, a pozycja O-004 wskazała, że rejestr okresu dzieli zegar z funkcją, którą miał chronić. Nowe zabezpieczenie jest **niezależne od zegara i firmware**: kondensator w torze bramki przenosi tylko zbocze, więc żaden stan wyjścia — także zamarznięty licznik — nie da ciągłego wyzwalania. Weryfikacja: T-IGN-005.

---

#### B.2.4 Grupa 3 — komunikacja i zasilanie (decyzja 2026-09-20)

| DTC | Usterka | Wykrycie | Potwierdzenie | Klasa | Reakcja |
|---|---|---|---|---|---|
| DTC-COM-01 | Zanik komunikacji z HMI | brak poprawnej ramki od HMI | 1000 ms (ECU-DIA-003) | **K1** | Log + praca silnika bez zmian |
| DTC-COM-02 | Ramka odrzucona — suma kontrolna lub licznik sekwencyjny | pojedyncze odrzucenie | — | **K0** | Tylko licznik odrzuceń |
| DTC-COM-02a | Seria odrzuceń — pogorszona jakość magistrali | > 10 odrzuceń w 1 s | — | **K1** | Komunikat „ZAKŁÓCENIA MAGISTRALI" |
| DTC-COM-03 | Kontroler CAN w stanie bus-off | flaga peryferium FDCAN | — | **K1** | Automatyczne odzyskiwanie; 3 wystąpienia w 10 s → komunikat |
| DTC-COM-04 | Niezgodność wersji protokołu ECU↔HMI | wymiana numerów wersji przy nawiązaniu połączenia (SYS-COM-005) | natychmiast | **K1** | **HMI wygasza wszystkie dane i wyświetla wyłącznie komunikat o niezgodności** — patrz decyzja niżej |
| **DTC-COM-05** | **HMI nie odpowiada mimo restartów zasilania** | 3 kolejne restarty zasilania HMI (SYS-COM-010) bez odzyskania ramek | — | **K1** | Log; dalej jedna próba restartu co 60 s; praca silnika bez zmian |
| **DTC-HMI-01** | **Przyciski HMI — stan nieprawidłowy lub zwarcie kabla** (od 9.11.2026, O-035) | zgłoszenie z HMI: odczyt drabinki poza oknami albo r < 0,016 przez > 1 s | 1 s | **K1** | Log; przyciski nieaktywne do ustąpienia; odblokowanie K4 kill switchem |
| **DTC-HMI-02** | **Przycisk HMI zablokowany** (od 9.11.2026, O-035) | zgłoszenie z HMI: przycisk trzymany > 30 s | 30 s | **K1** | Log; przycisk ignorowany do zwolnienia |
| **DTC-HMI-03** | **Panel HMI powyżej granicy pracy** (od 11.11.2026, O-034) | zgłoszenie z HMI: temperatura panelu > 70 °C | — | **K0** | Log z maksymalną temperaturą i czasem trwania; HMI ogranicza podświetlenie do 50 % (HMI-UI-004) |
| **DTC-HMI-04** | **Błędny układ ekranu HMI** (od 25.11.2026, O-055) | zgłoszenie z HMI: suma kontrolna albo wersja układu niezgodna przy starcie | — | **K1** | HMI pokazuje układ domyślny z firmware; ostrzeżenie „UKŁAD EKRANU USZKODZONY — WGRAJ PONOWNIE”; silnik bez zmian (HMI-UI-013) |
| **DTC-HMI-05** | **Czujnik światła HMI — usterka** (od 25.11.2026, O-055) | zgłoszenie z HMI: brak odpowiedzi albo wartość poza zakresem | 2 s | **K0** | Jasność 100 % (z ograniczeniem HMI-UI-004); log (HMI-UI-014) |
| DTC-PWR-05 | Napięcie akumulatora niskie przy pracującym silniku | < 11,0 V **przy obrotach > 2000 obr/min** | 5 s | **K1** | Ostrzeżenie „ŁADOWANIE — AWARIA" |
| DTC-PWR-06 | Napięcie krytycznie niskie | < 9,0 V | 2 s | **K1** | Ostrzeżenie krytyczne; poniżej 9,0 V wychodzimy poza SYS-ENV-001 |
| DTC-PWR-07 | Przepięcie | > 16,5 V | 200 ms | **K1** | Ostrzeżenie + **załączenie wentylatora jako obciążenia**; wyłączenie po spadku poniżej 15,5 V |
| DTC-PWR-08a | **Zasilanie czujników VSOUT1 poza zakresem** (od 1.11.2026) | ADC poza 4,50–5,50 V albo flaga UV/OV/ograniczenia prądu z PMIC | 100 ms | **K2 w MVP-A, K3 w B/C** | **MVP-A:** wszystkie czujniki z wiązki na wartościach zastępczych (B.2.1), bez limitu obrotów. **B/C:** grupa G3 — strategia jak przy utracie TPS (B.3.1) |
| DTC-PWR-08b | **Szyna VDD5 poniżej zakresu pracy MAX9926 albo przepięcie VDD5** (od 1.11.2026; próg i rozruch od 25.11.2026, O-044) | ADC VDD5 **< 4,55 V** (4,50 V z karty MAX9926 + zapas na błąd pomiaru ±1 %) albo flaga przepięcia VDD5 z PMIC (ENDRV już niski sprzętowo) | 100 ms | **K4 w PRACY; w ROZRUCHU i GOTOWOŚCI — bez zatrzasku** | **PRACA:** silnik gaśnie, **przyczyna źródłowa dla zatrzasku** — patrz decyzja niżej. **ROZRUCH, GOTOWOŚĆ:** iskra zablokowana, synchronizacja → BRAK (C.1.12), zapis w logu; po powrocie VDD5 rozruch można ponowić |
| DTC-PWR-09 | Szyna 3,3 V poza zakresem | ADC poza 3,15–3,45 V | 100 ms | **K1** | Ostrzeżenie + wymuszony zapis logu; przy dalszym spadku sprawę przejmuje brown-out (DTC-SAF, grupa 4) |
| DTC-PWR-10 | Zasilanie czujników VSOUT1 (PMIC) nie załączyło się | brak napięcia na szynie czujników po 5 ms od załączenia | 3 próby | **K3** | Blokada wyjścia ze stanu GOTOWOŚĆ — bez tej szyny nie ma odczytów czujników |

**Warunek obrotów przy DTC-PWR-05 jest konieczny.** Przy rozruchu zapad napięcia do 9 V jest normalny — rozrusznik pobiera kilkadziesiąt amperów. Bez warunku `obroty > 2000` ECU zgłaszałoby awarię ładowania przy każdym odpaleniu i kierowca przestałby zwracać uwagę na ten komunikat, co jest gorsze niż jego brak.

**Rozdzielenie DTC-PWR-08 — korekta wprowadzona 2026-09-22 po uwadze Pawła.** Pierwotnie awaria szyny 5 V miała jedną klasę K3 z ograniczeniem obrotów. To było niepełne: **MAX9926 jest zasilany z tej szyny**, więc przy jej zaniku nie ma czego ograniczać — silnik gaśnie z braku sygnału obrotów. Ograniczenie ma sens wyłącznie w paśmie, w którym szyna jest poza tolerancją, a układ dalej pracuje (4,50–5,50 V wg karty katalogowej MAX9926, przy progu wykrycia 4,75–5,25 V). Stąd dwie pozycje zamiast jednej.

Klasa K4 dla DTC-PWR-08b nie narusza zamkniętej listy zdarzeń odcinających z B.1.1 — odcięcie następuje przez zdarzenie 6 (utrata sygnału synchronizacji), które na tej liście jest. DTC-PWR-08b wskazuje przyczynę źródłową, nie tworzy nowego zdarzenia odcinającego.

##### Domeny zasilania — co pracuje w warunkach karty (25.11.2026, O-044)

**Przypadek „szyna 5 V = utrata sygnału obciążenia” nie występuje od 1.11.2026:** VDD5 (wewnętrzna) i VSOUT1 (czujniki w wiązce) to osobne szyny PMIC z osobnymi reakcjami (ECU-PWR-008a). Poniżej — dla każdego zakresu, które elementy pracują w gwarantowanych warunkach.

| Szyna i zakres | W warunkach karty | Wykrycie | Reakcja |
|---|---|---|---|
| **Akumulator 9,0–16,0 V** | wszystko (SYS-ENV-001) | ADC PE15 | — |
| **Akumulator 7,0–9,0 V** | PMIC i wszystkie szyny w regulacji; zapłon A z uzwojenia wzbudzającego (kopnięcie przy 7 V — A14) | ADC | DTC-PWR-06 — ostrzeżenie |
| **Akumulator ~5,2–7 V** (szacunek: spadek na diodzie polaryzacji i przetwornicy VDD6) | 3,3 V w regulacji (karta PMIC R1.3: działa do 4,5 V na VBATP); VDD6 w dropoucie; VDD5 zaczyna spadać | flaga VDD5_UV PMIC, ADC VDD5 | wg wiersza VDD5 |
| **VBATP < 4,5 V** | PMIC wyłączony | sprzętowo | NRES i ENDRV niskie — brak iskry niezależnie od firmware |
| **VDD5 4,55–5,20 V** | MAX9926 (4,5–5,5 V), TJA1043 VCC, bramka AND, komparator kill (dobór: praca od 4,5 V), sterowanie bramki tyrystora (wymiarowane przy 4,5 V) | ADC PD14 | — |
| **VDD5 4,50–4,55 V** | w karcie, ale w niepewności pomiaru | ADC PD14 | DTC-PWR-08b może zadziałać — po stronie bezpiecznej |
| **VDD5 < 4,50 V** | **MAX9926 i TJA1043 poza kartą**; komparator kill — nieokreślony; PMIC tylko ustawia flagę (tab. 5-2: NRES, ENDRV bez zmian) | ADC PD14 < 4,55 V | **DTC-PWR-08b:** w PRACY K4; w ROZRUCHU i GOTOWOŚCI blokada iskry bez zatrzasku. Ochrona wyłącznie programowa — firmware działa, bo 3,3 V jest w regulacji |
| **VDD5 5,20–5,45 V** (przepięcie) | — | PMIC sprzętowo | ENDRV niski — zapłon odcięty; DTC-PWR-08b |
| **3,3 V 3,17–3,43 V** | procesor, W25Q128, AIS2IH, KP464 | ADC (DTC-PWR-09 poza 3,15–3,45 V) | — |
| **3,3 V < 3,00–3,17 V** | — | PMIC sprzętowo | RESET: NRES i ENDRV niskie |
| **3,3 V > 3,43–3,60 V** | — | PMIC sprzętowo | ENDRV niski |
| **VSOUT1 4,50–5,50 V** | czujniki w wiązce, odczyt stosunkowy | ADC PC2 + flagi PMIC | — |
| **VSOUT1 poza 4,50–5,50 V** | — | jw. | DTC-PWR-08a: MVP-A — wartości zastępcze bez limitu obrotów; B/C — K3 |

**Wnioski dla schematu:**
- **Sterowanie bramki tyrystora wymiarowane przy VDD5 = 4,50 V**, nie 5,0 V — impuls ≥ 2 × IGT maks. w −40 °C musi być spełniony przy dolnej granicy pracy (`produkt.md` 3.2).
- **Komparator kill switcha:** w arkuszu kwalifikacji (pole 7) — praca od 4,5 V i stan wyjścia przy zasilaniu poniżej minimum. Między 4,5 V a jego minimum zezwolenie bramki AND nie jest gwarantowane — ochrona przez DTC-PWR-08b i drugą ścieżkę kill.
- **Próg tranzystorowy kill switcha** (zwarcie uzwojenia wzbudzającego): najniższe napięcie zasilania, przy którym klucz jeszcze zwiera — do sprawdzenia przy schemacie; ścieżka musi działać w całym zakresie VDD5 z tej tabeli.
- **Szacunek ~5,2 V** na akumulatorze dla progu VDD5 — do potwierdzenia pomiarem na prototypie (T-PWR-008a, przemiatanie napięcia akumulatora).

##### Nadzór odniesienia ADC (O-025, decyzje Pawła 9.11.2026)

Sprzęt: `produkt.md` 5.1. VREF+ = VDDA (VDD3/5 przez filtr LC).

- **Korekcja:** VREFINT w każdej sekwencji skanowania: VREF+ = 3,0 V × VREFINT_CAL / VREFINT_DATA; tym VREF+ przeliczane są wszystkie pomiary bezwzględne. Pomiary stosunkowe (czujniki na VSOUT1, NTC na płytce) korekcji nie potrzebują.
- **Kontrola krzyżowa co 100 ms:** VMON_BG PMIC (2,5 V ±2 %, multiplekser PMIC A.8, pin PD9) daje VREF+ drugą drogą. **Rozbieżność > 5 % przez 1 s → DTC-SYS-17** (decyzja Pawła 9.11.2026). Najgorszy przypadek tolerancji: VMON_BG ±2 % + VREFINT ±0,6 % (Z24) + offset ADC i ustalanie ±0,3 % ≈ 2,9 %; błąd wzmocnienia ADC się znosi, bo oba odniesienia mierzy ten sam przetwornik.
- **Druga droga pomiaru szyn** (VDD5/2, VSOUT1/4, VBATP/10 z multipleksera PMIC) służy do rozstrzygnięcia, czy przy DTC-PWR-08a/08b uszkodzona jest szyna, czy dzielnik — bez własnego progu.
- **Multiplekser PMIC:** przełączanie od wysokich napięć do niskich (karta 5.4.9.1), czas ustalania przed próbką, czas próbkowania ADC dopasowany do rezystancji wyjścia (3–15 kΩ dla VMON_BG, do 200 kΩ dla VBATP). Pin DIAG_OUT wspólny z multiplekserem cyfrowym — podział czasowy.
- **Próbki poza chwilą wyładowania CDI** — chwila iskry jest znana z HRTIM.
- **Zadziałanie bez usterki:** skrajne temperatury, stan przejściowy po przełączeniu multipleksera, za krótki czas próbkowania, zakłócenie od iskry. Przeciwdziała filtr 1 s, czas ustalania i próbkowanie poza iskrą. **Test negatywny:** −40…+85 °C i praca do 10 000 obr/min — brak DTC-SYS-17.

##### Decyzja — niezgodność wersji protokołu (2026-09-20)

**Przyjęte: każda niezgodność wersji wygasza dane na HMI.** Wyświetlacz pokazuje wyłącznie komunikat o niezgodności wraz z obiema wersjami; żadna wartość pomiarowa się nie pojawia.

Rozważany był podział na niezgodność `major` (dane wygaszone) i `minor` (dane pokazywane z ostrzeżeniem). **Odrzucony na rzecz jednej reguły.** Uzasadnienie wyboru: jedna ścieżka w kodzie i jeden przypadek testowy zamiast dwóch, brak klasy błędów polegających na złej ocenie, które pole jeszcze wolno zinterpretować. Przy wskazaniach, od których zależy prowadzenie motocykla, brak wskazania jest jednoznaczny, a wskazanie możliwie fałszywe — nie.

**Koszt tej decyzji i jak go usuwamy.** Skutkiem ubocznym jest to, że aktualizacja samego ECU zostawia kierowcę bez wskazań do czasu aktualizacji HMI. **Rozwiązanie przenoszone do punktu H (bootloader): pakiet aktualizacyjny zawiera obrazy firmware ECU i HMI razem, a aktualizacja jest jedną transakcją** — ECU jest nadrzędne na magistrali i potrafi przeprogramować HMI (SYS-COM-001a), więc rozdzielenie tych dwóch aktualizacji nie jest nikomu potrzebne. Przy takim pakiecie niezgodność wersji przestaje występować w normalnej eksploatacji i zostaje wyłącznie jako zabezpieczenie na wypadek podmiany jednego z modułów.

##### Decyzja — kolejność diagnozowania przy awarii szyny 5 V (2026-09-20)

**Przyjęte: przy jednoczesnym wystąpieniu DTC-PWR-08 i DTC-IGN-01 firmware zapisuje obie usterki, ale jako przyczynę zatrzasku podaje awarię zasilania.**

Powód wynika z topologii, nie z preferencji: MAX9926 pracuje na szynie 5 V, więc jej awaria zabiera sygnał obrotów i silnik gaśnie przez DTC-IGN-01 (K4, zatrzask). Bez reguły pierwszeństwa w logu zostałby „brak sygnału obrotów", co poprowadziłoby diagnostykę do cewki VR i okablowania czujnika — czyli w miejsce, gdzie nic nie jest uszkodzone.

**Zasada ogólna:** gdy jedna usterka jest fizyczną przyczyną drugiej, macierz wskazuje przyczynę źródłową jako powód przejścia w stan awarii. Pozostałe zapisywane są jako towarzyszące. Druga para tego rodzaju to DTC-PWR-10 i usterki odczytu czujników.

##### Odrzucone — MAX9926 poza przełącznikiem obciążenia (2026-09-20) — *nieaktualne od 1.11.2026: przełącznik zastąpiony PMIC, MAX9926 na VDD5, które w uśpieniu jest wyłączone razem z PMIC*

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
| *zdarzenie, nie kod usterki* | Kill switch naciśnięty | napięcie w oknie środkowym | 50 ms | — | Normalne gaszenie silnika, **bez zatrzasku**, wpis w logu jako zdarzenie (dawny DTC-SAF-01a, zmiana 25.11.2026) |
| DTC-SAF-02 | Reset watchdoga | rejestr przyczyny resetu w STM32G474 (IWDG, WWDG) **albo reset z PMIC przy ostatnim zapisanym WD_FAIL_CNT ≥ 5** (B.4) | natychmiast | **K4** | Zatrzask + zapis migawki (B.2.5.3) + inkrementacja licznika |
| DTC-SAF-03 | Trzeci reset watchdoga | licznik ≥ 3, zerowany po 60 s bezawaryjnej pracy silnika (ECU-SAF-006) | — | **K4** | Stan AWARIA trwały, koniec prób startu, kasowanie wyłącznie aplikacją desktop |
| DTC-SAF-04 | Zapaść napięcia (brown-out) | **reset nieplanowany:** zasilenie lub NRES z PMIC przy ustawionym znaczniku „ECU pracuje” (B.4). **Sama flaga BOR nie wystarcza** — ustawia się przy każdym włączeniu zasilania (poprawka 4.11.2026) | natychmiast | **K4** | Zatrzask + zapis migawki |
| DTC-SAF-05 | **Potwierdzona wywrotka** | kąt przechyłu **> 65°** z AIS2IH, **ważny tylko przy 0,8–1,2 g** (ECU-SAF-005) | **3 s nieprzerwanie; kąt nieważny zeruje licznik** | **K4** | Odcięcie + zatrzask |
| **DTC-SAF-06** | **Jedna ścieżka odcięcia kill switcha nie zadziałała** | przy przejściu w STOP: napięcie uzwojenia wzbudzającego nie zanikło **albo** linia wyzwalania tyrystora nie jest zablokowana (odczyt zwrotny) | 1 zdarzenie | **K1** | Ostrzeżenie „KILL SWITCH — USTERKA JEDNEJ ŚCIEŻKI”; kolejny start dozwolony — druga ścieżka działa (ECU-SAF-021) |
| **DTC-SAF-07** | **Kill switch: poziom poniżej RUN** — zwarcie przewodu do masy albo przerwa podciągnięcia w ECU | ADC poniżej dolnej granicy poziomu RUN (wartość z Fazy 4) | 50 ms | **K1** | **Bez odcięcia** (decyzja Pawła 1.11.2026). Ostrzeżenie „KILL SWITCH NIE DZIAŁA — GAŚ SPRZĘGŁEM” na HMI do usunięcia usterki; zapis w logu |
| **DTC-SAF-08** | **Kill switch: niezgodność odczytu ADC z wyjściami układów progowych** | stan z ADC inny niż stan komparatora albo progu tranzystorowego (odczyt zwrotny) | 50 ms | **K1** | Ostrzeżenie i zapis w logu; ścieżki sprzętowe działają niezależnie |
| DTC-SYS-02 | Błędna suma kontrolna firmware | autotest pełny przy starcie | — | — | **Brak startu**, komunikat, wejście w tryb bootloadera |
| DTC-SYS-03a | **Błędna suma kontrolna map sterowania** (zapłon, wtrysk, korekty, progi wentylatora, próg ogranicznika) | autotest pełny przy starcie | — | — | **Blokada startu silnika** + komunikat „MAPY USZKODZONE — WGRAJ PONOWNIE" |
| DTC-SYS-03b | **Błędna suma kontrolna konfiguracji użytkownika** (obwód koła, jednostki, akumulator, profil map; wygląd HMI — DTC-HMI-04) | autotest pełny przy starcie | — | **K1** | Podstawienie wartości domyślnych + ostrzeżenie. **Silnik pracuje normalnie** |
| **DTC-SYS-03c** | **Błędna suma kontrolna profilu granic** (od 25.11.2026, O-021) | autotest pełny przy starcie | — | — | **Blokada startu silnika** + komunikat „KALIBRACJA USZKODZONA — WGRAJ PONOWNIE” (D.1) |
| DTC-SYS-04 | Błąd testu RAM | autotest pełny przy starcie | — | — | Brak startu, komunikat |
| DTC-SYS-05 | Brak komunikacji z pamięcią W25Q128 | 3 nieudane odczyty SPI | 3 próby | **K1** | Logowanie i czarna skrzynka nieczynne, silnik pracuje |
| DTC-SYS-06 | Błąd zapisu do pamięci | weryfikacja odczytem po zapisie | 3 próby na różnych sektorach | **K1** | Po wyczerpaniu prób jak DTC-SYS-05 |
| DTC-SYS-07 | Brak wolnych sektorów lub zużycie pamięci | licznik cykli kasowania sektora | — | **K0** | Nadpisywanie najstarszych wpisów, zapis zdarzenia |
| DTC-SYS-08 | Zegar utracił czas | domena podtrzymywana nieważna **po odłączeniu akumulatora** dłuższym, niż wytrzyma superkondensator | — | **K0** | Znaczniki czasu względne od startu, **oznaczone w logu jako niepewne**; czas ustawia aplikacja desktop |
| DTC-SYS-10 | Niespójny licznik motogodzin | suma kontrolna rekordu | — | **K1** | Odtworzenie z ostatniego spójnego zapisu, zdarzenie w logu |
| **DTC-SYS-11** | **Naruszenie ochrony pamięci (MPU)** | wyjątek MemManage — zapis do chronionego obszaru, np. rejestrów HRTIM spoza modułu zapłonu (ECU-SAF-023) | natychmiast | **K4** | Reset z zapisem migawki i przyczyny, jak DTC-SAF-02; wlicza się do licznika resetów (ECU-SAF-006) |
| **DTC-SYS-12** | **Utrata domeny podtrzymywanej przy podłączonym akumulatorze** (od 4.11.2026) | domena nieważna przy starcie bez flagi Pwon (B.4) | — | **K1** | Log, ostrzeżenie; czas niepewny jak DTC-SYS-08. Wskazuje usterkę stałego stabilizatora, diody lub superkondensatora |
| **DTC-SYS-13** | Temperatura wnętrza ECU — próg T1 | **> 95 °C** (NTC lub czujnik MCU) | 5 s | **K1** | Ostrzeżenie na HMI (ECU-SAF-020) |
| **DTC-SYS-14** | Temperatura wnętrza ECU — próg T2 | **> 105 °C** | 5 s | **K1** | Wyłączenie świateł i wyjść aux; wentylator chłodnicy i rozrusznik pozostają (ECU-SAF-020) |
| **DTC-SYS-15** | Temperatura wnętrza ECU — próg T3 | **> 120 °C na dwóch niezależnych czujnikach naraz** (NTC i czujnik MCU) | 10 s | **K4** | Zgaszenie silnika, zatrzask; odblokowanie po ostygnięciu poniżej 95 °C (ECU-SAF-020, zatrzymanie nr 9 z listy B.1.1) |
| **DTC-SYS-16** | Czujnik temperatury ECU niewiarygodny | odczyt poza zakresem fizycznym (przerwa/zwarcie NTC) albo rozbieżność NTC–MCU > 20 °C | 1 s | **K1** | Kod usterki; **czujnik nie może uczestniczyć w T3** — zgaszenie termiczne nieczynne do usunięcia usterki |
| **DTC-SYS-17** | **Niezgodność odniesień ADC** (od 9.11.2026, O-025) | VREF+ z VREFINT różni się od VREF+ z VMON_BG PMIC o **> 5 %** | 1 s | **K1** | Ostrzeżenie; wstrzymane diagnostyki oparte na wartościach bezwzględnych (pomiar kondensatora ECU-IGN-028/029, spójność drabinki kill B.2.5.1); wartości bezwzględne w logu oznaczone jako niepewne; pomiary stosunkowe bez zmian; **na silnik bez wpływu** |
| **DTC-SYS-18** | **Konfiguracja sprzętowa niezgodna z płytką** (od 25.11.2026, O-021) | kod wariantu z rezystora (PB2) różny od wariantu w profilu granic albo poza oknami | przy starcie | — | **Blokada startu silnika** + komunikat z oboma wariantami (D.1) |

**Zakres autotestu pełnego:** DTC-SYS-02, 03a, 03b, 04. Wykonywany po podłączeniu akumulatora i po aktualizacji firmware.

**Zakres autotestu skróconego przy zwykłym wybudzeniu — domyka ECU-PWR-003a:** suma kontrolna map sterowania (DTC-SYS-03a) **oraz** odczyt identyfikatora pamięci W25Q128 (DTC-SYS-05). Pominięte: suma kontrolna firmware i test RAM. Uzasadnienie: firmware i RAM nie zmieniają się między uśpieniem a wybudzeniem — od ostatniego pełnego testu nikt ich nie dotykał. Mapy natomiast mogły zostać nadpisane przez aplikację desktop tuż przed uśpieniem, a to jedyna rzecz w tym zestawie, która potrafi się zmienić bez restartu. Suma kontrolna map to pojedyncze przejście przez kilkadziesiąt kilobajtów — mieści się w budżecie 200 ms (ECU-PWR-003) z zapasem.

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
        R_ser (w module przycisku)
         │
         ├── styk kill switcha ──┐   (zwarty = RUN)
         │                       │
        R_par (równolegle)       │
         │                       │
         └───────────────────────┴──► drugi przewód ──► masa ECU (pin złącza)
```

**Od 1.11.2026 (decyzja Pawła, O-015): obwód dwuprzewodowy.** Masa przycisku wraca osobnym przewodem do masy ECU, przycisk jest odizolowany od ramy. Przesunięcie masy ramy przy kręceniu rozrusznikiem nie zmienia poziomów, więc nie powoduje fałszywego odcięcia w trakcie rozruchu.

| Stan | Droga do masy | Napięcie na wejściu | Bramkowanie |
|---|---|---|---|
| **RUN** — styk zwarty | R_ser | **dolne** | przepuszcza |
| **STOP** — styk rozwarty | R_ser + R_par | **środkowe** | odcina |
| **Przerwa lub rozłączona wtyczka** | brak | **górne (pełne podciągnięcie)** | odcina |

**Bramkowanie sprzętowe wymaga jednego komparatora, nie dwóch.** Próg ustawiony pomiędzy poziomem RUN a poziomem STOP odcina zarówno przy naciśnięciu, jak i przy przerwie — obie sytuacje leżą powyżej progu. Rozróżnieniem zajmuje się mikrokontroler, czytając ten sam punkt przetwornikiem, i robi to wyłącznie na potrzeby logu i komunikatu. **Funkcja bezpieczeństwa nie zależy od tego odczytu.**

**Bilans pinów bez zmian.** Wejście kill switcha już istnieje; wymaga jedynie przypisania do pinu z dostępem do przetwornika ADC. Wyjście komparatora prowadzi do wejść EN driverów po stronie płytki i nie zajmuje pinu złącza.

**Zachowanie przy zwykłym przycisku bez rezystorów w wiązce** (ktoś podłączy fabryczny kill switch): styk zwarty daje poziom dolny, czyli RUN — poprawnie; styk rozwarty daje poziom górny, czyli odcięcie — również poprawnie, ale zgłoszone jako przerwa w przewodzie. **Degradacja jest bezpieczna**: funkcja działa, myli się wyłącznie komunikat. ⚠️ **Korekta 1.11.2026:** to zachowanie zakłada przycisk **normalnie zamknięty**. Typowy fabryczny przycisk enduro jest **normalnie otwarty** (wciśnięcie zwiera do masy). Taki przycisk bez naszej wiązki daje odcięcie w spoczynku — silnik pracuje tylko przy wciśniętym przycisku. Bezpieczne, ale nieużywalne. Typ przycisku Bety do sprawdzenia (`measurements/pomiar-wzbudzajacego.md`, krok 2). Wymóg zastosowania wiązki z rezystorami trafia do wymagań instalacyjnych (rozdz. 6.7 dok. procesu).

**Analiza pojedynczych uszkodzeń (O-015, 1.11.2026):**

| Element | Uszkodzenie | Skutek dla odcięcia | Wykrycie | Ocena |
|---|---|---|---|---|
| Przewód / wtyczka | przerwa | odcięcie (poziom górny) | DTC-SAF-01 | bezpieczne |
| Przewód | zwarcie do +12 V | odcięcie (poziom górny) | ADC poza zakresem | bezpieczne; wejście z rezystorem szeregowym i ograniczeniem napięcia |
| **Przewód** | **zwarcie do masy** | **kill nie działa — także dla firmware**, bo przycisk nie zmienia napięcia | DTC-SAF-07 (poziom poniżej RUN) | **ryzyko zaakceptowane — decyzja Pawła: kod usterki i ostrzeżenie, bez odcięcia** |
| **R_pull (w ECU)** | **przerwa** | jw. — napięcie 0 V, czyli RUN | DTC-SAF-07 | jw. |
| R_pull | zwarcie | odcięcie (poziom górny) | ADC | bezpieczne |
| R_ser | przerwa | odcięcie, zgłoszone jako przerwa | DTC-SAF-01 | bezpieczne |
| R_ser | zwarcie | RUN = 0 V, STOP nadal rozróżnialny | DTC-SAF-07 | dostępność; zalane rezystory |
| R_par | przerwa | STOP zgłoszony jako przerwa, odcięcie działa | DTC-SAF-01 | bezpieczne |
| **R_par / styk** | **zwarcie, mostek z wody lub błota** | **STOP przesuwa się do RUN — kill może nie zadziałać** | — | **reguła projektowa:** drabinka niskoomowa (setki Ω, prąd kilku mA) i rezystory zalane w module przycisku — decyzja Pawła |
| Styk | zablokowany rozwarty | silnik nie pracuje | widoczne | bezpieczne |
| **Styk** | **zablokowany zwarty** | **kill nie działa** | elektrycznie niewykrywalne | **ryzyko zaakceptowane** — bez stacyjki kill jest naciskany przy każdym gaszeniu, więc kierowca zauważy przy najbliższym postoju |
| Masa ramy | przesunięcie przy kręceniu rozrusznikiem | fałszywe odcięcie w rozruchu | — | **usunięte obwodem dwuprzewodowym** |
| Komparator / próg tranzystorowy | utknięcie w RUN | druga ścieżka działa | ECU-SAF-021, ECU-SAF-024 | bezpieczne (B.1.3) |
| Wejście ADC procesora | uszkodzenie | tylko diagnostyka; ścieżki sprzętowe działają | ECU-SAF-024 (niezgodność z wyjściami progów) | bezpieczne |
| Szyna VDD5 | zanik | komparator bez zasilania → bramka AND odcina | DTC-PWR-08b | bezpieczne |

**Wspólna przyczyna, która zostaje:** przewód i moduł przycisku — oba progi i ADC czytają ten sam punkt.

**Reguły dla schematu (O-015):** filtr RC na wejściu ze stałą czasową ≤ 1 ms (budżet 10 ms z ECU-SAF-001); histereza komparatora; dzielnik do wejścia ADC (5 V → zakres 3,3 V); rezystor szeregowy i ograniczenie napięcia na wejściu na wypadek zwarcia do +12 V; podciągnięcie z VDD5, nigdy z VSOUT1.

**Do domknięcia w Fazie 4:** wartości R_pull, R_ser i R_par wraz z analizą najgorszego przypadku (tolerancje rezystorów, rezystancja przejścia styku, spadki na złączach i wiązce) oraz dobór komparatora. **Komparatora świadomie nie wskazuję teraz** — zgodnie z zasadą przyjętą 20.09.2026 propozycja komponentu powstaje dopiero po sprawdzeniu karty katalogowej i dostępności w TME.

**Rozważone i odrzucone: wykorzystanie komparatora wbudowanego w STM32G474.** Układ ma sprzętowe komparatory z bezpośrednim połączeniem do HRTIM, więc kusi, żeby nie dokładać elementu. Odrzucone, bo komparator wewnętrzny jest konfigurowany przez firmware, a błąd firmware może go przekonfigurować lub wyłączyć — to dokładnie ta zależność, którą audyt zakwestionował w pozycji F-004. Zewnętrzny komparator działa od chwili podania zasilania i firmware nie ma do niego dostępu.

---

##### B.2.5.2 Uszkodzone mapy — blokada startu, z rozdzieleniem na dwa zakresy (decyzja 2026-09-22)

**Przyjęte: uszkodzenie map sterowania blokuje start silnika.** Odrzucone warianty: start na mapach awaryjnych zaszytych w firmware oraz start na drugiej kopii map. Uzasadnienie wyboru: praca silnika na czymkolwiek niezweryfikowanym to ryzyko po stronie silnika, a nie po stronie wygody.

**Doprecyzowanie wprowadzone przy zapisie decyzji — rozdzielenie DTC-SYS-03 na dwie pozycje.** Pierwotny zapis obejmował jedną sumą kontrolną „mapy lub konfigurację", co oznaczałoby, że uszkodzony bajt w ustawieniu jednostek prędkości albo w wyglądzie ekranu HMI unieruchamia motocykl. To nie jest to, co decyzja miała osiągnąć.

| Zakres | Zawartość | Reakcja na uszkodzenie |
|---|---|---|
| **Mapy sterowania** (DTC-SYS-03a) | **3 profile** mapy zapłonu (ECU-IGN-039), mapa wtrysku, korekty (temperatura, ciśnienie, napięcie), progi wentylatora, próg i histereza ogranicznika obrotów | **Blokada startu** |
| **Konfiguracja użytkownika** (DTC-SYS-03b) | Obwód koła (domyślnie 2180 mm — 90/90-21), jednostki, **typ i pojemność akumulatora, wybrany profil map** (od 16.11.2026), (wygląd ekranów i krzywa jasności — od 25.11.2026 w pamięci HMI, HMI-UI-013) | **Wartości domyślne + ostrzeżenie, silnik pracuje** |

Kryterium podziału: **czy wartość wpływa na to, co ECU robi z silnikiem.** Progi wentylatora i ogranicznika są po stronie map mimo że wyglądają na ustawienia użytkownika, bo ich uszkodzenie może doprowadzić do przegrzania lub przekroczenia obrotów.

**Ryzyko przyjęte świadomie:** uszkodzenie map unieruchamia motocykl tam, gdzie nie ma laptopa. Ograniczają je dwie rzeczy już obecne w projekcie — zapis transakcyjny map (APP-COM-006), który eliminuje przerwaną aktualizację jako przyczynę, oraz weryfikacja odczytem po zapisie (DTC-SYS-06). Pozostaje awaria samej pamięci, a przy uszkodzonej pamięci jazda na zawartości tej pamięci nie jest bezpieczniejsza od postoju.

---

##### B.2.5.3 Migawka stanu przy resecie watchdoga (decyzja 2026-09-22)

**Przyjęte: licznik resetów w pamięci nieulotnej, a wraz z nim zapis kontekstu — co się działo w chwili, gdy watchdog musiał zadziałać.** Sam licznik mówi, że coś zawiodło; nie mówi co, a to jest informacja o największej wartości diagnostycznej w całym systemie.

**Mechanizm dwustopniowy — rozwiązuje problem zużycia pamięci Flash:**

| Etap | Gdzie | Kiedy zapis |
|---|---|---|
| **Ślad bieżący** | rejestry domeny podtrzymywanej w STM32 (stały stabilizator, przy całkowitym zaniku zasilania superkondensator — od 4.11.2026) | **w trakcie pracy**, przy każdym punkcie kontrolnym — zero zapisów do Flash |
| **Migawka** | W25Q128 | **raz, po resecie**, w trakcie startu — ślad bieżący przepisywany do pamięci trwałej razem z licznikiem |

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
| **G2 — ochrona termiczna lub elektryczna** | Nic — dane są poprawne, problem jest po stronie sprzętu | **Limit obrotów 5000 obr/min, mapy bez zmian.** Cel: zdjęcie obciążenia z przegrzanego lub uszkodzonego elementu | DTC-INJ-03, DTC-OUT-01, DTC-INJ-04 (DTC-OUT-02 od 16.11.2026 tylko ostrzeżenie — ECU-DIA-005). *(DTC-SYS-01 — przegrzanie ECU — wycofany 25.10.2026, zastąpiony przez DTC-SYS-13…15, ECU-SAF-020)* |
| **G3 — utrata sygnału obciążenia** | Położenie przepustnicy albo zasilanie czujników VSOUT1 — **tylko warianty B/C**. **W MVP-A od 1.11.2026 G3 nie występuje:** VSOUT1 poza zakresem obsługują wartości zastępcze czujników (ECU-PWR-008a) | **Osobna strategia (B.3.2)** — mapa awaryjna + limit 3500 obr/min | DTC-SEN-04, DTC-PWR-08a (B/C) |

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
| Potwierdzenie na HMI | Przytrzymanie przycisku potwierdzenia **≥ 1 s**, rozpoczęte po wyświetleniu komunikatu o przyczynie; ramka niesie identyfikator wyświetlonego komunikatu (J, HMI-UI-010, 9.11.2026) | Czytelna informacja o powodzie zatrzasku; przypadkowe naciśnięcie albo potwierdzenie starego ekranu nie odblokowuje |

**Warunek wspólny, wymagany dla obu dróg (ECU-SAF-029, decyzja Pawła 4.11.2026):** wał zatrzymany = **≥ 2 s bez zbocza z czujnika wału**, spełnione w chwili przełączenia STOP→RUN albo potwierdzenia na HMI. Dotyczy A i B/C, niezależnie od typu czujnika (VR albo Hall, ECU-SEN-002). **Bez drugiego, niezależnego kanału** — ryzyko w rozdz. 9 `otwarte.md`.

**Uzbrojenie nie opiera się na domniemanym zerze.** Brak zboczy nie dowodzi, że wał stoi (uszkodzony czujnik; bardzo wolny obrót, przy którym VR nie daje sygnału). Dlatego po odblokowaniu zapłon i wtrysk wracają **dopiero po pełnej, świeżej synchronizacji — jak przy zimnym starcie** (C.1, ECU-IGN-019). Przy martwym czujniku po odblokowaniu iskry po prostu nie ma.

**Odblokowanie nie sprawdza, czy przyczyna ustąpiła.** Jeśli trwa, jej detektor zatrzaśnie K4 ponownie. Inaczej uszkodzony detektor (np. akcelerometr) unieruchomiłby motocykl na stałe. Wyjątki: DTC-SYS-15 — odblokowanie dopiero po ostygnięciu poniżej 95 °C (ECU-SAF-020); DTC-SAF-03 — kasowanie wyłącznie aplikacją desktop (ECU-SAF-006).

**Trwałość zatrzasku (ECU-SAF-028, decyzja Pawła 4.11.2026):**
- Zapis zatrzasku (flaga, przyczyna, suma kontrolna) w **rejestrach domeny podtrzymywanej**, natychmiast przy wejściu w K4 — bez Flash. Zerowany przy odblokowaniu. **Przeżywa każdy reset procesora.**
- **Zapis nieczytelny (zła suma kontrolna) = zatrzask aktywny.**
- Zapisu przed uśpieniem nie trzeba: ECU w AWARII nie usypia (rozdz. 9 `otwarte.md`).
- **Odłączenie akumulatora kończy zatrzask:** flaga Pwon z TJA1043 przy starcie kasuje go celowo, z wpisem do logu. Bez tego superkondensator trzymałby zatrzask jeszcze kilka dni i wynik zależałby od czasu odłączenia. Przyczyna zostaje w logu usterek (W25Q128).

**Rozpoznanie resetu przy starcie — poprawka 4.11.2026.** Flaga BOR procesora **ustawia się przy każdym włączeniu zasilania** (STM32G4: zaniku zasilania i zapaści nie da się rozróżnić flagami — potwierdzenie ST). PMIC wyłącza 3,3 V w uśpieniu, więc wykrywanie zapaści samą flagą BOR (dawne DTC-SAF-04) dawałoby K4 po każdym wybudzeniu. Rozróżnienie daje znacznik **„ECU pracuje”** w domenie podtrzymywanej: ustawiany po starcie, kasowany jako ostatnia czynność przed rozkazem uśpienia i przed planowym resetem programowym.

| Warunek przy starcie (w tej kolejności) | Interpretacja | Reakcja |
|---|---|---|
| Pwon z TJA1043, znacznik „ECU pracuje” ustawiony, w śladzie bieżącym stan ROZRUCH lub PRACA | Zasilanie zniknęło całkowicie przy pracującym silniku (wtyczka, bezpiecznik, klema); domenę utrzymał superkondensator | DTC-SAF-04, migawka ze śladu bieżącego, K4 |
| Pwon w pozostałych przypadkach | Akumulator odłączony, także w AWARII | Zatrzask skasowany, start normalny; przy domenie nieważnej DTC-SYS-08 |
| Flaga IWDG lub WWDG | Reset watchdoga procesora | DTC-SAF-02, K4 |
| Reset programowy, w domenie zapisana przyczyna MPU | Naruszenie ochrony pamięci | DTC-SYS-11, K4 |
| Zasilenie lub NRES z PMIC, **znacznik „ECU pracuje” ustawiony** | ECU było obudzone i straciło zasilanie albo PMIC wymusił reset | Ostatni zapisany licznik WD_FAIL_CNT PMIC ≥ 5 → reset watchdoga PMIC (DTC-SAF-02); inaczej zapaść napięcia (DTC-SAF-04). K4 |
| Znacznik skasowany | Wybudzenie z uśpienia albo planowy reset | Start normalny |
| Domena nieważna bez Pwon | Usterka zasilania domeny podtrzymywanej (stabilizator, dioda, superkondensator) albo uszkodzenie domeny (errata 2.2.5) | Start normalny, DTC-SYS-12 |

Uszkodzenie domeny po spadku napięcia bez resetu (errata 2.2.5, I.1) wykrywa suma kontrolna; w trakcie pracy zapis nieczytelny oznacza zatrzask aktywny.

**Konsekwencja testowa:** wymaganie ECU-SAF-003 weryfikuje się **dwoma wariantami testu** — T-SAF-003a (odblokowanie kill switchem) i T-SAF-003b (odblokowanie z HMI). To dwie różne ścieżki w kodzie i obie muszą przechodzić przez ten sam warunek zatrzymania wału.

**Zachowanie licznika resetów — doprecyzowane 2026-09-22:** licznik i migawka stanu w pamięci nieulotnej W25Q128, mechanizm dwustopniowy opisany w B.2.5.3. Licznik zerowany po 60 s bezawaryjnej pracy silnika (ECU-SAF-006); po trzecim resecie stan AWARIA trwały, kasowany wyłącznie aplikacją desktop.

*Do doprecyzowania: treść komunikatów (punkt J).*

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

> **Rozstrzygnięte 12.10.2026 (O-020, ECU-SAF-011):** w MVP-A bez czujnika przepustnicy zmiany przy pracującym silniku trafiają tylko do bufora; aktywacja przy rozbrojonym silniku albo w trybie stanowiskowym. Fizyczne zezwolenie trybu stanowiskowego — D.2 (25.11.2026). Blokada 5000 obr/min + 60 % dotyczy wariantów z TPS.

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

#### C.1.2 Model błędu prognozy kąta (przebudowa 11.11.2026, odtworzona 25.11.2026, O-008)

**Wycofane:** tabela z 0,20° / 0,05° / 0,02° i „pięciokrotnym zapasem powyżej 3000 obr/min”. Wartości były bez równań, nieodtwarzalne i sugerowały zapas tam, gdzie wiążący jest przypadek nagłej zmiany przyspieszenia przy małym wyprzedzeniu.

**Mechanizm.** Iskra pada po czasie t = Δθ / ω_est od krawędzi natarcia, gdzie **Δθ = 30° − wyprzedzenie**. Błąd kąta ≈ Δθ × względny błąd estymaty prędkości na odcinku Δθ. Estymata E1 (C.1.4) jest dokładna przy stałym przyspieszeniu — błąd powstaje przy **zmianie przyspieszenia** między pomiarem a iskrą. Wielkość wejściowa: **zmiana prędkości na obrót w %** = 60·a / N² (a — przyspieszenie w obr/min/s, N — obroty). **Nie zależy od obrotów** — model daje ten sam błąd przy 1500 i 8000 obr/min.

**Model:** `scripts/model_kata.py` — całkowanie czasu po kącie wału dla trzech profili zmiany prędkości (liniowo w kącie, zmiana skokowa w najgorszej z 24 faz obrotu, 6 kolejnych iskier). Największa zmiana prędkości na obrót, przy której prognoza mieści się w budżecie **0,7° za wcześnie / 1,7° za późno** (podział budżetu ECU-IGN-022 — C.1.9):

| Wyprzedzenie (Δθ) | Hamowanie od stałej prędkości | Odwrócenie: przyspieszanie → hamowanie | Przyspieszanie od stałej prędkości |
|---|---|---|---|
| 2° (28°) | **4,6 %** | **2,5 %** | **11,6 %** |
| 15° (15°) | 8,8 % | 5,1 % | 23,1 % |

Hamowanie i odwrócenie dają iskrę za wcześnie, przyspieszanie — za późno. **Przykład:** 4 % na obrót przy 3000 obr/min to 120 obr/min w ciągu jednego obrotu (20 ms), czyli 6000 obr/min/s; przy 1500 obr/min — 1500 obr/min/s.

**Wnioski:**
1. **Wiążące są małe wyprzedzenie (duże Δθ) i nagłe odwrócenie przyspieszenia** — przyspieszanie, a potem lądowanie albo szarpnięcie sprzęgłem. Nie zakres wysokich obrotów.
2. **Korekta przyspieszenia jest konieczna:** bez niej (E0) obwiednia przy 2° to 2,3 % hamowania i 6,1 % przyspieszania — mniej więcej dwa razy węższa.
3. **Warunek ECU-IGN-022: zmiana < 4 % na obrót i odwrócenie ≤ 2,5 % na obrót** (decyzje Pawła 11.11 i 25.11.2026). Poza warunkiem granica 100 % zapłonów nie jest gwarantowana — dlatego rozkład zmian prędkości w jeździe zapisuje czarna skrzynka (ECU-LOG-009); w Fazie 8 rozstrzyga on, czy warunek obejmuje rzeczywistą jazdę.
4. Ta sama metoda — prognoza z czasu poprzedniego obrotu — jest w nocie aplikacyjnej NXP AN4006 dla CDI z jednym wypustem, tam bez korekty przyspieszenia.

**Odtworzenie 25.11.2026:** model z 11.11.2026 przepadł razem ze środowiskiem roboczym; obecny skrypt napisano od nowa. Wobec wartości z 11.11 (4,4 / 2,9 / 12,2 %): hamowanie +0,2, odwrócenie −0,4, przyspieszanie −0,6 punktu procentowego. Próg odwrócenia w ECU-IGN-022 obniżony z 3 % do **2,5 %** (decyzja Pawła 25.11.2026) — przy 3 % nowy model daje iskrę 0,83° za wcześnie.

**Ograniczenia modelu (Z26):** profile liniowe w kącie ze skokową zmianą; bez tętnienia prędkości w obrębie obrotu (pomiar wypustu w tej samej fazie znosi jego część systematyczną, C.1.4); błąd statyczny liczony osobno (C.1.9). Potwierdzenie: T-IGN-022 na symulatorze i rozkład z ECU-LOG-009.

#### C.1.3 Ciągły model kąta wału

Firmware utrzymuje **ciągły model położenia wału**, a nie wyłącznie reakcję na zbocza. Model jest korygowany przy każdej ważnej krawędzi natarcia i ekstrapolowany między nimi.

Model jest konieczny z dwóch powodów:

| Powód | Wyjaśnienie |
|---|---|
| **Bramkowanie kątowe wejścia** | Bez wiedzy, gdzie jest wał, nie da się stwierdzić, że zbocze przyszło w złym miejscu (C.1.6) |

**Rozdzielenie dokładności — kluczowe dla zrozumienia całości:**

| Zdarzenie | Źródło wyznaczenia | Wymagana dokładność | Skutek błędu |
|---|---|---|---|
| **Iskra** | krawędź natarcia + wyliczona zwłoka | **1,0° (ECU-IGN-002)** | moc, detonacja, uszkodzenie silnika |

W AC-CDI nie ma ładowania cewki sterowanego przez firmware (25.10.2026) — model kąta służy bramkowaniu wejścia i restartowi w ruchu.

#### C.1.4 Estymata prędkości i korekta przyspieszenia

**Baza: interwał między krawędziami wypustu z poprzedniego obrotu.**

Wypust zajmuje te same 30° wału w każdym obrocie, więc czas jego przejścia daje prędkość chwilową **w dokładnie tej fazie wału, w której nastąpi iskra**. W jednocylindrowym dwusuwie prędkość w obrębie obrotu faluje — sprężanie hamuje wał, rozprężanie przyspiesza — więc średnia z pełnego obrotu jest wobec okolic GMP **systematycznie przesunięta**. Pomiar w tej samej fazie znosi ten błąd, bo powtarza się w tych samych warunkach.

**Korekta: przyspieszenie z dwóch kolejnych okresów obrotu.** Estymata z poprzedniego obrotu jest stara o jeden obrót; korekta liniowa redukuje błąd starzenia do drugiego rzędu. **Bez niej dopuszczalna zmiana prędkości na obrót jest mniej więcej dwa razy mniejsza** (C.1.2).

**Odrzucone: średnia z pełnego obrotu jako baza.** Prostsze i niezależne od kalibracji długości wypustu, ale obarczone błędem **systematycznym** od tętnienia prędkości — a błąd systematyczny nie uśrednia się i wchodzi wprost w kąt zapłonu.

#### C.1.5 Ładowanie kondensatora CDI (przebudowa 25.10.2026)

W AC-CDI kondensator zapłonowy ładuje się **biernie** z uzwojenia wzbudzającego — firmware nie steruje ładowaniem. Dawna tabela czasów ładowania cewki indukcyjnej przestała dotyczyć (VBG08H-E usunięty 15.10.2026).

**Jedyne ograniczenie dla firmware:** iskra może paść tylko wtedy, gdy kondensator jest naładowany. Okno kątowe ładowania wynika z fazy uzwojenia wzbudzającego względem GMP — **założenie Z14**, potwierdzane pomiarem (`measurements/pomiar-wzbudzajacego.md`). Jeśli okno nie obejmie całej mapy wyprzedzenia, mapa zostanie ograniczona do zakresu, w którym kondensator jest naładowany.

#### C.1.6 Bramkowanie kątowe wejścia — odrzucanie fałszywych zboczy (wymaganie Pawła, 2026-10-11)

**Zasada: zbocze, które przyszło w miejscu, w którym wypust nie może wystąpić, jest odrzucane, a nie przetwarzane.**

Instalacja zapłonowa generuje impulsy zdolne udawać krawędź wypustu. Bez bramkowania takie zbocze skorygowałoby model kąta w złym miejscu i przesunęło iskrę w przypadkowy punkt — przy pełnym obciążeniu groźny dla silnika.

| Stan | Zachowanie wejścia |
|---|---|
| Model kąta ważny | Przyjmowane są wyłącznie zbocza w **oknie spodziewanego położenia** krawędzi natarcia. Pozostałe odrzucane bez wpływu na model |
| Zbocze odrzucone | Zliczane; **zapłon przebiega normalnie** na podstawie modelu kąta — nie traci się iskry |
| Brak ważnego zbocza w oknie | Model pracuje dalej przez ograniczony czas; brak kolejnych zboczy prowadzi do DTC-IGN-01 |
| Model nieważny (rozruch, po resecie) | Bramkowanie nieaktywne — nie ma względem czego bramkować. Walidacja opiera się wtedy wyłącznie na długości wypustu |

**Szerokość okna — wartości wstępne; dane ze stanowiska zakłóceń (Faza 6, O-039) i z jazdy (Faza 8):**

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
| **DTC-IGN-02** | Sygnał obrotów niewiarygodny — kryterium spełnione powtarzalnie, **w PRACY** | **K4** | Odcięcie + zatrzask. W ROZRUCHU i GOTOWOŚCI: DTC-IGN-11, K0, powrót do BRAK (C.1.12) |
| **DTC-IGN-03** | Odrzucone zbocze pojedyncze | **K0** | Wyłącznie licznik. Zapłon bez zmian |
| **DTC-IGN-03a** | Podwyższona liczba odrzuceń — **> 5 na 100 obrotów** | **K1** | Ostrzeżenie o jakości sygnału; wskazuje na zakłócenia lub luźny czujnik |

Licznik odrzuceń jest wskaźnikiem jakości instalacji o dużej wartości diagnostycznej przy uruchamianiu i warto go udostępnić w aplikacji desktop.

#### C.1.8 Sekwencja rozruchu

> ⚠️ **Zmienione 25.10.2026 (decyzja Pawła, O-007): w stanie ROZRUCH iskra na krawędzi spływu (GMP), już przy pierwszym przejściu wypustu — ECU-IGN-019.** Powód: prognoza z czasu daje najwięcej błędu w kierunku za wczesnej iskry właśnie przy kopnięciu, kiedy sprężanie hamuje wał — ryzyko odbicia kopniaka. Poniższy tekst opisuje wersję z 11.10 i zostaje jako historia decyzji.

**Iskra od drugiego przejścia wypustu.** Pierwsze przejście służy wyłącznie do pomiaru: krawędź natarcia startuje pomiar, krawędź spływu go kończy, z czego powstaje pierwsza estymata prędkości i model kąta.

Uzasadnienie: kickstarter obraca wał kilkakrotnie w jednym ruchu nogi, więc wypust przechodzi pod czujnikiem wielokrotnie w trakcie tego samego kopnięcia. **Strata pierwszego obrotu nie kosztuje kopnięcia.** W zamian cały układ ma jedną ścieżkę w kodzie zamiast dwóch i żadnego przypadku szczególnego.

**Rozważone i odrzucone: iskra na pierwszym przejściu**, z ładowaniem na krawędzi natarcia i iskrą na krawędzi spływu, czyli w GMP przy zerowym wyprzedzeniu. Działało bez znajomości prędkości, ale wprowadzało drugą, zupełnie inną ścieżkę wyzwalania, używaną wyłącznie przez jeden obrót w całym cyklu życia uruchomienia.

**Przypadek szczególny do obsłużenia:** restart w ruchu, gdy silnik zgasł na biegu, a motocykl jedzie. Model kąta i estymata prędkości są wtedy **nadal ważne**, więc iskra musi pójść natychmiast z mapy, bez przechodzenia przez sekwencję rozruchową.

**Ograniczenie znane:** bardzo słabe lub krótkie kopnięcie dające tylko jeden obrót nie wywoła iskry. Wymaga powtórzenia kopnięcia.

**Przejście z ROZRUCHU na iskrę z prognozy (ECU-IGN-036, decyzja Pawła 11.11.2026):** dopiero przy **> 1000 obr/min** i **zmianie prędkości < 4 % na obrót przez 2 kolejne obroty**; do tego czasu iskra na krawędzi spływu (ECU-IGN-019). Pierwotnie 6 %, obniżone do 4 % dla spójności z warunkiem ECU-IGN-022.

#### C.1.9 Limity wyprzedzenia i budżet od krawędzi do iskry (przebudowa 11.11.2026, odtworzona 25.11.2026, O-006)

**Łańcuch od wypustu do iskry:**

| Ogniwo | Wartość | Uwagi |
|---|---|---|
| Krawędź mechaniczna wypustu | 30° przed GMP | pomiar tarczą (C.1.1) |
| **Zbocze elektryczne VR, θ_el** | **prawdopodobnie 25–27°** | MAX9926 przełącza przy przejściu sygnału przez zero, czyli kilka stopni po krawędzi mechanicznej. Wartość z pomiaru enkoderem (`measurements/pomiar-wzbudzajacego.md` krok 7, O-005) |
| Przechwycenie zbocza (HRTIM, filtr cyfrowy) | stała | w t_op |
| Obliczenie i zapis zwłoki do rejestru | **≤ 10 µs** (ECU-IGN-038) | timer jednokrotny: zapis spóźniony = iskra pominięta i zliczona, nigdy iskra w przypadkowej chwili; kondensator doładowuje się wtedy do progu ogranicznika (ECU-IGN-034) |
| Minimalna zwłoka δ_min | **2°** od zbocza elektrycznego (ECU-IGN-023) | iskra nigdy przed zboczem przy błędzie prognozy |
| Od zbocza do iskry łącznie, t_op | **~5–15 µs** (Z27) | tor wejściowy, impuls bramki, załączenie tyrystora, przebicie — pomiar na stanowisku |

**Największe osiągalne wyprzedzenie: α_max = θ_el − δ_min − ω·t_op.**

| θ_el | 1000 obr/min | 10 000 obr/min (t_op 15 µs = 0,9°) |
|---|---|---|
| 30° (zbocze = krawędź mechaniczna) | 27,9° | 27,1° |
| 27° | 24,9° | 24,1° |
| 26° | 23,9° | 23,1° |

**Stałe 28° jest nieosiągalne** nawet wtedy, gdy zbocze elektryczne pokrywa się z mechanicznym. **Limit geometryczny (ECU-IGN-015) liczony z kalibracji θ_el i obrotów, z twardym ograniczeniem 28°** (decyzja Pawła 11.11.2026). Wyższa wartość z mapy jest obcinana i zapisywana jako zdarzenie. Poprzednia wersja przyjmowała stałe 28° = 30° − 2° bez łańcucha opóźnień.

**Limit termodynamiczny** — bez zmian: niższy, z mapy, ustalany w Fazie 8 z obserwacją detonacji. **Limit geometryczny nie chroni silnika** przed detonacją, tylko przed błędem mapy.

**Budżet błędu kąta ECU-IGN-022 (+1° / −2°, decyzja Pawła 11.11.2026):**

| Składnik | Za wcześnie | Za późno | Warunek |
|---|---|---|---|
| Statyczny: kalibracja θ_el, długość wypustu, kwantyzacja timera | 0,3° | 0,3° | enkoder: θ_el ±0,15°, długość wypustu ±0,1° (ECU-IGN-037) |
| Prognoza (C.1.2) | 0,7° | 1,7° | zmiana < 4 % na obrót, odwrócenie ≤ 2,5 % na obrót |
| **Razem** | **1,0°** | **2,0°** | |

**Reguła przerwania (ECU-IGN-038):** obsługa zbocza wału ma najwyższy priorytet w systemie; zapis rejestru ≤ 10 µs po zboczu w najgorszym przypadku przy jednoczesnej pracy logowania, CAN i USB.

#### C.1.9a Bezwzględne granice błędu kąta (decyzje Pawła 25.10.2026, O-007)

**Kierunek błędu prognozy:** iskra liczona z czasu od krawędzi natarcia wypada **wcześniej**, gdy wał hamuje szybciej niż zakładała estymata, i **później**, gdy przyspiesza. Za wczesna iskra jest groźniejsza: detonacja w pracy, **odbicie kopniaka przy rozruchu**.

| Środek | Rodzaj | Wymaganie |
|---|---|---|
| Iskra w ROZRUCHU na krawędzi spływu (GMP), bez prognozy | **zapobieganie** — usuwa najgorszy przypadek (hamowanie wału przy kopnięciu) | ECU-IGN-019 |
| Timer startowany sprzętowo zboczem natarcia, minimalne opóźnienie 2° | **zapobieganie** — iskra przed zboczem niemożliwa **przy błędzie prognozy**; nie przy błędnym firmware (B.1.3, poz. 6) | ECU-IGN-023 |
| Granica +1° / −2° w 100 % zapłonów poza rozruchem | wymaganie wobec prognozy | ECU-IGN-022 |
| Przechwytywanie rzeczywistego wyzwolenia tyrystora | **wykrywanie** — nie cofa pojedynczej złej iskry (dopuszczalny czas = 0), zapobiega powtórzeniom | ECU-IGN-024, DTC-IGN-06, -07 |

**Dwa rodzaje przekroczeń, dwie reakcje:** usterka wykonania jest dowodem defektu — tryb zastępczy od pierwszego zdarzenia; błąd prognozy przy prawidłowym wyzwoleniu jest fizyką wału (lądowanie, szarpnięcie sprzęgłem) — reakcja dopiero przy powtarzalności 3/100, żeby twarde lądowanie nie wrzucało trybu zastępczego.

**Tryb zastępczy jest z natury bezpieczny:** iskra na krawędzi spływu nie zależy od prognozy, więc nie może być za wczesna.

#### C.1.10 Wymagania kalibracyjne — do punktu G

| Parametr | Pochodzenie | Uwaga |
|---|---|---|
| Długość kątowa wypustu (elektrycznie) | pomiar enkoderem (krok 7), **±0,1°**; domyślnie 30° | Baza estymaty prędkości — błąd przechodzi wprost do kąta (ECU-IGN-037) |
| **Zbocze elektryczne VR θ_el** względem GMP | pomiar enkoderem (krok 7), **±0,15°** | Offset całej mapy i α_max (ECU-IGN-015, -037) |
| **t_op** — od zbocza elektrycznego do iskry | pomiar na stanowisku (Z27) | Wchodzi do α_max (C.1.9) |
| Szerokość okna bramkowania | stanowisko zakłóceń (Faza 6, O-039), potwierdzenie w Fazie 8 | Wartości wstępne w C.1.6 |
| Próg odchyłki długości wypustu | Faza 8 | Wartość wstępna ±25% |

**Kalibracja musi być przechowywana jako dane, nie jako stałe w kodzie** — platforma ma obsługiwać różne silniki, a każdy ma inną geometrię koła.

#### C.1.12 Stany synchronizacji i dopuszczenie iskry (25.11.2026, O-009)

Stan modelu kąta jest **niezależny od stanu silnika** (A.1) i decyduje, czy iskra w ogóle może zostać zlecona.

| Stan | Wejście | Iskra |
|---|---|---|
| **BRAK** | start firmware; brak zbocza przez 3 ostatnie okresy, nie krócej niż 100 ms; niewiarygodny sygnał w ROZRUCHU lub GOTOWOŚCI (DTC-IGN-11); VDD5 < 4,55 V w ROZRUCHU lub GOTOWOŚCI (DTC-PWR-08b); wykryty ruch wsteczny | **zablokowana** |
| **POMIAR** | pierwsze pełne przejście wypustu (zbocze natarcia, potem spływu) z długością zgodną z kalibracją ±25 % | **zablokowana** — trwa potwierdzanie kierunku |
| **SYNCHRONIZACJA** | kierunek do przodu potwierdzony mechanizmem ECU-IGN-019 | ROZRUCH: na krawędzi spływu (ECU-IGN-019); PRACA: z prognozy po ECU-IGN-036 |

**Zasady (decyzje Pawła 25.11.2026):**
- **Iskra wyłącznie w stanie SYNCHRONIZACJA** (ECU-IGN-040). Kryterium „brak nieplanowanej iskry” jest osobne i bezwzględne: **0 iskier poza SYNCHRONIZACJĄ** w teście T-IGN-019.
- **Niewiarygodny sygnał w ROZRUCHU albo GOTOWOŚCI** (kryteria C.1.7) → powrót do BRAK, licznik DTC-IGN-11 (K0), **bez zatrzasku**. Nieudane kopnięcie z odbiciem wału daje właśnie taki sygnał; dwa takie kopnięcia nie mogą wymagać odblokowania K4. **W PRACY** bez zmian — DTC-IGN-01/02, K4.
- **Zatrzymanie wału w wypuście:** pierwsze zdarzenie po ruszeniu to krawędź spływu bez poprzedzającej krawędzi natarcia — w stanie BRAK ignorowane; POMIAR zaczyna się dopiero od pełnego przejścia.
- **Restart w ruchu** (silnik zgasł, koło napędza wał): SYNCHRONIZACJA trwa, dopóki zbocza przychodzą w oknach — iskra z mapy od razu (C.1.8).
- **Odbicie wału przy kopnięciu (kickback):** ruch wsteczny wykryty mechanizmem kierunku → BRAK. Do wyboru mechanizmu pozostaje ochrona kryterium długości wypustu (C.1.7) i pomiar napięcia kondensatora (iskra tylko przy naładowanym).

**Mechanizm potwierdzenia kierunku — po pomiarze (krok 6a), `[DO USTALENIA]` w ECU-IGN-019.** Krok 6a rejestruje jednocześnie pick-up (CH4) i uzwojenie wzbudzające (MATH), więc jedna sesja rozstrzyga między trzema kandydatami:

| Kandydat | Zasada | Sprzęt |
|---|---|---|
| **Faza uzwojenia wzbudzającego** | Przy ruchu wstecznym znak napięcia wzbudzającego w chwili zbocza pick-upu się odwraca — o ile geometria magnesów to daje | jest: pomiar wzbudzającego PC4 (ECU-SAF-021) |
| Dwa przejścia z wiarygodnym czasem | Dwie krawędzie natarcia odległe o pełen obrót z okresem zgodnym z przyspieszaniem | bez zmian |
| Asymetria sygnału VR | Różny kształt impulsów przy ruchu w przód i w tył | zależy od koła; może wymagać zmiany progu MAX9926 |

**Rejestr pierwszych iskier (T-IGN-019):** ≥ 200 rozruchów z 36 położeń wału co 10°, w tym ≥ 50 z cofnięciem wału; kopnięcia normalne, słabe i z odbiciem, rozrusznik. Zapis: położenie startu, liczba przejść wypustu do pierwszej iskry, kąt pierwszej iskry.

#### C.1.11 Pozycja otwarta — amplituda sygnału VR

Szczelina 0,18 mm jest wyraźnie mniejsza niż typowe 0,3–1,0 mm, co daje mocny sygnał przy rozruchu, ale **przy 10 000 obr/min amplituda może przekroczyć 100 V**, czyli górną granicę przyjętą w ECU-SEN-001.

Do zweryfikowania oscyloskopem na pracującym silniku i do uwzględnienia przy projektowaniu obwodu wejściowego MAX9926 w Fazie 4 — rezystor szeregowy ograniczający prąd wejściowy i klamra. Nie blokuje C.1, bo nie zmienia algorytmu.

---
### C.2 Pozostały zakres punktu C

*Do opracowania.* Mapa rozruchowa, wzbogacenie przy rozgrzewaniu, mapy zapłonu i wtrysku, korekty (temperatura powietrza i cieczy, ciśnienie atmosferyczne, napięcie akumulatora), odcięcie paliwa przy zamkniętej przepustnicy, ogranicznik obrotów, mapa awaryjna przy utracie TPS (B.3.2).

*(Dawne wymaganie skracania czasu ładowania cewki przy wysokich obrotach usunięte 25.10.2026 — dotyczyło zapłonu indukcyjnego.)*

### C.3 Wentylator, światła, profile map, liczniki i zegar (O-055, decyzje Pawła 11.11 i 16.11.2026)

**Wentylator przy pracy (ECU-AUX-001):** załączenie ≥ 88 °C, wyłączenie ≤ 84 °C. Usterka czujnika cieczy → załączony na stałe (DTC-SEN-01/02). Zwarcie kanału → DTC-OUT-02, tylko ostrzeżenie.

**Praca po zgaszeniu (ECU-AUX-002)** — w czasie czuwania przed uśpieniem (30 min, ECU-PWR-004), te same progi. Kończy się trwale przy pierwszym z warunków:

| Warunek | Wartość | Po co |
|---|---|---|
| Brak postępu | temperatura nie spadła o 2 K poniżej szczytu po zgaszeniu w ciągu 3 min od szczytu | **Pompa cieczy stoi** — wentylator chłodzi tylko chłodnicę; bez tego warunku kręciłby się do limitu akumulatora bez efektu |
| Ładunek | całka prądu IS wentylatora ≥ 10 % pojemności akumulatora (konfiguracja) | **Działa dla każdej chemii** — LiFePO4 trzyma ~13 V prawie do rozładowania, więc samo napięcie go nie chroni |
| Napięcie | < 12,0 V (ołowiowy/AGM) albo < 12,8 V (LiFePO4) przy pracującym wentylatorze, przez 10 s | Słaby akumulator kończy wcześniej |
| Czas | 15 min od zatrzymania silnika | Zabezpieczenie przy błędnej konfiguracji lub pomiarze |

Nie startuje po zgaszeniu przez wywrotkę (ECU-SAF-005). Kierowca jej nie przerywa (decyzja Pawła, ryzyko zaakceptowane). Przyczyna zakończenia — zdarzenie w logu.

**Konfiguracja akumulatora** (konfiguracja użytkownika, DTC-SYS-03b): typ (ołowiowy/AGM albo LiFePO4) i pojemność. **Wartość domyślna: ołowiowy, 4 Ah** — zachowawczo, do zmiany na dane akumulatora Bety.

**Profile map (ECU-IGN-039):** 3 profile, wybór z HMI w dowolnej chwili. Przejście: każda wartość wyjściowa (wyprzedzenie po korektach) liczona z obu profili i mieszana liniowo przez 0,5 s; ograniczenie ECU-IGN-015 po zmieszaniu. Ponowny wybór w trakcie przejścia startuje nowe przejście od bieżącej wartości. Wybrany profil w konfiguracji; numer stale na ekranie głównym HMI.

**Światła (ECU-AUX-004, decyzje Pawła 16.11.2026):**

| Zdarzenie | Postojowe | Mijania / drogowe |
|---|---|---|
| Uruchomienie silnika po uśpieniu | włączone | wyłączone do wyboru w HMI |
| Wybór w HMI | — | wyłączone / mijania / drogowe |
| Zgaśnięcie silnika z dowolnej przyczyny | włączone | wyłączone, stan zapamiętany |
| Ponowne uruchomienie bez uśpienia | włączone | stan sprzed zgaśnięcia |
| Uśpienie ECU albo 30 min po zgaśnięciu w stanie AWARIA | wyłączone | wyłączone, stan zapomniany |
| Utrata HMI | bez zmian | bez zmian |

Pobór postojowych po zgaśnięciu (do 30 min czuwania): LED ~0,2–0,4 A → ≤ 0,2 Ah.

**Liczniki (ECU-LOG-010, ECU-LOG-008):** przebieg 0,1 km z impulsów koła i obwodu koła; motogodziny 0,1 h w stanie PRACA. Część poniżej kroku zapisu trzymana w rejestrach domeny podtrzymywanej, pełny krok zapisywany do W25Q128 w strukturze dziennika z wyrównywaniem zużycia. Bez kasowania.

**Zegar (ECU-LOG-011):** RTC ustawiany z aplikacji (USB) i z HMI. Flaga resetu domeny podtrzymywanej przy starcie = czas nieważny → znaczniki w logu oznaczone, HMI pokazuje kreski zamiast godziny do ponownego ustawienia.

---

## D. Struktura danych i map

*Do opracowania — poniżej rozstrzygnięte 25.11.2026 (O-021).*

### D.1 Warstwy danych i ich ochrona (O-021)

**Zasada: granica, która chroni przed błędną mapą, nie może być zmieniana tą samą drogą co mapa.**

| Warstwa | Zawartość | Zmiana | Błąd sumy kontrolnej |
|---|---|---|---|
| **Firmware** | Twarde ograniczenie 28°, δ_min 2°, progi rozrusznika (ECU-SAF-008, -010) | tylko aktualizacja firmware | blokada startu (DTC-SYS-02) |
| **Profil granic** (ECU-SAF-032) | **kalibracja koła: θ_el, długość wypustu, t_op** (z nich α_max, ECU-IGN-015); **najwyższe obroty ogranicznika**; **konfiguracja sprzętowa**: typ czujnika wału, wariant A/B/C | **tylko w trybie kalibracji** (D.2) | **blokada startu** (DTC-SYS-03c) |
| **Mapy** — 3 profile (ECU-IGN-039) | zapłon, korekty, ogranicznik (nie wyżej niż granica), progi wentylatora | aplikacja — strojenie; aktywacja wg ECU-SAF-011 | blokada startu (DTC-SYS-03a) |
| **Konfiguracja użytkownika** | koło, jednostki, akumulator, wybrany profil | aplikacja, HMI | wartości domyślne (DTC-SYS-03b) |

**Mapy sprawdzane względem granic dwa razy:** przy zapisie (odrzucenie z przyczyną) i przy użyciu (obcięcie + zdarzenie). **Obwiednia wyprzedzenia od obrotów — odrzucona** (decyzja Pawła 25.11.2026): pomyłka w mapie mieszcząca się poniżej α_max nie jest wykrywana — ryzyko zaakceptowane (`otwarte.md` rozdz. 9).

**Wariant obsadzenia czytany z płytki (ECU-SAF-033):** rezystor kodujący wariant A/B/C, obsadzany razem ze stopniem zapłonu, czytany przez ADC (PB2) przy każdym starcie. Konfiguracja sprzętowa z profilu granic niezgodna z płytką → **blokada startu** (DTC-SYS-18). Powód: wariant B/C ustawiony na płytce A wysłałby do sterowania bramki tyrystora przebieg ładowania cewki TCI — tyrystor odpaliłby na jego początku, czyli w za wczesnym kącie.

### D.2 Tryb kalibracji i tryb stanowiskowy — fizyczne zezwolenie (O-021)

**Wejście:** wał nieruchomy, **kill switch i START wciśnięte jednocześnie przez 3 s**, potem **potwierdzenie w aplikacji**. Rozrusznik przy wciśniętym kill switchu i tak jest zablokowany (ECU-SAF-019), więc gest jest bezpieczny i wymaga obecności przy motocyklu. Tryb trwa do uśpienia ECU albo wyjścia z aplikacji; **na HMI stały napis „TRYB KALIBRACJI”**.

W trybie dozwolone: zmiana profilu granic (tylko przy nieruchomym wale) oraz **aktywacja map przy pracującym silniku na hamowni** — „tryb stanowiskowy” z ECU-SAF-011, z limitami szybkości zmian z B.5.3. **Testy negatywne:** sam kill switch 3 s — brak wejścia; gest przy obracającym się wale — brak wejścia; zmiana θ_el zwykłą drogą strojenia — odrzucona.

### D.3 Atomowa aktywacja zestawu map (ECU-SAF-034)

- **Dwa bufory:** aktywny i roboczy. Aktywacja = sprawdzenie kompletnego zestawu (suma kontrolna, zgodność z profilem granic) i **jedna atomowa zamiana wskaźnika**.
- **Jeden właściciel wersji na zdarzenie zapłonu:** przerwanie krawędzi natarcia odczytuje wskaźnik zestawu (i przy przejściu między profilami — oba wskaźniki ze współczynnikiem mieszania) **raz, na początku**, i liczy z tej kopii całe zdarzenie, łącznie z ograniczeniami. Zamiana w trakcie nie zmienia już liczonej iskry.
- **B/C (TCI):** wskaźnik pobierany przy decyzji o początku ładowania cewki; koniec ładowania i iskra z tej samej wersji — zmiana mapy nie rozdzieli decyzji o początku i końcu ładowania.
- MVP-A: aktywacja przy rozbrojonym silniku (ECU-SAF-011) albo w trybie stanowiskowym (D.2).

**Granica z budżetu wykonalności (O-067, decyzja Pawła 26.11.2026):** **profil map ≤ 8 KB** — MVP-A 0,34 KB, B/C ~6,3 KB przy siatkach 32 × 20 (`scripts/bilans_map.py`). **W RAM trzymane są wszystkie 3 profile i bufor zapisu** (4 × 8 KB = 32 KB w bilansie RAM, SYS-RES-001): zmiana profilu nie czyta W25Q128, a przejście 0,5 s (ECU-IGN-039) ma oba profile w RAM; bufor zapisu służy atomowej aktywacji D.3. Przydział 16 kB na kopię profilu w W25Q128 zostaje.

Zakres pozostały w D: wymiarowość map, interpolacja, organizacja pamięci flash z uwzględnieniem zużycia komórek.

Zakres: wymiarowość map, interpolacja, parametry konfiguracyjne, profile per model motocykla (L10), organizacja pamięci flash z uwzględnieniem zużycia komórek.

---

## E. Diagnostyka

*Do opracowania*

Zakres: lista błędów i kodów, klasyfikacja krytyczne/niekrytyczne (potrzebna dla decyzji A.5), przechowywanie z znacznikami czasu RTC, sygnalizacja na HMI i w aplikacji desktop. Monitorowanie heartbeat HMI (decyzja L22).

---

## F. Czarna skrzynka

*Rozstrzygnięte 25.11.2026 (O-042, decyzje Pawła); bilans: `scripts/bilans_logu.py`.*

### F.1 Strumień danych

| Kanały | Bajty × Hz | B/s |
|---|---|---|
| Nagłówek ramki: znacznik czasu, licznik | 6 × 100 | 600 |
| Obroty, wyprzedzenie zadane, kąt iskry przechwycony | 6 × 100 | 600 |
| Napięcie kondensatora, szczyt wzbudzającego | 4 × 100 | 400 |
| Stany: maszyna stanów, synchronizacja, kill, START, flagi usterek | 6 × 100 | 600 |
| Akcelerometr 3 osie | 6 × 200 | 1200 |
| Temperatury cieczy i powietrza, akumulator, VDD5, VSOUT1 | 10 × 10 | 100 |
| Bieg, prędkość koła, ciśnienie, temperatura ECU | 8 × 10 | 80 |
| **Razem** | | **~3,5 kB/s** |

Kanały i częstotliwości — propozycja; po zmianie skrypt przelicza bilans.

### F.2 Pierścień ciągły (ECU-LOG-012)

Strumień zapisywany na bieżąco do pierścienia w W25Q128 — **ostatnie 8 min pracy silnika** (1,7 MB). Okno „przed zdarzeniem” jest więc w pamięci, zanim zdarzenie nastąpi; odcięcie akumulatora zabiera najwyżej dane z bufora stron w RAM (≤ 0,3 s), a przy wykryciu zaniku zasilania bufor jest dopisywany (ECU-LOG-007). Każdy sektor kasowany co ~8 min pracy — 100 000 cykli to ~13 000 h pracy silnika.

### F.3 Zdarzenia z oknem danych (ECU-LOG-006)

**16 slotów po 15 s (10 s przed, 5 s po); zawsze nadpisywane najstarsze** (decyzja Pawła).

| Wyzwalacz | Uwagi |
|---|---|
| **Przeciążenie > 8 g przez ≥ 10 ms** (wypadkowa z AIS2IH) | wartość wstępna — korekta po pomiarze drgań (SYS-ENV-006) |
| **Usterka K3 albo K4** | **oprócz wywrotki (DTC-SAF-05)** — wywrotka w terenie jest częsta, tylko gasi silnik (ECU-SAF-005) i trafia do dziennika (F.4) |
| **Nieplanowana utrata zasilania albo reset w PRACY** | wykrywana przy następnym starcie znacznikiem „ECU pracuje” (B.4); okno = ostatnie 15 s pierścienia |

**Znacznik zdarzenia** zapisywany atomowo w chwili wyzwolenia (dwie kopie, numer kolejny, suma); po 5 s okno kopiowane z pierścienia do slotu. Przerwane kopiowanie dokańczane przy następnym starcie, dopóki pierścień nie nadpisał danych (8 min pracy). **Okno „po” nie powstaje, gdy zdarzenie odcina zasilanie** — ryzyko zaakceptowane (`otwarte.md` rozdz. 9); okno „przed” jest pełne do ≤ 0,3 s przed zanikiem.

### F.4 Dziennik usterek z ramką danych (ECU-LOG-013, decyzja Pawła)

**Każdy kod usterki i każde zdarzenie** (w tym wywrotka i kill switch) — rekord: czas z RTC z flagą ważności (ECU-LOG-011), kod, stan maszyny stanów, **wartość, która przekroczyła próg, i ten próg**, oraz ramka danych z chwili wykrycia: obroty, wyprzedzenie, temperatury, napięcia, bieg, prędkość, przyspieszenie. Rekord ~64 B; dziennik 256 kB (~4000 rekordów), **nadpisywane najstarsze**.

### F.5 Podział W25Q128 (16 MB; do 26.11.2026 W25Q64, 8 MB)

| Obszar | kB |
|---|---|
| Pierścień ciągły, 8 min | 1680 |
| Zdarzenia: 16 × 15 s | 896 |
| Dziennik usterek | 256 |
| Mapy: 3 profile × 2 kopie | 96 |
| Profil granic, konfiguracja, rekord transakcji — po 2 kopie | 24 |
| Liczniki | 64 |
| Histogram ECU-LOG-009 | 8 |
| **Obraz aplikacji ECU *nowy* (H.1, od 26.11.2026)** | 448 |
| **Obraz aplikacji ECU *poprzedni* (H.1)** | 448 |
| **Razem** | **3920 (24 %)**, granica 50 % (SYS-RES-002), rezerwa ~12 MB |

**Rozkład zmian prędkości wału (ECU-LOG-009, decyzja Pawła 11.11.2026):** histogram zmiany prędkości na obrót, osobno hamowanie, przyspieszanie i odwrócenie przyspieszenia, oraz licznik obrotów poza warunkiem ECU-IGN-022 (< 4 %, odwrócenie ≤ 2,5 %). Dane do Fazy 8 — czy warunek obejmuje rzeczywistą jazdę (Z26).


---

## G. Kalibracja

*Do opracowania*

Zakres: czujnik biegu (pozycje, z uwzględnieniem układu 1-N-2-3-4-5-6 i filtra czasowego), koło impulsowe (długość wypustu, położenie krawędzi natarcia względem GMP, opóźnienie detekcji w torze VR), a w wariantach z TPS także TPS (min/max).

---

## H. Bootloader i aktualizacja

**Wymagania: ECU-BTL-001…006 (decyzje Pawła 25.10.2026).** Rozpisanie procedury — po podziale pamięci (punkt D).

| Element | Ustalenie |
|---|---|
| Warunki dopuszczenia | Kill switch STOP + wał stoi (≥ 2 s bez VR **i** STOP) + VBAT ≥ 12,0 V; sprawdzane przez ECU, utrata warunku przerywa zapis |
| Rozbrojenie | Sprzętowe przez kill switch: zapłon (ECU-SAF-001) i rozrusznik (ECU-SAF-019) — niezależne od GPIO w trakcie kasowania Flash |
| Pamięć | Dwa banki; nowy obraz do banku nieaktywnego; przerwanie na dowolnym etapie = praca na poprzedniej wersji |
| Weryfikacja | CRC-32 (sprzętowy CRC) + zgodność wersji ECU/HMI/protokołu; **bez podpisu cyfrowego** (ryzyko zaakceptowane) |
| Potwierdzenie | Dojście do GOTOWOŚCI z poprawnym autotestem; 3 nieudane starty → powrót do poprzedniego banku |
| Bootloader | Zabezpieczony przed zapisem, zmiana tylko przez SWD |
| HMI | Przez ECU jako pośrednika po CAN (SYS-COM-001a), pakiet ECU+HMI jako jedna transakcja (SYS-COM-005b) |

### H.1 Instalacja i wybór obrazu przez bootloader (zmiana 26.11.2026 — decyzja Pawła, O-067; wcześniej dwa sloty, 25.11.2026, O-041; ECU-BTL-007)

**Podział Flash STM32G474VET (512 KB):** bootloader **≤ 64 KB** na początku, chroniony przed zapisem (ECU-BTL-006); **rekord startowy** — 2 strony po 2 KB na końcu Flash, poza ochroną; **jeden slot aplikacji 444 KB** między nimi — z niego zawsze wykonuje się program. **Obrazy w W25Q128 (F.5):** obszar *nowy* i obszar *poprzedni*, po 448 KB. Pakiet zawiera jeden obraz zlinkowany pod adres slotu.

**Powód zmiany (O-067):** przy dwóch slotach po 224 KB granica 50 % (SYS-RES-001) dawała 112 KB na aplikację przy szacunku 88–127 KB, a 32 KB bootloadera — 16 KB przy zmierzonych 15,9 KB samej warstwy USB i sterowników.

| Krok | Przerwanie zasilania w tym kroku → stan po ponownym starcie |
|---|---|
| 1. Aplikacja zapisuje obraz do obszaru *nowy*, sprawdza CRC (ECU-BTL-004) | stary program w slocie, obszar *nowy* nieważny |
| 2. Aplikacja zapisuje rekord startowy *do instalacji* (wersja, CRC obrazu) i restartuje | jw. albo bootloader widzi rekord i przechodzi do kroku 3 |
| 3. Bootloader kopiuje bieżący obraz ze slotu do obszaru *poprzedni* (pomijane, gdy CRC już się zgadza) | rekord bez zmian — bootloader powtarza kopiowanie od początku |
| 4. Bootloader kopiuje obraz *nowy* do slotu, sprawdza CRC w slocie, zapisuje rekord *próbny* z licznikiem startów | źródło w W25Q128 nienaruszone — kopiowanie od początku; slot bez poprawnego CRC **nigdy nie jest uruchamiany** |
| 5. Start próbny i zatwierdzenie (H.2) | jak w H.2 |
| 3 nieudane starty próbne | bootloader kopiuje obszar *poprzedni* do slotu, rekord *przywrócony* |

**HMI (STM32G474RE, 512 KB, dwa banki po 256 KB; do 26.11.2026 STM32G0B1xE):** bootloader ≤ 32 KB na początku banku 1, chroniony przed zapisem; slot A — reszta banku 1 (224 KB), slot B — bank 2; rekord startowy w dwóch kopiach (2 × 2 KB na końcu banku 2); obraz ≤ 224 KB, granica SYS-RES-001 — 112 KB. Zapis zawsze do banku, z którego nie wykonuje się kod (H.2) — HMI zostaje przy dwóch slotach, bo nie ma własnej pamięci zewnętrznej na obrazy.

**Kolejność gwarantuje kompletną kopię *poprzedni*, zanim slot zostanie nadpisany.** Rekord startowy w dwóch kopiach (numer sekwencji, CRC) w Flash procesora — bootloader nie zależy od W25Q128 przy zwykłym starcie: przy niedostępnej W25Q128 uruchamia slot z poprawnym CRC (aplikacja zgłasza DTC-SYS-05). **Option bytes nie są zapisywane** w ścieżce aktualizacji — ich przerwany zapis zostawia procesor w stanie zależnym od mechanizmu ładowania, czego nie da się zabezpieczyć kopią.

**Koszt:** powrót do poprzedniej wersji to kopiowanie (sekundy) zamiast przełączenia; bootloader obsługuje W25Q128 i kopiowanie; przy uszkodzonej W25Q128 nie ma powrotu do wersji poprzedniej, ale odzyskiwanie przez USB zostaje (H.4).

### H.2 Transakcja pakietu ECU + HMI (O-041, ECU-BTL-009)

| Krok | Przerwanie zasilania lub połączenia w tym kroku → stan po ponownym starcie |
|---|---|
| 1. Sprawdzenie warunków (ECU-BTL-001) | bez zmian |
| 2. Zapis obrazu HMI do nieaktywnego banku HMI po CAN, sprawdzenie CRC przez HMI | ECU i HMI na starych wersjach; niedokończony obraz HMI nieważny |
| 3. Zapis obrazu ECU do obszaru *nowy* w W25Q128, sprawdzenie CRC (H.1, kroki 1–2) | jw. |
| 4. ECU zapisuje rekord startowy *próbny* + znacznik transakcji z oczekiwaną wersją HMI; polecenie dla HMI: rekord *próbny* | po starcie ECU widzi znacznik transakcji: jeśli HMI nie przyjęło rekordu — ECU ponawia polecenie (obraz HMI jest już sprawdzony) |
| 5. Instalacja obrazu ECU przez bootloader (H.1, kroki 3–4), start próbny obu urządzeń | ECU sprawdza: autotest, **mapy i profil granic czytelne dla nowej wersji**, para wersji ECU/HMI zgodna (ECU-BTL-005) |
| 6. Zatwierdzenie: ECU, potem polecenie zatwierdzenia dla HMI | znacznik transakcji usuwany dopiero po potwierdzeniu z HMI; przy przerwie — ECU dokańcza po następnym starcie |
| Niepowodzenie startu próbnego 3 razy | bootloader przywraca obraz *poprzedni* (H.1); ECU poleca HMI powrót do poprzedniego banku |

**Zasada: ECU jest właścicielem transakcji** — po każdym starcie dokańcza albo wycofuje parę, zanim przejdzie do GOTOWOŚCI. Niezgodna para bez znacznika transakcji (np. podmieniony moduł) — DTC-COM-04, jak dotąd.

### H.3 Atomowe rekordy danych (O-041, ECU-BTL-010)

Mapy (3 profile), profil granic, konfiguracja użytkownika i liczniki zapisywane w W25Q128 jako **dwie kopie** (numer sekwencji, CRC, wersja formatu). Zapis: kasowanie sektora starszej kopii → zapis → odczyt kontrolny; nowa kopia obowiązuje dopiero, gdy jest poprawna. Zanik zasilania w dowolnej chwili zostawia poprzednią poprawną kopię. **Firmware wybiera najnowszą kopię w formacie, który rozumie** — po powrocie do starszej wersji firmware wraca też do kopii w starym formacie. Ten sam schemat w pamięci zasobów HMI (HMI-UI-013).

### H.4 Tryb odzyskiwania przez USB (decyzja Pawła 25.11.2026, ECU-BTL-008)

Brak poprawnego obrazu w slocie i w obszarze *poprzedni* → bootloader zostaje w **trybie odzyskiwania** i przyjmuje obraz z aplikacji desktop przez USB — bez działającej aplikacji ECU. Te same kontrole (CRC, zgodność, warunki ECU-BTL-001); zapłon i rozrusznik zablokowane sprzętowo (ECU-BTL-002). Obraz z USB trafia do obszaru *nowy* i jest instalowany jak w H.1; przy niedostępnej W25Q128 — wprost do slotu. Koszt: stos USB w bootloaderze — warstwa sterowników zmierzona szkieletem: 15,9 KB (`scripts/szkielet`, O-067). HMI: bootloader HMI chroniony przed zapisem przyjmuje obraz po CAN od ECU (SYS-COM-001a), więc HMI odzyskuje się przez ECU.

Pozostaje do rozpisania w punkcie H: format pakietu i sekwencja komend USB.

---

## I. Architektura zadań czasu rzeczywistego

*Do opracowania*

### I.2 Nadzór funkcji — watchdog i odzyskiwanie (O-012, decyzje Pawła 4.11.2026)

**Dwa poziomy watchdoga:**

| Poziom | Gdzie | Co wykrywa | Reakcja |
|---|---|---|---|
| 1 | Watchdog wewnętrzny procesora (własny oscylator) | Całkowite zawieszenie procesora | Reset |
| 2 | **Watchdog PMIC TPS65381A-Q1** (zewnętrzny; zastąpił TPS3430-Q1) | **Brak postępu funkcji bezpieczeństwa**, zły czas lub kolejność, usterka zgłoszona przez procesor | ENDRV niski — sprzętowa blokada zapłonu, rozrusznika, wtrysku i pompy; po 8 złych zdarzeniach reset |

Watchdog PMIC jest zaprojektowany do nadzoru procesora (karta PMIC rozdz. 5.4.10: *„monitors the correct operation of the MCU”*); **innych układów, np. HMI, nie nadzoruje.**

**Tryb pytanie–odpowiedź z sygnaturą (ECU-SAF-026).** Każda nadzorowana funkcja przy każdym przebiegu zapisuje punkt kontrolny. Zadanie nadzorcze sprawdza w każdej sekwencji, czy wszystkie funkcje odmeldowały się w swoim czasie i we właściwej kolejności. **Odpowiedź dla PMIC liczona jest z pytania i sygnatury punktów kontrolnych** i wysyłana po SPI3 — samo przerwanie timera nie wygeneruje poprawnej odpowiedzi. Sekwencja ~20 ms, więc ENDRV opada w ≤ 100 ms od zawieszenia funkcji. Wykrytą usterkę wewnętrzną (np. wyjątek MPU) procesor zgłasza impulsem niskim na pinie ERROR/WDI (monitor błędów PMIC w trybie impulsu niskiego, aktywny tylko w trybie pytanie–odpowiedź) — PMIC przechodzi w stan SAFE i od razu opuszcza ENDRV (karta 5.4.16, 5.4.24). Licznik błędów PMIC: ENDRV niski od 5 złych zdarzeń, reset przy kolejnym po 7 (karta 5.4.11).

**Nadzorowane funkcje bezpieczeństwa:**

| Funkcja | Punkt kontrolny | Uwagi |
|---|---|---|
| Tor zapłonu: synchronizacja, model kąta, planowanie iskry | każde zbocze wału | **tylko przy ważnej synchronizacji** — przy kopnięciu wał obraca się raz na ~200 ms |
| Zadanie bezpieczeństwa: kill switch, zatrzaski, ogranicznik obrotów | stały okres | — |
| Pomiary ADC: kill, uzwojenie wzbudzające, temperatury | stały okres | — |
| Wykrywanie wywrotki (AIS2IH) | stały okres | — |
| Wtrysk **[B/C]** | każdy cykl wtrysku | tylko przy ważnej synchronizacji |

**Poza watchdogiem — z własnym odzyskiwaniem (ECU-SAF-027):** CAN i HMI, USB, logi. Ich awaria nie gasi silnika (SYS-COM-008). Jeśli zablokuje procesor, funkcje bezpieczeństwa przestaną się odmeldowywać i watchdog zadziała pośrednio.

**Drabinka odzyskiwania (zasada, decyzja Pawła):** ponowienie → sprzętowy reset układu (kontroler CAN i transceiver przez STB_N/EN, stos USB, pamięć logów) → kod usterki i praca ograniczona, **z limitem prób**. Wartości dla każdej funkcji — przy specyfikacji zadań (punkt I).

**Odzyskiwanie HMI (SYS-COM-010):** (1) watchdog wewnętrzny procesora HMI (HMI-SYS-001); (2) brak ramek z HMI przez **5 s** przy obudzonym ECU → ECU odcina zasilanie HMI na **0,5 s** (ECU-PWR-011); (3) najwyżej **3 próby pod rząd**, potem DTC-COM-05 i **jedna próba co 60 s**. Nadzór wstrzymany podczas aktualizacji firmware HMI.

**Reguły przeciw fałszywemu odcięciu w jeździe:**
- kasowanie wewnętrznej pamięci Flash (wstrzymuje procesor) — tylko przy stojącym silniku;
- autotest logiczny PMIC w stanie ACTIVE opuszcza ENDRV na 21 ms — wyłącznie w stanie DIAGNOSTIC przy starcie;
- zadania wyzwalane zboczem wału nadzorowane tylko przy ważnej synchronizacji;
- priorytety przerwań tak, by CAN, USB i logi nie mogły zagłodzić funkcji bezpieczeństwa (punkt I).

### I.1 Errata STM32G474 (ES0430) — obejścia obowiązkowe (O-028, 3.11.2026)

Rewizje krzemu: Z, Y, X. Lista obowiązujących pozycji do potwierdzenia dla rewizji kupionej partii.

| Pozycja errata | Dotyczy nas, bo | Obejście |
|---|---|---|
| 2.2.2 Pamięć podręczna danych może się uszkodzić przy zapisie Flash w trakcie odczytu z drugiego banku | Bootloader: nowy obraz do banku nieaktywnego (ECU-BTL-003) | Wyłączenie pamięci podręcznej danych na czas programowania (wg errata) |
| 2.2.3 FLASH_ECCR uszkodzony po resecie lub zaniku zasilania w trakcie programowania | Przerwana aktualizacja (ECU-BTL-003) | Wg errata — obsługa przy starcie po przerwanym zapisie |
| 2.2.5 Domena podtrzymywana uszkodzona po spadku napięcia bez resetu zasilania | Migawka przy resecie watchdoga w domenie podtrzymywanej (ECU-SAF-006a), superkondensator | Wg errata; dane w domenie podtrzymywanej zawsze z sumą kontrolną |
| 2.2.4 Niestabilny LSI przy taktowaniu RTC | RTC | **RTC z kwarcu LSE** (decyzja Pawła 3.11.2026) |
| 2.2.8 Kwarc LSE zaburzany przez przełączanie PC13 (bez obejścia) | LSE | PC13 nieużywany, statyczny |
| 2.2.1 Pełny JTAG niedostępny przy PB4 jako GPIO | PB4 = GPIO | Debug wyłącznie przez SWD |
| 2.11.1 Fałszywa aktualizacja rejestrów HRTIM w trybie liczenia góra–dół | HRTIM | Tryb góra–dół nieużywany |
| 2.11.3 Błędny stan wyjścia HRTIM w trybie PWM z porównaniem „większe niż” | HRTIM | Konfiguracja bez tego trybu albo obejście wg errata |
| 2.19.1 Rozsynchronizowanie FDCAN przy włączonym filtrowaniu zbocza | CAN | Filtrowanie zbocza wyłączone |
| 2.19.2 Odwrócona kolejność ramek w Tx FIFO przy określonym użyciu buforów | CAN | Wg errata |
| 2.7.x ADC: kolejki kontekstów wstrzykiwanych, wpływ jednej instancji ADC na dokładność innej (2.7.11) | ADC — 17 kanałów na kilku instancjach, próbkowanie z HRTIM | Wg errata; próba dokładności przy jednoczesnej pracy instancji |
| 2.20.2 Błędna suma CRC16 w buforze USB (bez obejścia) | USB — aktualizacja i logi | **Integralność na poziomie aplikacji** — suma kontrolna każdego pakietu i CRC-32 obrazu (ECU-BTL-004) |
| 2.18.1 Bit BSY SPI może zostać ustawiony po wyłączeniu SPI | SPI1–3 | Wg errata |

Zakres: priorytety przerwań, budżet czasowy, obsługa watchdoga okienkowego, rozdział rdzeń real-time / zadania tła.

---

## J. Firmware HMI

### J.1 Wygląd, pamięć zasobów i profile (O-067, decyzje Pawła 26.11.2026)

**Wymaganie jakości (HMI-UI-015):** wygląd na wysokim poziomie — przezroczystości, gradienty, cienie i poświaty, obracane wskazówki, animowane symbole i przejścia, wygładzane czcionki. Realizacja: sterownik graficzny BT817Q (EVE4) rysuje i miesza warstwy sam; **cienie i poświaty jako gotowe obrazy z kanałem przezroczystości** (EVE nie liczy rozmycia na żywo); animowane symbole jako sekwencje klatek z pamięci modułu, odtwarzane przez koprocesor; procesor HMI (STM32G474RE, FPU) liczy co klatkę pozycje, krzywe animacji i formatowanie, buduje listę poleceń i wysyła ją przez Quad-SPI z DMA. **Ekran wzorcowy** sprawdzany na makiecie przed projektem płytki HMI (T-UI-015).

**Animacja startowa:** pełnoekranowe logo odtwarzane przy włączeniu jako wideo MJPEG z pamięci modułu (BT817Q odtwarza je samodzielnie); w zestawie wyglądu użytkownika, z domyślną w zasobach systemowych.

**Wygląd na profil (HMI-UI-016):** każdy z 3 profili map (ECU-IGN-039) ma **własny układ ekranu i własny dobór danych**. Układy korzystają ze **wspólnej biblioteki obrazów użytkownika** — ten sam obraz użyty w kilku profilach zajmuje miejsce raz. Zmiana profilu przełącza układ w ≤ 0,5 s z animowanym przejściem (razem z przejściem map). Elementy stałe HMI-UI-012 (pas usterek, numer profilu) — w każdym układzie.

**Podział pamięci modułu (32 MB, granica 50 % — SYS-RES-002):**

| Obszar | Rozmiar |
|---|---|
| Sterownik pamięci flash koprocesora (wymagany przez BT817Q) | 4 KB |
| Zasoby systemowe: czcionki, ikony, animacje, przejścia, układy domyślne — **2 kopie × 4 MB** (para z wersją firmware HMI) | 8 MB |
| Zestaw wyglądu użytkownika: 3 układy + biblioteka obrazów — **2 kopie × 3 MB** | 6 MB |
| Ustawienia HMI (krzywa jasności itp.) — rekordy H.3 | 64 KB |
| **Razem** | **~14,1 MB (44 %)** |

**Przebieg zmiany wyglądu:** aplikacja (edytor) zamienia obrazy na format EVE (ASTC z przezroczystością) i sprawdza limity HMI-UI-013 → pakiet USB → ECU → CAN do HMI (~20 kB/s, 3 MB ≈ 2,5 min) → zapis do nieaktywnej kopii przez koprocesor, sprawdzenie CRC → przełączenie rekordu. Przerwane wgrywanie zostawia poprzedni zestaw. Zmiana samych układów bez obrazów — HMI przepisuje bibliotekę z aktywnej kopii lokalnie, bez przesyłania po CAN. Zasoby systemowe zmieniają się tylko z firmware HMI (transakcja H.2) — powrót do starszego firmware wraca do pary zasobów.

**W pracy:** przy starcie i zmianie profilu HMI czyta do RAM tylko opis układu (kilka KB); duże obrazy rysowane bezpośrednio z pamięci modułu (ASTC), czcionki i obrazy częste — w pamięci graficznej 1 MB (granica 75 %, decyzja Pawła).


*Do opracowania*

**Ustalone:**
- Przy utracie komunikacji z ECU — komunikat o błędzie i **wygaszenie danych** (decyzja L11). Żadna wartość nie jest wyświetlana, żeby nie wprowadzać w błąd zamrożonym odczytem
- Po resecie MCU wymagana poprawna **reinicjalizacja koprocesora EVE4** (decyzja L22)
- **Timeout wyświetlacza 3 min** bez interakcji (decyzja A.2)
- **Uśpienie na polecenie ECU po CAN** (sekwencja: `produkt.md` rozdz. 6.4). ECU dyryguje; HMI potwierdza **po fizycznym wysłaniu ramki** i dopiero wtedy przechodzi w Go-to-Sleep; naciśnięcie przycisku w trakcie przerywa usypianie. **Własny timeout awaryjny 30 s** bez ramek z ECU. Obsługa zignorowanego Go-to-Sleep jak w ECU (A.4)
- **Wybudzanie przyciskiem (od 18.10.2026):** drabinka przycisków jest węzłem WAKE transceivera HMI; naciśnięcie włącza szyny HMI, firmware startuje od zera i dopiero wtedy ADC określa, który przycisk. **Nacisk budzący tylko budzi.** Przy starcie ta sama sekwencja odczytu ERR_N co w ECU (A.4)
- **Jasność wg temperatury (HMI-UI-004, decyzja Pawła 11.11.2026):** pełna jasność do 70 °C panelu; powyżej ograniczenie do 50 % i zgłoszenie DTC-HMI-03 do ECU; powrót poniżej 67 °C. Temperatura panelu = czujnik + przesunięcie z T-UI-004. Ściemnianie w zakresie pracy odrzucone — podświetlenie to ~10 % ciepła na słońcu (`produkt.md` 8.2)
- Przy zasypianiu: zakończenie zapisów, potwierdzenie do ECU, TJA1043 w Go-to-Sleep — szyny HMI gasną przez INH

**Przyciski (O-035, decyzje Pawła 9.11.2026; sprzęt: `produkt.md` 8.3):**
- Odczyt r co 5 ms; stan przyjęty po **4 kolejnych próbkach w tym samym oknie** (20 ms) — mieści się w HMI-UI-001.
- Stan **nieprawidłowy** (kombinacja bez P4, wartość poza oknami) — brak komendy. Trwa **> 1 s → DTC-HMI-01**.
- **Zwarcie kabla** (r < 0,016) **> 1 s → DTC-HMI-01**.
- Przycisk trzymany **> 30 s** — uznany za zablokowany, ignorowany do zwolnienia, **DTC-HMI-02**.
- Przycisk trzymany w chwili wybudzenia — ignorowany do zwolnienia (nacisk budzący tylko budzi).
- Zgłoszenia DTC idą po CAN do logu ECU.

**Potwierdzenie odblokowania K4 (HMI-UI-010)** — jedyna komenda z HMI wpływająca na silnik (start i kill idą wprost do ECU):
- naciśnięcie P1 **rozpoczęte po wyświetleniu komunikatu**, trzymane **≥ 1 s**, bez stanu nieprawidłowego w trakcie;
- ramka potwierdzenia niesie **identyfikator komunikatu, który był wyświetlony**, i licznik; ECU przyjmuje ją tylko dla komunikatu aktywnego w tej chwili — potwierdzenie starego ekranu nie działa na nowy;
- warunek zatrzymanego wału i pozostałe zasady odblokowania — B.4.

**Dane nieaktualne (HMI-UI-011):** każda wartość ma znacznik świeżości z licznika ramki, z której pochodzi. Wartość z ramki starszej niż **3 okresy nadawania** — kreski `---` w miejscu tej wartości, niezależnie od pozostałych. Utrata całej komunikacji — HMI-UI-003 (300 ms).

**Wygląd ekranu (HMI-UI-012, -013, decyzje Pawła 25.11.2026):** układ z pełnego edytora w aplikacji — widgety, czcionki z zestawu, własne obrazy; bez reguł czytelności. Firmware rysuje układ użytkownika, a **nad nim** elementy stałe: pas usterek P2/P3 i numer profilu map, w stałym stylu na własnym nieprzezroczystym tle. Ekrany P3 (K4) i potwierdzenie odblokowania zasłaniają układ w całości. Przy starcie kontrola sumy i wersji układu; błąd → układ domyślny z firmware + DTC-HMI-04.

**Jasność (HMI-UI-014, HMI-UI-004):** poziom = min(krzywa z czujnika światła, ograniczenie temperaturowe). Krzywa domyślna: < 10 lx → 5 %, 10–1000 lx → rampa logarytmiczna, > 1000 lx → 100 %; średnia z 2 s, zmiana przy różnicy ≥ 5 %. Usterka czujnika → 100 % + DTC-HMI-05.

Zakres do rozpisania: maszyna stanów HMI, struktura menu, format pliku układu i obrazów, obsługa heartbeat z ECU.
