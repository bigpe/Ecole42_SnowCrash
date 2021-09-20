import os
import subprocess
import sys

sys.path.append("../..")

from utils.ssh import connect_by_previous, exec, save_token, get_previous_password, get_current_level
from utils.text import print_title, print_output, print_action
from utils.config import VM_ADDRESS, VM_PORT

client = connect_by_previous()

file = exec(client, 'ls', title='Get files list')[0]
print_output(file)

output = exec(client, f'./{file}', title='Execute file')
print_output(output)
print_title('Out UID - 2013, expected 4242, try to debug and break?')

dev_null = open(os.devnull, 'w')
connect_command = f'sshpass -p {get_previous_password()} ssh {get_current_level()}@{VM_ADDRESS} -p {VM_PORT} ' \
                  f'-oStrictHostKeyChecking=no'

command = f"{connect_command} gdb -q ./{file}"
stream = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=dev_null)
print_action(command)
print_output(stream.stdout.readline().decode('utf-8'), 'Output')
print_title("Debugger started, okay, let's do this")
print_title('Inspect a little')

command = f"{connect_command} echo disass main | gdb -q ./{file}"
stream = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=dev_null)
print_action(command)
print_output([line.decode('utf-8') for line in stream.stdout.readlines()])
print_title('We can set breakpoint before UID check flag is set to false and a little cut execution way')

command = f"{connect_command} gdb -q ./{file}"
stream = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=dev_null)
print_action(command)

print_title('Send commands to debugger: [breakpoint -> run -> jump] to state where UID check expression passed')
command = b'break *0x0804859a\nrun\njump *0x080485cb\n'
print_action(f"\n{command.decode('utf-8')}")
stream.stdin.write(command)
output = stream.communicate()[0].decode('utf-8')
print_output(output)

token = output.split('is ', 1)[1].split('[')[0].strip()
print_output(token, 'Token')
print_title('We break program and obtained token, nice!')

save_token(token)

client.close()
