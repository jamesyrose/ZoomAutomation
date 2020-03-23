import os
import platform
import time
import pyautogui
import cv2
import numpy as np
from datetime import datetime

_cwd = os.path.dirname(os.path.abspath(__file__))
_img = os.path.join(_cwd, "SearchImg")
_os = platform.system() # Linux, Windows, OSX -> Darwin


class Zoom():
    def __init__(self, login: str, passwd: str, save_folder: str, unique_name: str):
        self.os = platform.system() # Linux, Windows, OSX -> Darwin
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(self.cwd, "SearchImg")
        self.screen_size = pyautogui.size()  # Tuple(w, h)
        self.login = login
        self.passwd = passwd
        self.save_fol = save_folder
        self.unique_name = unique_name


    @property
    def is_zoom_open(self):
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
        return self

    def launch_zoom(self):
        """
        Will Launch Zoom Application

        Kills all Zoom application first, zoom only allows one instance at a time

        :return:
        """
        if self.os in ["Darwin", "Linux"]:
            os.popen("zoom >/dev/null 2>&1 & ")
            time.sleep(1)  # let app open
        elif self.os == "Windows":
            zoom_exe = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Zoom", "bin", "Zoom.exe")
            os.popen(f"start {zoom_exe}")
        else:
            raise OSError(f"Operating system could not be identified: {self.os}")
        return self

    def login_zoom(self):
        # click login
        self.click_area_by_img("signin.png")
        time.sleep(.75)
        # add email/ username
        self.click_area_by_img("email_login.png")
        pyautogui.typewrite(list(self.login), interval=.025)
        # add passwd
        self.click_area_by_img("passwd_login.png")
        pyautogui.typewrite(list(self.passwd), interval=.025)
        # click login
        time.sleep(.5)  # give it time to enter login info
        pyautogui.press('enter')
        time.sleep(1)
        return self

    def click_zoom(self):
        if self.os in ["Linux", "Darwin"]:
            os.system("wmctrl -a 'Zoom -'")
        elif self.os == "Windows":
            try:
                self.click_area_by_img("ZoomLogo.png")
            except TypeError:
                print("Tried to raise window to foreground and failed")

    def enter_meeting(self, meeting_url, meeting_password=None):
        if not self.is_zoom_open:
            raise Exception("No Zoom Instance")
        self.click_area_by_img("login_signed.png", threshold=.97)
        time.sleep(.75)
        self.click_area_by_img("join_signed.png", threshold=.95)
        time.sleep(.25)
        pyautogui.typewrite(list(meeting_url), interval=.025)
        time.sleep(.5)
        pyautogui.press("enter")
        time.sleep(.75)
        if meeting_password is not None:
            self.click_area_by_img("signed_in_meeting_password.png", threshold=.95)
            time.sleep(.25)
            pyautogui.typewrite(list(str(meeting_password)), interval=.025)
            pyautogui.press("enter")

    def record_screen(self):
        """
        This is just a screen recording using ffmpeg

        If you change the window, it will record that
        :return:
        """
        save_name = os.path.join(self.save_fol, f"{self.unique_name}_{datetime.now().strftime('%Y-%m-%d')}.mov")
        while os.path.exists(save_name):
            save_name = save_name.replace(".mov", "1.mov")
        if self.os in ["Linux", "Darwin"]:
            command = f"ffmpeg -video_size {self.screen_size[0]}x{self.screen_size[1]} -framerate 10 -f x11grab -i " \
                      f"$DISPLAY -f alsa -ac 2 -i pulse -acodec aac -strict experimental -t 30 " \
                      f"{save_name} "
            os.popen(command)
        elif self.os == "Windows":
            command = f"ffmpeg -f dshow -i video='UScreenCapture':audio='Microphone' {save_name} >/dev/null 2>&1 & "
            os.popen(command)








