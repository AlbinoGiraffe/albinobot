import os
import csv

# get latest version of bot's board list
async def get_list():
    if(os.path.exists("stars.csv")):
        with open("stars.csv", newline='') as f:
            return list(csv.DictReader(f))

# check if message is already on board
async def check_board(id):
    star_board = await get_list()
    for row in star_board:
        if(int(row['MESSAGE_ID']) == id):
            return row['BOARD_ID']
    return None

# delete row matching message id
async def delete_row(mid):
    data = list()
    with open("stars.csv", "r") as f:
        reader = csv.reader(f)
        for r in reader:
            if(r[0] != str(mid)):
                data.append(r)

    with open("stars.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)

# add message and board ids to list
async def add_row(m, b, numStars):
    with open("stars.csv", "a", newline='') as f:
        fn = ['MESSAGE_ID', 'BOARD_ID', 'SERVER_ID', 'STAR_COUNT']
        writer = csv.DictWriter(f, fieldnames=fn)

        writer.writerow({'MESSAGE_ID': m.id, 'BOARD_ID': b.id, 'SERVER_ID': m.guild.id, 'STAR_COUNT': numStars})

