#DADSA Art Collector Coursework
#Sam Colwill
#October 2018

#Last Updated: 05/11/2018

#USEFUL CODE DELETE THIS AFTER COMPLETION
#print(u"\u00a3" + "{:,}".format(value))
#This prints a pound sign and formats the number with thousand commas

import csv
 
#Define Art Object Object
class ArtObject:
    def __init__(self, itemID, description, value):
        self.itemID = itemID
        self.description = description
        self.value = value
        
    def print_artobject(self):
        valueFormatted = u"\u00a3" + "{:,}".format(int(self.value))
        print (self.itemID + ", " + self.description + ", " + valueFormatted)

#Define Warehouse Object
class Warehouse:
    def __init__(self, name):
        self.name = name
        self.contents = []
        self.insurance = 2000000000
    
    def add_artobject(self, itemID, description, value):
        self.contents.append(ArtObject(itemID, description, value))
        
    def load_artobjects(self):
        with open('Warehouse Database\\' + self.name + '.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader);
            for row in reader:
                itemID, description, value = row
                self.contents.append(ArtObject(itemID, description, value))
                
    def get_contentsvalue(self):
        totalValue = 0;
        for ao in self.contents:
            totalValue = totalValue + int(ao.value)
        return totalValue
    
    def print_contents(self):
        for ao in self.contents:
            ao.print_artobject()

def GetUserInput(message):
    userInput = input(message + "\n<-:")
    return userInput

def GetMenuSelection(numMenuItems):
    menuSelection = None
    while menuSelection is None:
        try:
            menuSelection = int(input("<-:"))
            if ((menuSelection <= 0) or (menuSelection > numMenuItems)):
                print("Menu Selection " + str(menuSelection) + " does not exist.")
                menuSelection = None
        except ValueError:
            print("You did not enter an integer.")
    return menuSelection

#Main Menu
def MainMenu():
    print("--------------------------------------")
    print("Art Collection Manager (ACM)          ")
    print("                                      ")
    print("Menu                                  ")
    print("1 - Add a new Art Object              ")
    print("2 - View Art Objects                  ")
    print("3 - View Warehouses                   ")
    print("4 - Options                           ")
    print("5 - Save and Exit ACM                 ")
    return GetMenuSelection(5)

def AddNewArtObject():
    print("--------------------------------------")
    description = GetUserInput("Describe the Art Object")
    value = GetUserInput("Enter the Art Objects Value")
    if(warehouses[0])
    warehouses[0].add_artobject(itemID, description, value)
    
#Create the Warehouses and load there contents from the Warehouse Database
warehouses = list()
warehouses.append(Warehouse("A"))
warehouses.append(Warehouse("B"))
warehouses.append(Warehouse("C"))
warehouses.append(Warehouse("D"))

#Load the Art Objects from the Warehouse Database
for w in warehouses:
    w.load_artobjects()

#Art Collection Manager Main Loop
running = True
while running:
    mainMenu = MainMenu()
    if(mainMenu == 1): #Add a new Art Object
        AddNewArtObject()
    if(mainMenu == 2): #View Art Objects
        for w in warehouses:
            w.print_contents()
    if(mainMenu == 3): #View Warehouses
        for w in warehouses:
            print(u"\u00a3" + "{:,}".format(w.get_contentsvalue()))
    if(mainMenu == 4): #Options
        print("OPTIONS")
    if(mainMenu == 5): #Save and Exit
        print("SAVE AND EXIT")
        
with open('Warehouse Database\Warehouse A.csv', 'w', newline='') as csvfile:
    reader = csv.reader(csvfile)
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
