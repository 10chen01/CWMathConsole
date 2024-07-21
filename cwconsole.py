from sympy import *
import latex2sympy2
import turtle
from typing import *
from dataclasses import dataclass

INIT_GRAPH = False
EXTEND_VERSION = True


@dataclass
class CommandInformation:
    command: list[str]
    argument: dict[tuple[str, ...], str]
    extend_version_command: bool = False


command_information = {
    "help": CommandInformation(
        command=["help"],
        argument={}
    ),
    "exit_quit": CommandInformation(
        command=["exit", "quit"],
        argument={}
    ),
    "define_create": CommandInformation(
        command=["define", "create"],
        argument={
            ("var", "variable"): "创建一个变量",
            ("func", "function"): "创建一个函数"
        }
    ),
    "pyrun": CommandInformation(
        command=["pyrun"],
        argument={
            ("[file]",): "运行python文件"
        },
        extend_version_command=True
    )
}
var_dictionary: dict = {}
function_information: dict = {}


def not_extend_version_command_error(*_, **__):
    """
    当用户使用了Extend Version的功能但版本并非Extend Version时调用此函数
    Extend Version为Github中上传的版本
    Extend Version和Lite Version之间的区别详情请见README.md
    该函数仅作提示作用,可以有参数但不会用任何作用, 不返回返回值
    :param *_, *__
    :return: None
    """
    print("此CW Console版本不支持该Extend功能")
    print("建议使用Github中的Extend Version")
    print("Github Repository: https://github.com/10chen01/CWMathConsole")


def extension_command(command: Callable) -> Callable:
    """
    使用这个装饰器的函数将会被标记为Extend Version特有函数
    若EXTEND_VERSION标记值为False, 将会使用not_extend_version_command_error函数代替原本的函数
    :param command: 传入的CW Console的功能
    :return: 一个函数, 值为command或not_extend_version_command_error函数
    """
    if EXTEND_VERSION:
        return command
    else:
        return not_extend_version_command_error


def not_opened_command_used_error(*_, **__) -> None:
    """
    如果用户调用了尚未开放的功能, 就会触发该指令
    :return:
    """
    print("这个命令尚未开放使用")
    print("更多信息详情请见README.md和github")


def closing_command(_: Callable) -> Callable:
    """
    这是一个装饰器, 被装饰过的函数将被标记为未开放并替换为not_opened_command_used_error函数
    :param _:
    :return:
    """
    return not_opened_command_used_error


def help_document(_command_information: CommandInformation):
    def _wrapper_decorator(command_help: Callable) -> Callable:
        def _wrapper_document():
            print("Command:", "|".join(_command_information.command))
            if _command_information.extend_version_command:
                print("Extend Version Only.")
            if _command_information.argument != {}:
                print("Argument:")
                for _arg_h, _arg_v in _command_information.argument.items():
                    print(f"\t{'|'.join(_arg_h)}:  {_arg_v}")
            else:
                print("No Argument.")
            print("\n")
            command_help()

        _wrapper_document.__name__ = "Command_" +"_".join(_command_information.command) + "_doc"
        return _wrapper_document

    return _wrapper_decorator


@help_document(command_information["help"])
def help_doc() -> None:
    ...


@help_document(command_information["exit_quit"])
def exit_quit_doc() -> None:
    print("退出CWConsole的命令")


@help_document(command_information["define_create"])
def define_create_doc() -> None:
    print("此命令将会创建一个数学对象")
    print("若不在命令中指定var/func类型将会在单独打开命令后输入类型")


@help_document(command_information["pyrun"])
def pyrun_doc() -> None:
    print("可以使用pyrun命令运行python代码")
    print("如果不指定file参数将会进入pyshell模式, 可以使用[CWConsole]退出")
    print("如果指定file参数将会运行file参数指定的文件")


def draw_grid() -> None:
    """
    绘制坐标系网格
    :return:
    """
    turtle.color("#cccccc")
    for x in range(-400, 400, 20):
        turtle.penup()
        turtle.goto(x, -400)
        turtle.pendown()
        turtle.goto(x, 400)
        turtle.penup()
        turtle.goto(-400, x)
        turtle.pendown()
        turtle.goto(400, x)
        turtle.penup()
    turtle.width(2)
    turtle.color("#444444")
    turtle.goto(-400, 0)
    turtle.pendown()
    turtle.goto(400, 0)
    turtle.penup()
    turtle.goto(0, -400)
    turtle.pendown()
    turtle.goto(0, 400)
    turtle.penup()


if __name__ == '__main__':
    print("CW Console v1.0.0")
    print("输入 help 获取帮助")
    print("输入 exit 或 quit 退出终端")
    looper = True
    while looper:
        command_str: str = input("cw:>").strip()
        if command_str == "":
            continue
        # 获取函数的各个参数的详情
        command_lst: list = command_str.split(" ")
        main_command = command_lst[0]
        match main_command:
            case "help":
                # 帮助命令

                # @closing_command
                def help_main() -> None:
                    print("常用的命令:")
                    print("\tpyrun")
                    print("\tdefine/create")
                    print("\texit/quit")
                    print("\thelp")
                    print("")
                    print("可通过help [command]的形式获取具体命令的操作")


                def help_command(_command: str) -> None:
                    match _command:
                        case "help":
                            help_doc()
                        case "exit" | "quit":
                            exit_quit_doc()
                        case "define" | "create":
                            define_create_doc()
                        case "pyrun":
                            pyrun_doc()
                        case _:
                            print("未知的命令, 无法提供帮助@^@")

                if len(command_lst) == 1:
                    help_main()
                else:
                    help_command(command_lst[1])
            case "exit" | "quit":
                # 退出的指令
                print("good bye!")
                # 退出返回值0
                quit(0)
            case "define" | "create":
                # 创建变量或函数的指令

                def _create_variable() -> None:
                    # while (_variable_name := input("请输入变量的符号:>>").strip()) != "":
                    #     print("变量符号不能为空, 请重新输入")
                    _variable_name = input("请输入变量的符号:>>").strip()
                    print("输入的变量的符号为", _variable_name)
                    if _variable_name == "":
                        print("输入变量的符号不能为空")
                    _variable_symbol = Symbol(_variable_name)
                    # while (_variable_str := input("请输入变量的值:>>").strip()) != "":
                    #     print("变量的值不能为空, 请重新输入")
                    _variable_str = input("请输入变量的值:>>").strip()
                    print("输入变量的值为", _variable_str)
                    try:
                        _variable_value = latex2sympy2.latex2sympy(_variable_str)
                    except Exception as e:
                        print("值错误: ", e)
                        return
                    var_dictionary[_variable_symbol] = _variable_value


                def _create_function() -> None:
                    # while (_variable_name := input("请输入函数的符号:>>").strip()) != "":
                    #     print("函数符号不能为空, 请重新输入")
                    _variable_name: str
                    _variable_name = input("请输入函数的符号:>>").strip()
                    if _variable_name == "":
                        print("函数符号不能为空")
                        return
                    _variable_symbol = Symbol(_variable_name)
                    # while (_variable_str := input("请输入函数的解析式:>>").strip()) != "":
                    #     print("函数的解析式不能为空, 请重新输入")
                    _variable_str: str
                    _variable_str = input("请输入函数的解析式:>>").strip()
                    if _variable_str == "":
                        print("函数解析式不能为空")
                        return
                    try:
                        _variable_value = latex2sympy2.latex2sympy(_variable_str)
                    except Exception as e:
                        print("表达式错误: ", e)
                        return
                    var_dictionary[_variable_symbol] = _variable_value


                _create_type: Literal["variable", "function"]
                if len(command_lst) == 1:
                    _create_type_prompt: str = input("请输入创建对象的类型[var | func]:")
                else:
                    _create_type_prompt = command_lst[1]
                match _create_type_prompt:
                    case "var" | "variable":
                        _create_type = "variable"
                    case "func" | "function":
                        _create_type = "function"
                    case _:
                        print("未知类型")
                        continue
                match _create_type:
                    case "variable":
                        _create_variable()
                    case "function":
                        _create_function()
            case "solve":
                @closing_command
                def _solve_equation() -> None:
                    ...


                _solve_equation()
            case "redef" | "update":
                @closing_command
                def _redefine_variable() -> None:
                    ...


                _redefine_variable()
            case "undef" | "remove":
                @closing_command
                def _remove_variable() -> None:
                    ...


                _remove_variable()
            case "calc" | "eval":
                @closing_command
                def _calculate_expression() -> None:
                    expr = input("请输入表达式:>>")


                _calculate_expression()
            case "graph":
                @closing_command
                def _graph_function(fun_name: str) -> None:
                    global INIT_GRAPH
                    turtle.speed(0)
                    if not INIT_GRAPH:
                        is_draw_grid = input("是否绘制坐标网格?([y]/n): ")
                        if is_draw_grid.lower().strip() != "n":
                            draw_grid()
                        INIT_GRAPH = True


                @closing_command
                def _graph_pol_function(fun_name: str) -> None:
                    global INIT_GRAPH
                    turtle.speed(0)
                    if not INIT_GRAPH:
                        is_draw_grid = input("是否绘制坐标网格?([y]/n): ")
                        if is_draw_grid.lower().strip() != "n":
                            draw_grid()


                ...
            case "pyrun":
                @extension_command
                def run_pycode() -> None:
                    if  len(command_lst) > 1 and command_lst[1] == "file":
                        print("执行python代码")
                        if len(command_lst) == 2:
                            file_name = input("请输入python文件路径")
                            file_v = open(file_name, "r")
                        else:
                            # 去除前半部分的指令
                            _minus_string = "pyrun file"
                            file_name = command_str[len(_minus_string):]
                            file_v = open(file_name, "r")
                        try:
                            exec(file_v.read())
                        except Exception as e:
                            print("执行出错")
                            print("错误类型: ", type(e))
                            print("错误讯息", e)
                        return
                    print("已进入Python Shell模式")
                    print("输入[CWConsole]可退出此模式")
                    while True:
                        command = input("pyshell:>>").strip()
                        if command == "[CWConsole]":
                            break
                        try:
                            # 默认在python shell中的变量与是这个代码的全局变量域
                            # 目前暂不支持长篇python代码的编写和运行
                            exec(command)
                        except Exception as e:
                            print("执行错误: ", e)
                    print("已退出python模式")


                run_pycode()
            case _:
                print(f"未知命令: {main_command}")
