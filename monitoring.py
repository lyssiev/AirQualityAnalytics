# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification.
#
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations.
#
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
import requests
import datetime
from matplotlib import pyplot as mat_plot
import json


def get_live_data_from_api(site_code='MY1', species_code='NO', start_date=None, end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 

    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + \
               datetime.timedelta(days=1) if end_date is None else end_date

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"



    url = endpoint.format(
        site_code=site_code,
        species_code=species_code,
        start_date=start_date,
        end_date=end_date
    )

    res = requests.get(url)
    return res.json()


def get_group_codes():
    """
    returns a dictionary of possible group codes in the form of a .json file

    Returns:
        (file): returns a .json file which contains the response from the API

    """
    get_groups_endpoint = "https://api.erg.ic.ac.uk/AirQuality/Information/Groups/Json"
    grps_resp = requests.get(get_groups_endpoint)

    return print(grps_resp.json())


def get_site_codes(group_name):
    """returns a list of the possible group names from the LondonAir API

    Args:
        group_name (string): the name of the group the user is requesting the site codes for. used to specify in the URL

    Returns:
        list: returns a list of the possible site codes, as well as storing them in a .txt file
    """

    get_sitecodes_endpoint = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName={group}/Json"
    url = get_sitecodes_endpoint.format(group=group_name)
    result = str(requests.get(url).json())
    result = result.split("'")

    site_name = []
    site_code = []

    for i in range(len(result) - 1):  # splits every item in dictionary
        if result[i] == "@SiteCode":
            site_code.append(result[i + 2])  # adds to array of site codes
        elif result[i] == "@SiteName":
            site_name.append(result[i + 2])  # adds to array of site names

    string_for_file = ""
    for j in range(len(site_name)):  # loops through for the amount of site names there are
        string_for_file += site_name[j] + "," + site_code[j] + " \n"

    return string_for_file


def average_api():
    """
    allows the user to request the average amount of a pollutant between two specified dates. If the dates are not
    specified, then it will use the current date.

    Returns:
        (int): average of specified items

    """
    site_code = ""
    species_code = ""
    start_date = ""
    end_date = ""

    # user inputs
    try:
        print("Please enter the site code you want to use: ")
        site_code = input()
        print("Please enter the pollutant you want to monitor: ")
        species_code = input()
        print("Please enter the start date: ")
        start_date = input()
        print("Please enter the end date: ")
        end_date = input()
    except NameError:
        print("You have entered an invalid input.")

    data = get_live_data_from_api(site_code, species_code, start_date, end_date)  # retrieves data

    pollutant_data = data["RawAQData"]["Data"]
    pollutant_array = []
    number_of_values = 0
    for item in pollutant_data:
        if item["@Value"] != "":  # checks item is not null
            number_of_values += 1
            pollutant_array.append(item["@Value"])

    total = 0
    for item in pollutant_array:  # adds up all items in the array
        total += float(item)

    average = total / number_of_values  # uses mean formula
    return average


# average_api()


def create_graph(*args, **kwargs):
    try:
        print("Please enter the site code you want to use: ")
        site_code = input()
        print("Please enter the pollutant you want to monitor: ")
        species_code = input()
        print("Please enter the start date: ")
        start_date = input()
        print("Please enter the end date: ")
        end_date = input()
    except NameError:
        print("You have entered an invalid input.")

    data = get_live_data_from_api(site_code, species_code, start_date, end_date)  # retrieves data
    pollutant_data = data["RawAQData"]["Data"]
    pollutant_array = []
    date_array = []

    # adds dates and times to arrays
    for item in pollutant_data:
        if item["@Value"] != "":  # checks item is not null
            pollutant_array.append(float(item["@Value"]))
        date_array.append(item["@MeasurementDateGMT"])

    mat_plot.plot(date_array, pollutant_array)  # creates graph

    # names axis
    mat_plot.xlabel("x - Date")
    mat_plot.ylabel("y - " + str(species_code))

    mat_plot.title("Graph of " + str(species_code) + " over time")  # names title
    mat_plot.savefig('graph.png')  # saves as png
    mat_plot.show()

