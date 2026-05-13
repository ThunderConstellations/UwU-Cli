import difflib
from colorama import Fore, Style, init
init()
def show_preview(old_content, new_content, filename="file"):
    if old_content == new_content: return
    print(f"\n{Fore.CYAN}🔍 Proposed changes for {filename}:{Style.RESET_ALL}")
    diff = difflib.unified_diff(old_content.splitlines(), new_content.splitlines(), fromfile=f"a/{filename}", tofile=f"b/{filename}", lineterm='')
    for line in diff:
        if line.startswith('+') and not line.startswith('+++'): print(Fore.GREEN + line + Style.RESET_ALL)
        elif line.startswith('-') and not line.startswith('---'): print(Fore.RED + line + Style.RESET_ALL)
        elif line.startswith('@@'): print(Fore.MAGENTA + line + Style.RESET_ALL)
        else: print(line)
