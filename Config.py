
PROD = False

if(PROD):
    CONFIGDIR = "/home/mtvm/mtvm/bin/"
else:
    CONFIGDIR = "/home/akarasek/Pulpit/pendriver/"
    
CONFIGCSV ="configsql.csv"   
CONFIGDB= "config.sqlite"
ACTDB = "act.sqlite"
CONFIGDBPATH = CONFIGDIR+CONFIGDB
ACTDBPATH = CONFIGDIR+ACTDB
MAINWINDOWSIZE = "560x750"
FUNCTIONINFOSIZE = [560,300]
BUTTONWIDTH = 10
BUTTONHEIGHT = 2
    