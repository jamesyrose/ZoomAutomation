#!/usr/bin/python3
"""
Logs into your zoom account (if you wish) and records the screen and audio

Wrote this because I know I will miss a class here and there. <- Attendance can be monitored :)
It also servers as a reminder if I am using the computer.

Also, please note that you should be asking your professor/ who ever you are recording for permission

Author: James Rose
"""
import os
import platform
import time
from datetime import datetime
import pyautogui
import cv2
import numpy as np


class Zoom:
    def __init__(self, login: str, passwd: str, zoom_duration: int = 90,
                 sleep_multiplier: int = 1, save_folder: str = '', unique_name: str = ''):
        """
        :param login: Username/email
        :param passwd: zoom password
        :param save_folder: folder to save videos to
        :param unique_name:  some identifying name (class?)
        :param zoom_duration: how long is the class (minutes)
        :param sleep_multiplier: if your computer is slow youll want to increase sleep times
        """
        self.os = platform.system()  # Linux, Windows, OSX -> Darwin
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(self.cwd, "SearchImg")
        self.screen_size = pyautogui.size()  # Tuple(w, h)
        self.login = login
        self.passwd = passwd
        self.save_fol = save_folder
        self.unique_name = unique_name
        self.duration = zoom_duration * 60 + 300  # extra 5 minutes just to be safe
        self.sleep_multi = sleep_multiplier

    @property
    def is_zoom_open(self):
        """
        Checks for a zoom instance (zoom only allows one instance to be open

        :return:
        """
        if self.os in ["Darwin", "Linux"]:
            process = os.popen("ps -a | grep zoom").read()
            if len(process) > 1:
                return True
            else:
                return False

        elif self.os == "Windows":
            process = os.popen("tasklist | findstr Zoom.exe").read()
            if len(process) > 1:
                return True
            else:
                return False
        else:
            raise OSError(f"Operating system could not be identified: {self.os}")

    def click_area_by_img(self, img_name, threshold: float = 0.95):
        loc, size = self.find_img_loc(img_path=os.path.join(self.img_dir,
                                                            img_name
                                                            ),
                                      threshold=threshold
                                      )

        pyautogui.moveTo(int((loc[0] + size[0] / 2)), int((loc[1] + size[1] / 2)))
        pyautogui.click()

    def find_img_loc(self, img_path, threshold: float = 0.99, force=False):
        """
        Uses a png image and compares it to a screen shot to locate certain elements
        clicks that element

        force=True will recursively try to find it by iterating with lower thresholds.
        Not suggested to use... but its there.

        :param img_path: path to png image
        :param threshold: how similar does it need to be (i mean, you cant be perfect
        :param force:  do you want to recursively check until it finds something
        :return:
        """
        def img_loc(img_path, threshold):
            match_img = cv2.imread(img_path)
            template = cv2.cvtColor(np.array(pyautogui.screenshot()),
                                    cv2.COLOR_RGB2BGR
                                    )
            h, w = match_img.shape[:-1]

            res = cv2.matchTemplate(match_img,
                                    template,
                                    cv2.TM_CCOEFF_NORMED
                                    )
            loc = np.where(res >= threshold)

            if len(loc[0]) != 0:  # if there is a match
                x = int(loc[1].sum() / len(loc[1]))
                y = int(loc[0].sum() / len(loc[0]))
                return (x, y), (w, h)
            else:
                return None, None  # cant find match

        if force:
            # This can be bad to use. Should manually set threshold lower
            not_found = True
            location, size = None, None
            while not_found:
                location, size = img_loc(img_path, threshold)
                threshold -= .01
                if location is not None:
                    not_found = False
            return location, size
        else:
            return img_loc(img_path, threshold)

    def kill_zoom(self):
        """
        Will Kill Zoom Application


        :return:
        """
        if self.os in ["Darwin", "Linux"]:
            os.system("pkill -f zoom;")
        elif self.os == "Windows":
            os.system("taskkill /IM Zoom.exe /F")
        else:
            raise OSError(f"Operating system could not be identified: {self.os}")
        time.sleep(1 * self.sleep_multi)
        return self

    def launch_zoom(self):
        """
        Will Launch Zoom Application

        Kills all Zoom application first, zoom only allows one instance at a time

        :return:
        """
        if self.os in ["Darwin", "Linux"]:
            os.popen("zoom >/dev/null 2>&1 & ")
            time.sleep(1 * self.sleep_multi)  # let app open
        elif self.os == "Windows":
            zoom_exe = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Zoom", "bin", "Zoom.exe")
            os.popen(f"start {zoom_exe}")
        else:
            raise OSError(f"Operating system could not be identified: {self.os}")
        time.sleep(1.5 * self.sleep_multi)
        return self

    def login_zoom(self):
        """
        Enters login information to zoom and logs into it
        :return:
        """
        # click login
        self.click_area_by_img("signin.png")
        time.sleep(.75 * self.sleep_multi)
        # add email/ username
        self.click_area_by_img("email_login.png")
        pyautogui.typewrite(list(self.login), interval=.025)
        # add passwd
        self.click_area_by_img("passwd_login.png")
        pyautogui.typewrite(list(self.passwd), interval=.025)
        # click login
        time.sleep(.5 * self.sleep_multi)  # give it time to enter login info
        pyautogui.press('enter')
        time.sleep(1 * self.sleep_multi)  # log in speed is slow
        return self

    def click_zoom(self):
        """
        Brings zoom back to the top (foreground)_

        :return:
        """
        if self.os in ["Linux", "Darwin"]:
            os.system("wmctrl -a 'Zoom -'")
        elif self.os == "Windows":
            try:
                self.click_area_by_img("ZoomLogo.png")
            except TypeError:
                print("Tried to raise window to foreground and failed")

    def enter_meeting(self, meeting_url, meeting_password=None, signed_in: bool = True):
        """
        Enters the meeting information and joins the meeting

        Checks if zoom is open
        Clicks the corresponding button to enter the meeting
        Finds the sign in and types in the meeting url
        Finds the password (if needed) and enters that

        :param meeting_url:
        :param meeting_password: if there is one
        :param signed_in:  are you attending from a signed in account ?
        :return:
        """
        if not self.is_zoom_open:
            raise Exception("No Zoom Instance")
        if signed_in:
            time.sleep(5 * self.sleep_multi)   #  incase the login time takes to long
            self.click_area_by_img("login_signed.png", threshold=.95)
        else:
            self.click_area_by_img('join_no_signin.png', threshold=.95)
        time.sleep(2 * self.sleep_multi)
        self.click_area_by_img("join_signed.png", threshold=.95)
        time.sleep(.5 * self.sleep_multi)
        pyautogui.typewrite(list(meeting_url), interval=.025)
        time.sleep(.75 * self.sleep_multi)
        pyautogui.press("enter")
        time.sleep(1 * self.sleep_multi)
        if meeting_password is not None:
            self.click_area_by_img("signed_in_meeting_password.png", threshold=.95)
            time.sleep(.5 * self.sleep_multi)
            pyautogui.typewrite(list(str(meeting_password)), interval=.025)
            pyautogui.press("enter")

    def record_screen(self):
        """
        This is just a screen recording using ffmpeg
        using this over zooms integrated thing to avoid hassling for permissions

        If you change the window, it will record that
        :return:
        """
        save_name = os.path.join(self.save_fol, f"{self.unique_name}_{datetime.now().strftime('%Y-%m-%d')}.mov")
        while os.path.exists(save_name):
            save_name = save_name.replace(".mov", "1.mov")
        if self.os in ["Linux", "Darwin"]:
            command = f"ffmpeg -video_size {self.screen_size[0]}x{self.screen_size[1]} -framerate 10 -f x11grab -i " \
                      f"$DISPLAY -f alsa -ac 2 -i pulse -acodec aac -strict experimental -t {self.duration} " \
                      f"{save_name} >/dev/null 2>&1 & "
            os.popen(command)
        elif self.os == "Windows":
            command = f"ffmpeg -f dshow -i video='UScreenCapture':audio='Microphone' -t {self.duration} " \
                      f"{save_name} >/dev/null 2>&1 & "
            os.popen(command)


