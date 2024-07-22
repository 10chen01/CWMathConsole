from sympy import *
from re import *
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

# region
command_information = {
    "help": CommandInformation(
        command=["help"],
        argument={}
    ),
    "exit/quit": CommandInformation(
        command=["exit", "quit"],
        argument={}
    ),
    "define/create": CommandInformation(
        command=["define", "create"],
        argument={
            ("var", "variable"): "创建一个变量",
            ("func", "function"): "创建一个函数"
        }
    ),
    "redef/update": CommandInformation(
        command=["redef", "update"],
        argument={}
    ),
    "calc/eval": CommandInformation(
        command=["calc", "eval"],
        argument={}
    ),
    "undef/update": CommandInformation(
        command=["undef", "update"],
        argument={}
    ),
    "solve": CommandInformation(
        command=["solve"],
        argument={
            ("once",): "以单一方程形式解方程",
            ("multi",): "以方程组形式解方程"
        }
    ),
    "pyrun": CommandInformation(
        command=["pyrun"],
        argument={
            ("[file]",): "运行python文件",
            ("$file", ): "若带file参数则运行文件$file"
        },
        extend_version_command=True
    ),
    "graph": CommandInformation(
        command=["graph"],
        argument={
            ("rec", ): "以平面直角坐标系的为基础绘制函数图像",
            ("pol", ): "以极坐标系为基础绘制函数图像",
            ("$func", ): "绘制$func的图像"
        }
    )
}
# endregion
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


def closing_command(_command: Callable) -> Callable:
    """
    这是一个装饰器, 被装饰过的函数将被标记为未开放并替换为not_opened_command_used_error函数
    :param _command:
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
            # print("\n")
            print()
            command_help()

        _wrapper_document.__name__ = "Command_" + "_".join(_command_information.command) + "_doc"
        return _wrapper_document

    return _wrapper_decorator


@help_document(command_information["help"])
def help_doc() -> None:
    print("获取帮助信息")


@help_document(command_information["exit/quit"])
def exit_quit_doc() -> None:
    print("退出CWConsole的命令")


@help_document(command_information["define/create"])
def define_create_doc() -> None:
    print("此命令将会创建一个数学对象")
    print("若不在命令中指定var/func类型将会在单独打开命令后输入类型")


@help_document(command_information["redef/update"])
def redef_update_doc() -> None:
    print("用于修改变量/函数的表达式/值")


@help_document(command_information["calc/eval"])
def calc_eval_doc() -> None:
    print("用于计算变量/表达式的值")


@help_document(command_information["pyrun"])
def pyrun_doc() -> None:
    print("可以使用pyrun命令运行python代码")
    print("如果不指定file参数将会进入pyshell模式, 可以使用[CWConsole]退出")
    print("如果指定file参数将会运行file参数指定的文件")


@help_document(command_information["solve"])
def solve_doc() -> None:
    print("此命令用于解方程/方程组/不等式/不等式组")
    print("使用once命令可解单一方程")


@help_document(command_information["graph"])
def graph_doc() -> None:
    print("此命令用户绘制函数图像")
    print("可以指定颜色/粗细/基准单位")
    print("可以选择绘制网格")


def solve_equation(latex_text, formatter: Literal['sympy', 'latex'] = 'sympy'):
    try:
        regex = r"\\begin{cases}([\s\S]*)\\end{cases}"
        matches = findall(regex, latex_text, MULTILINE)
        equations = []
        if matches:
            matches = split(r"\\\\(?:\[?.*?])?", matches[0])
            for _match in matches:
                ins = latex2sympy2.latex2sympy(_match)
                if type(ins) == list:
                    equations.extend(ins)
                else:
                    equations.append(ins)
            solved = solve(equations)
        else:
            return False
        if formatter == 'latex':
            return latex(solved)
        else:
            return solved
    except Exception as e:
        print("表达式错误>_< :", e)


class FunctionGrapher:
    """
    坐标系画图类
    """

    def __init__(self, pol_graph: bool = False):
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pol_graph = pol_graph
        iden_str = input("请输入一个单位长度所对应的像素个数(默认10px):>>")
        try:
            self.iden = latex2sympy2.latex2sympy(iden_str).evalf(subs=var_dictionary)
            if self.iden <= 0:
                self.iden = 10
                print("错误: 像素个数不能为负数或零")
                print("已设置为默认值10")
        except Exception as e:
            self.iden = 10
            print("错误: ", e)
            print("已设定为默认值10")
        pnt_str = input("请输入画图的精度(一个正整数, 默认为2):>>")
        try:
            self.pnt = int(pnt_str)
            print("已将画图的精度设置为", self.pnt)
        except Exception as e:
            self.pnt = 2
            print("错误: ", e)
            print("已将画图的精度设置为默认值2")
        have_to_draw_grid = input("是否绘制网格[(y)/n]:>>")
        if have_to_draw_grid != "n":
            grid_pts = input("请输入网格的线与线之间的距离(单位长度的多少, 默认为1):>>")
            try:
                grid_pt = int(grid_pts)
            except Exception as e:
                grid_pt = 1
                print("错误: ", e)
                print("已将网格的线与线之间的距离设置为默认值1")
            self.draw_grid(grid_pt)

    @staticmethod
    def translate_polar(r: float, theta: float) -> tuple[float, float]:
        """
        将极坐标转换为直角坐标
        :param r: 极坐标x
        :param theta: 极坐标y
        :return: 直角坐标
        """
        return nfloat(r * cos(theta)), nfloat(r * sin(theta))

    def draw_function(self, func, color, width, l_limit: float, r_limit: float) -> None:
        self.pen.penup()
        if not self.pol_graph:
            try:
                try:
                    self.pen.width(width)
                except Exception as e:
                    print("出现错误", e)
                    self.pen.width(1)
                    print("已自动将笔粗细调味默认值:1")
                try:
                    self.pen.pencolor(color)
                except Exception as e:
                    print("出现错误: ", e)
                    self.pen.pencolor("#000000")
                    print("已自动将笔颜色调为默认值:#000000")
                pts = 10 ** self.pnt
                iden = self.iden
                self.pen.penup()
                for x in [u / pts for u in range(
                        round(l_limit * pts),
                        round(r_limit * pts))]:
                    try:
                        y = nfloat(func.evalf(subs=var_dictionary | {Symbol("x"): x}))
                        if y > 400 * iden or y < -400 * iden or x > 400 * iden or x < -400 * iden:
                            print(f"警告: ({x=}, {y=})超过画板, 无法画图")
                            self.pen.penup()
                        else:
                            turtle.goto((x * iden, y * iden))
                            print(x, y)
                            self.pen.pendown()
                    except Exception as e:
                        print(f"警告: 在{x=}时, 无法求出函数值({e})")
                        self.pen.penup()
            except Exception as e:
                print("画图时出现错误: ", e)
        else:
            try:
                self.pen.width(width)
                self.pen.pencolor(color)
                pts = 10 ** self.pnt
                iden = self.iden
                self.pen.penup()
                for theta in [u / pts for u in range(
                        round(l_limit * pts),
                        round(r_limit * pts))]:
                    try:
                        r = nfloat(func.evalf(subs=var_dictionary | {Symbol("theta"): theta}))
                        if FunctionGrapher.translate_polar(r, theta)[0] > 400 * iden or \
                                FunctionGrapher.translate_polar(r, theta)[0] < -400 * iden or \
                                FunctionGrapher.translate_polar(r, theta)[1] > 400 * iden or \
                                FunctionGrapher.translate_polar(r, theta)[1] < -400 * iden:
                            print(f"警告: ({theta=}, {r=})超过函数界限, 无法画图")
                            self.pen.penup()
                        else:
                            turtle.goto(tuple([t * iden for t in FunctionGrapher.translate_polar(r, theta)]))
                            print(FunctionGrapher.translate_polar(r, theta))
                            self.pen.pendown()
                    except Exception as e:
                        print(f"警告: 在{theta=}时, 无法求出函数值({e})")
                        self.pen.penup()
            except Exception as e:
                print("画图时出现错误: ", e)

    def draw_grid(self, u_iden: int) -> None:
        """
        绘制坐标系网格
        :return:
        """
        self.pen.color("#cccccc")
        for x in range(-400, 400, round(u_iden * self.iden)):
            self.pen.penup()
            self.pen.goto(x, -400)
            self.pen.pendown()
            self.pen.goto(x, 400)
            self.pen.penup()
            self.pen.goto(-400, x)
            self.pen.pendown()
            self.pen.goto(400, x)
            self.pen.penup()
        self.pen.width(2)
        self.pen.color("#444444")
        self.pen.goto(-400, 0)
        self.pen.pendown()
        self.pen.goto(400, 0)
        self.pen.penup()
        self.pen.goto(0, -400)
        self.pen.pendown()
        self.pen.goto(0, 400)
        self.pen.penup()
        self.pen.color("#000000")
        self.pen.width(1)


grapher: FunctionGrapher
pol_grapher: FunctionGrapher

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
                # region
                # 帮助命令

                # @closing_command
                def help_main() -> None:
                    print("常用的命令:")
                    # print("\t pyrun")
                    # print("\t define/create")
                    # print("\t exit/quit")
                    # print("\t help")
                    for _cmd_name in command_information.keys():
                        print("\t" + _cmd_name)
                    print("")
                    print("可通过help [command]的形式获取具体命令的操作")


                def help_command(_command: str) -> None:
                    match _command:
                        case "help":
                            help_doc()
                        case "exit" | "quit" | "exit/quit" | "quit/exit":
                            exit_quit_doc()
                        case "define" | "create" | "define/create" | "create_define":
                            define_create_doc()
                        case "redef" | "update" | "redef/update" | "update/redef":
                            redef_update_doc()
                        case "calc" | "eval" | "eval/calc" | "calc/eval":
                            calc_eval_doc()
                        case "pyrun":
                            pyrun_doc()
                        case "graph":
                            graph_doc()
                        case _:
                            print("未知的命令, 无法提供帮助@^@")


                if len(command_lst) == 1:
                    help_main()
                else:
                    help_command(command_lst[1])
                # endregion
            case "exit" | "quit":
                # region
                # 退出的指令
                print("good bye!")
                # 退出返回值0
                quit(0)
                # endregion
            case "define" | "create":
                # region
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
                        print("函数的解析式为: ", latex(_variable_value))
                    except Exception as e:
                        print("表达式错误: ", e)
                        return
                    var_dictionary[_variable_symbol] = _variable_value


                _create_type: Literal["variable", "function"]
                if len(command_lst) == 1:
                    _create_type_prompt: str = input("请输入创建对象的类型[var | func]:>>")
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
                # endregion
            case "solve":
                # region
                def _solve_equation() -> None:
                    equation = input("请输入方程:>>")
                    # unknowns = input("请输入方程的求解元:>>")
                    try:
                        expr = latex2sympy2.latex2sympy(equation)
                        if isinstance(expr, list):
                            res = solve(expr)
                        else:
                            res = solve([expr])
                    except Exception as e:
                        print("表达式错误:\t", e)
                        return
                    print(latex(res))


                def _solve_equation_cases() -> None:
                    equation = input("请输入方程组:>>")
                    try:
                        result = solve_equation(equation, formatter="latex")
                    except Exception as e:
                        print("表达式错误", e)
                        return
                    print(result)


                # _solve_type: Literal["once", "multi"]
                if len(command_lst) == 1:
                    _solve_str = input("请输入求解类型[once | multi]:>>")
                else:
                    _solve_str = command_lst[1]
                match _solve_str:
                    case "once":
                        _solve_equation()
                    case "multi":
                        _solve_equation_cases()
                    case _:
                        print("未知类型:", _solve_str)
                # endregion
            case "redef" | "update":
                # region
                def _redefine_variable() -> None:
                    var_name = input("要修改的变量符号:>>")
                    value_str = input("修改的值:>>")
                    try:
                        value_expr = latex2sympy2.latex2sympy(value_str)
                    except Exception as e:
                        print("表达式错误:", e)
                        return
                    var_dictionary[Symbol(var_name)] = value_expr


                _redefine_variable()
                # endregion
            case "undef" | "remove":
                # region
                def _remove_variable() -> None:
                    variable_name = input("请输入需要删除的对象符号:>>")
                    var_symbol = Symbol(variable_name)
                    if var_symbol in var_dictionary.keys():
                        del var_dictionary[var_symbol]
                    else:
                        print("未找到相应函数")


                _remove_variable()
                # endregion
            case "calc" | "eval":
                # region
                def _calculate_expression() -> None:
                    expr_str: str = input("请输入表达式:>>")
                    try:
                        expr = latex2sympy2.latex2sympy(expr_str)
                    except Exception as e:
                        print("表达式错误", e)
                        return
                    try:
                        print("表达式化简形式:<<", latex(simplify(expr)))
                    except:
                        print("无法化简")
                    print("表达式求值(以目前变量):<<", latex(expr.evalf(subs=var_dictionary)))


                _calculate_expression()
                # endregion
            case "graph":
                # region
                def _graph_function(function_tex: str) -> None:
                    global INIT_GRAPH, grapher
                    _color = input("请输入颜色:>>")
                    _width = input("请输入粗细:>>")
                    try:
                        _l_limit = nfloat(latex2sympy2.latex2sympy(input("请输入函数下界:>>")).evalf(subs=var_dictionary))
                        _r_limit = nfloat(latex2sympy2.latex2sympy(input("请输入函数上界:>>")).evalf(subs=var_dictionary))
                        _fun = latex2sympy2.latex2sympy(function_tex)
                    except Exception as e:
                        print("错误: ", e)
                        return
                    if not INIT_GRAPH:
                        grapher = FunctionGrapher()
                        INIT_GRAPH = True
                    grapher.draw_function(
                        _fun,
                        color=_color,
                        width=_width,
                        l_limit=_l_limit,
                        r_limit=_r_limit
                    )

                def _graph_pol_function(function_tex: str) -> None:
                    global INIT_GRAPH, pol_grapher
                    _color = input("请输入颜色:>>")
                    _width = input("请输入粗细:>>")
                    try:
                        _l_limit = nfloat(latex2sympy2.latex2sympy(input("请输入极坐标函数下界:>>")).evalf(subs=var_dictionary))
                        _r_limit = nfloat(latex2sympy2.latex2sympy(input("请输入极坐标函数上界:>>")).evalf(subs=var_dictionary))
                        _fun = latex2sympy2.latex2sympy(function_tex)
                    except Exception as e:
                        print("错误: ", e)
                        return
                    if not INIT_GRAPH:
                        pol_grapher = FunctionGrapher(pol_graph=True)
                        INIT_GRAPH = True
                    pol_grapher.draw_function(
                        func=_fun,
                        color=_color,
                        width=_width,
                        l_limit=_l_limit,
                        r_limit=_r_limit
                    )

                if _graph_function == _graph_pol_function == not_opened_command_used_error:
                    not_opened_command_used_error()
                    continue

                if len(command_lst) == 1:
                    _fun_type = input("请输入画图的函数类型[rec | pol]:")
                else:
                    _fun_type = command_lst[1]
                if len(command_lst) == 3:
                    _fun_expr = command_lst[2]
                elif len(command_lst) == 2 and command_lst[1] not in ["rec", "pol"]:
                    _fun_expr = command_lst[1]
                else:
                    _fun_expr = input("请输入函数表达式：>>")
                match _fun_type:
                    case "rec":
                        _graph_function(_fun_expr)
                    case "pol":
                        _graph_pol_function(_fun_expr)
                    case _:
                        print("未知类型:", _fun_type)
                # endregion
            case "pyrun":
                # region
                @extension_command
                def run_pycode() -> None:
                    if len(command_lst) > 1 and command_lst[1] == "file":
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
                # endregion
            case _:
                print(f"未知命令: {main_command}")
