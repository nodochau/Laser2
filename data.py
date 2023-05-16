import pandas as pd
from tkinter import messagebox

class ReadData:
  def __init__(self, filename):
    self.filename = filename

  def writeData(self, mat, xpos, ypos):
    try:
      with open(self.filename, 'r') as rf:
        rf.readline()
    except FileNotFoundError:
      with open(self.filename, 'a') as wf:
        print('MATERIAL', 'XPOS', 'YPOS', sep=',', file=wf)
        print(mat, xpos, ypos, sep=',', file=wf)
    else:
      with open(self.dataFile, 'a') as wf:
        data = pd.read_csv(self.filename)
        matList = list(data['MATERIAL'])
        if int(mat) in matList:
          answer = messagebox.askquestion('MATERIAL NUMBER STATUS', 'MATERIAL NUMBER IS EXISTED. DO YOU WANT TO OVERRIDE IT?')
          if answer == 'yes':
            index = matList.index(int(mat))
            data._set_value(index, 'XPOS', xpos)
            data._set_value(index, 'YPOS', ypos)
            data.to_csv(self.dataFile, index=False)
            messagebox.showinfo('SAVE DATA', f'MATERIAL: {mat} POSITIONS ARE UPDATED SUCCESSFULLY!')
        else:
          print(mat, xpos, ypos, sep=',', file=wf)
          messagebox.showinfo('SAVE DATA', 'POSITIONS ARE RECORDED SUCCESSFULLY!')
       
  def releasePos(self, mat):
    xpos = None
    ypos = None
    try:
      with open(self.filename, 'r') as rf:
        rf.readline()
    except FileNotFoundError:
      messagebox.showerror('MISSING FILE', 'NO FILES FOUND')
    else:
      with open(self.filename, 'a') as wf:
        data = pd.read_csv(self.filename)
        for row in data.itertuples():
          if row.MATERIAL == mat:
            xpos = row.XPOS
            ypos = row.YPOS      
        return xpos, ypos

  def validateMaterial(self, mat):
    is_mat_exist = False
    try:
      with open(self.filename, 'r') as rf:
        rf.readline()
    except FileNotFoundError:
      messagebox.showerror('MISSING FILE', 'NO FILES FOUND')
    else:
      with open(self.filename, 'a') as wf:
        data = pd.read_csv(self.filename)
        for row in data.itertuples():
          if row.MATERIAL == mat:
            is_mat_exist = True
    return is_mat_exist          


if __name__ == '__main__':
  mydata = ReadData('PartPosition.csv')
  print(mydata.releasePos(5678)[0])
  print(type(mydata.releasePos(5678)[0]))