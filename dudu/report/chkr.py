import requests

# Function to check if a proxy is working
def check_proxy(proxy):
    try:
        response = requests.get('http://www.google.com', proxies={'http': 'http://' + proxy, 'https': 'https://' + proxy}, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False

# Read proxies from file and check each one
def check_proxies_from_file(file_path):
    working_proxies = []
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    for proxy in proxies:
        if check_proxy(proxy):
            print(f'Proxy {proxy} is working.')
            working_proxies.append(proxy)
        else:
            print(f'Proxy {proxy} is not working.')
    return working_proxies

# Write the working proxies to a new file
def write_working_proxies(file_path, working_proxies):
    with open(file_path, 'w') as file:
        for proxy in working_proxies:
            file.write(proxy + 'n')

# Path to the file containing the list of proxies
input_file_path = 'http_proxies.txt'
# Path to the file where the working proxies will be written
output_file_path = 'working_proxies.txt'

# Check the proxies and write the working ones to a new file
working_proxies = check_proxies_from_file(input_file_path)
write_working_proxies(output_file_path, working_proxies)

