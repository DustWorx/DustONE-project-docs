# ECU „Dust ONE"

Samodzielna, programowalna jednostka sterująca silnika do motocykli enduro i adventure, razem z modułem wyświetlacza na kierownicę i aplikacją desktop do strojenia i diagnostyki.

**Przeznaczenie: motorsport i entuzjaści offroadu. Urządzenie nie jest i nie będzie homologowane drogowo.**

---

## Stan projektu

| | |
|---|---|
| Faza | **2-FW — specyfikacja firmware w toku** |
| Bramka | **G0 zablokowana** |
| Ostatni audyt | AUD-ECU-002, 11.10.2026 — werdykt **NO-GO** |
| Wykonane testy | **zero** |
| Zbudowany sprzęt | **brak** |

Zero wykonanych testów jest stanem oczekiwanym — nie zbudowano jeszcze żadnej płytki. 100 identyfikatorów testów to **miejsca na dowód, nie wykonane próby**. Żadne wymaganie nie jest zamknięte dowodem.

### Liczby

Generowane przez `scripts/kontrola.py`, nie wpisywane ręcznie.

| Pozycja | Stan |
|---|---|
| Wymagania z identyfikatorem | 107 |
| Pokrycie w tabeli traceability | 107 / 107 |
| Wymagania bez ustalonej wartości — **blokują G0** | **17** |
| Kody usterek w macierzy | 47 |
| Identyfikatory testów | 100 |
| Pozycje otwarte | 63 |
| Założenia (1 obalone, 1 potwierdzone, 11 niepotwierdzonych) | 13 |

---

## Pozycja o najwyższym priorytecie

**Nie jest ustalone, czy Beta 300 RR 2015 ma DC-CDI czy zapłon indukcyjny.** Instrukcja fabryczna wskazuje DC-CDI, a projekt przyjął driver cewki indukcyjnej (VBG08H-E) bez zapisania tego wniosku.

Jeśli motocykl ma CDI, przeprojektowania wymagają: dobór drivera zapłonu, architektura ładowania cewki, analiza termiczna i wybór obudowy.

**Rozstrzyga pomiar: [`measurements/triaz-zaplonu.md`](measurements/triaz-zaplonu.md)** — multimetr, 30 minut.

---

## Dokumentacja

Pięć plików. Każdy odpowiada na jedno pytanie.

| Plik | Odpowiada na pytanie |
|---|---|
| [`produkt.md`](produkt.md) | **Co budujemy i jak to jest zbudowane?** Zakres, warianty, decyzje sprzętowe z uzasadnieniami i odrzuconymi alternatywami, komponenty, zasilanie, złącze, uśpienie, HMI, budżety, obudowy, obwiednia środowiskowa |
| [`wymagania.md`](wymagania.md) | **Co musi być spełnione i czym to udowodnimy?** 105 wymagań z wartościami i metodą weryfikacji + tabela pokrycia od wymagania do dowodu |
| [`firmware.md`](firmware.md) | **Jak firmware ma się zachowywać?** Maszyna stanów, bezpieczeństwo i macierz usterek, trigger i synchronizacja, punkty C.2–J otwarte |
| [`otwarte.md`](otwarte.md) | **Czego jeszcze nie wiemy i co może być fałszywe?** Jedyny rejestr pozycji otwartych, założenia, ryzyka zaakceptowane świadomie |
| [`proces.md`](proces.md) | **W jakiej kolejności i kiedy można przejść dalej?** Fazy, bramki, kryteria odbioru wyrobu, plan prac |
| [`HISTORIA.md`](HISTORIA.md) | **Co się zmieniło i dlaczego?** Jedna linia na zmianę merytoryczną, najnowsze u góry |

| Katalog | Zawartość |
|---|---|
| `diagrams/` | Architektura systemu, łańcuch odcięcia zapłonu, zatrzask K4 — źródło Mermaid i render PNG |
| `measurements/` | Procedury pomiarowe do wykonania na sprzęcie i ich wyniki |
| `audit/` | Otrzymane raporty audytowe w formie dostarczonej |
| `scripts/` | Kontrola spójności i generowanie liczników |


**Od czego zacząć:** `otwarte.md` rozdz. „Co blokuje bramkę G0" i `proces.md` rozdz. 5. Dają aktualny obraz stanu na dwóch stronach.

---

## Zakres produktu

| Wariant | Motocykl odniesienia | Zakres sterowania |
|---|---|---|
| **MVP-A** — gaźnik | **Beta 300 RR 2015**, 1-cyl. 2T, **bez TPS** | Zapłon (mapa jednowymiarowa), ogranicznik obrotów, wskaźnik biegu, prędkość i przebieg, motogodziny, wyjścia mocy, diagnostyka |
| B — TPI | KTM EXC TPI | Dodatkowo wtrysk paliwa |
| C — TBI | KTM 890 Adventure | Dodatkowo przepustnica sterowana elektronicznie |

**Projektowany jest wyłącznie MVP-A.** Warianty B i C mają zarezerwowane zdolności sprzętowe, ale nie mają własnych specyfikacji.

Świadomie usunięte z produktu: **quickshifter i czujnik sprzęgła**, blokada rozrusznika na biegu, automatyczne ograniczenie mocy przy przegrzaniu, regulacja napięcia szyn przez mikrokontroler. Uzasadnienia w `produkt.md` rozdz. 1.1.

---

## Kontrola spójności

```bash
python3 scripts/kontrola.py
```

Sprawdza pokrycie wymagań, generuje liczniki, weryfikuje odwołania do pozycji otwartych i wykrywa osierocone identyfikatory. Kod wyjścia 1 oznacza znalezione rozbieżności.

Istnieje dlatego, że liczniki wpisywane ręcznie rozjechały się z rejestrami — dokumenty podawały 51 kodów usterek i 107 testów przy rzeczywistych 47 i 100.

---

## Dokumentacja przed konsolidacją

Stan dokumentacji sprzed 13.10.2026 — dawny dokument główny, odpowiedzi na oba audyty, przegląd komponentów i nieaktualna specyfikacja Fazy 3 — został na gałęzi **[`Old-docs`](https://github.com/DustWorx/DustONE-project-docs/tree/Old-docs)**, z tagiem `baseline-2026-10-13`. Ta gałąź jest kopią bezpieczeństwa: **nie jest rozwijana i nie należy jej traktować jako źródła aktualnego stanu.**

Aktualna dokumentacja żyje na gałęzi **`Actual-documentation`** i to ona jest jedynym źródłem obowiązującego stanu projektu.

---

## Ograniczenia, o których trzeba wiedzieć przy czytaniu

- **Nie było niezależnego przeglądu ludzkiego.** Oba audyty i cała dokumentacja powstały jako analiza wspierana modelem językowym. Przed uruchomieniem toru energii, odcięcia i synchronizacji potrzebny jest punktowy przegląd przez drugiego inżyniera — pozycja O-057.
- **Trzynaście założeń nie jest potwierdzonych pomiarem.** `otwarte.md` rozdz. 8 wymienia je wraz z tym, co się zawali, jeśli są fałszywe. Jedno już się zawaliło.
- Dokumenty opisują stan projektowy, nie zweryfikowany sprzętowo.
