# Day 1: Linux User Setup with Non-Interactive Shell

## Task
Create a user named `mark` with a non-interactive shell on `App Server 2`.

## Solution
- Entering `App Server 2`:
  - Go to docs from side menu.
  - Found there along with password:
    - server name: `stapp02`
    - user: `steve`
  - Run `ssh steve@stapp02` and the provided password
- Creating user:
  - To add user: `sudo useradd -m -s /sbin/nologin mark`
  - To check the user: `getent passwd mark`
  - To set password for the created user: `sudo passwd mark`

## Addiotional
- For non-interactive login shell, `/biin/false` or `/usr/sbin/nologin` can be selected in some systems.
- `/etc/passwd` keeps only account info as it's world-readable.
- `/etc/shadow` holds actual password hashes and readable only by root.
### `su` VS `sudo`
`su` (substitute user):
  - **Purpose**: Switch to another user account (default: root).
  - **Authentication**: Ener the password of the user.
  - **Scope**: Changes current shell — you remain that user until you exit.
  - **Typical use**:
    ```bash
    su          # become root (need root's password)
    su john     # become john (need john's password)
    su - john   # become john with full login shell
    ```
    `-` (hyphen) makes `su` start a login shell.
    This means:
    - It loads the user's environment variables (`PATH`, `HOME`, etc.)
    - It changes working directory to user's home directory (like `/home/john`).
    - It runs the shell specified in `/etc/passwd` for the user.

    Without the `-`, you keep your current environment, which can cause odd behavior.

`sudo` (superuser do)
  - **Purpose**: Run a single command as another user (default: root).
  - **Authentication**: Enter your own password (if you’re in sudoers).
  - **Scope**: Only for that command (unless an interactive shell with `-i` or `-s` is requested).
  - **Typical use**:
    ```bash
    sudo whoami               # run as root, prints "root"
    sudo -u john whoami       # run as john, prints "john"
    sudo -i                   # open interactive root shell
    ```