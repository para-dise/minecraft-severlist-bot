# minecraft-severlist-bot
Made in Discord.py


Usage:

- $help - list servers
- $server add [server ip/domain] [server port] [Icon URL] [name] [description]
- $server info [server name]

TBA if I CBA:
- Server tags
- Top servers
- Limit servers per user
- Blacklist users

Dependencies:

- https://github.com/kevinkjt2000/mcstatus - edited mcstatus
- https://pypi.org/project/aiofiles/ - async file management
- https://pypi.org/project/IPy/ - used it for IP validation
- https://github.com/kvesteri/validators - used it for domain validation


Features
- No database required. Text file stores all information.
- Automated parsing without database.
- Server ping
- Server playercount

Checks:
- Filters ":" in user input and replaces with UTF charcode, however it does display : back to the user.
- Domain & IP validation
- Duplicate name or IP check
- Length check
- A nice embed

Note: I'm sure I have useless values somewhere, if you find any just delete them.
