import sys
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import Ellipse
from kivy.graphics import Line
from kivy.core.window import Window

# Module implemented by Pedro Rivera
from score import score_accountant
# Module implemented by Cristian Collazos
from word_validation import find_word
# Module implemented by Pedro Narvaez
from word_selection import selection

class WordInput(TextInput):
	def __init__(self, *args, **kwargs):
		super(WordInput, self).__init__(*args, **kwargs)

	def insert_text(self, substring, from_undo=False):
		substring = substring[:1 - len(self.text)]
		return super(WordInput, self).insert_text(substring, from_undo=from_undo)

	def set_next(self, next):
		self.next = next

	def keyboard_on_key_down(self, window, keycode, text, modifiers):
		key, key_str = keycode
		self.key = key
		super(WordInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

class Hanged(StackLayout):
	def __init__(self, **kwargs):
		super(Hanged, self).__init__(**kwargs)
		self.orientation = 'lr-bt'
		self.positionX = Window.size[0];
		self.positionY = Window.size[1];
		self.lbl_score = None
		self.list_boxes = []
		self.word = None
		self.part = 0
		self.score = score_accountant(callback_func=self.show_score)

	def on_enter(self):
		print "Press enter"

	def show_score(self, score):
		self.lbl_score.text = str(score)

	def background(self):
		'Paints the background and where monkey hangs'
		self.part = 0 #restar counter body parts
		positionX_pole = (self.positionX / 2) + (self.positionX / 4)
		with self.canvas.before:
			Rectangle(size = Window.size, color=Color(255, 255, 255))
			Line(points=[positionX_pole, self.positionY / 2 - 200, positionX_pole, self.positionY / 2 + 200], width=6, color=Color(0,0,0))
			Line(points=[positionX_pole - 300, self.positionY / 2 + 200, positionX_pole, self.positionY / 2 + 200], width=6, color=Color(0,0,0))
	
	def remove_background(self):
		#self.canvas.clear()
		with self.canvas.before:
			Rectangle(size = Window.size, color=Color(255, 255, 255))
		
	def paint_monkey(self, body_part):
		'Paints the parts of the monkey'
		with self.canvas.before:
			if body_part == 1: #head
				Ellipse(pos =(self.positionX / 2, (self.positionY / 2) + 100), size =(50, 50), color = Color(0, 0, 0))
			elif body_part == 2: #body
				Line(points=[self.positionX / 2 + 25, self.positionY / 2, self.positionX / 2 + 25, self.positionY / 2 + 120], width=6)
			elif body_part == 3: #left arm
				Line(points=[self.positionX / 2 - 50, self.positionY / 2 + 50, self.positionX / 2 + 25, self.positionY / 2 + 100], width=6)
			elif body_part == 4: #right arm
				Line(points=[self.positionX / 2 + 100, self.positionY / 2 + 50, self.positionX / 2 + 25, self.positionY / 2 + 100], width=6)
			elif body_part == 5: #left legg
				Line(points=[self.positionX / 2 - 50, self.positionY / 2 - 50, self.positionX / 2 + 25, self.positionY / 2 ], width=6)
			elif body_part == 6: #right legg
				Line(points=[self.positionX / 2 + 100, self.positionY / 2 - 50, self.positionX / 2 + 25, self.positionY / 2 ], width=6)

	def paint_hanged(self):
		self.background()
		with self.canvas.before:
			Ellipse(pos =(self.positionX / 2, (self.positionY / 2) + 100), size =(50, 50), color = Color(0, 0, 0))
			Line(points=[self.positionX / 2 + 8, self.positionY / 2 - 50, self.positionX / 2 + 8, self.positionY / 2 + 120], width=6)

	def add_buttons(self):
		'Add the text boxes, buttons, and the label for the score'
		self.btn_next = Button(text="Next word", size_hint_x=.5, size_hint_y=.1)
		self.btn_next.bind(on_press=self.button_next)
		self.add_widget(self.btn_next)
		self.btn_exit = Button(text="Exit", size_hint_x=.5, size_hint_y=.1)
		self.btn_exit.bind(on_press=self.button_exit)
		self.add_widget(self.btn_exit)

	def create_boxes(self):
		width_chars = self.positionX / len(self.word)
		position = 0
		for char in self.word:
			box = WordInput(text='-', width=width_chars, size_hint=(None, 0.15))
			box.position = position
			box.bind(text=self.char_validate, on_text_validate=self.on_enter)
			self.list_boxes.append(box)
			self.add_widget(box)
			position += 1

	def create_label_score(self):
		self.lbl_score = Label(text="210",font_size='40sp',  color=[0, 0, 0, 1], size_hint_x=.1, size_hint_y=.1)
		self.add_widget(self.lbl_score)

	def restart_score(self):
		self.score.score = 210
	
	def new_word(self, first_time):
		self.word = selection()
		if not first_time:
			self.remove_lbl_score()
			self.remove_background()
		if len(self.list_boxes) == 0:
			self.background()
			self.create_boxes()
			self.create_label_score()
		else:
			self.remove_boxes()
			self.remove_lbl_score()
			self.background()
			self.create_boxes()
			self.create_label_score()

	def button_exit(self,btn):
		print("Exit")
		sys.exit(0)

	def button_next(self,btn):
		print("Next word")
		self.restart_score()
		self.new_word(False)
		
	def char_validate(self, instance, value):
		v = True
		print("Guest: {}".format(self.word))
		#keys: 8 tab, 9 backspace, 23 enter, 32 spacebar
		if instance.key not in (8,9, 13, 32):
			v = find_word(self.word, value, instance.position)
		if v:
			self.text_validate()
		elif not v and self.score.score > 0:
			self.score.reduce_score()
			self.part += 1
			self.paint_monkey(self.part)
		elif not v and self.score.score == 0:
			self.paint_hanged()
			self.game_over(False)
			
	def text_validate(self):
		check = True
		pos = 0
		for char in self.word:
			box_temp = self.list_boxes[pos]
			if box_temp.text != char:
				check = False
			pos += 1
		if check:
			self.game_over(True)
			
	def remove_boxes(self):
		for i in self.list_boxes:
			self.remove_widget(i)
		self.list_boxes = []
	
	def remove_lbl_score(self):
		self.remove_widget(self.lbl_score)
	
	def game_over(self, won):
		self.remove_boxes()
		self.btn_next.text = 'Restart'
		self.restart_score()
		self.lbl_score.font_size = '40sp'
		self.lbl_score.size_hint_x = 1
		self.lbl_score.size_hint_y = 0.3
		if won:
			self.lbl_score.text = "You won"
		else:
			self.lbl_score.text = "You Lost"
	
class HangedApp(App):
	def build(self):
		hanged = Hanged()
		hanged.add_buttons()
		hanged.new_word(True)
		return hanged

	def _update(self, instance, value):
		pass

	def exit(self,btn):
		self.exit()

if __name__ == '__main__':
	HangedApp().run()


# apt remove --purge openjdk-\*
# install jdk-8 
# apt install google-android-platform-19-installer
	#- dl.google.com
	#- esto me lleva a instalar todo el sdk manualmente [NO]
# download and unpackage android sdk: http://dl.google.com/android/android-sdk_r24.4.1-linux.tgz
# en lugar de hacer un update, se copia todos los tar.gz
# 
# for adb
	#apt install libc6:i386 libstdc++6:i386
# for aapt
	#apt install zlib1g:i386
# 
# 
