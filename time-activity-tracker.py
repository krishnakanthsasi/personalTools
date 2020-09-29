# -*- coding: utf-8 -*-

from win32gui import GetWindowText, GetForegroundWindow
from win32process import GetWindowThreadProcessId
from psutil import Process
from operator import add
import time
import uiautomation as auto


def printTime(t):
    """
    Takes time in seconds, and print in the output in human friendly format (DD:hh:mm:ss)
    """
    t = round(t)
    if t < 60:
        return ("%d seconds" %t), (0, 0, 0, t)
    else:
        m = int(t/60)
        s = t%60
        if (m < 60) & (m > 1):
            return ("%d minutes, %d seconds" %(m, s)), (0, 0, m ,s)
        elif m == 1:
            return ("%d minute, %d seconds" %(m, s)), (0, 0, m ,s)
        else:
            h = int(m/60)
            m = m%60
            if (h < 24) & (h > 1):
                return ("%d hours, %d minutes, %d seconds" %(h, m, s)), (0, h, m ,s)
            elif h == 1:
                return ("%d hour, %d minutes, %d seconds" %(h, m, s)), (0, h, m ,s)
            else:
                d = int(h/24)
                h = h%24
                if d > 1:
                    return ("%d days, %d hours, %d minutes, %d seconds" %(d, h, m, s)), (d, h, m ,s)
                else:
                    return ("%d day, %d hour, %d minutes, %d seconds" %(d, h, m, s)), (d, h, m ,s)
 

def checkforbrowser():
    '''
    Check whether the input is mozilla, and returns True if so.
    '''
    current_window_id = GetForegroundWindow()
    pid = GetWindowThreadProcessId(current_window_id)
    application_name = Process(pid[-1]).name()
    application_name = application_name.replace(".exe", "")
    if ((application_name == 'firefox') or (application_name == 'chrome')) or (application_name == 'iexplore'):
        return True
    else:
        return False
                   

def getBrowserUrl(current_window_id):
    '''
    Returns the domain url of the active window on the browser app
    '''
    browserControl = auto.ControlFromHandle(current_window_id)
    edit = browserControl.EditControl()
    url = edit.GetValuePattern().Value
    url_string = url.split('/')
    if len(url_string) > 2:
        return (url_string[2])
    elif len(url_string) == 2:
        return (url_string[1])
    else:
        return (url_string[0])

# Defining dictionary for storing values
app_dictionary = {}
                   
                
start = time.time()
last_window_id = GetForegroundWindow()
pid = GetWindowThreadProcessId(last_window_id)
application_name = Process(pid[-1]).name()
application_name = application_name.replace(".exe", "")
print(application_name)
    
while True:
    current_window_id = GetForegroundWindow()
    
    
    if (current_window_id != last_window_id) & (len(GetWindowText(current_window_id)) != 0):
        end = time.time()
        duration, time_tuple = printTime(end-start)
        #print(current_window_id)
        #print(len(GetWindowText(current_window_id)))
        if round(end-start)!=0:
            print(duration)
            try:
                app_dictionary[application_name] = tuple(map(add, time_tuple, app_dictionary[application_name]))
            except KeyError:
                app_dictionary[application_name] = time_tuple
            pid = GetWindowThreadProcessId(current_window_id)
            application_name = Process(pid[-1]).name()
            application_name = application_name.replace(".exe", "")
            print(application_name)
            start = time.time()
            last_window_id = current_window_id
        
            if ((application_name == 'firefox') or (application_name == 'chrome')) or (application_name == 'iexplore'):
                browser_id = current_window_id
                domain_name = getBrowserUrl(current_window_id)
                print(domain_name)
                while browser_id == GetForegroundWindow():
                    new_domain_name = getBrowserUrl(GetForegroundWindow())
                    if new_domain_name != domain_name:
                        print(new_domain_name)
                        domain_name = new_domain_name
                    
                    
                    
#                while checkforbrowser():
#                    new_domain_name = getBrowserUrl(current_window_id)
#                    if new_domain_name != domain_name:
#                        print(new_domain_name)
#                        domain_name = new_domain_name
#        
        
        
        
        

    
