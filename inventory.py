'''This project is a inventory checking system for a shoe company 
it takes in information from a txt file, adds each line to a shoe object
the list of shoe objects is then used in various ways as chosen by the user'''
#========Importing Modules Section=======
no_table = False
try:
    from tabulate import tabulate
except:
    no_table = True
#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
    def get_cost(self):
        #this method returns the int of the shoes price
        return(int(self.cost))

    def get_quantity(self):
        #this method returns an int of the shoes quantity
        return(int(self.quantity))

    def __str__(self):
        #prints a string representing all the data about the shoe
        print(f"For {self.product}: {self.code} in {self.country}, there are {self.quantity} units. The unit price is {self.cost}")


#=============Shoe list===========
shoe_list = []
#==========Functions outside the class==============
def read_shoes_data():
    #this function takes the information from the inventory file then appends it to the shoe list
    try:
        inventory= open("inventory.txt","r+",encoding='utf8')
        #first the try-except avoids errors if the inventory file is not found
    except IOError:
        print("Inventory file not found, please ensure it is in the correct folder.")
        exit()
        #if error is found program is exited to allow the user to fix the location issue
    line_counter = 0
    #with the file opened the information can be read after the first line is skipped
    for line in inventory:
        if line != "\n" and line_counter > 0:
            current_line = line
            current_line = current_line.replace("\n","")
            current_line = current_line.split(",")
            #The split line is then converted into a shoe class object
            new_shoe = Shoe(current_line[0],current_line[1],current_line[2],current_line[3],current_line[4])
            shoe_list.append(new_shoe)
            #which is then appended to the shoe list
        line_counter += 1
    inventory.close()

def capture_shoes():
    #this function allows the user to input a shoe object with various methods to avoid errors
    while True:
        new_shoe_country = input("Please enter the location of the stock of shoes: ")
        #this ensures the entry is a reasonable size for a location and that there are no commas
        if len(new_shoe_country) < 35:
            if ',' not in new_shoe_country:
                break
            else:
                print("Please do not include any commas in the location")
        else:
            print("Please enter a location less than 35 characters long")
    while True:
        new_shoe_code = input("Please enter the shoe's 5-digit product code [SKU*****]: ")
        try:
            #this try-except block casts the code to int
            new_shoe_code = int(new_shoe_code)
        except:
            pass
        #this logic ensures the code is a number and the correct length
        if isinstance(new_shoe_code,int) and len(str(new_shoe_code)) == 5:
            new_shoe_code = str(new_shoe_code)
            new_shoe_code_string = "SKU"+new_shoe_code
            break
        else:
            print("Please enter the 5 digit shoe code, numbers only")
    while True:
        #the only check needed here is to ensure the brand name is a realistic length and for ','
        new_shoe_product = input("Please enter the brand of the shoe: ")
        if len(new_shoe_product) < 35: 
            if ',' not in new_shoe_product:
                break
            else:
                print("Please do not include any commas in the brand name")
        else:
            print("Please enter a brand name less than 35 characters long")
    while True:
        #this checks that the cost entered is a number and prints an appropriate error message
        try:
            new_shoe_cost = int(input("Please enter the cost of the shoe: "))
            break
        except:
            print("Please only enter a number for the shoe's cost")
    while True:
        try:
            new_shoe_quantity = int(input("Please enter the quantity of the shoe: "))
            break
        except:
            print("Please only enter a number for the quantity of the shoe")
    #with all the errors checked and avoided, the shoe object is created
    new_shoe = Shoe(new_shoe_country,new_shoe_code_string,new_shoe_product,new_shoe_cost,new_shoe_quantity)
    #this new shoe object is then added to the shoe list
    shoe_list.append(new_shoe)
    #as the shoe being on the list means it could be added to the file, checks for commas are used

def view_all():
    #this function uses the __str__ function for each instance of shoe in the shoe list
    #if the user doesnt have the tabulate module installed then the no_table version is run
    if no_table == True:
        for shoe in shoe_list:
            Shoe.__str__(shoe)
    #otherwise a table is built for more easy viewing
    else:
        table_list = []
        for shoe in shoe_list:
            table_list.append([shoe.country,shoe.code,shoe.product,shoe.cost,shoe.quantity])
            #this loop creates a nested list with all the shoe data
        head = ["Country","Code","Product","Cost","Quantity"]
        #the header plus the new list are used to build the table 
        print(tabulate(table_list,headers=head,tablefmt="grid"))

def re_stock():
    #first the shoe_list is sorted by quantity and assigned to a new list 
    low_stock_list = sorted(shoe_list, key=Shoe.get_quantity)
    low_stock_shoe = low_stock_list[0]
    #the first entry to this list is the shoe object that may be changed
    print(f"The shoe with the lowest stock is {low_stock_shoe.product} in {low_stock_shoe.country}. It has {low_stock_shoe.quantity} remaining\n")
    #the user can choose to add a new number for the quantity of this shoe
    while True:
        user_choice = input("Would you like to add additional stock to this shoe? y/n: ")
        print(user_choice)
        if user_choice.lower() == "y" or user_choice.lower() == "n":
            break
        else:
            print("Only enter 'y' or 'n' to make your selection")
    #this avoids errors from unexpected user behaviour
    if user_choice.lower() == 'y':
    #if the user selects y the new stock will be written to the file after error checking
        while True:
            new_quantity = input("Please enter the new quantity you wish to add to the current stock: ")
            try:
                new_quantity = int(new_quantity)
                break
            except:
                print("Please only enter a numerical value")
        new_quantity = new_quantity + int(low_stock_shoe.quantity)
        #this adds the current quantity and the desired addition together for a new total
        for shoe in shoe_list:
            #the shoe list is searched through for the matching shoe
            if Shoe.get_quantity(shoe) == int(low_stock_shoe.quantity) and shoe.product == low_stock_shoe.product:
                x = shoe_list.index(shoe)
                print(shoe_list[x].quantity)
                shoe_list[x].quantity = new_quantity
                #the value is updated in the main list
                print(shoe_list[x].quantity)
        #with the list updated now the file must be rewritten in format with the updated stock
        inventory = open('inventory.txt','w+',encoding='utf8')
        #the first line is written with the labels as before
        inventory.write(("Country,Code,Product,Cost,Quantity")+("\n"))
        #then the rest of the file is written in format with , as seperators 
        for shoe in shoe_list:
            inventory.write((f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}") + ("\n"))
        inventory.close()

def search_shoe():
    #this function takes the SKU code from the user and prints the information for the shoe
    while True:
        search_code = input("Please enter the 5 digit code for the desired shoe: ")
        try:
            #block prevents errors from unexpected inputs
            search_code = int(search_code)
            #cast to int to check that the input only contains numbers
            search_code = str(search_code)
            #then cast back to ensure the length is correct
            if len(search_code) == 5:
                break
                #only if the entry is both numbers and 5 digits long will the loop exit
            else:
                print("Code is not 5-digits long, please enter a correct SKU code")
        except:
            print("Please only enter a 5-digit number for the shoe code")
    search = "SKU"+search_code
    #code is concatenated with SKU 
    print("")
    #improves ease of reading the console with some seperation
    found = False
    for shoe in shoe_list:
        if shoe.code == search:
            found = True
            Shoe.__str__(shoe)
            
            #all shoes with matching SKU are displayed to the user
    if found == False:
        #if a match is never found through the whole list this message is printed
        print(f"No matching shoes with code {search} were found.")
    print("")
def value_per_item():
    #this function prints to total value for each shoe in the shoe list
    value_table = []
    for shoe in shoe_list:
        total = Shoe.get_cost(shoe) * Shoe.get_quantity(shoe)
        #this checks if the user has the tabulate module, if not the information is printed
        if no_table == True:
            print(f"The total value for {shoe.product} is {total} ({shoe.cost} X {shoe.quantity})\n")
        else:
            value_table.append([shoe.product,shoe.cost,shoe.quantity,total])
    #if the user does have the module the value per item is displayed in a table
    if no_table == False:
        head = ["Product","Cost","Quantity","Total Value"]
        print(tabulate(value_table,headers=head,tablefmt="grid"))

        #the result is then printed in a more readable way for each shoe

def highest_qty():
    #this function creates a sorted list to find the highest quantity shoe, then displays the info
    highest_list = sorted(shoe_list, key=Shoe.get_quantity,reverse=True)
    #the list is reversed so the first value is the greatest
    highest_shoe = highest_list[0]
    print(f"\nThe shoe with the highest stock remaining is the {highest_shoe.product} in {highest_shoe.country}. It has {highest_shoe.quantity} units remaining")
    print(f"As such the {highest_shoe.product} is for sale!\n")
#==========Main Menu=============
read_shoes_data()
#the shoe list is created before the user is presented with a menu as it is needed in all functions
menu_choice = 0
#the menu loops until -1 is entered which exits the loop and ends the program
while menu_choice != -1:
    if no_table == True:
        print('''Please select the function you would like to perform
        1: Add Shoe - Creates a new shoe in the system
        2: View All - Displays information associated with each shoe
        3: Re-stock - Find the lowest stock shoe and add new units if desired
        4: Search Shoes - Use SKU code to find shoe in the system
        5: Value per item - Calculate the total cost of the stock for each shoe
        6: Highest Quantity - Find the highest quantity shoe in the system
        Or enter -1 to exit the program''')
    else:
        menu_table = [["1:", "Add Shoe", "Creates a new shoe in the system"],
        ["2:" , "View All" , "Displays information associated with each shoe"],
        ["3:" , "Re-stock" , "Find the lowest stock shoe and add new units if desired"],
        ["4:" , "Search Shoes" , "Use SKU code to find shoe in the system"],
        ["5:" , "Value per item" , "Calculate the total cost of the stock for each shoe"],
        ["6:", "Highest Quantity" , "Find the highest quantity shoe in the system"],
        ["-1:" , "Exit" , "Quits the program"]]
        menu_header = ["","Option","Description"]
        print("Please select the function you would like to perform:")
        print(tabulate(menu_table,headers=menu_header,tablefmt="grid"))
    while True:
        menu_choice = input("")
        try:
            menu_choice = int(menu_choice)
            break
        except:
            print("Please enter a number from the menu")
    if menu_choice == 1:
        #calls the capture shoes function which adds a shoe object to the list
        capture_shoes()
    elif menu_choice == 2:
        #calls the view all function
        view_all()
    elif menu_choice == 3:
        #calls the re_stock function
        re_stock()
    elif menu_choice == 4:
        #calls the search shoes function
        search_shoe()
    elif menu_choice == 5:
        #calls the value per item function
        value_per_item()
    elif menu_choice == 6:
        #calls the highest quantity function
        highest_qty()
print("Thank you for using the system")