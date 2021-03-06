# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:16:51 2021

@author: garvi
"""

months_array = ["Padding [Unknown]",
          "January",
          "Febuary",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"]

class SubProject:
    # A sublist is the bottom-most layer.

    def __init__(self, idx):
        self.project_name = "Empty-Project-Name"
        self.name = "Empty-Sub-Task"
        self.idx = idx
        # Members working on this task.
        self.members = 0
        
        # Sp dict holds data like so:
            # person_name: (eta, fin_date)
        
        # The len of this dict is numm_members
        self.sp_dict = {}
    
    def is_number(self, s):
        '''
        A simple function to check if something is numeric or not with float support
        '''
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    def process_and_return_data(self):
        '''
        Function to process SP data, return it to show in the GUI screen.
        Following same abstraction.
        
        Returns, [total_time_minutes, # members, date-string (the date to finish processed), time-string.]
        '''
        # Total effort in minutes.
        total_effort_left = 0
        for keys in self.sp_dict:
            # sp_dict holds {name: (eta, finish_date)}
            # Reminder: eta is time + mode.
            # can be 3 days, 6 years, 69 years. I dont know.
                        
            raw_string = self.sp_dict[keys][0]
            # this split may seem risky but it will always work, this is because how the data is stored first.
            raw_string_array = raw_string.split(' ')
            time_left_int = raw_string_array[0]
            
            # time_left_int is whatever the user put alongside the combo box option.
            # ^ this can be 3, 5, 6, or "pineapples"
            
            # combo_box option is raw_string_array[1]
            
            if (self.is_number(time_left_int) == True):
                
                try:
                    time_left = int(time_left_int)
                except:
                    time_left = int(float(time_left_int))
                    
                if (raw_string_array[1] == "Years"): 
                    total_effort_left += time_left * 365 * 24
                
                elif (raw_string_array[1] == "Months"):
                    # Average the month to 30; 366/12 = 30.50 days in a leap year
                    # Based on this you get 730.001
                    total_effort_left += time_left * 730.001
                    
                elif (raw_string_array[1] == "Days"):
                    total_effort_left += time_left * 24
                
                elif (raw_string_array[1] == "Hours"):
                    total_effort_left += time_left
                
                else:
                    total_effort_left += time_left / 60
                    
        from datetime import datetime, timedelta
        eta_from_now = datetime.now() + timedelta(minutes=total_effort_left)
                
        # month is a global array with months
        # This is faster than using stfttime,  
            # def _wrap_strftime(object, format, timetuple):
        # Does lots of checking and other stuff I dont care much about
        
        date_string = str(eta_from_now.day) + " " + str(months_array[eta_from_now.month]) + " " + str(eta_from_now.year)
        time_string = eta_from_now.strftime("%I:%M %p")
        print (date_string, time_string)
        
        return [total_effort_left, self.members, date_string, time_string]

                
    def return_data_string(self, data):
        '''
        Params: [total_effort_left, self.members, date-string, time-string]

        Returns the following string:
        Effort Remaining:
        Number of Members:
        Estimated Finish date:
        AI Advice: <TBD>
        '''
        
        ret_string = ""
        ret_string += "Number of Members: \t\t{} People\n".format(data[1])
        print ("HEY", data)
        if (data[0] * 60  < 60):
            ret_string += "Effort Remaining: \t\tLess than an hour left.\n"
        else:
            ret_string += "Effort Remaining: \t\t{:.0f} Hours Approximately\n".format(data[0])
        ret_string += "Estimated Finish Date: \t\t{}\n".format(data[2])
        ret_string += "AI Advice: \t\t\t<TBD>"
        
        return ret_string


    def add_data(self, data):
        '''
        Accepts data from the "Add member" button.
                data = [person_name, eta, fin_Date]
        '''
        self.sp_dict[data[0]] = (data[1], data[2])
        self.members += 1
        
        
        print ("Added data to: {}\t{}".format(self.name, self.sp_dict))
        
    def edit_data(self, data):
        '''
        Accepts data from gui and basically changes the sp_dict for whichever higher project in charge of this 
                ... bad boy
                
                data = [person_name, eta, fin_Date]
        '''
        is_found = False
        for keys in self.sp_dict:
            if (keys == data[0]):
                self.sp_dict[keys] = (data[1], data[2])
                is_found = True
                
        if (is_found == False):
            return -1
        # Dont change self.members. It's edit.
        print ("Editd data to: {}\t{}".format(self.name, self.sp_dict))

    def delete_data(self, data):
        '''
        Called from gui.py, onclick.
        data is an array containing all names to delete.
        '''
        
        # I forgot, if u delete and traverse the same dict, it causes problems.
        for names in data:
            del self.sp_dict[names]
            
            # MAN OVERBOARD!
            self.members -= 1
            
        print ("Deleted these names: {}".format(data))
        

    def update_sp_dicts(self):
        '''
        An hour has passed, change all the data.
        '''
        
        for members in self.sp_dict:
            
            # The tuple pair is (eta, fin_date)
            # Eta can be anything, 55 minutes or 55 years [<- wat?]
            time_array = self.sp_dict[members][0].split(' ')
            
            num_time = float(time_array[0])
            time_mode = time_array[1]
            
            if (time_mode == "Years"):
                num_time -= 0.000114155
            
            elif (time_mode == "Months"):
                num_time -= 0.00136986
                
            elif (time_mode == "Days"):
                num_time -= 0.0417 
                
            elif (time_mode == "Hours"):
                num_time -= 1
                
                if (num_time <= 0):
                    self.sp_dict[members] = ("Time's Up {}".format(members), "Was: {} {}".format(num_time, time_mode))
                    continue

                
            else:
                if (num_time <= 60):
                    # Delete this
                    self.sp_dict[members] = ("Time's Up {}".format(members), "Was: {} {}".format(num_time, time_mode))
                    continue
                else:
                    num_time -= 60
            
            new_num_time = str(num_time)
                    
            new_eta_findate_tuple = (new_num_time + " " + time_mode, self.sp_dict[members][1])
            
            self.sp_dict[members] = new_eta_findate_tuple
            pass
    
    def find_key_in_dict(self, data):
        '''
        A Function to find if a key exists in a dictionary,
        
        Params: Data, ideally a name or a string.
        '''
        
        for keys in self.sp_dict:
            if (keys == data):
                return 1
            
        return -1