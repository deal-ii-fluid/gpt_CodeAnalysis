import os
import ast
import astunparse
import fparser
from fparser.two.parser import ParserFactory
from fparser.common.readfortran import FortranStringReader

class CodeParser:
    def parse_and_extract_functions(self, source_code):
        raise NotImplementedError()

class PythonCodeParser(CodeParser):
    def parse_and_extract_functions(self, source_code):
        tree = ast.parse(source_code)
        new_body = [node for node in tree.body if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Str))]
        tree.body = new_body
        cleaned_code = astunparse.unparse(tree)

        functions = [(node.name, node.lineno, max((child.lineno for child in ast.walk(node) if hasattr(child, 'lineno')), default=node.lineno)) for node in tree.body if isinstance(node, (ast.FunctionDef))]

        return cleaned_code, functions

class FortranCodeParser(CodeParser):
    def parse_and_extract_functions(self, source_code):
        parser = ParserFactory().create(std="f2003")
        reader = FortranStringReader(source_code)
        parse_tree = parser(reader)
        new_content = [item for item in parse_tree.content if not isinstance(item, fparser.two.Fortran2003.Comment)]
        parse_tree.content = new_content
        cleaned_code = parse_tree.tofortran()

        functions = []
        for item in new_content:
            if isinstance(item, fparser.two.Fortran2003.Subroutine_Subprogram):
                name = str(item.content[0].items[1])
                start_line = item.content[0].item.span[0]
                end_line = item.content[-1].item.span[1]
                functions.append((name, start_line, end_line))
            elif isinstance(item, fparser.two.Fortran2003.Function_Subprogram):
                name = str(item.content[0].items[1])
                start_line = item.content[0].item.span[0]
                end_line = item.content[-1].item.span[1]
                functions.append((name, start_line, end_line))

        return cleaned_code, functions
