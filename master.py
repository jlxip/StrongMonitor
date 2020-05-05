from queue import Queue
import psycopg2, os

oldprint = print
def print(*argv):
	oldprint('[MASTER]', ' '.join(argv))

def start(q, config):
	print('I am listening.')

	# Connect to the database.
	with open('db_password.secret', 'r') as f:
		pwd = f.read().replace('\n', '')

	conn = psycopg2.connect(host=config['DB']['host'], database=config['DB']['database'], user=config['DB']['user'], password=pwd)
	cur = conn.cursor()

	while True:
		msg = q.get()

		# Do I know this IP?
		cur.execute('SELECT "whitelisted" FROM "ips" WHERE "IP"=%s', (msg['IP'],))
		response = cur.fetchall()

		if len(response) != 0:
			# I know them. Are they whitelisted?
			if response[0][0]:
				# They are. Stop everything.
				continue
		else:
			# Don't know them. Pleased to meet you.
			cur.execute('INSERT INTO "ips" VALUES (%s, false)', (msg['IP'],))
			conn.commit()

		oldprint(msg)
		if msg['TYPE'] == 'LOG':
			cur.execute('INSERT INTO "log" ("service", "IP", "timestamp", "data") VALUES (%s, %s, %s, %s)', (msg['SERVICE'], msg['IP'], msg['TIMESTAMP'], msg['LINE']))
			conn.commit()
		elif msg['TYPE'] == 'BAN':
			print('Banning %s' % msg['IP'])
			# Ban first, then touch the DB.
			ban = config['ban_command'] % msg['IP']
			os.system(ban)

			# Add it as banned.
			try:
				cur.execute('INSERT INTO "ban" VALUES (%s, %s, %s)', (msg['IP'], msg['TIMESTAMP'], msg['REASON']))
			except:
				# There might be some race conditions in which user is banned twice.
				pass

			conn.commit()

