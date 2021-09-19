import sys

sys.path.append("../..")

from utils.ssh import connect_by_previous, exec, get_token
from utils.text import print_title, print_output

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list)


client.close()
