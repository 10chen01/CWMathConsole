# CWMathConsole

一个简易的终端, 可以计算数学

正在开发中...

## 安装

可以使用两种方式安装CWMathConsole

### 方法1: 从Github上下载现成的可执行文件

具体不多赘述。可以直接下载现成的可执行文件。

这是等到作者已经基本完成一部分功能后会上传Assent

如果需要最新版的文件, 可以考虑方法2

### 方法2: 从Github上下载源码然后编译

这个方法就是直接将这个仓库克隆下来然后编译运行或打包

使用这个方法的前提是你需要拥有运行的环境和编译器

首先克隆仓库:

```shell
git clone https://github.com/10chen01/CWMathConsole.git
cd CWMathConsole
```

然后安装环境并编译

```shell
pip install -r requirements.txt
```

可以使用清华源提升下载速度

```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

或者手动安装以下包:
- `sympy`
- `latex2sympy2`

使用Python编译程序即可

```shell
python ./cwconsole.py
```

#### 打包编译好的Python程序

首先需要安装`pyinstaller`

```shell
pip install pyinstaller
```

然后使用`pyinstaller`打包软件

```shell
python -m pyinstaller -f cwconsole.py
```

即可获得CWMathConsole的可执行程序版本

下载完成后即可将CWMathConsole添加到PATH中方便使用

## 使用教程

CWMathConsole是简单的数学终端, 提供了一些命令以计算

### 基本语法

CWMathConsole的命令区分大小写, 并且默认必须是全部是小写

CWMathConsole的命令使用空格分割成一串链表, 其中第一项为**主命令**, 后面几项叫做**标记**

CWMathConsole的命令详细一般都是调用后指定。

#### 表达式格式

CWMathConsole使用`latex2sympy2`来读取并输出数学表达式, 所以在CWMathConsole中的数学表达式一般都是用LaTeX格式作为表达语言

如有使用符号的需要, 建议使用单个的拉丁字符或希腊字符的拉丁写法代替, 不建议使用几个拉丁字符的组合例如`destruction`, 后续使用这个符号会被latex2sympy2识别成几个拉丁字符所代表的乘积!

### 基本命令

#### `help` 命令

获取帮助信息

#### `exit` / `quit` 命令

退出CWMathConsole

#### `define` / `create` 命令

定义一个变量或函数

#### `redef` / `update` 命令

重新赋值一个变量或函数

#### `undef` / `remove` 命令

删除一个变量或函数

#### `calc` / `eval` 命令

求一个函数的值

#### `graph` 命令

绘制函数的图像(目前基于turtle)

#### `solve` 命令

解方程

#### `pyrun` 命令

`pyrun`命令支持运行一段python代码, 编写python代码解决问题

`pyrun`使用`exec`/`eval`实现, 而在某些平台上并没有相应的`exec`和`eval`实现, 因此`pyrun`命令被标记成`Extend Version`独有命令

`pyrun file`还可以执行一段文件中的代码,同样使用`exec`运行

直接使用`pyrun`会让CWMathConsole进入Pyshell模式, 命令提示符也将由`cw:>`变为`pyshell:>>`

在Pyshell模式下可以使用`[CWConsole]`退出Pyshell模式
