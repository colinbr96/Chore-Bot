# ----------------------------------------------------------------------------- IMPORTS

# Python Standard Library
import datetime
import time

# Third Party
import pytz # http://pytz.sourceforge.net/
import requests # http://docs.python-requests.org/
import yaml # http://pyyaml.org/

# ----------------------------------------------------------------------------- DATA & CONSTANTS

# Configuration
CONFIG_FILENAME = 'config.yaml'
config_data = dict() # Populated by load_config_data()
RUN_HOUR = 9
RUN_MINUTE = 0

# Chore Schedule
CHORES = {
    'Monday':    'Living Room & Front Patio',
    'Tuesday':   'Kitchen & Dining Room',
    'Wednesday': 'Bathroom & Outside Garbage',
    'Thursday':  'Kitchen & Dining Room',
    'Friday':    'Hallway & Backyard'
}

# Roommate Groups
GROUPS = [
    'Aaron & Rachel',
    'Colin & Jasper',
    'Christina & Rod',
    'Georgina & Luis'
]

# ----------------------------------------------------------------------------- EXCEPTIONS

class WeekendException(Exception):
    """ Raised if the bot tries to post on a weekend
    """
    pass

class SpamException(Exception):
    """ Raised if the bot tries to post within 18 hours of its last post
    """
    pass

# ----------------------------------------------------------------------------- FUNCTIONS

def load_config_data() -> None:
    """ Loads the contents of config.yaml into config_data
    """
    global config_data

    with open(CONFIG_FILENAME, 'r') as stream:
        try:
            config_data = yaml.load(stream)
        except yaml.YAMLError as err:
            print(err)

    if config_data['current_group'] > 4:
        config_data['current_group'] = 1

def save_config_data() -> None:
    """ Saves the contents of config_data to config.yaml
    """
    with open(CONFIG_FILENAME, 'w') as ostream:
        yaml.dump(config_data, ostream, default_flow_style=False)

def post_str(now) -> str:
    """ Returns the appropriate message for the chore reminder
    """
    todays_chore = CHORES[now.strftime('%A')]
    return '{}, your chore for today is: the {}\n({})'.format(
        GROUPS[config_data['current_group']-1],
        todays_chore,
        now.strftime('%a, %b %d, %Y')
    )

def bot_post(text, bot_ID) -> None:
    """ Performs an HTTP Post request to GroupMe
    """
    print("{}: {}".format(bot_ID, text))

    r = requests.post('https://api.groupme.com/v3/bots/post', data = {
        'bot_id': bot_ID,
        'text': text
    })

def debug_post(text) -> None:
    """ Posts to the Debugging Bot
    """
    bot_post(text, config_data['debug_bot'])

def chore_post(now) -> None:
    """ Posts the chore reminder and updates the config_data
    """
    global config_data
    message = post_str(now)

    bot_post(message, config_data['chore_bot'])
    config_data['current_group'] += 1
    config_data['last_ran'] = int(now.timestamp())
    save_config_data()

def pass_checks(now) -> None:
    """ Raises the appropriate Exception for SpamError or WeekendError
    """
    seconds_since_last_post = int(now.timestamp()) - config_data['last_ran']

    if seconds_since_last_post < 64800: # If it has not been at least 18 hours
        raise SpamException
    if now.weekday() >= 5: # If it is a weekend
        raise WeekendException

def run() -> None:
    """ Checks every hour to see if the post is within the hour
        If the post is within the hour, checks every minute to see if the post is within the minute
        If the post is within the minute, attempts to post (if it passes checks)
        Sleeps for a minute after posting
    """
    while True:
        now = datetime.datetime.now(pytz.timezone('US/Pacific'))
        next_run = datetime.datetime(now.year, now.month, now.day, RUN_HOUR, RUN_MINUTE, 0)
        delta = next_run - now.replace(tzinfo=None)

        if (delta.seconds // 60) < 60:
            if delta.seconds < 60:
                load_config_data()
                try:
                    pass_checks(now)
                    chore_post(now)
                except SpamException:
                    seconds_since_last_post = int(now.timestamp()) - config_data['last_ran']
                    debug_post("ABORTING - Spam: Chore-Bot ran {} seconds ago. (< 64800)".format(seconds_since_last_post))
                except WeekendException:
                    debug_post("ABORTING - Weekend: {}".format(now.strftime('%A')))
                time.sleep(60)
            else:
                time.sleep(30)
        else:
            time.sleep(3600)

# ----------------------------------------------------------------------------- EXECUTION

if __name__ == '__main__':
    run()