# ----------------------------------------------------------------------------- IMPORTS

# Python Standard Library
import datetime
import time
import sys

# Third Party
import pytz # http://pytz.sourceforge.net/
import requests # http://docs.python-requests.org/
import yaml # http://pyyaml.org/

# ----------------------------------------------------------------------------- DATA & CONSTANTS

# Configuration
CONFIG_FILE = 'config.yaml'
OUTPUT_FILE = 'output.log'
config_data = dict() # Populated by load_config_data()
RUN_HOUR = 9
RUN_MINUTE = 1

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

def log(message) -> None:
    template = "{} - {}\n"
    now = datetime.datetime.now(pytz.timezone('US/Pacific'))
    date_str = now.strftime('%Y-%m-%d %H:%M:%S')

    with open(OUTPUT_FILE, 'a') as f:
        f.write(template.format(date_str, message))

def load_config_data() -> None:
    """ Loads the contents of config.yaml into config_data
    """
    global config_data

    with open(CONFIG_FILE, 'r') as stream:
        try:
            config_data = yaml.load(stream)
        except yaml.YAMLError as err:
            log(err)

    if config_data['current_group'] > 4:
        config_data['current_group'] = 1

def save_config_data() -> None:
    """ Saves the contents of config_data to config.yaml
    """
    with open(CONFIG_FILE, 'w') as ostream:
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
    log("{}: {}".format(bot_ID, text))

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
    debug_post(message)

    config_data['current_group'] += 1
    config_data['last_ran'] = int(now.timestamp())
    save_config_data()

def pass_checks(now) -> None:
    """ Raises the appropriate Exception for SpamError or WeekendError
    """
    log("Attempting to pass checks")
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
        log("Looped")

        now = datetime.datetime.now(pytz.timezone('US/Pacific'))
        next_run = datetime.datetime(now.year, now.month, now.day, RUN_HOUR, RUN_MINUTE, 0)
        delta = next_run - now.replace(tzinfo=None)

        if (delta.seconds // 60) < 60: # Within hour
            if delta.seconds < 60: # Within minute
                load_config_data()
                try:
                    pass_checks(now)
                    chore_post(now)
                except SpamException:
                    seconds_since_last_post = int(now.timestamp()) - config_data['last_ran']
                    debug_post("ABORTING - Spam: Chore-Bot ran {} seconds ago. (< 64800)".format(seconds_since_last_post))
                except WeekendException:
                    debug_post("ABORTING - Weekend: {}".format(now.strftime('%A')))

                log("Sleeping for 1 minute")
                time.sleep(60)
            else:
                log("Sleeping for 30 seconds")
                time.sleep(30)
        else:
            log("Sleeping for 1 hour")
            time.sleep(3600)

# ----------------------------------------------------------------------------- EXECUTION

if __name__ == '__main__':
    log("Starting up")
    run()
