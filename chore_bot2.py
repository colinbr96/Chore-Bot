import datetime
import requests # http://docs.python-requests.org/

GROUP_FILENAME = 'group.txt'

# Bot IDs
CHORE_BOT = '58ae5dfd7dfe0acde6da2340f2'
NOTIFIER_BOT = 'e7cd7c4d3448e2eadcd0dca190'

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

# Performs an HTTP Post request to GroupMe
def bot_post(text, bot_ID):
	r = requests.post('https://api.groupme.com/v3/bots/post', data = {
		'bod_id': bot_ID,
		'text': text
	})

# Returns the number stored in the group-file
def load_group_file():
    file = open(GROUP_FILENAME, 'r')
    group_num = int(file.read())
    if group_num > 4:
    	group_num = 1
    return group_num

# Writes the given number to the group-file
def save_group_file(group_num):
    file = open(CURRENT_GROUP_FILE, 'w')
    file.write(str(group_num))

# Builds and posts the chore reminder
def chore_notify(date):
	todays_chore = chores[date.strftime('%A')]
	todays_group = load_group_file()

	message = '{}, your chore for today is: the {}\n({})'.format(
    	groups[todaysGroup-1],
    	todaysChore,
    	now.strftime('%a, %b %d, %Y')
    )

    bot_post(message)
    todays_group += 1
    save_group_file(todays_group)

# Runs chore reminder if weekday
def run():
	now = datetime.datetime.now()
	if now.weekday() >= 5: # If it is a weekend
		bot_post('Chore-Bot aborted post: Weekend', NOTIFIER_BOT)
	else:
		chore_notify()



if __name__ == '__main__':
	run()