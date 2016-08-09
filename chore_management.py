import datetime

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

todaysGroup = 0

def run():
	global todaysGroup

	now = datetime.datetime.now()
	todaysChore = chores[now.strftime('%A')]
	
	todaysGroup += 1
	if todaysGroup > 4:
		todaysGroup = 1
	
	if todaysChore != '':
		# post on groupme
		message = '{}, your chore today is: {}'.format(groups[todaysGroup], todaysChore)
		
if __name__ == '__main__':
	run()
