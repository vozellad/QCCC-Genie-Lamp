# py v2.7
# could be better, but that's always true. didn't have time to restructure

from __future__ import print_function
from gpiozero import Button
import RPi.GPIO as GPIO
import time
import random
from genielamp_header import *
import pygame

BUTTON1 = Button(26)
BUTTON2 = Button(16)
BUTTON3 = Button(12)
BUTTON4 = Button(17)

PIN1 = 27
#GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN1, GPIO.OUT)

BUTTONS_AMMOUNT = 3

randnums = []
genie_is_asleep = True
genie = True

pygame.mixer.init()

def button_init():
	print('button pressed')
	BUTTON1.when_pressed = None
	BUTTON2.when_pressed = None
	BUTTON3.when_pressed = None   

def get_answer1():
	playsound('A')
	time.sleep(1)
	button_init()
	playsound(QA_SETS[1][randnums[0]])
	
def get_answer2():
	playsound('B')
	time.sleep(1)
	button_init()
	playsound(QA_SETS[1][randnums[1]])

def get_answer3():
	playsound('C')
	time.sleep(1)
	button_init()
	playsound(QA_SETS[1][randnums[2]])

def playsound(filename):
	#dir = 'audio/{}.mp3'.format(filename)
	dir = 'audio/'
	dir += filename
	dir += '.mp3'

	pygame.mixer.music.load(dir)
	pygame.mixer.music.play()

def awaken_genie():
	BUTTON4.when_pressed = None
	global genie_is_asleep
	genie_is_asleep = False

def main():
	history = []

	while True:
		# pressure plate (not really)
#        while not GPIO.input(PIN1): print(GPIO.input(PIN1))
		GPIO.output(PIN1, GPIO.LOW)
		global genie_is_asleep
		genie_is_asleep = True
		while genie_is_asleep:
			BUTTON4.when_pressed = awaken_genie
		print('button pressed')
		# visually awaken genie
		#     lights
		GPIO.output(PIN1, GPIO.HIGH)
		#     todo: fans

		# randomly chooses questions        
		global randnums
		randnums = []
		counter = 0
		while counter < BUTTONS_AMMOUNT:
			tempnum = random.randint(0, len(QA_SETS[0]) - 1)
			
			# avoids duplicate and repeating questions
			if (tempnum not in randnums and
				tempnum not in history):
				randnums.append(tempnum)
				counter += 1
		history = randnums

		playsound('A')
		time.sleep(1)
		playsound(QA_SETS[0][randnums[0]])
		time.sleep(5)
		playsound('B')
		time.sleep(1)
		playsound(QA_SETS[0][randnums[1]])        
		time.sleep(5)
		playsound('C')
		time.sleep(1)
		playsound(QA_SETS[0][randnums[2]])        
		time.sleep(1)

	# wait for wish
		BUTTON1.when_pressed = get_answer1
		BUTTON2.when_pressed = get_answer2
		BUTTON3.when_pressed = get_answer3

		# genie goes to sleep

# testing audio files
#for x in range(11):
#    dir = 'audio/' + QA_SETS[0][x] + '.mp3'
#    pygame.mixer.music.load(dir)
#    pygame.mixer.music.play()
#    time.sleep(3)
#    dir = 'audio/' + QA_SETS[1][x] + '.mp3'
#    pygame.mixer.music.load(dir)
#    pygame.mixer.music.play()
#    time.sleep(3)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		# task failed successfully
		print()
