from tkinter import *
import csv
import subprocess
import sqlite3
from Functionality import *
# okienko wyboru ustawień
class SettingsMenu(Functionality):
    def __init__(self, root):
        self.frame = root
        super().__init__(root)
        
        defaultVar="Wybierz wartość"
        
        #zmienna wartości pola dropdown
        var = StringVar()
        var.set(defaultVar)

        #odczyt danych z csv
        self.csvList = readFromCSV()
        
        #odczyt danych z pierwszej kolumny (do wyświetlenia w etykiecie dropdown list)
        firstColumnValues = [row[0] for row in self.csvList[1:]]

        #nagłówki tabeli
        self.headers = self.csvList[0]
        
        #szerokość grid
        gridElementWidth=getGridWidth(2,root)
        
        #dropdown, wybór
        dropdown = OptionMenu(root, var, *firstColumnValues)
        dropdown.config(width=gridElementWidth)
        dropdown.grid(row=0, column=0,sticky="W")
        
        #guzik potwierdzenia
        confirmButton = Button(root, text="Aktualizuj", width=gridElementWidth,height=1, state=DISABLED, command=lambda: self.changeConfig(var.get()))
        confirmButton.grid(row=0, column=1,sticky="W")

        #funkcja co po zmianie pola
        def onVariableChange(*args):
            
            if(var.get()==defaultVar):
                confirmButton.config(state=DISABLED)
            else:
                confirmButton.config(state=NORMAL)

        
        var.trace("w", onVariableChange)
        self.tf = Frame(root, width=600, height=300)
        self.tf.grid(row=2, column=0, columnspan=2)
        
        # self.table = Table(tf,self.getCurrentConfig())
        #self.table = EditableTable(tf, self.getCurrentConfig())
        self.table = self.initializeSettings()
        
    #pobiera wartość dla wybranego klucza z na podstawie pliku csv (domyślnie 1, numer seryjny)   
    def getSelectedSqlConfigRecord(self,key,data):
        for row in data:
            if key in row:
                return row
    #Zmienia wartości w bazie danych config.sqlite na podstawie pliku csv
    def changeConfig(self,key):
        row = self.getSelectedSqlConfigRecord(key, self.csvList)
        for i in range (len(self.csvList[0])):
            if (dev==False):
                print('sqlite3 /home/mtvm/bin/config.sqlite "UPDATE settings SET value = ' + row[i]+ "' WHERE key = '" + self.csvList[0][i]+ "'"+ '"')
            else:
                db = connectToDb(cfConfigDbName)
                c = db.cursor()
                c.execute('UPDATE settings SET value = ? WHERE key = ?', (row[i], self.csvList[0][i]))
                db.commit()
                db.close()
        self.table=SettingsMenu(self.frame)
           
            