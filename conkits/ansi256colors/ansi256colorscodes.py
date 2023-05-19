CSI = '\033['  
RESET_ALL = '\033[0m'
ERROR_ANSI_STR = '\033[38;5;9m'


class Ansi256ColorsCode:
    def __init__(self, color_code, color_type):
        if color_code < 0 or color_code > 255:
            raise ValueError(ERROR_ANSI_STR + f'数值{color_code}超出范围0 - 255' + RESET_ALL)
        self.color_type = color_type
        if color_type == 'Fore':
            self._256csi = CSI + '38;5;'
        elif color_type == 'Back':
            self._256csi = CSI + '48;5;'
        else:
            raise TypeError(ERROR_ANSI_STR + f'未知256色类型{color_type}' + RESET_ALL)
        self.color_code = color_code
        self.csi_str = self._256csi + str(color_code) + 'm'

    def __add__(self, other):
        """加方法"""
        if isinstance(other, int):
            color_code = (self.color_code + other) % 256
            color_type = 'Fore' if self.color_type == 'Fore' else 'Back'
            return codes_set.get_code_obj(color_code, color_type)
        elif isinstance(other, str):
            return self.csi_str + other
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                color_code = (self.color_code + other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Fore')
            else:
                return self.csi_str + other.csi_str
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                color_code = (self.color_code + other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Back')
            else:
                return self.csi_str + other.csi_str

    def __radd__(self, other):
        """被加方法"""
        if isinstance(other, int):
            color_code = (self.color_code + other) % 256
            color_type = 'Fore' if self.color_type == 'Fore' else 'Back'
            return codes_set.get_code_obj(color_code, color_type)
        elif isinstance(other, str):
            return other + self.csi_str
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                color_code = (self.color_code + other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Fore')
            else:
                return other.csi_str + self.csi_str
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                color_code = (self.color_code + other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Back')
            else:
                return other.csi_str + self.csi_str

    def __sub__(self, other):
        """减方法"""
        if isinstance(other, int):
            color_code = (self.color_code - other) % 256
            color_type = 'Fore' if self.color_type == 'Fore' else 'Back'
            return codes_set.get_code_obj(color_code, color_type)
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                color_code = (self.color_code - other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Fore')
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能相减' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                color_code = (self.color_code - other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Back')
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与BackCode类型不能相减' + RESET_ALL)

    def __rsub__(self, other):
        """被减方法，效果同减方法"""
        return self.__sub__(other)

    def __mul__(self, other):
        """相乘方法"""
        if isinstance(other, int):
            color_code = (self.color_code * other) % 256
            color_type = 'Fore' if self.color_type == 'Fore' else 'Back'
            return codes_set.get_code_obj(color_code, color_type)
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                color_code = (self.color_code * other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Fore')
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能相乘' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                color_code = (self.color_code * other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Back')
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与类BackCode型不能相乘' + RESET_ALL)

    def __rmul__(self, other):
        """被乘方法"""
        return self.__mul__(other)

    def __floordiv__(self, other):
        """相除方法"""
        if isinstance(other, int):
            color_code = (self.color_code // other) % 256
            color_type = 'Fore' if self.color_type == 'Fore' else 'Back'
            return codes_set.get_code_obj(color_code, color_type)
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                color_code = (self.color_code // other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Fore')
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能做整除' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                color_code = (self.color_code // other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Back')
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与类BackCode型不能做整除' + RESET_ALL)

    def __int__(self):
        """供int()调用的方法"""
        return self.color_code

    def __rfloordiv__(self, other):
        """被整除方法"""
        if isinstance(other, int):
            color_code = (other // self.color_code) % 256
            color_type = 'Fore' if self.color_type == 'Fore' else 'Back'
            return codes_set.get_code_obj(color_code, color_type)
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                color_code = (other.color_code // self.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Fore')
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能做整除' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                color_code = (other.color_code // self.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Back')
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与类BackCode型不能做整除' + RESET_ALL)

    def __mod__(self, other):
        """求模方法"""
        if isinstance(other, int):
            color_code = (self.color_code % other) % 256
            color_type = 'Fore' if self.color_type == 'Fore' else 'Back'
            return codes_set.get_code_obj(color_code, color_type)
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                color_code = (self.color_code % other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Fore')
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能做求模运算' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                color_code = (self.color_code % other.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Back')
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与类BackCode型不能做求模运算' + RESET_ALL)

    def __rmod__(self, other):
        """被求模方法"""
        if isinstance(other, int):
            color_code = (other % self.color_code) % 256
            color_type = 'Fore' if self.color_type == 'Fore' else 'Back'
            return codes_set.get_code_obj(color_code, color_type)
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                color_code = (other.color_code % self.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Fore')
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能做求模运算' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                color_code = (other.color_code % self.color_code) % 256
                return codes_set.get_code_obj(color_code, 'Back')
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与类BackCode型不能做求模运算' + RESET_ALL)

    def __str__(self):
        """共给str()函数调用的方法，返回csi字符串"""
        return self.csi_str

    def __repr__(self):
        """ 用来将对象转换成供解释器读取的形式，用来阅读对象的底层继承关系及内存地址"""
        if self.color_type == 'Fore':
            return "'" + '\\033[38;5;' + str(self.color_code) + 'm' + "'"
        else:
            return "'" + '\\033[48;5;' + str(self.color_code) + 'm' + "'"

    def __eq__(self, other):
        """重载等于运算符"""
        if isinstance(other, int):
            return self.color_code == other
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                return self.color_code == other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能比较' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                return self.color_code == other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与类BackCode型不能比较' + RESET_ALL)

    def __lt__(self, other):
        """重载小于运算符"""
        if isinstance(other, int):
            return self.color_code < other
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                return self.color_code < other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能比较' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                return self.color_code < other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与类BackCode型不能比较' + RESET_ALL)

    def __gt__(self, other):
        """重载大于运算符"""
        if isinstance(other, int):
            return self.color_code > other
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                return self.color_code > other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能比较' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                return self.color_code > other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与类BackCode型不能比较' + RESET_ALL)

    def __le__(self, other):
        """重载小于等于运算符"""
        if isinstance(other, int):
            return self.color_code <= other
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                return self.color_code <= other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能比较' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                return self.color_code <= other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与类BackCode型不能比较' + RESET_ALL)

    def __ge__(self, other):
        """重载大于等于运算符"""
        if isinstance(other, int):
            return self.color_code >= other
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                return self.color_code >= other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能比较' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                return self.color_code >= other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与类BackCode型不能比较' + RESET_ALL)

    def __ne__(self, other):
        """重载不等于等于运算符"""
        if isinstance(other, int):
            return self.color_code != other
        elif isinstance(other, ForeCode):
            if self.color_type == 'Fore':
                return self.color_code != other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'BackCode类型与ForeCode类型不能比较' + RESET_ALL)
        elif isinstance(other, BackCode):
            if self.color_type == 'Back':
                return self.color_code != other.color_code
            else:
                raise TypeError(ERROR_ANSI_STR + f'ForeCode类型与类BackCode型不能比较' + RESET_ALL)


class ForeCode(Ansi256ColorsCode):
    def __init__(self, color_code):
        super(ForeCode, self).__init__(color_code, 'Fore')


class BackCode(Ansi256ColorsCode):
    def __init__(self, color_code):
        super(BackCode, self).__init__(color_code, 'Back')


class Codes:
    def __init__(self):
        for num in range(256):
            setattr(self, f'FORE{num}', ForeCode(num))
            setattr(self, f'BACK{num}', BackCode(num))

    def get_code_obj(self, color_code, color_type):
        color_type = 'FORE' if color_type == 'Fore' else 'BACK'
        return getattr(self, color_type + str(color_code))


codes_set = Codes()
