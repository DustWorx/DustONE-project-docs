# ECU „Dust ONE"

Samodzielna, programowalna jednostka sterująca silnika do motocykli enduro i adventure, razem z modułem wyświetlacza na kierownicę i aplikacją desktop do strojenia i diagnostyki.

**Przeznaczenie: motorsport i entuzjaści offroadu. Urządzenie nie jest i nie będzie homologowane drogowo.**

---

## Stan projektu — 13.10.2026

| | |
|---|---|
| Faza | **2-FW — specyfikacja firmware w toku** |
| Bramka | **G0 zablokowana** |
| Ostatni audyt | AUD-ECU-002, 11.10.2026 — werdykt **NO-GO** |
| Wykonane testy | **zero** |
| Zbudowany sprzęt | **brak** |

**Czego ten stan nie oznacza.** Zero wykonanych testów jest stanem oczekiwanym — nie zbudowano jeszcze żadnej płytki. 99 identyfikatorów testów w dokumentacji to **miejsca na dowód, nie wykonane próby**. Żadne wymaganie nie jest zamknięte dowodem.

### Liczby

Generowane skryptem `skrypty/kontrola.py`, nie wpisywane ręcznie.

| Pozycja | Stan |
|---|---|
| Wymagania z identyfikatorem | 105 |
| Pokrycie w tabeli traceability | 105 / 105 |
| Wymagania bez ustalonej wartości — **blokują G0** | **17** |
| Kody usterek w macierzy | 49 |
| Identyfikatory testów | 99 |
| Luki w rejestrze | 40 |
| Ryzyka w rejestrze | 18 |
| Założenia w rejestrze | 10 |

### Co blokuje bramkę G0

1. 17 wymagań bez ustalonej wartości
2. Brak wymagań bootloadera
3. **Nierozstrzygnięty typ zapłonu fabrycznego** — patrz niżej

---

## Pozycja o najwyższym priorytecie

Audyt AUD-ECU-002 wskazał, że nie ustalono, czy Beta 300 RR 2015 ma **DC-CDI czy zapłon indukcyjny**. Instrukcja fabryczna wskazuje DC-CDI, a projekt przyjął driver cewki indukcyjnej (VBG08H-E) bez zapisania tego wniosku.

Jeśli motocykl ma CDI, przeprojektowania wymagają: dobór drivera zapłonu, architektura ładowania cewki, analiza termiczna i wybór obudowy.

**Rozstrzyga pomiar: `pomiary/triaz-zaplonu.md`** — multimetr, 30 minut.

---

## Struktura repozytorium

| Katalog | Zawartość |
|---|---|
| `dokumentacja/` | Dokumenty projektu — patrz tabela niżej |
| `diagramy/` | Diagramy w źródle Mermaid (`.mermaid`) i renderze (`.png`) |
| `pomiary/` | Procedury pomiarowe do wykonania na sprzęcie i ich wyniki |
| `audyty/` | Otrzymane raporty audytowe, w formie dostarczonej |
| `skrypty/` | Kontrola spójności dokumentacji |
| `archiwum/` | Dokumenty nieaktualne, zachowane jako materiał źródłowy |

### Dokumenty

| ID | Plik | Wersja | Zawartość |
|---|---|---|---|
| DOC-001 | `dokumentacja/proces-rozwoju-ecu.md` | 3.9 | Dokument główny: proces, fazy, bramki, zasady, decyzje sprzętowe, budżety, rejestry luk, ryzyk i założeń, tabela pokrycia wymagań |
| DOC-002 | `dokumentacja/wymagania.md` | 1.5 | 105 wymagań z wartościami i metodą weryfikacji |
| DOC-003 | `diagramy/architektura-systemu.mermaid` | 1.2 | Diagram blokowy systemu |
| DOC-004 | `dokumentacja/faza2-fw-specyfikacja.md` | 1.7 | Specyfikacja firmware: punkt A maszyna stanów, B bezpieczeństwo i macierz usterek, C.1 trigger |
| DOC-005 | `dokumentacja/przeglad-komponentow.md` | 1.6 | Cykl życia i dostępność komponentów, rejestr wzorców błędów |
| DOC-006 | `dokumentacja/plan-naprawczy-audyt.md` | 1.7 | Odpowiedź na pierwszy audyt, 36 pozycji |
| DOC-007 | `archiwum/faza3-specyfikacja-fw.md` | 0.1 | **Nieaktualny** — do napisania od nowa po zamknięciu Fazy 2-FW |
| DOC-008 | `diagramy/diagram-bezpieczenstwa.mermaid` | 1.2 | Łańcuch odcięcia zapłonu z podziałem na ścieżki sprzętowe i programowe |
| DOC-009 | `diagramy/diagram-zatrzask.mermaid` | 1.0 | Zatrzask klasy K4, odblokowanie, licznik resetów |
| DOC-010 | `dokumentacja/dossier-audytowe.md` | 1.1 | Pakiet wejściowy do drugiego audytu |
| DOC-011 | `dokumentacja/plan-naprawczy-audyt2.md` | 1.0 | **Plan naprawczy po drugim audycie** — diagnoza wzorców pomijania, zakres zapożyczeń z automotive, plan na 6 etapów, triaż 50 ustaleń |

**Od czego zacząć czytanie:** DOC-011 rozdz. 6 (plan prac) i rozdz. 8 (triaż ustaleń audytu). Dają aktualny obraz stanu w kilku stronach, zamiast lektury dokumentu głównego.

---

## Zakres produktu

| Wariant | Motocykl odniesienia | Zakres sterowania |
|---|---|---|
| **MVP-A** — gaźnik | **Beta 300 RR 2015** | Zapłon (mapa jednowymiarowa, kąt w funkcji obrotów), ogranicznik obrotów, wskaźnik biegu, prędkość i przebieg, motogodziny, wyjścia mocy, diagnostyka |
| B — TPI | KTM EXC TPI | Dodatkowo wtrysk paliwa |
| C — TBI | KTM 890 Adventure | Dodatkowo przepustnica sterowana elektronicznie |

**Projektowany jest wyłącznie MVP-A.** Warianty B i C mają zarezerwowane zdolności sprzętowe (wymagania oznaczone `[HW]` i `[B/C]`), ale nie mają własnych specyfikacji.

Motocykl MVP-A **nie ma czujnika położenia przepustnicy** i nie będzie on dokładany — stwierdzone 11.10.2026.

### Czego produkt świadomie nie robi

- **Quickshifter i czujnik sprzęgła** — usunięte 29.09.2026
- Pełne logowanie sesji jazdy — zawężone do czarnej skrzynki
- Blokada rozrusznika na biegu — odpowiedzialność po stronie kierowcy
- Regulacja napięcia szyn przez mikrokontroler

---

## Kontrola spójności

```bash
python3 skrypty/kontrola.py
```

Sprawdza pokrycie wymagań, generuje liczniki, wykrywa osierocone odwołania i porównuje wersje w spisie dokumentów z metrykami plików. Kod wyjścia 1 oznacza znalezione rozbieżności.

Istnieje dlatego, że liczniki wpisywane ręcznie rozjechały się z rejestrami — ustalenie A50 drugiego audytu.

---

## Planowana zmiana struktury

Dokumentacja liczy ~3900 linii, z czego inżynierii jest ~1200. **Ten commit utrwala stan przed konsolidacją**, żeby przebudowa była czytelnym diffem, a nie nadpisaniem.

Cel: 8 plików dokumentacji → 4 (`produkt.md`, `wymagania.md`, `firmware.md`, `otwarte.md`), pięć równoległych rejestrów → jeden z jedną przestrzenią identyfikatorów, tabele historii zmian usunięte na rzecz historii repozytorium.

---

## Ograniczenia, o których trzeba wiedzieć przy czytaniu

- **Nie było niezależnego przeglądu ludzkiego.** Oba audyty i cała dokumentacja powstały jako analiza wspierana modelem językowym. Przed uruchomieniem toru energii, odcięcia i synchronizacji potrzebny jest punktowy przegląd przez drugiego inżyniera.
- Część założeń technicznych nie jest potwierdzona pomiarem — rejestr założeń w DOC-001 rozdz. 11.2 wymienia je wraz z tym, co się zawali, jeśli są fałszywe.
- Dokumenty opisują stan projektowy, nie zweryfikowany sprzętowo.
