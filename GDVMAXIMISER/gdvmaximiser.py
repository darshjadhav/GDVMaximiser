"""
Author: Darsh Jadhav
Title: GDV Maximiser
Description: A program to find the best possible combinations of properties within a given area
Version: 1.0
"""

from collections import Counter
import copy
import pandas as pd

# Simple data collection from user input
def data_collection():

    print("Input Total Area (Square Meters):>")
    areasqm = int(input())  # Target Number

    print("How many different types of properties (Different Area Sizes Possible):>")
    possibleDifferentBeds = int(input())  # For inputting extra data (no limit on different properties)

    propertysqm = [0] * possibleDifferentBeds  # Area of each property, used in algorithm
    noOfBeds = [0] * possibleDifferentBeds  # For identification of answer at the end (e.g. 2 1-beds, 1 2-beds, etc...)
    estgdv = [0] * possibleDifferentBeds  # Used to calculate gdv for each combination
    for i in range(len(propertysqm)):
        print("Number of Beds for Property %d :>" % (i + 1))
        noOfBeds[i] = int(input())
        print("Square Meters of Property %d :>" % (i + 1))
        propertysqm[i] = int(input())
        print("Estimated GDV of Property %d (£):>" % (i + 1))
        estgdv[i] = int(input())



    print("\n\nData Summary")
    print("---------------------------------------------")
    print("Total Area of Site (Square Meters): %d sqm" % areasqm)
    print("Number of Different Types of Properties: %d" % possibleDifferentBeds)
    for i in range(len(noOfBeds)):
        print("Area of %d-Bed Property: %d sqm" % (noOfBeds[i], propertysqm[i]))
        print("GDV of %d-Bed Property: £%d \n" % (noOfBeds[i], estgdv[i]))

    print("---------------------------------------------\n\n")

    return areasqm, possibleDifferentBeds, propertysqm, noOfBeds, estgdv


def testdata():

    areasqm = 1000
    possibleDifferentBeds = 2
    propertysqm = [41, 65]
    noOfBeds = [1, 2]
    estgdv = [200000, 240000]

    return areasqm, possibleDifferentBeds, propertysqm, noOfBeds, estgdv


# Removes duplicates from list in list
def remove_dupes(lst):
    return ([list(i) for i in {*[tuple(sorted(i)) for i in lst]}])


# Recursive Coin change algorithm for obtaining all combinations
def gdv_alg(areasqm, propertysqm):
    if areasqm < 0:
        return []
    # Create list in list if (areasqm - prev_property = 0)
    if areasqm == 0:
        return [[]]
    all_combinations = []

    for prev_property in propertysqm:
        combinations = gdv_alg(areasqm - prev_property, propertysqm)
        # Adds the previous property to the final larger list (list in list is formed)
        for c in combinations:
            c.append(prev_property)
            all_combinations.append(c)

    return remove_dupes(all_combinations)




# If no solution was found for the initial area provided, minus 1sqm to area and recalculate to find solution
def gdv_fail(combination_list, areasqm, propertysqm):
    empty = True
    temp_areasqm = copy.deepcopy(areasqm)
    areatracker = [temp_areasqm]
    while empty:
        if len(combination_list) < 10:
            temp_areasqm -= 1
            precheck = len(combination_list)
            combination_list.extend(gdv_alg(temp_areasqm, propertysqm))
            postcheck = len(combination_list)
            if precheck < postcheck:
                areatracker.append(temp_areasqm)

        elif len(combination_list) >= 10:
            print("SOLUTION FOUND FOR AREAS (sqm):")
            for i in range(len(areatracker)):
                print("%d sqm" % areatracker[i])
            empty = False

    return remove_dupes(combination_list)



# Retrieves index of property from the combinations (from gdv_alg() / gdv_fail() functions)
def indexing(all_combinations, propertysqm):
    storeind = all_combinations.copy()

    for i in range(len(all_combinations)):
        for j in range(len(all_combinations[i])):
            for k in range(len(propertysqm)):
                if (all_combinations[i][j] == propertysqm[k]):
                    storeind[i][j] = propertysqm.index(propertysqm[k])

    return storeind



# Gives a breakdown of the combinations in an understandable format
def breakdown_combinations(storeind, noofbeds):
    breakdown_property = storeind.copy()

    counter_var = []
    counterkeys = []
    countervals = []

    for i in range(len(breakdown_property)):
        counter_var.append(Counter(breakdown_property[i]))

    for i in range(len(counter_var)):
        counterkeys.append(list(counter_var[i].keys()))
        countervals.append(list(counter_var[i].values()))

    maxlength = len(max(counterkeys,key=len))
    indexlenvar = list(range(0, maxlength))

    for i in range(len(counterkeys)):
        if len(counterkeys[i]) < maxlength:
            for k in range(len(indexlenvar)):
                if indexlenvar[k] not in counterkeys[i]:
                    counterkeys[i].append(indexlenvar[k])
                    countervals[i].append(indexlenvar[k])


    for i in range(len(counterkeys)):
        for j in range(len(counterkeys[i])):
            counterkeys[i][j] = noofbeds[counterkeys[i][j]]

    for i in range(len(counterkeys)):
        counterkeys[i], countervals[i] = zip(*sorted(zip(counterkeys[i], countervals[i])))

    counterkeys = [list(i) for i in counterkeys]
    countervals = [list(i) for i in countervals]


    return counterkeys, countervals



# Sums gdv of each combination of properties
def sum_gdv(storeind, estgdv):
    gdv_lst = storeind.copy()

    sumgdvlst = []

    for i in range(len(storeind)):
        for j in range(len(storeind[i])):
            gdv_lst[i][j] = estgdv[storeind[i][j]]

    for i in range(len(gdv_lst)):
        sumgdvlst.append(sum(gdv_lst[i][:]))

    return sumgdvlst

# Output Function
def dataset_conversion(counterkeys, countervals, sumgdvlist, ratioval, url):
    dataset = pd.DataFrame(data=list(zip(countervals, sumgdvlist, ratioval)), columns=["No. of Beds: " + str(counterkeys[0]), "GDV", "Ratio Split"])
    dataset["GDV"] = dataset["GDV"].map('£{:,.2f}'.format)
    dataset = dataset.sort_values(by=["GDV"], ascending=False)
    dataset.to_csv(url)
    return dataset




def main():
    test = False
    if not test:
        # Live Function
        areasqm, possibleDifferentBeds, propertysqm, noOfBeds, estgdv = data_collection()
    elif test:
        # Test Function
        areasqm, possibleDifferentBeds, propertysqm, noOfBeds, estgdv = testdata()

    combination_list = gdv_alg(areasqm, propertysqm)

    if len(combination_list) < 10:
        combination_list = gdv_fail(combination_list, areasqm, propertysqm)

    indexes = indexing(combination_list, propertysqm)

    counterkeys, countervals = breakdown_combinations(indexes, noOfBeds)

    sumgdvlist = sum_gdv(indexes, estgdv)
    ratioval = copy.deepcopy(countervals)

    for i in range(len(counterkeys)):
        print("Combination %d" % (i + 1))
        print("---------------------")
        for j in range(len(counterkeys[i])):
            print("Number of %d-Beds: %d" % (counterkeys[i][j], countervals[i][j]))
            ratioval[i][j] = round((countervals[i][j] / sum(countervals[i]))*100)
        print("---------------------")
        print("Estimated GDV: £%d" % sumgdvlist[i])
        print("Ratio Split: %s" % ratioval[i])
        print("---------------------\n")

    dataset = dataset_conversion(counterkeys, countervals, sumgdvlist, ratioval, "output.csv")

    print("DATASET")
    print(dataset)




if __name__ == "__main__":
    main()