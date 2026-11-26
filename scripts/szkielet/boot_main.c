/* Szkielet bootloadera: zegar, GPIO, USB CDC (odzyskiwanie), FLASH, CRC. Bez logiki rekordów. */
#include "stm32g4xx_hal.h"
#include "usbd_core.h"
#include "usbd_cdc.h"
extern USBD_DescriptorsTypeDef Class_Desc; extern USBD_CDC_ItfTypeDef USBD_CDC_Template_fops;
USBD_HandleTypeDef husb; CRC_HandleTypeDef hcrc; volatile uint32_t sink; uint8_t buf[256];
static void clock(void){ RCC_OscInitTypeDef o={0}; RCC_ClkInitTypeDef c={0}; RCC_PeriphCLKInitTypeDef p={0};
 HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1_BOOST);
 o.OscillatorType=RCC_OSCILLATORTYPE_HSE|RCC_OSCILLATORTYPE_HSI48;o.HSEState=RCC_HSE_ON;o.HSI48State=RCC_HSI48_ON;o.PLL.PLLState=RCC_PLL_ON;o.PLL.PLLSource=RCC_PLLSOURCE_HSE;o.PLL.PLLM=RCC_PLLM_DIV2;o.PLL.PLLN=85;o.PLL.PLLP=RCC_PLLP_DIV2;o.PLL.PLLQ=RCC_PLLQ_DIV2;o.PLL.PLLR=RCC_PLLR_DIV2;HAL_RCC_OscConfig(&o);
 c.ClockType=RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK|RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;c.SYSCLKSource=RCC_SYSCLKSOURCE_PLLCLK;HAL_RCC_ClockConfig(&c,FLASH_LATENCY_4);
 p.PeriphClockSelection=RCC_PERIPHCLK_USB;p.UsbClockSelection=RCC_USBCLKSOURCE_HSI48;HAL_RCCEx_PeriphCLKConfig(&p);}
int main(void){ FLASH_EraseInitTypeDef e={0}; uint32_t err; GPIO_InitTypeDef g={0};
 HAL_Init();clock();__HAL_RCC_GPIOD_CLK_ENABLE();g.Pin=GPIO_PIN_0;g.Mode=GPIO_MODE_INPUT;HAL_GPIO_Init(GPIOD,&g);
 hcrc.Instance=CRC;HAL_CRC_Init(&hcrc);
 USBD_Init(&husb,&Class_Desc,0);USBD_RegisterClass(&husb,USBD_CDC_CLASS);USBD_CDC_RegisterInterface(&husb,&USBD_CDC_Template_fops);USBD_Start(&husb);
 for(;;){ USBD_CDC_SetTxBuffer(&husb,buf,64);USBD_CDC_TransmitPacket(&husb);USBD_CDC_ReceivePacket(&husb);
  sink+=HAL_CRC_Calculate(&hcrc,(uint32_t*)buf,64)+HAL_GPIO_ReadPin(GPIOD,GPIO_PIN_0);
  if(sink==7u){HAL_FLASH_Unlock();e.TypeErase=FLASH_TYPEERASE_PAGES;e.Banks=FLASH_BANK_2;e.NbPages=1;HAL_FLASHEx_Erase(&e,&err);HAL_FLASH_Program(FLASH_TYPEPROGRAM_DOUBLEWORD,0x08040000,sink);HAL_FLASH_Lock();}}}
void SysTick_Handler(void){HAL_IncTick();}
