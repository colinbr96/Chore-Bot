import datetime
import requests

CURRENT_GROUP_FILE = 'group.txt'
BOT_ID = '58ae5dfd7dfe0acde6da2340f2'

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
        
        if todaysGroup > 4:
            todaysGroup = 1

        save_group(todaysGroup)
        message = '{}, your chore for today is: the {}\n({})'.format(
        	groups[todaysGroup],
        	todaysChore,
        	now.strftime('%a, %b %d, %Y')
        )

        http_post(message)
        todaysGroup += 1
        print('POSTED: ' + message)


if __name__ == '__main__':
    run()
