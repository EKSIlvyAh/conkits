from conkits.ansi256colors import Colors256
from conkits.ansi import Fore, Back, Style


link_fore = Colors256.FORE33 + Style.UNDERLINEs  # fore链接样式的ansi代码

glass_green_fore = Colors256.FORE64  # fore草绿色
glass_green_back = Colors256.BACK64  # back草绿色

string_green_fore = Fore.GREENs  # fore字符串用的绿色
string_green_back = Fore.GREENs  # back字符串用的绿色

orange_fore = Colors256.FORE208  # fore橘黄色
orange_back = Colors256.BACK208  # fore橘黄色

light_yellow_fore = Colors256.FORE221  # fore亮黄色
light_yellow_back = Colors256.BACK221  # back亮黄色

function_purple_fore = Colors256.FORE97  # fore显示函数用的紫色
function_purple_back = Colors256.BACK97  # back显示函数用的紫色
