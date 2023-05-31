import sqlite3
import csv
import pandas as pd
from contextlib import closing
from tkinter import messagebox
import datetime
import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class ControlData:

  def addData(self, mat, x, y, status):
    with closing(sqlite3.connect(resource_path('material_data.db'))) as connection:
      with closing(connection.cursor()) as cursor:
        cursor.execute('CREATE TABLE IF NOT EXISTS mat_records (Material int primary key, Xpos int, Ypos int, Status varchar, Operator ID int)')
        material_to_add = self.getData(mat)
        if len(material_to_add) == 0:
          cursor.execute('INSERT INTO mat_records (Material, Xpos, Ypos, Status) VALUES (?, ?, ?, ?)', (mat, x, y, status))
          cursor.execute('COMMIT')
          messagebox.showinfo('SAVE DATA', 'POSITIONS ARE RECORDED SUCCESSFULLY!')
        else:
          answer = messagebox.askquestion('MATERIAL NUMBER STATUS', 'MATERIAL NUMBER IS EXISTED. DO YOU WANT TO OVERRIDE IT?')
          if answer == 'yes':
            self.updateData(mat, x, y, status)
            messagebox.showinfo('SAVE DATA', f'MATERIAL: {mat} POSITIONS ARE UPDATED SUCCESSFULLY!')

  def getAllData(self):
    with closing(sqlite3.connect(resource_path('material_data.db'))) as connection:
      with closing(connection.cursor()) as cursor:
        return cursor.execute('SELECT * FROM mat_records').fetchall()


  def getData(self, mat):
    with closing(sqlite3.connect(resource_path('material_data.db'))) as connection:
      with closing(connection.cursor()) as cursor:
        return cursor.execute('SELECT * FROM mat_records WHERE Material=?', (mat,)).fetchall()
        

  def updateData(self, mat, x=None, y=None, status=None, operator=None):
    with closing(sqlite3.connect(resource_path('material_data.db'))) as connection:
      with closing(connection.cursor()) as cursor:
        if len(self.getData(mat)) > 0:
          if operator == None: #Update at Setup
            cursor.execute('UPDATE mat_records SET (Xpos, Ypos) = (?, ?) WHERE Material=?',(x, y, mat))
          else:
            if x == None and y == None: # Update at run program to check out or in
              cursor.execute('UPDATE mat_records SET (Status, Operator) = (?, ?) WHERE Material=?',(status, operator, mat))
          cursor.execute('COMMIT')
          return True
        else:
          print('Material number not exist in database')
          return False


  def checkout(self, mat, name):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    with closing(sqlite3.connect(resource_path('material_data.db'))) as connection:
      with closing(connection.cursor()) as cursor:
        cursor.execute('CREATE TABLE IF NOT EXISTS mat_records (Material int, Operator varchar, Date varchar)')
        cursor.execute('INSERT INTO mat_records (Material, Operator, Date) VALUES (?, ?, ?)', (mat, name, today))
        cursor.execute('COMMIT')
        if len(self.getData(mat)) > 0:
          status = 'CHECKED-OUT'
          cursor.execute('UPDATE mat_records SET Status = ? WHERE Material=?',(status, mat))
          cursor.execute('COMMIT')
        messagebox.showinfo('CHECK OUT PROCESS', 'CHECKOUT COMPLETED SUCCESSFULLY!')


  def deleteMaterial(self, mat):
    with closing(sqlite3.connect(resource_path('material_data.db'))) as connection:
      with closing(connection.cursor()) as cursor:
        if len(self.getData(mat)) > 0:
          cursor.execute('DELETE FROM mat_records WHERE Material=?', (mat,))
          cursor.execute('COMMIT')
          messagebox.showinfo('DELETE MATERIAL', 'DELETION COMPLETED SUCCESSFULLY!')
          return True
        else:
          print('Material number not exist in database')
          return False


  def deleteTable(self, table_name):
    with closing(sqlite3.connect(resource_path('material_data.db'))) as connection:
      with closing(connection.cursor()) as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS {table_name}')


  def createCSV_ExcelFile(self):
    # writer = csv.writer(open('material_data_csv.csv', 'w'))
    # writer.writerow(['Material', 'XPos', 'YPos', 'Status', 'Operator'])
    # datas = self.getAllData()
    # for data in datas:
    #   writer.writerow([data[0], data[1], data[2], data[3], data[4]])
    with closing(sqlite3.connect(resource_path('material_data.db'))) as connection:
      with closing(connection.cursor()) as cursor:
        datas = pd.read_sql('SELECT * FROM mat_records', connection)
        datas.to_csv('materialData.csv', index=False)
        datas.to_excel('materialData.xlsx', index=False)
    
if __name__ == '__main__':
  app = ControlData()         
  print(app.createCSV_ExcelFile())
  
#addData(3456, 700, 800, 'AVAILABLE')

# data = cursor.execute('SELECT * FROM mat_records').fetchall()
# print(data)
# import sqlalchemy as db
# from sqlalchemy_utils import database_exists
# from sqlalchemy.orm import sessionmaker
# engine = db.create_engine("sqlite:///material_locations.db")

# conn = engine.connect()
# meta = db.MetaData()
# material_table = db.Table('material_data', meta,
#                           db.Column('Material', db.Integer(), primary_key=True),
#                           db.Column('Xpos', db.Integer(), nullable=False),
#                           db.Column('Ypos', db.Integer(), nullable=False),
#                           db.Column('Status', db.String(15), nullable=False),
#                           )
# meta.create_all(engine)
# # print(repr(meta.tables['material_data']))
# Session = sessionmaker(bind=engine)
# session = Session()

# def insertData(mat, x, y, status):
#   if database_exists("sqlite:///material_locations.db"):
#     if len(getPosition(mat)) == 0:
#       query = db.insert(material_table).values(
#         Material = mat,
#         Xpos = x,
#         Ypos = y,
#         Status = status
#       )
#       conn.execute(query)
#       conn.commit()
#     else:
#       print('Material number is already exist in database')


# def getPosition(mat):
#   return session.query(material_table).filter_by(Material=mat).all()


# insertData(1234, 500, 500, 'AV')

# print(f'Material: {getPosition(2345)[0][0]}')
# print(f'XPOS: {getPosition(2345)[0][1]}')
# print(f'YPOS: {getPosition(2345)[0][2]}')
# print(f'STATUS: {getPosition(2345)[0][3]}')