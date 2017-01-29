#include <string.h>
#include <jendefs.h>
#include <AppHardwareApi.h>
#include "utils.h"
#include "PingPong.h"
#include "config.h"
#include "Version.h"
#include "serial.h"
#include "fprintf.h"
#include "sprintf.h"
#include "ToCoNet.h"
#include "ToCoNet_mod_prototype.h"
#include "app_event.h"

typedef struct
{
    // MAC
    uint8 u8channel;
    uint16 u16addr;

    // LED Counter
    uint32 u32LedCt;

    // シーケンス番号
    uint32 u32Seq;

    // スリープカウンタ
    uint8 u8SleepCt;
} tsAppData;

static void vProcessEvCore(tsEvent *pEv, teEvent eEvent, uint32 u32evarg);
static void vInitHardware(int f_warm_start);
void vSerialInit(uint32 u32Baud, tsUartOpt *pUartOpt);
static void vHandleSerialInput(void);
static tsAppData sAppData;
PUBLIC tsFILE sSerStream;
tsSerialPortSetup sSerPort;
// Wakeup port
const uint32 u32DioPortWakeUp = 1UL << 7; // UART Rx Port
static int id = 0;

void cbAppColdStart(bool_t bAfterAhiInit)
{
	//static uint8 u8WkState;
	if (!bAfterAhiInit) {
		// before AHI init, very first of code.

		// Register modules
		ToCoNet_REG_MOD_ALL();

	} else {
		// disable brown out detect
		vAHI_BrownOutConfigure(0,//0:2.0V 1:2.3V
				FALSE,
				FALSE,
				FALSE,
				FALSE);

		// clear application context
		memset (&sAppData, 0x00, sizeof(sAppData));
		sAppData.u8channel = CHANNEL;

		// ToCoNet configuration
		sToCoNet_AppContext.u32AppId = APP_ID;
		sToCoNet_AppContext.u8Channel = CHANNEL;

		sToCoNet_AppContext.bRxOnIdle = TRUE;

		// others
		SPRINTF_vInit128();

		// Register
		ToCoNet_Event_Register_State_Machine(vProcessEvCore);

		// Others
		vInitHardware(FALSE);

		// MAC start
		ToCoNet_vMacStart();
	}
}

static bool_t bWakeupByButton;

void cbAppWarmStart(bool_t bAfterAhiInit)
{
	if (!bAfterAhiInit) {
		// before AHI init, very first of code.
		//  to check interrupt source, etc.
		bWakeupByButton = FALSE;

		if(u8AHI_WakeTimerFiredStatus()) {
			// wake up timer
		} else
		if(u32AHI_DioWakeStatus() & u32DioPortWakeUp) {
			// woke up from DIO events
			bWakeupByButton = TRUE;
		} else {
			bWakeupByButton = FALSE;
		}
	} else {
		// Initialize hardware
		vInitHardware(TRUE);

		// MAC start
		ToCoNet_vMacStart();
	}
}

void cbToCoNet_vMain(void)
{
	//vfPrintf(&sSerStream, LB"catch");
	/* handle uart input */
	vHandleSerialInput();
}

void cbToCoNet_vNwkEvent(teEvent eEvent, uint32 u32arg) {
	switch(eEvent) {
	default:
		break;
	}
}

uint8 j;
int16 acceData[30];
char payload[68];
void cbToCoNet_vRxEvent(tsRxDataApp *pRx) {
	//vfPrintf(&sSerStream, LB"catch");
	//uint32 i;
	static uint16 u16seqPrev = 0xFFFF;
	uint8 *p = pRx->auData;

	uint8 mode = G_OCTET();

	switch (mode) {
		case 'X':
			vfPrintf(&sSerStream, LB"[%04x,%c]",
				pRx->u32SrcAddr,
				//pRx->u8Len+4, // Actual payload byte: the network layer uses additional 4 bytes.
				//pRx->u8Seq,
				//pRx->u8Lqi,
				//pRx->u32Tick & 0xFFFF
				mode
			);
			break;

		case 'D':
			id += 10;
			//binary mode

			payload[0] = (pRx->u32SrcAddr >> 24) & 255;
			payload[1] = (pRx->u32SrcAddr >> 16) & 255;
			payload[2] = (pRx->u32SrcAddr >> 8) & 255;
			payload[3] = pRx->u32SrcAddr & 255;
			payload[4] = mode;

			uint32 timestamp_ms = G_BE_DWORD();

			if (timestamp_ms >> 16) {
				//payload[6] = (timestamp_ms >> 24) & 255;
				payload[5] = (timestamp_ms >> 16) & 255;
			} else {
				//payload[6] = 6;
				payload[5] = -1;
			}

			if (timestamp_ms >> 8) {
				payload[6] = (timestamp_ms >> 8) & 255;
			} else {
				payload[6] = -1;
			}

			if (timestamp_ms) {
				payload[7] = timestamp_ms & 255;
			} else {
				payload[7] = -1;
			}
			for (j=8 ; j<68; j++) {
				payload[j] = G_OCTET();
				if (! payload[j]) {
					payload[j] = 7;
				}
			}
			//binary mode

			//string mode
			/*uint32 timestamp_ms = G_BE_DWORD();
			for (j=0 ; j<30; j++) {
				acceData[j] = G_BE_WORD();
			}*/

			//binary mode
			vfPrintf(&sSerStream, payload);

			//string mode
			/*vfPrintf(&sSerStream, LB"[%04x,%d,%c,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d]",
			//vfPrintf(&sSerStream, LB"[%04x,%d,%c,%d,%d,%d,%d,%d,%d]",
				pRx->u32SrcAddr,
				//pRx->u8Len+4, // Actual payload byte: the network layer uses additional 4 bytes.
				//pRx->u8Seq,
				//pRx->u8Lqi,
				//pRx->u32Tick & 0xFFFF
				timestamp_ms,//id,
				mode,
				acceData[0],
				acceData[1],
				acceData[2],
				acceData[3],
				acceData[4],
				acceData[5],
				acceData[6],
				acceData[7],
				acceData[8],
				acceData[9],
				acceData[10],
				acceData[11],
				acceData[12],
				acceData[13],
				acceData[14],
				acceData[15],
				acceData[16],
				acceData[17],
				acceData[18],
				acceData[19],
				acceData[20],
				acceData[21],
				acceData[22],
				acceData[23],
				acceData[24],
				acceData[25],
				acceData[26],
				acceData[27],
				acceData[28],
				acceData[29]
			);*/
			break;
	}
}

void cbToCoNet_vTxEvent(uint8 u8CbId, uint8 bStatus) {
	return;
}

void cbToCoNet_vHwEvent(uint32 u32DeviceId, uint32 u32ItemBitmap)
{
    switch (u32DeviceId) {
    case E_AHI_DEVICE_TICK_TIMER:
    	// LED BLINK
   		vPortSet_TrueAsLo(PORT_KIT_LED2, u32TickCount_ms & 0x400);

   		// LED ON when receive
   		if (u32TickCount_ms - sAppData.u32LedCt < 300) {
   			vPortSetLo(PORT_KIT_LED1);
   		} else {
  			vPortSetHi(PORT_KIT_LED1);
   		}
    	break;

    default:
    	break;
    }
}

uint8 cbToCoNet_u8HwInt(uint32 u32DeviceId, uint32 u32ItemBitmap) {
	return FALSE;
}

static void vInitHardware(int f_warm_start)
{
	sToCoNet_AppContext.u16TickHz = 500;
	// Serial Initialize
#if 0
	// UART の細かい設定テスト
	tsUartOpt sUartOpt;
	memset(&sUartOpt, 0, sizeof(tsUartOpt));
	sUartOpt.bHwFlowEnabled = FALSE;
	sUartOpt.bParityEnabled = E_AHI_UART_PARITY_ENABLE;
	sUartOpt.u8ParityType = E_AHI_UART_EVEN_PARITY;
	sUartOpt.u8StopBit = E_AHI_UART_2_STOP_BITS;
	sUartOpt.u8WordLen = 7;

	vSerialInit(UART_BAUD, &sUartOpt);
#else
	vSerialInit(UART_BAUD, NULL);
#endif


	ToCoNet_vDebugInit(&sSerStream);
	ToCoNet_vDebugLevel(0);

	/// IOs
	vPortSetLo(PORT_KIT_LED1);
	vPortSetHi(PORT_KIT_LED2);
	vPortAsOutput(PORT_KIT_LED1);
	vPortAsOutput(PORT_KIT_LED2);
}

void vSerialInit(uint32 u32Baud, tsUartOpt *pUartOpt) {
	static uint8 au8SerialTxBuffer[96];
	static uint8 au8SerialRxBuffer[32];

	sSerPort.pu8SerialRxQueueBuffer = au8SerialRxBuffer;
	sSerPort.pu8SerialTxQueueBuffer = au8SerialTxBuffer;
	sSerPort.u32BaudRate = UART_BAUD;
	sSerPort.u16AHI_UART_RTS_LOW = 0xffff;
	sSerPort.u16AHI_UART_RTS_HIGH = 0xffff;
	sSerPort.u16SerialRxQueueSize = sizeof(au8SerialRxBuffer);
	sSerPort.u16SerialTxQueueSize = sizeof(au8SerialTxBuffer);
	sSerPort.u8SerialPort = E_AHI_UART_0;
	sSerPort.u8RX_FIFO_LEVEL = E_AHI_UART_FIFO_LEVEL_1;
	SERIAL_vInit(&sSerPort);

	sSerStream.bPutChar = SERIAL_bTxChar;
	sSerStream.u8Device = E_AHI_UART_0;
}

static void vHandleSerialInput(void)
{
    // handle UART command
	while (!SERIAL_bRxQueueEmpty(sSerPort.u8SerialPort)) {
		int16 i16Char;

		i16Char = SERIAL_i16RxChar(sSerPort.u8SerialPort);

		vfPrintf(&sSerStream, "\n\r# [%c] --> ", i16Char);
	    SERIAL_vFlush(sSerStream.u8Device);

		switch(i16Char) {
		case 't': // パケット送信してみる
			_C {
				// transmit Ack back
				tsTxDataApp tsTx;
				memset(&tsTx, 0, sizeof(tsTxDataApp));

				sAppData.u32Seq++;

				tsTx.u32SrcAddr = ToCoNet_u32GetSerial(); // 自身のアドレス
				tsTx.u32DstAddr = 0xFFFF; // ブロードキャスト

				tsTx.bAckReq = FALSE;
				tsTx.u8Retry = 0x80; // ブロードキャストで都合３回送る
				tsTx.u8CbId = sAppData.u32Seq & 0xFF;
				tsTx.u8Seq = sAppData.u32Seq & 0xFF;
				tsTx.u8Cmd = TOCONET_PACKET_CMD_APP_DATA;

				// SPRINTF でメッセージを作成
				SPRINTF_vRewind();
				vfPrintf(SPRINTF_Stream, "PING: %08X", ToCoNet_u32GetSerial());
				memcpy(tsTx.auData, SPRINTF_pu8GetBuff(), SPRINTF_u16Length());
				tsTx.u8Len = SPRINTF_u16Length();

				// 送信
				ToCoNet_bMacTxReq(&tsTx);

				// LEDの制御
				sAppData.u32LedCt = u32TickCount_ms;

				// ＵＡＲＴに出力
				vfPrintf(&sSerStream, LB "Fire PING Broadcast Message.");
			}
			break;

		default:
			break;
		}

		vfPrintf(&sSerStream, LB);
	    SERIAL_vFlush(sSerStream.u8Device);
	}
}

static void vProcessEvCore(tsEvent *pEv, teEvent eEvent, uint32 u32evarg) {
	if (eEvent == E_EVENT_START_UP) {
		// ここで UART のメッセージを出力すれば安全である。
		if (u32evarg & EVARG_START_UP_WAKEUP_RAMHOLD_MASK) {
			vfPrintf(&sSerStream, LB "RAMHOLD");
		}
	    if (u32evarg & EVARG_START_UP_WAKEUP_MASK) {
			vfPrintf(&sSerStream, LB "Wake up by %s. SleepCt=%d",
					bWakeupByButton ? "UART PORT" : "WAKE TIMER",
					sAppData.u8SleepCt);
	    } else {
	    	vfPrintf(&sSerStream, "\r\n*** ToCoNet PINGPONG SAMPLE %d.%02d-%d ***", VERSION_MAIN, VERSION_SUB, VERSION_VAR);
	    	vfPrintf(&sSerStream, "\r\n*** %08x ***", ToCoNet_u32GetSerial());
	    }
	}
}
