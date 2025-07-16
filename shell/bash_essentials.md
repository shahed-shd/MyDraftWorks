Bash Essentials (Concisely)

## What & Why
- **What:** Bourne Again Shell, a command language and Unix shell.
- **Why:** Powerful for automation, scripting, and system tasks etc.
- **Where used:** CI/CD, system admin tasks, deployment scripts, pipelines, quick data parsing etc.
  
## Variables & Strings
- Untyped strings
- Everything is a string unless used in arithmetic context
- Always quote like `"$var"`, except in arithmetic or array indexing
  - Prevents Word Splitting
  </br>
  ```bash
    filename="my file.txt"
    rm $filename     # ❌ Tries to delete `my` and `file.txt` separately
    rm "$filename"   # ✅ Correct: deletes "my file.txt"

  ```
  - Preserves Empty Strings
  </br>
  ```bash
    input=""
    [ $input == "yes" ]   # ❌ Error: unary operator expected
    [ "$input" == "yes" ] # ✅ No error
  ```
  - Handles special characters safely, like `*`, `&`, `!`
  </br>
  ```bash
    pattern="*.txt"
    ls $pattern     # ❌ Expands too early or fails
    ls "$pattern"   # ✅ Passed as literal

  ```
  - Array safety
  ```bash
  arr=("one word" "two")
  ```

| Type         | Keyword                   | Description                  |
| ------------ | ------------------------- | ---------------------------- |
| Integer      | `declare -i`              | Treat value as integer       |
| Array        | `declare -a`              | Indexed array                |
| Assoc. Array | `declare -A`              | Key-value pair array         |
| Readonly     | `readonly` / `declare -r` | Cannot be changed            |
| Exported     | `export` / `declare -x`   | Available to child processes |


```bash
name="Alice"         # No space around =
echo "Hi, $name"     # Interpolation
echo "Hi, ${name}"   # Safe style
```

```bash
declare name="Alice" # explicit declare
```
```bash
declare v=5
v=$(( $v + 3 ))
echo "Value: $v" # Value: 8
```
```bash
declare -i v=5
v=$v+3
echo "Value: $v" # Output: `Value: 8`
                 # Without -i switch, output will be `Value: 5+3`
```

## Arrays
```bash
arr=("a" "b" "c")

echo "Value at index 1: ${arr[1]}"
echo "Length: ${#arr[@]}"    
echo "All values: ${arr[@]}" # Expands to separate words
echo "All values: ${arr[*]}" # Expands to single word

arr[3]="d"      # New value at new index
echo "New value inserted: ${arr[@]}"

arr[2]="ccc"    # Modify value
echo "After value modification at index 2: ${arr[@]}"
```
With `-a` flag:
```bash
declare -a arr  # Declared
declare -a arr=("a", "b", "c") # Declared and initialized
```

## Conditionals
Basic `if` syntax
```bash
if [ condition ]; then
  # commands
fi
```
Alternate forms
```bash
if [[ condition ]]; then   # Safer for strings, supports pattern matching
if test condition; then    # Equivalent to [ ]
```
Example:
```bash
if [ "$x" -gt 10 ]; then
  echo "Big"
elif [ "$x" -gt 5 ]; then
  echo "Medium"
else
  echo "Small"
fi
```
Compound Conditions
```bash
# Using [[ ... ]]
if [[ $x -gt 5 && $x -lt 15 ]]; then
  echo "x is between 5 and 15"
fi

# Using -a and -o, but less portable
if [ $x -gt 5 -a $x -lt 15 ]; then
  echo "x is in range"
fi
```
### Common Conditions
| Condition       | Meaning                          |
| --------------- | -------------------------------- |
| `-z "$x"`       | is empty string                  |
| `-n "$x"`       | is non-empty string              |
| `"$a" == "$b"`  | strings are equal                |
| `"$a" != "$b"`  | strings not equal                |
| `"$a" < "$b"`  | string comparison                |
| `"$a" -eq "$b"` | numeric equality                 |
| `"$a" -gt "$b"` | greater than                     |
| `-f file`       | is regular file                  |
| `-d dir`        | is directory                     |
| `-e file`       | exists                           |
| `-r/-w/-x file` | readable / writable / executable |

### Comparision `[ ... ]` VS `[[ ... ]]` VS `test`

`[ ... ]` (Single Bracket)
  - POSIX-compliant (works in sh, dash, and bash)
  - Actually a command: `/usr/bin/[`
  - Requires careful quoting and limited in features
  ```bash
  [ "$x" = "abc" ]
  [ "$a" -gt 5 ]
  ```

#### `[[ ... ]]` (Double Bracket)
  - Bash-only (not POSIX), introduced for improved safety and usability
  - Safer and more powerful:
    - No word splitting
    - Supports `&&`, `||`, pattern matching (`== *.txt`)
    - Allows regex matching (`=~`)
    - Less need to quote variables
    ```bash
    [[ $x == abc ]]
    [[ $file == *.txt ]]   # pattern match
    [[ $x =~ ^[0-9]+$ ]]   # regex match
    ```

#### `test` Command
- Identical to `[ ... ]`
- Fully POSIX
- Rarely used directly, but equivalent
```bash
test "$x" = "abc" # Same as [ "$x" = "abc" ]
```
Dangerous Example
```bash
x=""
[ $x = "abc" ]   # ❌ Error: unary operator expected
[[ $x == "abc" ]] # ✅ No error
```
### Key Differences
| Feature                          | `[ ... ]` | `[[ ... ]]` | `test ...` |     |     |
| -------------------------------- | --------- | ----------- | ---------- | --- | --- |
| POSIX-compatible                 | ✅         | ❌           | ✅          |     |     |
| Pattern matching                 | ❌         | ✅           | ❌          |     |     |
| Regex support                    | ❌         | ✅           | ❌          |     |     |
| Logical operators (`&&`, `\|\|`) | ❌         | ✅           | ❌          |
| Safer with unquoted vars         | ❌         | ✅           | ❌          |     |     |
| Word splitting risk              | ✅         | ❌           | ✅          |     |     |

### Recommended Practice
- Use `[[ ... ]]` for all Bash scripts.
- Use `[ ... ]` or `test` only when writing POSIX-compliant scripts.

## Loops
`for` loop list-based
```bash
for item in apple banana cherry; do
  echo "$item"
done
```
From a command substitution
```bash
# Use with care, splits on spaces
for user in $(cat users.txt); do
  echo "$user"
done

# Safer
while IFS= read -r user; do
  echo "$user"
done < users.txt
```
C-style `for` loop
```bash
for ((i = 0; i < 5; i++)); do
    echo "value : $i"
done
```
Range
```bash
# 1 to 10
for i in {1..10}; do
    echo $i
done

# 1 to 10 with interval 2
for i in {1..10..2}; do
    echo $i
done
```
Loop over files
```bash
for f in *.txt; do
  echo "Found file: $f"
done
```
Loop over command output
```bash
for line in $(ls); do
  echo "$line"
done

# This breaks with spaces! Use `while read` instead

ls | while IFS= read -r line; do
  echo "$line"
done
```
`while` loop
```bash
count=0
while [ $count -lt 3 ]; do
    echo "count : $count"
    ((count++))
done
```
```bash
while read line; do
    echo "$line"
done < file.txt
```
`until` Loop (Runs **until** the condition becomes true)
```bash
x=1
until [ $x -gt 3 ]; do
    echo "x: $x"
    ((x++))
done
```
Loop Control
- `break` - exit the loop
- `continue` - skip to next iteration
```bash
for i in {1..10}; do
    if [ $i -eq 3 ]; then
        continue
    fi

    if [ $i -eq 5 ]; then
        break
    fi

    echo "i: $i"
done
```
## Functions
### Basic syntax
```bash
function greet() {
    echo "Hello";
}

# Alternatiavely, `function` keyword is optional
# greet() {
#     echo "Hello";
# }

# Invoking the function
greet
```
### Passing arguments
Arguments are passed like script arguments:
- `$1`, `$2`, ... – Positional arguments
- `$@` – All arguments
- `$#` - Total number of arguments
```bash
greet() {
  echo "Hello, $1!"
}

greet "Alice"  # → Hello, Alice!
```
```bash
sum() {
  echo "$(($1 + $2))"
}

sum 5 7  # → 12
```
```bash
function print_all() {
    echo "Total args: $#"
    echo "All args: $@"

    for arg in "$@"; do
        echo "$arg"
    done
}

print_all one two three
```

### Returning a value
Functions can only return integers (0–255), typically used as status codes
```bash
is_even() {
    if [ $(($1 % 2)) -eq 0 ]; then
        return 0
    else
        return 1
    fi

    # Alternatively
    #   (( $1 % 2 == 0 ))
    #   return $?
}

is_even 45 && echo "Even" || echo "Odd"
```
Use `echo` for non-integer output
```bash
get_hostname() {
    echo "$(hostname)"
}

host=$(get_hostname)
echo "Host: $host"
```
### Local Variables
Use `local` to avoid global pollution
```bash
name="Alice"

function foo() {
  local name="Bob"
  echo "Inner: $name"
}

foo

echo "Outer: $name"
```
### Recursion
```bash
function factorial() {
    local n=$1

    if (( n <= 1 )); then
        echo 1
    else
        echo $(( n * $( factorial $((n - 1)) ) ))
    fi
}

factorial 5 # → 120
```
### Best practices
- Always use `local` in functions unless you want globals.
- Use `"$@"` when passing all args to another command/function.
- Use `return` only for status codes, `echo` for values.
## Reading input
```bash
read -p "Enter name: " name
echo $name
```
```bash
read name # promptless
```
## File descriptor
- A **file descriptor** is a number that refers to an open file or stream.
- Standard FDs:

  | FD  | Name     | Purpose                         |
  | --- | -------- | ------------------------------- |
  | 0   | `stdin`  | Standard input (keyboard, pipe) |
  | 1   | `stdout` | Standard output (screen)        |
  | 2   | `stderr` | Standard error (errors)         |

- Redirections:

| Action                      | Example                                     |
| --------------------------- | ------------------------------------------- |
| Redirect stdout             | `command 1> out.txt` Or `command > out.txt` |
| Redirect stderr             | `command 2> err.txt`                        |
| Redirect both               | `command > all.txt 2>&1`                    |
| Append instead of overwrite | `command >> out.txt`                        |
| Discard stdout              | `command > /dev/null`                       |
| discard stderr              | `command 2> /dev/null`                      |
| Discard output (both)       | `command &> /dev/null`                      |
| Custom FD write             | `exec 3> log.txt; echo "hi" >&3`            |
| Custom FD read              | `exec 4< input.txt; read var <&4`           |

- Custom FD can be created (3–9+)
  ```bash
  exec 3> custom.log        # open FD 3 for writing
  echo "Custom log" >&3     # write via FD 3
  exec 3>&-                 # close FD 3
  ```
- Custom FD for readng
  ```bash
  exec 4< input.txt        # open file for reading
  read line <&4
  echo "Read: $line"
  exec 4<&-                # close FD
  ```
- Swapping stdout and stderr
  ```bash
  # Saves stdout to FD 3
  # Redirects stdout to stderr
  # Redirects stderr to saved stdout
  command 3>&1 1>&2 2>&3
  ```
- In Linux and Unix-like systems, `/dev` is a special directory that contains device files — these represent hardware devices, system resources, and virtual input/output streams.

  | File           | Purpose                                                                                                                                    | Use Case                                                                                                                            |
  | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
  | `/dev/null`    | The *Black Hole*.</br>A special device that discards all data written to it.<br/>Reading from it returns EOF (empty).                      | `command > /dev/null # Suppress stdout` </br> `command 2> /dev/null # Suppress stderr` </br> `command &> /dev/null # Suppress both` |
  | `/dev/stdin`   | Std input. Alternative to using `<&0`                                                                                                      | `cat < /dev/stdin`                                                                                                                  |
  | `/dev/stdout`  | Std output. Alternative to using `>&1`                                                                                                     | `echo "hi" > /dev/stdout`                                                                                                           |
  | `/dev/stderr`  | Std error. Alternative to using `>&2`                                                                                                      | `echo "err" > /dev/stderr`                                                                                                          |
  | `/dev/tty`     | User’s terminal                                                                                                                            | `read -p "input: " line < /dev/tty`                                                                                                 |
  | `/dev/zero`    | Infinite zeros.</br> Outputs an infinite stream of **null bytes** (0x00).</br>Useful for creating large files or initializing binary data. | `head -c 1024 < /dev/zero > file.bin`                                                                                               |
  | `/dev/random`  | Generate random data.</br>High-entropy (slow, blocks if not enough entropy)                                                                | `head -c 16 /dev/random`                                                                                                            | base64` | base64` |
  | `/dev/urandom` | Generate random data.</br>Faster, uses PRNG (pseudo-random)                                                                                | `head -c 16 /dev/urandom`                                                                                                           | base64` |

## Error Handling

- No exception throwing like other languages, command status codes (called exit codes) are checked.
- Every command returns an exit code
  - `0` indicates success
  - `>0` inidcates failure
- `$?` to check last command's exit code
  ```bash
  ls /not/exist
  echo $?  # → non-zero indicates error
  ```
### Using `&&` and `||`
Simple inline handling:
```bash
mkdir mydir && echo "Created" || echo "Failed"
```

### Using `if`
```bash
if cp file1.txt /tmp/; then
  echo "Copied successfully"
else
  echo "Copy failed"
fi
```

### Custom Error Function
```bash
function die() {
  echo "Error: $*" >&2
  exit 1
}

[ -f config.env ] || die "Missing config file"
```

## Command Substitution
```bash
now=$(date)
echo "Time: $now"
```
```bash
echo "Time: `date`" # legacy style
```

## File Reading
```bash
while IFS= read -r line; do echo $line; done < file.txt
```

```bash
cat file.txt | while read line; do echo $line; done
```

## Args & Scripts
```bash
echo "Script: $0, First: $1, Total: $#"
```
```bash
for arg in "$@"; do
    echo $arg
done
```

## Here Document
```bash
cat <<EOF
Multi-line text
EOF

```

## Redirection & Pipes
```bash
grep "fail" log.txt | sort | uniq > out.txt
```
```bash
awk '/fail/' log.txt | sort | uniq
````

## Sample Script (Rename files)
```bash
i=1
for f in *.jpg; do
    mv "$f" "img_$i.jpg";
    ((i++))
done
```
```bash
find . -name '*.jpg' | nl | while read n f; do mv "$f" "img_$n.jpg"; done
```

## `set` built-in
- Changes the shell's behavior **at runtime**
- `set -<option>` to enable an option
- `set +<option>` to disable it
- Some useful `set` options

| Option        | Full name  | Description                                                              |
| ------------- | ---------- | ------------------------------------------------------------------------ |
| `-e`          | `errexit`  | Exit immediately on any non-zero (failing) command                       |
| `-u`          | `nounset`  | Treat use of **unset** variables as an error                             |
| `-o pipefail` | `pipefail` | Causes a pipeline to fail if **any** command in the pipe fails           |
| `-x`          | `xtrace`   | Print each command **before executing it** (debugging)                   |
| `-v`          | `verbose`  | Print each line of the script as it is **read** (more verbose than `-x`) |
| `-n`          | `noexec`   | Parse the script but don’t execute (syntax checking)                     |

### `set -e` (exit on error)
Without `-e`, bash continues even after a failure.
```bash
set -e
cp file.txt /tmp/      # If this fails, script exits
echo "Will not run if cp fails"
```

### `set -u` (Unset variables)
Helps catch typos and missing variables.
```bash
set -u
echo "$undefined_var"  # Script exits with error
```

### `set -o pipefail` (Pipeline safety)
```bash
set -o pipefail
grep "foo" file.txt | sort | head  # Will fail if grep fails
```
Without it, only the last command (`head`) affects the pipeline exit code.

### `set -x` (Debug mode)
```bash
set -x
echo "Debugging..."
set +x
```
Useful for tracing script execution step-by-step.

### `set -n` (No-execute, dry run)
```bash
set -n
echo "This won't run"  # ✔️ Syntax is checked, not executed
```
Great for syntax validation.

## Subshell and Grouping
- A subshell is a child process created by the current shell to execute commands in isolation.
- In Bash, subshells run in separate environments, so variable changes inside them do not affect the parent shell.
- Subshell syntax: `( commands)`. Everything inside the parentheses runs in a new process.
  ```bash
  ( echo "This is a subshell" )
  ```
- Grouping means command group. All commands inside `{}` run in the current shell.
- Grouping syntax: `{ command1; command2; }`
  - Semicolon `;` or newline is required between commands.
  - Must have a space after `{` and before `}`.
- Subshells vs. Grouping `{}`
  | Syntax      | Subshell? | Effect on parent?    |
  | ----------- | --------- | -------------------- |
  | `( ... )`   | Yes       | No effect outside    |
  | `{ ... ; }` | No        | Affects parent shell |
  Example:
  ```bash
  var="outside"

  ( var="inside" )
  echo "$var"  # → outside

  { var="changed"; }
  echo "$var"  # → changed
  ```
- Since subshells spawn new processes, they’re heavier than `{}` blocks — use them only when needed or to avoid polluting parent shell.
- Common uses of subshells
  
  Isolate side effects:
  ```bash
  ( cd /tmp && run_temp_task )
  # Back in original directory
  ```
  Capture output:
  ```bash
  result=$( (echo one; echo two) )
  echo "$result"  # → one two
  ```

  Run background  tasks:
  ```bash
  ( sleep 5; echo "Done" ) &
  ```

  Subshell for redirection:
  ```bash
  (
    echo "Log started"
    echo "Time: $(date)"
  ) > script.log    # Only the content of the subshell is redirected.
  ```

  Group for redirections:
  ```bash
  {
    echo "Header"
    echo "Content"
    echo "Footer"
  } > output.txt    # All three lines are redirected to the same file.
                    # Without {}, only one command gets redirected.
  ```

  Conditional Execution on Group Result:
  ```bash
  # Entire block is evaluated together.
  { cp file.txt /backup/ && echo "Success"; } || echo "Failed"
  ```

## Misc
- Use `#!/usr/bin/env` bash for portability
- Manual logging
  ```bash
  function log() {
    echo "[INFO][$(basename "$0"):$LINENO] $*";
  }

  function log_error() {
    echo "[ERROR][$(basename "$0"):$LINENO] $*" >&2
  }

  log "Starting task..."
  log_error "Failed to connect to server"
  ```
  
### `IFS` (Internal Field Separator)
Controls how Bash splits strings into words during:
- Variable expansion (unquoted variables)
- read command
- for loops over unquoted expansions

Default value `IFS=$' \t\n'` (space, tab, newline)

Custom value for reading CSV-like or custom-delimited files
```bash
IFS=',' read -r name age <<< "Alice,30"
echo "$name is $age years old"
```
Readng entire line safely
```bash
while IFS= read -r line; do
  echo "Line: $line"
done < file.txt
```
- `IFS=` disables field splitting

- `-r` (raw) prevents backslash escapes
  
Temporary IFS (local scope). To change IFS just for one line
```bash
IFS=':' read -r user pass uid <<< "root:x:0"
```
Or, save/restore
```bash
OLDIFS=$IFS
IFS=','

# operations...

IFS=$OLDIFS
```

