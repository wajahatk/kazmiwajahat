from time import sleep
from random import choice


# ---------------------------------------------------------------------------- #
#1 mins - 10 mins
def med_wait(): 
        #Set list of nums for random sleep time:
        sleep_nums = [num for num in range(60, 601)]
        #Return a random sleep time:
        return sleep(choice(sleep_nums))


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    med_wait()