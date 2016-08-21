# ----------------------------------------------------------------------------- IMPORTS

import datetime
import requests # http://docs.python-requests.org/
import yaml # http://pyyaml.org/

# ----------------------------------------------------------------------------- DATA & CONSTANTS

# Configuration
config_file = 'config.yaml'
config_data = dict()

# Chore Schedule
CHORES = {
    'Monday':   'Living Room & Dining Room',
    'Tuesday':  'Kitchen',
    'Wednesday':    'Bathroom & Outside Garbage',
    'Thursday': 'Kitchen',
    'Friday':   'Hallway & Backyard',
}

# Roommate Groups
GROUPS = [
    'Aaron & Rachel',
    'Colin & Jasper',
    'Christina & Rod',
    'Georgina & Luis'
]

# ----------------------------------------------------------------------------- FUNCTIONS

# Loads the contents of config.yaml into config_data
def load_config_data():
    global config_data

    with open(config_file, 'r') as stream:
        try:
            config_data = yaml.load(stream)
        except yaml.YAMLError as err:
            print(err)

    if config_data['current_group'] > 4:
        config_data['current_group'] = 1

# Saves the contents of config_data to config.yaml
def save_config_data():
    with open(config_file, 'w') as ostream:
        yaml.dump(config_data, ostream, default_flow_style=False)

# Performs an HTTP Post request to GroupMe
def bot_post(text, bot_ID):
    r = requests.post('https://api.groupme.com/v3/bots/post', data = {
        'bot_id': bot_ID,
        'text': text
    })
    print(text)

# Posts to the Notifier Bot
def debug_post(text):
    bot_post(text, config_data['notifier_bot'])

# Builds and posts the chore reminder
def chore_notify(now):
    global config_data

    todays_chore = CHORES[now.strftime('%A')]
    message = '{}, your chore for today is: the {}\n({})'.format(
        GROUPS[config_data['current_group']-1],
        todays_chore,
        now.strftime('%a, %b %d, %Y')
    )

    bot_post(message, config_data['chore_bot'])
    config_data['current_group'] += 1
    config_data['last_ran'] = int(now.timestamp())
    save_config_data()

# Runs a chore reminder if weekday & at least 18 hours since last run
def run():
    load_config_data()
    now = datetime.datetime.now()
    seconds_since_last_post = int(now.timestamp()) - config_data['last_ran']

    if now.weekday() >= 5: # If it is a weekend
        debug_post('Chore-Bot aborted post: Weekend.')
    elif seconds_since_last_post < 64800: # If it has been at least 18 hours
        debug_post('Chore-Bot aborted post: Too recently ran: {} seconds ago (< 64800).'.format(seconds_since_last_post))
    else:
        chore_notify(now)
        debug_post('Chore-Bot posted.')

# ----------------------------------------------------------------------------- EXECUTION

if __name__ == '__main__':
    run()
