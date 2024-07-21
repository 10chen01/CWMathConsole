import latex2sympy2

import cwconsole
import pytest


class TestConsole:
    def test_decorator_1(self):
        @cwconsole.closing_command
        def my_close_command():
            return "Meow"

        assert my_close_command() != "Meow"

    def test_decorator_2(self):
        cwconsole.EXTEND_VERSION = False

        @cwconsole.extension_command
        def my_extend_command():
            return "CLS"

        assert my_extend_command() != "CLS"

        cwconsole.EXTEND_VERSION = True

