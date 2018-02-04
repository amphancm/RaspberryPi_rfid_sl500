from rfid_sl500 import SL500_RFID_Reader

reader = SL500_RFID_Reader('/dev/ttyUSB0', 19200)
# reader.DEBUG_MODE = True
# reader.MUTE_MODE = True
reader.set_key('\xFF\xFF\xFF\xFF\xFF\xFF')

card_data = reader.read_block(0)
print card_data

























reader.close()