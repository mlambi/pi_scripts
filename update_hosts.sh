
#!/bin/bash

# an attempt at writing a script to update the hosts file
# this does the job.  you need to start from a default
# hosts file.  This will append shared pi_scripts/hosts.txt
# 

while IFS= read -r line;do
    echo "$line" >> /etc/hosts
done < "/home/pi/pi_scripts/hosts.txt"
echo "completed"
