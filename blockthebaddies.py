import os
import re
import pandas as pd

# Get the directory where the .bat file is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define relative file paths
input_file_path = os.path.join(script_dir, 'wgsaudit.adt')
output_excel_path = os.path.join(script_dir, 'output.xlsx')
matched_excel_path = os.path.join(script_dir, 'matched.xlsx')
hostdeny_txt_path = os.path.join(script_dir, 'hostdeny.txt')

# Number of consecutive IPs required for matching
consecutive_threshold = 10


# Function to read IPs from a text file
def read_ips_from_file(filename):
    with open(filename, 'r') as file:
        ips = file.read().splitlines()
    return ips


# Function to write IPs to a text file
def write_ips_to_file(filename, ips):
    with open(filename, 'w') as file:
        for ip in ips:
            file.write(ip + '\n')


# Check if hostdeny.txt exists, and create it if it doesn't
if not os.path.exists(hostdeny_txt_path):
    with open(hostdeny_txt_path, 'w') as file:
        file.write('')  # Create an empty file

# Read the file as text
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Extract IP-like numbers using regex
ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
matched_ips = []

for line in lines:
    ips = ip_pattern.findall(line)
    matched_ips.extend(ips)

# Create a DataFrame with the matched IP-like numbers
output_df = pd.DataFrame({'IP Addresses': matched_ips})

# Export to Excel
output_df.to_excel(output_excel_path, index=False)  # index=False to exclude row numbers

# Read the output file containing IP addresses
output_df = pd.read_excel(output_excel_path)

# Initialize variables
consecutive_count = 1
previous_ip = None
matched_ips = []

# Iterate through each row in the DataFrame
for index, row in output_df.iterrows():
    current_ip = row['IP Addresses']

    # Check if the current IP starts with '192.168'
    if not current_ip.startswith('192.168'):
        # Check if the current IP matches the previous one
        if current_ip == previous_ip:
            consecutive_count += 1
        else:
            consecutive_count = 1

        # If consecutive_threshold consecutive occurrences are found, store the IP
        if consecutive_count == consecutive_threshold:
            matched_ips.append(current_ip)

        previous_ip = current_ip

# Create a DataFrame with matched IPs
matched_df = pd.DataFrame({'Matched IP Addresses': matched_ips})

# Export to a new Excel file
matched_df.to_excel(matched_excel_path, index=False)

# Read the matched IP addresses from 'matched.xlsx'
output_df = pd.read_excel(matched_excel_path)
matched_ips = set(output_df['Matched IP Addresses'])

# Read the hostdeny IPs from 'hostdeny.txt'
hostdeny_ips = read_ips_from_file(hostdeny_txt_path)

# Compare IPs and add unmatched ones to hostdeny
unmatched_ips = [ip for ip in matched_ips if ip not in hostdeny_ips]
hostdeny_ips.extend(unmatched_ips)

# Write updated hostdeny to 'hostdeny.txt'
write_ips_to_file(hostdeny_txt_path, hostdeny_ips)

# Display a message indicating the number of IPs added to hostdeny
num_added = len(unmatched_ips)
print(f"{num_added} baddies have been added to hostdeny.txt.")
