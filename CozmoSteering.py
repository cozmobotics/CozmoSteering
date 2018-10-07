#!/usr/bin/env python3

# CozmoSteering
# *************

# Mimicks a control stick like on a remote controlled airplane 
# In the center of the canvas, you will see a little circle. 
# Click and drag this cirkle 
# Dragging it up will send Cozmo forward, 
# dragging it down will send Cozmo backward, 
# dragging it to the right will make Cozmo turn right, 
# dragging it to the left will make Cozmo turn left.
# Any combinations of straight and turn are possible
# Cozmo will drive a curved line. 
# Alt-drag will make Cozmo turn in place,
# Shift-drag will make Cozmo drive straight. 



from tkinter import *
import cozmo
import math


def heartbeat ():
	global Speed
	global WindowSteering
	global Heartbeat
	global RobotGlobal
	global OldSpeed
	
	if (OldSpeed != Speed):
		RobotGlobal.drive_wheels(Speed[0], Speed[1])
		print (int(Speed[0]), int(Speed[1]))
		OldSpeed = Speed
	
	WindowSteering.after (Heartbeat, heartbeat)	# restart this function 

def calcSpeed (Straight,Curve):
	# global Speed
	global SpeedMax
	global Width
	global Height
	
	Straight =  Height/2 - Straight
	Curve    =  Width/2 - Curve
	SpeedLeft  = (Curve - Straight) / Width * SpeedMax * 2
	SpeedRight = (Curve + Straight) / Width * SpeedMax * 2
	
	if (SpeedLeft > SpeedMax):
		SpeedLeft = SpeedMax
	if (SpeedLeft < -SpeedMax):
		SpeedLeft = -SpeedMax
	if (SpeedRight > SpeedMax):
		SpeedRight = SpeedMax
	if (SpeedRight < -SpeedMax):
		SpeedRight = -SpeedMax
	# +++ jeweils andere Geschwindigkeit proportional verringern damit Kurvenradius gleich bleibt????
	
	return (SpeedLeft, SpeedRight)

def Mousedown (Event):
	global RelX
	global RelY
	global Width 
	global Height

	RelX = Event.x - Width/2	# compensate for the point where user clicked (which may not be in the center of the circle). 
	RelY = Event.y - Height/2

def Mouseup (Event):
	global Width 
	global Height
	global Radius
	global Speed

	CanvasSteering.coords (Stick, Width/2-Radius, Height/2-Radius, Width/2+Radius, Height/2+Radius) # bring the circle into the center again
	Speed = (0,0)																					# stop motors 
	# print (int(Speed[0]), int(Speed[1])) 

def Mousemove (Event):
	global RelX
	global RelY
	global Radius
	global CanvasSteering
	global Stick
	global Speed
	
	CanvasSteering.coords (Stick, Event.x-Radius-RelX, Event.y-Radius-RelY, Event.x+Radius-RelX, Event.y+Radius-RelY)
	Speed = calcSpeed (Event.x-RelX, Event.y-RelY)
	# print (int(Speed[0]), int(Speed[1]))
	
def AltMousemove (Event):
	global Width
	global Height
	global RelY
	MyEvent = Event
	
	MyEvent.y = Height/2 + RelY		# only movement along horizontal axis 
	Mousemove (MyEvent)				# go on like normal mouse move
	
def ShiftMousemove (Event):
	global Width
	global Height
	global RelX
	MyEvent = Event
	
	MyEvent.x = Width/2 + RelX		# only movement along vertical axis 
	Mousemove (MyEvent)				# go on like normal mouse move
	
def resizeWindow (Event):
	global WindowSteering
	global Width
	global Height
	
	WindowSteering.geometry(str(Width) + "x" + str(Height)) # do not allow the user to resize the window
	
# -------------------------------------------------------
	
# configuration 
Radius = 5			# radius of circle
Width = 200			# height and width of window
Height= Width
Heartbeat = 250		# cycle time in ms for updating motor speeds 
SpeedMax   = 200		# maximum motor speed in mm/sec

# global variables
RelX = 0
RelY = 0
SpeedRight = 0
SpeedLeft  = 0
OldSpeed = 0
Speed = (SpeedLeft,SpeedRight)
RobotGlobal = 0


WindowSteering = Tk()
WindowSteering.geometry(str(Width) + "x" + str(Height))					# something like "200x200"
WindowSteering.title("Cozmo Steering")

CanvasSteering = Canvas (WindowSteering, width=Width, height=Height)
CanvasSteering.pack()

CanvasSteering.create_line (0, Height/2, Width, Height/2, fill="#C0C0C0")
CanvasSteering.create_line (Width/2, 0, Width/2, Height, fill="#C0C0C0")
Stick = CanvasSteering.create_oval (Width/2-Radius, Height/2-Radius, Width/2+Radius, Height/2+Radius)
CanvasSteering.itemconfig (Stick, fill="#FFFFFF")

CanvasSteering.tag_bind (Stick, "<Button-1>", Mousedown) 
CanvasSteering.tag_bind (Stick, "<B1-Motion>", Mousemove) 
CanvasSteering.tag_bind (Stick, "<ButtonRelease-1>", Mouseup)

CanvasSteering.tag_bind (Stick, "<Alt-Button-1>", Mousedown) 			# same as normal click 
CanvasSteering.tag_bind (Stick, "<Alt-B1-Motion>", AltMousemove) 
CanvasSteering.tag_bind (Stick, "<Shift-B1-Motion>", ShiftMousemove) 
WindowSteering.bind ("<Configure>", resizeWindow)

WindowSteering.after (Heartbeat, heartbeat)								# start periodical function 

def robotProgram(robot: cozmo.robot.Robot):
	global WindowSteering
	global RobotGlobal
	
	RobotGlobal = robot
	WindowSteering.mainloop()



cozmo.run_program(robotProgram)


