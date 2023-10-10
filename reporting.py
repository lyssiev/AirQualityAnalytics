# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
import numpy as np
from datetime import datetime


def daily_average(data, monitoring_station, pollutant):
    """calculates the daily average of pollutants in a specific monitoring station

    Args:
        data (dict): contains a dictionary of lists that stores all the values in the files
        monitoring_station (string): name of the monitoring station the user is processing data about
        pollutant (string): name of the pollutant the user is processing data about

    Returns:
        list: returns a list of the daily average values
    """

    # returns a list that contains all values of the specified pollutant from the monitoring station
    pollutant_values = data[monitoring_station][pollutant]
    averages = []
    current_averages = []
    counter = 0  # counts the hours of the day
    for value in pollutant_values:  # loops through each value
        if counter == 24:  # checks if all hours of the day have been found
            if len(current_averages) == 0:
                averages.append(0)  # if the list is empty, the average is 0
            else:
                mean = sum(current_averages) / len(current_averages)  # calculate the average
                averages.append(mean)  # adds to list
                counter = 0  # gets added to after
                current_averages = []

        # checks after as the "pollutant_data" has already been fetched
        if counter < 24 and value != "No data":  # checks if there are still hours that have not been added to the array
            current_averages.append(float(value))

        counter += 1

    # adds last value
    if len(current_averages) == 0:
        averages.append(0)
    else:
        mean = sum(current_averages) / len(current_averages)
        averages.append(mean)

    return averages


# testing
# print(daily_average(1, "Harlington", "pm25"))


def daily_median(data, monitoring_station, pollutant):
    """returns a list with the daily median values for a particular pollutant and monitoring station

    Args:
        data (dict): contains a dictionary of lists that stores all the values in the files
        monitoring_station (string): name of the monitoring station the user is processing data about
        pollutant (string): name of the pollutant the user is processing data about

    Returns:
        list: returns a list of the daily median values
    """
    station_values = data[monitoring_station]
    pollutant_values = station_values[pollutant]
    medians = []
    temp_medians = []
    counter = 0
    for pollutant_data in pollutant_values:  # loops through pollutant values
        if counter == 24:
            # calculate the median using numpy
            if len(temp_medians) == 0:  # if the array is empty, the median value is 0
                medians.append(0)
            else:
                # calculates median then adds to array
                medians.append(np.median(temp_medians))
                counter = 0
                temp_medians = []

        # checks after as the "pollutant_data" has already been fetched
        if (counter < 24) and pollutant_data != "No data":  # check which hour the data comes from
            temp_medians.append(float(pollutant_data))
        counter += 1

    # add last value
    if len(temp_medians) == 0:
        medians.append(0)
    else:
        medians.append(np.median(temp_medians))

    return medians


# testing


def hourly_average(data, monitoring_station, pollutant):
    """Calculating the hourly average for a particular pollutant in a particular monitoring station

    Args:
        data (dict): contains a dictionary of lists that stores all the values in the files
        monitoring_station (string): name of the monitoring station the user is processing data about
        pollutant (string): name of the pollutant the user is processing data about

    Returns:
        list: returns a list of the hourly average values
    """
    # using a map function to divide each hour in the array
    averages = []
    pollutant_values = data[monitoring_station][pollutant]
    hours = {}

    # populate the dictionary
    for i in range(24):
        hours[i] = []

    # add values to correspoding values in the dictionary
    counter = 0
    for value in pollutant_values:
        if value != "No data":
            hours[counter].append(float(value))
        counter += 1
        if counter == 24:
            counter = 0

    # averaging every hour and adding it to a list
    for key in hours:
        mean = sum(hours[key]) / len(hours[key])
        averages.append(mean)

    return averages


def monthly_average(data, monitoring_station, pollutant):
    """returns a list with the monthly average values for a particular pollutant and monitoring station

    Args:
        data (dict): contains a dictionary of lists that stores all the values in the files
        monitoring_station (string): name of the monitoring station the user is processing data about
        pollutant (string): name of the pollutant the user is processing data about

    Returns:
        list: returns a list of the monthly average values
    """

    station_values = data[monitoring_station]
    pollutant_values = station_values[pollutant]
    averages = []
    old_dates = station_values["date"]
    dates = []
    for x in old_dates:
        dates.append(datetime.strptime(x, "%Y-%m-%d"))
    counter = 0
    current_month = 0
    months = {}

    # populate the dictionary
    for i in range(12):
        months[i] = []

    # add all values to dictionary according to month
    current_date = dates[0]
    for value in dates:
        if current_date.month != value.month:
            current_month += 1
        if pollutant_values[counter] != "No data":
            months[current_month].append(float(pollutant_values[counter]))

        counter += 1
        current_date = value

    for key in months:
        mean = sum(months[key]) / len(months[key])
        averages.append(mean)

    return averages


def peak_hour_date(data, date, monitoring_station, pollutant):
    """Finds the hour of the day with the highest pollution level and its corresponding value

    Args:
        data (dict): contains a dictionary of lists that stores all the values in the files
        date (string): date the user wants to check 
        monitoring_station (string): name of the monitoring station the user is processing data about
        pollutant (string): name of the pollutant the user is processing data about

    Returns:
        int: hour with the highest pollution level 
    """
    station_values = data[monitoring_station]
    dates = station_values["date"]
    pollutant_values = station_values[pollutant]
    current_hour_data = []
    counter = 0

    for value in dates:
        if value == date:
            if pollutant_values[counter] != "No data":
                current_hour_data.append(float(pollutant_values[counter]))

        counter += 1

    if len(current_hour_data) == 0:
        return []
    else:
        return (max(current_hour_data))


def count_missing_data(data,  monitoring_station, pollutant):
    """returns the number of "No data" entries are there in the data

    Args:
        data (dict): contains a dictionary of lists that stores all the values in the files
        monitoring_station (string): name of the monitoring station the user is processing data about
        pollutant (string): name of the pollutant the user is processing data about

    Returns:
        int: number of "No data" values
    """
    pollutant_values = data[monitoring_station][pollutant]  # returns the list of user-specified pollutant values
    counter = 0
    for value in pollutant_values:  # loops through every value in the pollutants
        if value == "No data":
            counter += 1

    return counter


def fill_missing_data(data, new_value,  monitoring_station, pollutant):
    """fills missing data entries with user specified inputs

    Args:
        data (dict): contains a dictionary of lists that stores all the values in the files
        monitoring_station (string): name of the monitoring station the user is processing data about
        pollutant (string): name of the pollutant the user is processing data about
        new_value (any): user specified value to change empty data values to


    Returns:
        list: list of data with missing values replaced
    """
    pollutant_values = data[monitoring_station][pollutant]
    counter = 0
    for value in pollutant_values:  # loops through every value in the pollutants
        if value == "No data":
            pollutant_values[counter] = new_value
        counter += 1

    return pollutant_values  # ásk sylvie if its the whole dict not just pollutant values
