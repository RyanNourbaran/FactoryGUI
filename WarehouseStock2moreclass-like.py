from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
root = Tk()
root.title('RestEasy Warehouse')

class EmptyError(Exception):
    def __init__(self):
        messagebox.showwarning('Empty Data Entry', 'Data Cannot Be Empty' )
        pass

class warehouse:
    def __init__(self,root):
        self.inventory = [] #keeps track of inventory items with all specifications
        self.itemnumbers = [] #keeps track of all item numbers
        self.editButtons = []
        self.data = []

        #Frames
        frame1 = ttk.Frame(root,padding = '3 3 3 3', relief = SUNKEN, borderwidth = 5)
        frame1.grid(column = 0, row = 0, sticky = (N,W,E,S),rowspan = 5)
        frame1.columnconfigure(0,weight = 1)
        frame1.rowconfigure(0,weight = 1)

        frame2 = ttk.Frame(root,padding = '3 3 3 3', relief = SUNKEN, borderwidth = 5)
        frame2.grid(column = 1, row = 0, sticky = (N,W,E,S))
        frame2.columnconfigure(0,weight = 1)
        frame2.rowconfigure(0,weight = 1)

        

        
        ###Text Entries
        self.itnumEntry = StringVar()
        self.itnumBox = ttk.Entry(frame1,  textvariable = self.itnumEntry)
        self.itnumBox.grid(column = 1, row = 0)
        self.data.append(self.itnumBox)

        itnumLabel = ttk.Label(frame1, text = 'Item Number : ')
        itnumLabel.grid(column = 0, row = 0, sticky = E)

        self.qtyEntry = StringVar()
        self.qtyBox = ttk.Entry(frame1,  textvariable = self.qtyEntry)
        self.qtyBox.grid(column = 1, row = 1)
        self.data.append(self.qtyBox)

        qtyLabel = ttk.Label(frame1, text = 'Quantity : ')
        qtyLabel.grid(column = 0, row = 1, sticky = E)

        self.nameEntry = StringVar()
        self.nameBox = ttk.Entry(frame1,  textvariable = self.nameEntry)
        self.nameBox.grid(column = 1, row = 2)
        self.data.append(self.nameBox)

        nameLabel = ttk.Label(frame1, text = 'Item Name : ')
        nameLabel.grid(column = 0, row = 2, sticky = E)

        self.locEntry = StringVar()
        self.locBox = ttk.Entry(frame1,  textvariable = self.locEntry)
        self.locBox.grid(column = 1, row = 3)
        self.data.append(self.locBox)

        locLabel = ttk.Label(frame1, text = 'Location : ')
        locLabel.grid(column = 0, row = 3, sticky = E)

        self.descEntry = StringVar()
        self.descBox = ttk.Entry(frame1,  textvariable = self.descEntry)
        self.descBox.grid(column = 1, row = 4)
        self.data.append(self.descBox)

        descLabel = ttk.Label(frame1, text = 'Description : ')
        descLabel.grid(column = 0, row = 4, sticky = E)

        

        ####Buttons
        bClear = ttk.Button(frame2, text = 'Clear', command = self.clear_entries)
        bClear.grid(column = 0, row = 0)
        
        bDlt = ttk.Button(frame2,  text = 'Delete', command = self.delete_entry)
        bDlt.grid(column = 0, row = 1)
        self.editButtons.append(bDlt)
        
        bSearch = ttk.Button(frame2,  text = 'Search', command = self.search_entry)
        bSearch.grid(column = 0, row = 2)
        self.editButtons.append(bSearch)

        bUpdate = ttk.Button(frame2,  text = 'Update', command = self.update_entry)
        bUpdate.grid(column = 0, row = 3)
        self.editButtons.append(bUpdate)

        bLoad = ttk.Button(frame2,  text = 'Load', command = self.load_entry)
        bLoad.grid(column = 1, row = 1)

        bSave = ttk.Button(frame2,  text = 'Save', command = self.save_entry)
        bSave.grid(column = 1, row = 2)

        bNew = ttk.Button(frame2, text = 'New', command = self.new_entry)
        bNew.grid(column = 1, row = 0)
        

        self.DisableButtons(self.editButtons)
        
    def EnableButtons(self,bList):
        for i in bList:
            i.config(state = NORMAL)
        return
        
    def DisableButtons(self,bList):
        for i in bList:
            i.config(state = DISABLED)
        return
        
    def clear_entries(self): #Defined a function that clears the entry boxes for tidyness
        self.itnumBox.delete(0,'end')
        self.qtyBox.delete(0,'end')
        self.nameBox.delete(0,'end')
        self.locBox.delete(0,'end')
        self.descBox.delete(0,'end')
            
    def new_entry(self,*Argv): #a new list of entries is made and inserted into inventory list

        for i in self.data:
                if i.get() == '':
                    raise EmptyError
        try:
            searchnum = eval(self.itnumEntry.get())
            if type(searchnum) != int:
                raise NameError
            
        except NameError:
            messagebox.showwarning('Incorrect Data Entry', "Item Number must be an integer")
            pass
        
        
        length = len(self.itemnumbers)-1
        if length >= 0:
            mid = length//2
            itemcheck  = self.binary_search(searchnum,mid, 0, length)
            if itemcheck != -1:
                self.clear_entries()
                messagebox.showerror('Error', 'An Item Exists With This Item Number!')
                return
        newitem = [searchnum] + [self.qtyEntry.get()]+ [self.nameEntry.get()] \
                  + [self.locEntry.get()] + [self.descEntry.get()] 

        self.inventory += [newitem]
        self.itemnumbers += [searchnum]
        self.clear_entries()
        self.inventory.sort() #inventory is then sorted again
        self.itemnumbers.sort() #itemnumbs are sorted as well
        self.EnableButtons(self.editButtons)
        print(self.inventory)
        print(self.itemnumbers)
            
    def delete_entry(self,*Argv):
        if messagebox.askquestion('Delete', ("Are you Sure you want to delete item #" + self.itnumEntry.get() + '?')) == 'yes':
            
            try:
                delitem = [eval(self.itnumEntry.get())] + [self.qtyEntry.get()]+ [self.nameEntry.get()] \
                          + [self.locEntry.get()] + [self.descEntry.get()]
                
                self.inventory.remove(delitem)
                self.itemnumbers.remove(eval(self.itnumEntry.get()))
                self.clear_entries()
                if self.inventory == []:
                    self.DisableButtons(self.editButtons)
                    
                
            except ValueError:
                self.clear_entries()
                messagebox.showerror('Error', 'Item Does not Exist!')
        else:
            self.clear_entries()
                
    def search_entry(self,*Argv):
        if self.inventory == []:
            self.clear_entries()
            messagebox.showerror('Error', 'Inventory is Empty!')
            return
        try:
            searchnum = eval(self.itnumEntry.get())
            self.clear_entries()
        except NameError:
            messagebox.showwarning('Incorrect Data Entry', "Item Number must be an integer")
            self.clear_entries()
            return
        length = len(self.itemnumbers)-1
        mid = length//2
        numposition = self.binary_search(searchnum,mid, 0, length)
        if numposition == -1:
            self.clear_entries()
            messagebox.showerror('Error', 'Item Does not Exist!')
            return
        self.itnumBox.insert('0',searchnum)
        self.qtyBox.insert('0',self.inventory[numposition][1])
        self.nameBox.insert('0',self.inventory[numposition][2])
        self.locBox.insert('0',self.inventory[numposition][3])
        self.descBox.insert('0',self.inventory[numposition][4])

    def binary_addsearch(self, x, mid, mins, maxs):##########################
        if self.itemnumbers[mid] :
            return
            
    def binary_search(self, x, mid, mins, maxs):
        if self.itemnumbers[mid] == x :
                return mid
                
        if maxs-mins > 2:
            if self.itemnumbers[mid] > x:
                mid2 = (mid + mins)//2
                return self.binary_search(x, mid2, mins, mid)
            if self.itemnumbers[mid] < x:
                mid2 = (mid + maxs)//2
                return self.binary_search(x, mid2, mid, maxs)
        elif x == self.itemnumbers[maxs]:
            return maxs
        elif x == self.itemnumbers[mins]:
            return mins
        else:
            return -1
            
    def update_entry(self,*Argv):
        searchnum = eval(self.itnumEntry.get())
        length = len(self.itemnumbers)-1
        mid = length//2
        numposition = self.binary_search(searchnum,mid, 0, length)
        if numposition == -1:
            self.clear_entries()
            messagebox.showerror('Error', 'Item Does not Exist!')
            return
        self.inventory[numposition][1] = self.qtyEntry.get()
        self.inventory[numposition][2] = self.nameEntry.get()
        self.inventory[numposition][3] = self.locEntry.get()
        self.inventory[numposition][4] = self.descEntry.get()
        print(self.inventory)
        
        self.clear_entries()
        
    def load_entry(self,*Argv):
        loadfile = filedialog.askopenfile(mode='r', defaultextension = '.txt', title = 'Load Previous Inventory', filetypes = [('All files', '.*'), ('Text files', '.txt')])
        self.inventory = []
        self.itemnumbers = []
        try:
            for i in loadfile.readlines():
                i = i[:-2]
                mylist = i.split(',')
                mylist[0] = eval(mylist[0])
                self.inventory += [mylist]
                self.itemnumbers += [mylist[0]]
        except NameError:
            messagebox.showerror('Incorrect Data Entry', "Item Numbers must be an integer")
        loadfile.close()
        
        self.itemnumbers.sort()
        self.inventory.sort()
        print(self.inventory)
        self.EnableButtons(self.editButtons)
    def save_entry(self,*Argv):
        savefile = filedialog.asksaveasfile(mode='w', defaultextension = '.txt', title = 'Load Previous Inventory', filetypes = [('All files', '.*'), ('Text files', '.txt')])
        for i in self.inventory:
            i[0] = str(i[0])
            print (','.join(i), file = savefile)



warehouse(root)
root.mainloop()

###########     THINGS TO CHECK

## all quantities must be ints/floats, names must be string, locations, etc...
## are blanks allowed? NOOOO ----- ESPECIALLY NOT THE ITEM NUMBER!!!!!!!!!!
## 
## exception handling for
## comments!



