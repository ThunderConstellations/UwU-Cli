import threading, time
class FXManager:
    def __init__(self, mode="soft"): self.mode = mode
    def run(self, fx_type, func, *args, **kwargs):
        if self.mode == "stealth": return
        threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()
