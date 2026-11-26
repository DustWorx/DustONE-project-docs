/* Szkielet platformy HMI (STM32G474RE): zegar, GPIO, DMA, Quad-SPI do EVE4 (BT817Q), FDCAN,
   I2C (czujniki temperatury i światła), ADC (drabinka przycisków, rewizja płytki), IWDG, FLASH, CRC.
   Cel: pomiar rozmiaru warstwy sterowników (HAL), nie działający firmware. */
#include "stm32g4xx_hal.h"
QSPI_HandleTypeDef hqspi; DMA_HandleTypeDef hdq,hdadc; FDCAN_HandleTypeDef hcan; I2C_HandleTypeDef hi2c;
ADC_HandleTypeDef hadc; IWDG_HandleTypeDef hiwdg; CRC_HandleTypeDef hcrc; volatile uint32_t sink; uint8_t buf[2][256]; uint16_t abuf[4];
static void clock(void){ RCC_OscInitTypeDef o={0}; RCC_ClkInitTypeDef c={0}; RCC_PeriphCLKInitTypeDef p={0};
 HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1_BOOST);
 o.OscillatorType=RCC_OSCILLATORTYPE_HSE|RCC_OSCILLATORTYPE_LSI;o.HSEState=RCC_HSE_ON;o.LSIState=RCC_LSI_ON;o.PLL.PLLState=RCC_PLL_ON;o.PLL.PLLSource=RCC_PLLSOURCE_HSE;
 o.PLL.PLLM=RCC_PLLM_DIV2;o.PLL.PLLN=85;o.PLL.PLLP=RCC_PLLP_DIV2;o.PLL.PLLQ=RCC_PLLQ_DIV2;o.PLL.PLLR=RCC_PLLR_DIV2;HAL_RCC_OscConfig(&o);
 c.ClockType=RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK|RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;c.SYSCLKSource=RCC_SYSCLKSOURCE_PLLCLK;HAL_RCC_ClockConfig(&c,FLASH_LATENCY_4);
 p.PeriphClockSelection=RCC_PERIPHCLK_FDCAN|RCC_PERIPHCLK_I2C1|RCC_PERIPHCLK_ADC12|RCC_PERIPHCLK_QSPI;p.FdcanClockSelection=RCC_FDCANCLKSOURCE_PCLK1;p.I2c1ClockSelection=RCC_I2C1CLKSOURCE_PCLK1;p.Adc12ClockSelection=RCC_ADC12CLKSOURCE_SYSCLK;p.QspiClockSelection=RCC_QSPICLKSOURCE_SYSCLK;HAL_RCCEx_PeriphCLKConfig(&p);}
static void dma(DMA_HandleTypeDef*h,DMA_Channel_TypeDef*ch,uint32_t req,uint32_t dir,uint32_t al,uint32_t mode){h->Instance=ch;h->Init.Request=req;h->Init.Direction=dir;h->Init.PeriphInc=DMA_PINC_DISABLE;h->Init.MemInc=DMA_MINC_ENABLE;h->Init.PeriphDataAlignment=al;h->Init.MemDataAlignment=al;h->Init.Mode=mode;h->Init.Priority=DMA_PRIORITY_HIGH;HAL_DMA_Init(h);}
int main(void){ GPIO_InitTypeDef g={0}; FDCAN_FilterTypeDef f={0}; ADC_ChannelConfTypeDef ac={0}; FLASH_EraseInitTypeDef e={0}; QSPI_CommandTypeDef q={0}; uint32_t err;
 HAL_Init();clock();__HAL_RCC_GPIOA_CLK_ENABLE();__HAL_RCC_GPIOB_CLK_ENABLE();__HAL_RCC_DMA1_CLK_ENABLE();__HAL_RCC_DMAMUX1_CLK_ENABLE();
 g.Pin=GPIO_PIN_4|GPIO_PIN_8;g.Mode=GPIO_MODE_OUTPUT_PP;HAL_GPIO_Init(GPIOA,&g);g.Pin=GPIO_PIN_3;g.Mode=GPIO_MODE_IT_FALLING;g.Pull=GPIO_PULLUP;HAL_GPIO_Init(GPIOB,&g);HAL_NVIC_EnableIRQ(EXTI3_IRQn);
 hqspi.Instance=QUADSPI;hqspi.Init.ClockPrescaler=3;hqspi.Init.FifoThreshold=4;hqspi.Init.SampleShifting=QSPI_SAMPLE_SHIFTING_HALFCYCLE;hqspi.Init.FlashSize=22;hqspi.Init.ChipSelectHighTime=QSPI_CS_HIGH_TIME_1_CYCLE;hqspi.Init.ClockMode=QSPI_CLOCK_MODE_0;HAL_QSPI_Init(&hqspi);
 dma(&hdq,DMA1_Channel1,DMA_REQUEST_QUADSPI,DMA_MEMORY_TO_PERIPH,DMA_PDATAALIGN_BYTE,DMA_NORMAL);__HAL_LINKDMA(&hqspi,hdma,hdq);
 hcan.Instance=FDCAN1;hcan.Init.ClockDivider=FDCAN_CLOCK_DIV1;hcan.Init.FrameFormat=FDCAN_FRAME_CLASSIC;hcan.Init.Mode=FDCAN_MODE_NORMAL;hcan.Init.AutoRetransmission=ENABLE;hcan.Init.NominalPrescaler=17;hcan.Init.NominalSyncJumpWidth=4;hcan.Init.NominalTimeSeg1=15;hcan.Init.NominalTimeSeg2=4;hcan.Init.StdFiltersNbr=4;hcan.Init.TxFifoQueueMode=FDCAN_TX_FIFO_OPERATION;HAL_FDCAN_Init(&hcan);
 f.IdType=FDCAN_STANDARD_ID;f.FilterType=FDCAN_FILTER_MASK;f.FilterConfig=FDCAN_FILTER_TO_RXFIFO0;f.FilterID1=0x100;f.FilterID2=0x700;HAL_FDCAN_ConfigFilter(&hcan,&f);HAL_FDCAN_ConfigGlobalFilter(&hcan,FDCAN_REJECT,FDCAN_REJECT,FDCAN_REJECT_REMOTE,FDCAN_REJECT_REMOTE);
 HAL_FDCAN_ActivateNotification(&hcan,FDCAN_IT_RX_FIFO0_NEW_MESSAGE|FDCAN_IT_BUS_OFF,0);HAL_FDCAN_Start(&hcan);HAL_NVIC_EnableIRQ(FDCAN1_IT0_IRQn);
 hi2c.Instance=I2C1;hi2c.Init.Timing=0x30A0A7FB;hi2c.Init.AddressingMode=I2C_ADDRESSINGMODE_7BIT;HAL_I2C_Init(&hi2c);
 hadc.Instance=ADC1;hadc.Init.ClockPrescaler=ADC_CLOCK_SYNC_PCLK_DIV4;hadc.Init.Resolution=ADC_RESOLUTION_12B;hadc.Init.ScanConvMode=ADC_SCAN_ENABLE;hadc.Init.NbrOfConversion=2;hadc.Init.DMAContinuousRequests=ENABLE;HAL_ADC_Init(&hadc);HAL_ADCEx_Calibration_Start(&hadc,ADC_SINGLE_ENDED);
 ac.Channel=ADC_CHANNEL_1;ac.Rank=ADC_REGULAR_RANK_1;ac.SamplingTime=ADC_SAMPLETIME_47CYCLES_5;ac.SingleDiff=ADC_SINGLE_ENDED;HAL_ADC_ConfigChannel(&hadc,&ac);ac.Channel=ADC_CHANNEL_2;ac.Rank=ADC_REGULAR_RANK_2;HAL_ADC_ConfigChannel(&hadc,&ac);
 dma(&hdadc,DMA1_Channel2,DMA_REQUEST_ADC1,DMA_PERIPH_TO_MEMORY,DMA_PDATAALIGN_HALFWORD,DMA_NORMAL);__HAL_LINKDMA(&hadc,DMA_Handle,hdadc);
 hiwdg.Instance=IWDG;hiwdg.Init.Prescaler=IWDG_PRESCALER_32;hiwdg.Init.Reload=500;hiwdg.Init.Window=IWDG_WINDOW_DISABLE;HAL_IWDG_Init(&hiwdg);
 hcrc.Instance=CRC;HAL_CRC_Init(&hcrc);
 for(;;){ FDCAN_TxHeaderTypeDef t={0};FDCAN_RxHeaderTypeDef r;uint8_t d[8]={0};
  q.Instruction=0xB0;q.InstructionMode=QSPI_INSTRUCTION_1_LINE;q.AddressMode=QSPI_ADDRESS_4_LINES;q.AddressSize=QSPI_ADDRESS_24_BITS;q.Address=0x302578;q.DataMode=QSPI_DATA_4_LINES;q.NbData=256;
  HAL_QSPI_Command(&hqspi,&q,2);HAL_QSPI_Transmit_DMA(&hqspi,buf[0]);q.NbData=4;HAL_QSPI_Command(&hqspi,&q,2);HAL_QSPI_Receive(&hqspi,buf[1],2);
  HAL_I2C_Mem_Read(&hi2c,0x90,0x00,I2C_MEMADD_SIZE_8BIT,buf[1],2,5);HAL_I2C_Mem_Write(&hi2c,0x52,0x01,I2C_MEMADD_SIZE_8BIT,buf[0],1,5);
  HAL_ADC_Start_DMA(&hadc,(uint32_t*)abuf,2);
  t.Identifier=0x201;t.IdType=FDCAN_STANDARD_ID;t.TxFrameType=FDCAN_DATA_FRAME;t.DataLength=FDCAN_DLC_BYTES_8;t.FDFormat=FDCAN_CLASSIC_CAN;HAL_FDCAN_AddMessageToTxFifoQ(&hcan,&t,d);
  if(HAL_FDCAN_GetRxMessage(&hcan,FDCAN_RX_FIFO0,&r,d)==HAL_OK)sink+=d[0];
  sink+=HAL_CRC_Calculate(&hcrc,(uint32_t*)buf[0],64)+abuf[0];HAL_IWDG_Refresh(&hiwdg);HAL_GPIO_TogglePin(GPIOA,GPIO_PIN_4);
  if(sink==7u){HAL_FLASH_Unlock();e.TypeErase=FLASH_TYPEERASE_PAGES;e.Banks=FLASH_BANK_2;e.NbPages=1;HAL_FLASHEx_Erase(&e,&err);HAL_FLASH_Program(FLASH_TYPEPROGRAM_DOUBLEWORD,0x08040000,sink);HAL_FLASH_Lock();}}}
void SysTick_Handler(void){HAL_IncTick();}
void DMA1_Channel1_IRQHandler(void){HAL_DMA_IRQHandler(&hdq);} void FDCAN1_IT0_IRQHandler(void){HAL_FDCAN_IRQHandler(&hcan);}
void EXTI3_IRQHandler(void){HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_3);} void QUADSPI_IRQHandler(void){HAL_QSPI_IRQHandler(&hqspi);}
