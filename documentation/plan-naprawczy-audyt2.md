# Plan naprawczy po audycie AUD-ECU-002

## 0. Metryka dokumentu

| | |
|---|---|
| **Identyfikator** | DOC-011 |
| **Wersja** | 1.0 |
| **Status** | roboczy — do realizacji |
| **Właściciel** | Paweł |
| **Opracowanie** | Claude |
| **Data** | 2026-10-12 |
| **Dokument nadrzędny** | `proces-rozwoju-ecu.md` (DOC-001) |
| **Źródło** | Audyt AUD-ECU-002 v1.0 z 11.10.2026, 50 ustaleń (13×P0, 36×P1, 1×P2), werdykt **NO-GO** |
| **Poprzedni plan naprawczy** | `plan-naprawczy-audyt.md` (DOC-006) — pierwszy audyt, 36 pozycji. **Nie jest zastępowany** |

### 0.1 Historia zmian

| Wersja | Data | Zmiana | Powód |
|---|---|---|---|
| **1.0** | **2026-10-12** | Pierwsze wydanie. Diagnoza pięciu wzorców pomijania, pięć nowych zasad procesu, zakres zapożyczeń z branży automotive, przebudowany plan prac na 6 etapów, triaż wszystkich 50 ustaleń | Audyt AUD-ECU-002 i decyzja Pawła: wyciągnąć z audytu nie tylko poprawki, ale zmianę sposobu pracy |

---

## 1. Po co ten dokument

Audyt AUD-ECU-002 znalazł 50 pozycji. Gdybyśmy je po prostu odhaczyli, za miesiąc trzeci audyt znalazłby pięćdziesiąt następnych tego samego rodzaju. Dlatego ten dokument ma trzy części, a nie jedną:

1. **Dlaczego pomijamy rzeczy** (rozdz. 2) — pięć powtarzalnych wzorców, każdy z dowodem z naszej własnej historii błędów i z mechanizmem, który by go zatrzymał.
2. **Czego nowego się uczymy od branży** (rozdz. 3 i 4) — wybrane normy i techniki automotive tam, gdzie dają realną wartość, oraz jawna lista tego, czego **nie** bierzemy i dlaczego.
3. **Co konkretnie robimy i w jakiej kolejności** (rozdz. 5–7) — sześć etapów i triaż wszystkich 50 ustaleń.

**Czego ten dokument nie robi:** nie zamyka żadnej pozycji audytu. Zamknięcie wymaga dowodu, nie wpisu do tabeli — to jest jedno z ustaleń audytu i obowiązuje także wobec tego planu.

---

## 2. Diagnoza — dlaczego regularnie pomijamy istotne rzeczy

Nie jest to jeden błąd powtarzany wielokrotnie. To **pięć różnych wzorców**, każdy z własną przyczyną i każdy wymagający innego mechanizmu. Dopóki nie były rozdzielone, każda naprawa trafiała obok.

### 2.1 Wzorzec A — „układ należy do właściwej kategorii, więc nadaje się do zadania"

**Wystąpienia:** TLE8104E (zły typ drivera), L9960 (zła kategoria), BMI088 („automotive-grade" bez podstawy), **BMI090L** („odpowiednik z kwalifikacją motoryzacyjną" — nieprawda), TJA1043 (zachowanie przy zaniku VCC/VIO), MAX9926 (zaproponowane wejście shutdown, które nie istnieje), **VBG08H-E** (przyjęta polaryzacja EN odwrotna do rzeczywistej).

**Przyczyna.** Zasada #10 mówi „sprawdzić kartę katalogową", ale nie mówi **których parametrów**. W efekcie karta była czytana wybiórczo — ten fragment, który dotyczył bieżącego pytania. Przy MAX9926 przeczytałem pobór prądu i przeoczyłem brak pinu shutdown. Przy VBG08H-E przeczytałem wyjście diagnostyczne C.F. i ograniczanie prądu, a nie przeczytałem polaryzacji EN ani prądu standby — obu rzeczy, które dziś są pozycjami audytu.

**Najgorszy przypadek z tej grupy:** zmiana BMI088 → BMI090L była **naprawą błędu tego typu popełnioną tym samym błędem**. Uzasadnieniem zmiany był brak AEC-Q100 w BMI088; BMI090L też go nie ma.

**Mechanizm blokujący:** arkusz kwalifikacji komponentu o **stałym zestawie pól** — zasada #18 (rozdz. 3.1). Pole puste = komponent nie jest proponowany. Koszt: ok. 30–45 minut na komponent, jednorazowo.

### 2.2 Wzorzec B — „mechanizm istnieje, więc ochrona jest zapewniona"

**Wystąpienia:** rejestr okresu HRTIM jako sufit czasu ładowania (istnieje, kasuje wyjście, sprawdziłem w CubeMX — ale **zakres 16 bitów to 1,54 ms przy założonym dwell 3 ms**, i mechanizm zależy od tego samego zegara, który steruje zapłonem); rezystory ściągające jako stan bezpieczny (istnieją, polaryzacja odwrotna); wyjście C.F. drivera jako diagnostyka (istnieje, nie wykrywa zwartego IGBT — ten jeden wyłapaliśmy sami).

**Przyczyna.** Sprawdzaliśmy **istnienie** mechanizmu, nie jego **zakres** ani **niezależność**. To dokładnie ta klasa błędu, dla której branża automotive ma gotowe pojęcia — i dlatego je zapożyczamy (rozdz. 4).

**Mechanizm blokujący:** trzy obowiązkowe pytania do każdego mechanizmu ochronnego — zasada #19 (rozdz. 3.2). Koszt: kilka zdań na mechanizm, ale wymaga myślenia; to najdroższa z nowych zasad i najbardziej wartościowa.

### 2.3 Wzorzec C — „budżet to suma tego, co wypisałem"

**Wystąpienia:** bilans uśpienia (cztery pozycje; **brak MCU, brak drugiego transceivera, brak watchdoga, brak drivera zapłonu**, a suma czterech wypisanych wierszy i tak nie zgadza się z podaną sumą); bilans pinów (liczył piny MCU, nie obwody wiązki — audyt A35); analiza termiczna (zbudowana na niepotwierdzonym dwell 3 ms).

**Przyczyna.** Budżet powstawał z pamięci — wypisywałem to, co w danym momencie przychodziło do głowy, zamiast przejść listę wszystkich odbiorników z drzewa zasilania. Dodatkowo bilans był liczony **na szynie 3,3 V**, a wymaganie dotyczy **zacisków akumulatora**; to dwie różne liczby.

**Mechanizm blokujący:** budżet generowany z wyliczonej listy domen, z kontrolą pokrycia BOM — zasada #20 (rozdz. 3.3). Koszt: jednorazowo tabela domen, potem skrypt.

### 2.4 Wzorzec D — „kryterium zadziała wtedy, kiedy się tego spodziewam"

**Wystąpienia:** quickshifter przy użyciu sprzęgła, wskazanie biegu bez warunku sprzęgła, dwa kolejne kryteria wykrycia zwartego czujnika sprzęgła.

**Ten wzorzec jest już zablokowany** zasadami #14 (obowiązkowa analiza scenariuszy rzeczywistej jazdy + test negatywny) i #15 (kryteria automatycznego zadziałania to propozycja, nie ustalenie). Audyt go nie znalazł ponownie. Zasady zostają bez zmian — jedyne, czego brakuje, to **egzekwowanie** (A45), objęte zasadą #21.

### 2.5 Wzorzec E — „twierdzenie o świecie zapisane jako fakt"

**Wystąpienia:** obecność TPS (Z1, obalone), dwell 3 ms (Z2), obroty wału na kopnięcie (Z3), moc statora (Z7), rezystancja wtryskiwaczy (Z6).

**Rejestr założeń (L35) ten wzorzec zablokował** — wyłapał Z1 w pierwszej godzinie istnienia. Ale ma lukę, którą odsłonił audyt: **decyzja 2.1 brzmi „tylko motocykle z akumulatorem 12 V — eliminuje obsługę surowego AC ze statora (klasyczne CDI)".** Wykluczyliśmy CDI zasilane ze statora i po cichu wyciągnęliśmy wniosek, że zostaje zapłon indukcyjny. **DC-CDI to CDI zasilane z akumulatora** — klasa, której ta decyzja nie wyklucza. Wniosek nigdy nie został zapisany, więc nie było czego zakwestionować.

**Mechanizm blokujący:** rejestr założeń obejmuje **wnioski, nie tylko twierdzenia** — każda decyzja wykluczająca opcję musi zapisać, co zostawia (rozdz. 3.4). Koszt: jedno zdanie na decyzję.

### 2.6 Podsumowanie diagnozy

| Wzorzec | Co sprawdzaliśmy | Czego nie sprawdzaliśmy | Mechanizm |
|---|---|---|---|
| A | kategorię komponentu | konkretne parametry z karty | #18 arkusz kwalifikacji |
| B | istnienie mechanizmu | jego zakres i niezależność | #19 trzy pytania |
| C | sumę wypisanych pozycji | kompletność listy i punkt odniesienia | #20 budżet z domen |
| D | że mechanizm działa | że nie działa, kiedy nie powinien | #14, #15 (działa) |
| E | twierdzenia | wnioski wyciągnięte z twierdzeń | rozszerzenie L35 |

**Wspólny mianownik wszystkich pięciu:** sprawdzaliśmy to, o co właśnie zapytaliśmy, i nie sprawdzaliśmy tego, o co nie zapytaliśmy. Dlatego mechanizmy mają formę **stałych list pól i pytań** — ich sensem jest zadanie pytania, które samo by nie przyszło do głowy.

---

## 3. Nowe zasady procesu

Pełne brzmienie do wstawienia do DOC-001 rozdz. 2.

### 3.1 Zasada #18 — arkusz kwalifikacji komponentu

> **Żaden komponent inny niż bierny i nieistotny dla bezpieczeństwa nie jest proponowany bez wypełnionego arkusza kwalifikacji.** Arkusz ma stały zestaw pól; każde pole wymaga numeru strony karty katalogowej albo jawnego wpisu „karta nie podaje". **Pole puste oznacza, że komponent nie jest proponowany.**

Pola obowiązkowe:

| # | Pole | Dlaczego jest w arkuszu |
|---|---|---|
| 1 | Pełny numer zamówieniowy (OPN) | Rodzina ≠ układ. Wariant temperaturowy i obudowa są w sufiksie |
| 2 | Status cyklu życia + data + źródło | Zasada #10. NRND dyskwalifikuje |
| 3 | Kwalifikacja (AEC-Q100/101/200, grade) **cytowana z dokumentu producenta** | Pozycja BMI090L. Marketingowe „automotive-proven" nie jest kwalifikacją |
| 4 | Zakres temperatury pracy vs nasza obwiednia | Pozycja BMI090L: 85 °C w ECU bez zdefiniowanej obwiedni |
| 5 | Domeny zasilania i prąd **w każdym trybie, w tym standby** | Pozycja VBG08H-E: 5 mA standby niezależnie od stanu EN |
| 6 | **Każdy pin sterujący: polaryzacja i stan przy braku sterowania** | Pozycja VBG08H-E: EN aktywne niskim, wewnętrznie podciągnięte |
| 7 | Zachowanie przy zaniku każdej z szyn zasilających | Pozycja TJA1043 |
| 8 | Limity ochron i diagnostyki **wraz z warunkami pomiaru** | Pozycja VBG08H-E: 25 µs to wartość typowa w jednym punkcie pracy, nie najgorszy przypadek |
| 9 | Zakresy rejestrów / timerów vs nasze wymagania | Pozycja HRTIM: 1,54 ms wobec wymaganych 3 ms |
| 10 | **Trzy rzeczy, których ten układ nie robi** | Pozycja MAX9926 (brak shutdown) i C.F. (nie wykrywa zwartego IGBT) |
| 11 | Obudowa, footprint, dostępność u dostawcy w kolejności TME→Mouser→Farnell→DigiKey | Zasada #10 |

Pole 10 jest najważniejsze i najmniej naturalne. Pola 1–9 opisują, co układ robi; **pole 10 wymaga wypisania, czego nie robi**, i właśnie tam siedziały dwa z naszych błędów.

### 3.2 Zasada #19 — analiza mechanizmu ochronnego

> **Każdy mechanizm opisany jako ochrona, zabezpieczenie, limit, sufit lub stan bezpieczny wymaga pisemnej odpowiedzi na trzy pytania, zanim zostanie uznany za pokrywający jakiekolwiek zagrożenie.**

1. **Co dokładnie pokrywa, a czego nie** — lista usterek objętych i jawnie nieobjętych.
2. **Jaki ma zakres lub limit i czy obejmuje najgorszy przypadek** — z liczbami.
3. **Od jakiego zasobu współdzielonego zależy** — zegar, szyna zasilania, ten sam MCU, ten sam rezystor. Mechanizm zależny od tego samego zasobu co funkcja, którą chroni, **nie jest niezależny** i nie wolno go opisywać jako działającego przy awarii tej funkcji.

Rejestr okresu HRTIM przy tych trzech pytaniach odpadłby w pierwszej godzinie: pytanie 2 ujawnia zakres 1,54 ms, pytanie 3 ujawnia wspólny zegar.

### 3.3 Zasada #20 — budżety wyliczane, nie wypisywane

> **Każdy budżet (prądu, mocy, cieplny, pinów, pamięci, czasu) powstaje z wyliczonej listy wszystkich elementów z odpowiedniego rejestru — drzewa zasilania, BOM, listy sygnałów — a nie z listy pozycji wypisanych z pamięci. Budżet podaje jawnie punkt odniesienia, w którym obowiązuje wymaganie, i jest weryfikowany skryptem sprawdzającym, że każdy element rejestru występuje w budżecie albo ma wpis „nie dotyczy" z uzasadnieniem.**

### 3.4 Rozszerzenie rejestru założeń — wnioski podlegają rejestracji

> **Do rejestru założeń trafiają nie tylko twierdzenia przyjęte bez weryfikacji, ale także wnioski wyciągnięte z takich twierdzeń. Każda decyzja wykluczająca jakąś opcję musi zapisać, co po tym wykluczeniu zostaje w zakresie** — wniosek niezapisany nie podlega kwestionowaniu.

### 3.5 Zasada #21 — status trójstanowy i egzekwowanie

> **Pozycja rejestru luk, ryzyk lub audytu ma trzy niezależne statusy: decyzja przyjęta, mechanizm wdrożony, dowód zaakceptowany. Pozycja jest zamknięta dopiero wtedy, gdy wszystkie trzy są spełnione. Bramka nie przechodzi, gdy pozycja bezpieczeństwa ma zamkniętą decyzję i otwarty dowód.**

Zamiast obecnego ✅/🟡:

| Pozycja | Decyzja | Mechanizm | Dowód | Stan |
|---|---|---|---|---|
| L34 repozytorium | ✅ zasada #16 | ❌ nie istnieje | ❌ | **otwarte** |
| L35 rejestr założeń | ✅ | ✅ rozdz. 11.2 | ✅ wyłapał Z1 | **zamknięte** |
| L36 standard kodowania | ✅ zasada #17 | ❌ brak narzędzi i progów | ❌ | **otwarte** |
| L37 kryteria wyrobu | 🟡 propozycja A1–A12 | — | ❌ | **otwarte** |

To rozwiązuje sprzeczność z A41: oznaczyłem L34 jako zamknięte, opisując w tym samym dokumencie, że repozytorium nie istnieje. Dwa statusy były potrzebne, a był jeden.

### 3.6 Korekta zasady #5 — elementy bierne istotne dla bezpieczeństwa

Zasada #5 pozwalała mi samodzielnie dobierać wszystkie elementy bierne. **To było za szeroko** (A45). Rezystory drabinki kill switcha, kondensator ustawiający okno watchdoga, dzielniki wejść ADC, filtry wejścia VR i boczniki pomiarowe decydują o progach bezpieczeństwa i o oknie nadzoru.

> **Zasada #5 (skorygowana):** samodzielnie dobierane są elementy bierne **nieistotne dla bezpieczeństwa** — blokady zasilania, filtry sygnałów cyfrowych, podciągnięcia magistral. Element bierny, którego wartość ustala próg detekcji, okno czasowe, poziom logiczny wejścia bezpieczeństwa albo stan przy braku sterowania, podlega zasadzie #18 w zakresie pól 4, 6 i 11 oraz wymaga zatwierdzenia.

---

## 4. Co bierzemy z branży automotive, a czego nie

Decyzja Pawła z 12.10.2026: **czerpać z wiedzy normatywnej tam, gdzie daje realną wartość; nie wprowadzać zgodności na siłę.** Produkt jest jawnie niehomologowany, przeznaczony do motorsportu — nie powstaje safety case i nie przypisujemy poziomów ASIL.

### 4.1 Bierzemy

| Źródło | Co z niego bierzemy | Co nam zamyka | Koszt |
|---|---|---|---|
| **ISO 16750-2** (obciążenia elektryczne) | **Strukturę listy prób**: przepięcie, nakładający się przebieg AC, powolny i gwałtowny spadek napięcia, zachowanie przy resecie, profil rozruchu, zrzut obciążenia, odwrotna polaryzacja, przesunięcie masy, rozwarcie, zwarcie | **A25** — obwiednia napięciowa i wymagania ochrony wejścia | Zdobycie normy lub publikowanego streszczenia |
| **ISO 16750-4** (obciążenia klimatyczne) | Strukturę wymagań temperaturowych i wilgotnościowych, cykle termiczne, szczelność | **A49** — dziś **nie mamy żadnego wymagania na temperaturę pracy ECU**; SYS-ENV-001/002 to napięcia | jw. |
| **ISO 16750-3** (obciążenia mechaniczne) | Strukturę profili wibracji i udarów | **SYS-ENV-006** — profil wibracji, otwarty od Fazy 0 | jw. |
| **ISO 7637-2** (zaburzenia przewodzone) | Zestaw impulsów testowych na linii zasilania | **A25**, **A38** — konkretne wymaganie dla ochrony wejścia | jw. |
| **ISO 26262** — wyłącznie techniki analityczne | **Stan bezpieczny zdefiniowany per wyjście**; **FTTI** (dopuszczalny czas od usterki do zagrożenia); **analiza niezależności i wspólnej przyczyny awarii** | **A02, A03, A04, A14, A15, A16, A17, A37** — osiem pozycji, w tym pięć P0 | Myślenie, nie dokumentacja |
| **MISRA C:2012** w podzbiorze | Reguły istotne dla kodu sterującego czasem rzeczywistym: arytmetyka wskaźników, konwersje typów, zachowanie nieokreślone | **L36**, zasada #17 | Konfiguracja narzędzia |
| **AEC-Q100/101/200** | Filtr doboru, **rozszerzony na elementy bierne istotne dla bezpieczeństwa** | **A31, A32, A45**, zasada #5 | W arkuszu #18 |

**Ważne zastrzeżenie co do ISO 16750:** normy są pisane dla samochodów. **Zrzut obciążenia skaluje się z wydajnością alternatora** — stator 150–200 W daje zaburzenie o rząd wielkości mniejsze niż alternator samochodowy 1–2 kW. Bierzemy więc **strukturę listy prób i definicje zjawisk**, a **wartości wyprowadzamy z naszego układu** albo z pomiaru. Inaczej przepłacimy za ochronę wejścia zaprojektowaną pod zjawisko, które w tym motocyklu nie wystąpi.

Normy są płatne. Do etapu 3 potrzebujemy albo dostępu do nich, albo publikowanych streszczeń profili — do rozstrzygnięcia w etapie 0.

### 4.2 Nie bierzemy

| Czego nie bierzemy | Dlaczego |
|---|---|
| Pełnej zgodności z ISO 26262, przypisania ASIL, safety case, zestawu work-products | Koszt liczony w osobomiesiącach przy zespole jednoosobowym i produkcie niehomologowanym. **Wartość siedzi w technikach analitycznych, nie w dokumentacji zgodności** |
| FMEDA z metrykami sprzętowymi (SPFM/LFM/PMHF) | Wymaga baz danych intensywności uszkodzeń. Zostaje **struktura** analizy: usterka → skutek → mechanizm detekcji → reakcja, bez liczb, których nie mamy |
| Kwalifikacji narzędzi (ISO 26262-8) | Zamiast tego: przypięte wersje kompilatora i narzędzi oraz odtwarzalny build — potrzebne nam i tak z innych powodów |
| ASPICE, oceny dojrzałości procesu | Czysty narzut przy jednej osobie |
| Homologacji drogowej, znaku E | Jawnie poza zakresem produktu od Fazy 0 |

### 4.3 Narzędzia

| Zadanie | Narzędzie | Koszt |
|---|---|---|
| Repozytorium, baseline | git, znaczniki na bramkach, kopia poza środowiskiem pracy | 0 |
| Analiza statyczna | cppcheck (dodatek MISRA) + clang-tidy + `-Wall -Wextra -Werror` | 0 |
| Testy jednostkowe na hoście | Unity/Ceedling albo GoogleTest; wstrzykiwanie usterek przez podmianę warstwy HAL | 0 |
| Odtwarzalny build i kontrola przy każdej zmianie | Makefile z przypiętą wersją arm-gcc + CI (build, cppcheck, testy) | 0 |
| Traceability | Zostaje obecne rozwiązanie: tabela w markdown + skrypt kontrolny. **Działa i wyłapał już realny błąd** | 0 |
| FMEA, arkusze kwalifikacji, budżety domen | Arkusz kalkulacyjny w repozytorium | 0 |
| Pomiary (etap 2) | Oscyloskop, sonda prądowa, koło podziałowe, niezależne odniesienie GMP | do ustalenia |

---

## 5. Co nowe pojęcia dają od razu — przykład roboczy

Żeby nie zostawiać rozdz. 4 na poziomie deklaracji: zastosowanie **FTTI** do naszego toru zapłonu daje wniosek, którego nie mieliśmy, i porządkuje cztery pozycje audytu naraz.

FTTI to dopuszczalny czas od wystąpienia usterki do chwili, w której zagrożenie staje się realne. Jeśli czas reakcji mechanizmu ochronnego jest dłuższy od FTTI, **ten mechanizm nie chroni przed tym zagrożeniem**, niezależnie od tego, jak dobrze działa.

| Zagrożenie | FTTI | Czy watchdog ~100 ms wystarcza? |
|---|---|---|
| Iskra pod błędnym kątem z powodu błędnej komendy firmware | **zero** — zagrożeniem jest pojedynczy impuls, nie jego powtórzenie | **Nie, i żaden mechanizm reaktywny nie wystarczy** |
| Wyjście zablokowane w stanie aktywnym, cewka ładowana ciągle | rzędu maksymalnego dopuszczalnego czasu ładowania, czyli **jednostek milisekund** | **Nie** — 100 ms to 16,7 obrotu wału przy 10 000 obr/min |
| Iskra przy awaryjnym wygaszeniu energii z cewki | zero — skutkiem jest sama iskra pod przypadkowym kątem | **Nie dotyczy** — to nie jest problem czasu, a kolejności sterowania INP i EN |
| Zawieszenie zadania nadzorującego, silnik pracuje dalej | setki ms | **Tak** |

**Trzy wnioski, które z tego wynikają:**

1. **Dla błędów kąta pojedynczego impulsu nie istnieje ochrona reaktywna.** Zostaje wyłącznie zapobieganie: bramkowanie kątowe, walidacja mapy po stronie ECU, limit geometryczny niekonfigurowalny z mapy, oraz **ograniczenie tego, co stopień wyjściowy jest w stanie zrobić**. To unieważnia każdą architekturę opartą na „wykryj i zareaguj" dla tej klasy usterek.
2. **Sufit czasu ładowania musi być sprzętowy i niezależny od HRTIM.** Przy FTTI rzędu milisekund i wspólnym zegarze mechanizm w rejestrze okresu nie spełnia warunku niezależności (zasada #19, pytanie 3). Groźny podprzypadek jest jeden i konkretny: **zegar zatrzymuje się, gdy wyjście jest aktywne** — zamarznięty licznik nie skasuje wyjścia. Potrzebny jest monostabilny albo układ RC w ścieżce bramki. **To jest zmiana na płytce, czyli decyzja przed G2, nie w firmware.**
3. **Okno watchdoga 100 ms nie jest ochroną toru zapłonu** i nie wolno go tak opisywać. Jest ochroną przed zawieszeniem nadzoru. Pozycja A14 jest zatem nie tylko o tym, **jak** obsługiwać WDI, ale o tym, **przed czym** watchdog w ogóle chroni.

### 5.1 Sprzeczność, której nie znalazł ani audyt, ani my

TPS3430-Q1 ma okno programowane kondensatorem w zakresie 63 ms–77 s; przyjęliśmy **~100 ms** jako wymaganie wiążące. W trybie Stop MCU nie obsługuje WDI. Zatem albo nadzór jest w uśpieniu wyłączany — a karta ma wejście wyłączające, co audyt słusznie wskazuje jako zagrożenie („silnik nie może pracować z wyłączonym nadzorem") — albo MCU budzi się częściej niż co 100 ms, co niszczy bilans uśpienia. **Rozdział o uśpieniu nie wspomina watchdoga ani razu.** Okno jest ustalane kondensatorem, czyli na stałe w sprzęcie: **to jedna decyzja, podejmowana przed PCB, obejmująca naraz nadzór i uśpienie.**

### 5.2 Bilans uśpienia przeliczony na zaciskach akumulatora

Audyt słusznie zauważa, że prąd szyny 3,3 V nie jest prądem akumulatora, ale nie podaje kierunku przeliczenia. Przy 3,6-krotnym stosunku napięć przeliczenie **obniża** wkład MCU:

| Składnik | Na akumulatorze (typ) | Uwaga |
|---|---|---|
| STM32G474 Stop 1 (80,5 µA @ 3,3 V) | **~37 µA** | 266 µW przy sprawności ~60% → ~443 µW z 12 V. **Sprawność 60% jest moim założeniem → rejestr, Z11** |
| 2× prąd własny przetwornic | 20–50 µA | mierzony na ich wejściu |
| 2× TJA1043 standby | 60–100 µA | **bilans liczył jeden** |
| TPS3430-Q1, dzielniki, podciągnięcia, upływy | **nie policzone** | |
| VBG08H-E standby, jeśli VS wisi na akumulatorze | **5 000 µA** | karta: 5 mA typ, **niezależnie od stanu EN** |
| **Razem bez pozycji nieobliczonych i z odłączonym VS** | **~117–187 µA** | |

Limit to **150 µA**. Przypadek typowy leży na granicy i prawdopodobnie ją przekracza; przypadek skrajny (Stop 1 max 640 µA → ~293 µA z akumulatora) przekracza wielokrotnie. **Wniosek jest ostrzejszy niż „bilans jest niekompletny": wymaganie 150 µA najprawdopodobniej nie jest osiągalne w obecnej architekturze.**

Trzy drogi, do rozstrzygnięcia w etapie 3:
- **Standby zamiast Stop** — pobór rzędu jednostek µA, ale traci zawartość RAM i wymaga zdefiniowanego pinu wybudzania;
- **domena MCU za przełącznikiem obciążenia**, sterowana maleńkim obwodem budzenia stale zasilanym;
- **zmiana wymaganej wartości** — decyzja produktowa, nie techniczna: ECU wisi na akumulatorze bez stacyjki, więc liczy się czas do rozładowania przy postoju zimowym.

---

## 6. Plan prac — sześć etapów

Kolejność wynika z jednej reguły: **dane wejściowe przed decyzjami, które od nich zależą.** Poprzedni plan tę regułę łamał — kontakt z motocyklem był w Fazie 8, na gotowym PCB, czyli po wszystkich decyzjach opartych na niezweryfikowanych założeniach.

### Etap 0 — Utrwalenie i uczciwe statusy

*Bez motocykla, bez zakupów. Nic tu nie zależy od pomiarów.*

| Zadanie | Zamyka |
|---|---|
| Repozytorium git, import DOC-001…011, kopia poza środowiskiem pracy, znacznik baseline | **A41**, L34 (mechanizm) |
| Wprowadzenie statusu trójstanowego we wszystkich rejestrach; **L34, L36, L37 wracają do stanu otwartego** | **A41, A42** |
| Wstawienie zasad #18–#21 i korekty #5 do DOC-001 | **A45** |
| Rejestr A01–A50 jako tabela śledzenia w repozytorium | — |
| Korekta zapisu o polaryzacji EN: **rezystory ściągające na linii EN są błędem**; ECU-SAF-016 wraca do stanu otwartego — poprawna postać zależy od schematu (etap 4) | **A02** (decyzja) |
| Korekta klasyfikacji szyny 5 V: z „utraty sygnału obciążenia" do **awarii domeny zasilania** | **A18** |
| Mapa awaryjna „na bogato" oznaczona jako niezweryfikowana koncepcja **poza baseline MVP-A** | **A20** |
| Usunięcie wymagań B/C z listy blokującej G0; baseline MVP-A z jawnie wyłączonymi B/C | **A43** |
| Korekta nagłówka 8.1 i bilansu uśpienia; liczniki generowane skryptem | **A50** |
| Założenia nowe: Z11 sprawność przetwornicy, Z12 typ zapłonu (do obalenia w etapie 1), plus wnioski wg rozdz. 3.4 | **A45** |
| Ustalenie dostępu do ISO 16750-2/-3/-4 i ISO 7637-2 | warunek etapu 3 |

### Etap 1 — Triaż zapłonu i oględziny

*Motocykl, multimetr, oględziny. Krótkie i tanie, a rozstrzyga najdroższe pytanie w projekcie.*

Jedno pytanie: **DC-CDI czy zapłon indukcyjny.** Jeśli CDI — dobór VBG08H-E, cała architektura dwell, analiza termiczna 4,8 W, założenie Z2 i wniosek o obudowie aluminiowej wymagają przeprojektowania. Dlatego ten etap jest przed pełną sesją pomiarową: **wynik zmienia połowę jej zakresu.**

Przy okazji, bez przyrządów: dostęp mechaniczny do bębna zmiany biegów (**A36**), sposób podłączenia rozrusznika — silnik czy cewka przekaźnika (**A34**), sposób zasilania cewki i obecność puszki CDI.

Procedurę triażu przygotuję osobno, przed wyjściem do motocykla.

### Etap 2 — Pełna sesja pomiarowa i naprawa założeń fizycznych

*Zakres zależy od wyniku etapu 1.*

Pomiary: parametry cewki, przebieg na uzwojeniu pierwotnym, **fabryczna krzywa wyprzedzenia względem GMP** (daje punkt odniesienia dla naszej mapy i rozstrzyga Z4 oraz pytanie o limit 28°), analogowy VR razem z COUT względem niezależnego GMP przy rozruchu i w całym zakresie obrotów, bicie i zmiana szczeliny na pełnym obrocie.

Jedna rzecz, którą pomiar musi rozróżnić, a która łatwo umknie: **czy offset między krawędzią mechaniczną a zboczem COUT jest stały, czy zmienny z obrotami.** Układ uzbraja detektor zera progiem 33% poprzedniego szczytu, więc offset pochodzący z dynamiki progu będzie zależny od obrotów i amplitudy — wtedy jedna stała kalibracyjna nie wystarczy i potrzebna jest krzywa korekcyjna. Zmierzenie offsetu przy jednych obrotach i uznanie sprawy za zamkniętą byłoby wzorcem B w nowym wydaniu.

Na tej podstawie: decyzja o topologii zapłonu, korekta kąta odniesienia, budżet latencji od znacznika do iskry, model usterek ogranicznika dwell.

Zamyka albo rozstrzyga: **A01, A05, A06, A07, A09, A11, A13, A34**, założenia **Z2, Z3, Z4, Z5, Z12**.

### Etap 3 — Zamknięcie bramki G0

| Zadanie | Zamyka |
|---|---|
| Obwiednia środowiskowa i elektryczna z rozdz. 4.1 — **w tym pierwsze w projekcie wymaganie na temperaturę pracy ECU** | **A25, A49**, SYS-ENV-006 |
| **Bezwzględna granica błędu kąta** obok percentyla, osobno dla iskry zbyt wczesnej, plus reakcja na przekroczenie | **A08** |
| Polityka live tuningu: blokada aktywacji przy pracującym silniku + osobny tryb stanowiskowy z fizycznym zezwoleniem (decyzja 12.10.2026) | **A21**, ECU-SAF-011 |
| Wymagania bootloadera, w tym **sprzętowe rozbrojenie wyjść przez cały czas aktualizacji** | **A23** |
| Scenariusze wybudzania i dopuszczone sposoby startu | **A28** |
| Rozstrzygnięcie bilansu uśpienia (rozdz. 5.2) i sprzeczności watchdog/uśpienie (rozdz. 5.1) | **A26, A27**, częściowo **A14** |
| Analiza zagrożeń dla MVP-A i uzasadnienie zamkniętej listy 7 zatrzymań | **A17** |
| Pokrycie od funkcji i zagrożeń do wymagań, nie tylko od identyfikatorów | **A44** |
| Budżet wykonalności i plan wyposażenia pomiarowego | **A47**, L38 |
| Zatwierdzenie kryteriów wyrobu A1–A12 | L37 (decyzja) |
| Zamiennik IMU: AEC-Q100, zakres 125 °C, 2–3 kandydatów z arkuszem #18 (decyzja 12.10.2026) | **A31, A32** |

### Etap 4 — Architektura, schemat, G1 i G2

Tor energii i wyzwalania dla wybranej topologii. Logika od resetu i kill switcha do każdego pinu wykonawczego, z tabelą prawdy, polaryzacją i stanem przy braku zasilania (**A02**). Rozdzielenie zaplanowanej iskry od awaryjnego rozładowania cewki, z kolejnością INP i EN (**A03**). **Niezależny sprzętowy sufit czasu ładowania** (**A04**, rozdz. 5 wniosek 2). Ponowne uzbrojenie po K4 bez utożsamiania braku VR ze stojącym wałem (**A15**). Pełna analiza usterek kill switcha i wspólnych przyczyn (**A16**). Nadzór szyn z niezależnym odniesieniem (**A37**). Odłączanie VS drivera w uśpieniu (**A26**). Macierz funkcji alternatywnych, DMA i errata (**A33**). Pinout wiązki i bilans obwodów (**A35**). Czujnik biegu — mechanika (**A36**). Termika HMI i drabinka przycisków (**A29, A30**). Masy, powroty prądowe i ochrona wejść przed PCB (**A38**).

**Warunek wejścia do PCB: punktowy przegląd toru energii, odcięcia i synchronizacji przez drugiego kompetentnego inżyniera (A46).** Ani audyt AUD-ECU-002, ani ja tego warunku nie zamykamy — oba są analizą wspieraną modelem.

### Etap 5 — Dokończenie C, punkt D, punkt H, protokoły

Na poprawionej podstawie: rozruch i synchronizacja ze stanami UNSYNC/ACQUIRE/SYNC (**A11, A12**), metoda odcięcia w ograniczniku (**A19**), korekta dwell od napięcia, osobna predykcja początku i końca impulsu (**A10**). Następnie punkt D: struktura map, walidacja po stronie ECU, **atomowa aktywacja z jednym właścicielem wersji na impuls** i granica bezpieczeństwa niezależna od edytowanej mapy (**A22**). Potem bootloader i odzyskiwanie po przerwanej aktualizacji (**A24**), czarna skrzynka z bilansem zapisu (**A39**), protokoły z semantyką operacji przed formatem transportu (**A40**).

### Etap 6 — Stanowisko i G3

Stanowisko Fazy 3 rozszerzone o analogowy VR i reprezentatywne obciążenia indukcyjne. Wstrzykiwanie usterek, próby aktualizacji, błędnych danych map, przeciążenia logowaniem. Zamknięcie zasady #17: standard kodowania, konfiguracja analizy statycznej, progi pokrycia testami, odtwarzalny build (**L36**, mechanizm i dowód). T-AUD-01…20 z audytu włączone do traceability.

---

## 7. Decyzje przyjęte 12.10.2026

| # | Decyzja | Uzasadnienie |
|---|---|---|
| 1 | **Triaż typu zapłonu przed pełną sesją pomiarową** | Wynik zmienia połowę zakresu pełnej sesji; triaż jest tani |
| 2 | **IMU: szukamy zamiennika AEC-Q100 w zakresie 125 °C** | BMI090L nie ma kwalifikacji i kończy się na 85 °C, a ma prawo odciąć silnik. Odrzucony wariant pozostawienia go z uzasadnieniem miejsca montażu oraz wariant odebrania mu prawa odcięcia |
| 3 | **Live tuning: blokada aktywacji przy pracującym silniku + osobny tryb stanowiskowy z fizycznym zezwoleniem, definiowany od razu** | Zgodne z rekomendacją audytu; wariant stanowiskowy zachowuje możliwość strojenia w kontrolowanych warunkach, zamiast odkładać ją na później |
| 4 | **Zakres normatywny: obwiednia z ISO 16750 i ISO 7637-2, techniki analityczne z ISO 26262 bez aparatu zgodności, MISRA C w podzbiorze, AEC-Q rozszerzone na bierne elementy istotne dla bezpieczeństwa** | Wartość siedzi w technikach i w gotowych definicjach zjawisk, nie w dokumentacji zgodności |

---

## 8. Triaż 50 ustaleń audytu

**Stanowisko ogólne: audyt przyjmujemy w całości.** Jedno ustalenie przyjęte z korektą mechanizmu (A06), dwa rozszerzone ponad treść audytu (A04, A14). Żadne nie zostało odrzucone — weryfikacja u źródeł potwierdziła wszystkie twierdzenia, które dało się sprawdzić bez motocykla.

Legenda: **P** = przyjęte · **P-K** = przyjęte z korektą · **P-R** = przyjęte i rozszerzone · **W** = weryfikacja wykonana przeze mnie u źródła

| ID | Prio | Stanowisko | Trafia do |
|---|---|---|---|
| A01 zgodność stopnia zapłonowego | P0 | **P** | Etap 1, potem 2 |
| A02 polaryzacja EN | P0 | **P** · **W: karta potwierdza EN aktywne niskim i wewnętrzny pull-up** | Etap 0 (zapis), 4 (obwód) |
| A03 iskra przy awaryjnym wygaszaniu | P0 | **P** | Etap 4 |
| A04 okres HRTIM nie jest niezależny | P0 | **P-R** — groźny podprzypadek: zegar staje przy aktywnym wyjściu; wymaga sufitu sprzętowego poza HRTIM | Etap 4 |
| A05 zakres 16-bitowy HRTIM | P0 | **P** · **W: 1,542 ms wobec założonych 3 ms** | Etap 2 |
| A06 elektryczny znacznik VR | P0 | **P-K** — zalecenie przyjęte w całości; **mechanizm „centrum zęba ≈ 15° przed GMP" nie dotyczy wypustu 30°**, bo długi wypust daje dwa osobne zdarzenia strumienia, nie jeden impuls z zerem w środku. Realne ryzyko to mniejszy offset **zależny od obrotów** | Etap 2 |
| A07 estymaty błędu nieodtwarzalne | P1 | **P** | Etap 2 |
| A08 percentyl bez granicy bezwzględnej | P0 | **P** | Etap 3 |
| A09 limit 28° bez budżetu latencji | P1 | **P** · **W: tdOFF 25 µs to wartość w jednym punkcie pracy** | Etap 2 |
| A10 predykcja początku ładowania | P1 | **P** | Etap 5 |
| A11 rozruch i ruch wsteczny | P0 | **P** | Etap 5 |
| A12 bramkowanie i odzysk synchronizacji | P1 | **P** | Etap 5 |
| A13 charakterystyka cewki | P1 | **P** | Etap 2 |
| A14 watchdog zdrowia funkcji | P0 | **P-R** — dochodzi analiza FTTI (rozdz. 5) i **sprzeczność watchdog/uśpienie** (rozdz. 5.1), której audyt nie nazwał | Etap 3, 4 |
| A15 zatrzask K4 przy uszkodzonym VR | P0 | **P** | Etap 4 |
| A16 kill switch — analiza usterek | P1 | **P** | Etap 4 |
| A17 lista 7 zatrzymań bez analizy zagrożeń | P1 | **P** | Etap 3 |
| A18 szyna 5 V nie jest sygnałem obciążenia | P1 | **P** | Etap 0 |
| A19 limit obrotów ≠ ochrona termiczna | P1 | **P** | Etap 5 |
| A20 bogata mapa awaryjna | P1 | **P** | Etap 0 |
| A21 live tuning | P0 | **P** — decyzja 3 z rozdz. 7 | Etap 3 |
| A22 atomowa aktywacja mapy | P1 | **P** | Etap 5 |
| A23 rozbrojone wyjścia w aktualizacji | P0 | **P** | Etap 3, 5 |
| A24 odporność aktualizacji na zanik zasilania | P1 | **P** | Etap 5 |
| A25 ochrona instalacji i obwiednia | P0 | **P** | Etap 3 (normy), 4 |
| A26 driver zapłonu w bilansie uśpienia | P1 | **P** · **W: 5 mA typ / 6 mA max, niezależnie od stanu EN** | Etap 0, 4 |
| A27 bilans uśpienia niekompletny | P1 | **P-R** — przeliczony na zaciskach akumulatora, rozdz. 5.2; wniosek: **limit 150 µA prawdopodobnie nieosiągalny** | Etap 0, 3 |
| A28 scenariusz wybudzania | P1 | **P** | Etap 3 |
| A29 termika HMI przed PCB | P1 | **P** | Etap 4 |
| A30 drabinka przycisków HMI | P1 | **P** | Etap 4 |
| A31 BMI090L bez AEC-Q100 | P1 | **P** · **W: flyer Boscha nie zawiera AEC-Q100; rynki docelowe AGD/roboty/drony; −40…+85 °C** | Decyzja 2, etap 3 |
| A32 cykl życia BMI090L | P1 | **P** | Decyzja 2, etap 3 |
| A33 bilans MCU i funkcje alternatywne | P1 | **P** | Etap 4 |
| A34 kanał rozrusznika | P1 | **P** | Etap 1, 4 |
| A35 złącze i wiązka | P1 | **P** | Etap 4 |
| A36 czujnik biegu — mechanika | P1 | **P** | Etap 1, 4 |
| A37 pomiary ratiometryczne i nadzór szyny | P1 | **P** | Etap 4 |
| A38 EMC przed integracją | P1 | **P** | Etap 4 |
| A39 czarna skrzynka | P1 | **P** | Etap 5 |
| A40 semantyka komend protokołu | P1 | **P** | Etap 5 |
| A41 L34 repozytorium otwarte | P1 | **P** · **W: sprzeczność statusu z opisem w tym samym dokumencie** | Etap 0 |
| A42 L36/L37 to decyzje, nie zamknięcia | P1 | **P** — wdrażamy status trójstanowy, zasada #21 | Etap 0 |
| A43 zakres G0 bez pozycji B/C | P1 | **P** | Etap 0, 3 |
| A44 pokrycie ≠ kompletność | P1 | **P** | Etap 3 |
| A45 egzekwowanie zasad | P1 | **P** — w tym korekta zasady #5 o elementach biernych | Etap 0 |
| A46 przegląd modelu ≠ przegląd ludzki | P1 | **P bez zastrzeżeń** — warunek wejścia do PCB | Etap 4 |
| A47 wyposażenie i budżet wykonalności | P1 | **P** | Etap 3 |
| A48 kolejność prac | P1 | **P** — plan przebudowany, rozdz. 6 | Ten dokument |
| A49 obwiednia środowiskowa | P1 | **P** | Etap 3 |
| A50 niespójne liczniki i sumy | P2 | **P** · **W: oba potwierdzone — nagłówek 8.1 i suma 51–110 vs 70–135 µA** | Etap 0 |

### 8.1 Pozycje weryfikowane przeze mnie u źródła

Siedem twierdzeń audytu dało się sprawdzić bez motocykla i **wszystkie siedem się potwierdziło**: A02, A05, A09, A26, A31, A41, A50. Twierdzenie A01 — typ zapłonu — nie zostało przeze mnie potwierdzone niezależnie; nie dotarłem do strony 23 instrukcji fabrycznej. Jest jednak zgodne z praktyką tej klasy silników, a w naszych dokumentach widać ślad powstania błędu: decyzja 2.1 wykluczyła CDI zasilane ze statora i pozostawiła niezapisany wniosek o zapłonie indukcyjnym. **Rozstrzygnięcie jest pomiarem z etapu 1.**

---

## 9. Nowe pozycje w rejestrach

Do wstawienia do DOC-001 w etapie 0.

### 9.1 Nowe założenia

| # | Założenie | Co się zawali, jeśli fałszywe | Sposób potwierdzenia |
|---|---|---|---|
| **Z11** | Sprawność przetwornic przy obciążeniu rzędu dziesiątek µA wynosi ok. 60% | Cały przeliczony bilans uśpienia (rozdz. 5.2) | Karta katalogowa wybranej przetwornicy, potem pomiar |
| **Z12** | Beta 300 RR 2015 ma zapłon indukcyjny, a nie DC-CDI | Dobór VBG08H-E, architektura dwell, analiza termiczna, Z2, obudowa aluminiowa | **Etap 1 — triaż na motocyklu** |
| **Z13** | Offset między krawędzią mechaniczną wypustu a zboczem COUT jest stały w funkcji obrotów | Jedna stała kalibracyjna zamiast krzywej korekcyjnej; dokładność kąta w całym zakresie | Etap 2 — pomiar przy kilku prędkościach |

### 9.2 Nowe luki

| # | Luka | Przypisanie |
|---|---|---|
| **L41** | Brak jakiegokolwiek wymagania na temperaturę pracy ECU i HMI — SYS-ENV-001/002 dotyczą napięcia | Etap 3 |
| **L42** | Brak zdefiniowanego stanu bezpiecznego per wyjście wykonawcze, z polaryzacją i stanem przy braku zasilania | Etap 4 |
| **L43** | Brak analizy niezależności i wspólnych przyczyn awarii dla mechanizmów bezpieczeństwa | Etap 4 |
| **L44** | Sprzeczność między oknem watchdoga 100 ms a trybem uśpienia — nierozstrzygnięta i nieopisana | Etap 3 |
| **L45** | Brak niezależnego przeglądu ludzkiego; dwa audyty to analizy wspierane modelem | Etap 4, przed PCB |

---

## 10. Czego ten plan nie rozwiązuje

Uczciwie, żeby nie powtarzać wzorca zamykania pozycji deklaracją:

- **Zasady #18–#21 są na razie zapisem, nie mechanizmem.** Ich wdrożenie to etap 0, a dowód skuteczności pojawi się dopiero wtedy, gdy zablokują konkretną propozycję. Pierwszym testem będzie arkusz kwalifikacji dla zamiennika IMU.
- **Nie wiemy, czy limit 150 µA jest osiągalny**, dopóki nie wybierzemy przetwornic i nie policzymy bilansu z pełnej listy domen.
- **Nie wiemy, czy VBG08H-E zostaje w projekcie.** Zależy to od jednego pomiaru, którego jeszcze nie wykonaliśmy.
- **Nie mamy dostępu do norm ISO** wymienionych w rozdz. 4.1 i nie znamy kosztu ich zdobycia.
- **Nie mamy przeglądu ludzkiego** i ten plan go nie zastępuje.
