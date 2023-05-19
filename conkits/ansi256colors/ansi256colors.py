from conkits.ansi import Style
from .ansi256colorscodes import Codes, codes_set


CSI = '\033['
RESET_ALL = '\033[0m'


ERROR_ANSI_STR = codes_set.FORE9
STYLE_VALUE = []
for name in dir(Style):
    if not name.startswith('_') and not name.endswith('s'):
        STYLE_VALUE.append(getattr(Style, name))
STYLE_VALUE = list(set(STYLE_VALUE))  # 去除重复的值


class Ansi256Colors(Codes):

    __FORE = '\033[38;5;'
    __BACK = '\033[48;5;'

    FORE = ''  # 仅供编辑器查找属性，方便补全代码
    BACK = ''

    RESET_FORE = '\033[39m'
    RESET_BACK = '\033[49m'

    RESET_ALL = '\033[0m'

    def get_fore(self, num, *args):
        return self.__get_value(num, Colors256.__FORE, *args)

    def get_back(self, num, *args):
        return self.__get_value(num, Colors256.__BACK, *args)

    def get_double(self, fore_num, back_num, *args):
        return self.__get_fore_and_back_value(fore_num, back_num, *args)

    def __get_value(self, num, csi_str, *args):
        style_str = ''
        if num < 0 or num > 255:
            raise ValueError(ERROR_ANSI_STR + f'数值{num}超出范围0 - 255' + RESET_ALL)
        for kwarg in args:
            if kwarg not in STYLE_VALUE:
                raise ValueError(ERROR_ANSI_STR + f'数值{kwarg}不正确，值256色的可变参数的值必须存在于Style类' + RESET_ALL)
            style_str += f';{kwarg}'
        style_str += 'm'
        return csi_str + str(num) + style_str

    def __get_fore_and_back_value(self, fore_num, back_num, *args):
        style_str = ''
        if fore_num < 0 or fore_num > 255:
            raise ValueError(ERROR_ANSI_STR + f'前景色数值{fore_num}超出范围0 - 255' + RESET_ALL)
        if back_num < 0 or back_num > 255:
            raise ValueError(ERROR_ANSI_STR + f'背景色数值{fore_num}超出范围0 - 255' + RESET_ALL)
        for arg in args:
            if arg not in STYLE_VALUE:
                raise ValueError(ERROR_ANSI_STR + f'数值{arg}不正确，值256色的可变参数的值必须存在于Style类' + RESET_ALL)
            style_str += f';{arg}'
        style_str += 'm'
        return CSI + '38;5;' + str(fore_num) + ';48;5;' + str(back_num) + style_str

    def show_color_scale(self, num=6):
        """
        0 - 7  标准色
        8 - 15  高强度标准色
        16 - 231  216色
        232 - 255  灰度色
        """
        show_nums_in_line = 1 if num <= 0 else num
        count = 0
        # 打印  0 - 7  标准颜色
        print('  ' + CSI + '1m\n\n标准色\n' + RESET_ALL)
        for num in range(0, 8):
            print(self.get_back(num) + f'  {num}  ' + RESET_ALL, end='')
            if (count + 1) % show_nums_in_line == 0:
                print()
            count += 1
        count = 0
        # 打印  8 - 15  高亮度标准颜色
        print('  ' + CSI + '1m\n\n高强度标准色\n' + RESET_ALL)
        for num in range(8, 16):
            prtstr = f'  {num}  ' if len(str(num)) == 1 else f' {num}  '
            print(self.get_back(num) + CSI + '30m' + prtstr + RESET_ALL, end='')
            if (count + 1) % show_nums_in_line == 0:
                print()
            count += 1
        count = 0
        # 打印  16 - 231  216种颜色
        print('  ' + CSI + '1m\n\n216色\n' + RESET_ALL)
        left_num = 16
        right_num = 33
        for _ in range(6):
            for num in range(left_num, right_num + 1):
                prtstr = f' {num}  ' if len(str(num)) == 2 else f' {num} '
                print(self.get_back(num) + prtstr + RESET_ALL, end='')
                if (count + 1) % show_nums_in_line == 0:
                    print()
                count += 1
            right_num += 19
            left_num = right_num
            right_num += 17
        print()
        count = 0
        left_num = 34
        right_num = 51
        for _ in range(6):
            for num in range(left_num, right_num + 1):
                prtstr = f' {num}  ' if len(str(num)) == 2 else f' {num} '
                print(self.get_back(num) + CSI + '30m' + prtstr + RESET_ALL, end='')
                if (count + 1) % show_nums_in_line == 0:
                    print()
                count += 1
            right_num += 19
            left_num = right_num
            right_num += 17
        count = 0
        # 打印  232 - 255  灰度
        print('  ' + CSI + '1m\n灰度色\n' + RESET_ALL)
        for num in range(232, 256):
            if 232 <= num <= 243:
                print(self.get_back(num) + f' {num} ' + RESET_ALL, end='')
            else:
                print(self.get_back(num) + CSI + '30m' + f' {num} ' + RESET_ALL, end='')
            if (count + 1) % show_nums_in_line == 0:
                print()
            count += 1
        print()


Colors256 = Ansi256Colors()
