# Historia zmian

Jedna linia na zmianę, najnowsze u góry. Pełny diff każdej zmiany jest w historii repozytorium — ten plik służy do tego, żeby nie trzeba było jej przeglądać, żeby wiedzieć, co się działo.

| Data | Zmiana | Pliki | Powód |
|---|---|---|---|
| 2026-10-15 | **Dokumentacja po konsolidacji przeniesiona na gałąź `Actual-documentation`.** Ta gałąź zawiera wyłącznie aktualne dokumenty; stan przed konsolidacją został na gałęzi `Old-docs` jako kopia bezpieczeństwa i nie jest rozwijany | wszystkie | Wypychanie całego repozytorium przy każdej zmianie, razem z archiwum, którego nie używamy |
| 2026-10-13 | **Obwiednia temperaturowa doprowadzona do praktyki automotive.** ECU **−40…+85 °C** otoczenia (było −20…+60 °C), HMI **−20…+70 °C** (ograniczone panelem LCD), przechowywanie **−40…+105 °C**. Nowe **SYS-ENV-003b** wiążące klasę temperaturową komponentu z temperaturą wewnątrz obudowy i marginesem 15 °C, z siatką klas AEC-Q100. Dwa nowe identyfikatory, 107 wymagań. **Skutek: BMP390 zdyskwalifikowany w obecnej roli, obok IMU** | `wymagania.md`, `produkt.md`, `otwarte.md` | Decyzja Pawła. Poprzednia wartość była nierealna dla ECU przy silniku dwusuwowym, a rozdział o obudowach podawał drugą, inną liczbę |
| 2026-10-13 | **DTC-SEN-04 nie został usunięty** — obowiązuje wyłącznie w wariantach B/C, gdzie czujnik przepustnicy istnieje. Opisanie go jako usuniętego przy obalaniu założenia Z1 było nieścisłością zapisu | `firmware.md`, `otwarte.md` | Niespójność wykryta przez skrypt kontrolny przy konsolidacji |
| 2026-10-13 | **Pełne numery katalogowe przeklasyfikowane na pracę zaplanowaną (Faza 4).** Powstają przy projektowaniu PCB, razem z doborem każdego elementu pod schemat. Dwa wyjątki rozstrzygane wcześniej, bo dyskwalifikuje je SYS-ENV-003b: IMU i BMP390 | `otwarte.md` | Decyzja Pawła |
| 2026-10-13 | **Konsolidacja dokumentacji: 8 plików w 5, pięć rejestrów w jeden.** 3917 linii → 2196. 162 identyfikatory w pięciu przestrzeniach (luki L, ryzyka R, założenia Z, audyt F, audyt A) zwinięte do 63 pozycji otwartych i 13 założeń w jednej przestrzeni `O-nnn`. Status rozbity na trzy niezależne: decyzja, mechanizm, dowód. Tabele historii zmian usunięte z treści dokumentów na rzecz tego pliku i historii repozytorium | wszystkie | Dwie trzecie dokumentacji opisywało projekt, nie produkt |
| 2026-10-13 | **Stan przed konsolidacją utrwalony w repozytorium**, tag `baseline-2026-10-13` | — | Żeby konsolidacja była czytelnym diffem, a nie nadpisaniem |
| 2026-10-12 | **Plan naprawczy po audycie AUD-ECU-002**: diagnoza pięciu wzorców pomijania, pięć nowych zasad procesu, zakres zapożyczeń z norm automotive, plan na 6 etapów, triaż 50 ustaleń. Zasady dyscypliny wyprowadzone z dokumentów do instrukcji roboczej | gałąź `Old-docs` | Werdykt NO-GO drugiego audytu |
| 2026-10-11 | **Obalone założenie Z1 — Beta 300 RR nie ma czujnika przepustnicy.** Skorygowane siedem zapisów pochodnych: mapa zapłonu MVP-A jednowymiarowa (nowe ECU-IGN-020), usunięte ECU-IGN-008, ECU-SEN-003 przeniesione do zdolności sprzętowych | `wymagania.md`, `firmware.md` | Pierwszy wpis do nowo utworzonego rejestru założeń okazał się fałszywy tego samego dnia |
| 2026-09-29 | **Quickshifter i czujnik sprzęgła usunięte z produktu.** 9 wymagań, 3 kody usterek, 2 komponenty i 2 piny poza zakresem | `wymagania.md`, `firmware.md`, `produkt.md` | Jedyna funkcja wymagająca wnioskowania o intencji kierowcy; trzy kolejne błędy specyfikacji |

## Zasady prowadzenia tego pliku

- Wpis powstaje **przy zmianie, nie po fakcie** — razem z commitem, który tę zmianę wprowadza
- Jedna linia na zmianę merytoryczną; poprawki literówek i formatowania nie trafiają tutaj
- Kolumna **Powód** jest obowiązkowa: bez niej po miesiącu nie da się odtworzyć, dlaczego coś zmieniono
- Zmiana wartości wymagania albo progu zadziałania **musi** mieć wpis, nawet jednoliterowa
