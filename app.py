# John Byron Garin
# 2021-02658

import csv
import math
from statistics import mean

def readCSVFile():
    # 2D array to store the data
    training_data = []

    with open('diabetes.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        
        # Iterate through each row in the CSV file
        for row in csvreader:
            # Convert the row into a list of numbers
            numbers = [float(value) for value in row]
            training_data.append(numbers)

    return training_data

def readInputFile():
    # 2D array to store the data
    input_data = []

    with open('input.in', 'r') as infile:
        # Iterate through each line in the file
        for line in infile:
            numbers = [float(value) for value in line.strip().split(',')]
            input_data.append(numbers)

    return input_data

def getDistance(input_data, training_data, k):
    # input_data = [ 
    #                 [3.0, 70.0, 34.0, 31.0, 77.0, 31.0, 0.59, 24.0],
    #                 [4.0, 135.0, 91.0, 0.0, 33.0, 34.6, 0.19, 25.0]
    #             ]

    # training_data = [
    #                 [6.0, 148.0, 72.0, 35.0, 0.0, 33.6, 0.627, 50.0, 1.0],
    #                 [1.0, 85.0, 66.0, 29.0, 0.0, 26.6, 0.351, 31.0, 0.0]
    #                 ]

    array_of_distance = []

    # Iterate through each input data array
    for input_array in input_data:
        distances = []
        
        # Iterate through each training data array
        for training_array in training_data:
            distances_with_classification = []
            distance = 0.0
            
            # Calculate the distance for each element (excluding the last element)
            for xi, vi in zip(input_array, training_array[:-1]):
                distance += (xi - vi) ** 2
            
            # Calculate the square root of the summation
            distance = math.sqrt(distance)
            
            distances_with_classification.append(distance)
            distances_with_classification.append(training_array[-1])     
               
            distances.append(distances_with_classification)
    
        array_of_distance.append(distances)
    

    # Sort the first elements of each sub-array and take the first k values
    sorted_array = [sorted(sub_array, key=lambda x: x[0])[:k] for sub_array in array_of_distance]
    
    return sorted_array

def classify(sorted_distance):
    # sorted_distance = [
    #     [[21.1215, 2.0], [22.0778, 2.0], [22.9674, 2.0], [31.1504, 0.0], [31.3804, 0.0], [28, 0.0]],
    #     [[34.3302, 0.0], [34.4718, 1.0], [35.0081, 0.0], [35.0322, 0.0], [35.5045, 1.0], [29, 0.0]],
    #     [[9.2286, 0.0], [9.8871, 1.0], [12.5231, 0.0], [12.9201, 0.0], [14.68, 0.0], [30, 0.0]],
    #     [[27.4088, 0.0], [28.5526, 1.0], [29.3175, 1.0], [30.6643, 1.0], [37.8418, 1.0], [31, 0.0]],
    #     [[8.1737, 0.0], [12.9805, 0.0], [13.0245, 0.0], [18.0624, 0.0], [18.5844, 1.0], [32, 0.0]],
    #     [[8.0937, 1.0], [13.6853, 2.0], [14.4423, 2.0], [14.5874, 1.0], [14.7641, 1.0], [33, 0.0]],
    #     [[15.257, 2.0], [20.8051, 2.0], [25.2113, 1.0], [27.3521, 1.0], [34.1725, 0.0], [34, 0.0]]
    # ]
    classification = []
    for sub_array in sorted_distance:
        # initializes 3 dictionaries that will be needed
        occurrences_array_version = {}
        occurrences_length_version = {}
        occurrences_average_version = {}
        for item in sub_array:
            second_element = item[1]
            if second_element not in occurrences_array_version:
                occurrences_average_version[second_element] = 0
                occurrences_array_version[second_element] = []
                occurrences_length_version[second_element] = 0
            occurrences_array_version[second_element].append(item[0]) 
            occurrences_length_version[second_element] = len(occurrences_array_version[second_element])
        
        print("Array version:")
        print(occurrences_array_version)
        print("Length version:")
        print(occurrences_length_version)

        max_value = max(occurrences_length_version.values())
        print("Maximum length:", max_value)
        
        key_values = []
        for classify in occurrences_length_version:
            if occurrences_length_version[classify] == max_value:
                key_values.append(classify)
        print("Key values containing max length:", key_values)

        if len(key_values) == 1: # no tie breaker
            print("No Tiebreaker")
            larger_len = 0
            larger_classify = 0
            for classify in occurrences_array_version:
                if(len(occurrences_array_version[classify]) > larger_len):
                    larger_len = len(occurrences_array_version[classify])
                    larger_classify = classify
            print("Classify: ", larger_classify)
            classification.append(larger_classify)
        else:
            print("With Tiebreaker")
            for classify in key_values:
                ave = mean(occurrences_array_version[classify])  # Calculate the mean using the mean function
                occurrences_average_version[classify] = ave
                print("Average:", ave)
            chosen_average = min(occurrences_average_version.values())
            print("Chosen Average:", chosen_average)

            for classify in occurrences_average_version:
                if occurrences_average_version[classify] == chosen_average:
                    print("Classify: ", classify)
                    classification.append(classify)
                    break
        print("\n")
    return classification

def writeOutputToFile(input_data, classification):
    with open('output.txt', 'w') as outfile:
        for input in input_data:
            output_line = ",".join(map(str, input))  # Convert the list to a space-separated string
            outfile.write(output_line + '\n')  # Write the line to the output file

k = 5

training_data = readCSVFile()
input_data = readInputFile()

print()
print("k lowest Distance: ")
sorted_distance = getDistance(input_data, training_data, k)
for d in sorted_distance:
    print(d)
print()

classification = classify(sorted_distance)
print("Classification:")
print(classification)
print()

print("Final Output")
counter = 0
for input in input_data:
    input.append(classification[counter])
    print(input)
    counter += 1

writeOutputToFile(input_data, classification)