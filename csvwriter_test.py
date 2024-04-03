import csv
def write_to_csv(data):
    with open("results.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

data = [1,2,3,4,5]
write_to_csv(data)      