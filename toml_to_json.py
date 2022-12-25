'''Convert VSCode snippets written in TOML-format to JSON-format.

This module converts TOML-formatted snippets to a JSON format
that can be used by VSCode. VSCode requires snippets to be written
in JSON format, but this is not human-readable.
TOML format allows for the use of multiline strings,
making it easier for humans to read and edit through copy and paste.

TOML-fometted snippets:
    [SNIPPET_NAME]
    scope = "LANG_TYPE"
    prefix = "SNIPPET_PREFIX"
    description = "SNIPPET_DESCRIPTION"
    body = """
    MULTI_LINE_SNIPPET_BODY
    """

Additionally, you can use the following attributes for more advanced
configurations. These are attributes that are not available in
original VSCode JSON snippets:

    # If the source attribute is specified, the body attribute will be ignored
    source = "SOURCE_FILE"
    # Use lines from START_LINE to END_LINE only (inclusive, 1-indexed)
    range = [START_LINE, END_LINE]
    # Removes leading blank lines. Default is false.
    trim_leading_blank_lines = false
    # Removes trailing blank lines. Default is false
    trim_trailing_blank_lines = false
'''

from typing import Any
import toml
import json
import os
import sys
import argparse


def process_body_data(data: dict[str, Any]) -> dict[str, Any]:
    """Process snippet body.

    If 'source' in data, load body from source file.
    If 'range' in data, crop lines.
    If 'trim_*_blank_lines' in data, delete blank lines.

    Args:
        data: dicitionary of snippets

    Returns:
        Processed snippet data
    """
    body = ''
    if 'source' in data:
        with open(data.pop('source'), encoding='utf-8') as source_file:
            body = source_file.read().splitlines()
    else:
        body = list(data['body'].split('\n'))
    if 'range' in data:
        range = data.pop('range')
        assert len(range) == 2
        assert range[0] <= range[1]
        assert range[0] >= 1
        body = body[range[0]-1:range[1]]
    if data.pop('trim_leading_blank_lines', False) is True:
        while len(body) > 0 and len(body[0]) == 0:
            body = body[1:]
    if data.pop('trim_trailing_blank_lines', False) is True:
        while len(body) > 0 and len(body[-1]) == 0:
            body = body[:-1]

    data['body'] = body
    return data


def convert_toml_string(toml_str: str) -> str:
    """Convert TOML string to JSON string.

    Args:
        toml_str: toml string snippet.

    Returns:
        JSON formatted snippet string.
    """
    data: dict[str, dict[str, Any]] = toml.loads(toml_str)
    data: dict[str, dict[str, Any]] = {
        k: process_body_data(v) for k, v in data.items()}
    result_json = json.dumps(data, indent=2)
    return result_json


def output_result(result_json: str, json_file_path: str | None,
                  overwrite: bool) -> None:
    """Output processed JSON.

    If `json_file_path` is None, output to stdout.
    Otherwise, save to `json_file_path`.

    Args:
        result_json: JSON snippet text.
        json_file_path: Output JSON file path.
        overwrite: When `json_file_path` exists,
            if overwrite == True then overwrites it, otherwise throws IOError.
    """
    if json_file_path is None:
        print(result_json)
        return None

    if os.path.exists(json_file_path) and overwrite is False:
        raise OSError(f'''OSError:
    the destination json file exists: {json_file_path}
    if you want to overwrite it, use '-f' flag.
''')
    with open(json_file_path, mode="w") as output_file:
        output_file.write(result_json)


def load_toml_string(toml_file_path: str | None) -> str:
    """Load TOML string from file or stdin."""
    if toml_file_path is None:
        res: str = sys.stdin.read()
    else:
        with open(toml_file_path) as f:
            res: str = f.read()
    return res


example_toml = '''
[for]
scope = "cpp"
prefix = "for"
description = "insert 'for'"
body = """
for(int ${1:i} = 0; ${1:i} < ${2:n}; ${1:i}++){
    $2
}
"""
trim_trailing_blank_lines = true

[lambda]
scope = "cpp"
prefix = "lambda"
description = "insert lambda"
body = """
auto ${1:lambda_name} = [&]($2){
    $3
};
"""
trim_trailing_blank_lines = true
'''

example_json = convert_toml_string(example_toml)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="toml_to_json.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description=f'''
Convert VSCode snippets written in TOML-format to JSON-format.

Example:
input TOML snippet
```toml
{example_toml}
```

output JSON snippet:
```json
{example_json}
```
''')
    parser.add_argument('-i', '--toml_file_path',
                        help='input toml snippet file', default=None)
    parser.add_argument('-o', '--json_file_path',
                        help='output json snippet file', default=None)
    parser.add_argument('-f', '--overwrite',
                        action='store_true',
                        help='Overwrites existing json file')
    args = parser.parse_args()

    input_toml = load_toml_string(args.toml_file_path)
    result_json = convert_toml_string(input_toml)
    output_result(result_json, args.json_file_path, args.overwrite)
