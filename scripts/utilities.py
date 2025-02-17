"""
Some useful utilities.
"""
import os
import sys
from glob import glob
from pathlib import Path
import pandas as pd
from time import strftime, gmtime

__author__ = "Johnathan Lin <jagonball@g-mail.nsysu.edu.tw>"
__email__ = "jagonball@g-mail.nsysu.edu.tw"


def create_folder(folder_name, path_to_folder, verbose = False):
    """Create folder if not already exist.

    :param folder_name: The folder name.
    :type folder_name: str
    :param path_to_folder: The path to check for the folder.
    :type path_to_folder: str
    :return: The full path to inside the folder.
    :rtype: str
    """
    final_folder = path_to_folder / folder_name
    if verbose:
        print(text_color(f"Checking if folder {folder_name} "
              f"exists in {path_to_folder}...", "gray"))
    if folder_name not in os.listdir(path_to_folder):
        if verbose:
            print(f'## Folder "{text_color(folder_name, "green")}" '
                  f'not found, creating...')
        os.mkdir(final_folder) 
    return final_folder


def search_target_files(file_list, folder_path):
    """Search files matching "file_list" in "folder_path".

    :param file_list: a list of files. (accept regular expression)
    :type file_list: list
    :param folder_path: The folder path to search for.
    :type folder_path: Path or str
    :return: A list of target files.
    :rtype: list
    """
    target_files_list = []
    for name in file_list:
        target_files = str(folder_path / name)
        target_files_list += glob(target_files)
    return target_files_list


def text_color(text, color=None, background=None):
    """Change the text and background color with ANSI escape code.
       The options are: 
       'black', 'red', 'green', 'yellow',
       'blue', 'magenta', 'cyan', 'white',
       'gray', 'bright_red', 'bright_green', 'bright_yellow',
       'bright_blue', 'bright_magenta', 'bright_cyan', 'bright_white'

    :param text: The input text.
    :type text: str
    :param color: The text color, defaults to None
    :type color: str, optional
    :param background: The background color, defaults to None
    :type background: str, optional
    :return: The color modified text
    :rtype: str
    """
    options = ['black', 'red', 'green', 'yellow',
               'blue', 'magenta', 'cyan', 'white',
               'gray', 'bright_red', 'bright_green', 'bright_yellow',
               'bright_blue', 'bright_magenta', 'bright_cyan', 'bright_white']
    fg_code = ['30', '31', '32', '33', '34', '35', '36', '37',
               '90', '91', '92', '93', '94', '95', '96', '97']
    bg_code = ['40', '41', '42', '43', '44', '45', '46', '47',
               '100', '101', '102', '103', '104', '105', '106', '107']
    if color in options:
        color = fg_code[options.index(color)]
    else:
        color = '39' # Default.
    if background in options:
        background = bg_code[options.index(background)]
    else:
        background = '49' # Default.
    # print(f'Color = {color}; Background = {background}')
    text = f'\033[{color}m\033[{background}m{text}\033[00m'
    return text
 

# Reference: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# black   = "\033[30m"
# red     = "\033[31m"
# green   = "\033[32m"
# yellow  = "\033[33m"
# blue 34
# magenta 35
# cyan 36
# white   = "\033[37m"
# nocolor = "\033[0m"


###====== Check variables ======###
def check_odd_even(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"


def check_type(var, clas):
    """
    clas can be str, list, multiple like (int, float)
    returns True/False
    """
    return isinstance(var, clas)


###====== Check config settings ======###
def check_input(input, options, para, section, config, exit=True):
    # Check inputs: input should be in options.
    if input not in options:
        error_message = f'Invalid parameter, the options are: '
        check_message = f'"{para}" in "{section}" section'
        error_config(error_message, options, check_message, config, exit)
    else:
        return input
    

def check_required_keys(input, keys, para, section, config, exit=True):
    # Check keys: input must contain all "keys".
    if not set(keys).issubset(set(input.keys())):
        error_message = f'Missing parameter, the requirements are: '
        check_message = f'"{para}" in "{section}" section'
        error_config(error_message, keys, check_message, config, exit)
        

def check_set_delimiter(para_str,
                        parent_para_str,
                        data,
                        options,
                        config,
                        default='\t'):
    if para_str in data[parent_para_str]:
        delimiter = check_input(data[parent_para_str][para_str],
                                options,
                                f'"{para_str}"',
                                f'"{parent_para_str}"',
                                config)
        delimiter = options[delimiter]
    else:  # Set to default
        delimiter = default
    return delimiter

def check_set_default(variable,
                      default,
                      para_name,
                      parent_para):
    variable = default
    if para_name in parent_para:
        variable = parent_para[para_name]
    return variable


###====== DataFrame management ======###
def read_df(file_path,
            sheet_name=0,
            delimiter='\t',
            header=0,
            index_col=None,
            usecols=None):
    """Read data matrix with Pandas, accept csv, tsv, or excel.

    :param file_path: Path to the file
    :type file_path: str or Path
    :param sheet_name: Strings are used for sheet names. Integers are used in zero-indexed sheet positions, defaults to 0
    :type sheet_name: str, int, optional
    :param delimiter: Character or regex pattern to treat as the delimiter, defaults to '\t'
    :type delimiter: str, optional
    :param header: Row number(s) containing column labels and marking the start of the data (zero-indexed), defaults to 0
    :type header: int, Sequence of int, optional
    :param index_col: Column(s) to use as row label(s), denoted either by column labels or column indices., defaults to None
    :type index_col: Hashable, Sequence of Hashable or False, optional
    :param usecols: Subset of columns to select, denoted either by column labels or column indices, defaults to None
    :type usecols: Sequence of Hashable or Callable, optional
    :return: The DataFrame
    :rtype: DataFrame
    """
    file_path = Path(file_path)
    # Check suffix, read file accordingly.
    excel = ['.xls', '.xlsx', '.xlsm',
             '.xlsb', '.odf', '.ods', '.odt']
    if file_path.suffix in excel:
        df = pd.read_excel(file_path,
                           sheet_name=sheet_name,
                           header=header,
                           index_col=index_col,
                           usecols=usecols)
    else:
        df = pd.read_table(file_path,
                           sep=delimiter,
                           header=header,
                           index_col=index_col,
                           usecols=usecols)
    return df


def df_cat_filter(df, col, condition, reset_index=True):
    """Filter category column with values.

    :param df: Input DataFrame
    :type df: DataFrame
    :param col: The category column name
    :type col: str
    :param condition: Target value(s) to keep
    :type condition: str, list
    :param reset_index: To reset index, defaults to True
    :type reset_index: bool, optional
    :return: The filtered DataFrame
    :rtype: DataFrame
    """
    if isinstance(condition, str):
        if reset_index:
            df_filtered = df[df[col] == condition].copy().reset_index(drop=True)
        else:
            df_filtered = df[df[col] == condition].copy()
    elif isinstance(condition, list):
        if reset_index:
            df_filtered = df[df[col].isin(condition)].copy().reset_index(drop=True)
        else:
            df_filtered = df[df[col].isin(condition)].copy()
    else:
        print(f'{text_color("Error", "bright red")}: '
              f'the condition must be '
              f'{text_color("string", "green")} or '
              f'{text_color("list", "green")}, '
              f'the provided input is: {text_color(condition, "red")}')
        sys.exit()
    return df_filtered


###====== Error messages ======###
def error_config(message, message_highlight, check_highlight, config_file, exit=True):
    """Print error message for config error and whether to exit program or not.

    :param message: The error message.
    :type message: str
    :param check_highlight: Highlited text. ex: "col in go section"
    :type check_highlight: str
    :param config_file: Path to config file.
    :type config_file: str or Path
    :param exit: To exit the program or not, defaults to True
    :type exit: bool, optional
    """
    print(f"{text_color('Error', 'bright_red')}: "
          f"{message}"
          f"{text_color(message_highlight, 'cyan')}. Please check "
          f"{text_color(check_highlight, 'bright_blue')} of the "
          f"{text_color(config_file, 'bright_green')}.")
    if exit:
        sys.exit()


###====== Utilities ======###
### Display time.
def show_time(time_used, text="Time taken:", color="bright_cyan"):
    """Display time in terminal.

    :param time_used: Time in seconds.
    :type time_used: float
    :param text: Text to display, defaults to "Time taken:"
    :type text: str, optional
    :param color: Display color, defaults to "bright_cyan"
    :type color: str, optional, options are: 
        ['black', 'red', 'green', 'yellow',
        'blue', 'magenta', 'cyan', 'white',
        'gray', 'bright_red', 'bright_green', 'bright_yellow',
        'bright_blue', 'bright_magenta', 'bright_cyan', 'bright_white']
    """
    time_format = strftime("%H:%M:%S", gmtime(time_used))
    if time_used >= 86400:
        days = time_used // 86400
        time_used %= 86400
        show_time = text_color(f"{days} day(s) {time_format}",
                               color)
    else:
        show_time = text_color(f"{time_format}", color)

    print(text_color(f"{text} {show_time}"))

## Not a function for calling.
def time(): # The function block is only for the code not to run.
    from time import time, sleep, strftime, gmtime, ctime

    time_start = time()
    print(f"Program start time: {ctime(time_start)}")
    # sleep(5)
    time_end = time()
    days = None
    time_used = time_end - time_start
    time_format = strftime("%H:%M:%S", gmtime(time_used))
    if time_used >= 86400:
        days = time_used // 86400
        time_used %= 86400
        show_time = text_color(f"{days} day(s) {time_format}",
                               'bright_cyan')
    else:
        show_time = text_color(f"{time_format}", 'bright_cyan')

    print(text_color(f"Total time taken: {show_time}"))