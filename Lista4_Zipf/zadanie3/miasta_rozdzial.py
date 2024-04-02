# Załadowanie danych do słownika w celu rozdziału danych o miastach w Polsce zaczerpniętych z Wikipedii.
data = 'dane_wikipedia.txt'
output = 'miasta.txt'
# Read data from the input file
with open(data, 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

# Process the data to extract city names and populations
cities_population = [line.split("\t") for line in lines]
output_lines = [f"{city[0]} {city[4]}\n" for city in cities_population if len(city) > 4]

# Write the processed data to the output file
with open(output, "w", encoding='utf-8') as output_file:
    output_file.writelines(output_lines)

output
