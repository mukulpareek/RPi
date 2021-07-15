# RPi
### Raspbian server cron jobs  
  
The `web_scrape_security.py` script is run by a cron job in the morning.  Another cron job then runs `push_to_github.sh`, which is a shell script with git commands to copy the new files to Github.  The shell script requires git config options to be set up in advance on the computer.
  
The cron job is set up as below using the command `crontab -e`:
