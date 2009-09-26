# -*- coding: iso-8859-1 -*-
from Xlib.display import Display
from Xlib import X
from Xlib.protocol import event
import Xlib.ext.xtest
from pymouse import PyMouseMeta

display = Display(":0")
root = display.screen().root
LEFT = X.Button1
RIGHT = X.Button2
MIDDLE = X.Button3

class PyMouse(PyMouseMeta):
	def press(self, x, y, button = 0):
		focus = display.get_input_focus().focus
		rel = focus.translate_coords(root, x, y)
		button_list = [LEFT, RIGHT, MIDDLE]

		try:
			mousePress = event.ButtonPress(
				time=X.CurrentTime,
				root=root,
				window=focus,
				same_screen=1,
				child=X.NONE,
				root_x=x,
				root_y=y,
				event_x=rel.x,
				event_y=rel.y,
				state=0,
				detail=button_list[button]
				)
			focus.send_event(mousePress)

        except:
			pass

		display.sync()

	def release(self, x, y, button = 0):
		focus = display.get_input_focus().focus
		rel = focus.translate_coords(root, x, y)
		button_list = [LEFT, RIGHT, MIDDLE]

		try:
			mouseRealease = event.ButtonRelease(
				time=X.CurrentTime,
				root=root,
				window=focus,
				same_screen=1,
				child=X.NONE,
				root_x=x,
				root_y=y,
				event_x=rel.x,
				event_y=rel.y,
				state=1,
				detail=button_list[button]
				)
			focus.send_event(mouseRealease)

		except:
			pass

		display.sync()

	def click(self, x, y, button = LEFT):
		try:
			self.press(x, y, button)
			self.release(x, y, button)
		except:
			# Using xlib-xtest fake input
			root.warp_pointer(x, y) # I believe you where not setting the position
			Xlib.ext.xtest.fake_input (d, X.ButtonPress, button)

		display.sync()

	def move(self, x, y):
		root.warp_pointer(x, y)
		display.sync()

	def position(self):
		coord = display.screen().root.query_pointer()._data
		return coord["root_x"], coord["root_y"]

	def screen_size(self):
		width = display.screen().width_in_pixels
		height = display.screen().height_in_pixels
		return (width, height)
