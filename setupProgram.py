import tkinter
from tkinter import messagebox
import customtkinter
from PIL import Image
import serial
import os, sys
# import pandas as pd
from database import ControlData
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# -------------------------------------- Image Links--------------------------------------------------#
x_plus = customtkinter.CTkImage(dark_image=Image.open(resource_path('images/arrow-right.png')), size=(50, 50))
y_minus = customtkinter.CTkImage(dark_image=Image.open(resource_path('images/arrow-down.png')), size=(50, 50))
y_plus = customtkinter.CTkImage(dark_image=Image.open(resource_path('images/arrow-up.png')), size=(50, 50))
x_minus = customtkinter.CTkImage(dark_image=Image.open(resource_path('images/arrow-left.png')), size=(50, 50))
x_315 = customtkinter.CTkImage(dark_image=Image.open(resource_path('images/315.png')), size=(70, 70))
x_225 = customtkinter.CTkImage(dark_image=Image.open(resource_path('images/225.png')), size=(70, 70))
x_45 = customtkinter.CTkImage(dark_image=Image.open(resource_path('images/45.png')), size=(70, 70))
x_135 = customtkinter.CTkImage(dark_image=Image.open(resource_path('images/135.png')), size=(70, 70))
coordinate = customtkinter.CTkImage(dark_image=Image.open(resource_path('images/Coordinate.png')), size=(100, 100))
#-----------------------------------------------------------------------------------------------------#
my_color = ("white", '#252525')
textColor = '#F9F54B'
button_color = '#0081B4'

class DeleteMaterial(customtkinter.CTkToplevel):
  def __init__(self, **kwargs):
    self.app = ControlData()
    super().__init__(**kwargs)
    self.title('DELETE MATERIAL')
    self.geometry('350x200+200+400')
    for i in range(3):
      self.grid_rowconfigure(i, weight=1)
    self.font = customtkinter.CTkFont(None, 16)

    self.pwEntry = customtkinter.CTkEntry(self,
                                           width=250,
                                           height=35,
                                           border_width=1,
                                           border_color='red',
                                           corner_radius=20,
                                           fg_color=my_color,
                                           justify='center',
                                           placeholder_text='Enter Password Here',
                                           font=self.font
                                           )
    self.pwEntry.grid(row=0, column=0, pady=5, padx=50, sticky='EW')

    self.matEntry = customtkinter.CTkEntry(self,
                                           width=250,
                                           height=35,
                                           border_width=1,
                                           border_color='red',
                                           corner_radius=20,
                                           fg_color=my_color,
                                           justify='center',
                                           placeholder_text='Enter Material Number Here',
                                           font=self.font
                                           )
    self.matEntry.grid(row=1, column=0, pady=5, padx=50, sticky='EW')
    self.deleteBtn = customtkinter.CTkButton(self,
                                            text='DELETE MATERIAL',
                                            width=250, height=35,
                                            corner_radius=25,
                                            font=self.font,
                                            fg_color=button_color,
                                            command=self.deleteMat)
    self.deleteBtn.grid(row=2, column=0, pady=5, padx=50, sticky='EW')
    
  def deleteMat(self):
    pw = self.pwEntry.get()
    if pw == '' or pw != '0011':
      messagebox.showerror('INVALID PASSWORD', 'PLEASE ENTER PASSWORD OR INVALID PASSWORD')
    else:
      mat = self.matEntry.get()
      if mat == '':
        messagebox.showerror('INVALID DATA', 'PLEASE ENTER MATERIAL NUMBER')
      else:
        mat = int(mat)
        if self.app.deleteMaterial(mat):
          self.destroy()


class Setup_Program(customtkinter.CTkToplevel):
  def __init__(self, arduino, window=None, **kwargs):
  # def __init__(self, arduino, **kwargs):
    self.arduino = arduino
    self.window = window
    #self.dataFile = 'PartPosition.csv'
    self.is_override = False
    self.homeBtnFlashSignal = 0
    self.controlData = ControlData()
    super().__init__(**kwargs)
    self.title('SET UP PROGRAM')
    w = 700
    h = 800
    x = int((self.winfo_screenwidth() - w)/2)
    y = int((self.winfo_screenheight() - h)/2)
    self.geometry(f"{w}x{h}+{x+100}+{y}")
    self.grid_rowconfigure([0,1], weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.font = customtkinter.CTkFont(None, 16)
    self.frame1 = customtkinter.CTkFrame(self, fg_color=my_color)
    self.frame1.grid(row=0, column=0)
    self.frame1.grid_rowconfigure([0, 1, 2, 3, 4, 5], weight=1)
    self.frame1.grid_columnconfigure([0, 1], weight=1)
    self.frame2 = customtkinter.CTkFrame(self, fg_color=my_color)
    self.frame2.grid(row=1, column=0)
    self.frame2.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)
    self.frame2.grid_columnconfigure([0, 1, 2, 3, 4], weight=1)


    self.matLable = customtkinter.CTkLabel(self.frame1,
                                           text='MATERIAL NUMBER',
                                           width=120,
                                           height=25,
                                           fg_color=my_color,
                                           text_color=textColor,
                                           font=self.font)
    self.matLable.grid(row=0, column=0, pady=10, sticky='NEWS')
    self.matEntry = customtkinter.CTkEntry(self.frame1,
                                           width=250,
                                           height=35,
                                           border_width=1,
                                           border_color='red',
                                           corner_radius=20,
                                           fg_color=my_color,
                                           justify='center',
                                           font=self.font
                                           )
    self.matEntry.grid(row=0, column=1, pady=10, padx=40)
    self.matEntry.focus()

    self.xLable = customtkinter.CTkLabel(self.frame1,
                                           text='X-POSITION',
                                           width=120,
                                           height=25,
                                           fg_color=my_color,
                                           text_color=textColor,
                                           font=self.font)
    self.xLable.grid(row=1, column=0, pady=10, sticky='NEWS')
    self.xEntry = customtkinter.CTkEntry(self.frame1,
                                           width=250,
                                           height=35,
                                           border_width=1,
                                           border_color='red',
                                           corner_radius=20,
                                           fg_color=my_color,
                                           justify='center',
                                           font=self.font
                                           )
    self.xEntry.grid(row=1, column=1, pady=10, padx=40)

    self.yLable = customtkinter.CTkLabel(self.frame1,
                                           text='Y-POSITION',
                                           width=120,
                                           height=25,
                                           fg_color=my_color,
                                           text_color=textColor,
                                           font=self.font)
    self.yLable.grid(row=2, column=0, pady=10, sticky='NEWS')
    self.yEntry = customtkinter.CTkEntry(self.frame1,
                                           width=250,
                                           height=35,
                                           border_width=1,
                                           border_color='red',
                                           corner_radius=25,
                                           fg_color=my_color,
                                           justify='center',
                                           font=self.font
                                           )
    self.yEntry.grid(row=2, column=1, pady=10, padx=40)

    self.homePartPos = customtkinter.CTkButton(self.frame1,
                                              text='MANUALLY ENTER POS',
                                              width=250, height=35,
                                              corner_radius=25,
                                              font=self.font,
                                              fg_color=button_color,
                                              command=self.sendManualPositions)
    self.homePartPos.grid(row=3, column=0, pady=10, padx=40)

    self.savePos = customtkinter.CTkButton(self.frame1,
                                          text='SAVE POSITION',
                                          width=250, height=35,
                                          corner_radius=25,
                                          font=self.font,
                                          fg_color=button_color,
                                          command=self.savePosition)
    self.savePos.grid(row=3, column=1, pady=10, padx=40)

    self.homeMachine = customtkinter.CTkButton(self.frame1,
                                              text='HOME MACHINE',
                                              width=250, height=35,
                                              corner_radius=25,
                                              font=self.font,
                                              fg_color=button_color,
                                              command=self.homingMachine)
    self.homeMachine.grid(row=4, column=0, pady=10, padx=40)

    self.finish = customtkinter.CTkButton(self.frame1,
                                          text='FINISH SETUP',
                                          width=250, height=35,
                                          corner_radius=25,
                                          font=self.font,
                                          fg_color=button_color,
                                          command=self.finishSetup)
    self.finish.grid(row=4, column=1, pady=10, padx=40)

  
    self.switch_var = customtkinter.StringVar(value="off")

    self.switch = customtkinter.CTkSwitch(self.frame1,
                                          text="TURN LASER OFF/ON",
                                          corner_radius=25,
                                          switch_width=100,
                                          switch_height=25,
                                          font=self.font,
                                          fg_color=button_color,
                                          command=self.switch_event,
                                          variable=self.switch_var,
                                          onvalue="on",
                                          offvalue="off"
                                          )
    self.switch.grid(row=5, column=0, padx=40, pady=10) 
    
    self.delete_mat = customtkinter.CTkButton(self.frame1,
                                          text='DELETE MATERIAL',
                                          width=250, height=35,
                                          corner_radius=25,
                                          font=self.font,
                                          fg_color=button_color,
                                          command=self.deleteMat)
    self.delete_mat.grid(row=5, column=1, pady=10, padx=40)

  #----------------------------Moving direction buttons--------------------------------
    self.yPlus = customtkinter.CTkButton(master=self.frame2,
                                        image=y_plus,
                                        width=150, height=10,
                                        text="", fg_color='#252525')
    self.yPlus.grid(row=0, column=2, pady=5)
    self.yPlus.bind('<ButtonPress-1>', self.jogYPlus)
    self.yPlus.bind('<ButtonRelease-1>', self.stopJogMotor)
    self.yMinus = customtkinter.CTkButton(master=self.frame2,
                                        image=y_minus,
                                        width=150, height=10,
                                        text="", fg_color='#252525')
    self.yMinus.grid(row=4, column=2, pady=5)
    self.yMinus.bind('<ButtonPress-1>', self.jogYMinus)
    self.yMinus.bind('<ButtonRelease-1>', self.stopJogMotor)
    self.xPlus = customtkinter.CTkButton(master=self.frame2,
                                        image=x_plus,
                                        width=150, height=10,
                                        text="", fg_color='#252525')
    self.xPlus.grid(row=2, column=4, pady=5)
    self.xPlus.bind('<ButtonPress-1>', self.jogxPlus)
    self.xPlus.bind('<ButtonRelease-1>', self.stopJogMotor)
    self.xMinus = customtkinter.CTkButton(master=self.frame2,
                                          image=x_minus,
                                          width=150, height=10,
                                          text="", fg_color='#252525')
    self.xMinus.grid(row=2, column=0, pady=5)
    self.xMinus.bind('<ButtonPress-1>', self.jogxMinus)
    self.xMinus.bind('<ButtonRelease-1>', self.stopJogMotor)
    self.x45 = customtkinter.CTkButton(master=self.frame2,
                                      image=x_45,
                                      width=150, height=10,
                                      text="", fg_color='#252525')
    self.x45.grid(row=1, column=3, pady=5)
    self.x45.bind('<ButtonPress-1>', self.jogx45)
    self.x45.bind('<ButtonRelease-1>', self.stopJogMotor)
    self.x135 = customtkinter.CTkButton(master=self.frame2,
                                      image=x_135, 
                                      width=150, height=10, 
                                      text="", fg_color='#252525')
    self.x135.grid(row=1, column=1, pady=5)
    self.x135.bind('<ButtonPress-1>', self.jogx135)
    self.x135.bind('<ButtonRelease-1>', self.stopJogMotor)
    self.x225 = customtkinter.CTkButton(master=self.frame2,
                                      image=x_225, width=150,
                                      height=10, text="",
                                      fg_color='#252525')
    self.x225.grid(row=3, column=1, pady=5)
    self.x225.bind('<ButtonPress-1>', self.jogx225)
    self.x225.bind('<ButtonRelease-1>', self.stopJogMotor)
    self.x315 = customtkinter.CTkButton(master=self.frame2,
                                        image=x_315,
                                        width=150, height=10,
                                        text="", fg_color='#252525')
    self.x315.grid(row=3, column=3, pady=5)
    self.x315.bind('<ButtonPress-1>', self.jogx315)
    self.x315.bind('<ButtonRelease-1>', self.stopJogMotor)
    self.coordinate = customtkinter.CTkButton(master=self.frame2,
                                              image=coordinate,
                                              width=150, height=10,
                                              text="", fg_color='#252525')
    self.coordinate.grid(row=2, column=2, pady=5)
    self.protocol('WM_DELETE_WINDOW', self.disabledClosingWindow)
    self.after(100, self.showing_position)
    self.after(500, self.flashHomeBtn)


  def disabledClosingWindow(self):
    pass

  def deleteMat(self):
    del_app = DeleteMaterial()
    del_app.focus_force()


  def switch_event(self):
    if self.switch_var.get() == 'off':
      self.writeToArduino('c')
    else:
      self.writeToArduino('g')
   

  def sendManualPositions(self):
    xpos = self.xEntry.get()
    ypos = self.yEntry.get()
    if (xpos != '' and ypos != ''):
      cmd = 'p' + 'X' + xpos + 'Y' + ypos
      self.writeToArduino(cmd)
      # (Output will be pX1234Y5689)
    else:
      messagebox.showerror('INVALID DATA', 'PLEASE ENTER A NUMBER.')


  def finishSetup(self):
    self.turn_off_lazer()
    self.window.deiconify()
    self.destroy()
    # self.arduino.close()


  def jogMotor(self, obj, cmd):
    obj.focus()
    #cmd = 'j'
    self.writeToArduino(cmd)


  def homingMachine(self):
    self.homeBtnFlashSignal = 1
    if self.arduino.isOpen():
      self.writeToArduino('h')
    else:
      print("COM3 is not connected")


  def writeToArduino(self, input):
    self.arduino.write(input.encode())


  def jogYPlus(self,event):
    self.jogMotor(self.yEntry, 'i')


  def jogYMinus(self,event):
    self.jogMotor(self.yEntry, 'l')


  def jogxPlus(self,event):
    self.jogMotor(self.xEntry, 'j')


  def jogxMinus(self,event):
    self.jogMotor(self.xEntry, 'k')


  def jogx45(self,event):
    self.jogMotor(self.xEntry, 'e')


  def jogx135(self,event):
    self.jogMotor(self.xEntry, 'v')


  def jogx225(self,event):
    self.jogMotor(self.xEntry, 'u')


  def jogx315(self,event):
    self.jogMotor(self.xEntry, 'w')


  def turn_off_lazer(self):
    self.writeToArduino('c')


  def stopJogMotor(self, event):
    self.writeToArduino('n')
    

  def savePosition(self):
    if (self.matEntry.get() != ""):
      x = int(self.xEntry.get())
      y = int(self.yEntry.get())
      self.controlData.addData(int(self.matEntry.get()), x, y, 'AVAILABLE')
      #self.writeData(self.matEntry.get(), x, y)     
    else:
      messagebox.showerror('MISSING INFO', 'PLEASE ENTER MATERIAL NUMBER')

  def readMotorPosition(self, data):
    motorPos = {} # store motor positions
    xtemp = ''
    ytemp = ''
    xPos = data.find('X')
    yPos = data.find('Y')
    
    if ((xPos >= 0) and (yPos >= 0)):
        for i in range(xPos+1, yPos):
            xtemp += data[i]
        for y in range(yPos+1, len(data)):
            ytemp += data[y]
        motorPos['X'] = xtemp
        motorPos['Y'] = ytemp
        return motorPos
    else:
        if (xPos == -1 and yPos >= 0):
            for i in range(yPos+1, len(data)):
                ytemp += data[i]
            motorPos['Y'] = ytemp
            return motorPos
        else:
            if (yPos == -1 and xPos >= 0):
                for i in range(xPos+1, len(data)):
                    xtemp += data[i]
                motorPos['X'] = xtemp
                return motorPos
            else:
                motorPos = {}
                return motorPos 


  def showing_position(self):
    if self.arduino.inWaiting()>0:
        line = str(self.arduino.readline().decode("utf-8"))
        line = line.strip()
        if (len(line) >= 2):
          myMotorXY = self.readMotorPosition(line)
          if (len(myMotorXY) == 2):
            self.xEntry.delete(0, customtkinter.END)
            self.xEntry.insert(0, myMotorXY['X'])
            self.yEntry.delete(0, customtkinter.END)
            self.yEntry.insert(0, myMotorXY['Y'])
          else:
            if (len(myMotorXY) == 1):
              if ('X' in line):
                self.xEntry.delete(0, tkinter.END)
                self.xEntry.insert(0, myMotorXY['X'])
              else:
                self.yEntry.delete(0, tkinter.END)
                self.yEntry.insert(0, myMotorXY['Y'])
    else:
      pass     
    self.after(100, self.showing_position)

  
  def flashHomeBtn(self):
    if self.homeBtnFlashSignal == 1:
      self.homeMachine.configure(fg_color='blue')
      self.homeMachine.after(100, lambda: self.homeMachine.configure(fg_color='#009EFF'))
    if self.homeBtnFlashSignal == 0:
      self.homeMachine.configure(fg_color=button_color)
    if (self.xEntry.get() == '0' and self.yEntry.get() == '0'):
      self.homeBtnFlashSignal = 0
      self.homeMachine.configure(fg_color=button_color)
    self.after(500, self.flashHomeBtn)


  # def readData(self):
  #   # This function to check the material number is existed in the database
  #   # And return a set data to use at writing data function
  #   try:
  #       with open(self.dataFile, 'r') as rf:
  #           rf.readline()
  #   except FileNotFoundError:
  #     messagebox.showerror('DATA MISSING', 'DATA RECORD NOT FOUND. PLEASE CHECK FILE PATH')
  #   else:
  #     data = pd.read_csv(self.dataFile)
  #     materialNumberList = list(data['MATERIAL'])
  #   return data, materialNumberList

if __name__ == '__main__':
  arduino = serial.Serial("COM3")
  arduino.baudrate = 9600
  if arduino.isOpen():
    print("{} is ready connected".format(arduino.port))
  app = Setup_Program(arduino)
  app.mainloop()
  # app = DeleteMaterial()
  # app.mainloop()