def is_float_convertible(value):
    try:
        float(value)
        return True
    except ValueError:
        print(f"Wrong float converting {value}")
        return False
def char_distance(string, char1, char2):
    try:
        index_char1 = string.index(char1)
        index_char2 = string.index(char2)
        distance = abs(index_char1 - index_char2)
        return distance
    except ValueError:
        return "One or both characters not found in the string."
    
def getFormatted(float_val):
    #formatted_string = "{:,}".format(int(float_val))
    formatted_string = str(int(float_val))
    #print(f"formatted_string: {formatted_string}")
    return formatted_string


