"""
    Scheduler example

    See: http://simeonfranklin.com/blog/2012/aug/14/scheduling-tasks-python/

"""



import daemon # install python-daemon from pypi

import sys
import sched
import time
from datetime import datetime as dt
import datetime

def now_str():
"""Return hh:mm:ss string representation of the current time."""
t = dt.now().time()
return t.strftime("%H:%M:%S")


def main():
def do_something_again(message):
print 'RUNNING:', now_str(), message
# Do whatever you need to do here
# then re-register task for same time
# tomorrow
t = dt.combine(dt.now() + datetime.timedelta(days=1), daily_time)
scheduler.enterabs(time.mktime(t.timetuple()), 1, do_something_again, ('Running again',))

# Build a scheduler
# object that will
# look at absolute
# times
scheduler = sched.scheduler(time.time, time.sleep)
print 'START:', now_str()
    # Put
    # task
    # for
    # today
    # at
    # 7am
    # on
    # queue.
    # Executes
    # immediately
    # if
    # past
    # 7am
daily_time = datetime.time(7)
first_time = dt.combine(dt.now(), daily_time)
    # time,
    # priority,
    # callable,
    # *args
        scheduler.enterabs(time.mktime(first_time.timetuple()), 1,
                                do_something_again, ('Run the first time',))
                                    scheduler.run()

                                    if __name__ == '__main__':
                                        if "-f" in sys.argv:
                                                main()
                                                    else:
                                                            with daemon.DaemonContext():
                                                                        main()
