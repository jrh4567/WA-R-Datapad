#Created by Jackson Holbrook for Whitefield Robotics, FTC team 11127
#Match data input has been commented out or changed by other notation, as its not actually necessary, or used at all.
#time.sleep("Memes") #instant kill
import time
import board
import displayio
from adafruit_pyportal import PyPortal
from adafruit_button import Button
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from terminalio import FONT
import adafruit_sdcard
import os
import digitalio
import busio
import storage
import adafruit_touchscreen
import gc
#from datapad_methods import datapadHelper #can't import other file b/c of memory limits
gc.enable()
print("Total Free RAM: ", gc.mem_free())
print("Total Allocated RAM: ", gc.mem_alloc())
cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)

# Fonts within /fonts folder
medium_font = cwd+"/fonts/Arial-16.bdf"
header_font = cwd+"/fonts/Collegiate-24.bdf"
#other_font = cwd+"/fonts/Arial-ItalicMT-17.bdf"
nunito_font = cwd+"/fonts/Nunito-Black-17.bdf"
arial12 = cwd+"/fonts/Arial-12.bdf"

print('loading fonts...')
arial_16 = bitmap_font.load_font(medium_font)
h_font = bitmap_font.load_font(header_font)
#arial_o = bitmap_font.load_font(other_font)
nunito = bitmap_font.load_font(nunito_font)
arial_12 = bitmap_font.load_font(arial12)

print("RAM (post-fonts load): ", gc.mem_free())

HEX_WHITE = 0xFFFFFF
HEX_BLUE = 0x0000FF
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
OFF = (0, 0, 0)
BLACK = 0x0


print("Loading...")
loadingScreenGroup = displayio.Group(max_size=5)
loading = Label(nunito, text="Loading,", color=HEX_WHITE, x=10, y=120)
plsWait = Label(nunito, text="please wait...", color=HEX_WHITE, x=10, y=135)
board.DISPLAY.show(loadingScreenGroup)
#board.DISPLAY.show(loadingScreenGroup)
#bufferGroup = displayio.Group(max_size=1)
#board.DISPLAY.show(bufferGroup)

print("RAM (before wolf load): ", gc.mem_free())
#'''
with open("/HowlingWolf.bmp", "rb") as f:
    odb = displayio.OnDiskBitmap(f)
    face = displayio.TileGrid(bitmap=odb, pixel_shader=displayio.ColorConverter()) #, position=(0,0))
    loadingScreenGroup.append(face)
    #'''
    loadingScreenGroup.append(loading)
    loadingScreenGroup.append(plsWait)
    #board.DISPLAY.show(loadingScreenGroup)
    # Wait for the image to load.
    board.DISPLAY.wait_for_frame()
gc.collect()
print("RAM (after wolf load): ", gc.mem_free())

#loadingScreenGroup.append(Label(arial_12, text="FTC-Skysotne \nSeason", color=HEX_WHITE, x=220, y=125))
loadingScreenGroup.append(Label(arial_12, text="Created By WA-R", color=HEX_WHITE, x=10, y=232))

dispelements = []
dispbuttons = []

superdict = {}

matchid = 0
teamid = 0

delay = 0.01
#/////////////Make Sure these are correct at the beginning of season////////////////////////
numStats = 12
columnHeaders = "TEAM_NUM,MATCH,rePosBase,delivSkySt,delivRegSt,placeSt_A,parkOnTape,delivTele,placeSt,towerLevel,capTower,capLevel,removeBase,parkInSite"

''' 
Repositioning Foundation to Building Site	= rePosBase
Delivering Skystones 						= delivSkySt
Delivering Stones under Alliance Skybridge	= delivRegSt
Placing Stones on Foundation 				= placeSt_A
Navigating under Skybridge					= parkOnTape

Driver-Controlled Period Scoring:
Delivering Stones under Alliance Skybridge 	= delivTele
Placing Stones on Foundation				= placeSt
Skyscraper Bonus							= towerLevel

End Game Scoring:
Capping Bonus								= capTower
Level Bonus 								= capLevel
Moving Foundation from Building Site 		= removeBase
Parking in Building Site					= parkInSite

'''
#//////////////////////////////////////////////////////////////////////////////////////////




# Set the background color
BACKGROUND_COLOR = 0x000000


#dpm = datapadHelper(11) #can't import other file b/c of memory limits
#dpm.ext_print_test()

print("Mounting SD Card")
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
print("SD Card Directories: ")
print(os.listdir('/sd'))

print("Initializing touchscreen")
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
                                      board.TOUCH_YD, board.TOUCH_YU,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(320, 240))


''' INITing TEAM ID Keypad '''


keypadSpots = [
	{'id': "0", 'pos': (10, 200), 'size': (160, 40), 'color': WHITE, 'label': "0"},
	{'id': "1", 'pos': (10, 150), 'size': (75, 40), 'color': WHITE, 'label': "1"},
	{'id': "2", 'pos': (95, 150), 'size': (75, 40), 'color': WHITE, 'label': "2"},
	{'id': "3", 'pos': (180, 150), 'size': (75, 40), 'color': WHITE, 'label': "3"},
	{'id': "4", 'pos': (10, 100), 'size': (75, 40), 'color': WHITE, 'label': "4"},
	{'id': "5", 'pos': (95, 100), 'size': (75, 40), 'color': WHITE, 'label': "5"},
	{'id': "6", 'pos': (180, 100), 'size': (75, 40), 'color': WHITE, 'label': "6"},
	{'id': "7", 'pos': (10, 50), 'size': (75, 40), 'color': WHITE, 'label': "7"},
	{'id': "8", 'pos': (95, 50), 'size': (75, 40), 'color': WHITE, 'label': "8"},
	{'id': "9", 'pos': (180, 50), 'size': (75, 40), 'color': WHITE, 'label': "9"},
	#{'id': "N", 'pos': (260, 150), 'size': (75, 40), 'color': WHITE, 'label': "N"},
	{'id': "clear", 'pos': (180, 200), 'size': (75, 40), 'color': WHITE, 'label': "C"},
	{'id': "acc", 'pos': (260, 200), 'size': (75, 40), 'color': GREEN, 'label': "A"},
]

keypadGroup = displayio.Group(max_size=15)

kbuttons = []
for spot in keypadSpots:
    button = Button(x=spot['pos'][0], y=spot['pos'][1],
                    width=spot['size'][0], height=spot['size'][1],
                    style=Button.ROUNDRECT,
                    fill_color=spot['color'], outline_color=0x222222,
                    name=spot['id'],label=spot['label'], label_font=arial_16)
    kbuttons.append(button)
    keypadGroup.append(button.group)
    print("Adding {} to kButtons".format(spot))


preMainGroup = displayio.Group(max_size=5) # if getting weird errors, increase max size
preMainGroup.append(keypadGroup)

#matchIdLabelText = Label(arial_16, text="Match ID:", color=HEX_WHITE, x=10, y=30)  #uncomment for matchid
#preMainGroup.append(matchIdLabelText)  #uncomment for matchid

#matchIdLabel = Label(arial_16, text="00", color=HEX_WHITE, x=110, y=30) #uncomment for matchid
#preMainGroup.append(matchIdLabel)  #uncomment for matchid

teamIdLabelText = Label(arial_16, text="Team ID:", color=HEX_WHITE, x=155, y=30)
preMainGroup.append(teamIdLabelText)

teamIdLabel = Label(arial_16, text="00000", color=HEX_WHITE, x=255, y=30)
preMainGroup.append(teamIdLabel)



def k_update_display():
    gc.collect()
    """Update the display with current info."""
    #matchIdLabel.text = "{00}".format(matchid)  #uncomment for matchid
    teamIdLabel.text = "{00000}".format(teamid)    
    board.DISPLAY.refresh_soon()

print("RAM (after keypad init, pre-spots): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())

""" INITing main disp elements """
#rePosBase: 95, 50
#nextpage: 10, 200
spots = [
	#PAGE 16
	{'id': "nextpage",		'Type': 'select',	 'pos': (10, 200), 'size': (70, 45), 'color': GREEN, 'label': "Next"}, #correct
	
	{'id': "rePosBase",		'Type': 'boolean',	 'pos': (95, 50), 'size': (70, 50), 'color': GRAY, 'label': "False"}, #correct
	
	{'id': "parkOnTape",	'Type': 'boolean',	 'pos': (95, 110), 'size': (70, 50), 'color': GRAY, 'label': "False"}, #correct
	
	{'id': "delivSkySt+",	'Type': 'int',		 'pos': (260, 35), 'size': (60, 40), 'color': BLUE, 'label': "+1"}, #correct
	{'id': "delivSkySt-",	'Type': 'int',		 'pos': (200, 35), 'size': (60, 40), 'color': RED, 'label': "-1"}, #correct
	
	{'id': "delivRegSt+",	'Type': 'int',		 'pos': (260, 110), 'size': (60, 40), 'color': BLUE, 'label': "+1"}, #correct
	{'id': "delivRegSt-",	'Type': 'int',		 'pos': (200, 110), 'size': (60, 40), 'color': RED, 'label': "-1"}, #correct
	
	{'id': "placeSt_A+",	'Type': 'int',		 'pos': (260, 185), 'size': (60, 40), 'color': BLUE, 'label': "+1"}, #correct
	{'id': "placeSt_A-",	'Type': 'int',		 'pos': (200, 185), 'size': (60, 40), 'color': RED, 'label': "-1"}, #correct
	
	#PAGE 2
	{'id': "back",			'Type': 'select',	 'pos': (10, 200), 'size': (70, 40), 'color': RED, 'label': "Back"}, #correct
	{'id': "write",			'Type': 'eject',	 'pos': (85, 200), 'size': (70, 45), 'color': GREEN, 'label': "Write"}, #correct
	
	{'id': "capTower",		'Type': 'boolean',	 'pos': (100, 45), 'size': (70, 45), 'color': GRAY, 'label': "False"}, #correct
	
	{'id': "removeBase",	'Type': 'boolean',	 'pos': (100, 95), 'size': (70, 45), 'color': GRAY, 'label': "False"}, #correct
	
	{'id': "parkInSite",	'Type': 'boolean',	 'pos': (100, 145), 'size': (70, 45), 'color': GRAY, 'label': "False"}, #correct
	
	{'id': "delivTele+",	'Type': 'int',		 'pos': (260, 18), 'size': (60, 40), 'color': BLUE, 'label': "+1"}, #correct
	{'id': "delivTele-",	'Type': 'int',		 'pos': (200, 18), 'size': (60, 40), 'color': RED, 'label': "-1"}, #correct
	
	{'id': "placeSt+",		'Type': 'int',		 'pos': (260, 75), 'size': (60, 40), 'color': BLUE, 'label': "+1"}, #correct
	{'id': "placeSt-",		'Type': 'int',		 'pos': (200, 75), 'size': (60, 40), 'color': RED, 'label': "-1"}, #correct
	
	{'id': "towerLevel+",	'Type': 'int',		 'pos': (260, 132), 'size': (60, 40), 'color': BLUE, 'label': "+1"}, #correct
	{'id': "towerLevel-",	'Type': 'int',		 'pos': (200, 132), 'size': (60, 40), 'color': RED, 'label': "-1"}, #correct
	
	{'id': "capLevel+",		'Type': 'int',		 'pos': (260, 189), 'size': (60, 40), 'color': BLUE, 'label': "+1"}, #correct
	{'id': "capLevel-",		'Type': 'int',		 'pos': (200, 189), 'size': (60, 40), 'color': RED, 'label': "-1"}, #correct
	]

print("RAM (post-spots): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())
page1 = ["nextpage", "rePosBase", "delivSkySt+", "delivSkySt-", "delivRegSt+", "delivRegSt-", "placeSt_A+", "placeSt_A-", "parkOnTape"]
page2 = ["back", "write", "delivTele+", "delivTele-", "placeSt+", "placeSt-", "towerLevel+", "towerLevel-", "capLevel+", "capLevel-", "capTower", "removeBase", "parkInSite"]

buttonsgroup1 = displayio.Group(max_size=len(page1))
buttonsgroup2 = displayio.Group(max_size=len(page2) + 1)

#buttons = []
buttonsAuto = []
buttonsTele = []
for spot in spots:
    button = Button(x=spot['pos'][0], y=spot['pos'][1],
                    width=spot['size'][0], height=spot['size'][1],
                    style=Button.ROUNDRECT,
                    fill_color=spot['color'], outline_color=0x222222,
                    name=spot['id'],label=spot['label'], label_font=arial_16)
    #buttons.append(button)
    if spot['id'] in page1:
        buttonsAuto.append(button)
        buttonsgroup1.append(button.group)
        print("Adding {} to pg1".format(spot))
    else:
        buttonsTele.append(button)
        buttonsgroup2.append(button.group)
        print("Adding {} to pg2".format(spot))



print("RAM (post-spots loop): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())

dispgroup1 = displayio.Group(max_size=9)

print("RAM (post-group init): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())

dispgroup1.append(Label(h_font, text="AutoScore", color=HEX_WHITE, x=15, y=25)) #correct

dispgroup1.append(Label(arial_12, text="BaseMove", color=HEX_WHITE, x=10, y=75)) #correct

dispgroup1.append(Label(arial_12, text="Park", color=HEX_WHITE, x=10, y=133)) #correct

dispgroup1.append(Label(arial_12, text="SkStDelived", color=HEX_WHITE, x=205, y=10)) #correct
delivSkyStLabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=27) #correct
dispgroup1.append(delivSkyStLabel)

dispgroup1.append(Label(arial_12, text="RgStDelived", color=HEX_WHITE, x=205, y=85)) #correct
delivRegStLabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=102) #correct
dispgroup1.append(delivRegStLabel) 

dispgroup1.append(Label(arial_12, text="StPlaced", color=HEX_WHITE, x=205, y=160)) #correct
placeSt_ALabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=177) #correct
dispgroup1.append(placeSt_ALabel)

print("RAM (post-dispgroup1): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())

dispgroup2 = displayio.Group(max_size=12)

dispgroup2.append(Label(h_font, text="TeleScore", color=HEX_WHITE, x=15, y=25)) #correct

dispgroup2.append(Label(arial_12, text="Cap", color=HEX_WHITE, x=10, y=60)) #correct

dispgroup2.append(Label(arial_12, text="RmoveBase", color=HEX_WHITE, x=10, y=110)) #correct

dispgroup2.append(Label(arial_12, text="Park", color=HEX_WHITE, x=10, y=160)) #correct

dispgroup2.append(Label(arial_12, text="Delivs", color=HEX_WHITE, x=205, y=10)) #correct
delivTeleLabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=10) #correct
dispgroup2.append(delivTeleLabel)

dispgroup2.append(Label(arial_12, text="Places", color=HEX_WHITE, x=205, y=67)) #correct
placeStLabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=67) #correct
dispgroup2.append(placeStLabel) 

dispgroup2.append(Label(arial_12, text="TwrLvl", color=HEX_WHITE, x=205, y=122)) #correct
towerLevelLabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=122) #correct
dispgroup2.append(towerLevelLabel)

dispgroup2.append(Label(arial_12, text="CapLvl", color=HEX_WHITE, x=205, y=180)) #correct
capLevelLabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=180) #correct
dispgroup2.append(capLevelLabel)

print("RAM (post-dispgroup2): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())
#'''
autoGroup = displayio.Group(max_size=5)
autoGroup.append(buttonsgroup1)
autoGroup.append(dispgroup1)

teleGroup = displayio.Group(max_size=5)
teleGroup.append(buttonsgroup2)
teleGroup.append(dispgroup2)

gc.collect()

print("RAM (post-labels)", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())

maindict = {
	"rePosBase"	: False,
	"delivSkySt": 0,
	"delivRegSt": 0,
	"placeSt_A"	: 0,
	"parkOnTape": False,
	"delivTele"	: 0,
	"placeSt"	: 0,
	"towerLevel": 0,
	"capTower"	: False,
	"capLevel"	: 0,
	"removeBase": False,
	"parkInSite": False
}
maindictorder = ["rePosBase", "delivSkySt", "delivRegSt", "placeSt_A", "parkOnTape", "delivTele", "placeSt", "towerLevel", "capTower", "capLevel", "removeBase", "parkInSite"]



def update_display(page):
	"""Update the display with current info."""
	#print("updating display")
	gc.collect()
	if page == 1:
		buttonArray = buttonsAuto
	else:
		buttonArray = buttonsTele
	
	for button in buttonArray:
		if button.name[len(button.name)-1:] in ["+", "-"]:
			type = "int"
		elif button.name in ["nextpage", "back", "write"]:
			type = "other"
		else:
			type = "boolean"
		#print("Looping through button {} with type {}".format(button.name, type))
		if type == "int":
			dictName = button.name[:len(button.name)-1]
			labelName = "{}Label".format(dictName)
			#print(labelName, dictName)
			exec('%s.text = "{00}".format(str(maindict["%s"]))' % (labelName, str(dictName)))
			
		elif type == "boolean":
			#maindict[button.name] = not(maindict[button.name])
			button.label = str(maindict[button.name])
			#print("maindict[{}] - {}".format(button.name, maindict[button.name]))
		gc.collect()
	#print("display update finished")

	'''
	pCtDepotDisp.text = "{000}".format(maindict["pCtDepot"])  
	pCtLanderDisp.text = "{000}".format(maindict["pCtLander"])
	
	#tf1 = buttons[3]
	if maindict["toggleDrop"] == True: 
		buttons[3].label = "True"
	else: #indentation visual glitch
		buttons[3].label = "False"

	#if lastPressed == "4":
	#tf2 = buttons[4]
	if maindict["toggleSample"] == True:
		buttons[4].label = "True"
	else:
		buttons[4].label = "False"
	'''
	gc.collect()
	print("RAM (update_disp): ", gc.mem_free())
	#print("Allocated RAM: ", gc.mem_alloc())
	board.DISPLAY.refresh_soon()


def sd_write():
	print("Writing to sd card...")
	superorder = []
	matchNum = 1
	
	for l in superdict:
		superorder.append(l)
		print(superorder)
	
	f = open('/sd/data.txt', 'a')
	#f.write(columnHeaders)
	#f.write("\n")
	for m in superorder:
		for x in range(len(superdict[m])):
			f.write(str(m)+",")
			f.write(str(matchNum)+",")
			matchNum += 1
			for y in range(numStats):
				if y == numStats-1:
					f.write(str(superdict[m][x][y]))
				else:
					f.write(str(superdict[m][x][y])+",")
				print(str(superdict[superorder[len(maindict)-1]][x][y]))
			f.write("\n")
		#f.write("\n")
	f.close()

def matrix_write():
	matchdata = []
	for v in maindictorder:
		if maindict.get(v) == False:
			matchdata.append("0")
		elif maindict.get(v) == True:
			matchdata.append("1")
		else:
			matchdata.append(str(maindict.get(v)))
		print(maindict.get(v))
	if teamid not in superdict:
		superdict[teamid] = []
	superdict[teamid].append(matchdata)
	print("Superdict:", superdict)

def write_data():
	matchdata = []
	for v in maindictorder:
		if maindict.get(v) == False:
			matchdata.append("0")
		elif maindict.get(v) == True:
			matchdata.append("1")
		else:
			matchdata.append(str(maindict.get(v)))
		print(maindict.get(v), "Appended to matchdata")
	print("Matchdata: {}".format(matchdata))
	
	f = open('/sd/data.txt', 'a')
	f.write("{},{},".format(teamid, matchid))
	
	for i in range(len(matchdata)):
		if i == numStats-1:
			f.write(str(matchdata[i])) #if end of sequence, don't add comma
		else:
			f.write(str(matchdata[i])+",")
	f.write("\n")
	f.close()

def handleButton(button):
	if button.name[len(button.name)-1:] in ["+", "-"]:
		type = "int"
	else:
		type = "boolean"
	
	if type == "int":
		dictName = button.name[:len(button.name)-1]
		if button.name[len(button.name)-1:] == "+":
			maindict[dictName] += 1
			print(dictName, maindict[dictName])
		elif button.name[len(button.name)-1:] == "-":
			maindict[dictName] -= 1
			print(dictName, maindict[dictName])
	
	if type == "boolean":
		maindict[button.name] = not(maindict[button.name])
		print(button.name, maindict[button.name])
		
gc.collect()
print("Writing Column Headers")
f = open('/sd/data.txt', 'a')
f.write(columnHeaders)
f.write("\n")
f.close()
print("Column Heads Written")
gc.collect()

#for i in range(len(loadingScreenGroup)):
#	loadingScreenGroup.pop(i)

gc.collect()
print("RAM (before loop main start): ", gc.mem_free())
#inPreMainLoop = 1
bypassKeyboard = False
print("Beginning Superloop")
while True:
	
	if bypassKeyboard == False:
		timesPressed = 0
		timesPressedMax = 5 #change to "2" for matchid
		inPreMainLoop = 1 #change to "2" for matchid
		board.DISPLAY.show(preMainGroup)
		k_update_display()
		gc.collect()
		print("Starting preMain Loop")
		print("RAM (post-spots loop): ", gc.mem_free())
		print("Allocated RAM: ", gc.mem_alloc())
		teamIdLabelText.color = HEX_BLUE
		timesPressedMax = 5
	while inPreMainLoop > 0:
		touch = ts.touch_point
		if touch:
			for button in kbuttons:
				if button.contains(touch):
					print("Touched", button.name)
					lastPressed = button.name
					if timesPressed < timesPressedMax:  #in coda, this looks wrong, but its fine
						if button.name in ["0","1","2","3","4","5","6","7","8","9"]:
							if inPreMainLoop == 2:
								matchid = int(str(matchid)+str(button.name))
								print("matchid:", matchid)
							if inPreMainLoop == 1:
								teamid = int(str(teamid)+str(button.name))
								print("teamid:", teamid)
							timesPressed += 1
					if button.name == "clear":
						if inPreMainLoop == 2:
							matchid = 0
							print("matchid:", matchid)
						if inPreMainLoop == 1:
							teamid = 0
							print("teamid:", teamid)
						timesPressed = 0
			
					elif button.name == "acc":
						inPreMainLoop -= 1
						timesPressed = 0
						teamIdLabelText.color = HEX_BLUE
						timesPressedMax = 5
						print("matchid:", matchid)
						print("Ack")
						
					k_update_display()
					gc.collect()
					print("RAM: ", gc.mem_free())
					#print("Allocated RAM: ", gc.mem_alloc())
					gc.collect()
					break
		time.sleep(delay)
	#time.sleep(1)
	inAutoLoop = True
	board.DISPLAY.show(autoGroup)
	update_display(1)
	gc.collect()
	print("Starting Auto Loop")
	#time.sleep(1)
	while inAutoLoop:
		touch = ts.touch_point
		if touch:
			for button in buttonsAuto:
				if button.contains(touch):
					print("Touched", button.name)
					lastPressed = button.name
					
					if button.name == "nextpage":
						inAutoLoop = False
						print("Broke autoLoop")
						
					else:
						handleButton(button)
						
					update_display(1)
					gc.collect()
					break
		time.sleep(delay)
	print("Starting Tele Loop")
	inTeleLoop = True
	board.DISPLAY.show(teleGroup)
	update_display(2)
	while inTeleLoop:
		touch = ts.touch_point
		if touch:
			#print("touched screen")
			for button in buttonsTele:
				if button.contains(touch):
					print("Touched", button.name)
					lastPressed = button.name
					
					if button.name == "write":
						#matrix_write()
						#sd_write()
						write_data()
						inTeleLoop = False
						bypassKeyboard = False
						print("Data written")
					
					elif button.name == "back":
						inAutoLoop = True
						inTeleLoop = False
						bypassKeyboard = True
						print("Returning to autoLoop")
						
					else:
						handleButton(button)
						
						
					update_display(2)
					gc.collect()
					break
		time.sleep(delay)
		
	if bypassKeyboard == False:
		matchid += 1
		teamid = 0
		maindict = {
			"rePosBase"	: False,
			"delivSkySt": 0,
			"delivRegSt": 0,
			"placeSt_A"	: 0,
			"parkOnTape": False,
			"delivTele"	: 0,
			"placeSt"	: 0,
			"towerLevel": 0,
			"capTower"	: False,
			"capLevel"	: 0,
			"removeBase": False,
			"parkInSite": False
		}
	gc.collect()
