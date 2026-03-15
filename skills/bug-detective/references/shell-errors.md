# Bash/Zsh Script Error Reference

## Common Error Types

### 1. Command Not Found

**Characteristic**: bash: command: command not found

**Common causes**:
- Misspelled command
- Command not installed
- Incorrect PATH environment variable
- Wrong script shebang

**Example**:
```bash
# Spelling error
pyhon script.py  # command not found

# Correct spelling
python script.py

# PATH issue
/usr/local/bin/mycommand  # if PATH does not include /usr/local/bin

# Use full path or add to PATH
export PATH="/usr/local/bin:$PATH"
mycommand
```

### 2. Syntax Error

**Characteristic**: syntax error near unexpected token

**Common causes**:
- Missing then/fi/done/esac
- Mismatched brackets
- Missing spaces around operators

**Example**:
```bash
# Missing then
if [ 1 -eq 1 ]
echo "yes"  # syntax error

# Correct
if [ 1 -eq 1 ]; then
    echo "yes"
fi
```

### 3. Permission Denied

**Characteristic**: bash: ./script.sh: Permission denied

**Solution**:
```bash
# Add execute permission
chmod +x script.sh

# Or run with bash
bash script.sh
```

## Debugging Techniques

### 1. Use set -x for execution tracing

```bash
#!/bin/bash
set -x  # enable command tracing

name="John"
echo "Hello $name"

# Output:
# + name=John
# + echo 'Hello John'
# Hello John
```

### 2. Use set -e to exit on error

```bash
#!/bin/bash
set -e  # exit if any command fails

cd /nonexistent  # script exits here
echo "This won't run"
```

### 3. Use set -u to detect undefined variables

```bash
#!/bin/bash
set -u  # error on undefined variable

echo $undefined_var  # error and exit
```

### 4. Combine debug options

```bash
#!/bin/bash
set -xeuo pipefail  # strict mode

# -x: print each command
# -e: exit on error
# -u: error on undefined variable
# -o pipefail: fail if any pipe component fails
```

### 5. Use trap to catch errors

```bash
#!/bin/bash
# Execute cleanup on script exit
trap 'echo "Script exited with code $?"' EXIT

# Execute on error
trap 'echo "Error on line $LINENO"' ERR

# Execute on interrupt
trap 'echo "Interrupted"; cleanup' INT
```

## Error Handling Patterns

### 1. Check command exit code

```bash
# Check if last command succeeded
if [ $? -eq 0 ]; then
    echo "Success"
else
    echo "Failed"
fi

# Or use ||
command || { echo "Failed"; exit 1; }

# Or use &&
command && echo "Success" || echo "Failed"
```

### 2. Use functions to encapsulate error handling

```bash
# Define error handler function
die() {
    local message=$1
    echo "Error: $message" >&2
    exit 1
}

# Usage
[ -f "$file" ] || die "File not found: $file"
```

### 3. Validate input arguments

```bash
#!/bin/bash
# Check argument count
[ $# -ge 1 ] || die "Usage: $0 <arg1> [arg2]"

# Check file exists
[ -f "$1" ] || die "File not found: $1"

# Check directory exists
[ -d "$2" ] || die "Directory not found: $2"
```

## Best Practices

### 1. Always use shebang

```bash
#!/bin/bash
# or
#!/usr/bin/env bash
```

### 2. Use set -euo pipefail

```bash
#!/bin/bash
set -euo pipefail
```

### 3. Quote all variables

```bash
# Unless you are sure the variable contains no spaces or globs
echo "$var"
```

### 4. Use [[ ]] instead of [ ]

```bash
# [[ is more powerful and safer
if [[ $name == "John" ]]; then
if [[ -f $file && $size -gt 100 ]]; then
```

### 5. Use $(command) instead of backticks

```bash
# $() is more readable and nestable
result=$(command1 $(command2))
```

### 6. Use functions to organize code

```bash
my_function() {
    local arg1=$1
    local arg2=$2
    # function body
}

my_function "value1" "value2"
```

## ShellCheck Static Analysis

ShellCheck is a static analysis tool for shell scripts:

```bash
# Install ShellCheck
brew install shellcheck  # macOS
apt install shellcheck   # Ubuntu

# Usage
shellcheck script.sh
```
