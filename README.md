## Zoom Automation
Attends and records your lectures  for you during this COVID-19 Epidemic.

Dont miss anything!

##### Functions
* Log into your Zoom account through the zoom app.
* Join meeting by meeting ID or URL. Password OK
* Screen Record

##### Heads Up:
For OSX and Windows Users. 
I did my best, you will probably have to debug it though. I assumed users
would be running this on a Linux server.

you should have a config.json file with: 
```
{
    "username": "YOUR-ZOOM-USERNAME", 
    "password": "YOUR-ZOOM-PASSWORD"
}
```

### Setup
#### Dependencies :
* python(3.4 +) 
Linux Users 
```
./linux_setup.bash
```
Mac Users
```
./osx_setup.bash
```
Windows Users (gitbash) 

zoom: https://zoom.us/client/latest/ZoomInstaller.exe
```
pip install -r pip_requirements.txt
```

### Use
```
python3 automate_zoom.py -c zoom_config /PATH/TO/CONFIG_FILE -m MEETING_ID  \
        -p MEETING_PASSWORD -d MEETING_DURATION -f /PATH/TO/RECORD/SAVE_FOLDER \ 
        -u COURSE_NAME --record True/False --logged_in True/False
```
For Further info on arguments
```
python automate_zoom.py --help
```

### VirtualBox 
Zoom is able to detect if Zoom is 'in focus'. Meaning, it knows when you click away.
 
You can easily overcome this by creating a VirtualBox and running it in there.

Just make sure the VirtualBox is open and running. It can be minimized and it will appear the same to Zoom.

Note: all recordings will be saved in the VirtualBox

Note: Virtual Boxes can be resource intensive  

#### Example Cron Job Setup
1 hour MWF Class @ 3PM 

(starting a little early to allow for startup time) 
```
58 14 * * 1,3,5 python3 ~/Documents/AutoZoom/automate_zoom.py -c ~/Documents/AutoZoom -m "0123456789" -d 60 -f ~/Documents/AutoZoom/Records -u UCSD_101 --record True --logged_in True  >/dev/null 2>&1 
```

### Disclaimer: 
Be aware of "Two Party Consent" laws. In some countries/states it is illegal to record some one else with out permission. 

Check your laws... You are responsible for any legal problems / damages you incur. 

### Buy me a beer 🍺 :)
Venmo: jyrose
