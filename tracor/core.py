import argparse
import traceback
import logging
from contextlib import contextmanager
from collections import defaultdict
from colorama import init, Fore, Style
import sys

# Initialize colorama
init(autoreset=True)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

error_details = []
error_stats = defaultdict(int)

@contextmanager
def execute_line_by_line_context():
    global_vars = {}
    local_vars = {}
    yield global_vars, local_vars

def log_execution(line_number, code_block, colors):
    logger.info(f"{colors['execution']}Executed line {line_number}: {code_block.strip()}")

def log_error(line_number, code_block, e, tb, show_traceback, colors):
    error_type = type(e).__name__
    error_message = str(e)
    logger.error(f"{colors['error']}Error on line {line_number}: {colors['code']}{code_block.strip()}")
    logger.error(f"{colors['error']}Type: {colors['type']}{error_type}, {colors['error']}Message: {colors['message']}{error_message}")
    if show_traceback:
        logger.error(f"{colors['error']}Traceback:\n{colors['traceback']}{tb}")

    # Collect error details for markdown report
    error_details.append({
        "line_number": line_number,
        "code": code_block.strip(),
        "error_type": error_type,
        "error_message": error_message,
        "traceback": tb if show_traceback else "Traceback hidden"
    })

    # Update error statistics
    error_stats[error_type] += 1

def execute_line_by_line(file_path, stop_on_error, max_errors, show_traceback, colors):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)
    line_number = 1
    code_block = ''
    inside_multiline = False
    error_count = 0

    logger.info(f"{Fore.BLUE}Starting execution of {file_path} ({total_lines} lines)...\n")

    with execute_line_by_line_context() as (global_vars, local_vars):
        while line_number <= total_lines:
            line = lines[line_number - 1]
            stripped_line = line.strip()
            code_block += line

            # Check if we are inside a multiline statement
            if stripped_line.endswith('\\') or inside_multiline:
                inside_multiline = True
                line_number += 1
                continue

            # Try executing the accumulated code block
            try:
                exec(code_block, global_vars, local_vars)
                log_execution(line_number, code_block, colors)
            except Exception as e:
                tb = traceback.format_exc()
                log_error(line_number, code_block, e, tb, show_traceback, colors)
                error_count += 1

                if stop_on_error or (max_errors and error_count >= max_errors):
                    logger.error(f"{colors['error']}Stopping execution due to error limit.\n")
                    break

            # Reset code block and flags for the next statement
            code_block = ''
            inside_multiline = False

            # Update progress
            progress = (line_number / total_lines) * 100
            sys.stdout.write(f"\r{Fore.CYAN}Progress: {progress:.2f}%")
            sys.stdout.flush()

            line_number += 1

    sys.stdout.write("\n")
    logger.info(f"{Fore.BLUE}\nExecution completed with {error_count} errors.\n")

def generate_markdown_report(file_path, output_file, show_traceback):
    if not output_file:
        output_file = file_path.replace('.py', '_error_report.md')

    with open(output_file, 'w') as report_file:
        report_file.write("# Error Report\n\n")
        report_file.write("## Summary\n\n")
        report_file.write(f"Total Errors: {len(error_details)}\n\n")
        report_file.write("## Error Statistics by Type\n\n")
        report_file.write("| Error Type         | Count |\n")
        report_file.write("|--------------------|-------|\n")
        for error_type, count in error_stats.items():
            report_file.write(f"| {error_type.ljust(18)} | {str(count).ljust(5)} |\n")
        report_file.write("\n## Details\n\n")
        report_file.write("| Line Number | Code                                    | Error Type       | Error Message                           | Traceback          |\n")
        report_file.write("|-------------|-----------------------------------------|------------------|-----------------------------------------|--------------------|\n")
        for error in error_details:
            line = f"| {str(error['line_number']).ljust(12)} " \
                   f"| `{error['code'][:40].ljust(40)}` " \
                   f"| {error['error_type'].ljust(16)} " \
                   f"| {error['error_message'][:40].ljust(40)} " \
                   f"| {error['traceback'][:30].replace('\n', ' ').ljust(30)} |\n"
            report_file.write(line)

    logger.info(f"{Fore.BLUE}Markdown report generated: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Python script line by line with error handling.')
    parser.add_argument('script_path', type=str, help='Path to the Python script to debug')
    parser.add_argument('--stop-on-error', action='store_true', help='Stop execution on the first error')
    parser.add_argument('--output-file', type=str, help='Specify the output markdown file for the error report')
    parser.add_argument('--log-level', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set the logging level')
    parser.add_argument('--max-errors', type=int, help='Limit the number of errors to report before stopping execution')
    parser.add_argument('--show-traceback', action='store_true', help='Include full traceback in the markdown report')
    parser.add_argument('--execution-color', type=str, default='GREEN', help='Color for executed lines')
    parser.add_argument('--error-color', type=str, default='RED', help='Color for error lines')
    parser.add_argument('--code-color', type=str, default='YELLOW', help='Color for code in error messages')
    parser.add_argument('--type-color', type=str, default='CYAN', help='Color for error type in error messages')
    parser.add_argument('--message-color', type=str, default='MAGENTA', help='Color for error message in error messages')
    parser.add_argument('--traceback-color', type=str, default='WHITE', help='Color for traceback in error messages')
    args = parser.parse_args()

    # Set logging level
    logger.setLevel(args.log_level)

    # Define colors
    colors = {
        'execution': getattr(Fore, args.execution_color.upper(), Fore.GREEN),
        'error': getattr(Fore, args.error_color.upper(), Fore.RED),
        'code': getattr(Fore, args.code_color.upper(), Fore.YELLOW),
        'type': getattr(Fore, args.type_color.upper(), Fore.CYAN),
        'message': getattr(Fore, args.message_color.upper(), Fore.MAGENTA),
        'traceback': getattr(Fore, args.traceback_color.upper(), Fore.WHITE),
    }

    execute_line_by_line(args.script_path, args.stop_on_error, args.max_errors, args.show_traceback, colors)
    generate_markdown_report(args.script_path, args.output_file, args.show_traceback)
