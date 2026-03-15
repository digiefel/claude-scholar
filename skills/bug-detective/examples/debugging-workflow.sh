#!/bin/bash
#
# Shell script debugging workflow example
# Demonstrates common Bash script errors and debugging methods
#

# ============================================
# Debug settings
# ============================================

# Uncomment to enable debug mode
# set -x   # print each command
# set -e   # exit on error
# set -u   # error on undefined variable
# set -o pipefail  # fail if any pipe component fails

# Or combine them
# set -xeuo pipefail  # strict mode


# ============================================
# Error handling functions
# ============================================

# Error exit function
die() {
    local message="$1"
    local exit_code="${2:-1}"
    echo "Error: $message" >&2
    exit "$exit_code"
}

# Logging function
log() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" >&2
}

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }


# ============================================
# Problem 1: Unquoted variables
# ============================================

# Example: variable not quoted
demo_unquoted_variable() {
    echo "=== Problem 1: Unquoted variables ==="

    local name="John Doe"

    # Wrong: unquoted variable, empty value causes syntax error
    # if [ $name = "John Doe" ]; then
    #     echo "Match"
    # fi

    # Correct: always quote variables
    if [ "$name" = "John Doe" ]; then
        log_info "Variable matched: $name"
    fi
}


# ============================================
# Problem 2: Continuing after command failure
# ============================================

demo_command_failure() {
    echo "=== Problem 2: Continuing after command failure ==="

    # Wrong: continues after cd fails
    # cd /nonexistent_directory
    # rm -rf file.txt  # would delete files in current directory!

    # Correct: check if command succeeded
    cd /tmp || die "Cannot switch to /tmp directory"
    log_info "Successfully changed to directory: $(pwd)"

    cd - > /dev/null || true
}


# ============================================
# Problem 3: Variable scope in loops (pipeline issue)
# ============================================

demo_pipeline_scope() {
    echo "=== Problem 3: Variable scope in pipelines ==="

    local count=0

    # Wrong: pipeline creates a subshell, outer variable is not changed
    # echo -e "1\n2\n3" | while read line; do
    #     count=$((count + 1))
    # done
    # echo "Count: $count"  # prints 0

    # Correct: use redirection
    while read line; do
        count=$((count + 1))
    done < <(echo -e "1\n2\n3")
    log_info "Count result: $count"
}


# ============================================
# Problem 4: Array operations
# ============================================

demo_array_operations() {
    echo "=== Problem 4: Array operations ==="

    local fruits=("apple" "banana" "cherry")

    # Wrong array access
    # echo $fruits[1]  # prints apple[1]

    # Correct array access
    log_info "First element: ${fruits[0]}"
    log_info "Second element: ${fruits[1]}"
    log_info "All elements: ${fruits[@]}"
    log_info "Array length: ${#fruits[@]}"

    # Iterate over array
    for fruit in "${fruits[@]}"; do
        log_info "Fruit: $fruit"
    done
}


# ============================================
# Problem 5: String comparison
# ============================================

demo_string_comparison() {
    echo "=== Problem 5: String comparison ==="

    local name="John"

    # Wrong: using = for numeric comparison
    # if [ $age = 18 ]; then

    # Correct: string comparison
    if [[ "$name" == "John" ]]; then
        log_info "String matched"
    fi

    # Correct: numeric comparison
    local age=18
    if [ "$age" -eq 18 ]; then
        log_info "Number matched"
    fi
}


# ============================================
# Problem 6: Arithmetic operations
# ============================================

demo_arithmetic() {
    echo "=== Problem 6: Arithmetic operations ==="

    local a=10
    local b=5

    # Wrong: using let or $(())
    # result = a + b  # this is a command call

    # Correct arithmetic operations
    local result=$((a + b))
    log_info "Addition: $a + $b = $result"

    result=$((a - b))
    log_info "Subtraction: $a - $b = $result"

    result=$((a * b))
    log_info "Multiplication: $a * $b = $result"

    result=$((a / b))
    log_info "Division: $a / $b = $result"

    # Using let
    let result=a+b
    log_info "let addition: $result"
}


# ============================================
# Argument validation
# ============================================

validate_arguments() {
    echo "=== Argument validation ==="

    # Check argument count
    if [ $# -lt 2 ]; then
        die "Usage: $0 <file> <directory>" 2
    fi

    local file="$1"
    local dir="$2"

    # Check file exists
    if [ ! -f "$file" ]; then
        die "File not found: $file" 3
    fi

    # Check directory exists
    if [ ! -d "$dir" ]; then
        die "Directory not found: $dir" 4
    fi

    log_info "Argument validation passed"
    log_info "File: $file"
    log_info "Directory: $dir"
}


# ============================================
# Using trap for cleanup
# ============================================

demo_trap() {
    echo "=== Using trap for cleanup ==="

    # Set cleanup function
    cleanup() {
        log_info "Performing cleanup..."
        # Cleanup operations go here
    }

    # Catch exit signal
    trap cleanup EXIT

    # Catch error signal
    trap 'log_error "Error occurred, line: $LINENO"' ERR

    # Catch interrupt signal
    trap 'log_warn "Script interrupted"; cleanup; exit 130' INT

    log_info "Performing some operations..."
    # Simulate operations
    sleep 1
}


# ============================================
# Debugging technique examples
# ============================================

demo_debugging() {
    echo "=== Debugging techniques ==="

    # 1. Use echo for debugging
    local value="test"
    echo "[DEBUG] value = $value" >&2

    # 2. Use printf for formatted output
    printf "[DEBUG] Count: %d, Name: %s\n" 42 "John" >&2

    # 3. Check if variable is set
    if [ -z "${unset_var+x}" ]; then
        log_warn "Variable unset_var is not set"
    fi

    # 4. Show call stack
    log_info "Call stack:"
    local i=0
    while caller $i; do
        ((i++))
    done 2>/dev/null || true
}


# ============================================
# File operation error handling
# ============================================

demo_file_operations() {
    echo "=== File operation error handling ==="

    local tmpfile=$(mktemp) || die "Cannot create temporary file"

    # Ensure file is deleted
    trap "rm -f '$tmpfile'" EXIT

    # Write to file
    echo "Test content" > "$tmpfile" || die "Cannot write to file: $tmpfile"

    # Read file
    local content
    content=$(cat "$tmpfile") || die "Cannot read file: $tmpfile"

    log_info "File content: $content"

    # trap handles cleanup automatically
}


# ============================================
# Operation with retry
# ============================================

demo_retry() {
    echo "=== Operation with retry ==="

    local max_attempts=3
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        log_info "Attempt $attempt/$max_attempts..."

        # Simulate potentially failing operation
        if [ $attempt -eq 2 ]; then
            log_info "Success!"
            return 0
        fi

        log_warn "Failed, retrying..."
        ((attempt++))
        sleep 1
    done

    log_error "All attempts failed"
    return 1
}


# ============================================
# Check dependencies
# ============================================

check_dependencies() {
    echo "=== Check dependencies ==="

    local required_commands=("curl" "jq" "git")

    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Missing dependency: $cmd"
            return 1
        fi
        log_info "OK: $cmd is available"
    done

    log_info "All dependencies satisfied"
}


# ============================================
# Main function
# ============================================

main() {
    echo "============================================"
    echo "Shell Script Debugging Examples"
    echo "============================================"

    # Run each example
    demo_unquoted_variable
    echo ""

    demo_command_failure
    echo ""

    demo_pipeline_scope
    echo ""

    demo_array_operations
    echo ""

    demo_string_comparison
    echo ""

    demo_arithmetic
    echo ""

    demo_trap
    echo ""

    demo_debugging
    echo ""

    demo_file_operations
    echo ""

    demo_retry
    echo ""

    check_dependencies
    echo ""

    log_info "All examples completed"
}

# Run main function
main "$@"
