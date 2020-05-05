#!/usr/bin/env python3

from threading import Thread
from queue import Queue

import master, json
from sm_modules import ssh

oldprint = print
def print(*argv):
	oldprint('[MAIN]', ' '.join(argv))

if __name__ == '__main__':
	print('Let\'s go!')

	# Read config.
	with open('config.json', 'r') as f:
		config = json.load(f)

	# Start thread communication.
	q = Queue()
	Thread(target=master.start, args=(q, config)).start()

	ts = []
	fails = []
	ts.append(Thread(target=ssh.start, args=(q, config)))
	fails.append(0)

	for i in range(len(ts)):
		ts[i].start()

	print('Everything running.')

	while True:
		for i in range(len(ts)):
			ts[i].join()
			fails[i] += 1

			if fails[i] == 3:
				print('Module %d failed thrice. Giving up.' % i)
				ts.pop(i)
			else:
				print('Module %d died. Giving it another go. %d/3' % (i, fails[i]))
				ts[i] = Thread(target=ssh.start, args=(q, config))
				ts[i].start()

		if(len(ts) == 0):
			print('Everyone is dead, now I am going to die too. See you.')
			exit()
