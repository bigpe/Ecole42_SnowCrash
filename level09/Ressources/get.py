import sys

sys.path.append("../..")

from utils.ssh import connect_by_previous, exec, get_token
from utils.text import print_title, print_output

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list)

file_content_bytes = exec(client, 'cat token', title='Read token file', read_method='read')
file_content_chars = [chr(c) for c in file_content_bytes]
print_output("".join(file_content_chars), 'File content')
print_title('Looks like usual string but a few characters out of ascii, cipher?')

output = exec(client, 'ltrace ./level09', title='Trace binary', err=True)
print_output(output)
print_title('Not reverse this? Funny, lets reverse')

output = exec(client, './level09 abcd')
print_output(output, 'Output')
output = exec(client, './level09 aaaa')
print_output(output, 'Output')
output = exec(client, './level09 axyz')
print_output(output, 'Output')
print_title('Got it, shift character by index, eg. aaaaaa -> a(0:a)a(1:b)a(2:c)a(3:d)a(4:e)a(5:f)')

print_title('Reverse cipher')
res = []
for i, c in enumerate(file_content_bytes):
    if c - i >= 0:
        res.append(chr(c - i))
flag_password = ''.join(res)
print_output(flag_password, 'Flag password')

client.close()
get_token(flag_password)
