# Tracor

## 🚀 Debug Python Scripts Faster

This utility script allows you to execute a Python script line by line, catch any errors that occur along the way, and provide essential debugging information with enhanced context. Additionally, it generates a well-formatted Markdown report highlighting the errors encountered during execution.

## Features

- Executes a Python script line by line.
- Catches and logs errors with detailed context and colored output for better readability.
- Generates a Markdown report summarizing the errors.
- Allows customizable colors for different parts of the error messages.
- Supports stopping execution on the first error or after a specified number of errors.
- Includes options to show full tracebacks in the Markdown report.

## Usage

### Basic Usage

You can download tracor from [PyPI](https://pypi.org/project/tracor/):
```sh
pip install tracor
```

Then, you can run it with:
```sh
tracor path/to/your_script.py [options]
```

### Usage With Flags
* `--stop-on-error`: Stop execution on the first error.
* `--output-file <file>`: Specify the output Markdown file for the error report.
* `--log-level <level>`: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
* `--max-errors <n>`: Limit the number of errors to report before stopping execution.
* `--show-traceback`: Include full traceback in the Markdown report.
* `--execution-color <color>`: Color for executed lines (default: GREEN).
* `--error-color <color>`: Color for error lines (default: RED).
* `--code-color <color>`: Color for code in error messages (default: YELLOW).
* `--type-color <color>`: Color for error type in error messages (default: CYAN).
* `--message-color <color>`: Color for error message in error messages (default: MAGENTA).
* `--traceback-color <color>`: Color for traceback in error messages (default: WHITE).


Example - 
```sh
tracor example_script.py --output-file custom_error_report.md --log-level DEBUG --max-errors 5 --show-traceback --execution-color GREEN --error-color RED --code-color YELLOW --type-color CYAN --message-color MAGENTA --traceback-color WHITE
```

## Output
### Terminal Output
The terminal output will show the execution of each line and any errors encountered with enhanced multi-colored highlighting for better readability.

### Markdown Report
A well-formatted Markdown report summarizing the errors will be generated. The report includes:

A summary section with the total number of errors.
A detailed table with line numbers, code snippets, error types, error messages, and tracebacks.