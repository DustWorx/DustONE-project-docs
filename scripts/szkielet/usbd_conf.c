#include "stm32g4xx_hal.h"
#include "usbd_core.h"
#include "usbd_cdc.h"
PCD_HandleTypeDef hpcd;
void HAL_PCD_SetupStageCallback(PCD_HandleTypeDef *h){USBD_LL_SetupStage(h->pData,(uint8_t*)h->Setup);}
void HAL_PCD_DataOutStageCallback(PCD_HandleTypeDef *h,uint8_t ep){USBD_LL_DataOutStage(h->pData,ep,h->OUT_ep[ep].xfer_buff);}
void HAL_PCD_DataInStageCallback(PCD_HandleTypeDef *h,uint8_t ep){USBD_LL_DataInStage(h->pData,ep,h->IN_ep[ep].xfer_buff);}
void HAL_PCD_SOFCallback(PCD_HandleTypeDef *h){USBD_LL_SOF(h->pData);}
void HAL_PCD_ResetCallback(PCD_HandleTypeDef *h){USBD_LL_SetSpeed(h->pData,USBD_SPEED_FULL);USBD_LL_Reset(h->pData);}
void HAL_PCD_SuspendCallback(PCD_HandleTypeDef *h){USBD_LL_Suspend(h->pData);}
void HAL_PCD_ResumeCallback(PCD_HandleTypeDef *h){USBD_LL_Resume(h->pData);}
void HAL_PCD_ISOOUTIncompleteCallback(PCD_HandleTypeDef *h,uint8_t ep){USBD_LL_IsoOUTIncomplete(h->pData,ep);}
void HAL_PCD_ISOINIncompleteCallback(PCD_HandleTypeDef *h,uint8_t ep){USBD_LL_IsoINIncomplete(h->pData,ep);}
void HAL_PCD_ConnectCallback(PCD_HandleTypeDef *h){USBD_LL_DevConnected(h->pData);}
void HAL_PCD_DisconnectCallback(PCD_HandleTypeDef *h){USBD_LL_DevDisconnected(h->pData);}
static USBD_StatusTypeDef st(HAL_StatusTypeDef s){return s==HAL_OK?USBD_OK:(s==HAL_BUSY?USBD_BUSY:USBD_FAIL);}
USBD_StatusTypeDef USBD_LL_Init(USBD_HandleTypeDef *p){hpcd.pData=p;p->pData=&hpcd;hpcd.Instance=USB;hpcd.Init.dev_endpoints=8;hpcd.Init.speed=PCD_SPEED_FULL;hpcd.Init.phy_itface=PCD_PHY_EMBEDDED;hpcd.Init.Sof_enable=DISABLE;hpcd.Init.low_power_enable=DISABLE;hpcd.Init.lpm_enable=DISABLE;hpcd.Init.battery_charging_enable=DISABLE;
 if(HAL_PCD_Init(&hpcd)!=HAL_OK)return USBD_FAIL;
 HAL_PCDEx_PMAConfig(&hpcd,0x00,PCD_SNG_BUF,0x18);HAL_PCDEx_PMAConfig(&hpcd,0x80,PCD_SNG_BUF,0x58);HAL_PCDEx_PMAConfig(&hpcd,0x81,PCD_SNG_BUF,0xC0);HAL_PCDEx_PMAConfig(&hpcd,0x01,PCD_SNG_BUF,0x110);HAL_PCDEx_PMAConfig(&hpcd,0x82,PCD_SNG_BUF,0x100);return USBD_OK;}
USBD_StatusTypeDef USBD_LL_DeInit(USBD_HandleTypeDef *p){return st(HAL_PCD_DeInit(p->pData));}
USBD_StatusTypeDef USBD_LL_Start(USBD_HandleTypeDef *p){return st(HAL_PCD_Start(p->pData));}
USBD_StatusTypeDef USBD_LL_Stop(USBD_HandleTypeDef *p){return st(HAL_PCD_Stop(p->pData));}
USBD_StatusTypeDef USBD_LL_OpenEP(USBD_HandleTypeDef *p,uint8_t a,uint8_t t,uint16_t m){return st(HAL_PCD_EP_Open(p->pData,a,m,t));}
USBD_StatusTypeDef USBD_LL_CloseEP(USBD_HandleTypeDef *p,uint8_t a){return st(HAL_PCD_EP_Close(p->pData,a));}
USBD_StatusTypeDef USBD_LL_FlushEP(USBD_HandleTypeDef *p,uint8_t a){return st(HAL_PCD_EP_Flush(p->pData,a));}
USBD_StatusTypeDef USBD_LL_StallEP(USBD_HandleTypeDef *p,uint8_t a){return st(HAL_PCD_EP_SetStall(p->pData,a));}
USBD_StatusTypeDef USBD_LL_ClearStallEP(USBD_HandleTypeDef *p,uint8_t a){return st(HAL_PCD_EP_ClrStall(p->pData,a));}
uint8_t USBD_LL_IsStallEP(USBD_HandleTypeDef *p,uint8_t a){PCD_HandleTypeDef*h=p->pData;return (a&0x80)?h->IN_ep[a&0x7F].is_stall:h->OUT_ep[a&0x7F].is_stall;}
USBD_StatusTypeDef USBD_LL_SetUSBAddress(USBD_HandleTypeDef *p,uint8_t a){return st(HAL_PCD_SetAddress(p->pData,a));}
USBD_StatusTypeDef USBD_LL_Transmit(USBD_HandleTypeDef *p,uint8_t a,uint8_t *b,uint32_t n){return st(HAL_PCD_EP_Transmit(p->pData,a,b,n));}
USBD_StatusTypeDef USBD_LL_PrepareReceive(USBD_HandleTypeDef *p,uint8_t a,uint8_t *b,uint32_t n){return st(HAL_PCD_EP_Receive(p->pData,a,b,n));}
uint32_t USBD_LL_GetRxDataSize(USBD_HandleTypeDef *p,uint8_t a){return HAL_PCD_EP_GetRxCount(p->pData,a);}
void USBD_LL_Delay(uint32_t d){HAL_Delay(d);}
void *USBD_static_malloc(uint32_t size){static uint32_t mem[(sizeof(USBD_CDC_HandleTypeDef)/4)+1];(void)size;return mem;}
void USBD_static_free(void *p){(void)p;}
void USB_LP_IRQHandler(void){HAL_PCD_IRQHandler(&hpcd);}
