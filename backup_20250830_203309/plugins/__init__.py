# plugins/__init__.py
"""
UwU-cli Plugin System
--------------------
Provides a simple API for creating plugins.
Plugins must define a `register(cli)` function that returns a dict with:
    - on_input: called whenever user types input (before execution)
    - on_command: called when a UwU-cli command is executed
    - on_start: called when UwU-cli starts
    - on_shutdown: called when UwU-cli exits
"""

# --- Example Plugin: Ali Mode ---
def register(cli):
    """
    Registers plugin hooks
    """
    def on_start():
        print("[Ali Mode Plugin] UwU-cli is now watching your vibes...")

    def on_input(user_input):
        # Example: if user types 'ali', respond playfully
        if "ali" in user_input.lower():
            print("[Ali Mode] UwU detected Ali in your message~ rawr x3")
        return user_input  # must return potentially modified input

    def on_command(command, args):
        # Example: special command handling
        if command == "aliroast":
            phrase = args[0] if args else "rawr UwU~"
            print(f"[Ali Mode Roast] {phrase}")
            return True  # True = handled, don't execute default
        return False  # False = pass to default handler

    def on_shutdown():
        print("[Ali Mode Plugin] UwU-cli is signing off. Stay wavy, cutie~")

    return {
        "on_start": on_start,
        "on_input": on_input,
        "on_command": on_command,
        "on_shutdown": on_shutdown
    } 