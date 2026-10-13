# Specyfikacja FW — Faza 3: Prototyp funkcjonalny

| | |
|---|---|
| **Identyfikator** | DOC-007 |
| **Wersja** | 0.1 |
| **Status** | **NIEAKTUALNY** — do napisania od nowa po zamknięciu Fazy 2-FW |
| **Właściciel** | Paweł |
| **Opracowanie** | Claude |
| **Data wersji** | 2026-08-31 |
| **Dokument nadrzędny** | `proces-rozwoju-ecu.md` (DOC-001) |

**Historia zmian**

| Wersja | Data | Zakres zmiany |
|---|---|---|
| 0.1 | ≤ 2026-08-30 | Utworzenie — przed zmianą struktury procesu |
| — | 2026-08-31 | Oznaczony jako nieaktualny (powody niżej); treść zachowana wyłącznie jako materiał źródłowy |

---


> ⚠️ **DOKUMENT NIEAKTUALNY (2026-08-31).**
>
> Powstał przed zmianą struktury procesu i zawiera założenia, które już nie obowiązują:
> - opisuje testy na prawdziwym motocyklu (Krok 2 i 3) — obecny proces dopuszcza kontakt z motocyklem **dopiero w Fazie 8**, na wyprodukowanym PCB
> - zakłada wyłącznie sterowanie zapłonem 1 cylindra — zakres Fazy 3 obejmuje teraz również wtrysk, czujniki, CAN i HMI
> - mapowanie pinów i architektura modułów pochodzą sprzed decyzji o architekturze uśpienia B, komparatorze i innych zmianach
>
> **Zostanie napisany od nowa po zamknięciu Fazy 2-FW**, na podstawie `faza2-fw-specyfikacja.md`.
> Zachowany wyłącznie jako zapis wcześniejszych ustaleń (logika zapłonu i tabela wyprzedzenia pozostają merytorycznie aktualne).

---

## Cel i zakres

Potwierdzić na sprzęcie deweloperskim, że firmware potrafi: odczytać sygnał pozycji wału korbowego, obliczyć aktualne obroty (RPM), wyznaczyć kąt wyprzedzenia zapłonu z mapy, i wyzwolić impuls zapłonowy w precyzyjnie obliczonym momencie.

**Poza zakresem Fazy 3** (dochodzi w Fazie 5): wtrysk, PROFET/wyjścia pomocnicze, CAN do HMI, USB do desktopu, IMU/czarna skrzynka, logowanie do flash. To wszystko zaprojektowane w architekturze (Faza 1-2), ale nieimplementowane jeszcze na tym etapie — najpierw dowodzimy, że rdzeń czasu rzeczywistego działa poprawnie.

## Platforma

**NUCLEO-G474RE** (STM32G474RET6, Cortex-M4F, 170MHz) — **to już docelowy mikrokontroler produkcyjny**, nie tymczasowe zastępstwo. Ten sam numer katalogowy trafi na finalne PCB w Fazie 4.

Podział zadań między peryferiami:
- **Dekodowanie sygnału wejściowego (crank signal, Pin B):** standardowy timer (TIM2, 32-bit) w trybie Input Capture — częstotliwość sygnału z czujnika obrotów jest wystarczająco niska, że standardowy timer daje w pełni wystarczającą precyzję pomiaru.
- **Generowanie sygnału zapłonu (Pin C) i w przyszłości wtrysku:** **HRTIM** (High Resolution Timer) — unikalne peryferium G4 z rozdzielczością <1ns, właśnie po to wybrane w Fazie 1/2. To już finalna implementacja, nie tymczasowe obejście jak było przy F411.

**Uwaga do implementacji (Claude Code):** dokładne przypisanie pinów do kanałów HRTIM (który TIMx: A-F, która linia wyjściowa) do zweryfikowania wprost w dokumentacji STM32G474 (RM0440) i pinout NUCLEO-G474RE podczas pisania kodu — nie zgaduję tego na tym etapie, żeby nie podać błędnego przypisania.

## Architektura modułowa

```
┌─────────────────────────────────────────────────┐
│                   main.c (pętla główna)           │
│         inicjalizacja, UART debug, stan systemu   │
└─────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ trigger_decoder  │  │ ignition_sched   │  │ ignition_timer_hal│
│ (ISR na wejściu  │─▶│ (obliczenie kąta │─▶│ (Output Compare, │
│  crank signal)   │  │  wyprzedzenia,   │  │  wyzwolenie pinu  │
│                   │  │  RPM, dwell)     │  │  do drivera coil) │
└─────────────────┘  └──────────────────┘  └──────────────────┘
```

### 1. `trigger_decoder` — dekodowanie sygnału obrotów

- Wejście: pojedynczy impuls na obrót (na starcie — najprostszy schemat, 1 ząb/magnes na kole zamachowym), obsługiwany przez przerwanie zewnętrzne (EXTI) w trybie Input Capture na timerze.
- Dla każdego zbocza: zapisz znacznik czasu (timer counter), oblicz okres między kolejnymi impulsami → **RPM = 60 / okres_w_sekundach** (przy 1 impulsie/obrót).
- Filtr odrzucający impulsy szumowe (odrzuć jeśli okres < 90% poprzedniego — typowe dla zakłóceń VR przy niskich obrotach).
- **Uwaga projektowa:** docelowy schemat produkcyjny (Faza 5) będzie prawdopodobnie wymagał koła z wieloma zębami (np. missing-tooth wheel) dla precyzyjniejszego określania kąta w cyklu, nie tylko RPM. Na Fazie 3 upraszczamy do 1 impulsu/obrót, żeby zweryfikować podstawowy mechanizm szeregowania zapłonu — punkt odniesienia kątowego (offset względem TDC) ustawiany na sztywno w kodzie na czas testów.

### 2. `ignition_scheduler` — logika zapłonu

- Tablica wyprzedzenia zapłonu: prosta mapa 1D (RPM → kąt wyprzedzenia w stopniach przed TDC), np. 10 punktów, interpolacja liniowa między nimi. Wartości startowe konserwatywne (niskie wyprzedzenie), do korekty przy realnych testach.
- Obliczenie **dwell time** (czas ładowania cewki) — na starcie wartość stała (np. 3ms), docelowo mapa zależna od napięcia akumulatora (kompensacja).
- Na podstawie aktualnego RPM i ostatniego znacznika czasu z `trigger_decoder`: oblicz moment (w tickach timera) kiedy ma nastąpić zapłon, zaprogramuj Output Compare.

### 3. `ignition_timer_hal` — warstwa sprzętowa

- Interfejs: `ignition_timer_schedule_spark(uint32_t timestamp_ticks)`, `ignition_timer_schedule_dwell_start(uint32_t timestamp_ticks)`.
- Implementacja: HRTIM, przerwanie/zdarzenie porównania wyzwala wyjście do drivera zapłonu (na start testu: prosty tranzystor NPN + cewka testowa lub bezpośrednio moduł ewaluacyjny VBG08H-E, jeśli dostępny na tym etapie).
- Interfejs funkcyjny zaprojektowany niezależnie od konkretnego peryferium — ułatwia ewentualne przyszłe zmiany bez przepisywania reszty kodu, ale to już finalna implementacja docelowa, nie tymczasowe obejście.

### 4. Bezpieczeństwo — na tym etapie

- **Ogranicznik obrotów awaryjny** (twardy rev limiter w kodzie, nie mapa) — odcięcie zapłonu powyżej ustalonego progu (np. 12 000 RPM), niezależnie od docelowej mapy — zabezpieczenie na wypadek błędu w kalkulacji przy pierwszych testach na silniku.
- Watchdog sprzętowy (IWDG) — reset MCU jeśli pętla główna się zawiesi, zapłon domyślnie wyłączony po resecie.

## Plan testów (kolejność)

**Krok 1 — Test na jednej płytce (bez silnika, bez drugiego urządzenia).**

Wykorzystujemy dwa niezależne piny na tej samej płytce NUCLEO-G474RE:

- **Pin A (wyjście, "udawany" sygnał koła):** osobny, prosty fragment kodu generuje regularne impulsy (włącz/wyłącz) ze stałym odstępem czasu — symuluje to, co w prawdziwym silniku wysyła czujnik na kole zamachowym. Zmieniając odstęp czasu między impulsami, symulujemy różne obroty silnika (RPM).
- **Pin B (wejście, prawdziwa logika zapłonu):** to właśnie ten pin, który w docelowym systemie ma nasłuchiwać prawdziwego czujnika. Łączymy go z Pinem A zwykłym przewodem (jumperem) — program na płytce nie odróżnia sygnału sztucznego od prawdziwego.
- Testowana logika (`trigger_decoder` + `ignition_scheduler`) odbiera sygnał na Pinie B, oblicza RPM i moment zapłonu, po czym wyzwala **Pin C (wyjście do drivera zapłonu)**.

**Weryfikacja oscyloskopem:** jedna sonda na Pin A (sygnał wejściowy/"koło"), druga sonda na Pin C (obliczony moment zapłonu). Na ekranie widać dokładnie, czy zapłon następuje we właściwym miejscu względem impulsu wejściowego, przy różnych symulowanych RPM. Nie jest potrzebna druga płytka ani zewnętrzny generator sygnału — wszystko dzieje się na jednym Nucleo.

**Krok 2 — Test na silniku bez zapłonu** (silnik obracany rozrusznikiem lub ręcznie, bez paliwa/iskry) — podłączamy realny czujnik z Bety 300RR do Pinu B zamiast sygnału sztucznego, potwierdzenie poprawnego odczytu RPM z rzeczywistego czujnika.

**Krok 3 — Pierwszy test z iskrą na silniku** — dopiero po potwierdzeniu kroków 1-2, z zachowawczą mapą wyprzedzenia.

## Mapowanie pinów (NUCLEO-G474RE)

| Sygnał | Peryferium | Uwaga |
|---|---|---|
| Pin A — wyjście, symulowany sygnał "koła" (tylko do testu z Kroku 1) | Dowolny GPIO z timerem ogólnego przeznaczenia (np. TIM3) | Do potwierdzenia konkretnego pinu przy implementacji |
| Pin B — wejście crank signal | TIM2 Input Capture | Standardowy timer, wystarczająca precyzja do pomiaru okresu |
| Pin C — wyjście do drivera zapłonu | HRTIM (kanał do ustalenia: TIMA-TIMF) | Finalna implementacja precyzyjnego timingu — **Claude Code potwierdza dokładny pin/kanał wg RM0440 i pinout NUCLEO-G474RE** |
| Debug UART | USART2 (przez wbudowany ST-LINK jako VCP) | Bez zmian względem wcześniejszego założenia |

**Do Kroku 1 testów:** połącz Pin A z Pinem B zwykłym przewodem (jumperem) — to jedyne fizyczne połączenie potrzebne na tym etapie.

## Do przygotowania przez Claude Code

1. Szkielet projektu (STM32CubeIDE lub CMake + STM32Cube HAL), konfiguracja zegara 170MHz (maksimum dla STM32G474).
2. Implementacja modułów: `trigger_decoder`, `ignition_scheduler`, `ignition_timer_hal`.
3. Prosty interfejs UART do logowania RPM/kąta wyprzedzenia na żywo (do obserwacji przez terminal).
4. Kod testowy do współpracy z generatorem sygnału (symulacja crank signal).
