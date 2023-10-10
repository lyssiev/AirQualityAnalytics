# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
import intelligence
import monitoring
import reporting
import datetime


# import utils
# import test_reporting


def main_menu():
    """main menu to allow for user interaction with all functions of the program
    """
    quit_ = False
    while not quit_:  # continue until quit is chosen
        # main menu interface
        print("\nMain Menu:\nR - Access the PR module \nI - Access the MI module \nM - Access the RM module \nA - "
              "Print the About text \nQ - Quit the application")
        choice = input().upper()  # makes not case-sensitive
        # depending on the user's input, different menus are displayed
        if choice == "R":
            print(reporting_menu())
        elif choice == "I":
            intelligence_menu()
        elif choice == "M":
            monitoring_menu()
        elif choice == "A":
            about()
        elif choice == "Q":
            quit()
            quit_ = True  # exits out of loop and program ends

        else:
            print("Sorry, you have entered an invalid input.")  # validation


def create_data():
    """
    creates a dictionary which stores the data from all .csv files

    Returns:
         dict: dictionary which contains all the data from file

    """
    # calls "create_dictionary" function for each file and stores in another dictionary
    main_dictionary = {"Harlington": create_dictionary("Harlington"),
                       "Marylebone Road": create_dictionary("Marylebone Road"),
                       "N Kensington": create_dictionary("N Kensington")}
    return main_dictionary


def create_dictionary(monitoring_station):
    """creates a dictionary for each monitoring station file with arrays that store the values of each heading

    Args:
        monitoring_station (string): the name of the monitoring station file

    Returns:
        dict: a dictionary that contains the values of each heading in the csv file
    """
    file = open("data/Pollution-London " + monitoring_station + ".csv", "r") # opens file
    file.readline() # ignores the first line as it contains headers
    # separate arrays for each header
    sub_dict = {
        "date": [],
        "time": [],
        "no": [],
        "pm10": [],
        "pm25": []
    }
    for line in file:
        # define variables
        comma_position = 0
        data = ""
        data_type = ""
        for i in range(len(line)):
            # checks whether the character is a comma to see if it is a new item of data
            if line[i] == ',':
                if comma_position == 0:
                    data_type = "date"
                elif comma_position == 1:
                    data_type = "time"
                elif comma_position == 2:
                    data_type = "no"
                elif comma_position == 3:
                    data_type = "pm10"

                sub_dict[data_type].append(data) # adds data to specific sub-dictionary
                comma_position += 1
                data = ""  # resets data

            # ensures commas and new lines are not added as part of the data value
            if line[i] != ',' and line[i] != '\n':
                data += line[i]

        data_type = "pm25"  # last data point would be missed otherwise
        sub_dict[data_type].append(data)
    return sub_dict


def reporting_menu():
    """allows the user to access all methods in the reporting module

    Returns:
        string: tells user that they have chosen to return to main menu
    """
    data = create_data()
    quitting = False
    while not quitting:
        # outputting all possible menu options
        print(
            "\nChoose an option:\n1 - daily average \n2 - daily median\n3 - hourly average\n4 - monthly average\n5 - "
            "peak hour of pollution on a specific date\n6 - count the missing data in a specific monitoring station "
            "and pollutant\n7 - fill the missing data for a specific monitoring station and pollutant\n8 - return to "
            "main menu")
        choice = input()
        if choice == "1":
            monitoring_station = choose_monitoring_station() # asks which station and pollutant the user wants to track
            pollutant = choose_pollutant()
            print(reporting.daily_average(data, monitoring_station, pollutant))
        elif choice == "2":
            monitoring_station = choose_monitoring_station()
            pollutant = choose_pollutant()
            print(reporting.daily_median(data, monitoring_station, pollutant))
        elif choice == "3":
            monitoring_station = choose_monitoring_station()
            pollutant = choose_pollutant()
            print(reporting.hourly_average(data, monitoring_station, pollutant))
        elif choice == "4":
            monitoring_station = choose_monitoring_station()
            pollutant = choose_pollutant()
            print(reporting.monthly_average(
                data, monitoring_station, pollutant))
        elif choice == "5":
            monitoring_station = choose_monitoring_station()
            pollutant = choose_pollutant()
            print("\nPlease input a date in the format yyyy-mm-dd: ")
            date = input()
            validate = validate_date(date)  # ensures date is in the right format
            if validate:
                print(reporting.peak_hour_date(
                    data, date, monitoring_station, pollutant))
            else:
                print("Please input a valid date.")
        elif choice == "6":
            monitoring_station = choose_monitoring_station()
            pollutant = choose_pollutant()
            print("number of 'No data' values: " +
                  str(reporting.count_missing_data(data, monitoring_station, pollutant)))
        elif choice == "7":
            print("\nPlease input the new value you want to replace 'No data' with: ")
            new_value = input()  # any string value is valid, so no validation is needed
            monitoring_station = choose_monitoring_station()
            pollutant = choose_pollutant()
            data = reporting.fill_missing_data(
                data, new_value, monitoring_station, pollutant)
            print(data)
            save_to_file(data)
        elif choice == "8":
            quitting = True  # breaks out of the loop
        else:
            print("Please enter a valid input.")
    return print("Returning to main menu.")


def save_to_file(data):
    """

    Args:
        data (string): saves string as a .txt file


    """
    f = open("new_data_test.txt", "w")
    f.write(str(data))
    f.close()


def validate_date(date):
    """checks the date is in the correct format

    Args:
        date (string): user input of the date

    Returns:
        bool: boolean value for whether the date is in the correct format
    """
    validate = True
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        validate = False
        print("Incorrect data format, should be YYYY-MM-DD")
    return validate


def choose_monitoring_station():
    """allows the user to choose a monitoring station

    Returns:
        string: name of the monitoring station
    """
    loop = True
    monitoring_station = ""
    while loop:
        print(
            "\nPlease enter the monitoring station you would like to analyse: \n1 - Harlington\n2 - Marylebone "
            "Road\n3 - North Kensington")
        choice = input()
        if choice == "1":
            loop = False
            monitoring_station = "Harlington"
        elif choice == "2":
            loop = False
            monitoring_station = "Marylebone Road"
        elif choice == "3":
            loop = False
            monitoring_station = "N Kensington"
        else:
            print("Please enter a valid input.")
    return monitoring_station


def choose_pollutant():
    """allows the user to choose the name of a pollutant they want to generate statistics for

    Returns:
        string: name of the pollutant
    """
    loop = True
    pollutant = ""
    while loop:
        print("\nPlease enter the pollutant you would like to analyse: \n1 - NO\n2 - PM10\n3 - PM25")
        choice = input()
        if choice == "1":
            loop = False
            pollutant = "no"
        elif choice == "2":
            loop = False
            pollutant = "pm10"
        elif choice == "3":
            loop = False
            pollutant = "pm25"
        else:
            print("Please enter a valid input.")
    return pollutant


def monitoring_menu():
    """allows the user to access all methods in the monitoring module

    Returns:
        string: tells user that they have chosen to return to main menu
    """
    print("************** PLEASE TAKE INTO ACCOUNT API WAS DOWN 18-12-22 and 19-12-22 :) **************")
    print("")
    quitting = False
    while not quitting:
        print(
            "\nChoose an option:\n1 - find live data from the API \n2 - find all group names \n3 - find all site "
            "codes and output them to a .txt file \n4 - "
            "average of the data between two dates \n5 - create a graph for data between two dates \n 6 - quit")
        choice = input()
        if choice == "1":
            try:
                # allows the user to input all parameters used in get live data from API
                print("Please enter the site code you want to use: ")
                site_code = input()
                print("Please enter the pollutant you want to monitor: ")
                species_code = input()
                print("Please enter the start date: ")
                start_date = input()
                print("Please enter the end date: ")
                end_date = input()
                print(monitoring.get_live_data_from_api(site_code, species_code, start_date, end_date))
            except NameError:
                print("You have entered an invalid input.")
        elif choice == "2":
            print(monitoring.get_group_codes())
        elif choice == "3":
            try:
                print("Please enter the name of group you would like the site codes for: ")
                group_name = input()
                data = (monitoring.get_site_codes(group_name))
                print("What do you want to call your .csv file?")
                file_name = input()
                f = open(file_name + ".txt", "w")  # writes to a .txt file
                f.write(str(data))
                f.close()
                print(data)
            except NameError:
                print("You have entered an invalid input.")
        elif choice == "4":
            print("\n Average of data: " + str(monitoring.average_api()))
        elif choice == "5":
            print(monitoring.create_graph())
        elif choice == "6":
            quitting = True
        else:
            print("Please enter a valid input.")
    return print("Returning to main menu.")


def intelligence_menu():
    """allows the user to access all methods in the intelligence module

    Returns:
        string: tells user that they have chosen to return to main menu
    """
    quitting = False
    img = []
    while not quitting:
        print(
            "\nChoose an option:\n1 - find red pixels \n2 - find cyan pixels \n3 - output connected components \n4 - "
            "sort connected components \n5 - quit")
        choice = input()
        if choice == "1":
            try:
                print("Please enter the name of the file you want to use (with a file extension): ")
                file_name = input()  # any string can be valid, so no validation needed
                img = intelligence.find_red_pixels(file_name)
            except NameError:
                print("You have entered an invalid input.")
        elif choice == "2":
            try:
                print("Please enter the name of the file you want to use (with a file extension): ")
                file_name = input()
                img = intelligence.find_cyan_pixels(file_name)
            except NameError:
                print("You have entered an invalid input.")
        elif choice == "3":
            print("Using the current loaded file from find red or cyan pixels... \n")
            try:
                intelligence.detect_connected_components(img)
            except:
                print("There is a problem. Have you loaded an image from find red or cyan pixels? \nNOT COMPLETED")
        elif choice == "4":
            try:
                intelligence.detect_connected_components_sorted(intelligence.detect_connected_components(img))
            except:
                print("There is a problem. Have you loaded an image from find red or cyan pixels? \nNOT COMPLETED")
        elif choice == "5":
            quitting = True
        else:
            print("Please enter a valid input.")
    return print("Returning to main menu.")


def about():
    """
    prints candidate number and module code

    """
    print("ECM1400, Candidate Number: 230519 ")


def quit():
    """allows the user to quit the program and displays a message
    """
    print("Thank you for using the program! :)")


if __name__ == '__main__':
    main_menu()
