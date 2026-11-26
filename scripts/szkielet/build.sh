#!/bin/bash
# Pomiar rozmiaru warstwy sterowników STM32G474 (HAL + USB CDC) — O-067.
# Użycie: scripts/szkielet/build.sh [katalog_pamięci_podręcznej]
# Pobiera: xPack arm-none-eabi-gcc 13.3.1-1.1 oraz repozytoria ST (HAL G4, CMSIS, USB Device) — wersje z wydruku poniżej.
set -e
D=$(cd "$(dirname "$0")" && pwd); C=${1:-$HOME/.cache/dustone-szkielet}; mkdir -p $C; cd $C
TC=xpack-arm-none-eabi-gcc-13.3.1-1.1
[ -d $TC ] || { curl -sSL -o gcc.tgz https://github.com/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases/download/v13.3.1-1.1/$TC-linux-x64.tar.gz; tar xzf gcc.tgz; }
for r in stm32g4xx_hal_driver cmsis_device_g4 stm32_mw_usb_device cmsis_core; do [ -d $r ] || git clone -q --depth 1 https://github.com/STMicroelectronics/$r.git; done
for r in stm32g4xx_hal_driver cmsis_device_g4 stm32_mw_usb_device; do echo "$r $(git -C $r log -1 --format=%h' '%cs)"; done
T=$C/$TC/bin/arm-none-eabi-; H=$C/stm32g4xx_hal_driver; U=$C/stm32_mw_usb_device; B=$C/build; rm -rf $B; mkdir -p $B/inc
cp $H/Inc/stm32g4xx_hal_conf_template.h $B/inc/stm32g4xx_hal_conf.h
sed -e 's/#include "stm32fxxx.h".*/#include "stm32g4xx_hal.h"/' -e 's/#define USBD_DEBUG_LEVEL .*/#define USBD_DEBUG_LEVEL 0U/' -e 's/#define USBD_CLASS_BOS_ENABLED .*//' -e 's/#define USBD_CLASS_USER_STRING_DESC .*//' -e 's/#define USBD_SUPPORT_USER_STRING_DESC .*//' $U/Core/Inc/usbd_conf_template.h > $B/inc/usbd_conf.h
cp $U/Core/Inc/usbd_desc_template.h $B/inc/usbd_desc.h; cp $U/Core/Src/usbd_desc_template.c $B/usbd_desc.c
sed -e 's/usbd_cdc_if_template.h/usbd_cdc.h/' $U/Class/CDC/Src/usbd_cdc_if_template.c > $B/usbd_cdc_if.c
CF="-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -Os -ffunction-sections -fdata-sections -DSTM32G474xx -DUSE_HAL_DRIVER -DHSE_VALUE=8000000 -I$B/inc -I$H/Inc -I$C/cmsis_device_g4/Include -I$C/cmsis_core/CMSIS/Core/Include -I$U/Core/Inc -I$U/Class/CDC/Inc"
LF="-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard --specs=nano.specs --specs=nosys.specs -Wl,--gc-sections"
WSP="$D/usbd_conf.c $B/usbd_desc.c $B/usbd_cdc_if.c $C/cmsis_device_g4/Source/Templates/system_stm32g4xx.c $U/Core/Src/usbd_core.c $U/Core/Src/usbd_ctlreq.c $U/Core/Src/usbd_ioreq.c $U/Class/CDC/Src/usbd_cdc.c"
zbuduj(){ # nazwa main.c ld moduły...
  n=$1; m=$2; ld=$3; shift 3; o=$B/$n; mkdir -p $o; S="$m $WSP"; for x in "$@"; do S="$S $H/Src/stm32g4xx_$x.c"; done
  for f in $S; do ${T}gcc $CF -c $f -o $o/$(basename $f .c).o; done
  ${T}gcc $CF -c $C/cmsis_device_g4/Source/Templates/gcc/startup_stm32g474xx.s -o $o/startup.o
  ${T}gcc $LF -T $ld $o/*.o -o $o/$n.elf 2>/dev/null || true; ${T}size $o/$n.elf | tail -1 | awk -v n=$n '{printf "%-10s Flash %6.1f KB  RAM %5.1f KB (w tym stos 4 KB)\n", n, ($1+$2)/1024, ($2+$3)/1024}'; }
zbuduj aplikacja $D/app_main.c $D/app.ld hal hal_cortex hal_rcc hal_rcc_ex hal_pwr hal_pwr_ex hal_gpio hal_dma hal_dma_ex hal_exti hal_flash hal_flash_ex hal_adc hal_adc_ex hal_hrtim hal_fdcan hal_spi hal_spi_ex hal_rtc hal_rtc_ex hal_crc hal_crc_ex hal_tim hal_tim_ex hal_pcd hal_pcd_ex ll_usb
zbuduj bootloader $D/boot_main.c $D/boot.ld hal hal_cortex hal_rcc hal_rcc_ex hal_pwr hal_pwr_ex hal_gpio hal_dma hal_flash hal_flash_ex hal_crc hal_crc_ex hal_pcd hal_pcd_ex ll_usb

# --- HMI: STM32G474RE (od 26.11.2026 zamiast STM32G0B1) - te same biblioteki co ECU, bez USB
zbuduj_bez_usb(){ n=$1; m=$2; ld=$3; shift 3; o=$B/$n; mkdir -p $o; S="$m $C/cmsis_device_g4/Source/Templates/system_stm32g4xx.c"; for x in "$@"; do S="$S $H/Src/stm32g4xx_$x.c"; done
  for f in $S; do ${T}gcc $CF -c $f -o $o/$(basename $f .c).o; done
  ${T}gcc $CF -c $C/cmsis_device_g4/Source/Templates/gcc/startup_stm32g474xx.s -o $o/startup.o
  ${T}gcc $LF -T $ld $o/*.o -o $o/$n.elf 2>/dev/null || true; ${T}size $o/$n.elf | tail -1 | awk -v n=$n '{printf "%-10s Flash %6.1f KB  RAM %5.1f KB (w tym stos 4 KB)\n", n, ($1+$2)/1024, ($2+$3)/1024}'; }
zbuduj_bez_usb hmi $D/hmi_main.c $D/app.ld hal hal_cortex hal_rcc hal_rcc_ex hal_pwr hal_pwr_ex hal_gpio hal_dma hal_dma_ex hal_exti hal_flash hal_flash_ex hal_qspi hal_fdcan hal_i2c hal_i2c_ex hal_adc hal_adc_ex hal_iwdg hal_crc hal_crc_ex
zbuduj_bez_usb hmi_boot $D/hmi_boot_main.c $D/boot.ld hal hal_cortex hal_rcc hal_rcc_ex hal_pwr hal_pwr_ex hal_gpio hal_dma hal_flash hal_flash_ex hal_fdcan hal_iwdg hal_crc hal_crc_ex
