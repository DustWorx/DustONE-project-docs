# Szkielet platformy — pomiar warstwy sterowników (O-067)

Szkielety **nie są firmware'em**. Inicjalizują i wywołują peryferia używane przez ECU i HMI (HRTIM, ADC2–5 z DMA, FDCAN, SPI1–3 z DMA, TIM2/TIM17, RTC, CRC, FLASH, USB CDC), żeby zmierzyć, ile pamięci zajmuje sama warstwa sterowników ST (HAL + biblioteka USB Device). Logika aplikacji jest w budżecie szacowana osobno (`scripts/budzet_wykonalnosci.py`).

Uruchomienie: `scripts/szkielet/build.sh` — pobiera kompilator xPack arm-none-eabi-gcc 13.3.1-1.1 i repozytoria ST z GitHuba, kompiluje z `-Os`, `--gc-sections`, newlib-nano.

Wynik z 26.11.2026 — ECU (STM32G474, `-mcpu=cortex-m4`): aplikacja 37,7 KB Flash / 9,5 KB RAM, bootloader 15,9 KB Flash / 7,0 KB RAM. HMI (STM32G474RE od 26.11.2026; Quad-SPI do EVE4, FDCAN, I2C, ADC, IWDG, FLASH, CRC): aplikacja 14,8 KB / 5,2 KB, bootloader 6,2 KB / 4,3 KB (liczby RAM z 4 KB stosu; liczby ECU i ~1,4 KB newlib stdio wciąganego przez `exit()` w starcie).
