import csv


def main():
    filename = 'google.csv'

    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        cnt = 0

        for row in reader:
            print("{} : {}".format(row['Name'], row['Phone 1 - Value']))
            cnt += 1

        print("cnt: {}", cnt)


if __name__ == '__main__':
    main()