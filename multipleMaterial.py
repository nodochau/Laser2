import customtkinter
from tkinter import messagebox
# from PIL import Image
# from data import ReadData
from database import ControlData

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
textColor = '#F9F54B'

class MultipleMaterial(customtkinter.CTkToplevel):
  def __init__(self, master, mat_entry, matList, status, **kw):
    self.matList = matList
    self.master = master
    self.mat_entry = mat_entry
    self.status = status
    self.validMat = ControlData()
    # self.validMat = ReadData('PartPosition.csv')
    super().__init__(**kw)
    self.title('RUN MULTIPLE MATERIAL NUMBER')
    self.width = 450
    self.height = 150
    self.row = 0
    self.wh = 0
    self.geometry(f'{self.width}x{self.height}+{500}+{200}')
    self.grid_columnconfigure([0, 1], weight=1)
    self.my_font = customtkinter.CTkFont(None, 16)
    self.matEntry = customtkinter.CTkEntry(master=self,
                               placeholder_text="Enter Material Number",
                               placeholder_text_color='#F9F54B',
                               width=200,
                               height=35,
                               border_width=2,
                               border_color='red',
                               justify='center',
                               corner_radius=35,
                               font=self.my_font)
    self.matEntry.grid(row=0, column=0, pady=20, padx=10)
    self.matEntry.bind('<KeyRelease>', self.validateMaterial)
    self.addBtn = customtkinter.CTkButton(self, text='ADD MATERIAL#', width=200, height=35, corner_radius=35, command=self.addMaterial, font=self.my_font)
    self.addBtn.grid(row=0, column=1, padx=10)
    self.doneBtn = customtkinter.CTkButton(self, text='FINISH', width=200, height=35, corner_radius=35, command=self.finish, font=self.my_font)
    if self.row != 0:
      self.doneBtn.grid(row=self.row+1, column=0, pady=10, columnspan=2)

  def addMaterial(self):
    mat = self.matEntry.get()
    if len(self.validMat.getData(int(mat))) > 0:
      if self.status == 'CHECK OUT':
        if self.validMat.getData(int(mat))[0][3] != 'CHECKED OUT':
          self.matList.append(int(mat))
          self.wh += 45
          self.row += 1
          self.label = customtkinter.CTkLabel(master=self,
                                            text='MAT# ADDED: ' + mat,
                                            width=120,
                                            height=25,
                                            fg_color=("white", '#252525'),
                                            font=self.my_font,
                                            text_color=textColor)
          self.label.grid(row=self.row, column=0, pady=10, columnspan=2)
          self.doneBtn.grid(row=self.row+1, column=0, pady=10, columnspan=2)
          self.geometry(f'{self.width}x{self.height + self.wh}+{500}+{200}')
          self.matEntry.delete(0, customtkinter.END)
        else:
          messagebox.showerror('MATERIAL# STATUS', 'MATERIAL NUMBER HAD BEEN CHECKED OUT')
      else:
        self.matList.append(int(mat))
        self.wh += 45
        self.row += 1
        self.label = customtkinter.CTkLabel(master=self,
                                          text='MAT# ADDED: ' + mat,
                                          width=120,
                                          height=25,
                                          fg_color=("white", '#252525'),
                                          font=self.my_font,
                                          text_color=textColor)
        self.label.grid(row=self.row, column=0, pady=10, columnspan=2)
        self.doneBtn.grid(row=self.row+1, column=0, pady=10, columnspan=2)
        self.geometry(f'{self.width}x{self.height + self.wh}+{500}+{200}')
        self.matEntry.delete(0, customtkinter.END)
    else:
      messagebox.showerror('MATERIAL# STATUS', 'MATERIAL NUMBER NOT FOUND IN DATABASE')
      self.matEntry.delete(0, customtkinter.END)
      self.matEntry.focus()

  def finish(self):
    multi_text = ''
    for i in range(len(self.matList)):
      if i == len(self.matList) - 1:
        multi_text += str(self.matList[i])
      else:
        multi_text += str(self.matList[i]) + '-'
    self.mat_entry.delete(0, customtkinter.END)
    self.mat_entry.insert(0, multi_text)
    self.master.deiconify()
    self.destroy()


  def validateMaterial(self, event):
    try:
      if self.matEntry.get() != "":
        e = int(self.matEntry.get())
    except ValueError:
      messagebox.showerror('VALIDATE DATA', 'INVALID DATA, PLEASE ENTER A NUMBER')
      self.matEntry.delete(0, customtkinter.END)
      self.matEntry.focus()
    else:
      pass
    
    

if __name__ == '__main__':
  matList = []
  appp = customtkinter.CTk()
  app = MultipleMaterial(appp, matList)
  app.mainloop()