from .predefinedcolors import *
from .anim import wait_anim0
from conkits.ansi import Cursor
from conkits.conio import Conio
from conkits.printtools import DynamicPrint, Choice
from .usage import usage_of_conkits


version = '0.2.1'
C256 = Colors256
normal_lp = DynamicPrint()  # 普通
simply_described_lp = DynamicPrint(print_delay=0.015, step=10)  # 打印简短描述
tips_lp = DynamicPrint(step=2, ansi_code=Style.ITALICs)  # 打印小提示
interactive_lp = DynamicPrint(print_delay=0.005, step=1)  # 交互式打印


escape_characters = ['Q', 'q']


def interrupted_reminder():
    print(Style.NORMALs + Fore.YELLOWs + '已打断' + Fore.RESETs + '\n')


# 什么是ansi代码
def what_is_ansi_code():
    print()
    description_of_ansi_code =[
        f'ansi control code(American National Standards Institute)\n'
        f'是美国国家标准协会制定的一组用于控制终端显示行为的代码\n' 
        f'通常以序列为 \\033[ 或者 \\x1b[ 开头，通常称该序列为 Control Code Interducer\n' 
        f'ansi控制码可以控制{Style.UNDERLINEs}终端的文本颜色，背景颜色，显示样式例如加粗高亮，斜体，反显等样式{Style.UNDERLINE_OFFs}还有{Style.UNDERLINEs}光标的移动和位置和一些其他的终端行为{Style.UNDERLINE_OFFs}\n' 
        f'下面简单介绍一下ansi控制码的常见用法来说明如何使用控制码\n',

        f'控制码都以 \\033[ 或者 \\x1b[ 开头，两者左右等价。其中\\033和\\x1b都表示键盘上的ESC按键对应的字符（下面我用以 \\033[ 举例）\n'
        f'控制颜色和样式的ansi代码格式通常为\n'
        f'\\033[ + 数值 + m\n'
        f'm 表示设置文本（前景）颜色，背景颜色和样式\n'
        f'例如\n',

        f'\\033[31m 能把文本设置为红色\n'
        f'\\033[0m 能重置所有设置\n'
        f'下面的代码可以将部分字符设置为红色\n',

        f'{Fore.GREENs}>>> {Fore.RESETs}\
{function_purple_fore}print{light_yellow_fore}({string_green_fore}"\
{orange_fore}\\033{string_green_fore}[31m能把文本设置为红色{orange_fore}\\033{glass_green_fore}[0m现在重置所有设置"{light_yellow_fore}){Style.RESET_ALLs}\n'
        f'运行结果为\n'
        f'{Style.NORMALs}\033[31m能把文本设置为红色\033[0m{Fore.RESETs + Style.NORMALs}现在重置所有设置\n',

        f'\\033[42m 能把背景设置为绿色\n'
        f'不过仅仅是设置字符显示的地方，而不是整个终端\n'
        f'示例代码如下\n',

        f'{Fore.GREENs}>>> {Fore.RESETs}\
{function_purple_fore}print{light_yellow_fore}({string_green_fore}"\
{orange_fore}\\033{string_green_fore}[42m可以把文字背景设置为绿色{orange_fore}\\033{glass_green_fore}[0m现在重置所有设置"{light_yellow_fore}){Style.RESET_ALLs}\n'
        f'运行结果为\n'
        f'{Style.NORMALs}\033[42m可以把文字背景设置为绿色\033[0m{Back.RESETs + Style.NORMALs}现在重置所有设置\n',

        f'\\033[3m 能字体设置为斜体\n'
        f'示例代码如下\n',

        f'{Fore.GREENs}>>> {Fore.RESETs}\
{function_purple_fore}print{light_yellow_fore}({string_green_fore}"\
{orange_fore}\\033{string_green_fore}[3m能把文字设置为斜体{orange_fore}\\033{glass_green_fore}[0m现在重置所有设置"{light_yellow_fore}){Style.RESET_ALLs}\n'
        f'运行结果为\n'
        f'\033[3m能把文字设置为斜体\033[0m{Style.ITALIC_OFFs}现在重置所有设置\n',

        f'可以一次性设置文字颜色背景和样式\n'
        f'例如 \\033[31;42;3m 能把设置红色字体，绿色背景和斜体样式\n'
        f'不分前后顺序和个数\n'
        f'设置时只需把控制码以;隔开，结尾时以m结尾\n'
        f'示例代码如下\n',

        f'{Fore.GREENs}>>> {Fore.RESETs}\
{function_purple_fore}print{light_yellow_fore}({string_green_fore}"\
{orange_fore}\\033{string_green_fore}[31;42;3m可以把文字设置为斜体{orange_fore}\\033{glass_green_fore}[0m现在重置所有设置"{light_yellow_fore}){Style.RESET_ALLs}\n'
        f'运行结果为\n'
        f'\033[31;42;3m可以把文字设置为红色字体，绿色背景和斜体样式\033[0m{Style.RESET_ALLs}现在重置所有设置\n',

        f'但是要注意，同一种类型设置中，如果存在多个设置\n'
        f'后面的设置会覆盖前面的设置\n'
        f'列如 \\033[32;31;36m\n'
        f'这里分别设置了绿色，红色，青色\n'
        f'但是最后生效的只有青色\n'
        f'示例代码如下\n',

        f'{Fore.GREENs}>>> {Fore.RESETs}\
{function_purple_fore}print{light_yellow_fore}({string_green_fore}"\
{orange_fore}\\033{string_green_fore}[32;31;36m最后生效的为青色{glass_green_fore}"{light_yellow_fore}){Style.RESET_ALLs}\n'
        f'运行结果为\n'
        f'\033[32;31;36m最后生效的为青色{Style.RESET_ALLs}\n',

        f'常用控制码如下\n'
        f'0 - 9 设置样式\n'
        f'30 - 37 设置前景色（文本颜色）\n'
        f'40 - 47 设置背景色\n'
        f'对于颜色代码，从30（40） - 37（47）依次为\n'
        f'黑，红，绿，黄，蓝，紫，青，白\n',

        f'如果想详细了解各个样式代码，还有光标代码的作用\n'
        f'请选择选项"了解库的用法"\n'
        f'如果你想了解更多ansi控制码及其相关内容\n'
        f'可以访问链接（需要挂梯子）\n'
        f'{link_fore}http://en.wikipedia.org/wiki/ANSI_escape_code{Style.RESET_ALLs}\n\n'
        ]
    tips = f"Tips:\n如果不小心选错该选项\n可以按q键来退出"
    tips_lp.print(tips + '\n')
    for text in description_of_ansi_code[0:1]:
        ch = simply_described_lp.print(text)
        if wait_anim0(ch in escape_characters) in [*escape_characters, None]:
            interrupted_reminder()
            return
    for text in description_of_ansi_code[1:-2]:
        ch = interactive_lp.print(text)
        if wait_anim0(ch in escape_characters) in [*escape_characters, None]:
            interrupted_reminder()
            return
    for text in description_of_ansi_code[-2:-1]:
        ch = simply_described_lp.print(text)
        if wait_anim0(ch in escape_characters) in [*escape_characters, None]:
            interrupted_reminder()
            return
    simply_described_lp.print(description_of_ansi_code[-1])


# 打印项目结构
def print_project_structure():
    print()
    line_color = C256.FORE64
    ver = f'{line_color}│{Fore.RESETs}'
    mid = f'{line_color}├──{Fore.RESETs}'
    end = f'{line_color}└──{Fore.RESETs}'
    dir_color = C256.FORE68 + Style.BRIGHTs
    file_color = C256.FORE250 + Style.ITALICs

    project_structure = f"""
    {dir_color}conkits{Style.RESET_ALLs}
      {mid} {dir_color}ansi256colors{Style.RESET_ALLs}
      {ver}     {mid} {file_color}__init__.py{Style.RESET_ALLs}
      {ver}     {mid} {file_color}ansi256colors.py{Style.RESET_ALLs}
      {ver}     {end} {file_color}ansi256colorscodes.py{Style.RESET_ALLs}
      {mid} {dir_color}help{Style.RESET_ALLs}
      {ver}     {mid} {file_color}__init__.py{Style.RESET_ALLs}
      {ver}     {mid} {file_color}anim.py{Style.RESET_ALLs}
      {ver}     {mid} {file_color}predefinedcolors.py{Style.RESET_ALLs}
      {ver}     {end} {file_color}usage.py{Style.RESET_ALLs}
      {mid} {dir_color}printtools{Style.RESET_ALLs}
      {ver}     {mid} {file_color}__init__.py{Style.RESET_ALLs}
      {ver}     {mid} {file_color}basicprinttool.py{Style.RESET_ALLs}
      {ver}     {mid} {file_color}ansistring.py{Style.RESET_ALLs}
      {ver}     {end} {file_color}dynamicprint.py{Style.RESET_ALLs}
      {mid} {file_color}__init__.py{Style.RESET_ALLs}
      {mid} {file_color}conio.py{Style.RESET_ALLs}
      {end} {file_color}ansi.py {Style.RESET_ALLs}
    """
    normal_lp.print(f'{Style.BRIGHTs}项目结构{Style.RESET_ALLs}')
    normal_lp.print(project_structure, step=34, print_delay=0.01)


def conkits_help():
    # 对库的简单描述
    description_of_conkits = f"\
{C256.FORE252}con{C256.FORE34}k{Style.ITALICs}i{Style.ITALIC_OFFs + C256.FORE34}ts{Style.RESET_ALLs}\n\
{C256.FORE249}({Style.ITALICs + C256.FORE252}console {C256.FORE34}kits  \
{C256.FORE60}version {C256.FORE214}{version}{C256.FORE249}){Style.RESET_ALLs}\n\n\
conkits是一个封装了常用ansi控制代码的库。\n\
其中包括前景色，背景色，样式，光标和256色的ansi控制代码的封装。\n\
除此之外，还附带了两个有趣的类，能够实现逐字打印字符串\
和创建选项。\n如果你对这个项目感兴趣，可以访问[{link_fore}https://gitbub.com/EKSIlvyAh/conkits/{Style.RESET_ALLs}]\
来查看项目的源代码，或者阅读README文件来了解库的基本用法。\n"

    t_char_fore = glass_green_fore
    t_sep_fore = Style.ITALICs + C256.FORE230 + Style.DIMs
    t_text_fore = C256.RESET_FORE + Style.NORMALs + Style.BRIGHTs
    # 小提示
    tips = f"Tips:\n\
按任意键可跳过打印动画\n\
在选项中，按键设置如下\n\
    {t_char_fore}w{t_sep_fore} ->  {t_text_fore}向上切换选项{Style.RESET_ALLs}\n\
    {t_char_fore}s{t_sep_fore} -> {t_text_fore}向下切换选项{Style.RESET_ALLs}\n\
    {t_char_fore}e{t_sep_fore}/{Style.NORMALs + t_char_fore}回车{t_sep_fore} ->  {t_text_fore}确认{Style.RESET_ALLs}\n"
    print()
    simply_described_lp.print(description_of_conkits, step=4)
    tips_lp.print(tips)
    Conio.interruptible_sleep(0.2)

    main_menu_options = [
        f' 什么是{Fore.BLUEs}ansi{Style.RESET_ALLs}控制码？',
        ' 打印项目结构',
        ' 了解库的用法',
        f' 打印256色阶',
        f' 退出{C256.FORE220}conkits_help{Style.RESET_ALLs} '
    ]
    main_menu_methods = [
        what_is_ansi_code,
        print_project_structure,
        usage_of_conkits,
        C256.show_color_scale
    ]
    main_menu_choice = Choice(options=main_menu_options, methods=main_menu_methods)
    main_menu_choice.set_indents(2, 4)
    triangle = f'{Style.BRIGHTs + Fore.CYANs}▶{Style.NORMALs}'
    current_index = f'{triangle} {Fore.GREENs + Style.BRIGHTs}help{Style.RESET_ALLs} '
    while True:
        print()
        normal_lp.print(current_index + Style.NORMALs, step=2)
        idx = main_menu_choice.run()
        print()
        if idx == len(main_menu_options) - 1:
            break

