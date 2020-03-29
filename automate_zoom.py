#!/usr/bin/python3
import os
from time import sleep
import argparse
import json
from AutoZoom import Zoom
from seleniumDriver import getLogger

cwd = os.path.dirname(os.path.abspath(__file__))
log = getLogger(os.path.join(cwd, ".err.log"))


def attend_meeting(config_path, duration, m_id, m_pass, s_multi, fol, unique_name, login, record):
    """
    Main Parsing and running of Zoom

    Parses args, confirms proper arguments give, and then runs zoom
    If a log in fails, it will not be able to find the 'join meeting' button and thus throw an error
    the sleep_multiplier should be increased if it fails consistently, this will give it more time in between steps
    If there is no password for meeting id, just leave it as None

    :param config_path:
    :param duration:
    :param m_id:
    :param m_pass:
    :param s_multi:
    :param fol:
    :param unique_name:
    :param login:
    :param record:
    :return:
    """
    user, passwd = None, None
    if login:
        try:
            config = json.load(open(config_path))
            user = config['username']
            passwd = config['password']
        except KeyError:
            raise ValueError("Bad JSON Config Given")
    if record:
        if fol is None or unique_name is None:
            raise ValueError("Cannot record with out a folder to save to an a name to give the video,  \n"
                             "Please pass a --unique_course_name and --save_folder argument")

    # >>>>>>>>>>> Zoom
    z_obj = Zoom(login=user, passwd=passwd, zoom_duration=duration, sleep_multiplier=s_multi,
                 save_folder=fol, unique_name=unique_name)
    z_obj.kill_zoom()  # make sure no instance is running preventing start
    try:
        z_obj.launch_zoom()  # launch zoom
    except OSError:
        log.error("failed to launch zoom")
        raise OSError
    try:
        if login:
            z_obj.login_zoom()  # log in
            # enter meeting
            z_obj.enter_meeting(meeting_url=m_id, meeting_password=m_pass, signed_in=True)
        else:
            # enter Meeting
            z_obj.enter_meeting(meeting_url=m_id, meeting_password=m_pass, signed_in=False)
    except (IndexError, OSError, TypeError):
        log.error("Unable To login or enter meeting")
        raise IndexError
    sleep(1 * s_multi)
    if record:
        # record
        z_obj.record_screen()
        # incase zoom is closed early
        while z_obj.is_zoom_open:
            sleep(10)
        os.system('pkill -f ffmpeg')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
                                     """
     --zoom_config_path/-c  : Path to your Zoom login information. this should be a JSON
                              Dictionary with keys 'username' and 'password'. You should
                              use an absolute path if running on cron(str)
     --meeting_id / -m      : ID For meeting that will be joined (str)
     --meeting_pass / -p    : Password for meeting to be joined. Do not pass anything if 
                              the meeting does not have a password. (str)
     --duration / -d        : Duration of lecture in minutes (60 or 90). Only needed if you 
                              are recording (--record / -r) . This limits the time the 
                              screen recording will run for.  (int)
     --sleep_multiplier /-s : If your computer is slow or has a lot of resources already 
                              used, pass a multiplier to allow each step more time (int)
     --save_folder / -f     : Folder to save videos recording to. Only needed if you 
                              are recording. Use Absolute path(str)
     --unique_name / -u     : Unique Name to save it by. The script records it with the date
                              as part of the name. This will be added to make sure you dont 
                              overwrite files when recording multiple in one day. Probably
                              pass the course name (str)
     --record / -r          : Do you want to record  (True / False) (bool)
     --logged_in / -l       : Do you want to log in ? This is needed if you want to 'attend'
                              (True / False) (bool) 
                                     """,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--zoom_config_path', '-c', default=None, type=str)
    parser.add_argument('--meeting_id', '-m', default=None, type=str)
    parser.add_argument('--meeting_pass', '-p', default=None, type=str)
    parser.add_argument('--duration', '-d', default=90, type=int)
    parser.add_argument('--sleep_multiplier', '-s', default=1, type=int)
    parser.add_argument('--save_folder', '-f', default=None, type=str)
    parser.add_argument('--unique_name', '-u', default=None, type=str)
    parser.add_argument('--record', '-r', default=False, type=bool)
    parser.add_argument('--logged_in', '-l', default=False, type=bool)

    arg_parse = parser.parse_args()
    args = vars(arg_parse)

    attend_meeting(config_path=args['zoom_config_path'], m_id=args['meeting_id'], m_pass=args['meeting_pass'],
                   duration=args['duration'], s_multi=args['sleep_multiplier'], fol=args['save_folder'],
                   unique_name=args['unique_name'], login=args['logged_in'], record=args['record'])

