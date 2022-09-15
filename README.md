# Timed Control
Automation script for @SelfControlApp app so you can run it on a desired hour 

# Installation
```bash
git clone https://github.com/DragonTechRoyale/timed_control
cd timed_control
chmod +x install.sh
./install.sh
```

# Usage:
```bash
$ python timed_control.py --block-for <hours:minutes> --start-time <start_hour:start_minute>
```

## Examples:
```bash
$ python timed_control.py --block-for 10:05 --start-time 22:00
Will start SelfControl at 22:00PM for 10 hours and 5 minutes
$ python timed_control.py --block-for 02:25 --start-time 8:00 --verbose
Will start SelfControl at 8:00AM for 2 hours and 25 minutes with debug messages
With no args ($ python timed_control.py) is default, equals to:
$ python timed_control.py --block-for 10:00 --start-time 22:00 -v
```
