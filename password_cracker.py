
import subprocess

# Retrieve the meta data of available Wi-Fi profiles
meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
# Decode the binary data to string
data = meta_data.decode('utf-8', errors="backslashreplace")
# Split the string into lines
data = data.split('\n')

profiles = []

# Extract the profile names
for line in data:
    if "All User Profile" in line:
        # Extract the profile name and remove unnecessary characters
        profile_name = line.split(":")[1].strip()
        profiles.append(profile_name)

# Print the Wi-Fi names and passwords
print("{:<30}| {:<}".format("Wi-Fi Name", "Password"))
print("----------------------------------------------")

for profile in profiles:
    try:
        # Retrieve the Wi-Fi password for the given profile
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'])
        results = results.decode('utf-8', errors="backslashreplace")
        results = results.split('\n')
        # Extract the password from the output
        password = [line.split(":")[1].strip() for line in results if "Key Content" in line]
        # Print the profile name and password
        print("{:<30}| {:<}".format(profile, password[0] if password else ""))
    except subprocess.CalledProcessError:
        print("Error occurred while retrieving password for", profile)