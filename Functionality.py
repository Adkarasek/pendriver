from tkinter import *



class Functionality():
    def __init__(self,root):
        self.root = root
        self.clearFrame()
        
        
    def clearFrame(self):
        for widgets in self.root.winfo_children():
            widgets.destroy() 