"""Entry point and UI for banking app."""
# Used GitHub Copilot Autocomplete & Next Edit Suggestions, Google AI Overview for
# minimal coding assistance., and ChatGPT, Gemini, GitHub Copilot, and Google AI Mode
# for help with debugging.

# Note: i was tired and running out of time, so i just quit halfway through on making the code clean and follow linting rules. it works though.

import msvcrt
import time
from collections.abc import Callable

import keyboard
import mysql.connector
from rich import print
from rich.align import Align
from rich.console import Console, Group, RenderableType
from rich.layout import Layout
from rich.live import Live
from rich.padding import Padding
from rich.panel import Panel
from rich.columns import Columns

from database_operations import check_pass, check_balance, create_user, deposit_money, withdraw_money, delete_user

keys_to_check = ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=",
                "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\",
                "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'",
                "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "backspace",
                "up", "down", "enter"]
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
            if key == "8" and keyboard.is_pressed("up"):
                key_states[key] = False
                continue
            if key == "2" and keyboard.is_pressed("down"):
                key_states[key] = False
                continue
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

def draw_screen(
        run_on_enter: Callable[[dict[int, str], int], bool | int | None],
        header_content: RenderableType,
        body_rows: list[str],
        input_rows: list[str],
        select_rows: list[str],
    ) -> bool | int | None:
    """Draw a live screen in terminal."""
    console = Console()
    layout = Layout()
    cursor_pos = 0
    blink_state = True
    layout.split_column(
        Layout(name="header", size=1),
        Layout(name="body"),
    )
    typed_inputs = dict.fromkeys(range(len(input_rows)), "")
    body_height = len(console.render_lines(layout["body"], console.options))
    body_width = console.width
    def draw_screen(cursor_pos: int) -> Panel:
        layout["header"].update(Align.center(header_content, vertical="top"))

        title_padding_dimensions = (
            0,
            0,
            0,
            body_width // 2 - 3 - 5,
        )
        body_renderables = [Padding(row, title_padding_dimensions) for row in body_rows]
        login_block = Group(*body_renderables, "")
        for input_row in input_rows:
            title_padding_dimensions = (
                0,
                0,
                0,
                body_width // 2 - 3 - 5,
            )
            if cursor_pos == input_rows.index(input_row) and blink_state:
                login_block.renderables.append(
                    Padding(f"    {input_row}: {typed_inputs[input_rows.index(input_row)]}█", title_padding_dimensions),
                )
            else:
                login_block.renderables.append(
                    Padding(f"    {input_row}: {typed_inputs[input_rows.index(input_row)]}", title_padding_dimensions),
                )

        for select_row in select_rows:
            title_padding_dimensions = (
                0,
                0,
                0,
                body_width // 2 - 3 - 5,
            )
            if cursor_pos == select_rows.index(select_row) and blink_state:
                login_block.renderables.append(Padding(f"[black on white]{select_row}", title_padding_dimensions))
            else:
                login_block.renderables.append(Padding(f"{select_row}", title_padding_dimensions))
        layout["body"].update(Padding(login_block, (body_height // 2 - 4, 0, 0, 0)))
        return Panel(layout, height=body_height)

    with Live(draw_screen(cursor_pos), refresh_per_second=10) as live:
        count = 0
        while True:
            key = current_key()
            time.sleep(0.01)
            count += 1
            if count % 50 == 0:
                blink_state = not blink_state
            if len(input_rows) != 0:
                if key == "up":
                    cursor_pos = max(0, cursor_pos - 1)
                elif key == "down":
                    cursor_pos = min(len(input_rows) - 1, cursor_pos + 1)
                elif key == "enter":
                    return run_on_enter(typed_inputs, cursor_pos)
                elif key == "backspace":
                    if cursor_pos == 0:
                        typed_inputs[cursor_pos] = typed_inputs[cursor_pos][:-1]
                    else:
                        typed_inputs[cursor_pos] = typed_inputs[cursor_pos][:-1]
                elif cursor_pos == 0:
                    typed_inputs[cursor_pos] += key
                else:
                    typed_inputs[cursor_pos] += key
            elif len(select_rows) != 0:
                if key == "up":
                    cursor_pos = max(0, cursor_pos - 1)
                elif key == "down":
                    cursor_pos = min(len(select_rows) - 1, cursor_pos + 1)
                elif key == "enter":
                    return run_on_enter(typed_inputs, cursor_pos)
            live.update(draw_screen(cursor_pos))
def login() -> list[bool | str] | int | None:
    """Show login screen for banking app."""
    def code_to_run(typed_inputs: dict[int, str], cursor_pos: int) -> list[bool | str] | int | None:
        return [check_pass(db, typed_inputs[0], typed_inputs[1]), typed_inputs[0], typed_inputs[1]]
    return draw_screen(code_to_run,
        "Welcome to SigmaBank!",
        ["Login:"],
        ["User", "Pass"],
        [],
    )

def menu(username: str) -> int | None:
    """Show main menu screen for banking app."""
    def code_to_run(typed_inputs: dict[int, str], cursor_pos: int) -> int:
        return cursor_pos
    options = ["Create Account",
        "Delete Account",
        "Deposit Money",
        "Withdraw Money",
        "Exit",
    ]
    return draw_screen(code_to_run,
        Columns([f"User: {username}", f"Balance: ${check_balance(db, username):.2f}"], expand=True),
        [],
        [],
        options,
    )

def create_account(username: str) -> None | int:
    """Show create account screen."""
    def code_to_run(typed_inputs: dict[int, str], cursor_pos: int) -> bool:
        create_user(db, typed_inputs[0], typed_inputs[1], float(typed_inputs[2]))
        return True
    return draw_screen(code_to_run,
        Columns([f"User: {username}", f"Balance: ${check_balance(db, username):.2f}"], expand=True),
        [],
        ["User", "Pass", "Initial Deposit"],
        [],
    )

def delete_account(username: str) -> None | int:
    """Show delete account screen."""
    def code_to_run(typed_inputs: dict[int, str], cursor_pos: int) -> bool:
        delete_user(db, typed_inputs[0])
        return True
    return draw_screen(code_to_run,
        Columns([f"User: {username}", f"Balance: ${check_balance(db, username):.2f}"], expand=True),
        [],
        ["User"],
        [],
    )

def deposit_money_screen(username: str) -> None | int:
    """Show deposit money screen."""
    def code_to_run(typed_inputs: dict[int, str], cursor_pos: int) -> bool:
        deposit_money(db, typed_inputs[0], float(typed_inputs[1]))
        return True
    return draw_screen(code_to_run,
        Columns([f"User: {username}", f"Balance: ${check_balance(db, username):.2f}"], expand=True),
        [],
        ["User", "Amount"],
        [],
    )

def withdraw_money_screen(username: str) -> None | int:
    """Show withdraw money screen."""
    def code_to_run(typed_inputs: dict[int, str], cursor_pos: int) -> bool:
        withdraw_money(db, typed_inputs[0], float(typed_inputs[1]))
        return True
    return draw_screen(code_to_run,
        Columns([f"User: {username}", f"Balance: ${check_balance(db, username):.2f}"], expand=True),
        [],
        ["User", "Amount"],
        [],
    )

def clear_input() -> None:
    """Clear input buffer."""
    while msvcrt.kbhit():
        msvcrt.getch()

def main() -> None:
    """Run main logic loop for banking app."""
    while True:
        login_result = login()
        if login_result[0]:
            username = login_result[1]
            while True:
                selected_option = menu(username)
                if selected_option == 0:
                    create_account(username)
                elif selected_option == 1:
                    delete_account(username)
                elif selected_option == 2:
                    deposit_money_screen(username)
                elif selected_option == 3:
                    withdraw_money_screen(username)
                elif selected_option == 4:
                    clear_input()
                    exit()
        else:
            print("Wrong username or password. Try again.")
            time.sleep(1)
main()
