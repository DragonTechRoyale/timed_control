#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
import atomac
import sys
import datetime
import time 


isDebug = False
blockFor = ""
startTime = ""


BundleId = 'org.eyebeam.SelfControl'
usage = """Usage:
$ python timed_control.py --block-for <hours:minutes> --start-time <start_hour:start_minute>

Examples:
$ python timed_control.py --block-for 10:05 --start-time 22:00
Will start SelfControl at 22:00PM for 10 hours and 5 minutes
$ python timed_control.py --block-for 02:25 --start-time 8:00 --verbose
Will start SelfControl at 8:00AM for 2 hours and 25 minutes with debug messages
With no args ($ python timed_control.py) is default, equals to:
$ python timed_control.py --block-for 10:00 --start-time 22:00 -v
"""
defaultMessage = """Setting default, equals to:
$ python timed_control.py --block-for 10:00 --start-time 22:00 -v
"""

def default():
    global isDebug
    global blockFor
    global startTime
    
    isDebug = True
    blockFor = "10:00"
    startTime = "22:00"
    print(defaultMessage)

def failure():
    print(usage)
    exit()


def timeToInt(timeStr):
    # gets a string timeStr in the format hours:minutes and returns a list on ints
    # Example:
    # gets: 12:34
    # returns [12, 34]
    # in case of error retuns empty list []
    
    if ':' not in timeStr:
        return [] # Error
    
    hoursMinutes = timeStr.split(':')
    if len(hoursMinutes) != 2:
        return [] # Error
    
    try:
        hours = int(hoursMinutes[0])
        minutes = int(hoursMinutes[1])
    except:
        return []
    
    return [hours, minutes]

def hoursMinutesToTotalMinutes(timeStr):
    # gets amount of hours and minutes and returns amount in slider value
    # 1 = 0h1m
    # 720 = 12h0m
    # 1440 = 24h0m
    hoursMinutes = timeToInt(timeStr)
    if len(hoursMinutes) != 2:
        return -1 # Error
    hours = hoursMinutes[0]
    minutes = hoursMinutes[1]
    
    total_minutes = minutes + (hours*60)
    if total_minutes > 1440:
        return 1440
    return total_minutes


def setBlocker(items, minutes):
    for item in items:
        if 'AXSlider' in str(item):
            item.AXValue = minutes
            if isDebug:
                print("Slider set to "+str(minutes)+" minutes.")
    for item in items:
        if 'AXButton' in str(item) and 'None' not in str(item) and 'Edit' not in str(item):
            item.Press()
            if isDebug:
                print("Start button is pressed")


def setArgs():
    global isDebug
    global blockFor
    global startTime
    
    args = sys.argv
    
    if len(args) <= 1:
        default()
        return
    
    blockForInArgs = "--block-for" in args
    startTimeInArgs = "--start-time" in args
    
    if blockForInArgs and startTimeInArgs:
        for i in range(len(sys.argv)):
            arg = args[i]
            if arg == '-v' or arg == 'V' or arg == '--verbose':
                isDebug = True
            if arg == "--block-for":
                if not i+1 >= len(args):
                    blockFor = args[i+1]
                else:
                    failure()
            if arg == "--start-time":
                if not i+1 >= len(args):
                    startTime = args[i+1]
                else:
                    failure() 
    else:
        failure()


def main():
    global isDebug
    global blockFor
    global startTime
    
    setArgs()

    atomac.launchAppByBundleId(BundleId)
    time.sleep(5)
    SelfControl = atomac.getAppRefByBundleId(BundleId)
    window = SelfControl.windows()[0]
    items = SelfControl.AXMainWindow.AXChildrenInNavigationOrder

    while True:
        time.sleep(59)
        
        hoursMinutes = timeToInt(startTime)
        startHour = int(hoursMinutes[0])
        startMinutes = int(hoursMinutes[1])

        thisHour = int(datetime.datetime.now().hour)
        thisMinute = int(datetime.datetime.now().minute)

        startNow = startHour == thisHour and startMinutes == thisMinute
        if isDebug:
            print("Starts at: "+str(startHour).zfill(2)+":"+str(startMinutes).zfill(2)+", for: "+blockFor)
            print("Now: "+str(thisHour).zfill(2)+":"+str(thisMinute).zfill(2))
            print("startNow: "+str(startNow))
            
        if startNow:
            totalMinutes = hoursMinutesToTotalMinutes(blockFor)
            if totalMinutes == -1:
                failure()
            setBlocker(items, totalMinutes)
            if isDebug:
                print("Sleeping for 1m")
            time.sleep(60)


if __name__ == '__main__':
    main()
