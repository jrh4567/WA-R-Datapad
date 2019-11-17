"""
CircuitPython library to handle the input and calculations

* Author(s): Melissa LeBlanc-Williams
"""


class datapadHelper():

	def __init__(self, num):
		self.numVars = num

	def ext_print_test(self):
		print("External Methods Online")


	def ex_display_update_all():
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
		
