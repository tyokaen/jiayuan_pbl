/****************************************************************************
 * (C) Tokyo Cosmos Electric, Inc. (TOCOS) - 2012 all rights reserved.
 *
 * Condition to use:
 *   - The full or part of source code is limited to use for TWE (TOCOS
 *     Wireless Engine) as compiled and flash programmed.
 *   - The full or part of source code is prohibited to distribute without
 *     permission from TOCOS.
 *
 ****************************************************************************/

#ifndef  ADXL345_INCLUDED
#define  ADXL345_INCLUDED

#if defined __cplusplus
extern "C" {
#endif

/****************************************************************************/
/***        Include Files                                                 ***/
/****************************************************************************/

/****************************************************************************/
/***        Macro Definitions                                             ***/
/****************************************************************************/
#define ADXL345_LOWENERGY_IDX_X 0
#define ADXL345_LOWENERGY_IDX_Y 1
#define ADXL345_LOWENERGY_IDX_Z 2

#define ADXL345_LOWENERGY_IDX_BEGIN 0
#define ADXL345_LOWENERGY_IDX_END (ADXL345_LOWENERGY_IDX_Z+1) // should be (last idx + 1)
/****************************************************************************/
/***        Type Definitions                                              ***/
/****************************************************************************/
typedef struct {
	// protected
	bool_t	bBusy;			// should block going into sleep

	// data
	int16	ai16Result[3];
	uint8	u8Interrupt;

	// working
	uint8	u8TickCount, u8TickWait;
} tsObjData_ADXL345;

/****************************************************************************/
/***        Exported Functions (state machine)                            ***/
/****************************************************************************/

/****************************************************************************/
/***        Exported Functions (primitive funcs)                          ***/
/****************************************************************************/
bool_t bADXL345_LowEnergy_Setting();

PUBLIC bool_t bADXL345_LowEnergyReset();
PUBLIC bool_t bADXL345_LowEnergyStartRead();
//PUBLIC uint8* i16ADXL345_LowEnergyReadResult( uint8 u8axis, uint8* ui8res, uint8 i );
PUBLIC int16 i16ADXL345_LowEnergyReadResult( uint8 u8axis );
PUBLIC uint8 i16ADXL345_ReadInter();

/****************************************************************************/
/***        Exported Variables                                            ***/
/****************************************************************************/
#if defined __cplusplus
}
#endif

#endif  /* ADXL345_INCLUDED */

/****************************************************************************/
/***        END OF FILE                                                   ***/
/****************************************************************************/
