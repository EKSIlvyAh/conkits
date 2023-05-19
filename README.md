# Conkits (Console Kits)

## 👋作用👋

该库旨在封装常见 ANSI 控制码，使其的使用更加清晰和方便(大概)。

ANSI 控制码包含了标准的前景色和背景色，256色，字体样式的设置，光标的移动和控制和终端擦除显示的功能。

除此之外，还包含两个有趣的类(Dynamic 和 Choice)，可以实现在终端逐字打印字符(就像 gal 游戏里面逐字文本显示一样)和更加友好的选项选择。

## ✨编写 conkits 的动机✨

在写这个库的时候，我还是一个刚入门两个月不到的 python 新手。

因为喜欢研究终端文本的显示效果，再加上我当时并不知道已经有很多类似封装 ANSI 代码的第三方库(而且还有像 rich 这种非常 nb 的库)，也不知道在 pypi 上搜索类似的库，导致我经常在代码中写了大量的 ANSI 控制代码😓。

逐渐的，我产生了一种想法，那就是写一个包含常用 ANSI 代码的 python 库，然后上传到 pypi，让不知道 ANSI 代码的人也可以轻松的设置终端文本的显示样式。(当时我竟天真的认为类似的库几乎没有😃)

然后有某天我接触到`colorama`这个库，才知道已经有人封装了 ANSI 代码😢。但是当时的我不太认可 colorama 封装的方式，认为写`Fore.GREEN`比写`\033[32m`要麻烦很多，何必在费力的去多敲这么多字符呢?

不过这也暂时打消了我写一个库的想法，但是经过我一段时间的使用，发现 colorama 似乎没有封装控光标移动的 ANSI 代码🤔？

这又突然激起了我写一个库的想法，于是，抱着扩展 colorama 库的想法并参考了 colorama 的部分代码，我决定写一个自己的第三方库，于是就有了 conkits。

然而当我写到一半才发现，已经有太多封装 ANSI 代码的库了，比如 blessing，colored，库名中包含 ansi, term, color 等等的各种库。而且大多代码写得都很好😢😢😢。

但是已经付出了这么多精力，总得有个结果吧，因为简单的封装大多数的库都有了，所以我决定再加一些特别的功能。

就这样经过中途不断的增改和调试，一个多月后，我终于上传了`conkits 0.2.1`，一个算是稳定能用的版本，之后就在也没更新过了。

就这样过了好几个月，回头再看这个库，发现很多地方的想法认知都有不少错误和不足，略感羞愧，于是我就从 pypi 中删除了 conkits。

然后最近，之前被我介绍过 conkits 的某网友跟我说，他的某个参赛代码中用到了我的库，但是我已经把库删除了😧，所以我在稍微改了一些代码后，又上传了 conkits 然后就是现在的版本 0.2.2。

## 🎁用法🎁

### 查看 conkits_help

`conkits_help`是一个在终端交互式介绍用法的函数。灵感来源于 python 的`help`函数。

当然这可能会不太方便，但是当时的我还不会写 Markdown，所以想了这么个歪招😭。

但是介绍真的很详细，写 conkits_help 花了我好几个星期，把我都快写吐了。

你可以在命令行通过以下命令运行 conkits_help:

```bash
python -m conkits
```

或者在 python 中通过以下代码运行 conkits_help:

```python
from conkits import conkits_help

conkits_help()
```

运行后大概会看到如下界面:

[conkits_help 运行截图](./conkits_help.jpg)

### 使用 Fore, Back, Style 设置文本颜色和样式

由于我当初设计上的问题，在定义的关于前/背景色和样式 ANSI 代码中，我保留了对应的 ANSI 整数值和 ANSI 代码字符串，因此，如果要真正的设置上样式，需要在对应属性的后面加上小写的`s`。

比如下面的代码:

```python
from conkits import Fore

# GREEN 代表对应的 ANSI 码，为整数值，GREENs 则是可以被终端识别的 ANSI 控制码字符串
print(Fore.GREEN, repr(Fore.GREENs))
print(Fore.YELLOWs + 'Hello' + Fore.GREENs + 'World' + Fore.RESETs)
```

运行后的输出为:

[设置文本样式示例 1](./ansi_attr.jpg)

除此之外，还有 Back, Style 两个类分别用于设置背景色和文本样式，用法也基本同上，具体包含的属性可以查看源代码，文件为***conkits/ansi.py***。

很简单，不用怕看不懂😀。

### 使用 Cursor 类控制光标移动

控制光标移动需要使用`Cursor`类，在该类中有一些方法带后缀`_s`，这表明该方法会返回一个可以输出到终端的 ANSI 控制码字符串，而不带`_s`后缀的则直接输出到终端。

比如下面的例子:

```python
from conkits import Cursor

print('你好', end='')
Cursor.move_left(2)
print('吗')
# 查看实际实际输出的 ANSI 控制码
print(repr(Cursor.move_left_s(2)))
```

[Cursor 示例](./Cursor_example.jpg)

上述代码中，我们先输出**你好**二字，并且**不换行**，然后让光标向左移动两个单元格，之后再输出的**吗**将会覆盖**好**。

实际上，上述代码中的`Cursor.move_left(2)`相当于`print(Cursor.move_left(2), flush=True, end='')`。

其余方法可以查看源代码，文件为***conkits/ansi.py**。

### 下面的内容可以在我的 Github 主页上查看

### 使用 Conio 类

#### 清除屏幕

#### 清除行

#### 进行非缓冲输入

#### 进行非阻塞性输入

#### 进行可打断的 sleep

### 使用 Colors256 设置前/背景色

### 使用 DynamicPrint 动态输出字符

### 使用 Choice 创建选项

