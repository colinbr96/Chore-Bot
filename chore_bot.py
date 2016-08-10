import datetime
import requests

CURRENT_GROUP_FILE = 'group.txt'
BOT_ID = 'e7cd7c4d3448e2eadcd0dca190'

chores = {
    'Monday':   'Living Room & Dining Room',
    'Tuesday':  'Kitchen',
    'Wednesday':    'Bathroom & Outside Garbage',
    'Thursday': 'Kitchen',
    'Friday':   'Hallway & Backyard',
    'Saturday': '',
    'Sunday':   ''
}

groups = [
    'Aaron & Rachel',
    'Colin & Jasper',
    'Christina & Rod',
    'Georgina & Luis'
]

def load_group() -> int:
    file = open(CURRENT_GROUP_FILE, 'r')
    group_num = file.read()
    return int(group_num)

def save_group(group_num):
    file = open(CURRENT_GROUP_FILE, 'w')
    file.write(str(group_num))

def http_post(text):
    r = requests.post('https://api.groupme.com/v3/bots/post', data = {
        'bot_id': BOT_ID,
        'text': text
    })

def run():
    todaysGroup = load_group()

    now = datetime.datetime.now()
    todaysChore = chores[now.strftime('%A')]
    
    if todaysChore != '':
        todaysGroup += 1
        if todaysGroup > 4:
            todaysGroup = 1

        save_group(todaysGroup)
        message = '{}, your chore for today is: the {}'.format(groups[todaysGroup-1], todaysChore)
        http_post(message)
        print('Bot posted to GroupMe: ' + message)


if __name__ == '__main__':
    run()
