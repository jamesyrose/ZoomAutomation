#!/usr/bin/python3
"""
Should automatically scrape the meetings required

need to do:
parse html code - waiting on actual code to work with (when quarter starts)

"""
import os
import pyautogui
import cv2
import platform
import time
import numpy as np


class LoginScrapper():
    def __init__(self, canvas_url,  sleep_multiplier: int = 1):
        """
        :param canvas_url: url to zoom lti pro page
        :param sleep_multiplier: if your computer is slow youll want to increase sleep times
        """
        self.os = platform.system()  # Linux, Windows, OSX -> Darwin
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(self.cwd, "SearchImg")
        self.screen_size = pyautogui.size()  # Tuple(w, h)
        self.sleep_multi = sleep_multiplier
        self.url = canvas_url

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

    def click_area_by_img(self, img_name, threshold: float = 0.95):
        loc, size = self.find_img_loc(img_path=os.path.join(self.img_dir,
                                                            img_name
                                                            ),
                                      threshold=threshold
                                      )

        pyautogui.moveTo(int((loc[0] + size[0] / 2)), int((loc[1] + size[1] / 2)))
        pyautogui.click()

    def open_chrome(self):
        """
        Opens chrome window
        :return:
        """
        if self.os in ["Darwin", "Linux"]:
            os.popen("google-chrome >/dev/null 2>&1 & ")
            time.sleep(1 * self.sleep_multi)  # let app open
        elif self.os == "Windows":
            os.popen(f"start chrome")
        else:
            raise OSError(f"Operating system could not be identified: {self.os}")
        return self

    def go_to_canvas_url(self):
        if self.os in ["Linux", "Windows"]:
            pyautogui.hotkey("ctrl", "l")
        elif self.os == "Darwin":
            pyautogui.hotkey("command", "l")
        else:
            raise OSError(f"Operating system could not be identified: {self.os}")
        time.sleep(.25 * self.sleep_multi)
        pyautogui.typewrite(list(self.url), interval=.025)
        time.sleep(.25 * self.sleep_multi)
        pyautogui.press("enter")
        time.sleep(1 * self.sleep_multi)

    def download_page_data(self):
        """
        Downloads page source
        :return:
        """
        save_path = os.path.join(self.cwd, '_tmp.html')
        if self.os in ["Linux", "Windows"]:
            pyautogui.hotkey("ctrl", "u")
            time.sleep(1 * self.sleep_multi)
            pyautogui.hotkey('ctrl', 's')
            time.sleep(.5 * self.sleep_multi)
            pyautogui.typewrite(list(save_path))
        elif self.os == "Darwin":
            pyautogui.hotkey("option", 'command', "u")
            time.sleep(1 * self.sleep_multi)
            pyautogui.hotkey('command', 's')
            time.sleep(.5 * self.sleep_multi)
            pyautogui.typewrite(list(save_path))
        else:
            raise OSError(f"Operating system could not be identified: {self.os}")
        time.sleep(1 * self.sleep_multi)

    def check_for_duo(self):
        """
        Will deal with duo if needed

        This is literally the only reason I cannot use selenium...

        Use the 7 day logged in. Otherwise youll have to accept the duo req every time
        and that defeats the prupose in all of this.

        Opening a chromium or firefox instance required me to still pass this.
        Ideally if you already use chrome this will never be needed

        :return:
        """
        time.sleep(3 * self.sleep_multi)  # duo takes a while to load
        duo_push_exists = True
        duo_pushed_exists = True
        try:
            self.click_area_by_img(os.path.join(self.img_dir, "push.png"), threshold=.9)
            duo_push_exists = True
        except ValueError:  # the image search returns none it should throw this error
            duo_push_exists = False
        try:
            self.click_area_by_img(os.path.join(self.img_dir, 'push_pushed.png'), threshold=.9)
            duo_pushed_exists = True
        except ValueError:
            duo_pushed_exists = True
        if duo_pushed_exists or duo_push_exists:
            self.check_for_duo()  # recursively check every 3 seconds
        else:  # if neither exists that means that it has been succesful
            return



