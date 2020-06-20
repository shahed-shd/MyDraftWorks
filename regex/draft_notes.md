### According to: Python 3.7, `re` module
---

| Notation | Short description |
|:------------------------------:|------------------------|
| `.` | Matches any character |
| `^` | The start of the string |
| `$` | The end of the string |
| `\` | If not using python raw string, either escapes special characters (permitting to match characters like '*', '?', and so forth), or signals a special sequence |
| | |
| | ***Repetition qualifiers*** |
| `*` | Matches 0 or more repetitions of the preceding RE |
| `+` | Matches 1 or more repetitions of the preceding RE |
| `?` | Matches 0 or 1 repetitions of the preceding RE |
| `*?`, `+?`, `??` | Performs the match in non-greedy or minimal fashion |
| `{m}` | Matches exactly m copies of the previous RE |
| `{m,n}` | Matches from m to n repetitions of the preceding RE. **Omitting** m specifies a lower bound of zero, and **omitting** n specifies an infinite upper bound. |
| `{m,n}?` | Matches from m to n repetitions of the preceding RE in non-greedy or minimal fashion |
| | |
| | ***Special sequences*** |
| `\number` | Matches the contents of the group of the same number, groups are numbered starting from 1, can only be used to match one of the first 99 groups. If the first digit of number is 0, or number is 3 octal digits long, it will not be interpreted as a group match, but as the character with octal value number. |
| `\g<number>`, `\g<name>` | named backreferences |
| `\A` | Matches only at the start of the string |
| `\b` | Matches the empty string, but only at the beginning or end of a word |
| `\B` | Matches the empty string, but only when it is not at the beginning or end of a word |
| `\d` | Matches any decimal digit |
| `\D` | Matches any character which is not a decimal digit |
| `\s`| Matches whitespace characters |
| `\S` | Matches any character which is not a whitespace character |
| `\w` | Matches word characters |
| `\W` | Matches any character which is not a word character |
| `\Z` | Matches only at the end of the string |
| `\a`, `\b`, `\f`, `\n`, `\r`, `\t`, `\u`, `\U`, `\v`, `\x`, `\\` | Most of the standard escapes supported by Python string literals are also accepted by the regular expression parser.  `\b` is used to represent word boundaries, and means “backspace” only inside character classes. `\u` and `\U` escape sequences are only recognized in Unicode patterns, in bytes patterns they are errors |
| | Octal escapes are included in a limited form. If the first digit is a 0, or if there are three octal digits, it is considered an octal escape. Otherwise, it is a group reference |
| | |
| `[]` | ***Character set*** |
| `[amk]` | Characters can be listed individually, e.g. `[amk]` will match 'a', 'm', or 'k'. |
| `[0-9A-Fa-f]` | Indicates range by two characters separated by a hyphen. Hyphen can be **escaped** by `\` or placing the hyphen as the first or last character |
| `[(+*)]` | Special characters lose their special meaning inside sets |
| `\w` or `\S` | Character classes such as \w or \S (defined below) are also accepted inside a set |
| `[^amk]` | Complementing the set |
| `[\]]` | To match a literal `]` inside a set, precede it with a backslash, or place it at the beginning of the set |
| `|` | A\|B, where A and B can be arbitrary REs, creates a regular expression that will match either A or B. An arbitrary number of REs can be separated by the '\|' in this way. To match a literal '\|', use \\\|, or enclose it inside a character class, as in [\|] |
| | |
| | ***Grouping*** |
| `(...)` | Group |
| `(?:...)` | Non-capturing group |
| `(?P<name\>...)` | Named group |
| `(?P=name)` | Backreference to named group |
| `(?#...)` | A comment; the contents of the parentheses are simply ignored |
|| Lookahead assertion, ex: `Isaac (?=Asimov)` will match `Isaac ` only if it’s followed by `Asimov` |
| `(?!...)` | Negative lookahead assertion, ex: `Isaac (?!Asimov)` will match `Isaac ` only if it’s not followed by `Asimov` |
| `(?<=...)` | Positive lookbehind assertion |
| `(?<!...)` | Positive lookbehind assertion |
| `(?(id/name)yes-pattern|no-pattern)` | Will try to match with `yes-pattern` if the group with given `id` or `name` exists, and with `no-pattern` if it doesn’t. `no-pattern` is optional and can be omitted. |


