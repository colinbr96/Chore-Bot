# ----------------------------------------------------------------------------- IMPORTS

import datetime
import requests # http://docs.python-requests.org/
import yaml # http://pyyaml.org/

# ----------------------------------------------------------------------------- DATA & CONSTANTS

# Configuration
CONFIG_FILE = 'config.yaml'
CONFIG_DATA = dict()

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

# Loads the contents of config.yaml into CONFIG_DATA
def load_config_data():
    global CONFIG_DATA

    with open(CONFIG_FILE, 'r') as stream:
        try:
            CONFIG_DATA = yaml.load(stream)
        except yaml.YAMLError as err:
            print(err)

    if CONFIG_DATA['current_group'] > 4:
        CONFIG_DATA['current_group'] = 1

# Saves the contents of CONFIG_DATA to config.yaml
def save_config_data():
    with open(CONFIG_FILE, 'w') as ostream:
        yaml.dump(CONFIG_DATA, ostream, default_flow_style=False)

# Performs an HTTP Post request to GroupMe
def bot_post(text, bot_ID):
    r = requests.post('https://api.groupme.com/v3/bots/post', data = {
        'bot_id': bot_ID,
        'text': text
    })
    print(text)

# Builds and posts the chore reminder
def chore_notify(date):
    global CONFIG_DATA

    todays_chore = chores[date.strftime('%A')]
    message = '{}, your chore for today is: the {}\n({})'.format(
        groups[CONFIG_DATA['current_group']-1],
        todays_chore,
        date.strftime('%a, %b %d, %Y')
    )

    bot_post(message, CONFIG_DATA['chore_bot'])
    bot_post('Chore-Bot posted.', CONFIG_DATA['notifier_bot'])

    CONFIG_DATA['current_group'] += 1
    save_config_data()

# Runs a chore reminder if weekday
def run():
    load_config_data()

    now = datetime.datetime.now()
    if now.weekday() >= 5: # If it is a weekend
        bot_post('Chore-Bot aborted post: Weekend.', CONFIG_DATA['notifier_bot'])
    else:
        chore_notify(now)

# ----------------------------------------------------------------------------- EXECUTION

if __name__ == '__main__':
    run()