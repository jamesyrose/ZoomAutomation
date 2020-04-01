## Zoom Automation
Attends and records your lectures  for you during this COVID-19 Epidemic.

Dont miss anything!

##### Functions
* Log into your Zoom account through the zoom app.
* Join meeting by meeting ID or URL. Password OK
* Screen Record

##### Heads Up:
Sorry Apple users, I dont have a Mac.
I did my best, you will probably have to debug it though.

Windows Users: you may have to configure the ffmpeg command

Linux Users: Its working on Mint19

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
python3 automate.py -c /PATH/TO/CONFIG_FILE -m MEETING_ID -p MEETING_PASSWORD \
                    -d MEETING_DURATION -f /PATH/TO/RECORD/SAVE_FOLDER \ 
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
### Additional Notes: 
This uses cv2 to compare an image to a screen shot in order to locate elements. Resizing the image led to 
inconsistent results. If it does not work for you because it cannot find the image, you may uncomment line 93-97. 
If it continues to not work, you can change "force=False" to "force=True" on line 77. This will search for a match until 
it finds one (which means that it can get stuck in a loop). If push comes to shove, reference the "SearchImg"
folder and replace them with your own. 

I have tested this on Windows 10 and Linux Mint 19 and it works on both. 

### Disclaimer: 
Be aware of "Two Party Consent" laws. In some countries/states it is illegal to record some one else with out permission. 

Check your laws... You are responsible for any legal problems / damages you incur. 

### Buy me a beer 🍺 :)
Venmo: jyrose
