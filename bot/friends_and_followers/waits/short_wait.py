from time import sleep
from random import choice


# ---------------------------------------------------------------------------- #

#0.5 mins - 1 min
def short_wait(): 
        #Set list of nums for random sleep time:
        sleep_nums = [num for num in range(30, 61)]
        #Return a random sleep time:
        return sleep(choice(sleep_nums))


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    short_wait()