from tkinter import *
import csv
import subprocess
import sqlite3
from Functionality import *
import Config
import os
import SettingsMenu

#połączenie z bazą danych            
def connectToDb(dbPath):
    db = sqlite3.connect(dbPath)
    return db
 


def getGridWidth(q, widget):
        return (int(widget.winfo_width()/q/10))
#Czyści ramkę akcji (tą na górze)   
def clearFrame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()  
#Odczyt danych z pliku csv      
def readFromCSV():
        with open(os.path.join(os.path.dirname(__file__), Config.CONFIGCSV), newline='\n') as sqlCsv:
            sqlCsvReader = list(csv.reader(sqlCsv, delimiter=','))
        return sqlCsvReader
    
#Tabela
class EditableTable(Frame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.rows = []
        self.headers = []

        self.table_frame = parent
        # self.table_frame.pack(fill='both', expand=True)

        self.canvas = Canvas(self.table_frame, width=Config.FUNCTIONINFOSIZE[0]-60)
        self.canvas.pack(side=LEFT, fill='both', expand=True)
       
        self.scrollbar = Scrollbar(self.table_frame, command=self.canvas.yview, width=30)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.configure_canvas)

        self.table = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table, anchor='nw')

        self.load_data()

    def load_data(self):
        # Tworzenie nagłówków na podstawie kluczy słownika
        self.headers = list(self.data.keys())
        for i, header in enumerate(self.headers):
            label = Label(self.table, text=header, font=("Arial", 8), width = 30,wraplength=150, justify=LEFT)
            label.grid(row=i, column=0, sticky='w')  # Zmiana miejsca umieszczenia nagłówka
        
        # Tworzenie wierszy na podstawie wartości w słowniku
        print (self.data.values())
        for row_idx, row_data in enumerate(self.data.values(), start=0):  # Modyfikacja indeksu startowego
            row = []
            entry = Entry(self.table, font=("Arial", 8), width=50)
            entry.insert(0, row_data)
            entry.grid(row=row_idx, column=1)
            row.append(entry)
            self.rows.append(row)

    def configure_canvas(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def destroy(self) -> None:
        return super().destroy()            
 
     
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
                print (row)
                return row
    #Zmienia wartości w bazie danych config.sqlite na podstawie pliku csv
    def changeConfig(self,key):
        row = self.getSelectedSqlConfigRecord(key, self.csvList)
        for i in range (len(self.csvList[0])):
            if (Config.PROD==False):
                print('sqlite3 /home/mtvm/bin/config.sqlite "UPDATE settings SET value = ' + row[i]+ "' WHERE key = '" + self.csvList[0][i]+ "'"+ '"')
            else:
                db = connectToDb(Config.CONFIGDBPATH)
                c = db.cursor()
                c.execute('UPDATE settings SET value = ? WHERE key = ?', (row[i], self.csvList[0][i]))
                db.commit()
                db.close()
        self.table=SettingsMenu(self.frame)
           
            
    #pobiera settingsy z config.sqlite
    def getCurrentConfig(self):
        settings = {}
        db = connectToDb(Config.CONFIGDBPATH)
        c = db.cursor()
        c.execute('SELECT * FROM settings ORDER BY key')
        for k, v in c:
            settings[k] = v
        db.close()      
        return settings
    
    def initializeSettings(self):
        try:
            self.table.destroy()
            
        except:
            pass
        
      
        return EditableTable(self.tf, self.getCurrentConfig())
                 
#okno główne programu             
class MainWindow:
    def __init__(self, root):
        self.cfRow=0
        self.cfCol=0
        row = 0
        self.root = root
        root.title("Ustawiarka")
        root.geometry(Config.MAINWINDOWSIZE)
        self.actionsFrame = Frame(self.root,highlightbackground="black", highlightthickness=2,height=400, width=560)
        self.actionsFrame.grid(row=row, column=0, columnspan=10)
        self.actionsFrame.grid_propagate(0)
        row+=1
        self.configButton=self.generateButton(root,"Config",lambda: SettingsMenu(self.actionsFrame),True)
        row+=1
        self.rebootButton = self.generateButton(root,"Reboot",lambda: self.reboot(),True)
        self.serviceModeButton = self.generateButton(root,"Serwis",lambda: self.serviceMode())
        

        
    def getFrame(self):
        return self.actionsFrame    
    
    def serviceMode(self):
        if(Config.PROD):
            subprocess.run('sudo killall mtvm -63')  
        else:
            print('sudo killall mtvm -63')
         
    def reboot(self):
        if(Config.PROD):
            subprocess.run('sudo reboot')   
        else:
            print('sudo reboot')
            
    def generateButton(self,root, text, command, newRow=False):
        if(newRow):
            self.cfRow= self.cfRow+1
            self.cfCol=0
        button = (Button(root, text=text, command=command, width=Config.BUTTONWIDTH, height=Config.BUTTONHEIGHT).grid(row=self.cfRow, column=self.cfCol))  
        self.cfCol+=1
        return button        

class BM1 (MainWindow):
    def __init__(self, root):
        super().__init__(root)
        root.title("dupiarka")
        root.geometry("560x700")
           
    
root = Tk()
app = MainWindow(root)
root.mainloop()