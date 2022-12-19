from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
     def __init__(self,name, date):
          #Your Code Here        
          self.name = name
          self.date = date

     def __str__ (self):
        # String output
          return(f"{self.name} ({self.date})")

        # Holiday output when printed.
     def getName(self):
          return self.name
     def getDate(self):
          return self.date
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
     def __init__(self):
         self.innerHolidays = []

     def getlist(self):
          return(self.innerHolidays)
   
     def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
          if isinstance(holidayObj, Holiday):
               self.innerHolidays.append(holidayObj)
               return True
          return False
     

     def findHoliday(self, HolidayName, d):
          # Find Holiday in innerHolidays
          # Return Holiday
          for h in self.innerHolidays:
               if h.getName() == HolidayName:
                    if h.getDate().strftime("%Y-%m-%d") == d.strftime("%Y-%m-%d"):
                         return h  
          return(None)
        

     def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
          name = True
          for h in self.innerHolidays:
               if h.getName().lower() == HolidayName.lower():
                    name = False
                    if h.getDate() == Date:
                         self.innerHolidays.pop(h)  
          if name:
               print(f'Error: {HolidayName} not found.')

        

     def read_json(self, filelocation):
          # Read in things from json file location
          # Use addHoliday function to add holidays to inner list.
          with open(filelocation, 'r') as f:
               data = json.load(f)
          for h in data['holidays']:
               tempholiday = Holiday(h['name'], datetime.strptime(h['date'], '%Y-%m-%d').date())
               self.addHoliday(tempholiday)



     def save_to_json(self, filelocation):
        # Write out json file to selected file.

          results = []
          d = {}
          for h in self.innerHolidays:
               d = {
                    "name": h.getName(),
                    "date": h.getDate().strftime("%Y-%m-%d")
               }
               results.append(d)

          hlist = {"holidays": results}

          with open(filelocation, 'w') as f:
               json.dump(hlist, f, indent = 4)
        
        
     def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     
          startyear = 2020
          while startyear <= 2024:
               r = requests.get(f"https://www.timeanddate.com/holidays/us/{startyear}")
               h = r.text    
               soup = BeautifulSoup(h,'html.parser')   
               table = soup.find('table',attrs = {'class':'table table--left table--inner-borders-rows table--full-width table--sticky table--holidaycountry'})        
               for row in table.tbody.find_all('tr'):
                    try:
                         colh = row.find_all('th')
                         cold = row.find_all('td')
                         hd = str(colh).split(">")
                         hd = hd[1].split("<")
                         hd = hd[0]
                         hd = datetime.strptime(f'{hd} {startyear}', '%b %d %Y').date()
                         n = cold[1]
                         n2 = str(n).split(">")
                         n2 = n2[2].split("<")
                         n2 = n2[0]
                         newholiday = Holiday(n2,hd)
                         if self.findHoliday(n2, hd) == None:
                              self.innerHolidays.append(newholiday)           
                    except:
                         pass
                        # print("Data Missing")
               startyear += 1

     def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return(len(self.innerHolidays))
    
     def filter_holidays_by_week(self, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
          newlist = []
          for h in self.innerHolidays:
               if h.getDate().isocalendar().week == week_number:
                    newlist.append(h)
          return newlist


        

     def displayHolidaysInWeek(self, week_number, dayear):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
          newlist = []
          for h in self.innerHolidays:
               if h.getDate().isocalendar().week == week_number:
                    if h.getDate().year == dayear.year:
                              print(h)
        

     

     def getWeather(self, weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.
        pass

     def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
          ntw = datetime.now().isocalendar().week
          nty = datetime.now().year
          self.displayHolidaysInWeek(ntw, nty)


def userAddHoliday(hlist):
     print("Add a Holiday")
     print("==============")
     hname = input("Holiday: ")
     hdate = input("Date Year-Month-Day: ")
     try:
          hdate = datetime.strptime(hdate, "%Y-%m-%d")
          h = Holiday(hname, hdate)
          hlist.addHoliday(h)
     except:
          print("Error adding holiday")
     

def userRemoveHoliday(hlist):
     print("Remove a Holiday")
     print("==============")
     hname = input("Holiday: ")
     hdate = input("Date Year-Month-Day: ")

     try:
          hlist.removeHoliday(hname, hdate)
     except:
          print("Error removing holiday")

def userSaveHoliday(hlist):
     print("Saving Holiday List")
     print("====================")
     sure = input("Are you sure you want to save your changes? [y/n]: ")
     if sure == 'n':
          print("Cancled: ")
          print("Holiday list file save canceled.")
          return False
     else:
          hlist.save_to_json("holidaysout.json")
          print("Your changes have been saved.")

def userViewHolidays(hlist):
     print("View Holidays")
     print("=================")
     y = input("Which Year: ")
     w = input("which Week [1-52, Leave blank for the current week]: ")
     if w == "":
          w = datetime.now().isocalendar().week
          print(w)
     else:
          w = int(w)
     y = datetime(int(y), 1, 1)
     
     hlist.displayHolidaysInWeek(w, y)



def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
    
     hl = HolidayList()

     location = "holidays.json"
     hl.read_json(location)
    

     hl.scrapeHolidays()


     print("Holiday Management")
     print("===================")
     print(f"There are {hl.numHolidays()} holidays stored in the system.")
     while True:
          print()
          print('''
Holiday Menue
===============
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit     
          ''')
          option = input("Select an option: ")
          print()
          if int(option) == 1:
               userAddHoliday(hl)
          elif int(option) == 2:
               userRemoveHoliday(hl)
          elif int(option) == 3:
               userSaveHoliday(hl)
          elif int(option) == 4:
               userViewHolidays(hl)
          elif int(option) == 5:
               sure = input(f"Are you sure you want to exit?\nYour changes will be lost.\n[y/n]: ")
               if sure == 'y':
                    print("Goodbye!")
                    break
if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





