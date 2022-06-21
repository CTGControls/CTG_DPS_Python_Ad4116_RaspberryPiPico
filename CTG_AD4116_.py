from CTG_AD4116Class import *
import board
import busio
import digitalio
from adafruit_bus_device.spi_device import SPIDevice
import time




class CTG_AD4116_:

    def startup(spiClk: int, CTG_AD4116: CTG_AD4116Class):
        #with busio.SPI(board.SCK, board.MOSI, board.MISO) as spi_bus:
        with busio.SPI(clock=board.GP2, MOSI=board.GP3,MISO=board.GP4) as spi_bus:


            cs = digitalio.DigitalInOut(board.GP10)
            cs.direction = digitalio.Direction.OUTPUT
            cs.value = False
            fspi = SPIDevice(spi_bus, cs, cs_active_value=False, polarity=1, phase=1,baudrate=spiClk)

            # check if the id matches 0x34DX, where X is don't care 
            CTG_AD4116.is_valid_id(fspi,spiClk)

            #/* set ADC input channel configuration */
            #/* enable channel 0 and channel 1 and connect each to 2 analog inputs for bipolar input */
            #/* CH0 - CH15 */
            #/* true/false to enable/disable channel */
            #/* SETUP0 - SETUP7 */
            #/* AIN0 - AIN16 */
            CTG_AD4116.set_channel_config(fspi, spiClk, adc7173_register_t.CH0, True, adc7173_register_t.SETUP0, analog_input_t.AIN0, analog_input_t.AIN1)

            #/* set the ADC SETUP0 coding mode to BIPLOAR output */
            #/* SETUP0 - SETUP7 */
            #/* BIPOLAR, UNIPOLAR */
            #/* AIN_BUF_DISABLE, AIN_BUF_ENABLE */
            #/* REF_EXT, REF_AIN, REF_INT, REF_PWR */
            CTG_AD4116.set_setup_config(fspi, spiClk, adc7173_register_t.SETUP0, coding_mode_t.BIPOLAR, ain_buf_mode_t.AIN_BUF_ENABLE, setup_ref_source_t.REF_EXT)

            #/* set ADC OFFSET0 offset value */
            #/* OFFSET0 - OFFSET7 */
            CTG_AD4116.set_offset_config(fspi, spiClk, adc7173_register_t.OFFSET0, 0x55) 


            #/* set the ADC FILTER0 ac_rejection to false and samplingrate to 1007 Hz */
            #/* FILTER0 - FILTER7 */
            #/* SPS_1, SPS_2, SPS_5, SPS_10, SPS_16, SPS_20, SPS_49, SPS_59, SPS_100, SPS_200 */
            #/* SPS_381, SPS_503, SPS_1007, SPS_2597, SPS_5208, SPS_10417, SPS_15625, SPS_31250 */
            #//CTG_AD4116.set_filter_config(fspi, spiClk, FILTER0, SPS_100);


            if(DEBUG_ENABLED):
                print(" ")
                print("set_filter_config:  ")

            #/* prepare the configuration value */
            value =  bytearray([0x00, 0x00])
            #/* SINC3_MAP0 [15], RESERVED [14:12], ENHFILTEN0 [11], ENHFILT0 [10:8], RESERVED [7], ORDER0 [6:5], ORD0 [4:0] */
            value[0] = 0x0E
            value[1] = 0x73

            #/* update the configuration value */
            CTG_AD4116.set_register(fspi, spiClk, adc7173_register_t.FILTER0, value, 2)

            #/* verify the updated configuration value */
            CTG_AD4116.get_register(fspi, spiClk, adc7173_register_t.FILTER0, value, 2)

            #/* set the ADC data and clock mode */
            #/* CONTINUOUS_CONVERSION_MODE, SINGLE_CONVERSION_MODE */
            #/* in SINGLE_CONVERSION_MODE after all setup channels are sampled the ADC goes into STANDBY_MODE */
            #/* to exit STANDBY_MODE use this same function to go into CONTINUOUS or SINGLE_CONVERSION_MODE */
            #/* INTERNAL_CLOCK, INTERNAL_CLOCK_OUTPUT, EXTERNAL_CLOCK_INPUT, EXTERNAL_CRYSTAL */
            #/* REF_DISABLE, REF_ENABLE */
            CTG_AD4116.set_adc_mode_config(fspi, spiClk, data_mode_t.CONTINUOUS_CONVERSION_MODE, clock_mode_t.INTERNAL_CLOCK, ref_mode_t.REF_DISABLE);

            #/* enable/disable CONTINUOUS_READ_MODE and appending STATUS register to data */
            #/* to exit CONTINUOUS_READ_MODE use CTG_AD4116.reset(); */
            #/* CTG_AD4116.reset(); returns all registers to default state, so everything has to be setup again */
            #/* true / false to enable / disable appending status register to data, 4th byte */
            CTG_AD4116.set_interface_mode_config(fspi, spiClk, False, False);

            #/* wait for ADC */
            time.sleep(0.1)



#from CTG_AD4116_Types import Color
#from CTG_AD4116_Types import *

#import CTG_AD4116_Types
#print(CTG_AD4116_Types.Color.CONTINUOUS_CONVERSION_MODE)

#from CTG_AD4116_Types import adc7173_register_t

        return 0
