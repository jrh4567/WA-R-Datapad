


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


def update_display(): #with ifs
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
		



dispgroup1.append(Label(nunito, text="Autonomous Scoring", color=HEX_WHITE, x=15, y=25)) #correct

dispgroup1.append(Label(arial_12, text="Moved Base?", color=HEX_WHITE, x=10, y=75)) #correct

dispgroup1.append(Label(arial_12, text="parkOnTape?", color=HEX_WHITE, x=10, y=133)) #correct

dispgroup1.append(Label(arial_12, text="Skystones Delived", color=HEX_WHITE, x=205, y=10)) #correct
delivSkyStLabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=27) #correct
dispgroup1.append(delivSkyStLabel)

dispgroup1.append(Label(arial_12, text="Reg Stones Delived", color=HEX_WHITE, x=205, y=85)) #correct
delivRegStLabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=102) #correct
dispgroup1.append(delivRegStLabel) 

dispgroup1.append(Label(arial_12, text="Stones Placed", color=HEX_WHITE, x=205, y=160)) #correct
placeSt_ALabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=177) #correct
dispgroup1.append(placeSt_ALabel)

print("RAM (post-dispgroup1): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())

dispgroup2 = displayio.Group(max_size=10)

dispgroup2.append(Label(nunito, text="TeleOp Scoring", color=HEX_WHITE, x=15, y=25)) #correct

dispgroup2.append(Label(arial_12, text="Capped Tower?", color=HEX_WHITE, x=10, y=60)) #correct

dispgroup2.append(Label(arial_12, text="Remove Base?", color=HEX_WHITE, x=10, y=110)) #correct

dispgroup2.append(Label(arial_12, text="Triangle Park?", color=HEX_WHITE, x=10, y=160)) #correct

dispgroup2.append(Label(arial_12, text="Stones Delived", color=HEX_WHITE, x=205, y=10)) #correct
delivTeleLabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=27) #correct
dispgroup2.append(delivTeleLabel)

dispgroup2.append(Label(arial_12, text="Stones Placed", color=HEX_WHITE, x=205, y=85)) #correct
placeStLabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=102) #correct
dispgroup2.append(placeStLabel) 

dispgroup2.append(Label(arial_12, text="Tower Level", color=HEX_WHITE, x=205, y=160)) #correct
towerLevelLabel = Label(arial_16, text="00", color=HEX_WHITE, x=255, y=177) #correct
dispgroup2.append(towerLevelLabel)

print("RAM (post-dispgroup2): ", gc.mem_free())
print("Allocated RAM: ", gc.mem_alloc())
