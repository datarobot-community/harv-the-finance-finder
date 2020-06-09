# Script to generate fake but realistic ESG category data that we'll use for training


import random
import csv

# Faking our data for esg distributions per sector ([0] - mean value, [1] - standard deviation)
sector_esg_distributions = { 
    "Electronic Technology": (27, 13),
    "Distribution Services": (30, 4),
    "Health Technology": (24, 2),
    "Commercial Services": (28, 6),
    "Industrial Services": (33, 8),
    "Finance": (25, 7),
    "Process Industries": (46,10),
    "Transportation": (30, 4),
    "Technology Services": (18, 2),
    "Producer Manufacturing": (32, 8),
    "Retail Trade": (19, 6),
    "Consumer Services": (20, 3),
    "Non-Energy Minerals": (26, 5),
    "Utilities": (30, 10),
    "Health Services": (24, 2),
    "Consumer Durables": (26, 5),
    "Consumer Non-Durables": (23, 7),
    "Communications": (20, 2),
    "Energy Minerals": (32, 6),
    "Government": (25, 5)
}

training_rows = [] # We're returning this

# Open all quotes
with open('data/stock_quotes_all.csv', newline='') as csvfile:

    csvReader = csv.reader(csvfile)    

    header = next(csvReader, None) # first line is the header
    header.append('esg_category') 
    training_rows.append(header)

    for row in csvReader:
        if random.randint(0,9) < 9: # skip 9/10 rows
            continue

        else:
            sector = row[20]
            if sector is None: # just in case of bad data
                esg_distribution = sector_esg_distributions[sector]
                esg_score = round(random.gauss(esg_distribution[0], esg_distribution[1]))
                esg_category = 1 if esg_score <= 18 else 2 if esg_score <= 27 else 3 if esg_score <= 36 else 4

                row.append(esg_category)
                training_rows.append(row)

            else: 
                continue

# Write the contents
with open('data/stock_quotes_esg_train.csv', mode='w', newline='') as outCsv:
    csvWriter = csv.writer(outCsv)
    csvWriter.writerows(training_rows)
