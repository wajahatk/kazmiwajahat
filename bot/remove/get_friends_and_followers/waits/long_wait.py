from time import sleep
from random import choice


# ---------------------------------------------------------------------------- #
def long_wait(): #10 min - 60 mins
        #Set list of nums for random sleep time:
        sleep_nums = [num for num in range(600, 3600)]
        #Return a random sleep time:
        return sleep(choice(sleep_nums))


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    long_wait()