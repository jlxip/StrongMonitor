# StrongMonitor
A modular and configurable monitor for GNU/Linux servers.

![Screenshot of StrongMonitor working](https://i.imgur.com/a5giDHv.jpg)

## Introduction
_StrongMonitor_ is a lightweight, modular and heavily configurable monitor and auto-banning software for GNU/Linux servers made in Python, similar to Fail2ban. It saves logs to a PostgreSQL database and takes action whenever the configured rules apply. Its configuration file is quite easy to read and very customizable.

Currently, StrongMonitor only monitors sshd, but in the near future (when I have more time) it will support nginx as well.

I wanted to create my own monitor since I was getting some bruteforce attacks in my VPS (nicknamed Stronghold, hence the name), and I thought I could make a really lightweight auto-banning program.

If you decide to try it out, please [inform on any issues](https://github.com/jlxip/StrongMonitor/issues) that you might encounter.

## Installation
### Dependencies
StrongMonitor relies on `journalctl` existing in the system (for reading logs asynchronously), as well as `python3` and the pip package `psycopg2` (for communicating with the PostgreSQL server). You must as well have some form of firewall. I personally use ufw.

### Creating the database
First, create a database in the PostgreSQL server, and import the schema from the file `DB_schema.sql`. You should probably want to create a user in the DBMS which only has permissions on this database.

### Filling the DB data in the config file
Modify the DB section of `config.json`, change `host`, `user` and `database` to whatever fits your environment. You must also create a different file, `db_password.secret`, containing the password to the user you specified above, in order to not have sensitive information in the config, making it freely shareable.

### Specifying a ban command
Whenever the rules decide so, an IP will be banned using your firewall.

For this, you must specify in `ban_command` which command to run, writing `%s` where the IP should go.

You should not run StrongMonitor as root, instead, use `sudo` in the ban command, as probably modifying your firewall configuration requires you to be root.

In the example `config.json`, `sudo /opt/banIP.sh %s` is in place, and the `sudoers` file is configured to not ask for a password when running it, with `[user] ALL=(root) NOPASSWD: /opt/banIP.sh *`. I would recommend to do this in order to reduce the possibility of privilege escalation in case an attacker breaks into the user with these sudo privileges.

That script, `/opt/banIP.sh`, in my server, runs `ufw insert 1 deny from "$1" comment 'StrongMonitor'`, but if you don't use ufw feel free to write it in any way you like.

### Writing the rules
In the `modules` part you can write whichever modules you would like to use (currently only `SSHD`). Then, specify whichever options you want. These are as follows:

#### `no_log`
`no_log` describes which starting strings (in the service log) must not be saved on the database, as they don't contain valuable information. For instance, example config includes `Disconnect from`, which would ignore any log such as `May 05 18:36:53 Stronghold sshd[31122]: Disconnected from (IP) port 48550 [preauth]`.

#### `rules`
`rules` specify the set of ban rules. Each ban rule contains:
- `name`. Could be anything, it's for storing in the database the ban reason.
- `str`. The string that must appear in the log to count as a suspicious request.
- `mode`. Whether `str` has to be at the beginning of the log line (`start`) or `anywhere`.
- `limit`. The maximum value of the counter of suspicious requests of this kind allowed. When exceeded, the IP is banned.

### Whitelisting
If you would like to whitelist an IP, there's no easy way to do it at the moment. You must manually modify the row in the database, table `ips`, which contains the IP to whitelist and change the value `whitelisted` to true. This feature will be implemented soon (read the TODO at the bottom).

### Creating a service
Run `strongmonitor.py` and do some tests in order to check that your configuration is working. Once you're sure, create a systemd service for StrongMonitor. For this, I provide the `strongmonitor.service` file, with it, you could create a symbolic link from `/etc/systemd/system/strongmonitor.service` (in Debian at least) to it.

Enable the service as usual, with `sudo systemctl enable strongmonitor` and run it for the first time with `sudo systemctl start strongmonitor`. You can read the output in real time to check that everything is working as intended with `journalctl -u strongmonitor -f`.

## TODO
- [ ] Auto-popullate the database with the tables so that the user doesn't need to manually create them with `DB_schema.sql`.
- [ ] Allow whitelisting from the `config.json` file instead of the DB.
- [ ] Allow the possibility of a backdoor, which would trigger a whitelist.
- [ ] Support nginx.

## I see you like to reinvent the wheel, don't you?
Correct.
