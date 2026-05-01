"""Entry point and UI for banking app."""
# Used GitHub Copilot Autocomplete & Next Edit Suggestions, Google AI Overview for
# minimal coding assistance., and ChatGPT, Gemini, GitHub Copilot, and Google AI Mode
# for help with debugging.

import msvcrt
import time

import keyboard
import mysql.connector
from rich import print
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.padding import Padding
from rich.panel import Panel

from database_operations import check_pass

keys_to_check = ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=",
                "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\",
                "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'",
                "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "backspace"]
spec_keys_to_check = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+",
                        "{", "}", "|",
                        ":", '"',
                        "<",  ">", "?"]
key_states = dict.fromkeys(spec_keys_to_check + keys_to_check, False)

db = mysql.connector.connect(
    host="192.168.4.112",
    user="root",
    password="password",
    database="bank",
)
def current_key() -> str:
    """Return last typed key."""
    for key, pressed in key_states.items():
        key_upper = None
        if keyboard.is_pressed(key):
            if key in spec_keys_to_check and not keyboard.is_pressed("shift"):
                key_states[key] = False
                continue
            if keyboard.is_pressed("shift"):
                if key.isalpha():
                    key_upper = key.upper()
                elif key not in spec_keys_to_check:
                    key_states[key] = False
                    continue
            if not pressed:
                key_states[key] = True
                if key_upper:
                    return key_upper
                return key
        else:
            key_states[key] = False

    return ""

def login() -> bool:
    """Login screen for banking app."""
    console = Console()
    layout = Layout()
    current_cursor_pos = 0
    blink_state = True
    typed_username = ""
    typed_password = ""
    layout.split_column(
        Layout(name="header", size=1),
        Layout(name="body"),
    )

    body_height = len(console.render_lines(layout["body"], console.options))
    body_width = console.width

    def draw_login_screen(cursor_pos: int) -> Panel:
        layout["header"].update(Align.center("Welcome to SigmaBank!", vertical="top"))

        if blink_state:
            if cursor_pos == 0:
                login_block = Group(
                    "Login:",
                    "",
                    f"    User: {typed_username}█",
                    f"    Pass: {typed_password}",
                )
            else:
                login_block = Group(
                    "Login:",
                    "",
                    f"    User: {typed_username}",
                    f"    Pass: {typed_password}█",
                )
        else:
            login_block = Group(
                "Login:",
                "",
                f"    User: {typed_username}",
                f"    Pass: {typed_password}",
            )
        title_padding_dimensions = (
            body_height // 2 - 4,
            0,
            0,
            body_width // 2 - 3 - 5,
        )
        layout["body"].update(Padding(login_block, title_padding_dimensions))
        return Panel(layout, height=body_height)

    with Live(draw_login_screen(current_cursor_pos), refresh_per_second=10) as live:
        count = 0
        while True:
            key = current_key()
            time.sleep(0.01)
            count += 1
            if count % 50 == 0:
                blink_state = not blink_state
            if keyboard.is_pressed("up"):
                current_cursor_pos = max(0, current_cursor_pos - 1)
            elif keyboard.is_pressed("down"):
                current_cursor_pos = min(1, current_cursor_pos + 1)
            elif keyboard.is_pressed("enter"):
                return check_pass(db, typed_username, typed_password)
            elif key == "backspace":
                if current_cursor_pos == 0:
                    typed_username = typed_username[:-1]
                else:
                    typed_password = typed_password[:-1]
            elif current_cursor_pos == 0:
                typed_username += key
            else:
                typed_password += key
            live.update(draw_login_screen(current_cursor_pos))

def clear_input() -> None:
    """Clear input buffer."""
    while msvcrt.kbhit():
        msvcrt.getch()

def main() -> None:
    """Run main logic loop for banking app."""
    while True:
        if login():
            clear_input()
            print("good")
            break
        clear_input()
        print("bad")
        break
main()
