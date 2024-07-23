# CWMathConsole

[English EN](./README_en.md) | [简体中文 CN](./README_cn.md)

A simple terminal for performing mathematical calculations.

Currently under development...

## Installation

There are two ways to install CWMathConsole:

### Method 1: Download the pre-built executable from Github

Details are not extensively covered here. You can directly download the ready-to-use executable file.

This will be uploaded once the author has completed a portion of the functionality.

For the latest version of the files, consider Method 2.

### Method 2: Download the source code from Github and compile it

This method involves directly cloning the repository and then compiling it for either running or packaging.

Using this method requires having the necessary runtime environment and compiler.

First, clone the repository:

```shell
git clone https://github.com/10chen01/CWMathConsole.git
cd CWMathConsole
```

Then install the environment and compile:

```shell
pip install -r requirements.txt
```

You can use Tsinghua's mirror to increase download speed:

```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

Alternatively, manually install the following packages:
- `sympy`
- `latex2sympy2`

Compile the program using Python.

**Note ⚠️: Python version must be >=3.10**

```shell
python ./cwconsole.py
```

#### Packaging the compiled Python program

First, you need to install `pyinstaller`.

```shell
# python package
pip install pyinstaller
# anaconda
conda install pyinstaller
```

Then use `pyinstaller` to package the software.

```shell
pyinstaller.exe -F cwconsole.py
```

This will yield the executable version of CWMathConsole.

After downloading, you can add CWMathConsole to your PATH for easy access.

## Usage Guide

CWMathConsole is a simple math terminal that offers several commands for calculations.

### Basic Syntax

CWMathConsole commands are case-sensitive and must always be in lowercase by default.

CWMathConsole commands are separated by spaces into a linked list, where the first item is the **main command**, and the following items are known as **arguments**.

The detailed usage of commands is generally specified upon invocation.

#### Expression Format

CWMathConsole uses `latex2sympy2` to read and output mathematical expressions, so mathematical expressions within CWMathConsole are typically written in LaTeX format as the language of expression.

When using symbols, it is recommended to use single Latin characters or the Latin transliteration of Greek characters instead; **avoid using combinations of multiple Latin characters such as `destruction`, as this symbol will be interpreted by latex2sympy2 as the product of several Latin characters!**

### Basic Commands

#### `help` Command

Get help information.

#### `exit` / `quit` Command

Exit CWMathConsole.

#### `define` / `create` Command

Define a variable or function

Parameters:
- `var` / `variable`: Define a variable
- `func` / `function`: Define a function

#### `redef` / `update` Command

Reassign a variable or function.

#### `undef` / `remove` Command

Remove a variable or function.

#### `calc` / `eval` Command

Evaluate the value of an expression, which will output both the simplified form of the expression and its value.

#### `graph` Command

Plot the graph of a function (currently based on turtle).

It can plot the rect/polar functions's graph on turtle panel.

#### `solve` Command

Solve equations, capable of solving single equations/systems of equations and inequalities/systems of inequalities.

Parameters:

- `once`: Indicates solving a single equation
- `multi`: Indicates solving a system of equations

#### `pyrun` Command

The `pyrun` command supports running a segment of Python code, allowing you to solve problems with Python code.

`pyrun` uses `exec`/`eval` implementation, but on certain platforms, there is no corresponding `exec` and `eval` implementation, thus the `pyrun` command is marked as an `Extend Version` exclusive command.

`pyrun file` can also execute code from a file, also using `exec` for execution.

Directly using `pyrun` will put CWMathConsole into Pyshell mode, and the command prompt will change from `cw:>` to `pyshell:>>`.

In Pyshell mode, you can exit by using `[CWConsole]`.
