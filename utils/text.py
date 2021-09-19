import colorama
import random
from typing import Union


def print_title(text: str):
    print(f'{colorama.Fore.YELLOW}{text}{colorama.Fore.RESET}')


def print_action(text: str):
    print(f'{colorama.Fore.CYAN}Execute command: {colorama.Fore.RESET}'
          f'{colorama.Fore.GREEN}{text}{colorama.Fore.RESET}')


def print_output(text: Union[str, list], prefix: str = None):
    if prefix:
        prefix = f'{prefix}: '
    else:
        prefix = ''
    p = lambda txt: print(f'{prefix}{colorama.Fore.MAGENTA}{txt.strip()}{colorama.Fore.RESET}')
    if isinstance(text, str):
        p(text)
    if isinstance(text, list):
        for t in text:
            p(t)


def print_magic(text: str):
    colors = [
        colorama.Fore.CYAN,
        colorama.Fore.GREEN,
        colorama.Fore.BLUE,
        colorama.Fore.MAGENTA,
        colorama.Fore.WHITE,
        colorama.Fore.RED
    ]
    for i, t in enumerate(text):
        end = '' if i + 1 != len(text) else '\n'
        print(f'{random.choice(colors)}{t}{colorama.Fore.RESET}', end=end)


