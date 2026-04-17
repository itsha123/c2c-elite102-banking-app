# Used GitHub Copilot Autocomplete & Next Edit Suggestions, and Google AI Overview for minimal coding assistance.
from rich import print
from rich.panel import Panel
from rich.align import Align
from rich.console import Group
from rich.prompt import Prompt

def login():
    username = ""
    login_screen_group = Group(
        Prompt.ask("Username")
    )
    print(username)
    print(Panel(login_screen_group))

def main():
    print(Align(Panel("Welcome to SigmaBank!"), align="center"))
    print("Login: ", end="")
    if not login():
        return
main()