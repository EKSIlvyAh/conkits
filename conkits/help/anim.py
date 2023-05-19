from .predefinedcolors import *
from conkits.ansi import Cursor
from conkits.conio import Conio
from conkits.printtools import DynamicPrint, Choice


def wait_anim0(is_jump=False):
    Cursor.hide()
    string = "press to continue ..."
    ansi_code = Colors256.FORE237
    if is_jump:
        return None
    while True:
        prt_str = ' ' * 20 if ansi_code == 237 else string
        print(ansi_code + prt_str + Style.RESET_ALLs)
        delay = 2 if ansi_code == 237 else 0.04
        ch = Conio.interruptible_sleep(delay)
        Cursor.up(1)
        if ch:
            Conio.erase_line()
            Cursor.show()
            return ch
        ansi_code += 1
        if ansi_code == 255:
            while int(ansi_code) > 237:
                delay = 0.8 if ansi_code == 255 else 0.05
                ansi_code -= 1
                print(ansi_code + prt_str + Style.RESET_ALLs)
                ch = Conio.interruptible_sleep(delay)
                Cursor.up(1)
                if ch:
                    Conio.erase_line()
                    Cursor.show()
                    return ch

