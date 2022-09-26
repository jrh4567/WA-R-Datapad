#Created by Jackson Holbrook for Whitefield Robotics, FTC team 11127
import time
import board
import displayio
from adafruit_pyportal import PyPortal
from adafruit_button import Button
from adafruit_display_text.label import Label
# from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font
from terminalio import FONT
import adafruit_sdcard
# import os
import digitalio
import busio
import storage
import adafruit_touchscreen
import gc

gc.enable()
print("Total Free RAM: ", gc.mem_free())
print("Total Allocated RAM: ", gc.mem_alloc())
cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)

# Fonts within /fonts folder
# medium_font = cwd+"/fonts/Arial-16.bdf"
# header_font = cwd+"/fonts/Collegiate-24.bdf"
# #other_font = cwd+"/fonts/Arial-ItalicMT-17.bdf"
# nunito_font = cwd+"/fonts/Nunito-Black-17.bdf"
# arial12 = cwd+"/fonts/Arial-12.bdf"

print('loading fonts...')
# arial_16 = bitmap_font.load_font(cwd+"/fonts/Arial-16.bdf")
# h_font = bitmap_font.load_font(cwd+"/fonts/Collegiate-24.bdf")
#arial_o = bitmap_font.load_font(other_font)
nunito = bitmap_font.load_font(cwd+"/fonts/Nunito-Black-17.bdf")
arial_12 = bitmap_font.load_font(cwd+"/fonts/Arial-12.bdf")
defFont = FONT

print("RAM (post-fonts load): ", gc.mem_free())

HEX_WHITE = 0xFFFFFF
HEX_BLUE = 0x0000FF
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
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
    board.DISPLAY.refresh()
gc.collect()
print("RAM (after wolf load): ", gc.mem_free())

#loadingScreenGroup.append(Label(arial_12, text="FTC-Skysotne \nSeason", color=HEX_WHITE, x=220, y=125))
loadingScreenGroup.append(Label(arial_12, text="Created By WA-R", color=HEX_WHITE, x=10, y=232))

dispelements = []
dispbuttons = []

superdict = {}

matchid = 0
teamid = 0

delay = 0.25
#/////////////Make Sure these are correct at the beginning of season////////////////////////
columnHeaders = "autoDuck,parkSquare,parkWarehouse,complParked,correctLevel,usedTSE,autoSq,autoShipHub,shipSq,shipLvl1,shipLvl2,shipLvl3,shipShared,duckCt,hubBalanced,sharedTipped,endPark,compEndPark,hubCapped"
autoTeleSplit = 8 #index of the FIRST TELEOP ITEM
''' 
Delivering duck in auto - autoDuck
Parked in Alliance Storage Unit - parkSquare
Parked in Warehouse - parkWarehouse
Completely parked (*2 multiplier) - complParked
Placed block on correct level - correctLevel
used Team Scoring Element - usedTSE
Freight in Square - autoSq
Freight on Hub (any position) - autoShipHub

Freight in Square - shipSq
Freight on hub:
	level 1 (lowest) - shipLvl1
	level 2 (mid) - shipLvl2
	level 3 (top) - shipLvl3
Freight on Shared Hub - shipShared
Ducks delivered: duckCt
Alliance Hub Balanced - hubBalanced
Shared Hub tipped - sharedTipped
Parked in warehouse - endPark
Completely Parked in Warehouse - compEndPark
Alliance Hub Capped - hubCapped


'''
#//////////////////////////////////////////////////////////////////////////////////////////

statList = []
for stat in columnHeaders.split(","):
	statList.append(stat)
numStats = len(statList)

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
# print("SD Card Directories: ")
# print(os.listdir('/sd'))

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
for spot in keypadSpots: #create displayio buttons with the keypadSpots matrix, then add them to an array
    button = Button(x=spot['pos'][0], y=spot['pos'][1],
                    width=spot['size'][0], height=spot['size'][1],
                    style=Button.RECT,
                    fill_color=spot['color'], outline_color=0x222222,
                    name=spot['id'],label=spot['label'], label_font=arial_12)
    kbuttons.append(button)
    keypadGroup.append(button.group)
#     print("Adding {} to kButtons".format(spot))
del keypadSpots
gc.collect()

preMainGroup = displayio.Group(max_size=5)
preMainGroup.append(keypadGroup)

#matchIdLabelText = Label(arial_12, text="Match ID:", color=HEX_WHITE, x=10, y=30)  #uncomment for matchid
#preMainGroup.append(matchIdLabelText)  #uncomment for matchid

#matchIdLabel = Label(arial_12, text="00", color=HEX_WHITE, x=110, y=30) #uncomment for matchid
#preMainGroup.append(matchIdLabel)  #uncomment for matchid

teamIdLabelText = Label(defFont, text="Team ID:", color=HEX_WHITE, x=100, y=30, scale=2)
preMainGroup.append(teamIdLabelText)

teamIdLabel = Label(defFont, text="00000", color=HEX_WHITE, x=200, y=30, scale=2)
preMainGroup.append(teamIdLabel)



def k_update_display():
    gc.collect()
    """Update the display with current info."""
    #matchIdLabel.text = "{00}".format(matchid)  #uncomment for matchid
    teamIdLabel.text = "{00000}".format(teamid)    
    board.DISPLAY.refresh()
    time.sleep(delay)
    gc.collect()

print("RAM (after keypad init, pre-spots): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())

""" INITing main disp elements """
#rePosBase: 95, 50
#nextpage: 10, 200

tfColumnOffset = 35
intColumnOffset = 35
leftColx = 50
leftColy = 25
rightColx = 130 #200
rightColy = 5 #10
bp = { #bp = buttonPos
	"nextPage": (225, 190),
	"autoDuck": (leftColx, leftColy + 0*tfColumnOffset),
	"parkSquare": (leftColx, leftColy + 1*tfColumnOffset),
	"parkWarehouse": (leftColx, leftColy + 2*tfColumnOffset),
	"complParked": (leftColx, leftColy + 3*tfColumnOffset),
	"correctLevel": (leftColx, leftColy + 4*tfColumnOffset),
	"usedTSE": (leftColx, leftColy + 5*tfColumnOffset),
	
	"autoSq": (rightColx, 10), #leftColy + 1*45), #For the integer buttons, this coord is the top-left of the label, and everything else is based on this
	"autoShipHub": (rightColx, 10 + 50),
	
	
	"hubBalanced": (leftColx, leftColy + 0*tfColumnOffset),
	"sharedTipped": (leftColx, leftColy + 1*tfColumnOffset),
	"endPark": (leftColx, leftColy + 2*tfColumnOffset),
	"compEndPark": (leftColx, leftColy + 3*tfColumnOffset),
	"hubCapped": (leftColx, leftColy + 4*tfColumnOffset),
	
	"duckCt": (rightColx, rightColy + 0*intColumnOffset),
	"shipLvl3": (rightColx, rightColy + 1*intColumnOffset),
	"shipLvl2": (rightColx, rightColy + 2*intColumnOffset),
	"shipLvl1": (rightColx, rightColy + 3*intColumnOffset),
	"shipShared": (rightColx, rightColy + 4*intColumnOffset),
	"shipSq": (rightColx, rightColy + 5*intColumnOffset),
}
del tfColumnOffset, intColumnOffset, leftColx, leftColy, rightColx, rightColy
gc.collect()

tfButtonSize = (60, 30)

intButtonOffset = 0 #10
intButtonXOffset = 61
intBothXOffset = 65
spots = [ # An Array of Dictionaries. I recommend using find+replace to change all the strings to their new values, especially for the int buttons. 
	#PAGE 1 - AUTONOMOUS
	{'id': "nextpage",		'pos': bp["nextPage"], 'size': (70, 45), 'color': GREEN, 'label': "Next"}, 
	
	{'id': "autoDuck",	 	'pos': bp["autoDuck"], 'size': tfButtonSize, 'color': GRAY, 'label': "False"}, 
	
	{'id': "parkSquare", 	'pos': bp["parkSquare"], 'size': tfButtonSize, 'color': GRAY, 'label': "False"},
	
	{'id': "parkWarehouse", 'pos': bp["parkWarehouse"], 'size': tfButtonSize, 'color': GRAY, 'label': "False"},
	
	{'id': "complParked", 	'pos': bp["complParked"], 'size': tfButtonSize, 'color': GRAY, 'label': "False"},
	
	{'id': "correctLevel", 	'pos': bp["correctLevel"], 'size': tfButtonSize, 'color': GRAY, 'label': "False"},
	
	{'id': "usedTSE",	 	'pos': bp["usedTSE"], 'size': tfButtonSize, 'color': GRAY, 'label': "False"},
	
	
	{'id': "autoSq+",	'pos': (bp["autoSq"][0] + intBothXOffset + intButtonXOffset, bp["autoSq"][1] + intButtonOffset), 'size': (60, 30), 'color': BLUE, 'label': "+1"}, 
	{'id': "autoSq-",	'pos': (bp["autoSq"][0] + intBothXOffset, bp["autoSq"][1] + intButtonOffset), 'size': (60, 30), 'color': RED, 'label': "-1"}, 
	
	{'id': "autoShipHub+",	'pos': (bp["autoShipHub"][0] + intBothXOffset + intButtonXOffset, bp["autoShipHub"][1] + intButtonOffset), 'size': (60, 30), 'color': BLUE, 'label': "+1"}, 
	{'id': "autoShipHub-",	'pos': (bp["autoShipHub"][0] + intBothXOffset, bp["autoShipHub"][1] + intButtonOffset), 'size': (60, 30), 'color': RED, 'label': "-1"}, 
	
	#PAGE 2 - TELEOP
	{'id': "back",			'pos': (10, 200), 'size': (70, 40), 'color': RED, 'label': "Back"}, 
	{'id': "write",		 	'pos': (85, 200), 'size': (70, 45), 'color': GREEN, 'label': "Write"}, 
	
	{'id': "hubBalanced",	'pos': bp["hubBalanced"], 'size': tfButtonSize, 'color': GRAY, 'label': "False"}, 
	
	{'id': "sharedTipped", 	'pos': bp["sharedTipped"], 'size': tfButtonSize, 'color': GRAY, 'label': "False"},
	
	{'id': "endPark", 		'pos': bp["endPark"], 'size': tfButtonSize, 'color': GRAY, 'label': "False"},
	
	{'id': "compEndPark", 	'pos': bp["compEndPark"], 'size': tfButtonSize, 'color': GRAY, 'label': "False"},
	
	{'id': "hubCapped", 	'pos': bp["hubCapped"], 'size': tfButtonSize, 'color': GRAY, 'label': "False"},
	
	{'id': "duckCt+",	'pos': (bp["duckCt"][0] + intBothXOffset + intButtonXOffset, bp["duckCt"][1] + intButtonOffset), 'size': (60, 30), 'color': BLUE, 'label': "+1"}, 
	{'id': "duckCt-",	'pos': (bp["duckCt"][0] + intBothXOffset, bp["duckCt"][1] + intButtonOffset), 'size': (60, 30), 'color': RED, 'label': "-1"},
	
	{'id': "shipLvl3+",	'pos': (bp["shipLvl3"][0] + intBothXOffset + intButtonXOffset, bp["shipLvl3"][1] + intButtonOffset), 'size': (60, 30), 'color': BLUE, 'label': "+1"}, 
	{'id': "shipLvl3-",	'pos': (bp["shipLvl3"][0] + intBothXOffset, bp["shipLvl3"][1] + intButtonOffset), 'size': (60, 30), 'color': RED, 'label': "-1"}, 
	
	{'id': "shipLvl2+",	'pos': (bp["shipLvl2"][0] + intBothXOffset + intButtonXOffset, bp["shipLvl2"][1] + intButtonOffset), 'size': (60, 30), 'color': BLUE, 'label': "+1"}, 
	{'id': "shipLvl2-",	'pos': (bp["shipLvl2"][0] + intBothXOffset, bp["shipLvl2"][1] + intButtonOffset), 'size': (60, 30), 'color': RED, 'label': "-1"}, 
	
	{'id': "shipLvl1+",	'pos': (bp["shipLvl1"][0] + intBothXOffset + intButtonXOffset, bp["shipLvl1"][1] + intButtonOffset), 'size': (60, 30), 'color': BLUE, 'label': "+1"}, 
	{'id': "shipLvl1-",	'pos': (bp["shipLvl1"][0] + intBothXOffset, bp["shipLvl1"][1] + intButtonOffset), 'size': (60, 30), 'color': RED, 'label': "-1"},
	
	{'id': "shipShared+",	'pos': (bp["shipShared"][0] + intBothXOffset + intButtonXOffset, bp["shipShared"][1] + intButtonOffset), 'size': (60, 30), 'color': BLUE, 'label': "+1"}, 
	{'id': "shipShared-",	'pos': (bp["shipShared"][0] + intBothXOffset, bp["shipShared"][1] + intButtonOffset), 'size': (60, 30), 'color': RED, 'label': "-1"},
	
	{'id': "shipSq+",	'pos': (bp["shipSq"][0] + intBothXOffset + intButtonXOffset, bp["shipSq"][1] + intButtonOffset), 'size': (60, 30), 'color': BLUE, 'label': "+1"}, 
	{'id': "shipSq-",	'pos': (bp["shipSq"][0] + intBothXOffset, bp["shipSq"][1] + intButtonOffset), 'size': (60, 30), 'color': RED, 'label': "-1"}, 
	]

print("RAM (post-spots): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())

# I really don't feel like taking the time to actually copy/paste all of those
page1 = ["nextpage"] #, "rePosBase", "delivSkySt+", "delivSkySt-", "delivRegSt+", "delivRegSt-", "placeSt_A+", "placeSt_A-", "parkOnTape"]
page2 = ["back", "write"] #, "delivTele+", "delivTele-", "placeSt+", "placeSt-", "towerLevel+", "towerLevel-", "capLevel+", "capLevel-", "capTower", "removeBase", "parkInSite"]

buttonsgroup1 = displayio.Group(max_size=30) #(max_size=len(page1)) 
buttonsgroup2 = displayio.Group(max_size=30) #(max_size=len(page2) + 1)

buttonsAuto = []
buttonsTele = []
for spot in spots:
    button = Button(x=spot['pos'][0], y=spot['pos'][1],
                    width=spot['size'][0], height=spot['size'][1],
                    style=Button.RECT,
                    fill_color=spot['color'], outline_color=0x222222,
                    name=spot['id'],label=spot['label'], label_font=arial_12)
    #buttons.append(button)
    if (spot['id'] in page1) or (spot['id'] in statList[0:autoTeleSplit]) or (spot['id'][0:len(spot['id'])-1] in statList[0:autoTeleSplit]):
        buttonsAuto.append(button)
        buttonsgroup1.append(button.group)
#         print("Adding {} to pg1".format(spot))
    else:
        buttonsTele.append(button)
        buttonsgroup2.append(button.group)
#         print("Adding {} to pg2".format(spot))

del spots, page1, page2, intButtonOffset, intButtonXOffset
gc.collect()

print("RAM (post-spots loop): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())

dispgroup1 = displayio.Group(max_size=15)

labelOffset = 15
intNumOffset = 50
intLabelOffset = 7
# T/F Labels
dispgroup1.append(Label(nunito, text="AutoScore", color=HEX_WHITE, x=10, y=10)) #Title

dispgroup1.append(Label(arial_12, text="Duck", color=HEX_WHITE, x=10, y=bp["autoDuck"][1] + labelOffset))

dispgroup1.append(Label(arial_12, text="Park\nSQ", color=HEX_WHITE, x=10, y=bp["parkSquare"][1] + labelOffset))

dispgroup1.append(Label(arial_12, text="Park\nWHSE", color=HEX_WHITE, x=10, y=bp["parkWarehouse"][1] + labelOffset))

dispgroup1.append(Label(arial_12, text="Park\nCompl", color=HEX_WHITE, x=10, y=bp["complParked"][1] + labelOffset))

dispgroup1.append(Label(arial_12, text="correct\nLevel", color=HEX_WHITE, x=10, y=bp["correctLevel"][1] + labelOffset))

dispgroup1.append(Label(arial_12, text="used\nTSE", color=HEX_WHITE, x=10, y=bp["usedTSE"][1] + labelOffset))

# INT Labels
dispgroup1.append(Label(arial_12, text="shipSQ", color=HEX_WHITE, x=bp["autoSq"][0], y=bp["autoSq"][1] + intLabelOffset)) 
autoSqLabel = Label(arial_12, text="00", color=HEX_WHITE, x=bp["autoSq"][0] + intNumOffset, y=bp["autoSq"][1] + intLabelOffset) #These var names must be `[the stat name]Label`
dispgroup1.append(autoSqLabel) #make sure this matches the line above

dispgroup1.append(Label(arial_12, text="shipHub", color=HEX_WHITE, x=bp["autoShipHub"][0], y=bp["autoShipHub"][1] + intLabelOffset)) 
autoShipHubLabel = Label(arial_12, text="00", color=HEX_WHITE, x=bp["autoShipHub"][0] + intNumOffset, y=bp["autoShipHub"][1] + intLabelOffset) 
dispgroup1.append(autoShipHubLabel) 

# dispgroup1.append(Label(arial_12, text="StPlaced", color=HEX_WHITE, x=205, y=160)) 
# placeSt_ALabel = Label(arial_12, text="00", color=HEX_WHITE, x=255, y=177) 
# dispgroup1.append(placeSt_ALabel)

print("RAM (post-dispgroup1): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())

dispgroup2 = displayio.Group(max_size=20)

# T/F Labels
dispgroup2.append(Label(nunito, text="TeleScore", color=HEX_WHITE, x=10, y=10)) 

dispgroup2.append(Label(arial_12, text="Hub\nBal.", color=HEX_WHITE, x=10, y=bp["hubBalanced"][1] + labelOffset))

dispgroup2.append(Label(arial_12, text="shared\ntipped", color=HEX_WHITE, x=10, y=bp["sharedTipped"][1] + labelOffset))

dispgroup2.append(Label(arial_12, text="Park\nWHSE", color=HEX_WHITE, x=10, y=bp["endPark"][1] + labelOffset))

dispgroup2.append(Label(arial_12, text="Park\ncompl.", color=HEX_WHITE, x=10, y=bp["compEndPark"][1] + labelOffset))

dispgroup2.append(Label(arial_12, text="hub\ncap", color=HEX_WHITE, x=10, y=bp["hubCapped"][1] + labelOffset))

# INT Labels
dispgroup2.append(Label(arial_12, text="ducks", color=HEX_WHITE, x=bp["duckCt"][0], y=bp["duckCt"][1] + intLabelOffset)) 
duckCtLabel = Label(arial_12, text="00", color=HEX_WHITE, x=bp["duckCt"][0] + intNumOffset, y=bp["duckCt"][1] + intLabelOffset) 
dispgroup2.append(duckCtLabel)

dispgroup2.append(Label(arial_12, text="lvl3", color=HEX_WHITE, x=bp["shipLvl3"][0], y=bp["shipLvl3"][1] + intLabelOffset)) 
shipLvl3Label = Label(arial_12, text="00", color=HEX_WHITE, x=bp["shipLvl3"][0] + intNumOffset, y=bp["shipLvl3"][1] + intLabelOffset) 
dispgroup2.append(shipLvl3Label)

dispgroup2.append(Label(arial_12, text="lvl2", color=HEX_WHITE, x=bp["shipLvl2"][0], y=bp["shipLvl2"][1] + intLabelOffset)) 
shipLvl2Label = Label(arial_12, text="00", color=HEX_WHITE, x=bp["shipLvl2"][0] + intNumOffset, y=bp["shipLvl2"][1] + intLabelOffset) 
dispgroup2.append(shipLvl2Label)

dispgroup2.append(Label(arial_12, text="lvl1", color=HEX_WHITE, x=bp["shipLvl1"][0], y=bp["shipLvl1"][1] + intLabelOffset)) 
shipLvl1Label = Label(arial_12, text="00", color=HEX_WHITE, x=bp["shipLvl1"][0] + intNumOffset, y=bp["shipLvl1"][1] + intLabelOffset) 
dispgroup2.append(shipLvl1Label)

dispgroup2.append(Label(arial_12, text="shared", color=HEX_WHITE, x=bp["shipShared"][0], y=bp["shipShared"][1] + intLabelOffset)) 
shipSharedLabel = Label(arial_12, text="00", color=HEX_WHITE, x=bp["shipShared"][0] + intNumOffset, y=bp["shipShared"][1] + intLabelOffset) 
dispgroup2.append(shipSharedLabel)

dispgroup2.append(Label(arial_12, text="shipSQ", color=HEX_WHITE, x=bp["shipSq"][0], y=bp["shipSq"][1] + intLabelOffset)) 
shipSqLabel = Label(arial_12, text="00", color=HEX_WHITE, x=bp["shipSq"][0] + intNumOffset, y=bp["shipSq"][1] + intLabelOffset) 
dispgroup2.append(shipSqLabel)

print("RAM (post-dispgroup2): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())
#'''
autoGroup = displayio.Group(max_size=5)
autoGroup.append(buttonsgroup1)
autoGroup.append(dispgroup1)

teleGroup = displayio.Group(max_size=5)
teleGroup.append(buttonsgroup2)
teleGroup.append(dispgroup2)

del bp
gc.collect()

print("RAM (post-labels)", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())

maindict = {
	"autoDuck"			: False,
	"parkSquare"		: False,
	"parkWarehouse"		: False,
	"complParked"		: False,
	"correctLevel"		: False,
	"usedTSE"			: False,
	"autoSq"			: 0,
	"autoShipHub"		: 0,
	"shipSq"			: 0, #Teleop \/
	"shipLvl1"			: 0,
	"shipLvl2"			: 0,
	"shipLvl3"			: 0,
	"shipShared"		: 0,
	"duckCt"			: 0,
	"hubBalanced"		: False,
	"sharedTipped"		: False,
	"endPark"			: False,
	"compEndPark"		: False,
	"hubCapped"			: False
}
maindictorder = statList#["rePosBase", "delivSkySt", "delivRegSt", "placeSt_A", "parkOnTape", "delivTele", "placeSt", "towerLevel", "capTower", "capLevel", "removeBase", "parkInSite"]



def update_display(page):
	"""Update the display with current info."""
	# page can either be 1 or 2, signifying Auto or Tele pages
	#print("updating display")
	gc.collect()
	if page == 1:
		buttonArray = buttonsAuto
	else:
		buttonArray = buttonsTele
	
	for button in buttonArray:
		if button.name[len(button.name)-1:] in ["+", "-"]:
#			type = "int"
			dictName = button.name[:len(button.name)-1]
			exec('%s.text = "{00}".format(str(maindict["%s"]))' % ("{}Label".format(dictName), str(dictName)))
		elif button.name in ["nextpage", "back", "write"]:
#			type = "other"
			pass
		else:
#			type = "boolean"
			button.label = str(maindict[button.name])

#		if type == "int":
#			dictName = button.name[:len(button.name)-1]
#			labelName = "{}Label".format(dictName)
#			exec('%s.text = "{00}".format(str(maindict["%s"]))' % (labelName, str(dictName)))
#			  exec('%s.text = "{00}".format(str(maindict["%s"]))' % ("{}Label".format(dictName), str(dictName)))
			
# 		elif type == "boolean":
			#maindict[button.name] = not(maindict[button.name])
# 			button.label = str(maindict[button.name])
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
# 	gc.collect()
	print("RAM (update_disp): ", gc.mem_free())
	#print("Allocated RAM: ", gc.mem_alloc())
	board.DISPLAY.refresh()

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

del odb, face

gc.collect()
print("RAM (before loop main start): ", gc.mem_free())
#inPreMainLoop = 1
bypassKeyboard = False
print("Beginning Superloop")
board.DISPLAY.show(preMainGroup)
del loadingScreenGroup
del nunito
del loading
del plsWait
gc.collect()
print("RAM (after del loadingScreenGroup): ", gc.mem_free())
while True:
	
	if bypassKeyboard == False: #bypassKeyboard is True when user wants to go back to the Auto screen from the Teleop screen, False when user needs to input new team number.
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
					if timesPressed < timesPressedMax:
						if button.name in ["0","1","2","3","4","5","6","7","8","9"]:
							if inPreMainLoop == 1:
								teamid = int(str(teamid)+str(button.name))
								print("teamid:", teamid)
							timesPressed += 1
# 							time.sleep(delay)
					if button.name == "clear":
						if inPreMainLoop == 1:
							teamid = 0
							print("teamid:", teamid)
						timesPressed = 0
# 						time.sleep(delay)
			
					elif button.name == "acc":
						inPreMainLoop -= 1
						timesPressed = 0
						teamIdLabelText.color = HEX_BLUE
						timesPressedMax = 5
						print("matchid:", matchid)
						print("Ack")
# 						time.sleep(delay)
						
					k_update_display()
					gc.collect()
					print("RAM: ", gc.mem_free())
					#print("Allocated RAM: ", gc.mem_alloc())
					gc.collect()
					break
# 		time.sleep(delay)
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
		time.sleep(0.01)
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
		time.sleep(0.01)
		
	if bypassKeyboard == False:
		matchid += 1
		teamid = 0
		maindict = {
			"autoDuck"			: False,
			"parkSquare"		: False,
			"parkWarehouse"		: False,
			"complParked"		: False,
			"correctLevel"		: False,
			"usedTSE"			: False,
			"autoSq"			: 0,
			"autoShipHub"		: 0,
			"shipSq"			: 0, #Teleop \/
			"shipLvl1"			: 0,
			"shipLvl2"			: 0,
			"shipLvl3"			: 0,
			"shipShared"		: 0,
			"duckCt"			: 0,
			"hubBalanced"		: False,
			"sharedTipped"		: False,
			"endPark"			: False,
			"compEndPark"		: False,
			"hubCapped"			: False
		}
	gc.collect()
