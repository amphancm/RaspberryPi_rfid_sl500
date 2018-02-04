from rfid_sl500 import SL500_RFID_Reader
from time import sleep

reader = SL500_RFID_Reader('/dev/ttyUSB0',19200)


def main():
	try:
		#reader = SL500_RFID_Reader('COM5', 19200)
		reader = SL500_RFID_Reader('/dev/ttyUSB0',19200)
	except:
		print 'No RFID Reader'
		return	

	#print reader
	# reader.DEBUG_MODE = True
	# reader.MUTE_MODE = True
	reader.set_key('\xFF\xFF\xFF\xFF\xFF\xFF')


	try:
		card_data = reader.read_block(0)
	except:
		print 'No RFID Card'
		return	

	print card_data
	reader.close()


if __name__ == '__main__':
	while(1):
		main()
		sleep(3)


