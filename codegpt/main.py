import os
import typer
import json
import logging
import concurrent.futures
import sys

sys.path.append("../codegpt")

from codegpt import gpt_interface as gpt

from codegpt import prompts
from codegpt import files

from typing import List, Optional
from pathlib import Path

from rich.progress import track




app = typer.Typer(
    no_args_is_help=True,
)


@app.command("do")
def edit_file(
    instruction: str = typer.Argument(
        ...,
        help="Instruction to edit the file(s). Keep it short! Wrap with quotes.",
    ),
    backup: bool = typer.Option(
        False,
        "--backup",
        "-b",
        help="Whether to create a backup of the original file(s).",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Don't ask for confirmation.",
    ),
    raw_code: str = typer.Option(
        None,
        "--raw-code",
        "-c",
        help="Raw code to edit. Overrides filenames. Use quotes to wrap the code.",
    ),
    json_out: bool = typer.Option(
        False, "--json-out", "-j", help="Output the response in raw json format."
    ),
    raw_out: bool = typer.Option(
        False,
        "--raw-out",
        "-r",
        help="Output the raw 'code' from the response and exit the function.",
    ),
    filenames: Optional[List[Path]] = typer.Argument(
        None, help="File(s) to edit or for context."
    ),
):
    """
    Do something given some code for context. Asking for documents, queries, etc. should work okay. Edits are iffy, but work a lot of the time.

    Your code better be in git before you use this. If the instruction is one of the quick prompt options (like 'comment' or 'docs'), it will do that prompt automatically. For more info, run 'codegpt quick --help'.

    FILENAMES: list of filenames to edit. If not provided, will prompt for input.
    INSTRUCTION: the instruction to edit the file(s). Keep it short!
    """

    if raw_out or json_out:
        logging.basicConfig(level=logging.CRITICAL)

    if not filenames and not raw_code:
        raise typer.BadParameter(
            "Either --filenames (-f) or --raw-code (-c) must be provided."
        )

    code = {"code": raw_code} if raw_code else files.load_text(filenames)

    if instruction in prompts.prompts:
        instruction = prompts.prompts[instruction]

    result = gpt.send_iffy_edit(instruction, code, yes=yes, clipboard=bool(raw_code))

    if json_out:
        print(json.dumps(result, sort_keys=True, indent=4))
        return

    if raw_out:
        print(result.get("code") or result)
        return

    files.write_text(result, backup)
    typer.secho("Done!", color=typer.colors.BRIGHT_BLUE)


@app.command("quick")
def quick_edit_file(
    option: str = typer.Argument(..., help=f"{{{'|'.join(prompts.prompts.keys())}}}"),
    backup: bool = typer.Option(
        False,
        "--backup",
        "-b",
        help="Whether to create a backup of the original file(s).",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Don't ask for confirmation.",
    ),
    raw_code: str = typer.Option(
        None,
        "--raw-code",
        "-c",
        help="Raw code to edit. Overrides filenames. Use quotes to wrap the code.",
    ),
    json_out: bool = typer.Option(
        False, "--json-out", "-j", help="Output the response in raw json format."
    ),
    raw_out: bool = typer.Option(
        False,
        "--raw-out",
        "-r",
        help="Output the raw 'code' from the response and exit the function.",
    ),
    filenames: Optional[List[Path]] = typer.Argument(
        None, help="File(s) to edit or for context."
    ),
):
    """
    Edit a file using codegpt's built in prompts.

    Arguments for `option`:
    - comment - Adds or updates comments
    - varnames - Makes variable names reasonable
    - ugh - Do anything GPT can to make the code suck less (might break stuff...)
    - docs - Generate (or update) docs, including README.md
    - bugs - Comment in code where the bugs are if GPT sees them (iffy)
    - vulns - Comment in code where the vulns are if GPT sees them (iffy)
    """
    if option not in prompts.prompts:
        raise typer.BadParameter(
            f"{option} is not a valid option. Must be one of {list(prompts.prompts.keys())}"
        )

    if not filenames and not raw_code:
        raise typer.BadParameter(
            "Either FILENAMES or --raw-code (-c) must be provided."
        )

    code = {"code": raw_code} if raw_code else files.load_text(filenames)
    result = gpt.send_iffy_edit(
        prompts.prompts[option], code, yes=yes, clipboard=bool(raw_code)
    )

    if json_out:
        print(json.dumps(result, sort_keys=True, indent=4))
        return

    if raw_out:
        print(result["code"])
        return

    files.write_text(result, backup)
    typer.secho("Done!", color=typer.colors.BRIGHT_BLUE)

def process_docs_file(filename, chunk, docs_directory="docs", retry=5):
    try:
        start = 0
        chunk_left = chunk
        result = None
        while chunk_left and retry:
            try:
                typer.secho(f"Starting process with chunk size: {len(chunk_left)}", fg="yellow")  # Log the start and chunk size
                prompt = prompts.generate_review_instructions(filename, chunk_left)
                result = gpt.send_normal_completion(prompt, 15000, True)
            except Exception as e:
                if "reduce the length of the messages" in str(e):
                    typer.secho(f"Too long, reducing chunk size in",fg="red")  # Log the reduction
                    chunk_left = chunk_left[:int(len(chunk_left) * 0.75)]  # decrease the chunk size
                    retry -= 1  # decrease retries
                else:
                    return str(e)  # return the exception message if it's not the known type
            else:
                break  # break the loop if no exception occurred
        start = len(chunk_left)
        chunk_left = chunk[start:]


# 暂时弃用
#        while chunk_left and retry:  # 暂时弃用该方案，会累计误差，导致分析失真
#            try:
#                typer.secho(f"Processing remaining chunk with size: {len(chunk_left)}",fg="yellow")  # Log the start of remaining chunk processing
#                prompt_x = prompts.generate_codemissing_instructions(filename, chunk_left, result)
#                result = gpt.send_normal_completion(prompt_x, 15000, True)
#            except Exception as e:
#                if "reduce the length of the messages" in str(e):
#                    typer.secho(f"Too long, reducing chunk size in chunk_left",fg="red")  # Log the reduction
#                    chunk_left = chunk_left[:int(len(chunk_left) * 0.75)]  # decrease the chunk size and continue the process
#                    retry -= 1
#                else:
#                    return str(e)  # return the exception message if it's not the known type
#            else:
#                start = len(chunk_left)
#                chunk_left = chunk[start:]  # update the remaining part of the chunk
#      
    except Exception as e:
            return str(e)  # return the exception message if it's not the known type
    
    # Write the documentation for the current code chunk to a file
    outname = f"./docs/{filename}.md"
    Path(outname).parent.mkdir(parents=True, exist_ok=True)
    files.write_text([{"filename": outname, "code": result}])
    typer.secho(f"Wrote documentation for {filename} to {outname}", fg="green")






@app.command("docs")
def docs(paths: List[Path] = typer.Argument(None, exists=True, dir_okay=True, file_okay=True)):
    data = files.split_code_into_chunks(paths)
    typer.secho(f"data: {data}")
    input("stop")
    typer.secho(f"Found {len(data)} files. Documenting...", color=typer.colors.BRIGHT_BLUE)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(process_docs_file, filename, chunk): filename for filename, chunk in track(data.items())}

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                filename = futures[future]
                typer.secho(f'{filename} generated an exception: {exc}', color=typer.colors.RED)

    typer.secho("Done!", color=typer.colors.GREEN)



@app.command("config")
def config():
    """
    Configuration instructions for the OpenAI secret key for the codegpt CLI.
    """
    # check if the secret key is already set in the environment variables
    if "OPENAI_API_KEY" in os.environ:
        typer.secho(
            "OPENAI_API_KEY is already set in the environment! You probably don't need this.",fg=typer.colors.BRIGHT_BLUE,
        )
    else:
        typer.confirm(
            """
I recommend setting your API key as an environment variable:
https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety

Windows users can also use `setx` like:

`$ export OPENAI_API_KEY=<sy-YOUR_API_KEY>`

from an admin console.""".strip()
        )


if __name__ == "__main__":
    app()
