"""
CircuitPython library to handle the input and calculations

* Author(s): Melissa LeBlanc-Williams
"""

# pylint: disable=eval-used
def calculate(number_one, operator, number_two):
    result = eval(number_one + operator + number_two)
    if int(result) == result:
        result = int(result)
    return str(result)

class datapadHelper:
    def __init__(self, calc_display, clear_button, label_offset):
        self._error = False
        self._calc_display = calc_display
        self._clear_button = clear_button
        self._label_offset = label_offset
        self._accumulator = "0"
        self._operator = None
        self._equal_pressed = False
        self._operand = None
        self._all_clear()

	def ext_print_test():
		print("External Print")

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
		
		