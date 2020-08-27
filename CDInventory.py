#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
#Brent Kieszling, 2020-Aug-17, Added function new_cd and add_cd
#Brent Kieszling, 2020-Aug-18, Updated function write_file
#Brent Kieszling, 2020-Aug-19, Fixed
#Brent Kieszling, 2020-Aug-24, Updated Data Processor and File Processor functions, 
#       converted from .txt to .dat file type, Added error handling, 
#------------------------------------------#

import os
import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {'ID': '', 'Title': '', 'Artist': ''}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
if os.path.exists(strFileName) != True:
    objFile = open(strFileName, 'ab')
    objFile.close()
class DataProcessor:
    """Processes the data"""
    @staticmethod
    def add_cd(tplNewCD, lstCurrentCDs):
        """Adds a new CD

        Takes the user input tplNewCD and assigns each value to a dictionary with keys:
        ID, Title, and Artist. Then it adds it to the active table.

        Args:
            tplNewCD (tuple): Contains 3 items: ID, Title, and Artist.
            lstCurrentCDs (list): A list of dictionaries all with the keys:
                'ID', 'Tittle', and 'Artist'

        Returns:
            lstCurrentCDs(list): Returns the updated list after adding the new entry
        """
        dicNewCD = {'ID': '', 'Title': '', 'Artist': ''}
        dicNewCD = {'ID': tplNewCD[0], 'Title': tplNewCD[1], 'Artist': tplNewCD[2]}
        lstCurrentCDs.append(dicNewCD)
        return lstCurrentCDs

    @staticmethod
    def delete_cd(remove_ID, lstCurrentCDs):
        """Deletes a CD

        Takes the user input remove_ID and searches the active table for the
        appropriate ID and removes it. Additionaly, tracks success 
        via blnCDRemoved.

        Args:
            remove_ID (interger): Holds the ID the user requested be removed.

        Returns:
            blnCDRemoved(boolean): True if row removed otherwise False.
            lstCurrentCDs(list): Returns the updated list after adding the new entry
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstCurrentCDs:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstCurrentCDs[intRowNr]
                blnCDRemoved = True
                break
        return blnCDRemoved, lstCurrentCDs



class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to import a list of dictionaries (lstSavedCollection) from a binary file.

        Args:
            file_name (string): name of file used to read the data from
            table (list): 2D table (list of dicts)

        Returns:
            table (list): 2D table (list of dicts)
        """
        table.clear()
#The try statement handles an instance where there is no saved data
        try:
            with open(file_name, 'rb') as fileObj:
                table = pickle.load(fileObj)
        except:
            pass
        return table

    @staticmethod
    def write_file(file_name, table):
        """Function to save a list of dictionaries (table) to a binary file

        Args:
            file_name (string): name of file used to read the data from
            table (list): 2D table (list of dicts)

        Returns:
            None.
        """
        with open(file_name, 'wb') as fileObj:
                pickle.dump(table, fileObj)


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def new_cd():
        """Allows the user to add a CD to the active inventory table

        Args:
            None.

        Returns:
            intID (interger): Serialized ID
            strTitle (string): Tittle of CD
            stArtist (string): Name of artist

        """
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID = input('Enter ID: ').strip()
        while True:
#This try handles the case where a non interger is entered
            try:
                intID = int(strID)
                break
            except:
                strID = input('Please enter an interger for the ID.')
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return intID, strTitle, stArtist


# 1. When program starts, read in the currently saved Inventory.
lstTbl = FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()

    # 3. Process menu selection
    strChoice = IO.menu_choice()
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled. ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        #This casts the return from IO.new_cd() into the function DataProcessor.add_cd
        lstTbl = DataProcessor.add_cd(IO.new_cd(), lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            strIDDel = input('Which ID would you like to delete? ').strip()
            try:
                intIDDel = int(strIDDel)
                break
            except:
                print('Please enter an integer.')
        # 3.5.2 search thru table and delete CD
        blnCDRemoved, lstTbl = DataProcessor.delete_cd(intIDDel, lstTbl)
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




