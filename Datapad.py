#Created by Jackson Holbrook for Whitefield Robotics, FTC team 11127
#Match data input has been commented out or changed by other notation, as its not actually necessary, or used at all.

import time
import board
import displayio
from adafruit_pyportal import PyPortal
from adafruit_button import Button
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from terminalio import FONT
import adafruit_sdcard
import os
import digitalio
import busio
import storage
import adafruit_touchscreen

cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)

# Fonts within /fonts folder
medium_font = cwd+"/fonts/Arial-16.bdf"
header_font = cwd+"/fonts/Collegiate-24.bdf"
other_font = cwd+"/fonts/Arial-ItalicMT-17.bdf"
nunito_font = cwd+"/fonts/Nunito-Black-17.bdf"
arial12 = cwd+"/fonts/Arial-12.bdf"

print('loading fonts...')
arial_16 = bitmap_font.load_font(medium_font)
h_font = bitmap_font.load_font(header_font)
arial_o = bitmap_font.load_font(other_font)
nunito = bitmap_font.load_font(nunito_font)
arial_12 = bitmap_font.load_font(arial12)

dispelements = []
dispbuttons = []

superdict = {}

matchid = 0
teamid = 0
#/////////////Make Sure these are correct at the beginning of season////////////////////////
numStats = 11
columnHeaders = "TEAM_NUM,MATCH,rePosBase,delivSkySt,delivRegSt,placeSt_A,parkOnTape,delivTele,placeSt,towerLevel,capTower,removeBase,parkInSite"

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
Level Bonus 								= n/a, should be calculated in Juypter
Moving Foundation from Building Site 		= removeBase
Parking in Building Site					= parkInSite

'''
#//////////////////////////////////////////////////////////////////////////////////////////


HEX_WHITE = 0xFFFFFF
HEX_BLUE = 0x0000FF
RED = (255, 0, 0)
ORANGE = (255, 34, 0)
YELLOW = (255, 170, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
VIOLET = (153, 0, 255)
MAGENTA = (255, 0, 51)
PINK = (255, 51, 119)
AQUA = (85, 125, 255)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
OFF = (0, 0, 0)
BLACK = 0x0

# Set the background color
BACKGROUND_COLOR = 0x000000

print("Loading...")
loadingscreen = Label(nunito, text="Loading, please wait...", color=HEX_WHITE, x=10, y=120)
lSVersionInfo = Label(arial_12, text="FTC-Skysotne Season", color=HEX_WHITE, x=10, y=150)
lSCredits = Label(arial_12, text="Created By Jackson Holbrook", color=HEX_WHITE, x=10, y=180)
loadingScreenGroup = displayio.Group(max_size=4)
loadingScreenGroup.append(loadingscreen)
loadingScreenGroup.append(lSVersionInfo)
loadingScreenGroup.append(lSCredits)
board.DISPLAY.show(loadingScreenGroup)


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


""" INITing main disp elements """

spots = [
	{'id': "write",			'Type': 'eject',	 'pos': (10, 200), 'size': (45, 45), 'color': VIOLET, 'label': "W"},
	{'id': "nextpage",		'Type': 'select',	 'pos': (65, 200), 'size': (45, 45), 'color': VIOLET, 'label': "N"},
	
	{'id': "rePosBase",		'Type': 'boolean',	 'pos': (260, 60), 'size': (60, 60), 'color': GRAY, 'label': "False"}, 
	
    {'id': "delivSkySt+",	'Type': 'int',		 'pos': (200, 60), 'size': (60, 60), 'color': BLUE, 'label': "+1"},
    {'id': "delivSkySt-",	'Type': 'int',		 'pos': (200, 60), 'size': (60, 60), 'color': RED, 'label': "-1"},
    
    {'id': "delivRegSt+",	'Type': 'int',		 'pos': (95, 10), 'size': (70, 50), 'color': BLUE, 'label': "False"},
    {'id': "delivRegSt-",	'Type': 'int',		 'pos': (95, 10), 'size': (70, 50), 'color': RED, 'label': "False"},
    
    {'id': "placeSt_A+",	'Type': 'int',		 'pos': (95, 80), 'size': (70, 50), 'color': BLUE, 'label': "False"},
    {'id': "placeSt_A-",	'Type': 'int',		 'pos': (95, 80), 'size': (70, 50), 'color': RED, 'label': "False"},
    
    {'id': "parkOnTape",	'Type': 'boolean',	 'pos': (260, 170), 'size': (60, 60), 'color': BLUE, 'label': "False"},
    
    {'id': "delivTele+",	'Type': 'int',		 'pos': (200, 170), 'size': (60, 60), 'color': BLUE, 'label': "+1"},
    {'id': "delivTele-",	'Type': 'int',		 'pos': (200, 170), 'size': (60, 60), 'color': RED, 'label': "-1"},
    
    {'id': "placeSt+",		'Type': 'int',		 'pos': (200, 170), 'size': (60, 60), 'color': BLUE, 'label': "+1"},
    {'id': "placeSt-",		'Type': 'int',		 'pos': (200, 170), 'size': (60, 60), 'color': RED, 'label': "-1"},
    
    {'id': "towerLevel+",	'Type': 'int',		 'pos': (200, 170), 'size': (60, 60), 'color': BLUE, 'label': "+1"},
    {'id': "towerLevel-",	'Type': 'int',		 'pos': (200, 170), 'size': (60, 60), 'color': RED, 'label': "-1"},
    
    {'id': "capTower",		'Type': 'boolean',	 'pos': (200, 170), 'size': (60, 60), 'color': GRAY, 'label': "False"},
    
    {'id': "removeBase",	'Type': 'boolean',	 'pos': (200, 170), 'size': (60, 60), 'color': GRAY, 'label': "False"},
    
    {'id': "parkInSite",	'Type': 'boolean',	 'pos': (200, 170), 'size': (60, 60), 'color': GRAY, 'label': "False"},
    ]

page1 = ["rePosBase", "delivSkySt+", "delivSkySt-", "delivRegSt+", "delivRegSt-", "placeSt_A", "parkOnTape"]
page2 = ["delivTele", "placeSt", "towerLevel", "capTower", "removeBase", "parkInSite"]

buttonsgroup = displayio.Group(max_size=25)

buttons = []
for spot in spots:
    button = Button(x=spot['pos'][0], y=spot['pos'][1],
                    width=spot['size'][0], height=spot['size'][1],
                    style=Button.SHADOWROUNDRECT,
                    fill_color=spot['color'], outline_color=0x222222,
                    name=spot['id'],label=spot['label'], label_font=arial_16)
    buttons.append(button)
    buttonsgroup.append(button.group)


dispgroup = displayio.Group(max_size=25)


pCtDepotDisp = Label(arial_16, text="000", color=HEX_WHITE, x=255, y=40)
dispelements.append(pCtDepotDisp)

pCtDepotLabel = Label(arial_12, text="mineralsInDepot", color=HEX_WHITE, x=205, y=20)
dispelements.append(pCtDepotLabel)


pCtLanderDisp = Label(arial_16, text="000", color=HEX_WHITE, x=255, y=160)
dispelements.append(pCtLanderDisp)

pCtLanderLabel = Label(arial_12, text="mineralsInLander", color=HEX_WHITE, x=205, y=130)
dispelements.append(pCtLanderLabel)


dl_drop = Label(arial_12, text="Drop?", color=HEX_WHITE, x=10, y=35)
dispelements.append(dl_drop)

dl_sample = Label(arial_12, text="Sample?", color=HEX_WHITE, x=10, y=95)
dispelements.append(dl_sample)

for thing in dispelements:
	dispgroup.append(thing)

maingroup = displayio.Group(max_size=5) # if getting weird errors, increase max size
maingroup.append(buttonsgroup)
maingroup.append(dispgroup)





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
    """Update the display with current info."""
    #matchIdLabel.text = "{00}".format(matchid)  #uncomment for matchid
    teamIdLabel.text = "{00000}".format(teamid)    
    board.DISPLAY.refresh_soon()

def changeLabelColor():
	if inPreMainLoop == 2:
		#matchIdLabelText.color = HEX_BLUE  #uncomment for matchid
		teamIdLabelText.color = HEX_WHITE
		timesPressedMax = 2
	elif inPreMainLoop == 1:
		#matchIdLabelText.color = HEX_WHITE  #uncomment for matchid
		teamIdLabelText.color = HEX_BLUE
		timesPressedMax = 5

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
	"removeBase": False,
	"parkInSite": False
}
maindictorder = ["TEAM_NUM", "MATCH", "rePosBase", "delivSkySt", "delivRegSt", "placeSt_A", "parkOnTape", "delivTele", "placeSt", "towerLevel", "capTower", "removeBase", "parkInSite"]




def update_display():
    """Update the display with current info."""
    if lastPressed == "1" or "2": pCtDepotDisp.text = "{000}".format(maindict["pCtDepot"])  
    if lastPressed == "5" or "6": pCtLanderDisp.text = "{000}".format(maindict["pCtLander"])
    
    if lastPressed == "3":  #this part looks wrongly indented in coda 2, but its right, dont touch it 
    	tf1 = buttons[3]
    	if maindict["toggleDrop"] == True: 
		tf1.label = "True"
	else: #indentation visual glitch
		tf1.label = "False"
    
    if lastPressed == "4":
	    tf2 = buttons[4]
	    if maindict["toggleSample"] == True:
	    	tf2.label = "True"
	    else:
	    	tf2.label = "False"

    board.DISPLAY.refresh_soon()

def display_update_all():
	pCtDepotDisp.text = "{000}".format(maindict["pCtDepot"]) 
	pCtLanderDisp.text = "{000}".format(maindict["pCtLander"])

	tf1 = buttons[3]
	if maindict["toggleDrop"] == True: 
		tf1.label = "True"
	else:
		tf1.label = "False"
	
	tf2 = buttons[4]
	if maindict["toggleSample"] == True:
		tf2.label = "True"
	else:
		tf2.label = "False"
	board.DISPLAY.refresh_soon()
		
def old_sd_write():  #uses maindict (dict) and maindictorder (array). the array provides order for the dictionary.
	print("Writing the matrix...")
	f = open('/sd/TESTfile.txt', 'a')
	f.write('\n\n')
	f.write("Match ID: ")
	f.write(str(matchid))
	f.write("\nTeam ID: ")
	f.write(str(teamid))
	f.write("\n")
	for v in maindictorder:
		if maindict.get(v) == False:
			f.write("0")
		elif maindict.get(v) == True:
			f.write("1")
		else:
			f.write(str(maindict.get(v)))
		f.write("\n")
		print(maindict.get(v))
	f.close()
	print("Writing Complete")

def sd_write_():
	print("Writing to sd card...")
	superorder = []
	quantiKey = []

	for l in superdict:
		superorder.append(l)
		print(superorder)
	
	f = open('/sd/data.txt', 'w')
	for m in superorder:
		quantiKey.append(len(superdict[m]))
		for x in range(len(superdict[m])):
				for y in range(numStats):
					f.write(superdict[m][x][y])
					print(superdict[m][x][y])
	
	f.close()
	print("Main Data Complete")
	
	f = open('/sd/dataTeamKey.txt', 'w')
	for z in superorder:	
		f.write(str(z))
		print("superorder: ", superorder)
	f.close()
	print("Team Data Complete")
	
	f = open('/sd/dataQuantiKey.txt', 'w')
	for z in quantiKey:	
		f.write(str(z))
		print("quantiKey: ", quantiKey)
	f.close()
	print("Match Quantity Data Complete")
	print("Writing Complete")


def sd_write():
	print("Writing to sd card...")
	superorder = []
	matchNum = 1
	
	for l in superdict:
		superorder.append(l)
		print(superorder)
	
	f = open('/sd/data.txt', 'a')
	f.write(columnHeaders)
	f.write("\n")
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
				print(str(superdict[m][x][y]))
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


def increment(value, condition, changeValue, direction, amount):
	#if value (button.name) == condition (the name of the value) then change the changeValue (maindict["str"]) in the direction by amount
	if value == condition:
		changeValue += amount
		print(changeValue)
	

print("Beginning Superloop")
while True:

	timesPressed = 0
	timesPressedMax = 5 #change to "2" for matchid
	inPreMainLoop = 1 #change to "2" for matchid
	board.DISPLAY.show(preMainGroup)
	k_update_display()
	print("Starting preMain Loop")
	changeLabelColor()
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
						changeLabelColor()
						timesPressedMax = 5
						print("matchid:", matchid)
						print("Ack")
		
					k_update_display()
					break
		time.sleep(0.05)

	inMainLoop = True
	board.DISPLAY.show(maingroup)
	display_update_all()
	print("Starting Main Loop")  
	while inMainLoop:
		touch = ts.touch_point
		if touch:
			for button in buttons:
				if button.contains(touch):
					print("Touched", button.name)
					lastPressed = button.name
					if button.name == "write":   
						matrix_write()
						sd_write()
						inMainLoop = False
			'''
					if button.name == "1":
						maindict["pCtDepot"] = maindict["pCtDepot"] + 1
						print(maindict["pCtDepot"])
					
					elif button.name == "2":
						maindict["pCtDepot"] = maindict["pCtDepot"] - 1
						print(maindict["pCtDepot"])
					
					elif button.name == "5":
						maindict["pCtLander"] = maindict["pCtLander"] + 1
						print(maindict["pCtLander"])
					
					elif button.name == "6":
						maindict["pCtLander"] = maindict["pCtLander"] - 1
						print(maindict["pCtLander"])
					
					
					elif button.name == "3":
						if maindict["toggleDrop"] == False:
							maindict["toggleDrop"] = True
						else:
							maindict["toggleDrop"] = False
						print(maindict["toggleDrop"]) 
					
					elif button.name == "4":
						if maindict["toggleSample"] == False:
							maindict["toggleSample"] = True
						else:
							maindict["toggleSample"] = False
						print(maindict["toggleSample"]) 
						'''
					
					update_display()
					break
		time.sleep(0.05)
	
	matchid += 1
	teamid = 0
	maindict = {
		"pCtDepot": 0,
		"pCtLander": 0,
		"toggleDrop": False,
		"toggleSample": False
	}
