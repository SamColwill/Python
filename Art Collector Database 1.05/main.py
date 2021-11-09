#DADSA Art Collector Coursework
#Sam Colwill
#October 2018

#Last Updated: 26/11/2018

import csv
import copy

class ArtObject:
    def __init__(self, itemID, description, value):
        self.itemID = int(itemID)
        self.description = description
        self.value = int(value)
    
    #Prints the Art Object
    def print_artobject(self):
        print (str(self.itemID) + ", " + self.description + ", " + FormatNumberIntoCurrency(self.value))

class Warehouse:
    def __init__(self, name):
        self.name = name
        self.contents = []
        self.insurance = 2000000000
    
    #Adds Art Object to Warehouse contents list
    def add_artobject(self, itemID, description, value):
        self.contents.append(ArtObject(itemID, description, value))
        
    #Removes Art Object from Warehouse contents list
    def remove_artobject(self, itemID):
        for ao in self.contents:
            if (ao.itemID == itemID):
                self.contents.remove(ao)
                return True
    
    #Get Art Object from Warehouse contents list
    def get_artobject(self, itemID):
        for ao in self.contents:
            if (ao.itemID == itemID):
                return ao
        
    #Loads all Art Objects from associated Warehouse Database csv file
    def load_artobjects(self):
        with open('Warehouse Database\\' + self.name + '.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader);
            for row in reader:
                itemID, description, value = row
                self.contents.append(ArtObject(itemID, description, value))
     
    #Returns total value of all Art Objects in the Warehouse           
    def get_contentsvalue(self):
        totalValue = 0;
        for ao in self.contents:
            totalValue = totalValue + int(ao.value)
        return totalValue
    
    #Returns most valuable Art Object in the Warehouse
    def get_mostvaluable(self):
        mostValuable = self.contents[0]
        for ao in self.contents:
            if ao.value > mostValuable.value:
                mostValuable = ao
        return mostValuable
    
    #Prints all Art Objects in the Warehouse
    def print_contents(self):
        for ao in self.contents:
            ao.print_artobject()

#Requests input from the user
def GetUserInput(message):
    userInput = input(message + "\n<-:")
    return userInput

#Requests a number from the user and will only accept a number
def GetUserInputNumber(message):
    userInput = None
    while userInput is None:
        try:
            userInput = float(input(message + "\n<-:"))
        except ValueError:
            print("You did not enter an number.")
    return round(userInput, 2)

#Requests the user to make a selection from a menu
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

#Formats a number to make it appear as currency (pound sterling)
def FormatNumberIntoCurrency(number):
    return u"\u00a3" + "{:,}".format(int(number))

#Main Menu Text Based Interface
def MainMenu():
    print("----------------------------------------------------------------")
    print("Art Collection Manager (ACM)                                    ")
    print("                                                                ")
    print("1 - Add a new Art Object                                        ")
    print("2 - Move an Art Object                                        ")
    print("3 - Remove an Art Object                                        ")
    print("4 - View Art Objects                                            ")
    print("5 - View Warehouse Details                                      ")
    print("6 - Exit ACM                                           ")
    return GetMenuSelection(6)

#Requests that the user confirm something
def Confirm(message, printLine):
    if (printLine):
        print("----------------------------------------------------------------")
    print(message)
    print("                                                                ")
    print("Continue?                                                ")
    print("1 - Yes                                                         ")
    print("2 - No                                                          ")
    if GetMenuSelection(2) == 1:
        return True
    else:
        return False

#Assigns a unique Item ID
def AssignItemID():
    itemID = 10000
    notAssigned = True
    while notAssigned:
        restart = False
        for w in warehouses:
            for ao in w.contents:
                if (itemID == ao.itemID):
                    itemID = itemID + 1;
                    restart = True
        if (restart == False):
            notAssigned = False
    return int(itemID);

#Returns the Warehouse with the most insurance remaining out of a sample of warehouses
def GetWarehouseWithMostInsuranceRemaining(sampleWarehouses):
    highestRemainingInsurance = 0
    for sw in sampleWarehouses:
        insuranceRemaining = sw.insurance - sw.get_contentsvalue()
        if(insuranceRemaining >= highestRemainingInsurance):
            highestRemainingInsurance = insuranceRemaining
            warehouseWithMostInsuranceRemaining = sw
    return warehouseWithMostInsuranceRemaining

#Returns an ordered list of warehouses from most to least insurance remaining
def GetOrderedWarehouses():
    warehousesCopy = warehouses.copy()
    orderedWarehouses = list() 
    orderedWarehouses.clear()
    while(warehousesCopy != []):
        warehouseWithMostInsuranceRemaining = GetWarehouseWithMostInsuranceRemaining(warehousesCopy)
        orderedWarehouses.append(warehouseWithMostInsuranceRemaining)
        warehousesCopy.remove(warehouseWithMostInsuranceRemaining)
    return orderedWarehouses

#Returns a list of Art Objects to try and move to make enough insurance for a new Art Object
def GetArtObjectMoveList(warehouse, insuranceRequired):
    artObjectMoveList = list()
    #The algorithm first finds the best Art Object to move, which if successfully moved
    #would be the only Art Object that needed to be moved in order add the new Art Object.
    artObjectBestMove = warehouse.get_mostvaluable();
    for ao in warehouse.contents:
        if (ao.value >= insuranceRequired):
            if(ao.value < artObjectBestMove.value):
                artObjectBestMove = ao
    artObjectMoveList.append(artObjectBestMove)
    #The algorithm then adds all Art Objects in the warehouse whose value is less than that
    #of the best Art Object incase the best Art Object cannot be moved.
    for ao in warehouse.contents:
        if (ao.value < artObjectBestMove.value):
            artObjectMoveList.append(ao)
    #It then sorts this list from highest value to smallest so that the minimum number of
    #Art Objects can be moved.
    artObjectMoveList.sort(key=lambda ao: ao.value, reverse = True)
    return artObjectMoveList

#Adds a new Art Object to the Art Collection
def AddNewArtObject():
    print("----------------------------------------------------------------")
    itemID = AssignItemID()
    description = GetUserInput("Describe the Art Object")
    value = GetUserInputNumber("Enter the Art Objects Value")
    
    #Reject new Art Object if its value is greater than 2 Billion
    if(value > 2000000000):
        print("----------------------------------------------------------------")
        print("Art Object could not be added." +
              "\nNo Warehouse has insurance greater than 2 Billion")
        return False
    
    #Reject new Art Object if its value is greater than the insurance remaining across all warehouses
    totalInsuranceRemaining = 8000000000;
    for w in warehouses:
        totalInsuranceRemaining = totalInsuranceRemaining - w.get_contentsvalue()
    if(value > totalInsuranceRemaining):
        print("----------------------------------------------------------------")
        print("Art Object could not be added.\n" + 
              "The total insurance remaining across all warehouses is less\n" +
              "than the value of the Art Object.")
        return False
    
    #To start the warehouses are sorted so that the algorithm can try and add the
    #new Art Object to the warehouse with the most insurance remaining.
    orderedWarehouses = GetOrderedWarehouses()
    if(value <= (orderedWarehouses[0].insurance - orderedWarehouses[0].get_contentsvalue())):
        if Confirm(description + " will be added to Warehouse " + orderedWarehouses[0].name +
                    "\nwith Item ID " + str(itemID) + " and a value of " + FormatNumberIntoCurrency(value), True):
            orderedWarehouses[0].add_artobject(itemID, description, value)
            print("----------------------------------------------------------------")
            print("Art Object successfully added.")
            return True
        else:
            print("----------------------------------------------------------------")
            print("Adding new Art Object cancelled.")
            return False
    else:
        #If the new Art Object could not be added to the warehouse with the most
        #space then the algorithm calculates the amount of insurance space required
        #then generates a list of art objects that could be moved to make room for
        #the new Art Object. If the algorithm moves an Art Object it will restart
        #so that the warehouses can be resorted and the best move can take place.
        print("----------------------------------------------------------------")
        findingSpace = True
        loopBreaker = 0;
        while(findingSpace):
            loopBreaker = loopBreaker + 1
            orderedWarehouses = GetOrderedWarehouses()
            insuranceRequired = value - (orderedWarehouses[0].insurance - orderedWarehouses[0].get_contentsvalue())
            artObjectMoveList = GetArtObjectMoveList(orderedWarehouses[0], insuranceRequired)
            artObjectMoved = False
            for ao in artObjectMoveList:
                if(artObjectMoved == False):
                    if(ao.value < orderedWarehouses[1].insurance - orderedWarehouses[1].get_contentsvalue()):
                        for w in warehouses:
                            if(w.name == orderedWarehouses[0].name):
                                w.contents.remove(ao)
                        for w in warehouses:
                            if(w.name == orderedWarehouses[1].name):
                                w.contents.append(ao)
                                destName = w.name
                        print(str(ao.itemID) + ", " + ao.description + ", " +
                                FormatNumberIntoCurrency(ao.value) + ". Move to Warehouse " + destName)
                        artObjectMoved = True
            if(value <= (orderedWarehouses[0].insurance - orderedWarehouses[0].get_contentsvalue())):
                print()
                if Confirm(description + " will be added to Warehouse " + orderedWarehouses[0].name +
                    "\nwith Item ID " + str(itemID) + " and a value of " + FormatNumberIntoCurrency(value) +
                    "\nbut the Art Objects listed above will need to be" +
                    "\nmoved out of the Warehouse for insurance purposes.", False):
                    orderedWarehouses[0].add_artobject(itemID, description, value)
                    print("----------------------------------------------------------------")
                    print("Art Object successfully added.")
                    return True
                else:
                    print("----------------------------------------------------------------")
                    print("Adding new Art Object cancelled.")
                    return False
            if(loopBreaker == 10000):
                #If the program has tried to move Art Objects 10,000 times with no
                #success then the program will break and print the user an exit message
                print("----------------------------------------------------------------")
                print("Art Object could not be added.\n" + 
                      "No amount of moving of the existing Art Objects will make room\n" +
                      "for the New Art Object.")
                return False

#Moves an Art Object between Warehouses
def MoveArtObject():
    print("----------------------------------------------------------------")
    itemID = GetUserInputNumber("Enter the ID of Art Object to Move")
    for w in warehouses:
        moveArtObject = w.get_artobject(itemID)
        if(moveArtObject != None):
            if Confirm(str(int(itemID)) + ", " + moveArtObject.description + ", " + FormatNumberIntoCurrency(moveArtObject.value) +
                       "\nMove this Art Object from Warehouse " + w.name, True):
                for w in warehouses:
                    if (w.remove_artobject(itemID)):
                        print("Art Object successfully removed from Warehouse " + w.name)
                print("Please select a Warehouse to move the Art Object to:")
                printNumber = 0
                for w in warehouses:
                    printNumber = printNumber + 1
                    if(moveArtObject.value < (w.insurance - w.get_contentsvalue())):
                        print(str(printNumber) + " - Warehouse " + w.name + " (Available)")
                    else:
                        print(str(printNumber) + " - Warehouse " + w.name + " (Not Available)")
                warehouseSelected = False
                while (warehouseSelected == False):
                    destWarehouse = GetMenuSelection(4)
                    if(moveArtObject.value < (warehouses[destWarehouse - 1].insurance - warehouses[destWarehouse - 1].get_contentsvalue())):
                        warehouses[destWarehouse - 1].add_artobject(itemID, moveArtObject.description, moveArtObject.value)
                        print("Art Object successfully moved.")
                        return 0;
                    else:
                        print("Selected Warehouse is not available.")
            else:
                print("Moving of Art Object has been cancelled.")
                return 0
    print("Art Object does not exist.")

#Removes an Art Object from the Warehouses
def RemoveArtObject():
    print("----------------------------------------------------------------")
    itemID = GetUserInputNumber("Enter the ID of Art Object to Remove")
    for w in warehouses:
        removeArtObject = w.get_artobject(itemID)
        if(removeArtObject != None):
            valueFormatted = u"\u00a3" + "{:,}".format(int(removeArtObject.value))
            if Confirm(str(int(itemID)) + ", " + removeArtObject.description + ", " + valueFormatted +
                       "\nRemove this Art Object from Warehouse " + w.name, True):
                for w in warehouses:
                    if (w.remove_artobject(itemID)):
                        print("Art Object successfully removed from Warehouse " + w.name)
                        return 0
            else:
                print("Removing of Art Object has been cancelled.")
                return 0
    print("Art Object does not exist.")

#Create the Warehouses and load there contents from the Warehouse Database 
warehouses = list()
warehouses.append(Warehouse("A"))
warehouses.append(Warehouse("B"))
warehouses.append(Warehouse("C"))
warehouses.append(Warehouse("D"))
for w in warehouses:
    w.load_artobjects()

#Art Collection Manager Main Loop
running = True
while running:
    mainMenu = MainMenu()
    if(mainMenu == 1): #Add a new Art Object
        warehousesBackup = copy.deepcopy(warehouses)
        added = AddNewArtObject()
        if (added == False):
            warehouses = copy.deepcopy(warehousesBackup)
    if(mainMenu == 2): #Move an Art Object
        MoveArtObject()
    if(mainMenu == 3): #Remove an Art Object
        RemoveArtObject()
    if(mainMenu == 4): #View Art Objects
        #Prints all Art Objects contained within each of the warehouses.
        for w in warehouses:
            print("----------------------------------------------------------------")
            print("Warehouse " + w.name + "\n")
            w.print_contents()
    if(mainMenu == 5): #View Warehouse Details
        #Displays some information on the warehouses as a whole followed by
        #some individual warehouse information.
        totalArtObjects = 0
        totalInsuranceRemaining = 8000000000;
        for w in warehouses:
            totalArtObjects = totalArtObjects + w.contents.__len__()
            totalInsuranceRemaining = totalInsuranceRemaining - w.get_contentsvalue()
        print("----------------------------------------------------------------")
        print("Warehouses Information")
        print("Total Art Objects: " + str(totalArtObjects))
        print("Total Art Collection Value: " + FormatNumberIntoCurrency(8000000000 - totalInsuranceRemaining))
        print("Total Insurance Remaining: " +  FormatNumberIntoCurrency(totalInsuranceRemaining))
        for w in warehouses:
            print("----------------------------------------------------------------")
            print("Warehouse " + w.name + "\n")
            print("Number of Art Objects: " + str(w.contents.__len__()))
            print("Total Value of Art Objects: " + u"\u00a3" + "{:,}".format(w.get_contentsvalue()))
            if(w.contents.__len__() != 0):
                print("Most Valuable Art Object:")
                w.get_mostvaluable().print_artobject()
    if(mainMenu == 6): #Exit
        input("Press Enter to Exit...")
        running = False

quit()