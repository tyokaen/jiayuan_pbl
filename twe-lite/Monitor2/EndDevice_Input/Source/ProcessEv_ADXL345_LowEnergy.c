/****************************************************************************
 * (C) Tokyo Cosmos Electric, Inc. (TOCOS) - all rights reserved.
 *
 * Condition to use: (refer to detailed conditions in Japanese)
 *   - The full or part of source code is limited to use for TWE (TOCOS
 *     Wireless Engine) as compiled and flash programmed.
 *   - The full or part of source code is prohibited to distribute without
 *     permission from TOCOS.
 *
 * 利用条件:
 *   - 本ソースコードは、別途ソースコードライセンス記述が無い限り東京コスモス電機が著作権を
 *     保有しています。
 *   - 本ソースコードは、無保証・無サポートです。本ソースコードや生成物を用いたいかなる損害
 *     についても東京コスモス電機は保証致しません。不具合等の報告は歓迎いたします。
 *   - 本ソースコードは、東京コスモス電機が販売する TWE シリーズ上で実行する前提で公開
 *     しています。他のマイコン等への移植・流用は一部であっても出来ません。
 *
 ****************************************************************************/

#include <jendefs.h>

#include "utils.h"

#include "ccitt8.h"

#include "Interactive.h"
#include "EndDevice_Input.h"

#include "sensor_driver.h"
#include "ADXL345_LowEnergy.h"

static void vProcessEvCore(tsEvent *pEv, teEvent eEvent, uint32 u32evarg);
static void vStoreSensorValue();
static void vProcessADXL345_LowEnergy(teEvent eEvent);
static uint8 u8sns_cmplt = 0;

static tsSnsObj sSnsObj;
static tsObjData_ADXL345 sObjADXL345;

static bool_t thre=TRUE;
static int throughCount = 0;
static int roopCount = 0;
uint32 thre_tick = 0;
int16 xyz_array[492];
/*int16 y_array[165];
int16 z_array[165];*/

enum {
	E_SNS_ADC_CMP_MASK = 1,
	E_SNS_ADXL345_CMP = 2,
	E_SNS_ALL_CMP = 3
};

/*
 * ADC 計測をしてデータ送信するアプリケーション制御
 */
PRSEV_HANDLER_DEF(E_STATE_IDLE, tsEvent *pEv, teEvent eEvent, uint32 u32evarg) {
	static bool_t bFirst = TRUE;
	if (eEvent == E_EVENT_START_UP) {
		if (u32evarg & EVARG_START_UP_WAKEUP_RAMHOLD_MASK) {
			// Warm start message
			V_PRINTF(LB "*** Warm starting woke by %s. ***", sAppData.bWakeupByButton ? "DIO" : "WakeTimer");
		} else {
			// 開始する
			// start up message
			vSerInitMessage();

			V_PRINTF(LB "*** Cold starting");
			V_PRINTF(LB "* start end device[%d]", u32TickCount_ms & 0xFFFF);
			// ADXL345 の初期化
		}

		// RC クロックのキャリブレーションを行う
		ToCoNet_u16RcCalib(sAppData.sFlash.sData.u16RcClock);

		// センサーがらみの変数の初期化
		u8sns_cmplt = 0;

		vADXL345_LowEnergy_Init( &sObjADXL345, &sSnsObj );
		if( bFirst ){
			V_PRINTF(LB "*** ADXL345 Setting...");
			bFirst = FALSE;
			bADXL345_LowEnergy_Setting();
		}
		vSnsObj_Process(&sSnsObj, E_ORDER_KICK);
		if (bSnsObj_isComplete(&sSnsObj)) {
			// 即座に完了した時はセンサーが接続されていない、通信エラー等
			u8sns_cmplt |= E_SNS_ADXL345_CMP;
			V_PRINTF(LB "*** ADXL345 comm err?");
			ToCoNet_Event_SetState(pEv, E_STATE_APP_SLEEP); // スリープ状態へ遷移
			return;
		}


		// ADC の取得
		vADC_WaitInit();
		vSnsObj_Process(&sAppData.sADC, E_ORDER_KICK);

		// RUNNING 状態
		ToCoNet_Event_SetState(pEv, E_STATE_RUNNING);
	} else {
		V_PRINTF(LB "*** unexpected state.");
		ToCoNet_Event_SetState(pEv, E_STATE_APP_SLEEP); // スリープ状態へ遷移
	}
}

PRSEV_HANDLER_DEF(E_STATE_RUNNING, tsEvent *pEv, teEvent eEvent, uint32 u32evarg) {
		// 短期間スリープからの起床をしたので、センサーの値をとる
	if ((eEvent == E_EVENT_START_UP) && (u32evarg & EVARG_START_UP_WAKEUP_RAMHOLD_MASK)) {
		V_PRINTF("#");
		vProcessADXL345_LowEnergy(E_EVENT_START_UP);
	}

	// 送信処理に移行
	if (u8sns_cmplt == E_SNS_ALL_CMP) {
		ToCoNet_Event_SetState(pEv, E_STATE_APP_WAIT_TX);
	}

	// タイムアウト
	if (ToCoNet_Event_u32TickFrNewState(pEv) > 100) {
		V_PRINTF(LB"! TIME OUT (E_STATE_RUNNING)");
		ToCoNet_Event_SetState(pEv, E_STATE_APP_SLEEP); // スリープ状態へ遷移
	}
}

PRSEV_HANDLER_DEF(E_STATE_APP_WAIT_TX, tsEvent *pEv, teEvent eEvent, uint32 u32evarg) {
	if (eEvent == E_EVENT_NEW_STATE) {
		// ネットワークの初期化
		if (!sAppData.pContextNwk) {
			// 初回のみ
			sAppData.sNwkLayerTreeConfig.u8Role = TOCONET_NWK_ROLE_ENDDEVICE;
			sAppData.pContextNwk = ToCoNet_NwkLyTr_psConfig_MiniNodes(&sAppData.sNwkLayerTreeConfig);
			if (sAppData.pContextNwk) {
				ToCoNet_Nwk_bInit(sAppData.pContextNwk);
				ToCoNet_Nwk_bStart(sAppData.pContextNwk);
			} else {
				ToCoNet_Event_SetState(pEv, E_STATE_APP_SLEEP); // スリープ状態へ遷移
				return;
			}
		} else {
			// 一度初期化したら RESUME
			ToCoNet_Nwk_bResume(sAppData.pContextNwk);
		}

		roopCount++;
		uint8	au8Data[12];
		uint8*	q = au8Data;
		S_OCTET(sAppData.sSns.u8Batt);
		S_BE_WORD(sAppData.sSns.u16Adc1);
		//S_BE_WORD(sAppData.sSns.u16Adc2);
		/*S_BE_WORD(sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X]);
		S_BE_WORD(sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y]);
		S_BE_WORD(sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z]);
		S_OCTET( 0xFE );
		int j;
				for(j=1; j<165; j++){
					vWait();*/
					/*uint32 tickCount = u32TickCount_ms;
					while(u32TickCount_ms - tickCount < 30){

					}

					vfPrintf(&sSerStream,"sleep");
					x_array[j] = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X];
					y_array[j] = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y];
					z_array[j] = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z];
				}
				int i;
				for(i=0; i<40; i++){
					S_BE_WORD(x_array[i]);
				}

				S_OCTET( 0xFE );
				if(bSendMessage( au8Data, q-au8Data )){

				}else{
					ToCoNet_Event_SetState(pEv, E_STATE_APP_SLEEP); // 送信失敗
				}*/
		if(thre){
			/*int16 ex_x = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X] >= 0 ? sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X] : -sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X];
			int16 ex_y = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y] >= 0 ? sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y] : -sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y];
			int16 ex_z = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z] >= 0 ? sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z] : -sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z];*/

			//加速度の3軸２乗合計の平方根の値を閾値と比較します
			if(sqrt((double)sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X] * sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X] + (double)sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y] * sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y] + (double)sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z] * sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z]) > 92.5){
				/*xyz_array[3*throughCount] = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X];
				xyz_array[3*throughCount+1] = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y];
				xyz_array[3*throughCount+2] = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z];*/
				//double xyz = sqrt((double)sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X] * sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X] + (double)sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y] * sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y] + (double)sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z] * sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z]);

				//TWE-LITE2525自体が一定周期で振動し、加速度が閾値を超える現象が起きるため、一定時間内で２度閾値を越えなければ、閾値を超えたとみなさない
				thre_tick |= u32TickCount_ms;
				if(thre_tick - u32TickCount_ms < 50 && thre_tick - u32TickCount_ms >0){
					throughCount++;
					thre = FALSE;
					S_BE_WORD(0);
					S_BE_WORD(sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X]);
					S_BE_WORD(sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y]);
					S_BE_WORD(sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z]);
					S_OCTET( 0xFE );
					if(bSendMessage( au8Data, q-au8Data )){
					}else{
						ToCoNet_Event_SetState(pEv, E_STATE_APP_SLEEP); // 送信失敗
					}
				}else{
					thre_tick = u32TickCount_ms;
				}
			}
		}else if(throughCount > 300){
			throughCount = 0;
			thre = TRUE;
		}else if(throughCount > 0){
			/*if(throughCount < 165){
			xyz_array[3*throughCount] = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X];
			xyz_array[3*throughCount+1] = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y];
			xyz_array[3*throughCount+2] = sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z];*/
			throughCount++;
			/*}
			if (throughCount % 30 == 0 && throughCount <= 164) {
				S_BE_WORD(0);
				int i;
				int n = (throughCount-1) / 30;
				for(i=0; i<30; i++){
					S_BE_WORD(xyz_array[30 * n + i]);

				}
				/*for(i=0; i<165; i++){
					S_BE_WORD(y_array[i]);
				}
				for(i=0; i<165; i++){
					S_BE_WORD(z_array[i]);
				}*/
				/*S_BE_WORD(x_array[0]);
				S_BE_WORD(x_array[50]);
				S_BE_WORD(x_array[100]);*/
				S_BE_WORD(0);
				S_BE_WORD(sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X]);
				S_BE_WORD(sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y]);
				S_BE_WORD(sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z]);
				S_OCTET( 0xFE );
				if(bSendMessage( au8Data, q-au8Data )){

				}else{
					ToCoNet_Event_SetState(pEv, E_STATE_APP_SLEEP); // 送信失敗
				}
				/*throughCount = 0;
				thre = TRUE;*/
			//}
			/*if(throughCount > 164){
				throughCount = 0;
				thre = TRUE;
			}*/
		}

		if (roopCount % 100 == 0) {
			S_BE_WORD(1);
			S_OCTET( 0xFE );
			 if(bSendMessage( au8Data, q-au8Data )){
			 }else {
				ToCoNet_Event_SetState(pEv, E_STATE_APP_SLEEP); // 送信失敗
			}
		}
/*
#ifdef LITE2525A
		vPortSetHi(LED);
#else
		vPortSetLo(LED);
#endif
*/
		V_PRINTF(" FR=%04X", sAppData.u16frame_count);
	}

	if (eEvent == E_ORDER_KICK) { // 送信完了イベントが来たのでスリープする
		ToCoNet_Event_SetState(pEv, E_STATE_APP_SLEEP); // スリープ状態へ遷移
	}

	// タイムアウト
	if (ToCoNet_Event_u32TickFrNewState(pEv) > 100) {
		V_PRINTF(LB"! TIME OUT (E_STATE_APP_WAIT_TX)");
		ToCoNet_Event_SetState(pEv, E_STATE_APP_SLEEP); // スリープ状態へ遷移
	}
}

PRSEV_HANDLER_DEF(E_STATE_APP_SLEEP, tsEvent *pEv, teEvent eEvent, uint32 u32evarg) {
	if (eEvent == E_EVENT_NEW_STATE) {
		// Sleep は必ず E_EVENT_NEW_STATE 内など１回のみ呼び出される場所で呼び出す。
		V_PRINTF(LB"! Sleeping...");
		V_FLUSH();

		// Mininode の場合、特別な処理は無いのだが、ポーズ処理を行う
		ToCoNet_Nwk_bPause(sAppData.pContextNwk);

		// センサー用の電源制御回路を Hi に戻す
		vPortSetSns(FALSE);

#ifdef LITE2525A
		vPortSetLo(LED);
#else
		vPortSetHi(LED);
#endif
		vAHI_DioWakeEnable(0, PORT_INPUT_MASK); // DISABLE DIO WAKE SOURCE
		ToCoNet_vSleep( E_AHI_WAKE_TIMER_0, sAppData.sFlash.sData.u32Slp, FALSE, FALSE);
	}
}

/**
 * イベント処理関数リスト
 */
static const tsToCoNet_Event_StateHandler asStateFuncTbl[] = {
	PRSEV_HANDLER_TBL_DEF(E_STATE_IDLE),
	PRSEV_HANDLER_TBL_DEF(E_STATE_RUNNING),
	PRSEV_HANDLER_TBL_DEF(E_STATE_APP_WAIT_TX),
	PRSEV_HANDLER_TBL_DEF(E_STATE_APP_SLEEP),
	PRSEV_HANDLER_TBL_TRM
};

/**
 * イベント処理関数
 * @param pEv
 * @param eEvent
 * @param u32evarg
 */
void vProcessEvCore(tsEvent *pEv, teEvent eEvent, uint32 u32evarg) {
	ToCoNet_Event_StateExec(asStateFuncTbl, pEv, eEvent, u32evarg);
}

#if 0
/**
 * ハードウェア割り込み
 * @param u32DeviceId
 * @param u32ItemBitmap
 * @return
 */
static uint8 cbAppToCoNet_u8HwInt(uint32 u32DeviceId, uint32 u32ItemBitmap) {
	uint8 u8handled = FALSE;

	switch (u32DeviceId) {
	case E_AHI_DEVICE_ANALOGUE:
		break;

	case E_AHI_DEVICE_SYSCTRL:
		break;

	case E_AHI_DEVICE_TIMER0:
		break;

	case E_AHI_DEVICE_TICK_TIMER:
		break;

	default:
		break;
	}

	return u8handled;
}
#endif

/**
 * ハードウェアイベント（遅延実行）
 * @param u32DeviceId
 * @param u32ItemBitmap
 */
static void cbAppToCoNet_vHwEvent(uint32 u32DeviceId, uint32 u32ItemBitmap) {
	switch (u32DeviceId) {
	case E_AHI_DEVICE_TICK_TIMER:
		vProcessADXL345_LowEnergy(E_EVENT_TICK_TIMER);
		break;

	case E_AHI_DEVICE_ANALOGUE:
		/*
		 * ADC完了割り込み
		 */
		V_PUTCHAR('@');
		vSnsObj_Process(&sAppData.sADC, E_ORDER_KICK);
		if (bSnsObj_isComplete(&sAppData.sADC)) {
			u8sns_cmplt |= E_SNS_ADC_CMP_MASK;
			vStoreSensorValue();
		}
		break;

	case E_AHI_DEVICE_SYSCTRL:
		break;

	case E_AHI_DEVICE_TIMER0:
		break;

	default:
		break;
	}
}

#if 0
/**
 * メイン処理
 */
static void cbAppToCoNet_vMain() {
	/* handle serial input */
	vHandleSerialInput();
}
#endif

#if 0
/**
 * ネットワークイベント
 * @param eEvent
 * @param u32arg
 */
static void cbAppToCoNet_vNwkEvent(teEvent eEvent, uint32 u32arg) {
	switch(eEvent) {
	case E_EVENT_TOCONET_NWK_START:
		break;

	default:
		break;
	}
}
#endif


#if 0
/**
 * RXイベント
 * @param pRx
 */
static void cbAppToCoNet_vRxEvent(tsRxDataApp *pRx) {

}
#endif

/**
 * TXイベント
 * @param u8CbId
 * @param bStatus
 */
static void cbAppToCoNet_vTxEvent(uint8 u8CbId, uint8 bStatus) {
	// 送信完了
	V_PRINTF(LB"! Tx Cmp = %d", bStatus);
	ToCoNet_Event_Process(E_ORDER_KICK, 0, vProcessEvCore);
}
/**
 * アプリケーションハンドラー定義
 *
 */
static tsCbHandler sCbHandler = {
	NULL, // cbAppToCoNet_u8HwInt,
	cbAppToCoNet_vHwEvent,
	NULL, // cbAppToCoNet_vMain,
	NULL, // cbAppToCoNet_vNwkEvent,
	NULL, // cbAppToCoNet_vRxEvent,
	cbAppToCoNet_vTxEvent
};

/**
 * アプリケーション初期化
 */
void vInitAppADXL345_LowEnergy() {
	psCbHandler = &sCbHandler;
	pvProcessEv1 = vProcessEvCore;
}

static void vProcessADXL345_LowEnergy(teEvent eEvent) {
	if (bSnsObj_isComplete(&sSnsObj)) {
		 return;
	}

	// イベントの処理
	vSnsObj_Process(&sSnsObj, eEvent); // ポーリングの時間待ち
	if (bSnsObj_isComplete(&sSnsObj)) {
		u8sns_cmplt |= E_SNS_ADXL345_CMP;

		V_PRINTF(LB"!ADXL345: X : %d, Y : %d, Z : %d",
			sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_X],
			sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Y],
			sObjADXL345.ai16Result[ADXL345_LOWENERGY_IDX_Z]
		);

		// 完了時の処理
		if (u8sns_cmplt == E_SNS_ALL_CMP) {
			ToCoNet_Event_Process(E_ORDER_KICK, 0, vProcessEvCore);
		}
	}
}

/**
 * センサー値を格納する
 */
static void vStoreSensorValue() {
	// センサー値の保管
	sAppData.sSns.u16Adc1 = sAppData.sObjADC.ai16Result[TEH_ADC_IDX_ADC_1];
#ifdef USE_TEMP_INSTDOF_ADC2
	sAppData.sSns.u16Adc2 = sAppData.sObjADC.ai16Result[TEH_ADC_IDX_TEMP];
#else
	sAppData.sSns.u16Adc2 = sAppData.sObjADC.ai16Result[TEH_ADC_IDX_ADC_2];
#endif
	sAppData.sSns.u8Batt = ENCODE_VOLT(sAppData.sObjADC.ai16Result[TEH_ADC_IDX_VOLT]);

	// ADC1 が 1300mV 以上(SuperCAP が 2600mV 以上)である場合は SUPER CAP の直結を有効にする
	if (sAppData.sSns.u16Adc1 >= VOLT_SUPERCAP_CONTROL) {
		vPortSetLo(DIO_SUPERCAP_CONTROL);
	}
}
