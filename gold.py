import csv
from os import close


def delete_row(mid):
    data = list()
    with open("gold.csv", "r") as f:
        reader = csv.reader(f)
        for r in reader:
            # print(r[0], ",", str(mid))
            if(r[0] != str(mid)):
                print(list(r))
                data.append(r)

    with open("gold.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)
            

delete_row(123)

# with open('gold.csv', 'a', newline='') as f:
#     fn = ['MESSAGE_ID', "BOARD_ID"]
#     writer = csv.DictWriter(f, fieldnames=fn)

#     writer.writerow({'MESSAGE_ID': '283490', 'BOARD_ID': '21900'})
#     f.close()

# with open('gold.csv', newline='') as f:
#     gold_board = list(csv.DictReader(f))
    
#     # print(list(gold_board))
#     for row in gold_board:
#         # print(row['MESSAGE_ID'], row['BOARD_ID'])
#         # print(list(row)):
#         print(row['MESSAGE_ID'])
#     f.close()