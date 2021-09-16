import os
import csv
import text2emotion as te

async def get_list():
    if (os.path.exists("socialcredit.csv")):
        with open("socialcredit.csv", newline='') as f:
            return list(csv.DictReader(f))
    else:
        print("No Roles list!")
        return

async def is_tracked(serverid, memberid):
    roles = await get_list()
    for row in roles:
        if (int(row['SERVER_ID']) == serverid):
            if (int(row['ROLE_ID']) == memberid):
                return True
    return False

def process_text(text):
    emotion = te.get_emotion(text)
    neg = emotion['Angry'] + emotion['Fear'] + emotion['Sad'] / 3
    pos = emotion['Surprise'] + emotion['Happy'] / 2
    print(f"Avg Negative: {neg}")
    print(f"Avg Positive: {pos}")
    if(neg > pos):
        decrease_credit(neg)
    if(pos > neg):
        increase_credit(pos)

while(1):
    val = input("Sentence")
    process_text(val)