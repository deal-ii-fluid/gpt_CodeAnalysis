import openai
import os
import glob
import concurrent.futures
from datetime import datetime
import traceback  # 用于获取错误堆栈
import chardet  # 导入编码检测库
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


# 设置您的 OpenAI API。
openai.api_base = 'https://api.ngapi.top/v1'
my_api_key = os.getenv('OPENAI_API_KEY')
if my_api_key is None:
    print("错误: 未设置 OPENAI_API_KEY 环境变量。")
    exit()

def send_request_to_openai(model, my_api_key, messages):
    openai.api_key = my_api_key
    response = openai.ChatCompletion.create(model=model, messages=messages, temperature=0.8)
    return response


def process_file(file_path, output_directory, log_file_path):
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在.")
        return

    try:
        # 使用 chardet 检测文件编码
        with open(file_path, 'rb') as file:
            rawdata = file.read()
        encoding_result = chardet.detect(rawdata)
        encoding = encoding_result['encoding']

        # 读取文件内容
        with open(file_path, 'r', encoding=encoding) as file:
            user_content = file.read()

        attempt = 0  # 尝试次数
        success = False

        while attempt < 5 and not success:  # 最多尝试5次-5次后为0.2373
            try:
                messages = [
                  {"role": "system", "content": "**Task Description**: You are an expert in Fortran 77 programming and the Finite Element Method (FEM) projects. Your mission, should you choose to accept it, involves performing an in-depth analysis of a specific Fortran subroutine within an FEM project. Dive deep into its functionalities and implementations! At the end of your analysis, craft a summary of the code in a docstring style, but here's the twist - it needs to be in **Chinese**. Make sure your summary is both precise and concise. ** Note**: There is only one subroutine; The output of this task is a descriptive summary only and **does not include the actual Fortran code**. Ready to embark on this coding adventure? \n**Please complete your analysis and summary in the sections below**:\n- **Subroutine Name**: \n- **One-liner Summary**: \n- **Detailed Parameter Description**: \n- **Specific Functionality**: \n- **Algorithm Implementation**: \n- **Points of Attention**: \n- **UML Diagram Code and Description**: \n $$-->>Here is the Example of Output Format you can follow<<--$$:  Subroutine [Name of Subroutine]: Summarize the main purpose of the subroutine in one crisp sentence. \n    1. Parameters: \n       Parameter name:  [Type], [specific purpose and any particular details of this parameter]\n  2. Specific Functionality: \n       [Describe the main functions that the subroutine accomplishes and how it interacts with other components]\n    3. Algorithm Implementation: \n       [Provide an overview of the algorithm, including key strategies and methods employed]\n    4. Points of Attention: \n       [List any issues or details to be particularly mindful of during the coding or execution process]\n    5. UML Diagram: \n       [Create a UML activity diagram using PlantUML syntax that outlines the code's workflow and structure. While the key parts of the UML diagram should be annotated in **Chinese**, UML syntax keywords (like 'start', 'stop', 'if', 'else', etc.) must be in English.  Here is Example plantUML Diagram you can follow:  @startuml\n  start\n  :initialize parameters;\n  if (Are parameters valid?) then (true)\n      :execute main computations;\n      if (Are additional steps required?) then (true)\n          :conduct additional steps;\n      else (false)\n          -[dashed]-> :continue process;\n      endif\n      :gather results;\n  else (false)\n      :return error message;\n  endif\n  :finalize;\n  stop\n  @enduml\n  ```\n"},
                    {'role': 'user', 'content': user_content[:len(user_content) * 3 // 4]},  # 取前3/4的文本
                ]

                print(f"处理文件: {file_path}")
                response = send_request_to_openai('gpt-3.5-turbo-16k', my_api_key, messages)
                translated_content = response.choices[0].message['content']

                # 若调用成功，则跳出循环
                success = True

            except openai.error.OpenAIError as e:  # 捕获 OpenAI 的错误
                if '当前分组上游负载已饱和' in str(e):
                    print(f"警告: 超出负载限制，正在减少请求大小并重试 ({attempt + 1})")
                    user_content = user_content[:len(user_content) * 3 // 4]  # 如果超出限制，减少文本大小
                    attempt += 1
                else:
                    raise  # 如果是其他类型的错误，继续向上抛出异常

        if not success:
            raise Exception("错误: 经过多次尝试后，请求仍然失败。")

        # 创建输出目录
        os.makedirs(output_directory, exist_ok=True)
        base_name = os.path.basename(file_path)
        output_file_path = os.path.join(output_directory, base_name)

        # 保存翻译后的内容
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(translated_content)

        print(f"翻译已保存到 {output_file_path}")

    except Exception as e:
        error_message = f"处理文件时出错 {file_path}: {str(e)}\n"
        print(error_message)

        # 记录错误信息
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(error_message)
            log_file.write(traceback.format_exc())  # 写入错误堆栈信息
            log_file.write("\n")


def start():
    src_directory = 'src'
    output_directory = 'src-1'

    fortran_files = glob.glob(os.path.join(src_directory, '*.f'))

    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    log_file_path = f'fail-{current_time}.log'

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future_to_file = {executor.submit(process_file, file_path, output_directory, log_file_path): file_path for file_path in fortran_files}

        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                future.result()
            except Exception as exc:
                print(f'{file} 生成异常: {exc}')


