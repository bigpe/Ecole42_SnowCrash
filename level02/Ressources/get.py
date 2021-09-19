import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve().absolute().joinpath('../..')))

from utils.ssh import get_token, download_from, connect_by_previous
from utils.text import print_title, print_output

client = connect_by_previous()
file_name = 'level02.pcap'
download_from(file_name)
print_title('Read file by Wireshark')
file_content = os.popen("tshark -Tfields -e data -r level02.pcap | tr -d '\n'").read()

print_title(f'Remove tmp file {file_name}')
os.unlink(file_name)

print_output(file_content, 'File content')

print_title("It's a Hex string")
print_title("Create bytes object from it")
hex_string = bytes.fromhex(file_content)
print_output(str(hex_string), 'Bytes file content')

print_title("Slice useful data")

encoded_password = hex_string.split(b"Password: ")[1].split(b"Login incorrect")[0]
print_output(str(encoded_password), 'Encoded password')

print_title("Cleanup it")
print_title("\\x7F (127) - is delete special char, a call to remove the character in front of it")
print_title("Also remove \\n (10) and \\r (13)")
res = []
for c in encoded_password:
    not_allowed = {127, 10, 13}
    if c == 127:
        res.pop()
    if c not in not_allowed:
        res.append(c)
flag_password = ''.join([chr(c) for c in res])
print_output(flag_password, 'Flag password (So clean)')

client.close()
get_token(flag_password)
