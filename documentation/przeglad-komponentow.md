# Przegląd komponentów — dostępność, cykl życia, dopasowanie

| | |
|---|---|
| **Identyfikator** | DOC-005 |
| **Wersja** | **1.6** |
| **Status** | roboczy — stany magazynowe TME do potwierdzenia przez Pawła |
| **Właściciel** | Paweł |
| **Opracowanie** | Claude |
| **Data wersji** | 2026-09-12 |
| **Dokument nadrzędny** | `proces-rozwoju-ecu.md` (DOC-001) |

**Historia zmian**

| Wersja | Data | Zakres zmiany |
|---|---|---|
| 1.0 | 2026-09-12 | Utworzenie: przegląd cyklu życia i dopasowania funkcjonalnego komponentów po wprowadzeniu zasady procesu #10 (TME → Mouser → Farnell → DigiKey, pełny OPN, aktywny status) |

---


⚠️ **Zakres weryfikacji:** sprawdziłem status cyklu życia i dopasowanie funkcjonalne dla części komponentów. **Stanów magazynowych TME nie potwierdziłem dla żadnego** — to wymaga sprawdzenia przez Ciebie bezpośrednio w katalogu TME.

---

## 1. Zweryfikowane — wykryte problemy

| Komponent | Problem | Działanie |
|---|---|---|
| **STM32G474RET6** | 🔴 **Zakres pracy -40…+85°C**, nie 125°C. Nasza analiza termiczna daje 58°C przy obudowie aluminiowej z dobrym kontaktem (OK), ale 87°C przy gorszym kontakcie — **poza specyfikacją**. Dokładnie pozycja audytu F-019 | **Zmiana na STM32G474RET3** (-40…+125°C, sufiks T3 zamiast T6). Status aktywny wg ST. Ten sam układ, inna klasa temperaturowa |
| **TLE8104E** | 🔴 **Status NRND** | Odrzucony, zastąpiony przez TLE9104SH (opisane w planie naprawczym rozdz. 10) |
| **BMI088** | 🟡 **Nie jest kwalifikowany AEC-Q100.** Bosch pozycjonuje go do dronów i robotyki, nie do motoryzacji. Mój wcześniejszy opis „automotive-grade" był nieuprawniony | Rozważyć **BMI090L** — automotive'owy odpowiednik Boscha z tej samej rodziny. Do sprawdzenia dostępność i cena |
| **BMP390** | 🟡 Czujnik ciśnienia klasy konsumenckiej/przemysłowej, **bez kwalifikacji automotive** | Zweryfikować zakres temperatur wobec naszych 58-87°C wewnątrz obudowy. Rozważyć alternatywę automotive |
| **W25Q64** | 🟡 Standardowa wersja Winbonda to klasa przemysłowa. Podałem też **niepełny numer** — „W25Q64" to rodzina, nie numer katalogowy | Ustalić pełny OPN i zweryfikować klasę temperaturową. Winbond ma warianty o rozszerzonym zakresie |

---

## 2. Zweryfikowane — bez zastrzeżeń

| Komponent | Pełny OPN | Status | Uwagi |
|---|---|---|---|
| **MAX9926** | MAX9926UAEE/V+ | ✅ Production | QSOP-16, -40…+125°C, automotive. **Uwaga:** to wersja dwukanałowa. Jednokanałowy odpowiednik MAX9924 jest mniejszy (10-pin) i tańszy — drugi kanał ma sens tylko jeśli czujnik fazy 4T okaże się typu VR |
| **VBG08H-E** | VBG08H-E / **VBG08HTR-E** (taśma) | ✅ Aktywny | -40…+175°C, OctaPAK. Dostępny w eStore ST, Newark, LCSC. Do produkcji wersja TR |
| **TLE9104SH** | TLE9104SHXUMA1 | ✅ Aktywny, AEC-Q100/101 | Opisany w planie naprawczym rozdz. 10 |

---

## 3. Niezweryfikowane — do sprawdzenia

Dla każdego brakuje: potwierdzenia statusu cyklu życia, pełnego numeru katalogowego, stanu magazynowego TME.

| Komponent | Co wymaga sprawdzenia |
|---|---|
| **TJA1043** | Pełny OPN (warianty obudowy), status. Dodatkowo audyt F-003 wymaga analizy domen VBAT/VCC/VIO — zadanie 1.5 |
| **BTS7008-2EPA** | Pełny OPN, status, dostępność ×3 sztuki |
| **LM5164-Q1** | Pełny OPN, status. Uwaga: przy przeprojektowaniu zasilania (zadanie 1.5) topologia może się zmienić i ten układ może zostać zastąpiony |
| **NCV8705** | Pełny OPN (wersja napięciowa), status, potwierdzenie AEC-Q100. Również objęty przeprojektowaniem zasilania |
| **TPS3430-Q1** | Pełny OPN, status, dostępność |
| **MLX90316** | Pełny OPN (warianty analog/PWM/SPI), status. Audyt F-026: to nie jest gotowy czujnik, tylko układ scalony wymagający magnesu i konstrukcji mechanicznej |
| **STM32G0B1** | Pełny OPN i **klasa temperaturowa** — prawdopodobnie ten sam problem T6/T3 co w G474 |
| **Riverdi RVT35HHBFWN00** | Status, zakres temperatur pracy panelu (istotne wobec analizy termicznej HMI: 76°C przy obudowie aluminiowej) |
| **Molex CMC 28** | Pełny OPN dla wersji do wlutowania w PCB i wersji na wiązkę, dostępność, wymiary |
| **Deutsch DTM04-4P / DTM04-3P** | Pełne OPN wtyków, gniazd, styków i uszczelek |
| **TMP112-Q1** (czujnik temp. HMI) | Propozycja robocza, niezweryfikowana |

---

## 4. Wnioski

**Powtarza się jeden wzorzec błędu:** opisywałem komponenty jako „automotive-grade" na podstawie zastosowania lub producenta, bez sprawdzenia kwalifikacji. Dotyczyło to BMI088, częściowo BMP390 i W25Q64, a wcześniej doprowadziło do błędu z L9960.

**Nawrót wzorca 20.09.2026 — MAX9926.** Zaproponowałem zmianę topologii zasilania opartą na założeniu, że układ ma wejście shutdown. Nie ma go, a pobór wynosi 4,7 mA typowo. Błąd wyłapał Paweł pytaniem, czy ten układ nie był za przełącznikiem właśnie z powodu wysokiego poboru w spoczynku. Dwie okoliczności obciążające: **wniosek był już zapisany** w rozdz. 6.4 dokumentu procesu, a propozycja i tak powstała; oraz dotyczyła zmiany w schemacie, czyli najdroższej kategorii pomyłek. **Wniosek procesowy: żadna propozycja zmiany sprzętowej nie jest przedstawiana Pawłowi przed sprawdzeniem karty katalogowej parametru, na którym się opiera** — nawet gdy zmiana wydaje się oczywistą poprawą.

**Zasada na przyszłość:** określenie „automotive" wymaga potwierdzenia kwalifikacji AEC-Q100 (układy scalone) lub AEC-Q200 (elementy bierne) w dokumentacji producenta. Sam fakt, że producent sprzedaje komponenty do motoryzacji, nie czyni konkretnego układu kwalifikowanym.

**Trzy zmiany wymagające decyzji:**
1. STM32G474RET6 → **STM32G474RET3** (temperatura) — rekomendacja jednoznaczna
2. BMI088 → **BMI090L** (kwalifikacja automotive) — do rozważenia wobec kosztu
3. MAX9926 → **MAX9924** (jeśli rezygnujemy z drugiego kanału VR) — do rozważenia wobec przyszłego czujnika fazy 4T


---

## 5. Decyzje podjęte (12.09.2026)

| Komponent | Było | Jest | Powód |
|---|---|---|---|
| Mikrokontroler ECU | STM32G474RET6 | **STM32G474RET3** | Zakres -40…+125°C zamiast -40…+85°C (audyt F-019) |
| IMU | BMI088 | **BMI090L** | Kwalifikacja AEC-Q100 |
| Driver wtryskiwaczy | L9960 → TLE8104E | **TLE9104SHXUMA1** | L9960 = błędna klasa układu; TLE8104E = status NRND |
| Kondycjoner VR | MAX9926 (bez OPN) | **MAX9926UAEE/V+** | Pełny numer, wariant motoryzacyjny. Pozostajemy przy wersji dwukanałowej — rezerwa pod czujnik fazy 4T |

**Rozważone i odrzucone:**
- **MAX9924** (jednokanałowy, tańszy) — odrzucony na rzecz rezerwy drugiego kanału
- **Front-end dyskretny + komparator w STM32** — odrzucony: przenosi ciężar na projekt i walidację, co przy audycie wytykającym braki analizy najgorszego przypadku byłoby ruchem w złą stronę
- **Przejście na czujniki Halla zamiast VR** — odrzucone: fabryczne czujniki w tych silnikach to cewki pickup zintegrowane ze stojanem. Rezygnacja z VR oznaczałaby wymianę czujnika przy każdej instalacji, zmieniając produkt z wymiany sterownika na przebudowę układu zapłonowego. Hall pozostaje jako alternatywna ścieżka (zworka na PCB)

## 6. Pozostaje do sprawdzenia przez Pawła

Stany magazynowe i pełne numery katalogowe w kolejności TME → Mouser → Farnell → DigiKey dla wszystkich pozycji z rozdziału 3, oraz:
- **MAX9926UAEE/V+** — dostępność i cena wariantu `/V` wobec standardowego (różni je kwalifikacja procesu, nie parametry elektryczne)
- **TLE9104SHXUMA1** — stan magazynowy
- **BMI090L** — dostępność i cena wobec BMI088
- **STM32G474RET3** — dostępność wariantu T3 (rzadziej magazynowany niż T6)

---

## 7. Weryfikacja bezpośrednia w STM32CubeMX (20.09.2026)

Sprawdzone w selektorze MCU zainstalowanego STM32CubeMX, nie z katalogu dystrybutora:

| Pozycja | Ustalenie |
|---|---|
| **STM32G474VET3** | Status marketingowy **Active**. Warianty w bazie: VET3, VET3TR, VET6, VET6TR — wszystkie Active. Obudowa LQFP100 14×14×1,4 mm, 512 kB Flash, 128 kB RAM, 170 MHz |
| Budżet pinów | Nowy projekt na tym układzie startuje z **86 wolnymi GPIO** wobec 55 sygnałów z bilansu pinów (plan naprawczy rozdz. 12) — margines większy niż zakładany |
| **VBG08H-E** | Karta katalogowa potwierdza wyjście diagnostyczne **C.F.** (pin 6, otwarty dren), próg prądu 6,5 A, ogranicznik 8,5–10,5 A, klamra 320–400 V, miękkie wyłączenie 150–175 °C złącza. Szczegóły i konsekwencje: `faza2-fw-specyfikacja.md` B.2.3 |

Stany magazynowe dystrybutorów nadal do potwierdzenia przez Pawła — CubeMX podaje status cyklu życia, nie dostępność.

---

## 8. Do potwierdzenia w kartach katalogowych (20.09.2026)

| Komponent | Co potwierdzić | Dlaczego to blokuje |
|---|---|---|
| **MAX9926UAEE/V+** | ~~Pobór w trybie SHDN~~ — **ustalone 20.09.2026, pozycja zamknięta** | Karta katalogowa: **brak wejścia shutdown**, pobór **4,7 mA typ. / 10 mA maks.** Układ musi być odcinany przełącznikiem obciążenia — propozycja zasilania go wprost z przetwornicy wycofana (spec. FW B.2.4) |
| **MAX9926UAEE/V+** | Czas ustalenia progu adaptacyjnego po załączeniu zasilania | Wchodzi w budżet 200 ms na gotowość do iskry (ECU-PWR-003); zakładane 1–2 ms wymaga potwierdzenia |
| **VBG08H-E** | Prąd cewki odpowiadający progowi C.F. przy docelowej cewce | Czas ładowania musi być na tyle długi, by prąd przekroczył 6,5 A — inaczej diagnostyka odczyta sprawną cewkę jako przerwaną (spec. FW B.2.3) |
| **Przełącznik obciążenia 5 V** | Ograniczanie prądu i czas narostu | Wykrycie niezaładowania po 5 ms (ECU-PWR-010) wymaga znajomości czasu narostu |
| **MAX9926UAEE/V+** | **Amplituda sygnału VR przy maksymalnych obrotach** | Zmierzona szczelina **0,18 mm** jest wyraźnie mniejsza niż typowe 0,3–1,0 mm, więc przy 10 000 obr/min amplituda może przekroczyć **100 V**, czyli górną granicę z ECU-SEN-001. Do pomiaru oscyloskopem na pracującym silniku; determinuje rezystor szeregowy i klamrę na wejściu (Faza 4) |
| **Wejście VR** | Dopasowanie do impedancji źródła **95,7 Ω** | Zmierzona rezystancja pick-upu Bety 300 RR; mieści się w fabrycznej specyfikacji 100 Ω ±20% |
| **Komparator kill switcha** | Pełny OPN, kwalifikacja AEC-Q100, dostępność w TME | Nowy element od 22.09.2026 (spec. FW B.2.5.1). Wymagania: próg ustawiany dzielnikiem, wyjście zdolne bramkować wejścia EN driverów, praca od chwili podania zasilania bez konfiguracji |
