import colorama
from colorama import Fore

colorama.init(autoreset=True)


def print_prompt(prompt, **kwargs):
    """
    Prints text in yellow.

    Parameters
    -----------
    prompt: str
        The text to be printed
    """
    print(Fore.YELLOW + prompt, **kwargs)


def print_option(option, **kwargs):
    """
    Prints text in cyan.

    Parameters
    -----------
    prompt: str
        The text to be printed
    """
    print(Fore.CYAN + option, **kwargs)


def print_hints(hints, **kwargs):
    """
    Prints text in green.

    Parameters
    -----------
    prompt: str
        The text to be printed
    """
    print(Fore.GREEN + hints, **kwargs)


def print_error(error, **kwargs):
    """
    Prints text in red.

    Parameters
    -----------
    prompt: str
        The text to be printed
    """
    print(Fore.RED + error, **kwargs)
