import serial, time

class SL500_RFID_Reader(object):
	"""SL500 RFID Reader Python API by Soft Power Group""" 
	"""SoftPowerGroup.net"""

	"""Full Library for Read/Write data , Read/Write Value ,Inc/Dec Value""" 
	"""Please Contact"""
	"""SoftPowerGroup.net"""

	BAUD_4800	= '\x00'
	BAUD_9600	= '\x01'
	BAUD_14400	= '\x02'
	BAUD_19200	= '\x03'
	BAUD_28800	= '\x04'
	BAUD_38400	= '\x05'
	BAUD_57600	= '\x06'
	BAUD_115200	= '\x07'

	LED_OFF		= '\x00'
	LED_RED		= '\x01'
	LED_GREEN	= '\x02'
	LED_YELLOW	= '\x03'

	TYPE_A		= 'A'
	TYPE_B		= 'B'
	ISO15693	= '1'

	RF_OFF		= '\x00'
	RF_ON		= '\x01'

	REQ_STD		= '\x26'
	REQ_ALL		= '\x52'

	KEY_A		= '\x60'
	KEY_B		= '\x61'

	DEBUG_MODE	= False
	MUTE_MODE	= False

	def __init__(self, port, baudrate):
		super(SL500_RFID_Reader, self).__init__()
		self.ser = serial.Serial(port, baudrate, timeout=0.02)
		self.rf_init_com()
		# self.rf_get_model()
		# self.rf_init_device_number()
		# self.rf_get_device_number()
		self.rf_init_type(self.TYPE_A) 
		self.rf_antenna_sta()

	def info(self):
		print(self.ser)
		print(self.BAUD_19200)
		
	# def min(self, a, b):
	# 	if (a < b):
	# 		return a
	# 	else:
	# 		return b

	# def max(self, a, b):
	# 	if (a > b):
	# 		return a
	# 	else:
	# 		return b

	def debug(self, source):
		if self.DEBUG_MODE:
			if isinstance(source, list):
				output = []
				for i in xrange(0, len(source)):
					output.insert(i, hex(ord(source[i])))
			else:
				output = source
			print output
		else:
			return

	def xor_strings(self, xs, ys):
		return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

	def read_response(self):
		all_output = []
		output = ''
		i = 0
		output = self.ser.read()
		while output != '':
			if i == 0:
				pass
			else:
				output = self.ser.read()
			if (i == 8) & (output != '\x00'):
				return False
			if output != '':
				all_output.insert(i, output)
			i += 1
		self.ser.flushOutput()
		return all_output

	def send_request(self, dev_id, cmd_code, param):
		length = len(param) + 5
		ver = '\x00'
		buf = []
		buf.insert(0, '\xAA')				# Command head
		buf.insert(1, '\xBB')
		buf.insert(2, chr(length))			# Length
		buf.insert(3, '\x00')
		buf.insert(4, dev_id[0])			# Device ID
		buf.insert(5, dev_id[1])
		buf.insert(6, cmd_code[0])			# Command code
		buf.insert(7, cmd_code[1])
		k = 0
		for i in range(8 , 8 + len(param)):
			buf.insert(i, param[k])
			k += 1
		for i in range(3 , len(buf)):
			ver = self.xor_strings(ver, buf[i])
		buf.insert(len(buf), ver)
		self.debug(buf)
		self.ser.write(buf)
		self.ser.flushInput()

	def rf_init_com(self):
		self.send_request(['\x00','\x00'], ['\x01','\x01'], [self.BAUD_19200])
		result = self.read_response()
		self.debug(result)
		return result

	def rf_get_model(self):
		self.send_request(['\x00','\x00'], ['\x04','\x01'], [])
		result = self.read_response()
		debug(result)
		return result

	def rf_init_device_number(self):
		self.send_request(['\x00','\x00'], ['\x02','\x01'], ['\x11','\x12'])
		result = self.read_response()
		self.debug(result)
		return result

	def rf_get_device_number(self):
		self.send_request(['\x00','\x00'], ['\x03','\x01'], [])
		result = self.read_response()
		debug(result)
		return result

	def rf_beep(self, time):
		if not self.MUTE_MODE:
			self.send_request(['\x11','\x12'], ['\x06','\x01'], [chr(time)])
			result = self.read_response()
			self.debug(result)
			return result

	def rf_light(self, color):
		self.send_request(['\x11','\x12'], ['\x07','\x01'], [color])
		result = self.read_response()
		self.debug(result)
		return result

	def rf_init_type(self, type):
		self.send_request(['\x00','\x00'], ['\x08','\x01'], [type])
		result = self.read_response()
		self.debug(result)
		return result

	def rf_antenna_sta(self):
		self.send_request(['\x11','\x12'], ['\x0c','\x01'], [self.RF_OFF])
		result = self.read_response()
		self.debug(result)
		return result

	def rf_request(self):
		self.send_request(['\x11','\x12'], ['\x01','\x02'], ['\x52'])
		result = self.read_response()
		self.debug(result)
		return result

	def rf_anticoll(self):
		self.send_request(['\x11','\x12'], ['\x02','\x02'], [])
		result = self.read_response()
		self.debug(result)
		return result

	def rf_select(self, card_id):
		self.send_request(['\x11','\x12'], ['\x03','\x02'], card_id)
		result = self.read_response()
		self.debug(result)
		return result

	def rf_M1_authentication2(self, block, key):
		param = ['\x60', chr(block), key[0], key[1], key[2], key[3], key[4], key[5]]
		self.send_request(['\x11','\x12'], ['\x07','\x02'], param)
		result = self.read_response()
		self.debug(result)
		return result

	def rf_read(self, block):
		self.send_request(['\x11','\x12'], ['\x08','\x02'], [chr(block)])
		result = self.read_response()
		result = self.read_response()
		if result:
			self.debug(result)
			output = ''
			for i in xrange(9, len(result) - 1):
				output += str(result[i].encode('hex'))
			return output
		else:
			return 'Reading RFID card is failed'

	def read_block(self, block):
		self.rf_light(self.LED_RED)
		if self.rf_request():
			result = self.rf_anticoll()
			if result:
				card_id = [result[9],result[10],result[11],result[12]]
				if self.rf_select(card_id):
					if self.rf_M1_authentication2(block, self.key) != False:
						self.rf_beep(1)
						self.rf_light(self.LED_GREEN)
						return self.rf_read(block)
					else:
						self.rf_beep(20)
						self.rf_light(self.LED_RED)
						return 'Authentication failed'		
		else:
			self.rf_beep(20)
			self.rf_light(self.LED_RED)
			return 'Cannot read RFID card'
	
	def set_key(self, key):
		self.key = key

	def close(self):
		self.ser.close()


	"""Full Library for Read/Write data , Read/Write Value ,Inc/Dec Value""" 
	"""Please Contact"""
	"""SoftPowerGroup.net"""		