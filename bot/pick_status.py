from random import choice


# ---------------------------------------------------------------------------- #
def pick_status():
    status_options = [
         "If you were a triangle you'd be acute one.",
        "eBay is so useless. I tried to look up lighters and all they had was 13,749 matches.",
        "(┛ಠ_ಠ)┛彡┻━┻",
        "Check out my creator's portfolio here: https://jharriswebdev.herokuapp.com/ #freelance #webdeveloper #coding #100DaysOfCode",
        "My creator is kind of funny, too. Check him out: @jheeeeezy #bot",
        "@jheeeeezy is the one that created me! Check him out!",
        "Beep boop boop bmmmmmmmmm *~*laser sounds*~* beep",
        "Best bot in the biz, baby! #bot #webdev #coding #python",
        "*- Does robot dance to future music -*",
        "Share a meme with me!",
        "これは英語ではありません！",
        "@jheeeeezy can create a bot for you, too! #bot #freelance #hitmeup #work",
        "https://jharriswebdev.herokuapp.com/ #freelance #webdev",
    ]
    return choice(status_options)


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    pick_status()