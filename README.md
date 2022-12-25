# TOML Snippet for VSCode
Convert VSCode snippets written in TOML-format to JSON-format.

[Snippets in Visual Studio Code](https://code.visualstudio.com/docs/editor/userdefinedsnippets)

---

This module converts TOML-formatted snippets to a JSON format
that can be used by VSCode. VSCode requires snippets to be written
in JSON format, but this is not human-readable.
TOML format allows for the use of multiline strings,
making it easier for humans to read and edit through copy and paste.

## TOML-fometted snippets:
Basic TOML snippet format. 

```toml
[SNIPPET_NAME]
scope = "LANG_TYPE" # optional
prefix = "SNIPPET_PREFIX"
description = "SNIPPET_DESCRIPTION"
body = """
MULTI_LINE_SNIPPET_BODY
"""
```

Additionally, you can use the following attributes for more advanced
configurations. These are attributes that are not available in
original VSCode JSON snippets.

```
source = "SOURCE_FILE"            # If the source attribute is specified, the body attribute will be ignored
range = [START_LINE, END_LINE]    # Use lines from START_LINE to END_LINE only (inclusive, 1-indexed)
trim_leading_blank_lines = false  # Removes leading blank lines. Default is false.
trim_trailing_blank_lines = false # Removes trailing blank lines. Default is false
```


## Installation

This module consists of a single python file `toml_to_json.py` so you can download
the file and start using it immediately. It has been tested with `python 3.10`.

```bash
$ git clone https://github.com/koyumeishi/TOML_Snippet_for_VSCode
```

## Usage
```bash
$ python toml_to_json.py -i TOML_FILE -o JSON_FILE
```

If the `-i` option is not specified, the TOML text is read from standard input.  
If the `-o` option is not specified, the converted JSON is output to standard output.  
If the destination JSON file already exists, an error will occur. 
You can overwrite it by specifying the `-f` option.


## Example

`input.toml`
```toml
[for]
scope = "cpp"
prefix = "for"
description = "insert 'for'"
body = """
for(int ${1:i} = 0; ${1:i} < ${2:n}; i++){
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
```

`output.json`
```json
{
  "for": {
    "scope": "cpp",
    "prefix": "for",
    "description": "insert 'for'",
    "body": [
      "for(int ${1:i} = 0; ${1:i} < ${2:n}; i++){",
      "    $2",
      "}"
    ]
  },
  "lambda": {
    "scope": "cpp",
    "prefix": "lambda",
    "description": "insert lambda",
    "body": [
      "auto ${1:lambda_name} = [&]($2){",
      "    $3",
      "};"
    ]
  }
}
```


