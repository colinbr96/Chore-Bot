import datetime
import requests

chores = {
	'Monday':		'Living Room & Dining Room',
	'Tuesday':		'Kitchen',
	'Wednesday':	'Bathroom & Outside Garbage',
	'Thursday':		'Kitchen',
	'Friday':		'Hallway & Backyard',
	'Saturday':		'',
	'Sunday':		''
}

groups = [
	'Aaron & Rachel',
	'Colin & Jasper',
	'Christina & Rod',
	'Georgina & Luis'
]

def load_group() -> int:
	file = open('group', 'r')
	group_num = file.read(1)
	return int(group_num)

def save_group(group_num):
	file = open('group', 'w')
	file.write(group_num)

def http_post(text):
	r = requests.post('https://api.groupme.com/v3/bots/post', data = {
		'bot_id': 'e7cd7c4d3448e2eadcd0dca190',
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
		message = '{}, your chore today is: {}'.format(groups[todaysGroup], todaysChore)
		http_post(message)


if __name__ == '__main__':
	run()