##############################
# Filter functions for dataframes
##############################

def cameos(x, codes):
    try:
        return codes['Description'][x]
    except:
        return "No Description returned for CAMEO code {0}".format(x)
