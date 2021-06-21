import os
import csv


# get latest version of bot's role list
async def get_list():
    if (os.path.exists("roles.csv")):
        with open("roles.csv", newline='') as f:
            return list(csv.DictReader(f))
    else:
        print("No Roles list!")
        return