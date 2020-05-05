from threading import Thread
import subprocess
from datetime import datetime
import re

MODULE_NAME = 'SSHD'

oldprint = print
def print(*argv):
	oldprint('[%s]' % MODULE_NAME, ' '.join(argv))

JOURNALCTL_COMM = 'sshd'

q = None
config = None
RECORD = {}

def handle(line):
	line = line.split(' ')
	timestamp = ' '.join(line[:3])
	timestamp = datetime.strptime(timestamp, '%b %d %H:%M:%S')
	timestamp = timestamp.replace(year=2020)
	timestamp = int(datetime.timestamp(timestamp))
	line = line[3:]

	line = line[2:] # Ignore "Stronghold sshd[20785]"
	line = ' '.join(line)

	# Some no problem scenarios.
	for i in config['no_log']:
		if line.startswith(i):
			return

	# Get the IP.
	ip = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
	if len(ip):
		ip = ip[-1]	# ip[0] would be insecure
	else:
		# If there's no IP there's probably nothing interesting.
		return

	# If it has arrived at this point, it has to be logged.
	q.put({'TYPE': 'LOG', 'SERVICE': 'SSHD', 'TIMESTAMP': timestamp, 'IP': ip, 'LINE': line})

	# What's it doing?
	for i in config['rules']:
		match = False
		if i['mode'] == 'start':
			match = line.startswith(i['str'])
		elif i['mode'] == 'anywhere':
			match = i['str'] in line
		else:
			print('[ERROR] Unsupported mode "%s"' % i['mode'])
			exit()

		if match:
			RECORD.setdefault(ip, {}).setdefault(i['name'], 0)
			RECORD[ip][i['name']] += 1

			# Ban?
			if RECORD[ip][i['name']] > i['limit']:
				q.put({'TYPE': 'BAN', 'TIMESTAMP': timestamp, 'IP': ip, 'REASON': '[%s] %s' % (MODULE_NAME, i['name'])})

def start(q_, config_):
	print('Started.')

	global q, config
	q = q_
	config = config_['modules'][MODULE_NAME]

	# Redirect journal stdout.
	journal = subprocess.Popen(['journalctl', '_COMM='+JOURNALCTL_COMM, '-f'], stdout=subprocess.PIPE)

	# Discard first line ("-- Logs begin at Tue 2020-05-05 00:32:28 CEST. --")
	journal.stdout.readline()

	# Start reading
	while True:
		line = journal.stdout.readline().decode('utf-8')
		line = line.replace('\n', '')
		if line == '':
			# Ctrl+C or something.
			break
		handle(line)

	exit()
