import pprint

from .predefinedcolors import *
from conkits.ansi import Cursor
from conkits.conio import Conio
from conkits.printtools import DynamicPrint, Choice
from .anim import wait_anim0


def interrupted_reminder():
    print(Style.NORMALs + Fore.YELLOWs + '已打断' + Fore.RESETs + '\n')


def description_printer(text_list, printer, print_delay=None, step=None, ansi_code=None):
    """
    专门用于交互式打印文本
    需要传递一个DynamicPrint实例来用于打印
    如果返回True表示要跳出这一级选项
    """
    if not isinstance(printer, DynamicPrint):
        raise TypeError(Fore.LIGHTREDs + '需要传递一个DynamicPrint实例' + Style.RESET_ALLs)
    print_delay = printer.get_print_delay() if print_delay is None else print_delay
    step = printer.get_step() if step is None else step
    ansi_code = printer.get_ansi_code() if ansi_code is None else ansi_code
    is_wait = True
    for text in text_list:
        char = printer.print(text, print_delay=print_delay, step=step, ansi_code=ansi_code)
        # 如果是e键就退出，如果是q键则可以留在后面来判断
        if char is not None:
            char = char.lower()
        if char == 'e':
            is_wait = False
            print_delay = 0.010
            step += 2
        if is_wait:
            char2 = wait_anim0(char in [*escape_characters])
            if char2 in [*escape_characters, None]:
                interrupted_reminder()
                return True
            if char2.lower() == 'e':
                is_wait = False
                print_delay = 0.005
                step += 10
    return False


class IndexManager:
    triangle = f'{Style.RESET_ALLs + Style.BRIGHTs + Fore.CYANs}▶{Style.RESET_ALLs}'
    base_index = f'{triangle} {Fore.WHITEs + Style.DIMs}help{Style.RESET_ALLs} '

    def __init__(self):
        self.cur_idx_color = Fore.GREENs + Style.BRIGHTs
        self.prev_idx_color = Fore.WHITEs + Style.DIMs
        self._cur_idx = IndexManager.base_index
        self._index_list = []

    def append(self, name):
        self._index_list.append(name)

    def pop(self):
        self._index_list.pop()

    @property
    def current_index(self):
        add = ''
        count = 1
        if self._index_list:
            for name in self._index_list[:-1]:
                add += IndexManager.triangle + f' {self.prev_idx_color}' + name + f' {Style.RESET_ALLs}'
                count += 1
                if count % 3 == 0:
                    add += '\n'
                    is_add_endl = True
            add += IndexManager.triangle + f' {self.cur_idx_color}' + self._index_list[-1] + f' {Style.RESET_ALLs}'
        return self._cur_idx + add


C256 = Colors256
im = IndexManager()
normal_lp = DynamicPrint()  # 普通
simply_described_lp = DynamicPrint(print_delay=0.015, step=10)  # 打印简短描述
tips_lp = DynamicPrint(step=2, ansi_code=Style.ITALICs, is_wait=True)  # 打印小提示
interactive_lp = DynamicPrint(print_delay=0.005, step=1)  # 交互式打印


escape_characters = ['Q', 'q']


tips = 'TIPS:\n'\
    '如果不小心选错选项，可以按q/Q退出\n'\
    '按任意键可跳过打印动画\n'\
    '按e/E可跳过交互式描述\n'


simple_description_of_usage = [
    f'{Style.BRIGHTs + Fore.GREENs}USAGE OF CONKITS{Style.RESET_ALLs}\n\n'
    f'如果你使用过colorama\n'
    f'那么你一定能快速上手conkits的基本功能\n'
    f'conkits拥有和colorama相似的功能\n',
    '不过conkits增加了一些新的功能和特性\n',
    '如下所示，目前，可直接从conkits导入8个可调用对象\n' 
    '控制颜色样式：Fore，Back，Style，Colors256\n'
    '控制光标：Cursor\n'
    '功能性：Conio，DynamicPrint，Choice\n',
    '其中Fore，Back，Style，Cursor，Colors256，Conio均为类实例，可直接调用其属性和方法\n'
    '而DynamicPrint，Choice是定义好的类，需初始化生成实例后才可以使用\n'
    '和很多封装了ansi代码的库一样，conkits只是通过ansi代码控制终端的显示行为\n',
    '因此在一些终端下，某些ansi代码可能不起作用，不过大部分的ansi代码还是能够使用\n',
    '为防止出现大量类似conkits.Fore.YELLOWs这样的代码\n',
    '建议使用from conkits import xxx 语句来导入对象\n',
    '如\nfrom conkits import Fore, Back, Style, Colors256\n'
    'from conkits import Conio, DynamicPrint, Choice\n'
    '或者这样\nfrom conkits import *\n'
    '如要解各个对象的用法，请选择下面的选项\n'
]


def usage_of_fore_back_style():
    def attributes():
        def attrs_of_fore_and_back():
            fore_attrs = []
            back_attrs = []
            color_names = [
                '黑色', '红色', '绿色', '黄色', '蓝色', '紫色',
                '青色', '白色', '', '灰色', '亮红色', '亮绿色',
                '亮黄色', '亮蓝色', '亮紫色', '亮青色', '亮白色'
            ]
            for name in dir(Fore):
                if not name.startswith('_') and not name.endswith('s'):
                    fore_attrs.append((name, getattr(Fore, name)))
                    back_attrs.append((name, getattr(Back, name)))

            fore_attrs_list = sorted(fore_attrs, key=lambda x: x[1], reverse=False)
            back_attrs_list = sorted(back_attrs, key=lambda x: x[1], reverse=False)
            print('\nFore的属性')
            print('{: <8}{: >4} {: >7}{: >7}'.format('属性名', '值', '代码', '含义'))
            idx = 0
            for name, value in fore_attrs_list:
                color_name = color_names[idx] if name != 'RESET' else '重置前景色'
                normal_lp.print(f'\033[{value}m' + '{: <14}'.format(name) + Fore.RESETs, end='', step=14)
                normal_lp.print('{: <4}{: >10}{: >5}'.format(value, f'\\033[{value}m', color_name), step=100,
                                print_delay=0.01)
                idx += 1
            print()
            print('Back的属性')
            print('{: <8}{: >4} {: >7}{: >7}'.format('属性名', '值', '代码', '含义'))
            idx = 0
            for name, value in back_attrs_list:
                color_name = color_names[idx] if name != 'RESET' else '重置背景色'
                normal_lp.print(f'\033[{value}m' + '{: <14}'.format(name) + Back.RESETs, end='', step=14)
                normal_lp.print('{: <4}{: >10}{: >5}'.format(value, f'\\033[{value}m', color_name), step=100,
                                print_delay=0.01)
                idx += 1
            print()

        def attrs_of_style():
            style_attrs = []
            color_names = [
                '重置', '明亮', '黯淡', '斜体', '下划线', '反显', '隐藏', '划除',
                '正常', '关闭斜体', '关闭下划线', '关闭反显', '关闭隐藏', '关闭划除'
            ]
            for name in dir(Style):
                if not name.startswith('_') and not name.endswith('s'):
                    style_attrs.append((name, getattr(Style, name)))

            fore_attrs_list = sorted(style_attrs, key=lambda x: x[1], reverse=False)
            print('\nStyle的属性')
            print('{: <8}{: >4} {: >7}{: >9}'.format('属性名', '值', '代码', '含义'))
            idx = 0
            for name, value in fore_attrs_list:
                normal_lp.print('{: <14}'.format(name), end='', step=14)
                normal_lp.print('{: <3}{: >10}{: >8}'.format(value, f'\\033[{value}m', color_names[idx]), step=90)
                idx += 1
            print()

        im.append('attrs')
        attr_options = [
            ' 查看Fore，Back的属性 ',
            ' 查看Style的属性',
            ' 返回上一级菜单'
        ]
        attr_methods = [
            attrs_of_fore_and_back,
            attrs_of_style
        ]
        attr_choice = Choice(options=attr_options, methods=attr_methods)
        attr_choice.set_indents(2, 4)
        normal_lp.print(f'\nPS:这部分建议直接{Fore.REDs}ctrl + 左键{Fore.RESETs}去看代码，里面都有注释\n'
                        f'如果你使用的是手机，那就凑合看看吧', step=2)
        wait_anim0()
        while True:
            print()
            normal_lp.print(im.current_index, step=2)
            n = attr_choice.run()
            if n == len(attr_options) - 1:
                im.pop()
                break

    def description():
        def description_of_fore_and_back():
            description_of_fb = [
                f'因为Fore和Back的属性名完全一致\n'
                f'所以我把这两个放在了一起\n',
                f'Fore设置前景色，Back设置背景色\n'
                f'在使用时，代码看起来大概像这样\n',
                f"string = Fore.GREENs + Back.REDs + 'an example string' + Fore.RESETs + Back.RESETs\n"
                f"print(string)\n",
                f'这样能把字符串设置为绿色字体 + 红色背景\n'
                f'后面再接上Fore.RESETs，Back.RESETs，来分别重置前景和背景设置\n'
                f'这也能防止误给后续的其他字符串设置上颜色\n',
                f'{orange_fore}在使用时要注意，属性名只是整数值，属性名加上s的值才是ansi字符串{Fore.RESETs}\n',
                f'例如下面的代码\n',
                f"print(Fore.LIGHTBLUE + 'maybe this will go wrong' + Fore.RESETs)\n",
                f'运行之后会出现如下报错\n'
                f"{Fore.REDs}TypeError: unsupported operand type(s) for +: 'int' and 'str'{Fore.RESETs}\n",
                f'所以在使用时一定要记得加上s\n',
                f'我自己用的时候也经常出现这样的问题\n'
                f'因为带s后后缀的属性是生成实例后才有的\n'
                f'在用ide写代码时大概率不会有这些属性的代码补全\n'
                f'这时就得靠我们自己去加上s\n',
                f'我考虑过把原有属性直接设置为ansi字符串\n'
                f'但是整数属性在Conio里面会用到\n'
                f'所以仍然保留了这一特性\n'
            ]
            print()
            if description_printer(description_of_fb, interactive_lp):
                return

        def description_of_style():
            description_of_s = [
                f"Style主要用来设置样式\n",
                f"在使用时，代码看起来大概像这样\n",
                f"string = Style.BRIGHTs + 'this string is set to bright' + Style.NORMALs\n"
                f"print(string)\n",
                f"这样能把字符串设置为明亮的样式\n",
                f"其他属性的用法基本一致，就不再重复阐述\n",
                f"在Style中，有些属性的作用可能不太明显\n"
                f"所以我分别解释一下这些属性的作用\n",
                f"RESET_ALL 重置前面的所有设置\n",
                f"它会重置包括颜色，样式，光标隐藏设置\n"
                f"所以有时候会出现，明明之前设置了光标为隐藏，但是后面又莫名显示的问题（不经意间使用了RESET_ALL）\n",
                f"NORMAL  普通\n",
                f"由于不知道怎么取名才准确，我就给他取了个normal\n"
                f"它的作用是使 颜色或者亮度恢复正常\n"
                f"就是说，重置之前设置的前景色，背景色，明亮，黯淡这4个属性\n",
                f"INVERSION  反显\n",
                f"它的作用是交换当前字符串设置的前景色和背景色",
                f"例如下面的代码\n",
                f"string = Fore.YELLOWs + Back.BLACKs + 'inversion exchange fore and back' + Style.RESET_ALLs\n"
                f"print(string)\n"
                f"print(Style.INVERSIONs + string + Style.INVERSION_OFFs)\n",
                f"运行之后的结果为\n",
                f"{Fore.YELLOWs + Back.BLACKs}inversion exchange fore and back{Style.RESET_ALLs}\n"
                f"{Back.YELLOWs + Fore.BLACKs}inversion exchange fore and back{Style.RESET_ALLs}\n",
                f"可以看到这个字符串的前景色和背景色进行了交换\n",
                f"HIDE  隐藏\n",
                f"它会将作用范围之内的字符\n"
                f"在显示时替换成等宽度的空格，以达到不显示的效果\n"
                f"因为只是替换成空格，所以给字符设置的背景色还能显示\n"
                f"{orange_fore}注意，这个属性某些终端可能不支持\n{Fore.RESETs}",
                f"DELETE  划除\n",
                f"它能给显示的字符中间添加一条横线，看起来就像我们平时用笔划除文字一样\n"
                f"大概效果你们可以自己去试，我就不多说了\n",
                f"{orange_fore}注意，具体效果看你们用的终端，有些属性不一定支持，导致用了也没效果，或者跟我描述的略有出入{Fore.RESETs}\n"
                f"我也不方便去标记那些能用那些不能用\n"
                f"所以使用前可以先试试看自己的终端支不支持\n",
                f"如果你不是按顺序看的，或者还没看过Fore，Back的用法\n"
                f"亦或者是还没看过这一段\n",
                f"那么请继续往下看，否则你可以直接按q/Q退出了\n",
                f'{orange_fore}在使用时要注意，属性名只是整数值，属性名加上s的值才是ansi字符串{Fore.RESETs}\n',
                f'例如下面的代码\n',
                f"print(Style.BRIGHT + 'this way to write code is wrong' + Style.NORMAL)\n",
                f'运行之后会出现如下报错\n'
                f"{Fore.REDs}TypeError: unsupported operand type(s) for +: 'int' and 'str'{Fore.RESETs}\n",
                f'带s后置的属性名的值才是字符串，不带的是整数值\n',
                f'所以在使用时一定要记得加上s\n',
                f"否则就会出现 整数 和 字符串 不能相加的报错\n"
            ]
            print()
            if description_printer(description_of_s, interactive_lp):
                return

        simple_description_of_fbs = [
            f'Fore，Back，Style分别是自下面三个类生成的实例：\n'
            f'ansiFore，ansiBack，ansiStyle\n',
            f'这三个类都位于conkits内的ansi模块\n'
            f'但是使用时只需从这三个实例中调用属性\n',
            f'不过要注意\n'
            f'在使用过程中，不要给Fore，Back，Style赋值\n'
            f'否则会丢失原来的引用\n'
        ]
        im.append('description')
        attr_options = [
            ' 查看Fore，Back的用法 ',
            ' 查看Style的用法',
            ' 返回上一级菜单'
        ]
        attr_methods = [
            description_of_fore_and_back,
            description_of_style
        ]
        print()
        if description_printer(simple_description_of_fbs, interactive_lp):
            return
        description_choice = Choice(options=attr_options, methods=attr_methods)
        description_choice.set_indents(2, 4)
        while True:
            print()
            normal_lp.print(im.current_index, step=2)
            n = description_choice.run()
            if n == len(attr_options) - 1:
                im.pop()
                break

    obj_options = [
        ' 查看Fore，Back或Style的属性 ',
        ' 查看Fore，Back或Style的用法 ',
        ' 返回上一级菜单'
    ]
    obj_methods = [
        attributes,
        description
    ]
    fbs_choice = Choice(options=obj_options, methods=obj_methods)
    fbs_choice.set_indents(2, 4)
    im.append('fore back style')
    while True:
        print()
        normal_lp.print(im.current_index, step=2)
        idx = fbs_choice.run()
        if idx == len(obj_options) - 1:
            im.pop()
            break


def usage_of_cursor():
    def callable_methods():
        method_names1 = [
            'up', 'down', 'move_left', 'move_right',
            'hide', 'show',
            'pos', 'hor_pos', 'moveto_linehead',
        ]
        method_args1 = [
            'n=1', 'n=1', 'n=1', 'n=1', '',
            '', 'x=1, y=1', 'x=1', '',
        ]
        use_of_methods1 = [
            '光标上移n行',
            '光标下移n行',
            '光标左移n列',
            '光标右移n列',
            '显示光标',
            '隐藏光标',
            '移动光标到指定列行（x对应列，y对应行）',
            '水平移动光标到指定列',
            '移动光标到该行行首'
        ]
        corresponding_code1 = [
            'nA',
            'nB',
            'nD',
            'nC',
            '?25l',
            '?25h',
            'y;xH',
            'nG',
            '\\r'
        ]
        method_names2 = [
            'moveto_next_line',
            'moveto_prev_line',
            'restore_pos',
            'save_pos',
        ]
        method_args2 = [
            'n=1', 'n=1', '', ''
        ]
        use_of_methods2 = [
            '光标相对于当前位置，往上移动n行，并且回到行首',
            '光标相对于当前位置，往下移动n行，并且回到行首',
            '保存光标位置',
            '恢复光标位置（到之前保存的位置，如果没设置新的位置，默认屏幕开头）'
        ]
        corresponding_code2 = [
            'nE',
            'nF',
            'u',
            's',
        ]
        normal_lp.print(f'\nPS:这部分建议直接{Fore.REDs}ctrl + 左键{Fore.RESETs}去看代码，里面都有注释\n'
                        f'如果你使用的是手机，那就凑合看看吧', step=2)
        wait_anim0()
        normal_lp.print(f'\nCursor所含方法\n{orange_fore}带_s后缀的函数返回ansi字符串，不带的直接执行{Fore.RESETs}\n')
        wait_anim0()
        for idx, name in enumerate(method_names1):
            print(Fore.LIGHTYELLOWs + name + '(' + Fore.RESETs + method_args1[idx] + Fore.LIGHTYELLOWs + ')' + Fore.RESETs)
            print(Fore.LIGHTYELLOWs + name + '_s' + '(' + Fore.RESETs + method_args1[idx] + Fore.LIGHTYELLOWs + ')' + Fore.RESETs)
            print('作用：' + use_of_methods1[idx])
            if name != 'moveto_linehead':
                print('对应ansi代码： \\033[' + corresponding_code1[idx])
            else:
                print('对应转义序列：' + corresponding_code1[idx])
            print()
        wait_anim0()
        normal_lp.print(f'{orange_fore}某些终端可能不支持下面的控制代码{Fore.RESETs}\n')
        wait_anim0()
        for idx, name in enumerate(method_names2):
            print(Fore.LIGHTYELLOWs + name + '(' + Fore.RESETs + method_args2[idx] + Fore.LIGHTYELLOWs + ')' + Fore.RESETs)
            print(Fore.LIGHTYELLOWs + name + '_s' + '(' + Fore.RESETs + method_args2[idx] + Fore.LIGHTYELLOWs + ')' + Fore.RESETs)
            print('作用：' + use_of_methods2[idx])
            print('对应ansi代码： \\033[' + corresponding_code2[idx])
            print()

    def description_of_c():
        details_description = [
            f'Cursor的用法也非常简单\n'
            f'关键是搞清楚各个方法的作用\n'
            f'你们可以自己下去试试，这样比起看别人解释，更好理解\n',
            f'在使用时要注意\n'
            f'带_s后缀的方法会返回字符串，而不带的会直接执行\n'
            f'例如下面的代码\n',
            f"print(1234567, end='')\n"
            f"print(Cursor.move_left_s(6) + 'G')\n"
            f"\n"
            f'这里先打印7个数字，然后设置print不换行\n'
            f'之后通过用print输出光标控制代码来使光标左移6个宽度，然后打印G\n',
            f'这样会使G在2的位置上打印，并且覆盖掉2\n',
            f'运行结果如下\n'
            f'1G34567\n',
            f'或者你可以使用下面这种更加简单明了的写法\n',
            f'使用不带_s后缀的方法\n'
            f"print(1234567, end='')\n"
            f"Cursor.move_left(6)\n"
            f"print('G')\n",
            f"运行之后也是同样的效果\n",
            f'其他方法的用法与上面完全一致\n',
            f'为了逻辑更清晰，我给一些方法加上了数值判断\n',
            f'在使用不带_s后缀的方法时\n'
            f'除开两个定位的pos，hor_pos方法\n'
            f'其他方法如果传递的值n <= 0\n'
            f'则不起任何作用\n',
            f'有些方法的作用不是比较清楚\n'
            f'所以下面我解释一下我认为不太好理解的方法\n',
            f'如果你更喜欢自己操作，或者已经看过，那么你现在可以按q/Q退出了\n',
            f'Cursor.pos(x=1, y=1)  定位光标\n',
            f'它的作用是把光标 移动到 {Fore.YELLOWs}相对于当前屏幕{Fore.RESETs} 的 指定列行\n'
            f'x对应列，y对应行\n',
            f'你可以把它想象成是一个x，y坐标平面\n',
            f'不过这个坐标平面的起始值是1，而不是0\n'
            f'而且有最大值的限制，具体数值看你们自己的终端\n',
            f'比如一个终端的最大高度，宽度分别35，35（一个空格算一个宽度）\n'
            f'那么x和y的数值会被限制在1 - 35\n'
            f'小于1的会自动限制为1，大于35的会自动限制为35\n',
            f'然后有一点需要理解\n'
            f'字符会在光标所在位置打印，不是在光标前面或者后面\n',
            f'该方法对应的控制代码为\\033[y;xH\n'
            f'x，y的位置和我方法参数列表是反过来的\n',
            f'因为行列比较顺口，所以控制代码的参数是y在前，x在后\n',
            f'由于我们在定位光标时，一般习惯xy坐标平面的形式\n'
            f'所以我把在参数里面把顺序改成了x，y\n',
            f'Cursor.hor_pos(x=1)  水平定位光标\n',
            f'它和Cursor.pos的区别是它只控制x坐标，即列坐标\n'
            f'然后其他的和Cursor.pos一致\n',
            f'Cursor.moveto_next_line(n=1)  光标相对当前位置下移n行\n',
            f'这个方法和Cursor.down方法差不多\n'
            f'只不过多了一个回到行首的效果\n'
            f'当传递的参数n=1时，它的作用等同于换行符号\n',
            f'Cursor.moveto_prev_line(n=1)  光标相对当前位置上移n行\n',
            f'它的作用正好和moveto_next_line相反\n'
            f'是往上移动光标，然后其他基本一致\n',
            f'Cursor.save_pos()  保存光标位置\n',
            f'它能让终端保存当前的光标位置（x，y坐标）\n'
            f'然后使用Cursor.restore_pos方法可以让光标回到保存的位置\n'
            f'不过，这个位置还是{Fore.YELLOWs}相对于当前屏幕{Fore.RESETs}\n',
            f'Cursor.restore_pos()  恢复光标位置\n',
            f'他的作用是 恢复光标位置 到最近一次保存 的位置\n'
            f'如果没设置新的位置，默认恢复到屏幕开头（即x=1，y=1的位置）\n',
        ]
        print()
        if description_printer(details_description, interactive_lp):
            return
            # f"\n"
            # f'\n'
    obj_options = [
        ' 查看类方法 ',
        ' 了解用法',
        ' 返回上一级菜单 '
    ]
    im.append('cursor')
    obj_methods = [callable_methods, description_of_c]
    cursor_choice = Choice(options=obj_options, methods=obj_methods)
    cursor_choice.set_indents(2, 4)
    while True:
        print()
        normal_lp.print(im.current_index, step=2)
        idx = cursor_choice.run()
        if idx == len(obj_options) - 1:
            im.pop()
            break


def usage_of_colors256():
    def attributes():
        def example_add_method1():
            fore_code = Colors256.FORE0  # 先获取对Colors256.FORE0的引用
            Cursor.hide()
            for _ in range(256):
                print(fore_code + ' FORE COLOR' + Colors256.RESET_FORE)
                Cursor.up()  # 光标上升一行
                fore_code += 1  # 颜色数值加1
                if Conio.interruptible_sleep(0.05):
                    # 可打断的sleep，如果有返回值，说明触发了按键，就退出循环
                    Cursor.show()
                    break
            Cursor.show()

        def example_add_method2():
            str_code = str([Colors256.FORE0])[2:-2]
            # 由于\033字符不可见，先用这个方式转成可显示的
            print('Colors256.FORE0  对应值' + str_code)
            # 打印此时的值
            Colors256.FORE0 += 20  # 加等于20
            str_code = str([Colors256.FORE0])[2:-2]
            print('Colors256.FORE0  对应值' + str_code)
        description_of_attrs = [
            f"Colors256里面大部分属性都是生成实例之后才有的\n",
            f"所以在用ide写代码时，你不会看到这些属性的代码补全\n",
            f"不过这些属性的命名都很有规律，不用担心记不住\n",
            f"基本5个符串类型的属性如下\n",
            f"FORE，BACK  对应空字符串  仅供ide查找属性属性，方便代码补全\n\n"
            f"RESET_ALL  对应ansi代码  \\033[0m  同Style.RESET_ALLs\n\n"
            f"RESET_FORE  对应ansi代码  \\033[39m  同FORE.RESETs\n\n"
            f"RESET_BACK  对应ansi代码  \\033[49m  同BACK.RESETs\n",
            f"256色的颜色代码范围为 0 - 255 \n",
            f"设置前景色的ansi代码为 \\033[38;5;颜色代码m\n"
            f"对应属性 FORE0 - FORE255\n",
            f"设置背景色的ansi代码为 \\033[48;5;颜色代码m\n"
            f"对应属性 BACK0 - BACK255\n",
            f"只需改变FORE或者BACK后面的数字，即可设置不同的颜色\n",
            f"使用时，代码看起来像下面这样\n",
            f"c256 = Colors256  # 闲打字麻烦的话可以这样写\n\n"
            f"string = c256.FORE208 + 'this string si effected by 256colors' + c256.RESET_FORE\n"
            f"# 设置前景色为颜色代码208对应的颜色（橘黄色）\n\n"
            f"print(f'{{c256.BACK0}} add a back color {{string}} {{c256.RESET_BACK}}')\n"
            f"# 设置黑色背景，可以使用f格式字符串这样的写法，然后打印\n\n"
            f"运行结果如下\n",
            f"{Colors256.BACK0} add a back color {Colors256.FORE208}this string si effected by 256colors{Colors256.RESET_FORE} {Colors256.RESET_BACK}\n",
            f"可以看出基本用法和Fore，Back，Style一样\n"
            f"区别是它不需要再加s后缀了\n",
            ]
        description_of_operation_rules_add = [
            f"除此之外，我还定义一些的运算操作\n",
            f"首先要了解，FORE0 - 255，BACK0 - 255的值不是字符串，而是一个我自定义的一个类的实例\n",
            f"它们分别由ForeCode，BackCode类生成\n",
            f"这两个类都包含256色的ansi控制头和相应的颜色代码\n"
            f"同时，这两个类继承自ansi256ColorsCode类\n",
            f"只要是ansi256ColorsCode类支持的运算，ForeCode，BackCode都支持\n",
            f"ansi256ColorsCode类可以进行的运算操作有\n"
            f"加，减，乘，整除，求模，关系运算\n"
            f"还可以被int()，str()这两个内置函数调用\n",
            f"下面简单介绍一下用法\n",
            f"加  add for ansi256ColorsCode\n",
            f"其实只要详细介绍加方法，其他方法的逻辑也清楚了\n"
            f"所以加方法的描述篇幅会相对比较多\n",
            f"1.ForeCode/BackCode对象和int对象相加\n",
            f"这样会进行如下运算操作\n"
            f"结果 = （当前对象的颜色代码 + 整数值）% 256\n"
            f"返回：结果数值对应的ForeCode/BackCode对象（如果是ForeCode + int，那么结果就是ForeCode对象，BackCode以此类推）\n",
            f"2.ForeCode/BackCode对象与str对象相加\n",
            f"这样会进行如下运算操作\n"
            f"结果 = （ForeCode/BackCode对象对应的ansi代码（字符串） + 字符串）\n"
            f"返回：拼接后的字符串\n",
            f"3.ForeCode/BackCode与ForeCode/BackCode相加\n",
            f"对于这两个对象，只有类型一样才能相加\n"
            f"运算规则跟和int对象相加差不多\n"
            f"结果 = （两个对象的颜色代码数值相加 % 256）\n"
            f"返回：结果数值对应的ForeCode/BackCode对象\n",
            f"注意，除了我上面介绍的3个类型，其他的都不能和ForeCode/BackCode对象进行运算\n",
            f"为了让运算不重复生成实例，我采取了一个比较暴力的方法\n",
            f"在生成ansi256Colors实例时就分别在这个实例中生成了256个ForeCode和256个BackCode对象\n",
            f"也就是说，Colors256对象包含512个ansi256ColorsCode的子类对象\n",
            f"运算结果如果是ForeCode/BackCode对象\n"
            f"就直接返回ansi256ColorsCode实例中对应的ForeCode/BackCode对象的引用\n",
            f"这算是一个折中的办法，虽然防止了重复生成对象，但大部分ForeCode/BackCode对象不一定会用到\n"
            f"所以非必要不要重复使用调用ansi256Colors生成实例\n",
            f"下面是一些示例代码\n",
        ]
        description_of_other_operation = [
            '其余的运算操作的逻辑和加方法基本一致\n',
            '只不过区别是，他们的运算对象都不支持str类了\n'
            '只支持int和ForeCode/BackCode之间的运算\n',
            '- * // % 等运算的逻辑和加方法一样，只是替换了一个运算符号而已\n',
            '同时 * 运算和字符串的不一样，它只是像加方法一样改变颜色代码\n'
            '而不是复制，因为对应ansi字符串来说，复制没有意义\n',
            '同时还有关系运算符\n'
            '比的也只是颜色代码，所以也很好理解\n'
            '剩余的你们可以自己下去试试\n',
        ]
        example_code_for_add_operation = [
            [
                '示例1  在一行用256色打印颜色可变的字符串',
f"""
fore_code = Colors256.FORE0  # 先获取对Colors256.FORE0的引用
Cursor.hide()  # 隐藏光标
for _ in range(256):
    print(fore_code + ' FORE COLOR' + Colors256.RESET_FORE)
    Cursor.up()  # 光标上升一行
    fore_code += 1  # 颜色数值加1
    time.sleep(0.05)  # 延时0.05秒
Cursor.show()  # 运行完之后让光标恢复显示
""",

                f'运行结果如下（{Fore.YELLOWs}可按任意键退出演示{Fore.RESETs}）\n'
            ],

            [
                '\n\n但是要注意，千万别对Colors256中的属性（示例）使用 += 运算\n'
                '否则会丢失原来的引用\n',
                '下面是一个错误的例子\n',
                '示例2 错误地对ansi256ColorsCode对象使用 += 运算\n',
"""
str_code = str([Colors256.FORE0])[2:-2]
# 由于\\033字符不可见，先用这个方式转成可显示的
print('Colors256.FORE0  对应值' + str_code)
# 打印此时的值
Colors256.FORE0 += 20  # 加等于20
str_code = str([Colors256.FORE0])[2:-2]
print('Colors256.FORE0  对应值' + str_code)
# 打印自加之后的值
""",
                f'运行结果如下（{Fore.YELLOWs}可按任意键退出演示{Fore.RESETs}）',
            ],
            [
                '\n通过对比可以看出来\n'
                'Colors256.FORE0已经丢失了原来的引用，指向了Colors.FORE20\n',
                '所以应该使用示例1的写法\n',
            ],
        ]
        example_methods_for_add_operation = [
            example_add_method1,
            example_add_method2
        ]
        print()
        if description_printer(description_of_attrs, interactive_lp):
            return
        if description_printer(description_of_operation_rules_add, interactive_lp):
            return
        if description_printer(example_code_for_add_operation[0], interactive_lp):
            return
        example_methods_for_add_operation[0]()
        if description_printer(example_code_for_add_operation[1], interactive_lp):
            return
        example_methods_for_add_operation[1]()
        if description_printer(example_code_for_add_operation[2], interactive_lp):
            return
        if description_printer(description_of_other_operation, interactive_lp):
            return

    def callable_methods():

        def c256_usage_of_get_fore():
            description_of_c256_get_fore = [
                'Colors256.get_fore(self, num, *args)\n',
                '参数 num：为256色的颜色代码，为int类型，范围0 - 255 \n\n'
                '参数 *args：任意数量的Style代码，为int类型，该数值必须存在与Style对象内\n\n'
                '返回值：256色前景色的ansi代码和控制样式的ansi代码拼接而成的字符串\n\n',
                '作用：如果你想同时设置前景色和样式，可以调用用这个方法\n',
            ]
            example_codes_of_get_fore = [
                [
                    '示例代码\n'
"""
from conkits import Colors256, Style
C256 = Colors256
ansi_head = C256.get_fore(45, Style.BRIGHT, Style.UNDERLINE)
# 等同于代码 ansi_head = C256.FORE45 + Style.BRIGHTs, Style.UNDERLINEs
# 这里就用到了Style的整数值属性
# 如果你记得住Style对应的整数代码，你也可以直接填数字
print(ansi_head + 'example code 1 of Colors256.get_fore' + Style.RESET_ALLs)
""",
                    '运行结果如下\n'
                    f"{Colors256.get_fore(45, Style.BRIGHT, Style.UNDERLINE)}example code 1 of Colors256.get_fore{Style.RESET_ALLs}\n",
                ]
            ]
            print()
            if description_printer(description_of_c256_get_fore, interactive_lp):
                return
            if description_printer(example_codes_of_get_fore[0], interactive_lp):
                return

        def c256_usage_of_get_back():
            description_of_c256_get_fore = [
                'Colors256.get_back(self, num, *args)\n',
                '参数 num：为256色的颜色代码，为int类型，范围0 - 255 \n\n'
                '参数 *args：任意数量的Style代码，为int类型，该数值必须存在与Style对象内\n\n'
                '返回值：256色背景色的ansi代码和控制样式的ansi代码拼接而成的字符串\n\n',
                '作用：如果你想同时背景色和样式，可以调用用这个方法\n',
            ]
            example_codes_of_get_fore = [
                [
                    '示例代码\n'
                    """
from conkits import Colors256, Style
C256 = Colors256
ansi_head = C256.get_back(56, Style.BRIGHT, Style.UNDERLINE)
# 等同于代码 ansi_head = C256.BACK56 + Style.BRIGHTs, Style.UNDERLINEs
# 这里用到了Style的整数值属性
# 如果你记得住Style对应的整数代码，你也可以直接填数字
print(ansi_head + 'example code 1 of Colors256.get_back' + Style.RESET_ALLs)
""",
'运行结果如下\n'
                    f"{Colors256.get_back(56, Style.BRIGHT, Style.UNDERLINE)}example code 1 of Colors256.get_back{Style.RESET_ALLs}\n",
                ]
            ]
            print()
            if description_printer(description_of_c256_get_fore, interactive_lp):
                return
            if description_printer(example_codes_of_get_fore[0], interactive_lp):
                return

        def c256_usage_of_get_double():
            description_of_c256_get_fore = [
                'Colors256.get_double(self, fore_num, back_num, *args)\n',
                '参数 fore_num：为256色的颜色代码（前景），为int类型，范围0 - 255 \n\n'
                '参数 back_num：为256色的颜色代码（背景），为int类型，范围0 - 255 \n\n'
                '参数 *args：任意数量的Style代码，为int类型，该数值必须存在与Style对象内\n\n'
                '返回值：256色前景色 + 背景色的ansi代码和控制样式的ansi代码拼接而成的字符串\n\n',
                '作用：如果你想同时设置前景色，背景色和样式，可以调用用这个方法\n',
            ]
            example_codes_of_get_fore = [
                [
                    '示例代码\n'
"""     
from conkits import Colors256, Style
C256 = Colors256
ansi_head = C256.get_double(0, 208, Style.BRIGHT)
# 等同于代码 ansi_head = C256.FORE0 + C256.BACK208 + Style.BRIGHTs
# 这里就用到了Style的整数值属性
# 如果你记得住Style对应的整数代码，你也可以直接填数字
print(ansi_head + 'example code 1 of Colors256.get_double' + Style.RESET_ALLs)
""",
                    '运行结果如下\n'
                    f"{Colors256.get_double(0, 208, Style.BRIGHT)} example code 1 of Colors256.get_double {Style.RESET_ALLs}\n",
                ]
            ]
            print()
            if description_printer(description_of_c256_get_fore, interactive_lp):
                return
            if description_printer(example_codes_of_get_fore[0], interactive_lp):
                return

        def c256_usage_of_show_color_scale():
            description_of_c256_show_color_scale = [
                'Colors256.show_color_scale(self, num=6)\n',
                '参数 num：一行打印色块的个数，默认值为6\n\n'
                '无返回值\n\n'
                '作用：可以用来查看各个颜色代码对应的颜色\n',
                '主菜单打印色阶调用的时这个函数，相信你们已经看过，就不演示了\n'
            ]
            print()
            if description_printer(description_of_c256_show_color_scale, interactive_lp):
                return

        c256_method_names = [
            ' get_fore',
            ' get_back',
            ' get_double',
            ' show_color_scale ',
            ' 返回上一级菜单 '
        ]
        c256_methods = [
            c256_usage_of_get_fore,
            c256_usage_of_get_back,
            c256_usage_of_get_double,
            c256_usage_of_show_color_scale
        ]
        print()
        normal_lp.print('Colors256所含方法如下', step=2)
        im.append('methods')
        method_choice = Choice(options=c256_method_names, methods=c256_methods)
        method_choice.set_indents(2, 4)
        while True:
            print()
            normal_lp.print(im.current_index, step=2)
            idx = method_choice.run()
            if idx == len(c256_method_names) - 1:
                im.pop()
                break

    def short_description():
        c256_description = [
            f"Colors256是由位于模块conkits.ansi256colors内的ansi256Colors类生成的实例\n",
            f"因为标识符不能用数字开头，所以实例名字和类是相反的\n",
            f"顾名思义，Colors256就是指256种颜色\n",
            f"colorama出于对跨平台和兼容性的考虑\n"
            f"并没有封装256色的ansi代码\n",
            f"而现在大部分终端都支持256色\n"
            f"所以我增加了256色的封装\n",
            f"在后续我还会更新 24bit RGB色彩的ansi代码的封装\n"
            f"不过或许会有些终端不支持，具体能不能用还得看使用的终端\n",
            f"在256色的封装中\n"
            f"我给里面的实例属性定义了一些运算符操作\n"
            f"可以让其用起来更加方便\n",
            f"详细用法请选择上面两个选项\n"
        ]
        print()
        if description_printer(c256_description, interactive_lp):
            return

    obj_options = [
        ' 查看属性介绍',
        ' 查看可调用方法 ',
        ' 查看简介',
        ' 返回上一级菜单',
    ]
    im.append('colors256')
    obj_methods = [attributes, callable_methods, short_description]
    c256_choice = Choice(options=obj_options, methods=obj_methods)
    c256_choice.set_indents(2, 4)
    while True:
        print()
        normal_lp.print(im.current_index, step=2)
        idx = c256_choice.run()
        if idx == len(obj_options) - 1:
            im.pop()
            break


def usage_of_conio():
    def callable_method():
        def example_wait_confirm():
            print('press any key to continue ...')
            Conio.getch()

        def conio_usage_of_erase_line():
            erase_line_description = [
                'PS：带s后缀，会返回ansi字符串\n'
                '    不带的直接执行\n',
                'Conio.erase_line_s(self, mode=2)\n'
                'Conio.erase_line(self, mode=2)\n'
                '擦除行（默认模式2）\n',
                '作用：清除一行的字符\n'
                '对应的ansi字符串为 \\033[modeK\n'
                '有3种模式（如果缺失该参数则认为是模式0，这里我默认选择模式2）\n',
                '模式0：清除光标到该行行尾之间的部分\n'
                '模式1：清除光标到改行行首之间的部分\n'
                '模式2：清除整行\n',
            ]
            example_codes_of_erase_line = [
                '示例代码1  使用模式2(默认参数)清除行',
"""
print('g'*10, end='')
# 打印10个g，设置print不换行
Cursor.move_left(5)
# 光标左移5个宽度
Conio.erase_line()
# 清除行 模式2
""",
                '运行结果为\n'
                '\n',
                '可以看到没有任何显示，说明这一行的字符被清除了',
                '示例代码2  使用模式0清除行\n',

"""
print('g'*10, end='')
Cursor.move_left(5)
print(Conio.erase_line_s(0))
# 清除行 模式0 用打印ansi
""",
                '运行结果为\n'
                'ggggg\n',
                '只显示了前面5个g，说明清除的是光标到该行行尾之间的部分',
                '示例代码3  使用模式1清除行\n',
"""
print('g'*10 + Cursor.move_left_s(5) + Conio.erase_line_s(1))
# 清除行 模式1 一行版写法
""",
                '运行结果为\n'
                '     ggggg',
                '只显示了后面5个g，说明清除的是光标到该行行首之间的部分',
            ]
            print()
            if description_printer(erase_line_description, interactive_lp):
                return
            if description_printer(example_codes_of_erase_line, interactive_lp):
                return

        def conio_usage_of_erase_display():
            erase_display_description = [
                'PS：带s后缀，会返回ansi字符串\n'
                '    不带的直接执行\n',
                'Conio.erase_display_s(self, mode=2)\n'
                'Conio.erase_display(self, mode=2)\n'
                '擦除显示（默认模式2）\n',
                '作用：清除屏幕中显示的字符\n'
                '对应的ansi字符串为 \\033[modeJ\n'
                '共有4种模式（如果缺失该参数则认为是模式0，这里我默认选择模式2）\n',
                '模式0：清除光标位置到屏幕末尾的部分\n'
                '模式1：清除光标位置到屏幕开头的部分\n'
                '模式2：清除整个屏幕\n'
                '模式3：清除整个屏幕并且删除回滚区中所有行（某些终端可能不支持）\n'
            ]
            example_codes_of_erase_display = [
                [
                    '首先我们先测试一下模式1\n'
                    '即清除光标位置到屏幕开头的部分\n'
                    '运行下面代码',
"""
print("0this line won't be erase")
Cursor.up()  
# 这样能把光标移动到上行行首
Conio.erase_display(1)
""",
                ],
                [
                    " this line won't be erase\n"
                    "可以看到，刚刚打印的 this line won't be erase 没有被清除\n"
                    "而当前屏幕能显示到的内容且位于光标前的字符都被清除了\n",
                    "同时前面的0被清除了\n"
                    "说明光标所在位置的字符也会被清除\n",
                    "但是你往前翻的话会发现，没显示到的部分并没有被清除\n"
                    "这些部分就属于回滚区，模式0，1，2都不能清除里面的内容\n",
                    '模式0和模式1差不多，只是清除的方向相反\n'
                    '所以就不写示例了\n',
                    '下面我们看看模式2，也就是默认的模式\n',
                    '这里我们直接运行Conio.erase_display()\n',
                ],
                [
                    '运行过后，屏幕貌似被清除了\n',
                    '但是我们翻看之前打印的记录\n'
                    '会发现前面打印的语句并没有被清除\n',
                    '只是换了很多行，以到达间接清除的效果\n',
                    '如果你确实是想要清除当前屏幕显示的所有内容\n'
                    '那么请使用clrscr()方法\n',
                    '至于模式3\n'
                    '某些终端可能不支持\n'
                    '就不做演示了，同时也不建议使用这个模式\n',
                ]

            ]
            print()
            if description_printer(erase_display_description, interactive_lp):
                return
            if description_printer(example_codes_of_erase_display[0], interactive_lp):
                return
            print("0this line won't be erase")
            Cursor.up()
            # 这样能把光标移动到上行行首
            Conio.erase_display(1)
            if description_printer(example_codes_of_erase_display[1], interactive_lp):
                return
            Conio.erase_display()
            if description_printer(example_codes_of_erase_display[2], interactive_lp):
                return

        def conio_usage_of_clrscr():
            clrscr_description = [
                'PS：带s后缀，会返回ansi字符串\n'
                '    不带的直接执行\n',
                'Conio.clrscr_s(self)\n'
                'Conio.clrscr(self)\n'
                "清屏\n",
                "作用：仅清除屏幕，同时把光标移动到屏幕开头\n",
                "它分别调用erase_display(0)和erase_display(1)\n"
                "清除光标前面和后面的字符\n"
                "然后调用Cursor.pos()\n"
                "来使光标移动到屏幕开头\n"
                '理论上来说是可以起到清屏的效果\n'
            ]
            if description_printer(clrscr_description, interactive_lp):
                return

        def conio_usage_of_init():
            init_description = [
                'PS：带s后缀，会返回ansi字符串\n'
                '    不带的直接执行\n',
                'Conio.init_s(self)\n'
                'Conio.init(self)\n'
                "初始化\n",
                '作用：清除屏幕，并重置所有设置（颜色设置，光标隐藏等）\n',
                '该方法仅仅只是使用ansi字符串\\033c而已\n',
                '跟clrscr一样都有清屏效果\n'
                '但是有点小区别\n',
                'clrscr不会重置所有设置\n\n'
                'init不会把光标移动到屏幕开头\n'
            ]
            print()
            if description_printer(init_description, interactive_lp):
                return

        def conio_usage_of_getch():
            getch_description = [
                'Conio.getch(self)\n'
                '作用：从输入流读取一个字符并返回\n',
                '该方法作用和C语言中的getch()函数一样\n'
                '而且我提供了windows和linux两个系统上的实现\n'
                '只要你使用的不是macOS，我就可以保证它会正常运行\n',
                '如果你没学过C语言或者没用过getch()\n'
                '那么可以继续看下面的解释\n',
                '你可以把Conio.getch()理解为\n'
                '只读取一个字符 而且 不要回车确认的 input()方法\n',
                f'{Fore.LIGHTYELLOWs}不过要注意{Fore.RESETs}\n',
                '一些特殊按键是多个字符组成的\n'
                '如方向键，PgUp，PgDn等\n',
                '同时，如果遇到无法解码的字符（多处于按下特殊键时）\n'
                'Conio.getch()会返回None\n'
            ]
            example_codes_of_getch = [
                [
                    '看下面的示例\n'
"""
print('该程序可以检测你的按键（按q/Q退出）')
while True:
    ch = Conio.getch()
    if ch is None:
        ch = 'None'
    print('按键为' + ch)
    if ch.lower() == 'q':
        break
    # 如果按键是Q/q就退出
print('已退出')
""",
                ],
                [
                    '\n同时你也可以用它来当做等待确认的一个方法\n',
                    '看下面的示例'
"""
def wait_confirm():
    print('press any key to continue ...')
    Conio.getch()
    
print('just a test')
wait_confirm()
""",
                    '运行结果如下\n'
                ]
            ]
            print()
            if description_printer(getch_description, interactive_lp):
                return
            if description_printer(example_codes_of_getch[0], interactive_lp):
                return
            print('运行结果如下\n')
            print('该程序可以检测你的按键（按q/Q退出）')
            while True:
                ch = Conio.getch()
                if ch is None:
                    ch = 'None'
                print('按键为' + ch)
                if ch == 'Q'.lower():
                    break
                # 如果按键是Q/q就退出
            print('已退出')
            if description_printer(example_codes_of_getch[1], interactive_lp):
                return
            print('just a test')
            example_wait_confirm()

        def conio_usage_of_kbhit():
            kbhit_description = [
                "Conio.kbhit(self)\n",
                "作用：检测有无输入，如果有就返回读取到的这个字符，否则返回None\n",
                "它和Conio.getch()不同\n",
                "当执到Conio.getch()时，不会像Conio.kbhit()或input()那样等待输入\n"
                "而是直接检查有无输入，然后继续执行后面的语句\n",
                "这个方法是仿照C语言里面的kbhit函数来实现的\n",
                "它也有windows和linux两个不同的实现\n",
                "不过该方法和C语言里面的kbhit有点不同\n",
                "C语言的kbhit()\n"
                "如果发现有按键输入，返回1，否则返回0\n",
                "Conio.kbhit()\n"
                "如果有发现有按键输入，返回读取到的这个字符，否则返回None\n",
            ]
            example_codes_of_kbhit = [
                [
                    '看下面的示例代码\n'
                    '该代码会在一行实时打印时间，直到按下q/Q键退出'
"""
import time


Cursor.hide()
print('按下Q/q退出')
while True:
    t = time.localtime(time.time())
    localtime = time.asctime(t)
    str = "当前时间:" + time.asctime(t)
    print(str)
    Cursor.up()
    ch = Conio.kbhit()
    if ch is not None:
        ch = ch.lower()
    if ch == 'q':
        Cursor.up()
        break
"""
                ]
            ]
            print()
            if description_printer(kbhit_description, interactive_lp):
                return
            if description_printer(example_codes_of_kbhit[0], interactive_lp):
                return
            import time

            Cursor.hide()
            print('按下Q/q退出')
            while True:
                t = time.localtime(time.time())
                localtime = time.asctime(t)
                str = "当前时间:" + time.asctime(t)
                print(str)
                Cursor.up()
                ch = Conio.kbhit()
                if ch is not None:
                    ch = ch.lower()
                if ch == 'q':
                    Cursor.up()
                    break
            print('\n')

        def conio_usage_of_get_ansistr():
            get_ansistr_description = [
                "Conio.get_ansistr(self, *args)\n"
                "获取ansi字符串\n",
                "参数 args: 任意数量的Fore, Back, Style参数，实际类型为int，无前后顺序\n"
                "返回：对应的ansi字符串\n",
                "作用：当你一次性要设置多个颜色样式，而且你又能记住相应的整数代码时\n"
                "使用该方法较为方便\n",
                "注意参数需存在与Fore, Back, Style对象中\n"

            ]
            example_codes_of_get_ansistr = [
                "示例代码\n"
"""
settings1 = Conio.get_ansistr(Fore.BLUE, Back.YELLOW, Style.BRIGHT)
# 这是一种写法，比较麻烦
# 不如直接用字符串属性相加
settings2 = Conio.get_ansistr(34, 43, 1, 4)
# 当你能记住相应的数值时
# 可以用这种较为简便的方法
# 这里一次性设置了，蓝色前景色，黄色背景，明亮样式，下划线样式
print(settings1 + ' EXAMPLE STRING ' + Style.RESET_ALLs)
print(settings2 + ' EXAMPLE STRING ' + Style.RESET_ALLs)
""",
                "运行结果如下\n"
            ]
            print()
            if description_printer(get_ansistr_description, interactive_lp):
                return
            if description_printer(example_codes_of_get_ansistr, interactive_lp):
                return
            settings1 = Conio.get_ansistr(Fore.BLUE, Back.YELLOW, Style.BRIGHT)
            # 这是一种写法，比较麻烦
            # 不如直接用字符串属性相加
            settings2 = Conio.get_ansistr(34, 43, 1, 4)
            # 当你能记住相应的数值时
            # 可以用这种较为简便的方法
            # 这里一次性设置了，蓝色前景色，黄色背景，明亮样式，下划线样式
            print(settings1 + ' EXAMPLE STRING' + Style.RESET_ALLs)
            print(settings2 + ' EXAMPLE STRING' + Style.RESET_ALLs)
            print()

        def conio_usage_of_packing_str():
            paket_str_description = [
                "Conio.paket_str(self, text, *args)\n"
                '包装字符串\n',
                "参数 text：要包装的字符串，或其他可以被str()调用的类型\n"
                "参数 kwargs：任意数量的Fore, Back, Style参数，实际类型为int\n"
                "返回：整理好的ansi字符串，并在尾部自动附上\033[0m",
                "作用：当你需要给一个字符串设置样式时，不想这些设置影响后续输出时\n"
                "使用该方法会给你提供些许便利\n",
                "注意参数需存在与Fore, Back, Style对象中\n",
            ]
            example_codes_of_packing_str = [
                "示例代码如下\n"
                "以下3种写法效果一样\n"
"""
string = 'a string waited to print'
# 写法1
print(Fore.YELLOWs + Back.BLACKs + Style.BRIGHTs + string + Style.RESET_ALLs)

# 写法2
packed_str = Conio.packing_str(string, Fore.YELLOW, Back.BLACK, Style.BRIGHT)
print(packed_str)

# 写法3
packed_str = Conio.packing_str(string, 33, 40, 1)
print(packed_str)
""",
                "运行结果如下\n"
            ]
            print()
            if description_printer(paket_str_description, interactive_lp):
                return
            if description_printer(example_codes_of_packing_str, interactive_lp):
                return
            string = ' a string waited to print '
            # 写法1
            print(Fore.YELLOWs + Back.BLACKs + Style.BRIGHTs + string + Style.RESET_ALLs)
            # 写法2
            packed_str = Conio.packing_str(string, Fore.YELLOW, Back.BLACK, Style.BRIGHT)
            print(packed_str)
            # 写法1
            packed_str = Conio.packing_str(string, 33, 40, 1)
            print(packed_str)

        def conio_usage_of_interruptible_sleep():
            interruptible_sleep_description = [
                "Conio.interruptible_sleep(\n"
                "                   self, \n"
                "                   delay, \n"
                "                   *break_char_set, \n"
                "                   case_insensitive=False)\n"
                "可打断的sleep\n",
                "参数：delay 延时时长（单位秒）\n"
                "参数：break_char_set 为任意数量触发打断按键字符，留空即为任意键打断\n"
                "参数：case_insensitive 大小写敏感开关\n"
                "返回：触发打断的字符\n",
                "该方法是相对sleep的一些修改\n"
                "使其的延时可以被按键打断\n",
            ]
            example_codes_of_interruptible_sleep = [
                "示例代码如下\n"
                "该代码会等待5秒后退出，或者被你打断后退出\n"
"""
ch = None
for _ in range(5):
    print(f'i am sleeping zzz..., {5 - _} seconds left')
    # 通过查看返回值，来确定是否触发打断
    ch = Conio.interruptible_sleep(1)
    if ch:
        print('Oh fuck, you You interrupted me !')
if ch is None:
    print('emm nice sleeping')
""",

            ]
            print()
            if description_printer(interruptible_sleep_description, interactive_lp):
                return
            if description_printer(example_codes_of_interruptible_sleep, interactive_lp):
                return
            tips = [
                f'{Fore.GREENs}居然硬等了5秒，这样就看不出效果了，要不要重试(Y/N)？{Fore.RESETs}',
                f'{Fore.GREENs}你tm又不按键盘？还要试一次吗(Y/N)？{Fore.RESETs}',
                f'{Fore.GREENs}我靠你这b还想试？(Y/N){Fore.RESETs}',
                f'{Fore.GREENs}吃饱了没事干是吧，帮你退了{Fore.RESETs}',
            ]
            retry_times = 0
            is_quit = False
            print(f"运行结果如下\n提醒：{Fore.YELLOWs}按任意键可以打断{Fore.RESETs}")
            while not is_quit:
                ch = None
                for _ in range(5):
                    print(f'i am sleeping zzz..., {5 - _} seconds left')
                    # 通过查看返回值，来确定是否触发打断
                    ch = Conio.interruptible_sleep(1)
                    if ch:
                        print('Oh fuck, you You interrupted me !')
                        is_quit = True
                        break
                if ch is None:
                    print('emm nice sleeping')
                    if retry_times < 1:
                        prt_tips = tips[0]
                    elif retry_times < 2:
                        prt_tips = tips[1]
                    elif retry_times < 3:
                        prt_tips = tips[2]
                    else:
                        normal_lp.print(tips[3])
                        print('已退出')
                        break
                    normal_lp.print(prt_tips)
                    if input().lower() == 'y':
                        retry_times += 1
                        continue
                    else:
                        print('已退出')
                        break

        im.append('methods')
        conio_method_names = [
            ' erase_line（_s）',
            ' erase_display（_s）',
            ' clrscr（_s）',
            ' init（_s）',
            ' getch',
            ' kbhit',
            ' get_ansistr',
            ' packing_str',
            ' interruptible_sleep ',
            ' 返回上一级菜单 '
        ]
        conio_methods = [
            conio_usage_of_erase_line,
            conio_usage_of_erase_display,
            conio_usage_of_clrscr,
            conio_usage_of_init,
            conio_usage_of_getch,
            conio_usage_of_kbhit,
            conio_usage_of_get_ansistr,
            conio_usage_of_packing_str,
            conio_usage_of_interruptible_sleep
        ]
        conio_methods_choice = Choice(options=conio_method_names, methods=conio_methods)
        conio_methods_choice.set_indents(2, 4)
        while True:
            print()
            normal_lp.print(im.current_index, step=2)
            idx = conio_methods_choice.run()
            if idx == len(conio_method_names) - 1:
                im.pop()
                break

    def description():
        details_description = [
                f'Conio是由位于模块conkits.conio内的Consoleio类生成的实例\n',
                f'这个类的名字来自C语言中的conio.h头文件\n'
                f'因为里面实现了一些conio.h里面很有用的方法\n'
                f'所以我就取名为了Conio\n',
                f'Conio中有一些很有用的方法\n'
                f'如清除屏幕，获取输入等\n'
                f'该类没有需要考虑的属性，只有方法\n',
                f'使用时只需从Conio示例调用方法即可\n'
                f'具体用法请选择选项”查看可调用方法“\n',
            ]
        print()
        if description_printer(details_description, interactive_lp, step=2):
            return
    obj_options = [
        ' 查看可调用方法 ',
        ' 查看简介 ',
        ' 返回上一级菜单 '
    ]
    obj_methods = [
        callable_method,
        description
    ]
    im.append('conio')
    conio_choice = Choice(options=obj_options, methods=obj_methods)
    conio_choice.set_indents(2, 4)
    while True:
        print()
        normal_lp.print(im.current_index, step=2)
        idx = conio_choice.run()
        if idx == len(obj_options) - 1:
            im.pop()
            break


def usage_of_dynamicprint():
    def attribute():
        simple_description_of_dp_attributes = [
            'DynamicPrint类一共有7个可供设置的属性\n',
            '如下所示，这些属性都可以在初始化时设置\n',
            'scrwid  屏幕宽度\n',
            '默认值：os模块中提供的终端最大宽度  int类型\n'
            '数值限制范围：>= 0\n'
            '需要通过get/set方法来获取和设置\n'
            '影响部分打印方法，\n',
            '目前类中可用方法只有print\n'
            '所以该属性暂时不需要考虑\n',
            'print_delay  打印延时\n',
            '默认值 0.012  int类型  单位秒\n'
            '数值限制范围：>= 0\n'
            '需要通过get/set方法来获取和设置\n'
            '每次打印后等待的时间，影响打印的速度\n',
            'ansi_code  ansi字符串\n',
            "默认值：''  str类型\n"
            '需要通过get/set方法来获取和设置\n'
            '影响颜色，样式，光标的ansi字符串\n'
            '可以改变打印时的显示效果\n',
            'step  步长\n',
            '默认值：1  int类型\n'
            '数值限制范围：>= 1\n'
            '需要通过get/set方法来获取和设置\n'
            '影响每次打印的字符个数\n',
            'is_auto_reset  是否自动重置\n',
            '默认值：False  bool类型\n'
            '每次打印结束时，是否重置之前设置的颜色样式\n'
            'True  重置\n'
            'False  不重置\n',
            'is_wait  是否等待\n',
            '默认值：False  bool类型\n'
            '每次打印结束时，是否等待按键\n'
            'True  等待\n'
            'False  不等待\n',
            'is_case_insensitive  是否大小写敏感\n',
            '默认值：False  bool类型\n'
            '影响触发打断打印的字符判断\n'
            'True  敏感\n'
            'False  不敏感\n',
            'interruptible_chars  打断字符列表\n',
            '默认值：[]  list类型\n'
            '用于设置打断打印的触发按键\n',
        ]
        print()
        if description_printer(simple_description_of_dp_attributes, interactive_lp):
            return

    def callable_methods():
        def description_of_dp_method_print():
            description_of_dp_print = [
                'DynamicPrint.print(\n'
                '       self, \n'
                "       *args, \n"
                "       sep=' ', \n"
                "       end='\\n', \n"
                '       ansi_code=None, \n'
                '       print_delay=None,\n'
                '       step=None\n'
                '       is_wait=None, is_auto_reset=None\n'
                '       is_case_insensitive=None\n'
                "       interruptible_chars='unset'\n"
                ')\n'
                "动态打印字符串\n",
                "除开参数*args，sep，end外\n"
                "其余参数如果未提供，会使用类里面的预设值\n"
                '同时这些参数的作用和"查看类属性"里描述的一样\n'
                "就不再重复\n",
                "参数 args： 任意数量的字符串或者可以被str()调用的对象\n"
                "参数 sep： 同print里面的sep，默认为空格\n"
                "参数 end： 同print里面的end，默认为换行\n"
                "返回：如果打印途中被打断，会返回触发打断的那个字符，否则就返回None\n",
                "该方法和内置方法print很像\n"
                "你可以像使用print一样使用它\n"
            ]
            print()
            if description_printer(description_of_dp_print, interactive_lp):
                return

        callable_method_names_of_dp = [
            ' print',
            ' 返回上一级菜单 '
        ]
        callable_methods_of_dp = [
            description_of_dp_method_print
        ]
        im.append('methods')
        callable_methods_choice = Choice(options=callable_method_names_of_dp, methods=callable_methods_of_dp)
        callable_methods_choice.set_indents(2, 4)
        while True:
            print()
            normal_lp.print(im.current_index, step=2)
            idx = callable_methods_choice.run()
            if idx == len(callable_method_names_of_dp) - 1:
                im.pop()
                break

    def example_codes():
        def example_of_init():
            codes = [
                [
                    '1.无参数初始化\n'
                    '示例代码如下\n',
"""
from conkits import DynamicPrint


dp = DynamicPrint()
# 这样会全部使用默认参数
dp.print("你TM真是个小可爱 shabi !@%&#*(&(*4108541")
# 测试一下效果
""",
                    '运行结果如下\n'
                ],
                [
                    '2.可以在初始化的时候通过关键字传递参数\n'
                    '示例代码为\n',
"""
from conkits import DynamicPrint, Fore, Colors256


dp = DynamicPrint(print_delay=0.05,
                  ansi_code=Fore.YELLOWs + Colors256.BACK0,
                  step=2,
                  is_wait=True,
                  is_auto_reset=True,
                  is_case_insensitive=True,
                  interruptible_chars=[
                      'E', '\\n', '\\r'
                  ]
                )
# 也可以在初始化时传递参数
dp.print("你TM真是个小可爱 shabi !@%&#*(&(*4108541")
# 然后测试一下效果
"""
                ],
                [
                    "3.也可以通过类方法和属性赋值来改变参数\n"
                    '示例代码为\n',
"""
from conkits import DynamicPrint, Fore, Colors256


dp = DynamicPrint()
dp.set_print_delay(0.01)
dp.set_ansi_code(Fore.BLUEs + Colors256.BACK0)
dp.set_step(3)
dp.is_wait=True,
dp.is_auto_reset=True,
dp.is_case_insensitive=True,
dp.interruptible_chars.append('\\n')
# append是列表的方法
dp.interruptible_chars = [
    'E', '\\n', '\\r'
    ]
# 也可以直接传递一个新列表，这将替换原来的列表
dp.print("你TM真是个小可爱 shabi !@%&#*(&(*4108541")
# 再测试一下效果
""",
                ],
            ]
            print()
            if description_printer(codes[0], interactive_lp, step=4):
                return
            dp = DynamicPrint()
            # 这样会全部使用默认参数
            dp.print("你TM真是个小可爱 shabi !@%&#*(&(*4108541\n")
            # 测试一下效果
            if description_printer(codes[1], interactive_lp, step=4):
                return
            print('运行结果如下\n')
            dp = DynamicPrint(print_delay=0.05,
                              ansi_code=Fore.YELLOWs + Colors256.BACK0,
                              step=2,
                              is_wait=True,
                              is_auto_reset=True,
                              is_case_insensitive=True,
                              interruptible_chars=[
                                  'E', '\\n', '\\r'
                              ]
                              )
            # 也可以在初始化时传递参数
            dp.print("你TM真是个小可爱 shabi !@%&#*(&(*4108541\n")
            # 然后测试一下效果
            if description_printer(codes[2], interactive_lp, step=4):
                return
            dp = DynamicPrint()
            dp.set_print_delay(0.01)
            dp.set_ansi_code(Fore.BLUEs + Colors256.BACK0)
            dp.set_step(3)
            dp.is_wait = True,
            dp.is_auto_reset = True,
            dp.is_case_insensitive = True,
            dp.interruptible_chars.append('\\n')
            # append是列表的方法
            dp.interruptible_chars = [
                'E', '\\n', '\\r'
            ]
            print('运行结果如下\n')
            # 也可以直接传递一个新列表，这将替换原来的列表
            dp.print("你TM真是个小可爱 shabi !@%&#*(&(*4108541\n")
            # 再测试一下效果

        def example_of_print():
            codes = [
                [
                    "最简单的使用方法在初始化里面讲过\n"
                    "下面分别说明一下各个参数对print的影响\n",
                    "参数print_delay对print的影响\n",
                    "首先我们把print_delay设置为1\n"
                    "示例代码如下\n",
"""
from conkits import DynamicPrint


dp = DynamicPrint()
test_str = '0123456789'
dp.print(test_str, print_delay=1)
""",
                    "运行结果为\n"
                ],
                [
                    "可以看到打印得很慢\n",
                    "如果把print_delay设置为0呢\n"
                    "示例代码如下\n",
                    """
from conkits import DynamicPrint


dp = DynamicPrint()
test_str = '0123456789'
dp.print(test_str, print_delay=0)
                    """,
                    "运行结果为\n"
                ],
                [
                    "几乎一瞬间就打印完了，和print一样\n",
                    "参数step对print的影响\n",
                    "为了更清晰的理解step\n"
                    "我们把延时设置为1秒\n",
                    "然后看步长为2时的效果\n"
                    "示例代码如下\n",
                    """
from conkits import DynamicPrint


dp = DynamicPrint()
test_str = '0123456789'
dp.print(test_str, print_delay=1, step=2)
                    """,
                    "运行结果为\n"
                ],
                [
                    "可以很清除的看到，每次都打印2个字符\n",
                    "不过step的数值必须 >= 1\n"
                    "当你设置的数值 < 1会自动限制为1\n",
                    "下面我们看看step大于字符串长度的情况\n",
                    "示例代码如下\n",
                    """
from conkits import DynamicPrint


dp = DynamicPrint()
test_str = '0123456789'
dp.print(test_str, print_delay=1, step=50)
# 步长明显大于字符串,
                    """,
                    "运行结果为\n"
                ],
                [
                    "也是一次性就打印完了\n",
                    "下面看看ansi_code对print的影响\n",
                    "这里我们使用的字符串中间的部分，也被设置了ansi字符串，为绿色前景色\n"
                    "然后参数ansi_code设置为Fore.YELLOWs（黄色）\n",
                    "示例代码如下\n",
                    """
from conkits import DynamicPrint, Fore, Style


dp = DynamicPrint()
test_str = f'0123{Fore.GREENs}45{Style.RESET_ALLs}6789'
dp.print(test_str, ansi_code=Fore.YELLOWs)
                    """,
                    "运行结果为\n"
                ],
                [
                    "这里可以发现\n",
                    "没在字符串中设置ansi字符串的部分显示为黄色\n",
                    "也就是说不被所给字符串中的ansi字符串影响的部分\n"
                    "会被参数ansi_code影响\n",
                    "下面再看一个例子\n"
                    "这次我们用Fore.RESETs结尾，而不是Style.RESETs\n",
                    "示例代码如下\n",
                    """
from conkits import DynamicPrint, Fore, Style


dp = DynamicPrint()
test_str = f'0123{Fore.GREENs}45{Fore.RESETs}6789'
dp.print(test_str, ansi_code=Fore.YELLOWs)    
                    """,
                    "运行结果为\n"
                ],
                [
                    "现在我们发现\n",
                    "只有前半部分被设置了黄色\n",
                    "后面除开绿色的部分都没设置颜色\n",
                    "为什么会出现这种情况？\n",
                    "这是因为只有被\\033[0m的影响的部分才会被设置为参数ansi_code的颜色\n"
                    "（Style.RESET_ALLs即\\033[0m）\n",
                    "而Fore.RESETs是\\033[39m\n",
                    "所以被它影响的部分没有如期被参数ansi_code的颜色\n",
                    "如果我们只想要字符串中一部分单独设置ansi字符串\n"
                    "其他部分使用参数ansi_code的颜色\n",
                    "那么这单独设置的部分一定要以Style.RESET_ALLs结尾\n",
                    "参数interruptible_chars\n",
                    "这个参数很好理解，设置为None或者[]\n"
                    "这样任意按键都能打断\n",
                    "那如果要是不想被打断呢？\n",
                    "这时只需要把打断字符设置为空字符即可\n"
                    "示例代码如下\n",
                    """
from conkits import DynamicPrint


dp = DynamicPrint()
test_str = f'0123456789'
print('现在按键试试看能不能打断')
dp.print(test_str, print_delay=0.2, interruptible_chars=[''])      
                    """,
                    "运行结果为\n"
                ],
                [
                    "\n看得出来，无论按什么键都不会打断\n",
                    "其他的参数作用都很好理解\n"
                    "就不写示例了（主要是特别麻烦）\n"
                ]
            ]
            print()
            if description_printer(codes[0], interactive_lp, step=4):
                return
            dp = DynamicPrint()
            test_str = '0123456789'
            dp.print(test_str, print_delay=1)
            if description_printer(codes[1], interactive_lp, step=4):
                return
            dp = DynamicPrint()
            test_str = '0123456789'
            dp.print(test_str, print_delay=0)
            if description_printer(codes[2], interactive_lp, step=4):
                return
            dp = DynamicPrint()
            test_str = '0123456789'
            dp.print(test_str, print_delay=1, step=2)
            if description_printer(codes[3], interactive_lp, step=4):
                return
            dp = DynamicPrint()
            test_str = '0123456789'
            dp.print(test_str, print_delay=1, step=50)
            if description_printer(codes[4], interactive_lp, step=4):
                return
            dp = DynamicPrint()
            test_str = f'0123{Fore.GREENs}45{Style.RESET_ALLs}6789'
            dp.print(test_str, ansi_code=Fore.YELLOWs)
            if description_printer(codes[5], interactive_lp, step=4):
                return
            dp = DynamicPrint()
            test_str = f'0123{Fore.GREENs}45{Fore.RESETs}6789'
            dp.print(test_str, ansi_code=Fore.YELLOWs)
            if description_printer(codes[6], interactive_lp, step=4):
                return
            dp = DynamicPrint()
            test_str = f'0123456789'
            print('现在按键试试看能不能打断')
            dp.print(test_str, print_delay=0.2, interruptible_chars=[''])
            if description_printer(codes[7], interactive_lp, step=4):
                return

        example_codes_of_dp = [
            ' 初始化DynamicPrint类',
            ' 使用DynamicPrint.print打印字符串 ',
            ' 返回上一级菜单 '
        ]
        example_methods_of_dp = [
            example_of_init,
            example_of_print
        ]
        im.append('example codes')
        callable_methods_choice = Choice(options=example_codes_of_dp, methods=example_methods_of_dp)
        callable_methods_choice.set_indents(2, 4)
        while True:
            print()
            normal_lp.print(im.current_index, step=2)
            idx = callable_methods_choice.run()
            if idx == len(example_codes_of_dp) - 1:
                im.pop()
                break

    def simple_description():
        details_description = [
            "DynamicPrint是一个包含各种打印方法的工具类\n",
            "不过目前这个类并不完善\n",
            "能用只有一个print方法\n",
            "在使用这个类时\n",
            "你既可以通过设置类属性来设置打印方法的默认参数\n",
            "也可以单独给类方法设置参数\n",
            "后续的所有打印方法都会按照这一思路来编写\n",
            "了解详细用法请选择其他选项\n",
            "\n",
        ]
        print()
        if description_printer(details_description, interactive_lp):
            return

    obj_options = [
        ' 查看类属性',
        ' 查看可调用方法  ',
        ' 查看示例代码',
        ' 查看简介',
        ' 返回上一级菜单 '
    ]
    im.append('dynamic print')
    obj_methods = [
        attribute,
        callable_methods,
        example_codes,
        simple_description
    ]
    dynamicprint_choice = Choice(options=obj_options, methods=obj_methods)
    dynamicprint_choice.set_indents(2, 4)
    while True:
        print()
        normal_lp.print(im.current_index, step=2)
        idx = dynamicprint_choice.run()
        if idx == len(obj_options) - 1:
            im.pop()
            break


def usage_of_choice():
    def attribute():
        simple_description_of_dp_attributes = [
            "Choice类目前一共有10个可设置的属性\n"
            "以下参数均可在初始化时设置\n",
            'scrwid  屏幕宽度\n',
            '默认值：os模块中提供的终端最大宽度  int类型\n'
            '数值限制范围：>= 0\n'
            '需要通过get/set方法来获取和设置\n'
            '该参数在Choice类中非常重要\n',
            '它会影响可打印的选项长度\n'
            '如果选项太长超出了屏幕宽度会进行截断\n',
            "options  要打印的选项列表\n",
            '需要通过get/set方法来获取和设置\n'
            f"{Fore.LIGHTYELLOWs}首先需要强调一点{Fore.RESETs}\n",
            f"千万别在作为选项的字符串中使用{Fore.LIGHTYELLOWs}光标控制符{Fore.RESETs}\n"
            "包括\\b，\\r，\\n这些转义字符\n",
            f"{Fore.LIGHTREDs}否则会出现显示错误{Fore.RESETs}\n",
            "但是在选项字符串中使用ansi字符串添加颜色和样式是允许的\n"
            "这样你能给选项的某个部分设置单独设置样式\n",
            "methods  选项对应的方法列表\n",
            '需要通过get/set方法来获取和设置\n'
            "一个选项对应一个方法\n"
            "按列表索引一一对应\n",
            "如果传递的方法少于选项个数（前提方法列表长度不为0）\n"
            "会自动填充空函数（什么也不干的函数）\n",
            "如果传递的方法多余选项个数\n"
            "多余的会被忽略\n",
            "sep_line  每个选项的间隔行数\n",
            "默认值：0  int类型\n"
            "数值范围：>= 0\n"
            '需要通过get/set方法来获取和设置\n'
            "影响每个选项的间隔行数\n"
            "不过大多数情况下你不会设置这个属性\n",
            "unchecked_indents  没选中选项缩进\n",
            "默认值：0  int类型\n"
            "数值范围：>= 0 and <= scrwid\n"
            '需要通过get/set方法来获取和设置\n'
            "影响打印时未选中选项的缩进\n",
            "checked_indents  被选中选项缩进\n",
            "默认值：0  int类型\n"
            "数值范围：>= unchecked_indents and <= scrwid\n"
            '需要通过get/set方法来获取和设置\n'
            "影响打印时选中选项的缩进\n",
            "和unchecked_indents拉开恰当差值的话\n"
            "可以增强被选中的效果\n",
            "key_setting  键位设置\n",
            "默认值：\n"
            "{\n"
            "   'up': 'w', 'down': 's', \n"
            "   'confirm': ['e', '\\r', '\\n']\n"
            "}\n"
            "dict类型\n"
            '需要通过get/set方法来获取和设置\n'
            "就是字面意义的键位设置\n",
            "每个键位对应的可以是字符，也可是包含字符列表\n",
            "checked_ansi_code  被选中时，选项使用的ansi字符串\n",
            "影响选中时选项的显示效果\n"
            "建议此参数不设置前景色\n",
            "unchecked_ansi_code  未选中时，选项使用的ansi字符串\n",
            "影响未选中时选项的显示效果"
            "建议此参数不设置背景色\n",
            "click_ansi_code  确认时，选项使用的ansi字符串\n",
            "影响未选中时选项的显示效果\n",
            "is_pop  打印选项时是否需要弹出式效果\n",
            "默认值：True  类型bool\n"
            "True  开启\n"
            "False  关闭\n",
        ]
        print()
        if description_printer(simple_description_of_dp_attributes, interactive_lp):
            return

    def example_codes():

        def p1():
            print('You choice the option 1')
            print('press any key to continue')
            Conio.getch()

        def p2():
            print('You choice the option 2')
            print('press any key to continue')
            Conio.getch()

        def p3():
            print('You choice the option 3')
            print('press any key to continue')
            Conio.getch()

        def p4():
            print('You choice the option 4')
            print('press any key to continue')
            Conio.getch()

        example_options = [
            '测试选项1',
            '测试选项2',
            '测试选项3',
            '测试选项4'
        ]
        example_options_prf = [
            ' 测试选项1 ',
            ' 测试选项2 ',
            ' 测试选项3 ',
            ' 测试选项4 ',
            ' 返回 '
        ]
        example_methods = [
            p1,
            p2,
            p3,
            p4
        ]

        def example_of_init():
            codes = [
                [
                    "在下面的示例中，按键设置都如下\n",
                    "w -> 上\n"
                    "s -> 下\n"
                    "e/回车 -> 确认\n",
                    "1.不带参数初始化\n",
                    "这时候虽然可以成功初始化\n"
                    "但是选项完全不能运行\n"
                    "如果对其调用run方法则不起任何作用\n"
                    "示例代码如下\n",
"""
from conkits import Choice


example_choice = choice()
example_Choice.run()
# 运行入口方法
"""
                    "运行结果为\n"
                ],
                [
                    "果不其然，什么也没发生\n",
                    "如果想要其能运行\n",
                    "需要才初始化时通过options关键参数添加选项列表\n"
                    "或者通过set_options方法添加选项\n",
                    "不过要注意，重新设置选项会覆盖掉之前的选项\n",
                    "2.使用set_options方法重设选项\n"
                    "示例代码如下\n",
"""
from conkits import Choice


example_options1 = [
    '测试选项1',
    '测试选项2',
    '测试选项3',
    '测试选项4'
]
example_options2 = [
    '测试选项5',
    '测试选项6',
    '测试选项7',
    '测试选项8'
]
print('初始化时设置的选项')
example_choice = Choice(options=example_options1)
example_choice.run()
print('通过set_options设置的选项')
example_choice.set_options(example_options2)
example_choice.run()
""",
                    "运行结果为\n"
                ],
                [

                    "\n很明显，第二次设置选项时，覆盖掉了原来的选项\n",
                    "现在我们来试试添加一个方法列表\n",
                    "3.添加方法列表\n"
                    "示例代码如下\n",
"""
from conkits import Choice


def p1():
    print('You choice the option 1')
    print('press any key to continue')
    Conio.getch()
    
    
def p2():
    print('You choice the option 2')
    print('press any key to continue')
    Conio.getch()
    
    
def p3():
    print('You choice the option 3')
    print('press any key to continue')
    Conio.getch()
    
    
def p4():
    print('You choice the option 4')
    print('press any key to continue')
    Conio.getch()
    
    
example_options = [
    '测试选项1',
    '测试选项2',
    '测试选项3',
    '测试选项4'
]
example_methods = [
    p1,
    p2,
    p3,
    p4
]                    
example_choice = Choice(
    options=example_options,
    methods=example_methods
)
example_choice.run()
print('press any key to quit')        
""",
                    "运行结果为\n"
                ],
                [
                    "\n但除了添加选项和方法之外\n",
                    "你还可以在初始化时就传递一些其他参数\n"
                    "来修改默认的属性\n"
                    "初始化方法的函数头如下\n",
"""
Choice.__init__(self,
         scrwid=None,
         options=None,
         methods=None,
         sep_line=None,
         checked_ansi_code=None,
         unchecked_ansi_code=None,
         click_ansi_code=None,
         unchecked_indents=None,
         checked_indents=None,
         is_pop=True)   
""",
                    "上面的各个参数的作用在选项“查看类属性”都有过解释\n"
                    "若不清楚可以再回去看看\n",
                ],
            ]
            print()
            if description_printer(codes[0], interactive_lp, step=4):
                return
            example_choice = Choice()
            example_choice.run()
            if description_printer(codes[1], interactive_lp, step=4):
                return
            example_options1 = [
                '测试选项1',
                '测试选项2',
                '测试选项3',
                '测试选项4'
            ]
            example_options2 = [
                '测试选项5',
                '测试选项6',
                '测试选项7',
                '测试选项8'
            ]
            print('初始化时设置的选项')
            example_choice = Choice(options=example_options1)
            example_choice.run()
            print('通过set_options设置的选项')
            example_choice.set_options(example_options2)
            example_choice.run()
            if description_printer(codes[2], interactive_lp, step=4):
                return
            example_choice = Choice(
                options=example_options,
                methods=example_methods
            )
            example_choice.run()
            print('press any key to quit')
            if description_printer(codes[3], interactive_lp, step=4):
                return

        def example_of_quickly_create_choice():
            codes = [
                [
                    "在初始化中，我们创建的选项都是一次性的\n",
                    "那如果想创建一个可复用的选项呢？\n",
                    "只要加上循环\n"
                    "添加一个退出选项就行了\n",
                    "这里我们cv一点前面的示例代码\n",
                    "示例代码如下\n"
"""
from conkits import Choice


def p1():
    print('You choice the option 1')
    print('press any key to continue')
    Conio.getch()
    
    
def p2():
    print('You choice the option 2')
    print('press any key to continue')
    Conio.getch()
    
    
def p3():
    print('You choice the option 3')
    print('press any key to continue')
    Conio.getch()
    
    
def p4():
    print('You choice the option 4')
    print('press any key to continue')
    Conio.getch()
    
    
example_options = [
    '测试选项1',
    '测试选项2',
    '测试选项3',
    '测试选项4,
    '退出'
]
example_methods = [
    p1,
    p2,
    p3,
    p4
]                    
qc = Choice(
    options=example_options,
    methods=example_methods
)
while True:
    idx = qc.run()
    if idx == len(example_options) - 1:
        break
    # 如果返回索引是最后一个，就直接退出
"""
                    "运行结果为\n",
                ],
                [
                    "\n现在选项已经基本能用了\n",
                    "如果你观察后面的代码\n"
                    "会发现这里退出选项使用了run方法的返回值\n",
                    "run方法会返回被确认选项的列表索引\n",
                    "如果返回的索引是 列表长度 - 1\n"
                    "也就是最后一个选项\n",
                    "就直接break退出循环\n",
                ]
            ]
            print()
            if description_printer(codes[0], interactive_lp, step=4):
                return
            example_options.append('退出')
            qc = Choice(
                options=example_options,
                methods=example_methods
            )
            while True:
                idx = qc.run()
                if idx == len(example_options) - 1:
                    break
            example_options.pop()
            if description_printer(codes[1], interactive_lp, step=4):
                return

        def example_of_custom_display_effect():
            codes = [
                [
                    "如果你不喜欢默认的样式\n",
                    "你可以通过以下参数来更改\n",
                    "unchecked_ansi_code\n"
                    "默认的值为\n"
                    "Colors256.FORE255 + Style.DIMs\n\n"
                    "checked_ansi_code\n"
                    "默认的值为\n"
                    "Colors256.BACK64 + Colors256.FORE255 + Style.BRIGHTs\n\n"
                    "click_ansi_code\n"
                    "默认的值为\n"
                    "Colors256.BACK249 + Colors256.FORE232\n\n"
                    "这些参数在选项“查看类属性”中都描述过\n",
                    "它们可以通过直接赋值的方式来修改\n"
                    "我们在前面的代码上进行修改\n",
                    "示例代码如下\n"
"""
. . .（省略）
qc = Choice(
    options=example_options,
    methods=example_methods,
    unchecked_ansi_code='',
    checked_ansi_code=Back.CYANs + Style.BRIGHTs,
    click_ansi_code=Back.LIGHTREDs + Fore.BLACKs,
)
while True:
    idx = qc.run()
    if idx == len(example_options) - 1:
        break

""",
                    "运行结果为\n"
                ],
                [
                    "但是这样感觉效果还是不行\n",
                    "背景色离选项过近\n"
                    "同时选项之间切换的过度也略显生硬\n",
                    "这时候我们就可以通过以下两种办法来增强以下效果\n",
                    "1.给选项两边各添加一个空格\n",
                    "后面的空格只要给最长的选项添加就行了\n"
                    "其余的会自动补齐\n",
                    "2.使用set_indents方法\n",
                    "Choice.set_indent(self,\n"
                    "                  unchecked,\n"
                    "                  checked\n"
                    ")\n"
                    "设置缩进\n",
                    "参数 unchecked：未选中选项行的缩进\n"
                    "参数 checked：被选中选现行的缩进\n"
                    "在设置时需注意\n",
                    "checked的值必须大于等于unchecked，小于等于屏幕宽度\n",
                    "推荐设置\n"
                    "set_indent(2, 4)\n",
                    "同时还有一个Choice.get_indent(self)方法\n",
                    "该方法会返回一个命名元组 -- indents\n"
                    "该元组内容为(unchecked, checked)这两个参数的值\n",
                    "现在我们添加这两个效果\n"
                    "示例代码如下\n",
"""
example_options_prf = [
            ' 测试选项1 ',
            ' 测试选项2 ',.
            ' 测试选项3 ',
            ' 测试选项4 ',
            ' 返回 '
        ]
qc = Choice(
    options=example_options_prf,
    methods=example_methods,
    unchecked_ansi_code='',
    checked_ansi_code=Back.CYANs + Style.BRIGHTs,
    click_ansi_code=Back.LIGHTREDs + Fore.BLACKs,
)
qc.set_indents(2, 4)
# 添加缩进
while True:
    idx = qc.run()
    if idx == len(example_options_prf) - 1:
        break        
""",
                    "运行结果为\n"
                ],
                [
                    "对比前面的选项\n",
                    "经过这两步的修改观感相对好了一些\n"
                ]
            ]
            print()
            if description_printer(codes[0], interactive_lp, step=4):
                return
            example_options.append('退出')
            qc = Choice(
                options=example_options,
                methods=example_methods,
                unchecked_ansi_code='',
                checked_ansi_code=Back.CYANs + Style.BRIGHTs,
                click_ansi_code=Back.LIGHTREDs + Fore.BLACKs,
            )
            while True:
                idx = qc.run()
                if idx == len(example_options) - 1:
                    break
            example_options.pop()
            if description_printer(codes[1], interactive_lp, step=4):
                return
            qc = Choice(
                options=example_options_prf,
                methods=example_methods,
                unchecked_ansi_code='',
                checked_ansi_code=Back.CYANs + Style.BRIGHTs,
                click_ansi_code=Back.LIGHTREDs + Fore.BLACKs,
            )
            qc.set_indents(2, 4)
            # 添加缩进
            while True:
                idx = qc.run()
                if idx == len(example_options_prf) - 1:
                    break
            if description_printer(codes[2], interactive_lp, step=4):
                return

        def example_of_custom_key_setting():
            codes = [
                [
                    "除了更改样式之外\n",
                    "你还可以自定义键位\n"
                    "通过方法Choice.set_keys(self, setting_dict)\n"
                    "方法来修改键位\n",
                    "该方法的参数setting_dict是一个字典\n",
                    "该字典需要有以下三个键\n"
                    "'up'  向上切换\n"
                    "'down'  向下切换\n"
                    "'confirm'  确认\n",
                    "对应的键值可以是字符或者字符列表\n"
                    "如：\n",
                    "{'up': '8', 'down': '2'}\n"
                    "{'confirm': ['e', 'E', 'f']}\n",
                    "传递的字典不一定要包含全部的键位\n"
                    "甚至可以不包含\n",
                    "不包含的键位会被忽略\n"
                    "不会修改原来的键位\n",
                    "示例代码如下\n",
"""
. . .（省略）
qc = Choice(
    options=example_options_prf,
    methods=example_methods,
)
qc.set_keys({
    'confirm': 'f',
})
print('确认键位被修改成了f')
while True:
    idx = qc.run()
    if idx == len(example_options_prf) - 1:
        break  
""",
                    "运行结果为\n"
                ]
            ]
            print()
            if description_printer(codes[0], interactive_lp, step=4):
                return
            qc = Choice(
                options=example_options_prf,
                methods=example_methods,
            )
            qc.set_keys({
                'confirm': 'f',
            })
            print('确认键位被修改成了f')
            while True:
                idx = qc.run()
                if idx == len(example_options_prf) - 1:
                    break

        example_codes_of_dp = [
            ' 初始化Choice类',
            ' 快速创建选项 ',
            ' 自定义选项显示效果 ',
            ' 自定义选项键位 ',
            ' 返回上一级菜单 '
        ]
        example_methods_of_dp = [
            example_of_init,
            example_of_quickly_create_choice,
            example_of_custom_display_effect,
            example_of_custom_key_setting,
        ]
        im.append('example codes')
        callable_methods_choice = Choice(options=example_codes_of_dp, methods=example_methods_of_dp)
        callable_methods_choice.set_indents(2, 4)
        while True:
            print()
            normal_lp.print(im.current_index, step=2)
            idx = callable_methods_choice.run()
            if idx == len(example_codes_of_dp) - 1:
                im.pop()
                break

    def simple_description():
        details_description = [
            "Choice类是一个可以快速创建选项的工具类\n",
            "一个Choice实例只能管理一个选项列表和对应的方法列表\n"
            "目前Choice类只支持一个选项占一行\n",
            "后续更新会增加多行选项的支持\n"
            "了解详细用法请选其他选项\n",
        ]
        print()
        if description_printer(details_description, interactive_lp):
            return

    obj_options = [
        ' 查看类属性',
        ' 查看示例代码',
        ' 查看简介',
        ' 返回上一级菜单 '
    ]
    im.append('choice')
    obj_methods = [
        attribute,
        example_codes,
        simple_description
    ]
    choice_choice = Choice(options=obj_options, methods=obj_methods)
    choice_choice.set_indents(2, 4)
    while True:
        print()
        normal_lp.print(im.current_index, step=2)
        idx = choice_choice.run()
        if idx == len(obj_options) - 1:
            im.pop()
            break


options = [
    ' 如何使用Fore, Back, Style ',
    ' 如何使用Cursor',
    ' 如何使用Colors256',
    ' 如何使用Conio',
    ' 如何使用DynamicPrint',
    f' 如何使用Choice',
    ' 返回主菜单'
]

methods = [
    usage_of_fore_back_style,
    usage_of_cursor,
    usage_of_colors256,
    usage_of_conio,
    usage_of_dynamicprint,
    usage_of_choice
]


def usage_of_conkits():
    print()
    tips_lp.print(tips)
    if description_printer(simple_description_of_usage, simply_described_lp):
        return
    usage_choice = Choice(options=options, methods=methods)
    usage_choice.set_indents(2, 4)
    im.append('usage')
    while True:
        print()
        normal_lp.print(im.current_index, step=2)
        idx = usage_choice.run()
        if idx == len(options) - 1:
            im.pop()
            break

