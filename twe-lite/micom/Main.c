#include <string.h>
#include <jendefs.h>
#include <AppHardwareApi.h>
#include "utils.h"
#include "Main.h"
#include "config.h"
#include "Version.h"
#include "serial.h"
#include "fprintf.h"
#include "sprintf.h"
#include "SMBus.h"
//#include "24XX00.h"
#include "BH1715.h"
//#include "SHT21.h"
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
int16 i16TransmitPingMessage(uint8 *pMsg);
static void startADXL();
uint8 readInter();
bool_t sendData(int16 *acceData);

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
//static uint32 tmp2 = 81;
static uint8 interresult;
static uint32 inter2 = 0;
static bool_t wakeUpByTimer = FALSE;
static uint32 sleepTimeStamp = 0;
static bool_t isFirstMessage = TRUE;
static char* mode_now = 's';
uint32 startTickCount_ms;
uint32 this_startTickCount_ms;
static int data_cnt = 0;


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
		inter2 = u32AHI_DioWakeStatus();
		if(u8AHI_WakeTimerFiredStatus() && mode_now == 's') {
			// wake up timer
			wakeUpByTimer = TRUE;
			isFirstMessage = TRUE;
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

void cbToCoNet_vMain(void)
{
	/* handle uart input */
	vHandleSerialInput();
}

void cbToCoNet_vNwkEvent(teEvent eEvent, uint32 u32arg) {
	switch(eEvent) {
	default:
		break;
	}
}

void cbToCoNet_vRxEvent(tsRxDataApp *pRx) {
	return;
}

void cbToCoNet_vTxEvent(uint8 u8CbId, uint8 bStatus) {
	return;
}

uint8 i = 0;
int16 i16res[30];
//uint8 ui8res[60];
void cbToCoNet_vHwEvent(uint32 u32DeviceId, uint32 u32ItemBitmap)
{
    switch (u32DeviceId) {
    case E_AHI_DEVICE_TICK_TIMER:
    	if (wakeUpByTimer && (u32TickCount_ms - sleepTimeStamp) < 0x80000000) {
			wakeUpByTimer = FALSE;
			ToCoNet_vSleep(E_AHI_WAKE_TIMER_0, 15000, FALSE, FALSE);
		}
		// LED BLINK
   		vPortSet_TrueAsLo(PORT_KIT_LED2, u32TickCount_ms & 0x400);

   		// LED ON when receive
   		if (u32TickCount_ms - sAppData.u32LedCt < 300) {
   			vPortSetLo(PORT_KIT_LED1);
   		} else {
  			vPortSetHi(PORT_KIT_LED1);
   		}
   		//vfPrintf(&sSerStream, LB "OK"LB);
   		if (! wakeUpByTimer) {
   		if (result == FALSE) {
			result = bADXL345_LowEnergy_Setting();
			if (result) {
				mode_now = 'm';
				vfPrintf(&sSerStream, LB "Setting:OK"LB);
				startADXL();
				u32KickedTimeStamp += 3000;
			} else {
				vfPrintf(&sSerStream, LB "Setting:NG"LB);
			}
		} else if (u8KickedSensor && (u32TickCount_ms - u32KickedTimeStamp) < 0x80000000) { // タイムアウトした

   			//SPRINTF_vRewind();
			mode_now = 'm';
   			switch(u8KickedSensor) {
   			case KICKED_SENSOR_BH1715:
   				if (data_cnt++ == 0) startTickCount_ms = u32TickCount_ms;
   				if (i == 0) this_startTickCount_ms = u32TickCount_ms - startTickCount_ms;
   				//else if (data_cnt == 5000) data_cnt = 0;
   				//for (;i<30;) {
				i16res[i++] = i16ADXL345_LowEnergyReadResult(0);
				i16res[i++] = i16ADXL345_LowEnergyReadResult(1);
				i16res[i++] = i16ADXL345_LowEnergyReadResult(2);
				//vfPrintf(&sSerStream, "%d", i16res[i-3] >> 8);
   				//}
   				/*i16ADXL345_LowEnergyReadResult(0,ui8res, i);
   				//vfPrintf(&sSerStream, LB "%d", ((int16)(ui8res[i] | (ui8res[i+1] << 8))));
   				i += 2;
   				i16ADXL345_LowEnergyReadResult(1,ui8res, i);
   				i += 2;
   				i16ADXL345_LowEnergyReadResult(2,ui8res, i);
   				i += 2;*/
   				if (i == 30) {
   					i = 0;
   					//u8KickedSensor = 0;
   					//uint32 time_per30 = u32TickCount_ms - startTickCount_ms - this_startTickCount_ms;
   					//vfPrintf(&sSerStream, LB"time_per30: %d"LB, time_per30);
   					//sendData(ui8res);
   					//vfPrintf(&sSerStream, LB"send"LB);
   					sendData(i16res);
   				}
				//vfPrintf(SPRINTF_Stream, "ADXL --> %d[%d]" LB, i16res, num);
   				break;

   			}

   			//vfPrintf(&sSerStream, "%s", SPRINTF_pu8GetBuff());
   			//i16TransmitPingMessage(SPRINTF_pu8GetBuff());

   			startADXL();
   		}
   		}
    	break;

    case E_AHI_DEVICE_SYSCTRL:
    	//vfPrintf(&sSerStream, LB"%d"LB, u32ItemBitmap);

    	if (u32ItemBitmap & (1UL << PORT_INPUT2)) {
    		inter = readInter();
    		if (inter & 8) {
				vfPrintf(&sSerStream, "s"LB);
				mode_now = 's';
				//vfPrintf(&sSerStream, "sleep"LB);
				data_cnt = 0;
				wakeUpByTimer = FALSE;
				ToCoNet_vSleep(E_AHI_WAKE_TIMER_0, 15000, FALSE, FALSE);
    		}
    	}

    	if(u32ItemBitmap & (1UL << PORT_INPUT3)) {
			//readInter();
			/*int k;
			for (k=0; k<20; k++) {
				i16ADXL345_LowEnergyReadResult(0);
				i16ADXL345_LowEnergyReadResult(1);
				i16ADXL345_LowEnergyReadResult(2);

			}*/
			//vfPrintf(&sSerStream, "water"LB);
			startADXL();
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
	sToCoNet_AppContext.u16TickHz = 1000;
	//sToCoNet_AppContext.u16TickHz = 100;
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

		case 't': // パケット送信してみる
			_C {
				// transmit Ack back
				tsTxDataApp tsTx;
				memset(&tsTx, 0, sizeof(tsTxDataApp));

				sAppData.u32Seq++;

				tsTx.u32SrcAddr = ToCoNet_u32GetSerial(); // 自身のアドレス
				tsTx.u32DstAddr = 0xFFFF; // ブロードキャスト

				tsTx.bAckReq = FALSE;
				tsTx.u8Retry = 0; // ブロードキャストで都合３回送る
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

uint8 readInter() {
	interresult = 0;
	while (! interresult) {
		interresult = i16ADXL345_ReadInter();
	}
	vfPrintf(&sSerStream, "%d"LB, interresult);
	return interresult;
}

bool_t sendData(int16 *acceData) {
	tsTxDataApp tsTx;
	memset(&tsTx, 0, sizeof(tsTxDataApp));

	sAppData.u32Seq++;

	tsTx.u32SrcAddr = ToCoNet_u32GetSerial(); // 自身のアドレス
	tsTx.u32DstAddr = 0xFFFF; // ブロードキャスト

	tsTx.bAckReq = FALSE;
	tsTx.u8Retry = 0; // ブロードキャストで都合３回送る
	//tsTx.u8CbId = sAppData.u32Seq & 0xFF;
	//tsTx.u8Seq = sAppData.u32Seq & 0xFF;
	tsTx.u8Cmd = TOCONET_PACKET_CMD_APP_DATA;

	uint8 *q =  tsTx.auData;
	S_OCTET('D');
	//uint16 timestamp_ms = u32TickCount_ms - startTickCount_ms;
	S_BE_DWORD(this_startTickCount_ms);


	//binary mode
	uint8 j;
	for (j=0 ; j<30; j++) {
		if (acceData[j]) {
			S_BE_WORD(acceData[j]);
		} else {
			S_BE_WORD(1700);
		}
	}
	//binary mode

	//string mode
	/*uint8 j;
	for (j=0 ; j<30; j++) {
		S_BE_WORD(acceData[j]);
	}*/
	//string mode

	//vfPrintf(&sSerStream, LB "%d",acceData[0]);
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
	//vfPrintf(&sSerStream, LB "Fire PING Broadcast Message.");

	return -1;
}

int16 i16TransmitPingMessage(uint8 *pMsg) {
	tsTxDataApp tsTx;
	memset(&tsTx, 0, sizeof(tsTxDataApp));

	sAppData.u32Seq++;

	tsTx.u32SrcAddr = ToCoNet_u32GetSerial(); // 自身のアドレス
	tsTx.u32DstAddr = 0xFFFF; // ブロードキャスト

	tsTx.bAckReq = FALSE;
	tsTx.u8Retry = 0; // ブロードキャストで都合３回送る
	//tsTx.u8CbId = sAppData.u32Seq & 0xFF;
	//tsTx.u8Seq = sAppData.u32Seq & 0xFF;
	tsTx.u8Cmd = TOCONET_PACKET_CMD_APP_DATA;

	uint8 *q =  tsTx.auData;
	char mode_ = 'x';
	if (pMsg[10] == 'O') mode_ = 'X';
	S_OCTET(mode_);
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
	vfPrintf(&sSerStream, LB "Fire PING Broadcast Message. (%s)", pMsg);

	return -1;
}

static void vProcessEvCore(tsEvent *pEv, teEvent eEvent, uint32 u32evarg) {
	if(inter2 & (1UL << PORT_INPUT3)) {
		//readInter();
		/*int k;
		for (k=0; k<20; k++) {
			i16ADXL345_LowEnergyReadResult(0);
			i16ADXL345_LowEnergyReadResult(1);
			i16ADXL345_LowEnergyReadResult(2);

		}*/
		//vfPrintf(&sSerStream, "water"LB);
		startADXL();
	}
	if (eEvent == E_EVENT_START_UP) {
	    //readInter();
	    //vfPrintf(&sSerStream, "inter2: %d"LB, inter2);

	    if(inter2 & (1UL << PORT_INPUT2)) {
	    	inter = readInter();
	    	vfPrintf(&sSerStream, "wake up"LB);
		}

	    if (wakeUpByTimer && isFirstMessage && mode_now == 's') {
	    	result = bADXL345_LowEnergy_Setting();

	    	isFirstMessage = FALSE;
	    	//vfPrintf(&sSerStream, LB"wake up by timer"LB);
	    	if (result) {
	    	char msg[] = "Config is OK";
	    	i16TransmitPingMessage(msg);
	    	} else {
	    	char msg[] = "Config is NG";
	       	i16TransmitPingMessage(msg);
	    	}
	    	/*bool_t bOk = TRUE;
			uint8 com = 0x28;
			bOk &= bSMBusWrite(ADXL345_ADDRESS, ADXL345_POWER_CTL, 1, &com );*/
	    	/*(void)u32AHI_DioInterruptStatus();
	    	vAHI_DioInterruptEnable(PORT_INPUT_MASK_ADXL345, 0);
	    	vAHI_DioWakeEnable(PORT_INPUT_MASK_ADXL345, 0); // also use as DIO WAKE SOURCE
	   		vAHI_DioWakeEdge(PORT_INPUT_MASK_ADXL345, 0); // 割り込みエッジ（立上がりに設定*/
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
			u32KickedTimeStamp = u32TickCount_ms+1;
		} else {
			vfPrintf(&sSerStream, LB "ADXL is not found.");
		}
	/*} else {
		u32KickedTimeStamp = u32TickCount_ms + 2;
		num++;
	}*/
}
