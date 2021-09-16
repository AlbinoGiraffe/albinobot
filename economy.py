import os
import csv
import shutil
import tempfile
import pandas as pd
from pandas.io.parsers.readers import MANDATORY_DIALECT_ATTRS
import text2emotion as te
from tempfile import NamedTemporaryFile

# get user credit list
async def get_list():
    if (os.path.exists("socialcredit.csv")):
        with open("socialcredit.csv", newline='') as f:
            return list(csv.DictReader(f))
    else:
        print("No socialcredit list!")
        return

# check if user is being tracked
async def is_tracked(serverid, memberid):
    roles = await get_list()
    for row in roles:
        if (int(row['SERVER_ID']) == serverid):
            if (int(row['MEMBER_ID']) == memberid):
                return True
    return False

# stop tracking a user
async def delete_row(sid, mid):
    ind = -1
    df = pd.read_csv("socialcredit.csv")
    for index in df.index:
        if(df.loc[index, 'SERVER_ID'] == sid and df.loc[index, 'MEMBER_ID'] == mid):
            ind = index
    if(ind < 0):
        return

    df.drop(ind, axis=0, inplace=True)
    df.to_csv("socialcredit.csv", index=False)

# start tracking a user
async def add_row(sid, mid, cred):
    with open("socialcredit.csv", "a", newline='') as f:
        fn = ['SERVER_ID', 'MEMBER_ID', 'CREDIT']
        writer = csv.DictWriter(f, fieldnames=fn)

        writer.writerow({
            'SERVER_ID': sid,
            'MEMBER_ID': mid,
            'CREDIT': cred,
        })

# update users credits
async def update_cred(sid, mid, cred):
    ind = -1
    df = pd.read_csv("socialcredit.csv")
    for index in df.index:
        if(df.loc[index, 'SERVER_ID'] == sid and df.loc[index, 'MEMBER_ID'] == mid):
            ind = index
    if(ind < 0):
        return

    df.loc[ind, 'CREDIT'] = df.loc[ind, 'CREDIT'] + cred
    df.to_csv("socialcredit.csv", index=False)

# return users credits
async def get_cred(sid, mid):
    ind = -1
    df = pd.read_csv("socialcredit.csv")
    for index in df.index:
        if(df.loc[index, 'SERVER_ID'] == sid and df.loc[index, 'MEMBER_ID'] == mid):
            ind = index

    return df.loc[ind, 'CREDIT']

async def process_text(text):
    emotion = te.get_emotion(text)
    neg = emotion['Angry'] + emotion['Fear'] + emotion['Sad'] / 3
    pos = emotion['Surprise'] + emotion['Happy'] / 2
    # print(f"Avg Negative: {neg}")
    # print(f"Avg Positive: {pos}")
    return [neg, pos]

async def get_user_list(sid):
    scores = []
    df = pd.read_csv("socialcredit.csv")
    for index in df.index:
        if(df.loc[index, 'SERVER_ID'] == sid):
            scores.append([df.loc[index, 'MEMBER_ID'], df.loc[index, 'CREDIT']])
    return scores
            

