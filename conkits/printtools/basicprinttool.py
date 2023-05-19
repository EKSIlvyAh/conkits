import pprint
import re
import os


ERROR_ANSI_STR = '\033[38;5;9m'
RESET_ALL = '\033[0m'


ANSI_RE = re.compile('\001?\033\\[((?:\\d|;)*)([a-zA-Z])\002?')  # 从colorama复制过来的


def error_str(err_info):
    return ERROR_ANSI_STR + err_info + RESET_ALL


class BasicPrintTool:
    """用于提供基本的print工具函数"""
    @staticmethod
    def _scr_width_limit(scrwid):
        """限制屏幕宽度"""
        if scrwid <= 0:
            raise ValueError(error_str('屏幕宽度数值不能小于0'))
        return scrwid

    def __init__(self, screen_width=None):
        try:
            temp = os.get_terminal_size()[0] if screen_width is None else self._scr_width_limit(screen_width)
        except WindowsError:
            temp = 35
        self.__screen_width = temp
        self.__trace_stack = []

    def set_default_scrwid(self):
        self.__screen_width = os.get_terminal_size()[0]

    def set_scrwid(self, screen_width):
        self.__screen_width = self._scr_width_limit(screen_width)

    def get_scrwid(self):
        return self.__screen_width

    @staticmethod
    def _is_normal_character(char):
        if char.isascii():
            return True

    @staticmethod
    def _is_emoji(content):
        if not content:
            return False
        if u"\U0001F600" <= content <= u"\U0001F64F":
            return True
        elif u"\U0001F300" <= content <= u"\U0001F5FF":
            return True
        elif u"\U0001F680" <= content <= u"\U0001F6FF":
            return True
        elif u"\U0001F1E0" <= content <= u"\U0001F1FF":
            return True
        else:
            return False

    @staticmethod
    def _is_chinese(character):
        """判断单个字符是否为中文字符"""
        if not '\u0e00' <= character <= '\u9fa5':
            return False
        else:
            return True

    @staticmethod
    def _wid(string):
        """返回字符串占屏幕的总宽度"""
        wid = 0
        for char in list(string):
            if char in ['\n', '\r']:
                wid += 0
            if BasicPrintTool._is_chinese(char):
                wid += 2
            elif BasicPrintTool._is_emoji(char):
                wid += 2
            elif BasicPrintTool._is_normal_character(char):
                wid += 1
            else:
                wid += 2
        return wid

    @staticmethod
    def wid(string):
        """返回字符串占屏幕的总宽度"""
        wid = 0
        for char in list(string):
            if char in ['\n', '\r']:
                wid += 0
            if BasicPrintTool._is_chinese(char):
                wid += 2
            elif BasicPrintTool._is_emoji(char):
                wid += 2
            elif BasicPrintTool._is_normal_character(char):
                wid += 1
            else:
                wid += 2
        return wid

    @staticmethod
    def _cut_str(string, max_wid, ignore_endl=False):
        """
        如果超出指定宽度就截断字符串, 并且返回截断后的字符串列表
        :param string: 要剪切的字符串
        :param max_wid: 最大宽度
        :param ignore_endl: 是否忽略换行，如果不忽略，遇到换行符就会进行截断，否则不影响
        :return: 剪切后的字符串列表
        """
        if string == '' or max_wid <= 0:
            return ['']
        string_wid = 0  # 记录字符串的宽度
        cuted_string_list = []  # 截断后的字符串列表
        index = 0
        pre_index = 0  # 记录上一次的索引
        string_list = list(string)
        while index < len(string_list):  # 索引在下面的操作中可能存在回退，所以不用for，用while
            char = string_list[index]
            # 遇到换行直接剪切
            if char == '\n':
                cuted_string_list.append(''.join(string_list[pre_index:index + 1]))
                pre_index = index + 1  # 记录上一次没剪到的字符
                string_wid = 0  # 重置宽度
                index += 1  # 执行完这部操作索引要 +1
                continue
            string_wid += BasicPrintTool._wid(char)  # 判断字符宽度
            if string_wid < max_wid:
                index += 1
                continue  # 如果小于就不执行下面的剪切操作
            elif string_wid == max_wid:
                pass  # 刚好等于的画就可以直接剪切
            else:
                while string_wid > max_wid:  # 超过了要回退索引直到剪切的长度不会超过
                    wid = BasicPrintTool._wid(string_list[index])  # 判断当前字符宽度
                    if wid > max_wid:
                        raise ValueError(f'\033[31;1m单个字符"{string_list[index]}"的宽度{wid}大于给定宽度{max_wid}，无法剪切\033[0m')
                    index -= 1
                    string_wid -= wid
            # 剪切操作  (index+1 是因为列表剪切操作的右边索引位置是不包括的
            cuted_string_list.append(''.join(string_list[pre_index:index + 1]))
            pre_index = index + 1  # 记录上一次没剪到的字符
            string_wid = 0  # 重置宽度
            index += 1  # 执行完这部操作索引要 +1
        # 在执行完上面操作可能出现 遍历完字符串列表 但 长度没超的情况
        if len(string_list[pre_index:index + 1]) != 0:
            cuted_string_list.append(''.join(string_list[pre_index:index + 1]))
        # 这个是处理整个字符串长度都没超的情况
        if len(cuted_string_list) == 0:
            cuted_string_list.append(string)
        return cuted_string_list

    @staticmethod
    def __count_endl_in_string(string):
        endl_count = 0
        for char in list(string):
            if char == '\n':
                endl_count += 1
        return endl_count

    def _trace_cursor_movement(self, string):
        """
        处理逻辑适配格式【\033[...[a-zA-Z]....】
        即\033开始后面接一个字符串，字符串后面不能接csi控制代码，
        这样才能保证反向调用光标控制符时不会出错
        """
        csi_codes = re.findall(ANSI_RE, string)
        for csi_code in csi_codes:
            if csi_code[1] == 'A':
                self.__trace_stack.append(f'\033[{csi_code[0]}B')
            if csi_code[1] == 'B':
                self.__trace_stack.append(f'\033[{csi_code[0]}A')
            if csi_code[1] == 'C':
                self.__trace_stack.append(f'\033[{csi_code[0]}D')
            if csi_code[1] == 'D':
                self.__trace_stack.append(f'\033[{csi_code[0]}C')
            if csi_code[1] == 'E':
                self.__trace_stack.append(f'\033[{csi_code[0]}F')
            if csi_code[1] == 'F':
                self.__trace_stack.append(f'\033[{csi_code[0]}E')
            if csi_code[1] == 'G':
                self.__trace_stack.append(f'\033[{csi_code[0]}G')
            if csi_code[1] == 'H':
                self.__trace_stack.append(f'\033[{csi_code[0]}H')
        endl_count = self.__count_endl_in_string(string)
        if endl_count > 0:
            self.__trace_stack.append(f'\033[{endl_count}F')

    def _clear_trace_stack(self, is_execute=True):
        while len(self.__trace_stack) != 0:
            csi_code = self.__trace_stack.pop()
            if is_execute:
                print(csi_code, end='')

    def _show_stack(self):
        pprint.pprint(self.__trace_stack)


if __name__ == '__main__':
    s = '                  csi_code=Fore.YELLOWs + Colors256.BACK0,'
    print(BasicPrintTool.wid(s))

