/* Szkielet bootloadera HMI (STM32G474RE): zegar, FDCAN (odbiór obrazu od ECU), FLASH, CRC, IWDG. Bez logiki rekordów. */
#include "stm32g4xx_hal.h"
FDCAN_HandleTypeDef hcan; CRC_HandleTypeDef hcrc; IWDG_HandleTypeDef hiwdg; volatile uint32_t sink; uint8_t buf[64];
int main(void){ RCC_OscInitTypeDef o={0}; RCC_ClkInitTypeDef c={0}; RCC_PeriphCLKInitTypeDef p={0}; FDCAN_FilterTypeDef f={0}; FLASH_EraseInitTypeDef e={0}; uint32_t err;
 HAL_Init();o.OscillatorType=RCC_OSCILLATORTYPE_HSE;o.HSEState=RCC_HSE_ON;o.PLL.PLLState=RCC_PLL_ON;o.PLL.PLLSource=RCC_PLLSOURCE_HSE;o.PLL.PLLM=RCC_PLLM_DIV2;o.PLL.PLLN=85;o.PLL.PLLP=RCC_PLLP_DIV2;o.PLL.PLLQ=RCC_PLLQ_DIV2;o.PLL.PLLR=RCC_PLLR_DIV2;HAL_RCC_OscConfig(&o);
 c.ClockType=RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK|RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;c.SYSCLKSource=RCC_SYSCLKSOURCE_PLLCLK;HAL_RCC_ClockConfig(&c,FLASH_LATENCY_4);
 p.PeriphClockSelection=RCC_PERIPHCLK_FDCAN;p.FdcanClockSelection=RCC_FDCANCLKSOURCE_PCLK1;HAL_RCCEx_PeriphCLKConfig(&p);
 hcan.Instance=FDCAN1;hcan.Init.FrameFormat=FDCAN_FRAME_CLASSIC;hcan.Init.Mode=FDCAN_MODE_NORMAL;hcan.Init.NominalPrescaler=17;hcan.Init.NominalSyncJumpWidth=4;hcan.Init.NominalTimeSeg1=15;hcan.Init.NominalTimeSeg2=4;hcan.Init.StdFiltersNbr=2;HAL_FDCAN_Init(&hcan);
 f.IdType=FDCAN_STANDARD_ID;f.FilterType=FDCAN_FILTER_MASK;f.FilterConfig=FDCAN_FILTER_TO_RXFIFO0;f.FilterID1=0x700;f.FilterID2=0x7F0;HAL_FDCAN_ConfigFilter(&hcan,&f);HAL_FDCAN_Start(&hcan);
 hcrc.Instance=CRC;HAL_CRC_Init(&hcrc);hiwdg.Instance=IWDG;hiwdg.Init.Prescaler=IWDG_PRESCALER_32;hiwdg.Init.Reload=500;hiwdg.Init.Window=IWDG_WINDOW_DISABLE;HAL_IWDG_Init(&hiwdg);
 for(;;){ FDCAN_RxHeaderTypeDef r;FDCAN_TxHeaderTypeDef t={0};uint8_t d[8]={0};
  if(HAL_FDCAN_GetRxMessage(&hcan,FDCAN_RX_FIFO0,&r,d)==HAL_OK){buf[sink&63]=d[0];sink++;}
  t.Identifier=0x7F1;t.IdType=FDCAN_STANDARD_ID;t.TxFrameType=FDCAN_DATA_FRAME;t.DataLength=FDCAN_DLC_BYTES_8;t.FDFormat=FDCAN_CLASSIC_CAN;HAL_FDCAN_AddMessageToTxFifoQ(&hcan,&t,d);
  sink+=HAL_CRC_Calculate(&hcrc,(uint32_t*)buf,16);HAL_IWDG_Refresh(&hiwdg);
  if(sink==7u){HAL_FLASH_Unlock();e.TypeErase=FLASH_TYPEERASE_PAGES;e.Banks=FLASH_BANK_2;e.NbPages=1;HAL_FLASHEx_Erase(&e,&err);HAL_FLASH_Program(FLASH_TYPEPROGRAM_DOUBLEWORD,0x08040000,sink);HAL_FLASH_Lock();}}}
void SysTick_Handler(void){HAL_IncTick();}
