import os
from pathlib import Path
from typing import Dict, List

class ContextScanner:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).absolute()
        self.manifest_files = ["package.json", "setup.py", "pyproject.toml", "requirements.txt", "README.md", "TASKS.md"]

    def get_context_string(self) -> str:
        summary = "--- LORD LEVEL ENGINEER PROJECT CONTEXT ---\n"
        summary += f"Current Root: {self.root}\n\n"

        summary += "Top Level Files:\n"
        try:
            files = [f.name for f in self.root.iterdir() if f.is_file() and not f.name.startswith('.')]
            summary += ", ".join(files[:20]) + "\n\n"
        except: pass

        summary += "Manifest Summaries:\n"
        for m in self.manifest_files:
            p = self.root / m
            if p.exists():
                try:
                    with open(p, 'r') as f:
                        content = f.read(500)
                        summary += f"[{m}]: {content}...\n\n"
                except: pass

        summary += "Objective: Act as a senior software architect. Provide efficient, production-ready solutions based on the project structure above.\n"
        summary += "--- END CONTEXT ---\n"
        return summary
