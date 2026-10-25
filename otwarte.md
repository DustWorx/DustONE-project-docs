# Pozycje otwarte — ECU „Dust ONE"

Jedyny rejestr pozycji otwartych w projekcie. Zastępuje pięć wcześniejszych: luki `L`, ryzyka `R`, pozycje pierwszego audytu `F`, pozycje drugiego audytu `A` oraz rejestr założeń. Kolumna **Pochodzenie** zachowuje stare identyfikatory, żeby odwołania w dokumentach i w audytach nadal dawały się odnaleźć.

**Stan na 13.10.2026.** Liczby w tym pliku generuje `scripts/kontrola.py`.

## Jak czytać

**Trzy niezależne statusy.** Pozycja jest zamknięta dopiero wtedy, gdy wszystkie trzy są spełnione — to reakcja na sytuację, w której pozycja „brak repozytorium" była oznaczona jako zamknięta, a repozytorium nie istniało.

| Status | Znaczenie |
|---|---|
| **D** | decyzja przyjęta — wiadomo, co robimy |
| **M** | mechanizm wdrożony — rozwiązanie istnieje w dokumencie, schemacie lub kodzie |
| **W** | dowód zaakceptowany — pomiar, test albo przegląd potwierdził skuteczność |

**Pozycja zamknięta wypada z tego pliku.** Historię nosi repozytorium, a pełne uzasadnienia zamkniętych pozycji zostały w dokumentacji przed konsolidacją, na gałęzi `Old-docs` tego repozytorium. Nie prowadzimy listy rzeczy zrobionych.

**Założenia są osobnym rodzajem obiektu** i mają własną sekcję: to nie praca do wykonania, a twierdzenia, które mogą być fałszywe, razem z listą tego, co się przez nie zawali.

---

## Co blokuje bramkę G0

Pozycje, bez których nie da się zamknąć wymagań. **Reguła nadrzędna: bramka nie przechodzi, jeśli otwarta jest choćby jedna pozycja P0 albo pozycja dotycząca bezpieczeństwa.**

| ID | Pozycja |
|---|---|
| **O-001** | Tor AC-CDI: wymagania i diagramy przebudowane 25.10.2026; otwarte: pomiar wzbudzającego, izolacja WN (ECU-IGN-027), dobór elementów |
| **O-007** | Granica błędu kąta ustalona 25.10.2026 (+1° / −2°, rozruch na krawędzi spływu); zostaje model O-008 i testy |
| **O-013** | Watchdog a uśpienie — rozstrzygnięte architekturą INH 18.10.2026; zostaje schemat i dowód |
| **O-016** | Analiza zagrożeń wykonana 25.10.2026 (B.1.2); zostaje niezależny przegląd (O-057) i testy |
| **O-019** | Rozbrojenie przy aktualizacji — rozstrzygnięte 25.10.2026 (kill switch STOP); zostaje dowód |
| **O-020** | Live tuning — wymaganie zapisane 18.10.2026 (ECU-SAF-011); zostaje implementacja i testy |
| **O-022** | Obwiednia napięciowa ustalona 18.10.2026; zostaje pomiar statora i dobór TVS |
| **O-023** | Bilans uśpienia — ≤ 63 µA po zmianie architektury; zostaje dobór elementów w przydziałach i pomiar |
| **O-024** | Scenariusze startu rozstrzygnięte 18.10.2026; zostaje implementacja i próby |
| **O-040** | Bootloader — wymagania ECU-BTL-001…006 zapisane 25.10.2026; zostaje projekt i testy |
| **O-047** | Profil wibracji — plan pomiaru ustalony 25.10.2026 (zestaw AIS2IH + iPhone); czeka na pomiar |
| **O-050** | Kryteria odbioru A1–A15 zatwierdzone 25.10.2026 (A4 z granicą O-007); zostaje dowód przy odbiorze |
| **O-051** | Wyposażenie i budżet ustalone 25.10.2026 (`proces.md` 5.1); zostaje kompletowanie przyrządów |
| **O-058** | 2 wymagania bez ustalonej wartości: SYS-ENV-006 (zamykane w O-047) i ECU-IGN-027 — odstępy izolacyjne z pomiaru napięcia szczytowego (O-001) |

---

## 1. Zapłon i synchronizacja

Obszar o najwyższym priorytecie. Pozycje O-001 i O-005 są warunkiem wstępnym dla pozostałych — bez nich reszta opiera się na niezweryfikowanych danych wejściowych.

| ID | Pozycja | Dowód zamknięcia | Bramka | D | M | W | Pochodzenie |
|---|---|---|---|---|---|---|---|
| **O-001** | **Tor energii zapłonu MVP-A: AC-CDI — decyzja Pawła 18.10.2026.** Topologia fabryczna potwierdzona: osobne uzwojenie wzbudzające w statorze, fabryczna cewka RC01 IG5128 zachowana. Energia iskry z uzwojenia wzbudzającego, logika ECU z akumulatora. Odrzucone: DC-CDI i zapłon indukcyjny. **Rozstrzygnięte 25.10.2026:** impulsowa bramka tyrystora (ECU-IGN-005), odcięcie dwiema ścieżkami — zwarcie uzwojenia wzbudzającego i bramki tyrystora — z testem przy każdym zgaszeniu (ECU-SAF-001, -021), wymagania energii, rozładowania i izolacji (ECU-IGN-025…027), **przebudowa zapisów VBG08H-E wykonana** (B.2.3, C.1.3, C.1.5, rozdz. 9.2 i 10, DTC-IGN-04/05 wycofane, zastąpione przez DTC-IGN-08). **Otwarte:** (1) przebieg uzwojenia wzbudzającego względem GMP (Z14); (2) napięcie szczytowe → odstępy izolacyjne i styki złącza (ECU-IGN-027); (3) dobór i arkusze kwalifikacji elementów bloku CDI. Diagramy przebudowane 25.10.2026 | Pomiar wzbudzającego względem GMP; karta złącza; arkusze kwalifikacji | G1 | ✅ | ❌ | ❌ | A01, Z12 |
| **O-002** | **Polaryzacja wyłączenia drivera zapłonu — NIEAKTUALNE 25.10.2026.** Dotyczyła EN drivera VBG08H-E, usuniętego 15.10.2026. W AC-CDI bramka tyrystora ma rezystor bramka–katoda i sprzężenie pojemnościowe; stan bezpieczny per wyjście dalej w O-017 | — | — | — | — | — | A02, ECU-SAF-016 |
| **O-003** | **Odcięcie awaryjne nie może samo wytworzyć iskry (przeredagowane 25.10.2026 pod AC-CDI).** Dawny mechanizm — przerwanie prądu cewki indukcyjnej — nie występuje. W AC-CDI: zwarcie uzwojenia wzbudzającego nie rozładowuje kondensatora (blokuje dioda ładująca), zwarcie bramki do katody nie wyzwala tyrystora. Pozostaje do wykluczenia **samoczynne załączenie tyrystora stromym narastaniem napięcia** w chwili przełączania ścieżek odcięcia — rezystor bramka–katoda i obwód tłumiący na tyrystorze | Dobór tyrystora z kartą (dopuszczalna stromość napięcia); test zadziałania kill switcha w wielu fazach obrotu z detekcją iskry | G1, G3 | ❌ | ❌ | ❌ | A03 |
| **O-004** | **Sufit czasu ładowania nie był niezależnym nadzorem** (rejestr okresu HRTIM dzielił zegar z chronioną funkcją). **Rozstrzygnięte 25.10.2026:** w AC-CDI zastąpione bramką tyrystora sprzężoną pojemnościowo — niezależną od zegara i firmware; zawieszone wyjście daje najwyżej jedną iskrę (ECU-IGN-005) | Model usterek bramki; test T-IGN-005 z wymuszonym stanem wysokim i zamrożonym zegarem | G1, G2 | ✅ | ❌ | ❌ | A04, A05 |
| **O-005** | **Elektryczny punkt odniesienia VR nie wynika z geometrii wypustu.** Kąt odniesienia przyjęto z krawędzi mechanicznej 30° przed GMP; zbocze używane przez MCU powstaje w kondycjonerze i nie musi wypadać pod tym kątem | Równoczesny pomiar pozycji wału, analogowego VR i COUT przy rozruchu i w pełnym zakresie obrotów, z niezależnym odniesieniem GMP | G1, przegląd C.1 | ❌ | ❌ | ❌ | A06, Z13 |
| **O-006** | **Limit wyprzedzenia 28° bez budżetu wykonalności.** Margines 2° od odniesienia to 33,3 µs przy 10 000 obr/min, a sam czas wyłączenia drivera to 25 µs w jednym punkcie pracy. Po korekcie znacznika VR cały limit może wymagać zmiany | Budżet od znacznika do rzeczywistej iskry z kompensacją i rozrzutem w funkcji obrotów, napięcia, prądu i temperatury | G1, G3 | ❌ | ❌ | ❌ | A09 |
| **O-007** | **Bezwzględna granica błędu kąta.** **Rozstrzygnięte 25.10.2026 (decyzje Pawła):** +1° / −2° w 100 % zapłonów poza rozruchem (ECU-IGN-022); iskra nigdy przed zboczem natarcia — strukturalnie (ECU-IGN-023); w ROZRUCHU iskra na krawędzi spływu bez prognozy (ECU-IGN-019, odwraca C.1.8); reakcja: usterka wykonania od 1. zdarzenia, błąd prognozy przy 3/100 (ECU-IGN-024). Osiągalność +1° w dolnym zakresie obrotów zależy od modelu O-008 | Model błędu O-008; testy T-IGN-022…024 | **G0** | ✅ | ❌ | ❌ | A08 |
| **O-008** | **Model błędu synchronizacji nieodtwarzalny.** Podano 0,20°, 0,05°, 0,02° i starzenie estymaty 5,3% bez równań, profilu przyspieszenia i niepewności pomiaru | Udokumentowany model z jednostkami i parametrami; raport błędów w rozruchu, przy pulsacji momentu, odciążeniu i nagłej zmianie obrotów | G1, G3 | ❌ | ❌ | ❌ | A07 |
| **O-009** | **Rozruch, ruch wsteczny i odzysk synchronizacji.** Jeden wypust nie daje informacji o prędkości i kierunku po pierwszym zboczu. Nieobsłużone: odbicie wału, cofnięcie przy kompresji, kickback, zatrzymanie w wypuście. Okna bramkowania ±10°/±20° przyjęto bez danych o zakłóceniach. **Nowy scenariusz negatywny (25.10.2026):** przy iskrze na krawędzi spływu w rozruchu (ECU-IGN-019) **cofnięcie wału przy nieudanym kopnięciu** zamienia kolejność krawędzi — „drugie” zbocze wypada wtedy w pozycji 30° przed GMP przy ruchu wstecznym. Firmware musi rozpoznać kierunek albo zablokować iskrę, zanim ECU-IGN-019 zostanie zaimplementowane; dane: zapis kopnięcia z cofnięciem w sesji pomiarowej | Stany UNSYNC/ACQUIRE/SYNC z warunkami dopuszczenia ładowania i iskry; rejestr pierwszych iskier dla startów z różnych pozycji. **Brak nieplanowanej iskry jako osobne kryterium** | zamknięcie C, G3 | ❌ | ❌ | ❌ | A11, A12 |
| **O-010** | **Początek ładowania wymagał osobnej predykcji — NIEAKTUALNE 25.10.2026.** W AC-CDI kondensator ładuje się biernie z uzwojenia wzbudzającego; firmware nie steruje początkiem ładowania. Pozostała kwestia okna, w którym kondensator jest naładowany, jest w Z14 | — | — | — | — | — | A10 |
| **O-011** | **Energia iskry i metoda odcięcia w ograniczniku (przeredagowane 25.10.2026 pod AC-CDI).** Dwell od napięcia i flaga prądu dotyczyły zapłonu indukcyjnego — nieaktualne. Zostaje: energia iskry względem fabrycznego CDI (ECU-IGN-025) i rozróżnianie uszkodzeń cewki, przewodu WN i świecy. Ogranicznik w CDI = pominięcie impulsu bramki, bez skutku termicznego | Pomiar napięcia kondensatora w zakresie obrotów; próby z obciążeniem otwartym, zwartym i częściowo uszkodzonym | zamknięcie C, G2 | 🟡 | ❌ | ❌ | A13, A19, Z2 |

---

## 2. Bezpieczeństwo

| ID | Pozycja | Dowód zamknięcia | Bramka | D | M | W | Pochodzenie |
|---|---|---|---|---|---|---|---|
| **O-012** | **Watchdog musi potwierdzać zdrowie funkcji, nie samo życie procesora.** Przerwanie lub timer mogą obsługiwać WDI przy martwej logice zapłonu. Przy FTTI rzędu milisekund okno 100 ms nie jest ochroną toru zapłonu — to 16,7 obrotu wału przy 10 000 obr/min | Obsługa WDI po sprawdzeniu postępu funkcji krytycznych; całkowity czas wykrycia i wygaszenia; awaria każdego zadania osobno przy działających przerwaniach | G1, G3 | ❌ | ❌ | ❌ | A14 |
| **O-013** | **Okno watchdoga 100 ms kontra tryb uśpienia.** W trybie Stop zasilony watchdog resetowałby śpiący procesor, a jego programowe wyłączanie tworzyłoby stan „silnik pracuje, nadzór wyłączony”. **Rozstrzygnięte 18.10.2026 (decyzja Pawła):** w uśpieniu szyny wyłączane przez INH TJA1043 — watchdog jest zasilany zawsze, gdy zasilany jest procesor, bez programowego wyłącznika (ECU-SAF-017, `produkt.md` rozdz. 6) | Schemat zgodny z ECU-SAF-017; test: procesor zasilony ⇒ watchdog aktywny w każdym stanie, łącznie ze startem | **G0**, G1 | ✅ | ❌ | ❌ | L44 |
| **O-014** | **Zatrzask K4 przy uszkodzonym pomiarze obrotów.** Odblokowanie wymaga zatrzymania wału, a jedną z przyczyn K4 jest utrata sygnału obrotów. Brak impulsów może znaczyć stojący wał albo obracający się wał z uszkodzonym czujnikiem. Zatrzask w RAM może przepaść przy resecie | Rozdzielenie potwierdzonego zera od braku wiarygodnego pomiaru; procedura ponownego uzbrojenia nieoparta na domniemanym zerze; trwałość blokady po każdym rodzaju resetu | G1, G3 | ❌ | ❌ | ❌ | A15 |
| **O-015** | **Kill switch — pełna analiza usterek i wspólnych przyczyn.** Jeden próg nie rozróżnia przerwy, zwarcia do masy i zwarcia do zasilania. Rezystor lub zasilanie wspólne dla MCU, ADC i komparatora tworzą wspólną przyczynę awarii. Komparator nie został wybrany | Tabela każdego uszkodzenia przewodu, przycisku, rezystora i zasilania; dobór logiki do tej tabeli; reakcja na uszkodzenie samego komparatora; pomiar czasu reakcji | G2, G3 | 🟡 | ❌ | ❌ | A16, R12, L1 |
| **O-016** | **Analiza zagrożeń zamkniętej listy zatrzymań — wykonana 25.10.2026** (`firmware.md` B.1.2): 7 zatrzymań MVP-A z zagrożeniem, mechanizmem, czasem i fałszywym zadziałaniem; uszkodzenia elementów wykonawczych. Wynik: dwie luki zamknięte decyzjami Pawła — test obu ścieżek kill switcha (ECU-SAF-021) i drugi klucz rozrusznika (ECU-SAF-022) | Niezależny przegląd ludzki analizy (O-057); testy wstrzykiwania T-SAF-* | **G0**, G1 | ✅ | ❌ | ❌ | A17 |
| **O-017** | **Brak zdefiniowanego stanu bezpiecznego per wyjście wykonawcze**, z polaryzacją i stanem przy braku zasilania | Tabela: wyjście → stan bezpieczny → sposób jego wymuszenia → zachowanie przy braku zasilania | G1 | ❌ | ❌ | ❌ | L42 |
| **O-018** | **Brak analizy niezależności i wspólnych przyczyn awarii** dla mechanizmów opisanych jako niezależne od firmware | Dla każdego mechanizmu: zasób współdzielony, zakres pokrycia, usterki jawnie nieobjęte | G1 | ❌ | ❌ | ❌ | L43 |
| **O-019** | **Aktualizacja musi mieć fizycznie rozbrojone wyjścia.** **Rozstrzygnięte 25.10.2026:** aktualizacja tylko przy kill switchu w STOP — zapłon i rozrusznik (nowe ECU-SAF-019) blokowane sprzętowo przez cały czas aktualizacji (ECU-BTL-001, -002). Zerowa liczba impulsów VR nie jest samodzielnym warunkiem | Pomiar wyjść od startu bootloadera do startu aplikacji bez nieplanowanego impulsu (T-BTL-002) | **G0**, G1 | ✅ | ❌ | ❌ | A23 |
| **O-020** | **Live tuning bez TPS.** Wymaganie zapisane 18.10.2026 w ECU-SAF-011. Decyzja podjęta 12.10.2026: blokada aktywacji zmian przy pracującym lub uzbrojonym silniku, edycja w buforze, aktywacja po rozbrojeniu i jawnej komendzie; osobny tryb stanowiskowy z fizycznym zezwoleniem definiowany od razu | Wymaganie z warunkami rozbrojenia; testy prób zapisu i aktywacji przy ruchu wału, utracie VR i zerwaniu komunikacji | **G0**, zamknięcie C | ✅ | ❌ | ❌ | A21, R1, ECU-SAF-011 |
| **O-021** | **Mapa wymaga atomowej aktywacji i granicy niezależnej od siebie samej.** Edycja mapy nie może zmieniać granicy, która ma chronić przed błędną edycją. Zmiana mapy w środku zdarzenia zapłonu może rozdzielić decyzję o początku i końcu ładowania | Zweryfikowany profil dopuszczalnych nastaw osobno od mapy; aktywacja kompletnego zestawu w określonym punkcie cyklu, z jednym właścicielem wersji na impuls | punkt D, G3 | ❌ | ❌ | ❌ | A22 |

---

## 3. Zasilanie i termika

| ID | Pozycja | Dowód zamknięcia | Bramka | D | M | W | Pochodzenie |
|---|---|---|---|---|---|---|---|
| **O-022** | **Obwiednia napięciowa i ochrona wejścia.** **Ustalone 18.10.2026 (decyzje Pawła):** obwiednia w `produkt.md` rozdz. 13.1 — regulator AKM6000/SH721AA (jednofazowy bocznikowy), akumulator kwasowy zawsze podłączony; 18 V ciągle, −14 V / 60 s, zrzut ograniczony 35 V / 400 ms (wstępnie), impulsy ISO 7637-2 dla 12 V, 24 V poza zakresem, zapad 4,5 V akceptowany. Nowe SYS-ENV-008, -009, -010. TVS dwukierunkowy, elementy wejściowe ≥ 40 V | Pomiar napięcia jałowego uzwojenia ładującego i tętnień; dobór i obliczenie energii TVS; progi nadzoru napięcia i kolejność uruchamiania szyn w schemacie | **G0**, G1 | ✅ | 🟡 | ❌ | A25, R2 |
| **O-023** | **Bilans uśpienia.** Architektura Stop dawała ~117–187 µA przy limicie 150 µA. **18.10.2026 (decyzja Pawła): szyny wyłączane przez INH TJA1043** — bilans z listy elementów zasilanych z akumulatora w uśpieniu **≤ 63 µA** (ECU) i **≤ 60 µA** (HMI), w tym przydziały dla elementów niewybranych (`produkt.md` rozdz. 6.1, 8.1). Driver VBG08H-E (5 mA w standby) wypadł razem z zapłonem indukcyjnym | Dobór przetwornic, TVS i PROFET w granicach przydziałów; pomiar T-PWR-001 i T-PWR-002 na prototypie | **G0**, G2 | ✅ | 🟡 | ❌ | A26, A27, R9, Z11 |
| **O-024** | **Scenariusze startu i wybudzania.** **Rozstrzygnięte 18.10.2026 (decyzje Pawła):** start przyciskiem z uśpienia budzi i — przy przycisku trzymanym do gotowości ≤ 200 ms — kręci (ECU-SAF-018); kopnięcie i popych przy uśpionym ECU wymagają najpierw przycisku (ograniczenie do instrukcji); pełna praca bez HMI (SYS-COM-008); po podłączeniu akumulatora zachowanie wg Z15 (`produkt.md` rozdz. 6.3) | Implementacja sekwencji w FW (A.4); próby: rozruch po długim postoju, bez HMI, ze słabym akumulatorem (7 V), z przyciskiem puszczonym przed gotowością | **G0**, G1 | ✅ | ❌ | ❌ | A28 |
| **O-025** | **Pomiary ratiometryczne potrzebują niezależnego nadzoru szyny.** Użycie uszkodzonej szyny jako odniesienia do badania jej samej może ukryć awarię | Dla każdego wejścia ADC: domena, referencja, dzielnik, tolerancje, filtr, ochrona. Nadzór krytycznej szyny na niezależnym odniesieniu | G1, G2 | ❌ | ❌ | ❌ | A37 |
| **O-026** | **Odprowadzanie ciepła z ECU.** Po usunięciu VBG08H-E straty MVP-A **~2,1 W** (rozdz. 9.2, przebudowa 25.10.2026), w tym blok CDI ≤ 1,5 W — szacunek. Przy 85 °C otoczenia: ~91 °C wewnątrz przy dobrym kontakcie termicznym, ~102 °C przy złym (Z17) | Pomiar strat bloku CDI; pomiar temperatur w komorze +85 °C (A8) i w jeździe (ECU-SAF-020) | G3 | 🟡 | 🟡 | ❌ | R14, L16 |

---

## 4. Komponenty, złącze, HMI

| ID | Pozycja | Dowód zamknięcia | Bramka | D | M | W | Pochodzenie |
|---|---|---|---|---|---|---|---|
| **O-027** | **Akcelerometr zamiast BMI090L.** **Decyzje Pawła 25.10.2026:** sam akcelerometr (bez żyroskopu — wrażliwość na drgania, wywrotka to kąt grawitacji); **ST AIS2IH** (AEC-Q100, ±16 g, −40…+115 °C), zapasowy Murata SCA3300-D01-1; reguła wywrotki z bramką ważności kąta 0,8–1,2 g (ECU-SAF-005). Warunek: Z17 | Arkusz kwalifikacji AIS2IH w Fazie 4; analiza termiczna po pomiarze bloku CDI (Z17); testy fałszywej wywrotki przy przechyle, skoku, drganiach i awarii transmisji | G2 przed zakupem | ✅ | ❌ | ❌ | A31, A32 |
| **O-063** | **ZAPLANOWANE, nie przeoczenie — Faza 4, przy projektowaniu PCB** (decyzja Pawła 13.10.2026). Pełne numery katalogowe i arkusze kwalifikacji powstają wtedy, gdy dobierany jest każdy element pod schemat, nie wcześniej. Dotyczy: **W25Q64** (rodzina, nie numer; wersja standardowa klasy przemysłowej), **TJA1043, BTS7008-2EPA, TPS3430-Q1, MLX90316**, złącze Molex CMC, obie przetwornice, komparator kill switcha, przełącznik obciążenia. **Dwa wyjątki rozstrzygnięte wcześniej (25.10.2026), bo SYS-ENV-003b dyskwalifikowało poprzednie układy:** akcelerometr AIS2IH (O-027) i czujnik ciśnienia **Infineon KP464** (zamiast BMP390) | Arkusz kwalifikacji dla każdej pozycji wg zasady #18: pełny numer, status cyklu życia z datą i źródłem, kwalifikacja cytowana z dokumentu producenta, zakres temperatury wobec SYS-ENV-003b, pobór w każdym trybie, polaryzacja i stan domyślny każdego pinu sterującego, zachowanie przy zaniku szyn, limity ochron z warunkami pomiaru, trzy rzeczy, których układ nie robi | **Faza 4**, G2 przed zakupem | ✅ | ❌ | ❌ | A33 |
| **O-028** | **Bilans MCU wymaga macierzy funkcji alternatywnych.** Sama liczba pinów nie dowodzi możliwości jednoczesnego użycia HRTIM, capture, ADC, CAN, USB i DMA. Rewizja krzemu zmienia obowiązujące obejścia | Konfiguracja pinów i peryferiów potwierdzona narzędziem producenta + przegląd erraty dla użytej rewizji | G2 | ❌ | ❌ | ❌ | A33 |
| **O-029** | **Kanał rozrusznika — nieokreślone obciążenie.** Nie ustalono, czy kanał zasila silnik rozrusznika, czy cewkę fabrycznego przekaźnika. To dwa zupełnie różne obciążenia, a limit zwarciowy drivera nie jest dopuszczalnym prądem roboczym | Schemat obciążenia, pomiar prądu i energii przy wyłączeniu, próba sklejonego przekaźnika, przycisk przytrzymany przez reset | G1, G2 | ❌ | ❌ | ❌ | A34 |
| **O-030** | **Złącze i wiązka wymagają bilansu obwodów.** Wybrano Molex CMC 28-obwodowe bez potwierdzonych wymiarów; bilans 55 sygnałów dotyczył pinów procesora, nie obwodów zewnętrznych. Prąd i temperatura ograniczają liczbę jednocześnie obciążonych styków | Rzeczywisty pinout wiązki MVP-A, przekroje, zabezpieczenia, kluczowanie, obciążalność z deratingiem; potwierdzenie przestrzeni montażowej przed zamrożeniem PCB | G2 | ❌ | ❌ | ❌ | A35, R3 |
| **O-031** | **Czujnik biegu — wykonalność mechaniczna na Becie.** Rozwiązanie odwzorowane z KTM 4T; brak konstrukcji mocowania, magnesu i uszczelnienia. Modyfikacja pokrywy może ingerować w motocykl bardziej niż odrzucony TPS. Pozycja między biegami nie dowodzi zazębienia | Rysunek mechaniczny i ocena montażu bez ingerencji w funkcję skrzyni; kalibracja N i biegów; stan niejednoznaczny rozdzielony od neutralnego. **Wskazanie nie może być interlockiem bezpieczeństwa bez osobnego dowodu** | G1, G2 | ❌ | ❌ | ❌ | A36, R6, Z9 |
| **O-032** | **Typ czujnika prędkości koła.** Założono pasywny; czujnik aktywny wymaga dodatkowego pinu | Pomiar na motocyklu | G2 | ❌ | ❌ | ❌ | R4, Z8 |
| **O-033** | **MAX9926 — jedno źródło zaopatrzenia i niezdefiniowana polityka.** Układ niedostępny w TME. Zapis „jedyne źródło spoza UE" wymaga definicji: kraj dystrybutora, producenta, wytwarzania i montażu to różne kryteria | Definicja polityki, potem ocena BOM wobec niej | G2 | ❌ | ❌ | ❌ | R17 |
| **O-034** | **Termika i czytelność wyświetlacza.** Analiza daje 76 °C przy dopuszczalnych 70 °C dla modułu, bez podanej metody wyznaczenia. Wyłączenie podświetlenia może nie obniżyć temperatury od promieniowania słonecznego. Jasność katalogowa nie dowodzi czytelności przez osłonę. **To ryzyko architektoniczne, nie próba terenowa** | Bilans cieplny od słońca i elektroniki; ocena obudowy, koloru i osłony; funkcje ECU przy utracie HMI; test termiczny reprezentatywnej konstrukcji | G1, G2, potwierdzenie G5 | ❌ | ❌ | ❌ | A29, R15, R8 |
| **O-035** | **Drabinka przycisków bez analizy najgorszego przypadku.** Tolerancje, wilgoć, drgania i kilka naciśniętych przycisków mogą dać napięcie zgodne z inną komendą. Odbiór starego ekranu lub opóźnionego CAN nie może wyglądać jak stan aktualny | Rozłączne przedziały z marginesem i stanem nieprawidłowym; świeża jednoznaczna czynność dla komend istotnych; oznaczanie danych nieaktualnych | G1, G2 | ❌ | ❌ | ❌ | A30 |
| **O-036** | Liczba warstw PCB nieustalona — wpływa na koszt i EMI | Decyzja przy projekcie PCB | G2 | ❌ | ❌ | ❌ | L17 |
| **O-037** | Powłoka ochronna PCB — do rozważenia mimo obudowy IP67, z powodu kondensacji | Decyzja przy projekcie PCB | G2 | ❌ | ❌ | ❌ | L18 |
| **O-038** | Punkty testowe do diagnostyki produkcyjnej i znakowanie seryjne płytek | Decyzja przy projekcie PCB | G2 | ❌ | ❌ | ❌ | L19, L20 |
| **O-039** | **EMC musi wejść do projektu przed PCB.** Tor zapłonu, zasilanie, masy i wiązka silnie się sprzęgają. Cyfrowa symulacja idealnych impulsów nie odtwarza napięć wspólnych ani sprzężeń od iskry. Późne wykrycie nieodpornego wejścia VR wymusi zmianę PCB | Rozdział mas mocy i czujników, odprowadzanie energii zakłóceń, filtry, ochrona wejść, topologia wiązki — przed PCB. Stanowisko uzupełnione o analogowy VR i obciążenia indukcyjne | G1, G2, potwierdzenie G4 | ❌ | ❌ | ❌ | A38, R2 |

---

## 5. Firmware, dane, komunikacja

| ID | Pozycja | Dowód zamknięcia | Bramka | D | M | W | Pochodzenie |
|---|---|---|---|---|---|---|---|
| **O-040** | **Bootloader.** **Wymagania zapisane 25.10.2026 (decyzje Pawła): ECU-BTL-001…006** — warunki dopuszczenia, sprzętowe rozbrojenie, dwa banki, CRC-32 bez podpisu, potwierdzenie sprawności z powrotem po 3 startach, bootloader nieaktualizowalny | Projekt po podziale pamięci (punkt D); testy T-BTL-001…006 | **G0** | ✅ | ❌ | ❌ | L31, R18, A23 |
| **O-041** | **Odporność aktualizacji i konfiguracji na zanik zasilania.** Sprawne ECU może zostać unieruchomione przerwaniem aktualizacji. Suma kontrolna wykrywa uszkodzenie, ale nie dostarcza poprawnego obrazu; dwubankowa pamięć nie gwarantuje poprawnego powrotu | Schemat aktualizacji i odzyskiwania z kontrolą integralności i zgodności obrazu, ochroną bootloadera i atomowymi rekordami konfiguracji; przerywanie zasilania na każdym etapie | punkt H, G3 | ❌ | ❌ | ❌ | A24 |
| **O-042** | **Czarna skrzynka bez bilansu zapisu.** 17 minut zapisu z 8 MB to ~7,8 kB/s przed narzutem; nie określono rekordów, częstotliwości, zużycia pamięci ani zachowania po zaniku zasilania. Zapis po wypadku może nie istnieć, jeśli zdarzenie odłączy akumulator | Format, rezerwa, bufor pierścieniowy, atomowy znacznik zdarzenia, zasady nadpisywania; realistyczne okno po zdarzeniu albo jawna akceptacja jego braku | punkt F, G3 | ❌ | ❌ | ❌ | A39, ECU-LOG-006 |
| **O-043** | **Protokoły CAN i USB — semantyka komend przed formatem transportu.** Wersjonowanie `major.minor.patch` nie definiuje jednostek, kolejności bajtów, świeżości, własności sesji ani rozstrzygania powtórzeń. Poprawna suma kontrolna nie chroni przed składniowo poprawną komendą o błędnym znaczeniu | Specyfikacja operacji, roli i blokad po stronie ECU; transakcje, potwierdzenia, idempotencja, timeouty. **Blokady w ECU nie mogą zależeć od interfejsu aplikacji** | Faza 2-Desktop | ❌ | ❌ | ❌ | A40, F-010, SYS-COM-004 |
| **O-044** | **Szyna 5 V jest klasyfikowana jako utrata sygnału obciążenia.** To pozostałość po warianie z wtryskiem; w MVP-A mapa zależy tylko od obrotów. Spadek 5 V może jednocześnie zakłócić kondycjoner VR, czujnik biegu i inne pomiary, więc cofnięcie zapłonu nie dowodzi, że informacja o kącie jest wiarygodna | Przeniesienie przypadku do awarii domeny zasilania; dla każdego zakresu napięcia wskazanie, które elementy pracują w gwarantowanych warunkach | zamknięcie B i C | ❌ | ❌ | ❌ | A18 |
| **O-045** | **Mapa awaryjna „na bogato" jest niezweryfikowaną koncepcją.** Dotyczy wyłącznie wariantów B/C; stała dawka pełnego obciążenia przy małym dopływie powietrza może prowadzić do zalewania. W MVP-A dawkę podaje gaźnik, więc strategia nie jest funkcją tego wariantu | Oznaczenie jako koncepcji poza baseline MVP-A; walidacja składu mieszanki dopiero przy specyfikacji B/C | bramki B/C | ❌ | ❌ | ❌ | A20 |
| **O-060** | **Niezależny sygnał obciążenia dla wariantów TPI/TBI.** Przy utracie TPS ECU zostaje bez informacji o obciążeniu; fabryczny system KTM ma czujnik ciśnienia w skrzyni korbowej. Po usunięciu quickshiftera zwolniły się dwa piny, więc luka ma miejsce w złączu | Rozstrzygnięcie przy projektowaniu wariantu B/C, razem z ponownym bilansem pinów | bramki B/C | ❌ | ❌ | ❌ | L33 |
| **O-061** | **Parametry sterowania wtryskiwaczami TPI/TBI.** Rezystancja znana z internetu, nie z pomiaru; czas martwy i prąd podtrzymania niezmierzone | Pomiar na fizycznym wtryskiwaczu | G3, warianty B/C | ❌ | ❌ | ❌ | R5, Z6, F-014 |
| **O-062** | **Czujnik fazy wałka rozrządu w silnikach 4T** — brak potwierdzenia, czy występuje w jednocylindrowych enduro. Wniosek z rozumowania, nie z dokumentacji serwisowej | Dokumentacja serwisowa albo oględziny | poza MVP-A | ❌ | ❌ | ❌ | R10 |

---

## 6. Środowisko pracy

| ID | Pozycja | Dowód zamknięcia | Bramka | D | M | W | Pochodzenie |
|---|---|---|---|---|---|---|---|
| **O-046** | **Obwiednia temperaturowa — decyzja podjęta 13.10.2026, dowód otwarty.** Korekta mojego wcześniejszego ustalenia: wymaganie **istniało** (SYS-ENV-003), ale miało wartość −20…+60 °C, nierealną dla ECU przy silniku dwusuwowym latem i sprzeczną z klasą komponentów −40 °C; rozdział o obudowach podawał z kolei −20…+85 °C, czyli **drugą, inną liczbę**. Przyjęte: ECU **−40…+85 °C**, HMI **−20…+70 °C** (ograniczone panelem), przechowywanie **−40…+105 °C**, plus **SYS-ENV-003b** wiążące klasę komponentu z temperaturą wewnątrz obudowy i marginesem 15 °C. **Skutek: BMP390 (85 °C) jest tym wymaganiem zdyskwalifikowany w obecnej roli, podobnie jak IMU** | Wymagania wyprowadzone ze struktury ISO 16750-4: miejsce montażu, dopuszczalne temperatury, cykle, wilgotność, szczelność | **G0**, G2 | ❌ | ❌ | ❌ | L41, A49 |
| **O-047** | **Brak profilu odporności na wibracje i udary.** **Plan ustalony 25.10.2026 (decyzje Pawła):** ECU montowane pod siedzeniem przy airboxie; pomiar drgań silnika zestawem z docelowym AIS2IH (STEVAL-MKI218V1 + STEVAL-MKI109D, 1600 Hz) i udarów w jeździe iPhone/phyphox (~100 Hz) — `measurements/pomiar-drgan.md`. Profil: obwiednia ISO 16750-3 pokrywająca oba pomiary z zapasem | Profile wyprowadzone ze struktury ISO 16750-3, z wartościami uzasadnionymi pomiarem w miejscu montażu; potwierdzenie braku nasycenia ±16 g | **G0**, G2 | ✅ | ❌ | ❌ | SYS-ENV-006, A49 |

---

## 7. Proces

| ID | Pozycja | Dowód zamknięcia | Bramka | D | M | W | Pochodzenie |
|---|---|---|---|---|---|---|---|
| **O-048** | **Repozytorium i odtwarzalny baseline.** Mechanizm wdrożony 13.10.2026 — repozytorium z pierwszym commitem i tagiem `baseline-2026-10-13` | Odtworzenie pełnego pakietu dokumentów z repozytorium i działająca kopia poza środowiskiem pracy | przed G0 | ✅ | ✅ | ❌ | L34, A41 |
| **O-049** | **Standard kodowania, analiza statyczna i progi pokrycia testami.** Ustalony jest obowiązek, nie treść: nie wybrano standardu, narzędzia, progów ani sposobu walidacji narzędzi budowania | Konfiguracja analizy statycznej uruchamiana przy każdej zmianie, kryterium wyniku, odtwarzalny build z przypiętą wersją narzędzi | przed pierwszym firmware | ✅ | ❌ | ❌ | L36, A42 |
| **O-050** | **Kryteria akceptacji wyrobu A1–A15** — **zatwierdzone przez Pawła 25.10.2026, kryterium po kryterium** (`proces.md` rozdz. 4). Zmiany: A6 bez rewizji, A8 mierzalne (komora + logi), A10 z przerwaną aktualizacją, nowe A14 (rozruch przy 7 V, ≤ 5 kopnięć) i A15 (zero fałszywych wywrotek na hopach). A4 uzupełnione o granicę z O-007 | Mapowanie na wymagania kompletne; A4 uzupełnione po O-007 | **G0** | ✅ | ✅ | ❌ | L37, A42 |
| **O-051** | **Budżet i wyposażenie pomiarowe.** **Ustalone 25.10.2026:** budżet i zakupy prowadzi Paweł; jedna iteracja PCB z pełnym przeglądem przed zamówieniem; plan przyrządów z niezależnym odniesieniem kąta (symulator VR na Nucleo) i niezależnym narzędziem CAN — `proces.md` rozdz. 5.1. Przyjęte luki: −40 °C bez pomiaru, EMC bez laboratorium | Przyrządy dostępne przed Fazą 6; symulator VR zbudowany i sprawdzony | **G0**, G2 | ✅ | ❌ | ❌ | L30, L38, R16, A47 |
| **O-052** | **Brak przypadków użycia i wymagań niefunkcjonalnych aplikacji desktop.** Jedyne wymaganie dotyczy transakcyjności zapisu | Przypadki użycia przed projektem protokołu; wymagania wersji systemu, instalacji, wydajności i obsługi błędów | Faza 2-Desktop | ❌ | ❌ | ❌ | L39, A40 |
| **O-053** | **Warianty B i C nie mają zakresu ani odbiorcy jako wyroby.** Nie mają też motocykli odniesienia — podane wcześniej były zmyślone i trafiły do dossier audytowego (korekta 15.10.2026). Oba są jednocylindrowymi 2T na tej samej platformie KTM/Husqvarna/GasGas, więc ich tor zapłonu jest **jednym pytaniem, nie dwoma** | Minimalny kontrakt rezerw wspólnego sprzętu teraz; pełny zakres po zamknięciu MVP-A | po MVP-A | 🟡 | ❌ | ❌ | L40 |
| **O-054** | **Lista blokująca G0 zawierała wymagania wariantów B/C** (parametry wtrysku), przez co bramka mogła stać się niemożliwa do zamknięcia w deklarowanej kolejności. **Wykonane 18.10.2026:** wymagania wtrysku i TPS oznaczone **[B/C]**; skrypt kontrolny liczy je osobno i nie wlicza do G0 | Baseline MVP-A z jawnie wyłączonymi B/C; lista G0 zawierająca wyłącznie pozycje tego wariantu | **G0** | ✅ | ✅ | ✅ | A43 |
| **O-055** | **Pokrycie 105/105 opisuje istniejące identyfikatory, nie kompletność wyrobu.** Funkcje bez wymagań: bootloader, wentylator, przełączanie map, przebieg, korekta wysokości, RTC, konfigurator wyglądu | Pokrycie prowadzone od każdej funkcji wyrobu i każdego zagrożenia do wymagania, osobno od pokrycia identyfikatorów | **G0**, każda bramka | ❌ | 🟡 | ❌ | A44 |
| **O-056** | **Egzekwowanie zasad przeciw udokumentowanym wzorcom błędów.** Zasady istniały, a wzorce nawracały — w tym przy naprawie błędu tego samego typu | Mechanizm wdrożony 13.10.2026 jako instrukcja robocza stosowana automatycznie. Dowód: próba wprowadzenia nieudokumentowanego parametru zatrzymuje propozycję | G0, G1 | ✅ | ✅ | ❌ | A45 |
| **O-057** | **Brak niezależnego przeglądu ludzkiego.** Oba audyty i cała dokumentacja powstały jako analiza wspierana modelem językowym. Inny model znajduje błędy, ale nie zastępuje drugiego inżyniera | Imienny zapis przeglądu toru energii, odcięcia i synchronizacji, z rozstrzygniętymi uwagami; autor, zatwierdzający i recenzent rozdzieleni | **przed PCB** | ✅ | ❌ | ❌ | L45, A46 |
| **O-058** | **Wymagania bez ustalonej wartości.** 18.10.2026: 11 wartości zatwierdzonych przez Pawła, ECU-IGN-003/004 wycofane (AC-CDI), 4 wymagania przeniesione do B/C. **Zostają SYS-ENV-006** — zamykane w O-047 — **i ECU-IGN-027** (od 25.10.2026, odstępy izolacyjne z pomiaru, O-001). Lista generowana przez `scripts/kontrola.py` | Zamknięcie wszystkich albo jawne przeniesienie do wariantów B/C | **G0** | ✅ | 🟡 | ❌ | DOC-002 |
| **O-059** | **Liczniki w dokumentach rozjechały się z rejestrami**, bo były wpisywane ręcznie. Dokumenty podawały 51 kodów usterek i 107 testów przy rzeczywistych 49 i 99 | Mechanizm wdrożony 13.10.2026: `scripts/kontrola.py`. Dowód: uruchamianie przy każdej zmianie | przed wydaniem | ✅ | ✅ | ❌ | A50 |

---

## 8. Założenia

Twierdzenia przyjęte bez weryfikacji, na których zbudowano inne ustalenia. **Założenie obalone nie jest usuwane** — zostaje razem z listą tego, co przez nie trzeba było poprawić.

Rejestracji podlegają także **wnioski** wyciągnięte z takich twierdzeń: każda decyzja wykluczająca jakąś opcję musi zapisać, co zostawia. Z12 jest przykładem wniosku, który nigdy nie został wypowiedziany.

| # | Założenie | Co się zawali, jeśli fałszywe | Potwierdzenie | Stan |
|---|---|---|---|---|
| **Z1** | ~~Beta 300 RR 2015 ma czujnik położenia przepustnicy~~ | Mapa 2D, strategia zastępcza przy utracie TPS, interlock oparty na obciążeniu, pin w złączu | Oględziny | ❌ **OBALONE 11.10.2026** — motocykl nie ma TPS i nie będzie dokładany. Skutki skorygowane w 7 zapisach. **Korekta 13.10.2026: kod usterki DTC-SEN-04 nie został usunięty** — obowiązuje w wariantach B/C, gdzie czujnik istnieje; opisanie go jako usuniętego było nieścisłością |
| **Z2** | ~~Czas ładowania cewki wynosi ok. 3 ms~~ — ❌ **OBALONE 15.10.2026**: zapłon nie jest indukcyjny, więc pojęcie czasu ładowania cewki w tej architekturze nie występuje. Pierwotny zapis: | Analiza termiczna, tabela startu ładowania, wniosek o obudowie aluminiowej, **wybór rejestru okresu HRTIM jako sufitu — zakres timera to 1,54 ms** | Pomiar na docelowej cewce | ❌ **OBALONE 15.10.2026** — zapłon nie jest indukcyjny |
| **Z3** | Kickstarter obraca wał kilkakrotnie w jednym ruchu nogi | ECU-IGN-019 — iskra od drugiego przejścia wypustu. Przy jednym obrocie silnik nie odpali | Policzenie obrotów koła przy kopnięciu | 🟡 Niepotwierdzone |
| **Z4** | Wyprzedzenie zapłonu dwusuwu 300 mieści się w 0–25° przed GMP | Limit geometryczny 28° (ECU-IGN-015) | Pomiar fabrycznej krzywej wyprzedzenia | 🟡 Niepotwierdzone |
| **Z5** | Szczelina 0,18 mm jest wartością fabryczną, nie stanem tego egzemplarza | Oszacowanie amplitudy VR i dobór obwodu wejściowego | Instrukcja serwisowa albo drugi egzemplarz | 🟡 Niepotwierdzone |
| **Z6** | Wtryskiwacze KTM TPI/TBI mają 11,7 Ω nominalnie | Dobór TLE9104SH i tryb nasycony zamiast peak-and-hold | Pomiar na wtryskiwaczu | 🟡 Niepotwierdzone |
| **Z7** | Stator Bety oddaje 150–200 W | Budżet energetyczny i wniosek, że szczyt 151 W się domyka | Instrukcja serwisowa albo pomiar | 🟡 Niepotwierdzone |
| **Z8** | Czujnik prędkości koła jest pasywny | Bilans pinów złącza | Pomiar na motocyklu | 🟡 Niepotwierdzone |
| **Z9** | Czop bębna zmiany biegów jest dostępny w 2T tak jak w 4T | Wskaźnik biegu | Oględziny | 🟡 Niepotwierdzone |
| **Z10** | Dwusuw pali co obrót, więc jeden wypust wystarcza i nie trzeba rozpoznawać fazy | Cała architektura triggera; brak czujnika wałka | Zasada działania silnika | 🟢 Potwierdzone rozumowaniem |
| **Z11** | Sprawność przetwornic przy obciążeniu rzędu dziesiątek µA wynosi ok. 60% | Cały przeliczony bilans uśpienia | Karta wybranej przetwornicy, potem pomiar | 🟡 Niepotwierdzone |
| **Z12** | ~~Beta ma zapłon indukcyjny~~ | Dobór VBG08H-E, architektura dwell, analiza termiczna, Z2, obudowa aluminiowa | Triaż wykonany 15.10.2026 | ❌ **OBALONE** — pomiar w `measurements/wynik-triazu-zaplonu.md`. Zapłon jest **AC-CDI** — osobne uzwojenie wzbudzające w statorze, sterownik Kokusan CU7542 z zasilaniem logiki 12 V. Topologia przyjęta dla MVP-A (O-001) |
| **Z13** | Offset między krawędzią mechaniczną wypustu a zboczem z kondycjonera jest stały w funkcji obrotów | Jedna stała kalibracyjna zamiast krzywej korekcyjnej; dokładność kąta w całym zakresie | Pomiar przy kilku prędkościach | 🟡 Niepotwierdzone |
| **Z14** | Uzwojenie wzbudzające naładuje kondensator zapłonowy przed każdą iskrą w całym zakresie wyprzedzenia naszej mapy, od kopnięcia do 10 000 obr/min | Decyzja AC-CDI (O-001), zakres wyprzedzenia mapy, rozruch kopnięciem przy słabym akumulatorze (ECU-IGN-021). Wniosek z tego, że układ fabryczny działa — przy fabrycznej krzywej wyprzedzenia, nie przy naszej | Oscyloskop: przebieg wzbudzającego względem GMP przy kopnięciu, biegu jałowym i wysokich obrotach | 🟡 Niepotwierdzone |
| **Z15** | Po pierwszym podłączeniu akumulatora TJA1043 wchodzi w Standby z aktywnym INH, czyli ECU startuje samo — karta i AH1014 tego nie opisują, przedstawiciel NXP na forum podaje odwrotnie (Sleep) | Opis zachowania po podłączeniu akumulatora w instrukcji. **Oba wyniki są bezpieczne** — przy Sleep ECU czeka na przycisk | Prototyp: podłączenie zasilania, obserwacja INH | 🟡 Niepotwierdzone |
| **Z16** | Niesterowane piny STB_N i EN (procesor w resecie lub przed konfiguracją portów) dają tryb Standby z aktywnym INH — wniosek z prądu wejściowego 1–10 µA w stanie wysokim (wewnętrzne ściąganie w dół), którego karta nie opisuje wprost. Schematy NXP nie mają zewnętrznych rezystorów | Brak zewnętrznych ściągnięć STB_N/EN (decyzja 18.10.2026). Jeśli fałszywe: reset procesora może wyłączyć zasilanie ECU przy pracującym silniku | Prototyp: procesor trzymany w resecie przy pracy z zasilacza — INH musi zostać aktywne; próba przy −40 °C i +85 °C | 🟡 Niepotwierdzone |
| **Z17** | Temperatura w miejscu akcelerometru AIS2IH przy 85 °C otoczenia nie przekracza **100 °C** (115 °C z karty minus 15 °C marginesu SYS-ENV-003b). Szacunek: straty ECU bez VBG08H-E ~0,7 W + blok CDI ≤ 1,5 W (nieznany do pomiaru) → przyrost ~7 °C przy obudowie aluminiowej z dobrym kontaktem (~3 K/W) | Dobór AIS2IH (O-027). Jeśli fałszywe: zamiana na SCA3300-D01-1 albo przeniesienie czujnika w chłodniejsze miejsce PCB | Analiza termiczna po pomiarze uzwojenia wzbudzającego (straty bloku CDI) + pomiar temperatury na prototypie w komorze | 🟡 Niepotwierdzone |

---

## 9. Ryzyka zaakceptowane świadomie

Nie są pozycjami otwartymi — decyzja zapadła, ryzyko resztkowe przyjęte. Zapisane, żeby nie wracały jako „przeoczenia".

| Pozycja | Decyzja | Uzasadnienie |
|---|---|---|
| **Brak blokady rozrusznika na biegu** | Odpowiedzialność po stronie kierowcy, jak w części motocykli sportowych. Wymaga ostrzeżenia w instrukcji | Czujnik sprzęgła jako warunek rozruchu mógłby przy awarii przełącznika unieruchomić motocykl w terenie. Audyt nie narzuca powrotu blokady, ale wymaga opisania przypadków: przycisk przytrzymany przez reset, sklejony przekaźnik, zachowanie po wybudzeniu — to jest objęte O-029 |
| **Firmware bez podpisu cyfrowego** | Weryfikacja obrazu tylko sumą kontrolną CRC-32 (ECU-BTL-004) — decyzja Pawła 25.10.2026 | Wykrywa uszkodzenie obrazu, nie wykrywa podmiany: każdy z dostępem do USB może wgrać własny firmware sterujący zapłonem. Przyjęte jako właściwość produktu dla entuzjastów; ochrona przed fizycznym skutkiem złego firmware pozostaje sprzętowa (kill switch, ECU-SAF-001, -019) |
| **Brak automatycznego ograniczenia mocy przy przegrzaniu silnika** | Tylko ostrzeżenie na HMI; decyzja o zatrzymaniu należy do kierowcy | W zawodach automatyczna redukcja mocy może być groźniejsza od przegrzania |
| **Brak sygnalizacji stanu na samym ECU** | Diagnostyka wyłącznie przez HMI i aplikację | — |
| **HMI wygasza dane przy utracie komunikacji** | Komunikat o błędzie, żadna wartość nie jest wyświetlana | Zamrożony odczyt wprowadza w błąd silniej niż brak odczytu |
| **Testy z silnikiem dopiero po bramkach stanowiskowych** | Aktywna integracja po G3 | Zmodyfikowane po audycie: **pasywna charakterystyka fabrycznego motocykla jest dopuszczona od razu** i jest teraz pozycją o najwyższym priorytecie (O-001) |

---

## 10. Co wypadło z rejestrów

Dla porządku, żeby nikt nie szukał: **pozycje zamknięte nie są tu prowadzone.** Pełne uzasadnienia 36 pozycji pierwszego audytu i diagnoza wzorców błędów wraz z triażem 50 pozycji drugiego audytu zostały w dokumentacji przed konsolidacją, na gałęzi `Old-docs` tego repozytorium — ta gałąź jest kopią bezpieczeństwa i nie jest rozwijana. Historię zmian każdego dokumentu nosi repozytorium.

Z 162 identyfikatorów w pięciu rejestrach zostało **63 pozycje otwarte i 13 założeń**. Różnica to zamknięcia i duplikaty: ta sama rzecz występowała jednocześnie jako luka, ryzyko i pozycja w dwóch audytach, pod czterema numerami.
