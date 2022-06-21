import time
from adafruit_bus_device.spi_device import SPIDevice
from CTG_AD4116Types import *


DEBUG_ENABLED = True

class CTG_AD4116Class:
	#/* ADC data mode */
	m_data_mode = bool(False)

	def __init__(self):
		time.sleep(10)

	def init(SPIDevice):
		return 0

	def print_byte(value):
		format = "0x%.2X " % value
		print(format)
		return

	def set_register(spi: SPIDevice, spiClk: int, reg: adc7173_register_t , value: bytearray, value_len: int):
		readWritebuff = bytearray(value_len)

		i=0
		while i < value_len and i < len(value):
			readWritebuff[i] = value[i]
			if i == len(value) - 1:
				readWritebuff[i] = readWritebuff[i]
			i += 1

		with spi as device:
			device.write(bytes([0x00]))

		with spi as device:
			device.write(bytes([0x00]))
			device.write(bytes([0x00 | reg]))
			device.write(readWritebuff)
		value[:] = readWritebuff[:] 

		if(DEBUG_ENABLED):
			msg = ("set_register: set [ " )
			for result in readWritebuff:
				format = "0x%.2X " % result
				msg += str(format)
			msg += "] from reg [ "
			format = "0x%.2X " % reg
			msg += str(format)
			msg += " ]"
			print(msg)
			#CTG_AD4116Class.get_register(spi, spiClk, reg, value, value_len)
		return readWritebuff

	def get_register(spi: SPIDevice, spiClk: int, reg: adc7173_register_t , value: bytearray, value_len: int):
		readWritebuff = bytearray(value_len)

		i=0
		while i < value_len and i < len(value):
			readWritebuff[i] = value[i]
			i += 1

		with spi as device:
			#device.write(bytes([0x00,0x00]))
			device.write(bytes([0x40 | reg]))



			device.readinto(readWritebuff)
		value[:] = readWritebuff[:]

		if(DEBUG_ENABLED):
			msg = ("get_register: got [ " )
			for result in readWritebuff:
				format = "0x%.2X " % result
				msg += str(format)
			msg += "] from reg [ "
			format = "0x%.2X " % reg
			msg += str(format)
			command = 0x40 | reg
			format = "0x%.2X " % command
			msg += "] using command [ " 
			msg += format
			msg += " ] "
			print(msg)
		return readWritebuff


	def set_adc_mode_config(spi: SPIDevice, spiClk: int, data_mode: data_mode_t, clock_mode: clock_mode_t, ref_mode:ref_mode_t):
		#/* Address: 0x01, Reset: 0x2000, Name: ADCMODE */
		if(DEBUG_ENABLED):
			print(" ")
			print("CTG_AD4116Class.set_adc_mode_config:  ")

		#/* prepare the configuration value */
		#/* REF_EN [15], RESERVED [14], SING_CYC [13], RESERVED [12:11], DELAY [10:8], RESERVED [7], MODE [6:4], CLOCKSEL [3:2], RESERED [1:0] */
		value = bytearray([0x00,0x00])
		value[1] = ((data_mode << 4) | (clock_mode << 2)) & 0xFF
		value[0] = (ref_mode << 7) & 0xFF

		#/* update the configuration value */
		CTG_AD4116Class.set_register(spi, spiClk, adc7173_register_t.ADCMODE_REG, value, 2)

		#/* verify the updated configuration value */
		CTG_AD4116Class.get_register(spi, spiClk, adc7173_register_t.ADCMODE_REG, value, 2)

		#/* return error code */
		return 0

	def set_interface_mode_config(spi: SPIDevice, spiClk: int, continuous_read: bool, append_status_reg: bool):
		#/* Address: 0x02, Reset: 0x0000, Name: IFMODE */

		if(DEBUG_ENABLED):
			print(" ")
			print("CTG_AD4116Class.set_interface_mode_config:  ")

		#/* prepare the configuration value */
		#/* RESERVED [15:13], ALT_SYNC [12], IOSTRENGTH [11], HIDE_DELAY [10], RESERVED [9], DOUT_RESET [8], CONTREAD [7], DATA_STAT [6], REG_CHECK [5], RESERVED [4], CRC_EN [3:2], RESERVED [1], WL16 [0] */
		value = bytearray([0x00,0x00])
		value[1] = ((continuous_read << 7) | (append_status_reg << 6))  & 0xFF

		#/* update the configuration value */
		CTG_AD4116Class.set_register(spi, spiClk, adc7173_register_t.IFMODE_REG, value, 2)

		#/* verify the updated configuration value */
		CTG_AD4116Class.get_register(spi, spiClk, adc7173_register_t.IFMODE_REG, value, 2)

		#/* when continuous read mode */
		if continuous_read:
			#/* update the data mode */
			CTG_AD4116Class.m_data_mode = data_mode_t.CONTINUOUS_READ_MODE

		#/* enable or disable appending status reg to data */
		CTG_AD4116Class.append_status_reg = append_status_reg

		#/* return error code */
		return 0
	
	def is_valid_id(spi: SPIDevice, spiClk: int):
		#/* get the ADC device ID */
		if(DEBUG_ENABLED):
			print(" ")
			print("CTG_AD4116Class.is_valid_id:  ")	

		value = bytearray([0x00,0x00])

		CTG_AD4116Class.get_register(spi, spiClk, adc7173_register_t.ID_REG, value, 2)

		#/* check if the id matches 0x30DX, where X is don't care */
		valid_id = value[0] == 0x34 and value[1] == 0xD0
		if(DEBUG_ENABLED):
			if (valid_id):
				print("AD4116 ID is valid" )
			else:
				print("AD4116 ID is invalid")

	
	def set_channel_config(spi: SPIDevice, spiClk: int, channel: adc7173_register_t , enable: bool, setup: adc7173_register_t, ain_pos: analog_input_t, ain_neg: analog_input_t ):
		#Address: 0x10, Reset: 0x8001, Name: CH0
		#Address Range: 0x11 to 0x1F, 
		#Reset: 0x0001, 
		#Name: CH1 to CH15

		if(DEBUG_ENABLED):
			print(" ")
			print("CTG_AD4116Class.set_channel_config:  ")		
		#prepare the configuration value
		#CH_EN0 [15], SETUP_SEL0 [14:12], RESERVED [11:10], AINPOS0 [9:5], AINNEG0 [4:0]
		value = bytearray([0x00,0x00])

		value[0] = ((enable << 7) | (setup << 4) | (ain_pos >> 3)) & 0xFF
		value[1] = ((ain_pos << 5) | ain_neg) & 0xFF

		#update the configuration value */
		CTG_AD4116Class.set_register(spi, spiClk, channel, value, 2)

		#verify the updated configuration value */
		CTG_AD4116Class.get_register(spi, spiClk, channel, value, 2)

		#return error code
		return 0
	
	def set_setup_config(spi: SPIDevice, spiClk: int, setup: adc7173_register_t , coding_mode: coding_mode_t, ain_buf_mode: ain_buf_mode_t,setup_ref_source: setup_ref_source_t ):
		#/* Address Range: 0x20 to 0x27, Reset: 0x1000, Name: SETUPCON0 to SETUPCON7 */

		if(DEBUG_ENABLED):
			print(" ")
			print("CTG_AD4116Class.set_setup_config:  ")

		#/* prepare the configuration value */
		value = bytearray([0x00,0x00])
		value[0] = ((coding_mode << 4) | ain_buf_mode) & 0xFF
		value[1] = ((setup_ref_source << 4)) & 0xFF

		#/* update the configuration value */
		CTG_AD4116Class.set_register(spi, spiClk, setup, value, 2)

		#/* verify the updated configuration value */
		CTG_AD4116Class.get_register(spi, spiClk, setup, value, 2)

		#/* return error code */
		return 0

	def set_offset_config(spi: SPIDevice, spiClk: int, offset: adc7173_register_t , offset_value: int):

		if(DEBUG_ENABLED):
			print(" ")
			print("CTG_AD4116Class.set_offset_config:  ")
		#/* Address Range: 0x30 to 0x37, Reset: 0x0000, Name: OFFSET0 to OFFSET7 */

		#/* add the default offset value */
		offset_value += 8388608;
		#/* prepare the configuration value */
		value = bytearray([0x00,0x00,0x00])
		value[0] = (offset_value >> 16) & 0xFF
		value[1] = (offset_value >> 8) & 0xFF
		value[2] = (offset_value) & 0xFF 
		x = int(0)

		#/* update the configuration value */
		CTG_AD4116Class.set_register(spi, spiClk, offset, value, 3)
		while True and x < 10000:
			#/* update the configuration value */
			CTG_AD4116Class.get_register(spi, spiClk, offset, value, 3)
		time.sleep(0.5)

		#/* return error code */
		return 0