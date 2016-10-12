/****************************************************************************
 * (C) Tokyo Cosmos Electric, Inc. (TOCOS) - 2013 all rights reserved.
 *
 * Condition to use:
 *   - The full or part of source code is limited to use for TWE (TOCOS
 *     Wireless Engine) as compiled and flash programmed.
 *   - The full or part of source code is prohibited to distribute without
 *     permission from TOCOS.
 *
 ****************************************************************************/

/****************************************************************************/
/***        Include files                                                 ***/
/****************************************************************************/
#include <string.h>

#include <jendefs.h>
#include <AppHardwareApi.h>

#include "utils.h"

#include "Main.h"
#include "config.h"
#include "Version.h"

// DEBUG options

#include "serial.h"
#include "fprintf.h"
#include "sprintf.h"

#include "SMBus.h"
#include "24XX00.h"
#include "BH1715.h"
#include "SHT21.h"

/****************************************************************************/
/***        ToCoNet Definitions                                           ***/
/****************************************************************************/
// Select Modules (define befor include "ToCoNet.h")
//#define ToCoNet_USE_MOD_NBSCAN // Neighbour scan module
//#define ToCoNet_USE_MOD_NBSCAN_SLAVE

// includes
#include "ToCoNet.h"
#include "ToCoNet_mod_prototype.h"

#include "app_event.h"

/****************************************************************************/
/***        Macro Definitions                                             ***/
/****************************************************************************/

/****************************************************************************/
/***        Type Definitions                                              ***/
/****************************************************************************/

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


/****************************************************************************/
/***        Local Function Prototypes                                     ***/
/****************************************************************************/

static void vProcessEvCore(tsEvent *pEv, teEvent eEvent, uint32 u32evarg);

static void vInitHardware(int f_warm_start);

void vSerialInit(uint32 u32Baud, tsUartOpt *pUartOpt);
static void vHandleSerialInput(void);

int16 i16TransmitPingMessage(uint8 *pMsg);

static void startADXL();
void readInter();
bool_t sendData(int16 *acceData);

/****************************************************************************/
/***        Exported Variables                                            ***/
/****************************************************************************/

/****************************************************************************/
/***        Local Variables                                               ***/
/****************************************************************************/
/* Version/build information. This is not used in the application unless we
   are in serial debug mode. However the 'used' attribute ensures it is
   present in all binary files, allowing easy identifaction... */

/* Local data used by the tag during operation */
static tsAppData sAppData;

PUBLIC tsFILE sSerStream;
tsSerialPortSetup sSerPort;

// Wakeup port
const uint32 u32DioPortWakeUp = 1UL << 7; // UART Rx Port

// センサー状況
#define KICKED_SENSOR_SHT21_TEMP 1
#define KICKED_SENSOR_SHT21_HUMD 2
#define KICKED_SENSOR_BH1715 3

#define PORT_INPUT1 12
#define PORT_INPUT2 13
#define PORT_INPUT3 11
#define DIO_BUTTON (PORT_INPUT1)
#define PORT_INPUT_MASK_ADXL345 (/* (1UL << DIO_BUTTON) |*/ (1UL << PORT_INPUT2) | (1UL <<  PORT_INPUT3))

static uint8 u8KickedSensor; //!< 開始されたセンサーの種類
static uint32 u32KickedTimeStamp; //! 開始されたタイムスタンプ

static uint16 num = 0;
static bool_t result = FALSE;
static uint32 inter = 0;
static uint32 tmp2 = 81;
static uint8 interresult;
static uint32 inter2 = 0;
static bool_t wakeUpByTimer = FALSE;
static uint32 sleepTimeStamp = 0;

/****************************************************************************
 *
 * NAME: AppColdStart
 *
 * DESCRIPTION:
 *
 * RETURNS:
 *
 ****************************************************************************/
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

/****************************************************************************
 *
 * NAME: AppWarmStart
 *
 * DESCRIPTION:
 *
 * RETURNS:
 *
 ****************************************************************************/
static bool_t bWakeupByButton;

void cbAppWarmStart(bool_t bAfterAhiInit)
{
	if (!bAfterAhiInit) {
		// before AHI init, very first of code.
		//  to check interrupt source, etc.
		bWakeupByButton = FALSE;
		inter2 = u32AHI_DioWakeStatus();
		if(u8AHI_WakeTimerFiredStatus()) {
			// wake up timer
			wakeUpByTimer = TRUE;
		} else
		if(inter2 & u32DioPortWakeUp) {
			// woke up from DIO events
			bWakeupByButton = TRUE;
		} else {
			bWakeupByButton = FALSE;
		}
		//inter2 = u32AHI_DioWakeStatus();
	} else {
		// Initialize hardware
		vInitHardware(TRUE);

		// MAC start
		ToCoNet_vMacStart();
	}
}

/****************************************************************************/
/***        Local Functions                                               ***/
/****************************************************************************/
/****************************************************************************
 *
 * NAME: vMain
 *
 * DESCRIPTION:
 *
 * RETURNS:
 *
 ****************************************************************************/
void cbToCoNet_vMain(void)
{
	/* handle uart input */
	vHandleSerialInput();
}

/****************************************************************************
 *
 * NAME: cbToCoNet_vNwkEvent
 *
 * DESCRIPTION:
 *
 * PARAMETERS:      Name            RW  Usage
 *
 * RETURNS:
 *
 * NOTES:
 ****************************************************************************/
void cbToCoNet_vNwkEvent(teEvent eEvent, uint32 u32arg) {
	switch(eEvent) {
	default:
		break;
	}
}

/****************************************************************************
 *
 * NAME: cbvMcRxHandler
 *
 * DESCRIPTION:
 *
 * RETURNS:
 *
 ****************************************************************************/
void cbToCoNet_vRxEvent(tsRxDataApp *pRx) {
	/*int i;
	static uint16 u16seqPrev = 0xFFFF;
	//uint8 *p = pRx->auData;

	// print coming payload
	vfPrintf(&sSerStream, LB"[PKT Ad:%04x,Ln:%03d,Seq:%03d,Lq:%03d,Tms:%05d \"",
			pRx->u32SrcAddr,
			pRx->u8Len+4, // Actual payload byte: the network layer uses additional 4 bytes.
			pRx->u8Seq,
			pRx->u8Lqi,
			pRx->u32Tick & 0xFFFF);
	for (i = 0; i < pRx->u8Len; i++) {
		if (i < 32) {
			sSerStream.bPutChar(sSerStream.u8Device,
					(pRx->auData[i] >= 0x20 && pRx->auData[i] <= 0x7f) ? pRx->auData[i] : '.');
		} else {
			vfPrintf(&sSerStream, "..");
			break;
		}
	}
	vfPrintf(&sSerStream, "C\"]");

	// 打ち返す
	if (    pRx->u8Seq != u16seqPrev // シーケンス番号による重複チェック
		&& !memcmp(pRx->auData, "PING:", 5) // パケットの先頭は PING: の場合
	) {
		u16seqPrev = pRx->u8Seq;
		// transmit Ack back
		tsTxDataApp tsTx;
		memset(&tsTx, 0, sizeof(tsTxDataApp));

		tsTx.u32SrcAddr = ToCoNet_u32GetSerial(); //
		tsTx.u32DstAddr = pRx->u32SrcAddr; // 送り返す

		tsTx.bAckReq = TRUE;
		tsTx.u8Retry = 0;
		tsTx.u8CbId = pRx->u8Seq;
		tsTx.u8Seq = pRx->u8Seq;
		tsTx.u8Len = pRx->u8Len;
		tsTx.u8Cmd = TOCONET_PACKET_CMD_APP_DATA;

		tsTx.u16DelayMin = 64; // 最小遅延
		tsTx.u16DelayMax = 256; // 最大遅延

		if (tsTx.u8Len > 0) {
			memcpy(tsTx.auData, pRx->auData, tsTx.u8Len);
		}
		tsTx.auData[1] = 'O'; // メッセージを PONG に書き換える

		ToCoNet_bMacTxReq(&tsTx);

		// turn on Led a while
		sAppData.u32LedCt = u32TickCount_ms;

		// ＵＡＲＴに出力
		vfPrintf(&sSerStream, LB "Fire PONG Message to %08x" LB, pRx->u32SrcAddr);
	} else if (!memcmp(pRx->auData, "PONG:", 5)) {
		// ＵＡＲＴに出力
		vfPrintf(&sSerStream, LB "PONG Message from %08x" LB, pRx->u32SrcAddr);
	}*/
	return;
}

/****************************************************************************
 *
 * NAME: cbvMcEvTxHandler
 *
 * DESCRIPTION:
 *
 * PARAMETERS:      Name            RW  Usage
 *
 * RETURNS:
 *
 * NOTES:
 ****************************************************************************/
void cbToCoNet_vTxEvent(uint8 u8CbId, uint8 bStatus) {
	return;
}

/****************************************************************************
 *
 * NAME: cbToCoNet_vHwEvent
 *
 * DESCRIPTION:
 * Process any hardware events.
 *
 * PARAMETERS:      Name            RW  Usage
 *                  u32DeviceId
 *                  u32ItemBitmap
 *
 * RETURNS:
 * None.
 *
 * NOTES:
 * None.
 ****************************************************************************/
uint8 i = 0;
int16 i16res[30];

void cbToCoNet_vHwEvent(uint32 u32DeviceId, uint32 u32ItemBitmap)
{
    switch (u32DeviceId) {
    case E_AHI_DEVICE_TICK_TIMER:
    	if (wakeUpByTimer && (u32TickCount_ms - sleepTimeStamp) < 0x80000000) {
			wakeUpByTimer = FALSE;
			ToCoNet_vSleep(E_AHI_WAKE_TIMER_0, 5000, FALSE, FALSE);
		}
		// LED BLINK
   		vPortSet_TrueAsLo(PORT_KIT_LED2, u32TickCount_ms & 0x400);

   		// LED ON when receive
   		if (u32TickCount_ms - sAppData.u32LedCt < 300) {
   			vPortSetLo(PORT_KIT_LED1);
   		} else {
  			vPortSetHi(PORT_KIT_LED1);
   		}

   		if (result == FALSE) {
			result = bADXL345_LowEnergy_Setting();
			if (result) {
				vfPrintf(&sSerStream, LB "Setting:OK"LB);
				startADXL();
				u32KickedTimeStamp += 3000;
			} else {
				vfPrintf(&sSerStream, LB "Setting:NG"LB);
			}
		} else if (u8KickedSensor && (u32TickCount_ms - u32KickedTimeStamp) < 0x80000000) { // タイムアウトした

   			SPRINTF_vRewind();

   			switch(u8KickedSensor) {
   			case KICKED_SENSOR_BH1715:
   				i16res[i++] = i16ADXL345_LowEnergyReadResult(0);
   				i16res[i++] = i16ADXL345_LowEnergyReadResult(1);
   				i16res[i++] = i16ADXL345_LowEnergyReadResult(2);
   				if (i == 30) {
   					i = 0;
   					sendData(i16res);
   				}
				//vfPrintf(SPRINTF_Stream, "ADXL --> %d[%d]" LB, i16res, num);
   				break;

   			case KICKED_SENSOR_SHT21_HUMD:
				i16res[0] = i16SHT21readResult(NULL, NULL);
				vfPrintf(SPRINTF_Stream, "SHT21 --> %d[%% x 100]" LB, i16res);
   				break;

   			case KICKED_SENSOR_SHT21_TEMP:
				i16res[0] = i16SHT21readResult(NULL, NULL);
				vfPrintf(SPRINTF_Stream, "SHT21 --> %d[oC x 100]" LB, i16res);
   				break;
   			}
   			//u8KickedSensor = 0;

   			vfPrintf(&sSerStream, "%s", SPRINTF_pu8GetBuff());
   			//i16TransmitPingMessage(SPRINTF_pu8GetBuff());

   			startADXL();
   		}
    	break;

    case E_AHI_DEVICE_SYSCTRL:
    	//vfPrintf(&sSerStream, LB"割り込み<%d>"LB, u32ItemBitmap);

    	/*if (u32ItemBitmap & PORT_INPUT_MASK_ADXL345){
    		if (u32ItemBitmap != 8192)
    	    	inter = u32ItemBitmap & PORT_INPUT_MASK_ADXL345;
    	}*/
    	if (u32ItemBitmap & (1UL << PORT_INPUT2)) {
    		vfPrintf(&sSerStream, LB"sleep"LB);
    		ToCoNet_vSleep(E_AHI_WAKE_TIMER_0, 5000, FALSE, FALSE);
    	} else if (u32ItemBitmap & (1UL << PORT_INPUT3)) {
    		//readInter();
    	}
    	break;
    default:

    	break;
    }
}

/****************************************************************************
 *
 * NAME: cbToCoNet_u8HwInt
 *
 * DESCRIPTION:
 *   called during an interrupt
 *
 * PARAMETERS:      Name            RW  Usage
 *                  u32DeviceId
 *                  u32ItemBitmap
 *
 * RETURNS:
 *                  FALSE -  interrupt is not handled, escalated to further
 *                           event call (cbToCoNet_vHwEvent).
 *                  TRUE  -  interrupt is handled, no further call.
 *
 * NOTES:
 *   Do not put a big job here.
 ****************************************************************************/
uint8 cbToCoNet_u8HwInt(uint32 u32DeviceId, uint32 u32ItemBitmap) {
	return FALSE;
}

/****************************************************************************
 *
 * NAME: vInitHardware
 *
 * DESCRIPTION:
 *
 * RETURNS:
 *
 ****************************************************************************/
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

	vPortAsInput(PORT_INPUT2);
	vPortAsInput(PORT_INPUT3);
	vPortDisablePullup(PORT_INPUT2);
	vPortDisablePullup(PORT_INPUT3);
	(void)u32AHI_DioInterruptStatus();
	vAHI_DioInterruptEnable(PORT_INPUT_MASK_ADXL345, 0);
	vAHI_DioWakeEnable(PORT_INPUT_MASK_ADXL345, 0); // also use as DIO WAKE SOURCE
	vAHI_DioWakeEdge(PORT_INPUT_MASK_ADXL345, 0); // 割り込みエッジ（立上がりに設定）


	// SMBUS
	vSMBusInit();
	//result = bADXL345_LowEnergy_Setting();
}

/****************************************************************************
 *
 * NAME: vInitHardware
 *
 * DESCRIPTION:
 *
 * RETURNS:
 *
 ****************************************************************************/
void vSerialInit(uint32 u32Baud, tsUartOpt *pUartOpt) {
	/* Create the debug port transmit and receive queues */
	static uint8 au8SerialTxBuffer[864];
	static uint8 au8SerialRxBuffer[128];

	/* Initialise the serial port to be used for debug output */
	sSerPort.pu8SerialRxQueueBuffer = au8SerialRxBuffer;
	sSerPort.pu8SerialTxQueueBuffer = au8SerialTxBuffer;
	sSerPort.u32BaudRate = u32Baud;
	sSerPort.u16AHI_UART_RTS_LOW = 0xffff;
	sSerPort.u16AHI_UART_RTS_HIGH = 0xffff;
	sSerPort.u16SerialRxQueueSize = sizeof(au8SerialRxBuffer);
	sSerPort.u16SerialTxQueueSize = sizeof(au8SerialTxBuffer);
	sSerPort.u8SerialPort = UART_PORT_SLAVE;
	sSerPort.u8RX_FIFO_LEVEL = E_AHI_UART_FIFO_LEVEL_1;
	SERIAL_vInitEx(&sSerPort, pUartOpt);

	sSerStream.bPutChar = SERIAL_bTxChar;
	sSerStream.u8Device = UART_PORT_SLAVE;
}

/****************************************************************************
 *
 * NAME: vHandleSerialInput
 *
 * DESCRIPTION:
 *
 * PARAMETERS:      Name            RW  Usage
 *
 * RETURNS:
 *
 * NOTES:
 ****************************************************************************/
static void vHandleSerialInput(void)
{
    // handle UART command
	while (!SERIAL_bRxQueueEmpty(sSerPort.u8SerialPort)) {
		int16 i16Char;

		i16Char = SERIAL_i16RxChar(sSerPort.u8SerialPort);

		vfPrintf(&sSerStream, "\n\r# [%c] --> ", i16Char);
	    SERIAL_vFlush(sSerStream.u8Device);

		switch(i16Char) {
		case 'a': // ADXL
			startADXL();
			break;

		case 's': // SHT21 Temperature
			if (!u8KickedSensor) {
				bool_t bres = bSHT21startRead(SHT21_TRIG_TEMP);
				if (bres) {
					vfPrintf(&sSerStream, LB "Start SHT21 temperature sensing...");
					u8KickedSensor = KICKED_SENSOR_SHT21_TEMP;
					u32KickedTimeStamp = u32TickCount_ms + 32;
				} else {
					vfPrintf(&sSerStream, LB "SHT21 is not found.");
				}
			}
			break;

		case 'b':
			result = bADXL345_LowEnergy_Setting();
			if (result) {
				vfPrintf(&sSerStream, LB "Setting:OK"LB);
			} else {
				vfPrintf(&sSerStream, LB "Setting:NG"LB);
			}
			break;

		case 'r':
			interresult = i16ADXL345_ReadInter();
			vfPrintf(&sSerStream, LB "inter:%d", interresult);
			break;

		case 'h': // SHT21 Humidity
			if (!u8KickedSensor) {
				bool_t bres = bSHT21startRead(SHT21_TRIG_HUMID);
				if (bres) {
					vfPrintf(&sSerStream, LB "Start SHT21 humidity sensing...");
					u8KickedSensor = KICKED_SENSOR_SHT21_HUMD;
					u32KickedTimeStamp = u32TickCount_ms + 32;
				} else {
					vfPrintf(&sSerStream, LB "SHT21 is not found.");
				}
			}
			break;

		case 'e': // 24AA00
			_C {
				#define U8SIZ 8
				static uint32 u32ct = 0;
				bool_t bOk;
				uint8 u8buf[U8SIZ], i, *p;

				vWait(10000);

				for (i = 0; i < U8SIZ; i++) {
					u8buf[i] = 0xA5;
				}
				bOk = b24xx01_Read(0, u8buf, U8SIZ);

				vfPrintf(&sSerStream,  "\n\r24AA01 READ(%d):", bOk);

				for (i = 0; i < U8SIZ; i++) {
					vfPrintf(&sSerStream,  " %02X", u8buf[i]);
				}

				p = (uint8*)&(u32ct);

				for (i = 0; i < U8SIZ; i++) {
					u8buf[i] = p[i % 4];
				}
				bOk = b24xx01_Write(0, u8buf, U8SIZ);

				vfPrintf(&sSerStream, "\n\r24AA01 WRITE(%d):", bOk);

				u32ct++;
			}
			break;

		case '>': case '.':
			/* channel up */
			sAppData.u8channel++;
			if (sAppData.u8channel > 26) sAppData.u8channel = 11;
			sToCoNet_AppContext.u8Channel = sAppData.u8channel;
			ToCoNet_vRfConfig();
			vfPrintf(&sSerStream, "set channel to %d.", sAppData.u8channel);
			break;

		case '<': case ',':
			/* channel down */
			sAppData.u8channel--;
			if (sAppData.u8channel < 11) sAppData.u8channel = 26;
			sToCoNet_AppContext.u8Channel = sAppData.u8channel;
			ToCoNet_vRfConfig();
			vfPrintf(&sSerStream, "set channel to %d.", sAppData.u8channel);
			break;

		case 'd': case 'D':
			_C {
				static uint8 u8DgbLvl;

				u8DgbLvl++;
				if(u8DgbLvl > 5) u8DgbLvl = 0;
				ToCoNet_vDebugLevel(u8DgbLvl);

				vfPrintf(&sSerStream, "set NwkCode debug level to %d.", u8DgbLvl);
			}
			break;

		case 't': // パケット送信してみる
			_C {
				// transmit Ack back
				tsTxDataApp tsTx;
				memset(&tsTx, 0, sizeof(tsTxDataApp));

				sAppData.u32Seq++;

				tsTx.u32SrcAddr = ToCoNet_u32GetSerial(); // 自身のアドレス
				tsTx.u32DstAddr = 0xFFFF; // ブロードキャスト

				tsTx.bAckReq = FALSE;
				tsTx.u8Retry = 0x82; // ブロードキャストで都合３回送る
				tsTx.u8CbId = sAppData.u32Seq & 0xFF;
				tsTx.u8Seq = sAppData.u32Seq & 0xFF;
				tsTx.u8Cmd = TOCONET_PACKET_CMD_APP_DATA;

				// SPRINTF でメッセージを作成
				SPRINTF_vRewind();
				vfPrintf(SPRINTF_Stream, "PING: %08X", ToCoNet_u32GetSerial());
				memcpy(tsTx.auData, SPRINTF_pu8GetBuff(), SPRINTF_u16Length());
				tsTx.u8Len = SPRINTF_u16Length();

				// 送信
				if (ToCoNet_bMacTxReq(&tsTx)){;

				// LEDの制御
				sAppData.u32LedCt = u32TickCount_ms;

				// ＵＡＲＴに出力
				vfPrintf(&sSerStream, LB "Fire PING Broadcast Message.");
				}
			}
			break;

		default:
			break;
		}

		vfPrintf(&sSerStream, LB);
	    SERIAL_vFlush(sSerStream.u8Device);
	}
}

void readInter() {
	interresult = i16ADXL345_ReadInter();
	vfPrintf(&sSerStream, LB "inter:%d", interresult);
}

bool_t sendData(int16 *acceData) {
	tsTxDataApp tsTx;
	memset(&tsTx, 0, sizeof(tsTxDataApp));

	sAppData.u32Seq++;

	tsTx.u32SrcAddr = ToCoNet_u32GetSerial(); // 自身のアドレス
	tsTx.u32DstAddr = 0xFFFF; // ブロードキャスト

	tsTx.bAckReq = FALSE;
	tsTx.u8Retry = 0x82; // ブロードキャストで都合３回送る
	//tsTx.u8CbId = sAppData.u32Seq & 0xFF;
	//tsTx.u8Seq = sAppData.u32Seq & 0xFF;
	tsTx.u8Cmd = TOCONET_PACKET_CMD_APP_DATA;

	uint8 *q =  tsTx.auData;
	S_OCTET('D');

	uint8 j;
	for (j=0 ; j<30; j++) {
		S_BE_WORD(acceData[j]);
	}
	// SPRINTF でメッセージを作成
	/*SPRINTF_vRewind();
	vfPrintf(SPRINTF_Stream, "from main: %08X", ToCoNet_u32GetSerial());
	memcpy(tsTx.auData, SPRINTF_pu8GetBuff(), SPRINTF_u16Length());*/
	tsTx.u8Len = q - tsTx.auData;//SPRINTF_u16Length();

	// 送信
	ToCoNet_bMacTxReq(&tsTx);
	ToCoNet_Tx_vProcessQueue();

	// LEDの制御
	sAppData.u32LedCt = u32TickCount_ms;

	// ＵＡＲＴに出力
	vfPrintf(&sSerStream, LB "Fire PING Broadcast Message.");

	return -1;
}

int16 i16TransmitPingMessage(uint8 *pMsg) {
	tsTxDataApp tsTx;
	memset(&tsTx, 0, sizeof(tsTxDataApp));

	sAppData.u32Seq++;

	tsTx.u32SrcAddr = ToCoNet_u32GetSerial(); // 自身のアドレス
	tsTx.u32DstAddr = 0xFFFF; // ブロードキャスト

	tsTx.bAckReq = FALSE;
	tsTx.u8Retry = 0x82; // ブロードキャストで都合３回送る
	//tsTx.u8CbId = sAppData.u32Seq & 0xFF;
	//tsTx.u8Seq = sAppData.u32Seq & 0xFF;
	tsTx.u8Cmd = TOCONET_PACKET_CMD_APP_DATA;

	uint8 *q =  tsTx.auData;
	S_OCTET('X');
	// SPRINTF でメッセージを作成
	/*SPRINTF_vRewind();
	vfPrintf(SPRINTF_Stream, "from main: %08X", ToCoNet_u32GetSerial());
	memcpy(tsTx.auData, SPRINTF_pu8GetBuff(), SPRINTF_u16Length());*/
	tsTx.u8Len = q - tsTx.auData;//SPRINTF_u16Length();

	// 送信
	ToCoNet_bMacTxReq(&tsTx);
	ToCoNet_Tx_vProcessQueue();

	// LEDの制御
	sAppData.u32LedCt = u32TickCount_ms;

	// ＵＡＲＴに出力
	vfPrintf(&sSerStream, LB "Fire PING Broadcast Message.");
	// transmit Ack back
	/*tsTxDataApp tsTx;
	memset(&tsTx, 0, sizeof(tsTxDataApp));
	uint8 *q = tsTx.auData;

	sAppData.u32Seq++;

	tsTx.u32SrcAddr = ToCoNet_u32GetSerial(); // 自身のアドレス
	tsTx.u32DstAddr = 0xFFFF; // ブロードキャスト

	tsTx.bAckReq = FALSE;
	tsTx.u8Retry = 0x82; // ブロードキャストで都合３回送る
	tsTx.u8CbId = sAppData.u32Seq & 0xFF;
	tsTx.u8Seq = sAppData.u32Seq & 0xFF;
	tsTx.u8Cmd = TOCONET_PACKET_CMD_APP_DATA;

	// SPRINTF でメッセージを作成
	S_OCTET('P');
	S_OCTET('I');
	S_OCTET('N');
	S_OCTET('G');
	S_OCTET(':');
	S_OCTET(' ');

	uint8 u8len = strlen((const char *)pMsg);
	memcpy(q, pMsg, u8len);
	q += u8len;
	tsTx.u8Len = q - tsTx.auData;

	// 送信
	if (ToCoNet_bMacTxReq(&tsTx)) {
		ToCoNet_Tx_vProcessQueue();
		// LEDの制御
		sAppData.u32LedCt = u32TickCount_ms;

		// ＵＡＲＴに出力
		vfPrintf(&sSerStream, LB "Fire PING Broadcast Message.");

		return tsTx.u8CbId;
	} else {
		return -1;
	}*/
	return -1;
}

/****************************************************************************
 *
 * NAME: vProcessEvent
 *
 * DESCRIPTION:
 *
 * RETURNS:
 *
 ****************************************************************************/
static void vProcessEvCore(tsEvent *pEv, teEvent eEvent, uint32 u32evarg) {
	if (eEvent == E_EVENT_START_UP) {
		// ここで UART のメッセージを出力すれば安全である。
		/*if (u32evarg & EVARG_START_UP_WAKEUP_RAMHOLD_MASK) {
			vfPrintf(&sSerStream, LB "RAMHOLD");
		}
	    if (u32evarg & EVARG_START_UP_WAKEUP_MASK) {
			vfPrintf(&sSerStream, LB "Wake up by %s. SleepCt=%d",
					bWakeupByButton ? "UART PORT" : "WAKE TIMER",
					sAppData.u8SleepCt);
	    } else {
	    	vfPrintf(&sSerStream, "\r\n*** ToCoNet I2C SAMPLE %d.%02d-%d ***", VERSION_MAIN, VERSION_SUB, VERSION_VAR);
	    	vfPrintf(&sSerStream, "\r\n*** %08x ***", ToCoNet_u32GetSerial());
	    }*/
	    //vfPrintf(&sSerStream, LB"<%d>"LB, inter2);
	    if(inter2 & (1UL << PORT_INPUT3)) {
	    	readInter();
	    	vfPrintf(&sSerStream, LB"wake up"LB);
	    }

	    if (wakeUpByTimer) {
	    	//vfPrintf(&sSerStream, LB"wake up by timer"LB);
	    	char msg[] = "abc";
	    	i16TransmitPingMessage(msg);
	    	sleepTimeStamp = u32TickCount_ms + 5;
	    }
	}
}

static void startADXL(){
	//if (!u8KickedSensor) {
		bool_t bres = bADXL345_LowEnergyStartRead();
		num++;
		if (bres) {
			//vfPrintf(&sSerStream, LB "Start ADXL sensing...");
			u8KickedSensor = KICKED_SENSOR_BH1715;
			u32KickedTimeStamp = u32TickCount_ms + 2;
		} else {
			vfPrintf(&sSerStream, LB "ADXL is not found.");
		}
	/*} else {
		u32KickedTimeStamp = u32TickCount_ms + 2;
		num++;
	}*/
}
/****************************************************************************/
/***        END OF FILE                                                   ***/
/****************************************************************************/
