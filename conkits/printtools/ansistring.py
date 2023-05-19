import re
from .basicprinttool import BasicPrintTool


FIND_ANSI_PATTERN = re.compile('\033\\[.*?[a-zA-z]')


def check_reset_code(string):
    """检查是否全是\033[0m"""
    res = re.findall(FIND_ANSI_PATTERN, string)
    for code in res:
        if code != '\033[0m':
            return False
    return True


class AnsiStringMethods(BasicPrintTool):
    """提供ansiString类字符串信息整理的方法"""
    def __init__(self, scrwid=None):
        super().__init__(scrwid)

    def _sort_string(self, string):
        info = []
        search_str = string
        prev_ansi = ''
        while True:
            ansi = re.search(FIND_ANSI_PATTERN, search_str)
            if ansi is None:
                prev_ansi = '' if check_reset_code(prev_ansi) else prev_ansi
                info.append({'ansi': prev_ansi, 'str': search_str, 'len': len(search_str)})
                break
            else:
                ansi_left = ansi.span()[0]
                ansi_right = ansi.span()[1]
            if ansi_left != 0:
                prev_ansi = '' if check_reset_code(prev_ansi) else prev_ansi
                info.append({'ansi': prev_ansi, 'str': search_str[:ansi_left], 'len': len(search_str[:ansi_left])})
                prev_ansi = '' if search_str[ansi_left:ansi_right] == '\033[0m' else search_str[ansi_left:ansi_right]
            else:
                prev_ansi += '\033[0m' if search_str[ansi_left:ansi_right] == '\033[0m' else search_str[ansi_left:ansi_right]
            search_str = search_str[ansi_right:]
        # if info[-1]['ansi'] == '\033[0m':
        #     info[-1]['ansi'] = ''
        # 这时候就说明这部分ansi控制代码应该用类里面预设的了
        # 为防止把'\033[0m'加到末尾ansi控制代码，导致无法使用类里面预设的，所以手动把他设置为空字符
        # pprint(info)
        # print('\033[32m' + '='*80 + '\033[0m')
        return info

    def _sort_string_with_limited_wid(self, single_string, limited_wid, limited_line=None, default_ansi_code='',
                                       is_complete=False):
        """
        它的参数是__sort_prt_string函数的返回结果
        格式如下，记为sorted_info1
        [
            {'ansi': str_value, 'str': str_value, 'len': str_value},
            ...
        ]
        在此基础上根据屏幕宽度重新整理打印的字符串信息
        返回字符串格式
        [
            {
            'is_endl': bool_value,  （代表这一行是否使用了换行符）
            'leftover_wid': int_value,  （这一行剩余宽度）
            'line_wid': int_value, （这一行占的宽度）
            'str_info': [
                            {'str_wid': int_value, 'ansi': str_value, 'str': str_value, 'len': str_value},
                            ...
                        ]  （供打印函数解析的字符串信息）
            }, （这一个字典代表一行的字符串信息）
            ...
        ]  （由于一个选项可以占多个行，所以这个一个列表就储存一个选项的信息，空行用None占位）
        然后再嵌套这个列表，就得到了多个选项的打印信息
        :param single_string: 单个字符串，会按照宽度给这个字符串截断为一种特殊的格式，供PrintLive类的方法打印
        :param limited_wid: 屏幕宽度（实际可）
        :param limited_line: 限制的行数
        :param default_ansi_code: 当字符串某部分ansi代码没有或者为\033[0m的时候，自动加上的ansi代码
        :param is_complete: 决定是否当行数不足限制行数时，补上空行，需要limited_line参数不为None
        :return sorted_info: 上述经整理的字符串信息
        """
        if is_complete:
            if limited_line is None:
                raise ValueError('\033[32;1m当limited_line参数为空时，不能设置is_complete为True\033[0m')
        limited_line = 9999 if limited_line is None else limited_line
        line_count = 0  # 计数行数
        info_list = self._sort_string(single_string)
        sorted_info = [{
            'is_endl': False,
            'leftover_wid': limited_wid,
            'line_wid': 0,
            'str_info': []
        }]
        for info in info_list:
            if line_count >= limited_line:
                break
            current_ansi_code = default_ansi_code if info['ansi'] == '' else info['ansi']  # 当前的ansi代码
            current_str = info['str']  # 当前要剪切的字符串
            current_cut_wid = sorted_info[-1]['leftover_wid']  # 尾行剩余宽度
            cut_str_list = self._cut_str(current_str, current_cut_wid)  # 根据剩余宽度剪切字符串得到字符串列表
            # pprint(cut_str_list)
            first_cut_str = cut_str_list[0]
            first_cut_str_wid = self._wid(first_cut_str)
            if first_cut_str.endswith('\n'):  # 如果第一个字符串是以换行符结尾的
                # 直接附加到尾行（除去换行）
                sorted_info[-1]['str_info'].append(
                    {'str_wid': first_cut_str_wid, 'ansi': current_ansi_code,
                     'str': first_cut_str[:-1], 'len': len(first_cut_str[:-1])})
                # 再设置行已结束
                sorted_info[-1]['is_endl'] = True
            else:
                # 直接附加到尾行
                sorted_info[-1]['str_info'].append(
                    {'str_wid': first_cut_str_wid, 'ansi': current_ansi_code,
                     'str': first_cut_str, 'len': len(first_cut_str)})
            # 修改剩余宽度和当前宽度
            sorted_info[-1]['leftover_wid'] -= first_cut_str_wid
            sorted_info[-1]['line_wid'] += first_cut_str_wid
            is_add_line = False  # 记录是否执行了换行操作
            if sorted_info[-1]['is_endl'] or sorted_info[-1]['leftover_wid'] == 0:
                # 新增空行
                sorted_info.append({'is_endl': False, 'leftover_wid': limited_wid, 'line_wid': 0, 'str_info': []})
                is_add_line = True
                line_count += 1
            if line_count >= limited_line:
                break
            # 如果剪切得到的字符串不止一个
            if len(cut_str_list) > 1:
                if not is_add_line:
                    # 如果上面没换行，但是剪切到的字符列表内容又不止一个，说明也需要换行
                    # 原因是cut_str方法保证字符串的字符不因剪切而丢弃，会出现实际剪切的字符串宽度比给定宽度要小的情况
                    sorted_info.append({'is_endl': False, 'leftover_wid': limited_wid, 'line_wid': 0, 'str_info': []})
                    line_count += 1
                    if line_count >= limited_line:
                        break
                leftover_part_str = ''
                # 拼接剩余字符串
                for cut_str in cut_str_list[1:]:
                    leftover_part_str += cut_str
                # 以屏幕宽度再次剪切，因为这时尾行一定等于屏幕宽度
                cut_str_list = self._cut_str(leftover_part_str, limited_wid)
                # print('第二次剪切', end='')
                # pprint(cut_str_list)
                for idx, cut_str in enumerate(cut_str_list):
                    cut_str_wid = self._wid(cut_str)
                    if cut_str.endswith('\n'):  # 如果第一个字符串是以换行符结尾的
                        # 直接附加到尾行（除去换行）
                        sorted_info[-1]['str_info'].append(
                            {'str_wid': cut_str_wid, 'ansi': current_ansi_code,
                             'str': cut_str[:-1], 'len': len(cut_str[:-1])})
                        # 再设置行已结束
                        sorted_info[-1]['is_endl'] = True
                    else:
                        # 直接附加到尾行
                        sorted_info[-1]['str_info'].append(
                            {'str_wid': cut_str_wid, 'ansi': current_ansi_code,
                             'str': cut_str, 'len': len(cut_str)})
                    # 修改剩余宽度和当前宽度
                    sorted_info[-1]['leftover_wid'] -= cut_str_wid
                    sorted_info[-1]['line_wid'] += cut_str_wid
                    if sorted_info[-1]['is_endl'] or sorted_info[-1]['leftover_wid'] == 0:
                        # 新增空行
                        sorted_info.append(
                            {'is_endl': False, 'leftover_wid': limited_wid, 'line_wid': 0, 'str_info': []})
                        line_count += 1
                        if line_count >= limited_line:
                            break
        # pprint(sorted_info)
        # print('\033[33m' + '=' * 80 + '\033[0m')
        if is_complete:
            while len(sorted_info) < limited_line:
                sorted_info.append({
                    'is_endl': False, 'leftover_wid': limited_wid, 'line_wid': 0,
                    'str_info': [{'str_wid': 0, 'ansi': default_ansi_code, 'str': '', 'len': 0}]})
        return sorted_info


class AnsiString(AnsiStringMethods):
    """
    在区分好ansi作用范围和与可显示字符分离的情况下，
    实现字符串的基本运算操作（主要实现索引，切片，加方法）
    """
    def __init__(self, string):
        super().__init__()
        self.orig_str = string  # 原来的字符串
        self.sorted_str_info = self._sort_string(string)  # 整理过的字符串信息


class AnsiStringWidLimited(AnsiStringMethods):
    """
    在区分好ansi作用范围和与可显示字符分离的情况下，
    将字符串按限制宽度分为多行，
    并实现字符串的基本运算操作（主要实现索引，切片，加方法）
    """
    def __init__(self, string, limited_wid=None):
        super().__init__(limited_wid)
        # 经宽度限制整理的字符串信息
        self.orig_str = string  # 原来的字符串
        self.sorted_str_info_limited = self._sort_string_with_limited_wid(string, self.get_scrwid())

    # 索引方法重载
    def __getitem__(self, item):
        pass

    # 用于给实例返回一个索引值
    def __index__(self):
        pass

