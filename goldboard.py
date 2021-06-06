import os
import csv

# get latest version of bot's board list
async def get_list():
    if(os.path.exists("gold.csv")):
        with open("gold.csv", newline='') as f:
            # gold_board = list(csv.reader(f, delimiter=" ", quotechar="|"))
            return list(csv.DictReader(f))

# check if message is already on board
async def check_board(id):
    gold_board = await get_list()
    for row in gold_board:
        if(int(row['MESSAGE_ID']) == id):
            return row['BOARD_ID']
    return None

# delete row matching message id
async def delete_row(mid):
    data = list()
    with open("gold.csv", "r") as f:
        reader = csv.reader(f)
        for r in reader:
            if(r[0] != str(mid)):
                data.append(r)

    with open("gold.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)

# add message and board ids to list
async def add_row(m, b):
    with open("gold.csv", "a", newline='') as f:
        fn = ['MESSAGE_ID', 'BOARD_ID']
        writer = csv.DictWriter(f, fieldnames=fn)

        writer.writerow({'MESSAGE_ID': m, 'BOARD_ID': b})

