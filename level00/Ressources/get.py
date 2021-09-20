import sys

sys.path.append("../..")

from utils.ssh import connect, exec, get_token
from utils.text import print_output, print_title

client = connect('level00', 'level00')

files = exec(client, 'find / -user flag00', title='Find all flag00 files')
print_output(files, 'Find files')

file_content = exec(client, f'cat {files[0]}', title='Read this files')[0]
print_output(file_content, 'File content')

print_title("It's a Caesar cipher")
print_title("Brute this")

flag_password = None

for i in range(26):
    cipher = []
    for c in file_content:
        c = ((ord(c) - 97 + i) % 26) + 97
        cipher.append(chr(c))
    res = "".join(cipher)
    if i == 11:
        flag_password = res.strip()
    print_output(f'{res} {"<- Its our flag00 password (I hope)" if i == 11 else ""}', f'ROT {i}')

get_token(flag_password)

client.close()
