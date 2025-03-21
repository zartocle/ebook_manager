import subprocess
import logging
import platform


def select_folder() -> str:
    """This function will open a dialog that lets the user select a directory, and returns the dir path as a string"""
    oper_system = platform.system()
    if oper_system == "Linux":
        try:
            result = subprocess.run(
                ["kdialog", "--getexistingdirectory", "~"],
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()  # Rimuove spazi vuoti o newline
        except Exception as e:
            logging.exception(f"Error while trying to open the file dialog")
            return {}


def name_without_file_extension(file_name: str):
    """Given a filename as a string, it trims off the file extension if present"""
    import re

    return re.search("^([0-9A-Za-z_-]+).", file_name).group(1)


def confirm_action(folder):
    """Shows a confirmation message prompting the user to make sure their choice is sound"""
    result = subprocess.run(
        [
            "kdialog",
            "--yesno",
            f"Hai selezionato la cartella\n{folder}\nVuoi continuare?",
        ],
        capture_output=True,
    )
    return result.returncode == 0  # 0 means the user clicked on "Yes"
