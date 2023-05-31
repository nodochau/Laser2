import customtkinter
from tkinter import messagebox
from PIL import Image
import serial, time
from setupProgram import Setup_Program
# from data import ReadData
from database import ControlData
from multipleMaterial import MultipleMaterial
import os, sys

"""
  This program to control the movement of laser to turn the relay on/off
  The timer is set with function 2 and the out put is NO and COM
  X1 connect to DO of light sensor
"""
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

arduino = serial.Serial("COM3")
arduino.baudrate = 9600
time.sleep(2)
line = "" # variable to store command send from arduino
previousMaterial = '' 
greenFlashSignal = 1
positionIndex = 0
textColor = '#F9F54B'
# myPosition = ReadData('PartPosition.csv')
myPosition = ControlData()
ENTRY_WIDTH = 220
ENTRY_HEIGHT = 35
rm = None # runMulti after function call 

if arduino.isOpen():
  print("{} is connected".format(arduino.port))
  

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def positionMainScreen(window, appWidth, appHeight):
  x = int((window.winfo_screenwidth() - appWidth)/2)
  y = int((window.winfo_screenheight() - appHeight)/2)
  window.geometry(f'{appWidth}x{appHeight}+{x+100}+{y}')


def Flashing ():
  global greenFlashSignal
  if arduino.inWaiting()>0:
    line = str(arduino.readline().decode("utf-8"))
    line = line.strip()
    if ('X' in line ) or ('Y' in line):
      greenFlashSignal = 0
      operatorEntry.delete(0, customtkinter.END)    
  else:
    pass
  if greenFlashSignal == 1:
    button_img.grid_forget()
    fakeBtn.grid(row=0, column=0, columnspan=2, sticky='NEWS', pady=20)
    button_img.after(300, lambda: button_img.grid(row=0, column=0, columnspan=2, sticky='NEWS', pady=20)) 
  app.after(500, Flashing)


def writeToArduino(input):
  arduino.write(input.encode())


def sendPositions(mat):
  global greenFlashSignal
  if len(myPosition.getData(mat)) > 0:
    xpos = myPosition.getData(mat)[0][1]
    ypos = myPosition.getData(mat)[0][2]
    if (xpos != None and ypos != None):
      greenFlashSignal = 1
      xEntry.delete(0, customtkinter.END)
      xEntry.insert(0, str(xpos))
      yEntry.delete(0, customtkinter.END)
      yEntry.insert(0, str(ypos))
      cmd = 'p' + 'X' + str(xpos) + 'Y' + str(ypos)
      writeToArduino(cmd)
    # (Output will be pX1234Y5689)
  else:
    messagebox.showerror('INVALID DATA', 'SORRY! THE MATERIAL IS NOT IN DATABASE.')


def runMultiMaterial():
  global rm, positionIndex, greenFlashSignal, stop
  if positionIndex == len(matList) and greenFlashSignal == 0:
    if processEntry.get() == 'CHECK OUT':
      status = 'CHECKED OUT'
    else:
      status = 'CHECKED IN'
    operator_id = int(operatorEntry.get())
    for mat in matList:
      myPosition.updateData(mat, None, None, status, operator_id)
    matList.clear()
    greenFlashSignal = 0
    materialEntry.delete(0, customtkinter.END)
    xEntry.delete(0, customtkinter.END)
    yEntry.delete(0, customtkinter.END)
    app.after_cancel(rm)
    app.after_cancel(stop)
    positionIndex = 0
  else:
    rm = app.after(2000, runMultiMaterial)
    stop = app.after(100, getStopSignalFromArduino)
  if greenFlashSignal == 0 and positionIndex < len(matList):
    greenFlashSignal = 1
    materialEntry.delete(0, customtkinter.END)
    materialEntry.insert(0, matList[positionIndex])
    xEntry.delete(0, customtkinter.END)
    xEntry.insert(0, myPosition.getData(matList[positionIndex])[0][1])
    yEntry.delete(0, customtkinter.END)
    yEntry.insert(0, myPosition.getData(matList[positionIndex])[0][2])
    sendPositions(matList[positionIndex])
    positionIndex += 1
  

def getMatStatus(mat, status):
  my_mat = myPosition.getData(mat)
  if len(my_mat) > 0:
    if my_mat[0][3] == 'CHECKED OUT' and status == 'CHECKED OUT':
      messagebox.showinfo('MATERIAL STATUS', 'THE MATERIAL YOU ENTERED HAD BEEN CHECKED OUT')
      return False
    else:
      if my_mat[0][3] != 'CHECKED OUT':
        # if status == 'CHECKED OUT':
          #elif my_mat[0][3] == 'AVAILABLE' or my_mat[0][3] == 'CHECKED IN':
        return True
      else:
        if status != 'CHECKED OUT':
          return True
  else:
    messagebox.showinfo('MATERIAL STATUS', 'THE MATERIAL YOU ENTERED NOT EXIST IN DATABASE')
    return False


def runProgram():
  global rm, stop, greenFlashSignal, matList
  if operatorEntry.get() != '':
    operator_id = int(operatorEntry.get())
    if processEntry.get() == 'SELECT PROCESS':
      messagebox.showerror('MISSING DATA', 'PLEASE SELECT CHECK IN OR CHECK OUT PROCESS')
    else:
      if len(matList) == 0:
        if materialEntry.get() != '':
          if processEntry.get() == 'CHECK OUT':
            status = 'CHECKED OUT'
          else:
            status = 'CHECKED IN'
          if getMatStatus(int(materialEntry.get()), status):
            stop = app.after(100, getStopSignalFromArduino)
            greenFlashSignal = 1
            myMaterial = int(materialEntry.get())
            if processEntry.get() == 'CHECK OUT':
              status = 'CHECKED OUT'
            else:
              status = 'CHECKED IN'
            sendPositions(myMaterial)
            myPosition.updateData(myMaterial, None, None, status, operator_id)
          # else:
          #   messagebox.showerror('INVALID DATA', 'THE MATERIAL NUMBER NOT EXIST IN DATABASE')
        else:
          messagebox.showerror('MISSING DATA', 'PLEASE ENTER MATERIAL NUMBER')
      else:
        rm = app.after(2000, runMultiMaterial)
  else:
    messagebox.showerror('MISSING DATA', 'PLEASE ENTER OPERATOR ID')
    
def getStopSignalFromArduino():
  # This function to listen to the signal s after arduino finishs one run
  # If the arduino send the signal s then the running button stops flashing 
  global line, greenFlashSignal, stop
  if greenFlashSignal == 1:
    app.after(100, getStopSignalFromArduino)
  else:
    app.after_cancel(stop)

  if arduino.inWaiting()>0:
    line = str(arduino.readline().decode("utf-8"))
    line = line.strip()  
    if (line == "s"):
      greenFlashSignal = 0
      line = ""     
    else:
      if (line == "X0Y0"):
        greenFlashSignal = 0
        line = ""
  else:
    pass
  
  
my_image = customtkinter.CTkImage(light_image=Image.open(resource_path("images/green1.png")), size=(50, 50))
my_fakeimage = customtkinter.CTkImage(light_image=Image.open(resource_path("images/blue.png")), size=(50, 50))

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
positionMainScreen(app, 700, 600)
app.iconbitmap(resource_path('images/bg.ico'))
app.title("B&G TOOL LOCATOR")
app.grid_columnconfigure([0, 1], weight=1)
my_font = customtkinter.CTkFont(None, 16)
matList = [] # to store material numbers 


def disable_closing_window():
  pass


# def slider_event(value):
#     text_var.set(str(int(value)))


def openSetupProgram():
  app.iconify()
  setupApp = Setup_Program(arduino=arduino, window=app)


def exitProgram():
  arduino.close()
  app.destroy()


def openMultiMaterial():
  if processEntry.get() != 'SELECT PROCESS' and operatorEntry.get() != '':
    status = processEntry.get()
    app.iconify()
    add_mat = MultipleMaterial(app, materialEntry, matList, status)
    add_mat.focus()
  else:
    if operatorEntry.get() == '':
      messagebox.showerror('MISSING DATA', 'PLEASE ENTER OPERATOR ID')
    else:
      if processEntry.get() == 'SELECT PROCESS':
        messagebox.showerror('MISSING DATA', 'PLEASE SELECT CHECK IN OR CHECK OUT PROCESS')
      
      

  
# The fake button set here to prevent the grid_forget could cause all widgets move 
# (flashing the run button) when running the program is activated.
fakeBtn = customtkinter.CTkButton(master=app, image=my_fakeimage, width=10, height=10, text="", fg_color='#252525', hover='disable')
fakeBtn.grid(row=0, column=0, columnspan=2, sticky='NEWS', pady=20)
button_img = customtkinter.CTkButton(master=app, image=my_image, width=10, height=10, text="", fg_color='#252525', hover='disable')
button_img.grid(row=0, column=0, columnspan=2, sticky='NEWS', pady=20)

# ----------This section to show motor speed adjustment---------------------
# text_var = tkinter.StringVar(value="50")
# slider_label = customtkinter.CTkLabel(master=app,
#                                       textvariable=text_var,
#                                       width=120,
#                                       height=25,
#                                       fg_color=("white", '#252525'),
#                                       font=my_font)
# slider_label.grid(row=1, column=1)
# motoSpeedLabel = customtkinter.CTkLabel(master=app,
#                                       text='MOTOR SPEED',
#                                       width=120,
#                                       height=25,
#                                       fg_color=("white", '#252525'),
#                                       font=my_font,
#                                       text_color=textColor)
# motoSpeedLabel.grid(row=2, column=0)
# slider = customtkinter.CTkSlider(master=app, from_=0, to=100, command=slider_event)
# slider.grid(row=2, column=1, sticky='NEWS', padx=20)
#---------------------------------------------------------------------------
operatorLabel = customtkinter.CTkLabel(master=app,
                                      text='OPERATOR ID',
                                      width=120,
                                      height=25,
                                      fg_color=("white", '#252525'),
                                      font=my_font,
                                      text_color=textColor)
operatorLabel.grid(row=1, column=0)
operatorEntry = customtkinter.CTkEntry(master=app,
                               width=ENTRY_WIDTH,
                               height=ENTRY_HEIGHT,
                               border_width=2,
                               border_color='red',
                               justify='center',
                               corner_radius=35,
                               font=my_font)
operatorEntry.grid(row=1, column=1)

process = customtkinter.CTkLabel(master=app,
                                      text='SELECT PROCESS',
                                      width=120,
                                      height=25,
                                      fg_color=("white", '#252525'),
                                      font=my_font,
                                      text_color=textColor)
process.grid(row=2, column=0, pady=(30, 0))

optionmenu_var = customtkinter.StringVar(value="SELECT PROCESS")
processEntry = customtkinter.CTkOptionMenu(master=app,
                                          values=['CHECK IN', 'CHECK OUT', 'AVAILABLE'],
                                          width=ENTRY_WIDTH,
                                          height=ENTRY_HEIGHT,
                                          corner_radius=35,
                                          fg_color='blue', 
                                          anchor='center',
                                          font=my_font,
                                          variable=optionmenu_var)

processEntry.grid(row=2, column=1, pady=(30, 0))

materialLabel = customtkinter.CTkLabel(master=app,
                                      text='MATERIAL NUMBER',
                                      width=120,
                                      height=25,
                                      fg_color=("white", '#252525'),
                                      font=my_font,
                                      text_color=textColor)
materialLabel.grid(row=3, column=0, pady=30)
xPosLabel = customtkinter.CTkLabel(master=app,
                                      text='X-POSITION',
                                      width=120,
                                      height=25,
                                      fg_color=("white", '#252525'),
                                      font=my_font,
                                      text_color=textColor)
xPosLabel.grid(row=4, column=0)
yPosLabel = customtkinter.CTkLabel(master=app,
                                      text='Y-POSITION',
                                      width=120,
                                      height=25,
                                      fg_color=("white", '#252525'),
                                      font=my_font,
                                      text_color=textColor)
yPosLabel.grid(row=5, column=0, pady=30)

materialEntry = customtkinter.CTkEntry(master=app,
                               width=ENTRY_WIDTH,
                               height=ENTRY_HEIGHT,
                               border_width=2,
                               border_color='red',
                               justify='center',
                               corner_radius=35,
                               text_color='#F9F54B',
                               font=my_font)
materialEntry.grid(row=3, column=1)
# materialEntry.bind('<FocusIn>', checkMaterialStatus)

xEntry = customtkinter.CTkEntry(master=app,
                               width=ENTRY_WIDTH,
                               height=ENTRY_HEIGHT,
                               border_width=2,
                               border_color='red',
                               justify='center',
                               corner_radius=35,
                               font=my_font)
xEntry.grid(row=4, column=1)

yEntry = customtkinter.CTkEntry(master=app,
                               width=ENTRY_WIDTH,
                               height=ENTRY_HEIGHT,
                               border_width=2,
                               border_color='red',
                               justify='center',
                               corner_radius=35,
                               font=my_font)
yEntry.grid(row=5, column=1)

setupBtn = customtkinter.CTkButton(app, text='SETUP PROGRAM', width=250, height=35, corner_radius=35, command=openSetupProgram, fg_color='blue', font=my_font)
setupBtn.grid(row=6, column=0, pady=30)
runBtn = customtkinter.CTkButton(app, text='RUN PROGRAM', width=250, height=35, corner_radius=35, font=my_font, fg_color='blue', command=runProgram)
runBtn.grid(row=6, column=1, pady=30)
exitBtn = customtkinter.CTkButton(app, text='EXIT PROGRAM', width=250, height=35, corner_radius=35, command=exitProgram, fg_color='blue', font=my_font)
exitBtn.grid(row=7, column=0, pady=15)
multiBtn = customtkinter.CTkButton(app, text='ADD MULTI MAT#', width=250, height=35, corner_radius=35, command=openMultiMaterial, fg_color='blue', font=my_font)
multiBtn.grid(row=7, column=1, pady=15)
app.protocol('WM_DELETE_WINDOW', disable_closing_window)
app.after(500, Flashing)
stop = app.after_cancel(getStopSignalFromArduino)
# stop = app.after(100, getStopSignalFromArduino)
rm = app.after_cancel(runMultiMaterial)
#homing_status = app.after_cancel(homing)
app.mainloop()

