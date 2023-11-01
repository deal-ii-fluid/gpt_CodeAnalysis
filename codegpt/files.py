import os
import sys
import typer
import math
import re
import magic
from pathlib import Path

import ast
import astunparse
import fparser
from fparser.two.parser import ParserFactory
from fparser.common.readfortran import FortranStringReader




def load_text(filenames):
    out = {}
    for filename in filenames:
        with open(filename, "r") as f:
            out[filename] = f.read()
    return out


def write_text(files, backup=False):
    # If the backup option is specified and the file exists,
    # write the existing file to <filename>.bak
    for i, out in enumerate(files):
        filename = out.get("filename", f"{i}.txt").strip()
        if backup and os.path.exists(filename):
            with open(filename, "r") as f_in:
                with open(f"{filename}.bak", "w") as f_out:
                    f_out.write(f_in.read())

        # Write the new text to the file
        with open(filename, "w") as f:
            f.write(out["code"])
        if "explanation" in out:
            typer.secho(f"{filename} - " + out["explanation"], color=typer.colors.BLUE)


def split_code_into_chunks(paths):
    chunks = {}
    for path in paths:
        if path.is_dir():
            for root, _, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    typer.secho(f"Processing file 1: {file_path}")
                    chunks.update(process_file(file_path))
        else:
            typer.secho(f"Processing file 2: {path}")
            chunks.update(process_file(path))
    return chunks


class CodeParser:
    def parse_and_extract_functions(self, source_code):
        raise NotImplementedError()

class PythonCodeParser(CodeParser):
    def parse_and_extract_functions(self, source_code):
        # 第一次解析：移除注释
        tree = ast.parse(source_code)
        new_body = [node for node in tree.body if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Str))]
        tree.body = new_body
        cleaned_code = astunparse.unparse(tree)

        # 第二次解析：在清理过的代码上提取函数
        tree_clean = ast.parse(cleaned_code)
        functions = [(node.name, node.lineno, max((child.lineno for child in ast.walk(node) if hasattr(child, 'lineno')), default=node.lineno)) for node in tree_clean.body if isinstance(node, (ast.FunctionDef))]

        return cleaned_code, functions

class FortranCodeParser(CodeParser):
    def parse_and_extract_functions(self, source_code):
        # 解析并移除注释
        parser = ParserFactory().create(std="f2003")
        reader = FortranStringReader(source_code)
        parse_tree = parser(reader)
        new_content = [item for item in parse_tree.content if not isinstance(item, fparser.two.Fortran2003.Comment)]
        parse_tree.content = new_content
        cleaned_code = parse_tree.tofortran()

        # 在清理过的代码上提取函数
        reader_clean = FortranStringReader(cleaned_code)
        parse_tree_clean = parser(reader_clean)
        functions = []
        for item in parse_tree_clean.content:
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

def process_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    parsers = {
        '.py': PythonCodeParser(),
        '.f': FortranCodeParser(),
        '.F': FortranCodeParser(),
    }

    parser = parsers.get(file_extension)
    if parser is None:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    with open(file_path, 'r') as file:
        source_code = file.read()

    cleaned_code, functions = parser.parse_and_extract_functions(source_code)

    chunks = {}
    for fn_name, start_line, end_line in functions:
        chunk = '\n'.join(cleaned_code.splitlines()[start_line-1: end_line]) # -1 as splitlines is 0 indexed
        chunks[fn_name] = chunk

    return chunks

