import colorama
from colorama import Fore

colorama.init(autoreset=True)


def print_prompt(prompt, **kwargs):
    print(Fore.YELLOW + prompt, **kwargs)


def print_option(option, **kwargs):
    print(Fore.CYAN + option, **kwargs)


def print_hints(hints, **kwargs):
    print(Fore.GREEN + hints, **kwargs)


def print_error(error, **kwargs):
    print(Fore.RED + error, **kwargs)
