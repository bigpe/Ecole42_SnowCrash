import os
import subprocess
import sys

sys.path.append("../..")

from utils.ssh import connect_by_previous, exec, save_token, get_previous_password, get_current_level
from utils.text import print_title, print_output, print_action, print_magic
from utils.config import VM_ADDRESS, VM_PORT

client = connect_by_previous()

file = exec(client, 'ls', title='Get files list')
print_output(file)
print_title('Empty, strange!!!')
print_title('Try to find clue!')

files = exec(client, 'find / -user level14 ! -name /proc/*"', title='Find all level14 files')
print_output(files)
print_title('Empty!!!')

files = exec(client, 'find / -user flag14"', title='Find all flag14 files')
print_output(files)
print_title('Again???')

passwd_row = exec(client, 'cat /etc/passwd | grep 14', title='Find passwd rows')
print_output(passwd_row, 'Passwd row')
print_title('Flag14 UID - 3014 - remember it!')

output = exec(client, 'ltrace getflag', title='Try to trace getflag')
print_output(output, 'Output')
print_title("I've heard it before, your turn buddy...")

output = exec(client, 'strings /bin/getflag | grep ptrace', title='A little inspect')
print_output(output, 'Interested thing')
print_title("Ptrace detect if we debug program, oh no...")

dev_null = open(os.devnull, 'w')
connect_command = f'sshpass -p {get_previous_password()} ssh {get_current_level()}@{VM_ADDRESS} -p {VM_PORT}'

print_magic('Disassemble time!')
command = f"{connect_command} gdb -q getflag"
stream = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=dev_null)
print_action(command)

print_title('We go the familiar way')
print_title('Breakpoint on ptrace, cheat ptrace check, breakpoint on getuid and cheat it too!')
command = b'break ptrace\nrun\nstep\nset $eax=0\nbreak getuid\ncontinue\nstep\nset $eax=3014\ncontinue'
print_action(f"\n{command.decode('utf-8')}")
stream.stdin.write(command)
output = stream.communicate()[0].decode('utf-8')
print_output(output)

token = output.split('your token : ', 1)[1].split('[')[0].strip()
print_output(token, 'Token')
print_title('We break everything, oh my gash, amazing!')

print_title('Check it works')
command = f"sshpass -p {token} ssh flag14@{VM_ADDRESS} -p {VM_PORT}"
print_action(command)
stream = subprocess.Popen(command.split(" "), stdin=dev_null, stderr=dev_null)
print_output('Congratulation. Type getflag to get the key and send it to me the owner of this livecd :)', 'Ouptup')

save_token(token)
print_title('Oh wait, no more levels, so sad...')

client.close()
