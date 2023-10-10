# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification

def sumvalues(values):
    """
    adds all values

    Args:
        values (list): values to add

    Returns:
        int: total value

    """
    total = 0
    for value in values:
        if (isinstance(value, int) or isinstance(value, float)) == False: # checks is an integer or a float
            raise Exception("Sorry, you can only sum numerical values")
        else:
            total += value
    return total


# print(sumvalues([1, 2, 3, 4, "a"])) -> testing


def maxvalue(values):
    """
    finds the maximum value

    Args:
        values (list): values to check to find the maximum value

    Returns:
        int: max value

    """
    current_max = 0
    for value in values:
        if (isinstance(value, int) or isinstance(value, float)) == False:  # checks that data is an integer or float
            raise Exception(
                "Sorry, you can only find the max of numerical values")
        else:
            if value > current_max: # checks if it is higher than the current maximum
                current_max = value
    return current_max


#print(maxvalue([1, 2023, 3843.4, 4, 45])) <- testing


def minvalue(values):
    """
    finds the minimum value

    Args:
        values (list): values to check to find the min value

    Returns:
        int: min value

    """
    current_min = values[0]
    for value in values:
        if (isinstance(value, int) or isinstance(value, float)) == False:
            raise Exception(
                "Sorry, you can only find the min of numerical values")
        else:
            if value < current_min:
                current_min = value
    return current_min


# print(minvalue([2, 2023, 3843.4, 4, 45])) <- testing


def meannvalue(values):
    """
        finds the average value

        Args:
            values (list): values to check to find the average

        Returns:
            int: average value

        """
    total = 0
    for value in values:
        if (isinstance(value, int) or isinstance(value, float)) == False:
            raise Exception(
                "Sorry, you can only find the average of numerical values")
        else:
            total += value
    average = total / len(values)  # uses mean formula
    return average


# print(meanvalue([1, 2, 3.5, 4, 5, "a", 7])) <- testing


def countvalue(values, xw):
    """
            finds how many of one value there are in a list

            Args:
                values (list): values to search

            Returns:
                int: number of values there are present in the list

            """
    instances = 0
    for value in values:
        if (isinstance(value, int) or isinstance(value, float)) == False:
            raise Exception(
                "Sorry, you can only find numerical values, or your list contains a non-numerical value")
        else:
            if value == xw:
                instances += 1
    return instances


# print(countvalue([1, 7, 3.5, 7, 5, 7], 7)) <- testing
