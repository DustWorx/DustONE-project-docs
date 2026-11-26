/* Szkielet platformy ECU: inicjalizacja i typowe wywołania peryferiów używanych przez Dust ONE.
   Cel: pomiar rozmiaru warstwy sterowników (HAL + USB), nie działający firmware. */
#include "stm32g4xx_hal.h"
#include "usbd_core.h"
#include "usbd_cdc.h"
extern USBD_DescriptorsTypeDef Class_Desc;
extern USBD_CDC_ItfTypeDef USBD_CDC_Template_fops;
USBD_HandleTypeDef husb;
HRTIM_HandleTypeDef hhrtim; ADC_HandleTypeDef hadc2,hadc3,hadc4,hadc5;
DMA_HandleTypeDef hdma_adc[4], hdma_spi[6]; FDCAN_HandleTypeDef hcan;
SPI_HandleTypeDef hspi1,hspi2,hspi3; RTC_HandleTypeDef hrtc; CRC_HandleTypeDef hcrc;
TIM_HandleTypeDef htim2,htim17; volatile uint32_t sink; uint16_t adcbuf[4][16]; uint8_t sbuf[2][256];
static void clock(void){
 RCC_OscInitTypeDef o={0}; RCC_ClkInitTypeDef c={0}; RCC_PeriphCLKInitTypeDef p={0};
 HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1_BOOST); HAL_PWR_EnableBkUpAccess();
 o.OscillatorType=RCC_OSCILLATORTYPE_HSE|RCC_OSCILLATORTYPE_LSE|RCC_OSCILLATORTYPE_HSI48;
 o.HSEState=RCC_HSE_ON;o.LSEState=RCC_LSE_ON;o.HSI48State=RCC_HSI48_ON;o.PLL.PLLState=RCC_PLL_ON;o.PLL.PLLSource=RCC_PLLSOURCE_HSE;
 o.PLL.PLLM=RCC_PLLM_DIV2;o.PLL.PLLN=85;o.PLL.PLLP=RCC_PLLP_DIV2;o.PLL.PLLQ=RCC_PLLQ_DIV2;o.PLL.PLLR=RCC_PLLR_DIV2; HAL_RCC_OscConfig(&o);
 c.ClockType=RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK|RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;c.SYSCLKSource=RCC_SYSCLKSOURCE_PLLCLK; HAL_RCC_ClockConfig(&c,FLASH_LATENCY_4);
 p.PeriphClockSelection=RCC_PERIPHCLK_USB|RCC_PERIPHCLK_FDCAN|RCC_PERIPHCLK_RTC|RCC_PERIPHCLK_ADC12|RCC_PERIPHCLK_ADC345;
 p.UsbClockSelection=RCC_USBCLKSOURCE_HSI48;p.FdcanClockSelection=RCC_FDCANCLKSOURCE_PCLK1;p.RTCClockSelection=RCC_RTCCLKSOURCE_LSE;
 p.Adc12ClockSelection=RCC_ADC12CLKSOURCE_SYSCLK;p.Adc345ClockSelection=RCC_ADC345CLKSOURCE_SYSCLK; HAL_RCCEx_PeriphCLKConfig(&p);
 HAL_RCC_EnableCSS(); }
static void gpio(void){ GPIO_InitTypeDef g={0}; __HAL_RCC_GPIOA_CLK_ENABLE();__HAL_RCC_GPIOB_CLK_ENABLE();__HAL_RCC_GPIOC_CLK_ENABLE();__HAL_RCC_GPIOD_CLK_ENABLE();__HAL_RCC_GPIOE_CLK_ENABLE();
 GPIO_TypeDef* P[5]={GPIOA,GPIOB,GPIOC,GPIOD,GPIOE};
 for(int i=0;i<5;i++){g.Pin=GPIO_PIN_All;g.Mode=GPIO_MODE_ANALOG;HAL_GPIO_Init(P[i],&g);}
 g.Pin=GPIO_PIN_0|GPIO_PIN_1;g.Mode=GPIO_MODE_OUTPUT_PP;HAL_GPIO_Init(GPIOD,&g); g.Pin=GPIO_PIN_2;g.Mode=GPIO_MODE_IT_RISING_FALLING;g.Pull=GPIO_PULLUP;HAL_GPIO_Init(GPIOE,&g);
 g.Pin=GPIO_PIN_5|GPIO_PIN_6|GPIO_PIN_7;g.Mode=GPIO_MODE_AF_PP;g.Alternate=GPIO_AF5_SPI1;HAL_GPIO_Init(GPIOA,&g);
 HAL_NVIC_SetPriority(EXTI2_IRQn,5,0);HAL_NVIC_EnableIRQ(EXTI2_IRQn); }
static void dma(DMA_HandleTypeDef*h,DMA_Channel_TypeDef*ch,uint32_t req,uint32_t dir,uint32_t al,uint32_t mode){h->Instance=ch;h->Init.Request=req;h->Init.Direction=dir;h->Init.PeriphInc=DMA_PINC_DISABLE;h->Init.MemInc=DMA_MINC_ENABLE;h->Init.PeriphDataAlignment=al;h->Init.MemDataAlignment=al;h->Init.Mode=mode;h->Init.Priority=DMA_PRIORITY_HIGH;HAL_DMA_Init(h);}
static void adc(ADC_HandleTypeDef*h,ADC_TypeDef*in,DMA_HandleTypeDef*d,DMA_Channel_TypeDef*ch,uint32_t req,uint16_t*buf){
 ADC_ChannelConfTypeDef c={0}; ADC_InjectionConfTypeDef j={0};
 h->Instance=in;h->Init.ClockPrescaler=ADC_CLOCK_SYNC_PCLK_DIV4;h->Init.Resolution=ADC_RESOLUTION_12B;h->Init.ScanConvMode=ADC_SCAN_ENABLE;h->Init.NbrOfConversion=6;
 h->Init.ExternalTrigConv=ADC_EXTERNALTRIG_HRTIM_TRG1;h->Init.ExternalTrigConvEdge=ADC_EXTERNALTRIGCONVEDGE_RISING;h->Init.DMAContinuousRequests=ENABLE;h->Init.OversamplingMode=ENABLE;h->Init.Oversampling.Ratio=ADC_OVERSAMPLING_RATIO_8;h->Init.Oversampling.RightBitShift=ADC_RIGHTBITSHIFT_3;
 HAL_ADC_Init(h); HAL_ADCEx_Calibration_Start(h,ADC_SINGLE_ENDED);
 for(int i=0;i<6;i++){c.Channel=ADC_CHANNEL_1+i;c.Rank=ADC_REGULAR_RANK_1+i;c.SamplingTime=ADC_SAMPLETIME_47CYCLES_5;c.SingleDiff=ADC_SINGLE_ENDED;HAL_ADC_ConfigChannel(h,&c);}
 j.InjectedChannel=ADC_CHANNEL_2;j.InjectedRank=ADC_INJECTED_RANK_1;j.InjectedSamplingTime=ADC_SAMPLETIME_6CYCLES_5;j.InjectedNbrOfConversion=1;j.ExternalTrigInjecConv=ADC_EXTERNALTRIGINJEC_HRTIM_TRG2;j.ExternalTrigInjecConvEdge=ADC_EXTERNALTRIGINJECCONV_EDGE_RISING;HAL_ADCEx_InjectedConfigChannel(h,&j);
 dma(d,ch,req,DMA_PERIPH_TO_MEMORY,DMA_PDATAALIGN_HALFWORD,DMA_CIRCULAR); __HAL_LINKDMA(h,DMA_Handle,*d);
 HAL_ADC_Start_DMA(h,(uint32_t*)buf,6); HAL_ADCEx_InjectedStart_IT(h); }
static void spi(SPI_HandleTypeDef*h,SPI_TypeDef*in,DMA_HandleTypeDef*tx,DMA_HandleTypeDef*rx,DMA_Channel_TypeDef*ct,DMA_Channel_TypeDef*cr,uint32_t rt,uint32_t rr){
 h->Instance=in;h->Init.Mode=SPI_MODE_MASTER;h->Init.Direction=SPI_DIRECTION_2LINES;h->Init.DataSize=SPI_DATASIZE_8BIT;h->Init.CLKPolarity=SPI_POLARITY_LOW;h->Init.CLKPhase=SPI_PHASE_1EDGE;h->Init.NSS=SPI_NSS_SOFT;h->Init.BaudRatePrescaler=SPI_BAUDRATEPRESCALER_4;h->Init.FirstBit=SPI_FIRSTBIT_MSB;h->Init.CRCCalculation=SPI_CRCCALCULATION_DISABLE;HAL_SPI_Init(h);
 dma(tx,ct,rt,DMA_MEMORY_TO_PERIPH,DMA_PDATAALIGN_BYTE,DMA_NORMAL);dma(rx,cr,rr,DMA_PERIPH_TO_MEMORY,DMA_PDATAALIGN_BYTE,DMA_NORMAL);__HAL_LINKDMA(h,hdmatx,*tx);__HAL_LINKDMA(h,hdmarx,*rx);}
static void hrtim(void){
 HRTIM_TimeBaseCfgTypeDef tb={0}; HRTIM_TimerCfgTypeDef tc={0}; HRTIM_OutputCfgTypeDef oc={0}; HRTIM_EventCfgTypeDef ev={0}; HRTIM_CompareCfgTypeDef cc={0}; HRTIM_CaptureCfgTypeDef cap={0}; HRTIM_ADCTriggerCfgTypeDef at={0};
 hhrtim.Instance=HRTIM1;hhrtim.Init.HRTIMInterruptResquests=HRTIM_IT_NONE;hhrtim.Init.SyncOptions=HRTIM_SYNCOPTION_NONE;HAL_HRTIM_Init(&hhrtim);HAL_HRTIM_DLLCalibrationStart(&hhrtim,HRTIM_CALIBRATIONRATE_3);HAL_HRTIM_PollForDLLCalibration(&hhrtim,10);
 ev.Source=HRTIM_EEV3SRC_GPIO;ev.Polarity=HRTIM_EVENTPOLARITY_HIGH;ev.Sensitivity=HRTIM_EVENTSENSITIVITY_BOTHEDGES;ev.FastMode=HRTIM_EVENTFASTMODE_DISABLE;ev.Filter=HRTIM_EVENTFILTER_NONE;HAL_HRTIM_EventConfig(&hhrtim,HRTIM_EVENT_3,&ev);HAL_HRTIM_EventConfig(&hhrtim,HRTIM_EVENT_10,&ev);
 uint32_t T[3]={HRTIM_TIMERINDEX_TIMER_A,HRTIM_TIMERINDEX_TIMER_E,HRTIM_TIMERINDEX_TIMER_F};
 for(int i=0;i<3;i++){tb.Period=0xFFDF;tb.PrescalerRatio=HRTIM_PRESCALERRATIO_DIV4;tb.Mode=HRTIM_MODE_CONTINUOUS;HAL_HRTIM_TimeBaseConfig(&hhrtim,T[i],&tb);
  tc.InterruptRequests=HRTIM_TIM_IT_CPT1|HRTIM_TIM_IT_CMP1;tc.DMARequests=HRTIM_TIM_DMA_NONE;tc.PreloadEnable=HRTIM_PRELOAD_ENABLED;tc.UpdateTrigger=HRTIM_TIMUPDATETRIGGER_NONE;tc.ResetTrigger=HRTIM_TIMRESETTRIGGER_NONE;HAL_HRTIM_WaveformTimerConfig(&hhrtim,T[i],&tc);
  cc.CompareValue=1000;HAL_HRTIM_WaveformCompareConfig(&hhrtim,T[i],HRTIM_COMPAREUNIT_1,&cc);HAL_HRTIM_WaveformCompareConfig(&hhrtim,T[i],HRTIM_COMPAREUNIT_2,&cc);
  cap.Trigger=HRTIM_CAPTURETRIGGER_EEV_3;HAL_HRTIM_WaveformCaptureConfig(&hhrtim,T[i],HRTIM_CAPTUREUNIT_1,&cap);}
 oc.Polarity=HRTIM_OUTPUTPOLARITY_HIGH;oc.SetSource=HRTIM_OUTPUTSET_TIMCMP1;oc.ResetSource=HRTIM_OUTPUTRESET_TIMCMP2;oc.IdleMode=HRTIM_OUTPUTIDLEMODE_NONE;oc.IdleLevel=HRTIM_OUTPUTIDLELEVEL_INACTIVE;oc.FaultLevel=HRTIM_OUTPUTFAULTLEVEL_INACTIVE;
 HAL_HRTIM_WaveformOutputConfig(&hhrtim,HRTIM_TIMERINDEX_TIMER_A,HRTIM_OUTPUT_TA1,&oc);HAL_HRTIM_WaveformOutputConfig(&hhrtim,HRTIM_TIMERINDEX_TIMER_E,HRTIM_OUTPUT_TE1,&oc);HAL_HRTIM_WaveformOutputConfig(&hhrtim,HRTIM_TIMERINDEX_TIMER_F,HRTIM_OUTPUT_TF2,&oc);
 at.UpdateSource=HRTIM_ADCTRIGGERUPDATE_TIMER_A;at.Trigger=HRTIM_ADCTRIGGEREVENT13_TIMERA_CMP3;HAL_HRTIM_ADCTriggerConfig(&hhrtim,HRTIM_ADCTRIGGER_1,&at);
 HAL_HRTIM_WaveformOutputStart(&hhrtim,HRTIM_OUTPUT_TA1|HRTIM_OUTPUT_TE1|HRTIM_OUTPUT_TF2);HAL_HRTIM_WaveformCountStart_IT(&hhrtim,HRTIM_TIMERID_TIMER_A|HRTIM_TIMERID_TIMER_E|HRTIM_TIMERID_TIMER_F);
 HAL_NVIC_SetPriority(HRTIM1_TIMA_IRQn,0,0);HAL_NVIC_EnableIRQ(HRTIM1_TIMA_IRQn); }
static void can(void){ FDCAN_FilterTypeDef f={0};
 hcan.Instance=FDCAN1;hcan.Init.ClockDivider=FDCAN_CLOCK_DIV1;hcan.Init.FrameFormat=FDCAN_FRAME_CLASSIC;hcan.Init.Mode=FDCAN_MODE_NORMAL;hcan.Init.AutoRetransmission=ENABLE;hcan.Init.NominalPrescaler=17;hcan.Init.NominalSyncJumpWidth=4;hcan.Init.NominalTimeSeg1=15;hcan.Init.NominalTimeSeg2=4;hcan.Init.StdFiltersNbr=8;hcan.Init.TxFifoQueueMode=FDCAN_TX_FIFO_OPERATION;HAL_FDCAN_Init(&hcan);
 f.IdType=FDCAN_STANDARD_ID;f.FilterIndex=0;f.FilterType=FDCAN_FILTER_MASK;f.FilterConfig=FDCAN_FILTER_TO_RXFIFO0;f.FilterID1=0x100;f.FilterID2=0x700;HAL_FDCAN_ConfigFilter(&hcan,&f);
 HAL_FDCAN_ConfigGlobalFilter(&hcan,FDCAN_REJECT,FDCAN_REJECT,FDCAN_REJECT_REMOTE,FDCAN_REJECT_REMOTE);
 HAL_FDCAN_ActivateNotification(&hcan,FDCAN_IT_RX_FIFO0_NEW_MESSAGE|FDCAN_IT_BUS_OFF|FDCAN_IT_ERROR_PASSIVE,0);HAL_FDCAN_Start(&hcan);HAL_NVIC_EnableIRQ(FDCAN1_IT0_IRQn);}
void HAL_FDCAN_RxFifo0Callback(FDCAN_HandleTypeDef*h,uint32_t it){FDCAN_RxHeaderTypeDef r;uint8_t d[8];(void)it;if(HAL_FDCAN_GetRxMessage(h,FDCAN_RX_FIFO0,&r,d)==HAL_OK)sink+=d[0];}
static void can_tx(uint32_t id,uint8_t*d){FDCAN_TxHeaderTypeDef t={0};t.Identifier=id;t.IdType=FDCAN_STANDARD_ID;t.TxFrameType=FDCAN_DATA_FRAME;t.DataLength=FDCAN_DLC_BYTES_8;t.FDFormat=FDCAN_CLASSIC_CAN;if(HAL_FDCAN_GetTxFifoFreeLevel(&hcan))HAL_FDCAN_AddMessageToTxFifoQ(&hcan,&t,d);
 FDCAN_ErrorCountersTypeDef e;FDCAN_ProtocolStatusTypeDef ps;HAL_FDCAN_GetErrorCounters(&hcan,&e);HAL_FDCAN_GetProtocolStatus(&hcan,&ps);sink+=e.TxErrorCnt+ps.BusOff;}
static void rtc(void){ RTC_TimeTypeDef t={0}; RTC_DateTypeDef d={0}; hrtc.Instance=RTC;hrtc.Init.HourFormat=RTC_HOURFORMAT_24;hrtc.Init.AsynchPrediv=127;hrtc.Init.SynchPrediv=255;HAL_RTC_Init(&hrtc);
 if(HAL_RTCEx_BKUPRead(&hrtc,RTC_BKP_DR0)!=0x5A5A){HAL_RTC_SetTime(&hrtc,&t,RTC_FORMAT_BIN);HAL_RTC_SetDate(&hrtc,&d,RTC_FORMAT_BIN);HAL_RTCEx_BKUPWrite(&hrtc,RTC_BKP_DR0,0x5A5A);}
 HAL_RTC_GetTime(&hrtc,&t,RTC_FORMAT_BIN);HAL_RTC_GetDate(&hrtc,&d,RTC_FORMAT_BIN);sink+=t.Seconds+d.Year;}
static void tim(void){ TIM_OC_InitTypeDef oc={0}; TIM_IC_InitTypeDef ic={0};
 htim2.Instance=TIM2;htim2.Init.Prescaler=169;htim2.Init.Period=999;HAL_TIM_PWM_Init(&htim2);oc.OCMode=TIM_OCMODE_PWM1;oc.Pulse=500;HAL_TIM_PWM_ConfigChannel(&htim2,&oc,TIM_CHANNEL_2);HAL_TIM_PWM_Start(&htim2,TIM_CHANNEL_2);
 htim17.Instance=TIM17;htim17.Init.Prescaler=169;htim17.Init.Period=0xFFFF;HAL_TIM_IC_Init(&htim17);ic.ICPolarity=TIM_ICPOLARITY_FALLING;ic.ICSelection=TIM_ICSELECTION_DIRECTTI;ic.ICFilter=15;HAL_TIM_IC_ConfigChannel(&htim17,&ic,TIM_CHANNEL_1);HAL_TIM_IC_Start_IT(&htim17,TIM_CHANNEL_1);}
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef*h){sink+=HAL_TIM_ReadCapturedValue(h,TIM_CHANNEL_1);}
static void flash_ops(void){ FLASH_EraseInitTypeDef e={0}; uint32_t err; FLASH_OBProgramInitTypeDef ob={0};
 HAL_FLASH_Unlock();e.TypeErase=FLASH_TYPEERASE_PAGES;e.Banks=FLASH_BANK_2;e.Page=0;e.NbPages=1;HAL_FLASHEx_Erase(&e,&err);HAL_FLASH_Program(FLASH_TYPEPROGRAM_DOUBLEWORD,0x08040000,0x1122334455667788ULL);HAL_FLASH_Lock();HAL_FLASHEx_OBGetConfig(&ob);sink+=ob.WRPStartOffset;}
int main(void){
 HAL_Init(); clock(); gpio(); __HAL_RCC_DMA1_CLK_ENABLE();__HAL_RCC_DMA2_CLK_ENABLE();__HAL_RCC_DMAMUX1_CLK_ENABLE();
 hrtim();
 adc(&hadc2,ADC2,&hdma_adc[0],DMA1_Channel1,DMA_REQUEST_ADC2,adcbuf[0]);adc(&hadc3,ADC3,&hdma_adc[1],DMA1_Channel2,DMA_REQUEST_ADC3,adcbuf[1]);
 adc(&hadc4,ADC4,&hdma_adc[2],DMA1_Channel3,DMA_REQUEST_ADC4,adcbuf[2]);adc(&hadc5,ADC5,&hdma_adc[3],DMA1_Channel4,DMA_REQUEST_ADC5,adcbuf[3]);
 spi(&hspi1,SPI1,&hdma_spi[0],&hdma_spi[1],DMA2_Channel1,DMA2_Channel2,DMA_REQUEST_SPI1_TX,DMA_REQUEST_SPI1_RX);
 spi(&hspi2,SPI2,&hdma_spi[2],&hdma_spi[3],DMA2_Channel3,DMA2_Channel4,DMA_REQUEST_SPI2_TX,DMA_REQUEST_SPI2_RX);
 spi(&hspi3,SPI3,&hdma_spi[4],&hdma_spi[5],DMA2_Channel5,DMA2_Channel6,DMA_REQUEST_SPI3_TX,DMA_REQUEST_SPI3_RX);
 can(); rtc(); tim(); hcrc.Instance=CRC;HAL_CRC_Init(&hcrc);
 USBD_Init(&husb,&Class_Desc,0);USBD_RegisterClass(&husb,USBD_CDC_CLASS);USBD_CDC_RegisterInterface(&husb,&USBD_CDC_Template_fops);USBD_Start(&husb);
 for(;;){
  HAL_SPI_TransmitReceive_DMA(&hspi1,sbuf[0],sbuf[1],256);HAL_SPI_TransmitReceive(&hspi2,sbuf[0],sbuf[1],8,2);HAL_SPI_Transmit(&hspi3,sbuf[0],4,2);HAL_SPI_Receive(&hspi3,sbuf[1],4,2);
  sink+=HAL_ADCEx_InjectedGetValue(&hadc2,ADC_INJECTED_RANK_1); sink+=HAL_CRC_Calculate(&hcrc,(uint32_t*)sbuf[0],64);
  can_tx(0x101,sbuf[0]); HAL_GPIO_TogglePin(GPIOD,GPIO_PIN_0); sink+=HAL_GPIO_ReadPin(GPIOE,GPIO_PIN_2);
  __HAL_HRTIM_SETCOMPARE(&hhrtim,HRTIM_TIMERINDEX_TIMER_A,HRTIM_COMPAREUNIT_1,sink&0xFFF);sink+=HAL_HRTIM_GetCapturedValue(&hhrtim,HRTIM_TIMERINDEX_TIMER_A,HRTIM_CAPTUREUNIT_1);
  USBD_CDC_SetTxBuffer(&husb,sbuf[0],64);USBD_CDC_TransmitPacket(&husb);USBD_CDC_ReceivePacket(&husb);
  if(sink==12345u)flash_ops(); rtc();
 } }
void SysTick_Handler(void){HAL_IncTick();}
void HRTIM1_TIMA_IRQHandler(void){HAL_HRTIM_IRQHandler(&hhrtim,HRTIM_TIMERINDEX_TIMER_A);}
void HRTIM1_TIME_IRQHandler(void){HAL_HRTIM_IRQHandler(&hhrtim,HRTIM_TIMERINDEX_TIMER_E);}
void ADC3_IRQHandler(void){HAL_ADC_IRQHandler(&hadc3);} void ADC1_2_IRQHandler(void){HAL_ADC_IRQHandler(&hadc2);}
void ADC4_IRQHandler(void){HAL_ADC_IRQHandler(&hadc4);} void ADC5_IRQHandler(void){HAL_ADC_IRQHandler(&hadc5);}
void DMA1_Channel1_IRQHandler(void){HAL_DMA_IRQHandler(&hdma_adc[0]);} void DMA2_Channel1_IRQHandler(void){HAL_DMA_IRQHandler(&hdma_spi[0]);} void DMA2_Channel2_IRQHandler(void){HAL_DMA_IRQHandler(&hdma_spi[1]);}
void SPI1_IRQHandler(void){HAL_SPI_IRQHandler(&hspi1);} void FDCAN1_IT0_IRQHandler(void){HAL_FDCAN_IRQHandler(&hcan);}
void TIM1_TRG_COM_TIM17_IRQHandler(void){HAL_TIM_IRQHandler(&htim17);} void EXTI2_IRQHandler(void){HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_2);}
