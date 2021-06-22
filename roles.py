import os
import csv

# get latest version of bot's board list
async def get_list():
    if (os.path.exists("roles.csv")):
        with open("roles.csv", newline='') as f:
            return list(csv.DictReader(f))
    else:
        print("No Roles list!")
        return


# check if role is assignable
async def is_assignable(id):
    roles = await get_list()
    for row in roles:
        # print(row)
        if (int(row['ROLE_ID']) == id):
            return True
    return None


# delete row matching message id
async def delete_row(ctx, role):
    data = list()
    with open("roles.csv", "r") as f:
        reader = csv.reader(f)
        for r in reader:
            if (r[1] != str(role.id)):
                data.append(r)

    with open("roles.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)


# add message and board ids to list
async def add_row(m, r):
    with open("roles.csv", "a", newline='') as f:
        fn = ['SERVER_ID', 'ROLE_ID', 'ROLE_NAME']
        writer = csv.DictWriter(f, fieldnames=fn)

        writer.writerow({
            'SERVER_ID': m.guild.id,
            'ROLE_ID': r.id,
            'ROLE_NAME': r.name,
        })


async def get_assignable_roles():
    role_list = list()
    if (os.path.exists("roles.csv")):
        with open("roles.csv", newline='') as f:
            return list(csv.DictReader(f))
    else:
        print("No Roles list!")
        return