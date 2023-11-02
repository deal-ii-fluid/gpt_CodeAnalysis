from fparser.common.readfortran import FortranStringReader
from fparser.two.parser import ParserFactory

# 假设这是你的Fortran源代码，包含了一些注释
fortran_code = """
! 这是一个注释
program hello
  ! 另一个注释
  print *, "Hello, World!"
end program hello
"""

# 创建一个FortranReaderBase对象，启用保留注释选项
reader = FortranStringReader(fortran_code, ignore_comments=True)

# 创建一个Fortran2003解析器
factory = ParserFactory()
parser = factory.create(std="f2003")

# 使用创建的解析器读取和解析Fortran源代码
ast = parser(reader)

# 打印解析出的AST（抽象语法树）
print(ast)

