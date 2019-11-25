


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
		
