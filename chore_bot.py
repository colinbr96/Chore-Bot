# ----------------------------------------------------------------------------- IMPORTS

import datetime
import requests # http://docs.python-requests.org/

# ----------------------------------------------------------------------------- DATA & CONSTANTS

CONFIG_FILE = 'config.ini'
CHORE_BOT = ''
NOTIFIER_BOT = ''
CURRENT_GROUP = 0

# Chore Schedule
chores = {
    'Monday':   'Living Room & Dining Room',
    'Tuesday':  'Kitchen',
    'Wednesday':    'Bathroom & Outside Garbage',
    'Thursday': 'Kitchen',
    'Friday':   'Hallway & Backyard',
}

# Roommate Groups
groups = [
    'Aaron & Rachel',
    'Colin & Jasper',
    'Christina & Rod',
    'Georgina & Luis'
]

# ----------------------------------------------------------------------------- FUNCTIONS

# Returns the contents of CONFIG_FILE as a dict
def load_config_data():
    global CHORE_BOT, NOTIFIER_BOT, CURRENT_GROUP

    file = open(CONFIG_FILE, 'r')
    lines = file.readlines()
    data = dict()
    for l in lines:
        key, value = l.strip().split(' = ')
        data[key] = value
    
    CURRENT_GROUP = int(data['group'])
    if CURRENT_GROUP > 4:
        CURRENT_GROUP = 1
    CHORE_BOT = data['chore_bot']
    NOTIFIER_BOT = data['notifier_bot']


def save_config_data():
    file = open(CONFIG_FILE, 'w')
    file.writelines([
        'group = {}\n'.format(CURRENT_GROUP),
        'chore_bot = {}\n'.format(CHORE_BOT),
        'notifier_bot = {}'.format(NOTIFIER_BOT)
    ])

# Performs an HTTP Post request to GroupMe
def bot_post(text, bot_ID):
    r = requests.post('https://api.groupme.com/v3/bots/post', data = {
        'bot_id': bot_ID,
        'text': text
    })
    print(text)

# Builds and posts the chore reminder
def chore_notify(date):
    global CURRENT_GROUP

    todays_chore = chores[date.strftime('%A')]
    message = '{}, your chore for today is: the {}\n({})'.format(
        groups[CURRENT_GROUP-1],
        todays_chore,
        date.strftime('%a, %b %d, %Y')
    )

    bot_post(message, CHORE_BOT)
    bot_post('Chore-Bot posted.', NOTIFIER_BOT)

    CURRENT_GROUP += 1
    save_config_data()

# Runs a chore reminder if weekday
def run():
    load_config_data()

    now = datetime.datetime.now()
    if now.weekday() >= 5: # If it is a weekend
        bot_post('Chore-Bot aborted post: Weekend.', NOTIFIER_BOT)
    else:
        chore_notify(now)

# ----------------------------------------------------------------------------- EXECUTION

if __name__ == '__main__':
    run()