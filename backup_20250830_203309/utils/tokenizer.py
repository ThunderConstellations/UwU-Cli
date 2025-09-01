# utils/tokenizer.py
"""
Context-aware tokenizer and entity extraction for UwU-CLI
Detects filenames, function names, code diffs, and other entities in user input
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Any

# Patterns to detect code entities
FILENAME_PATTERN = r'[\w\-/\\]+\.(py|js|ts|txt|md|json|yaml|yml|cpp|c|java|sh|bat|ps1|exe|dll|so|dylib)'
FUNCTION_PATTERN = r'(?:def|function|func)\s+(\w+)\s*\('
CLASS_PATTERN = r'class\s+(\w+)(?:\s*\(|:)'
CODE_DIFF_PATTERN = r'^[\+\-]{1,2}.*$'  # lines starting with + or -
IMPORT_PATTERN = r'(?:import|from)\s+([\w\.]+)'
VARIABLE_PATTERN = r'\b(\w+)\s*='  # variable assignments
URL_PATTERN = r'https?://[^\s]+'
PATH_PATTERN = r'(?:^|\s)([\/\\][^\s]*|~[\/\\][^\s]*)'
GIT_PATTERN = r'git\s+(?:add|commit|push|pull|clone|init|status|branch|checkout|merge|rebase)'
PYTHON_PATTERN = r'\b(?:python|pip|conda|venv|virtualenv)\b'
NODE_PATTERN = r'\b(?:node|npm|yarn|npx)\b'
DOCKER_PATTERN = r'\b(?:docker|dockerfile|docker-compose)\b'

def extract_filenames(text: str) -> List[str]:
    """Return a list of detected filenames in the input."""
    matches = re.findall(FILENAME_PATTERN, text, re.IGNORECASE)
    # Filter out common false positives
    filtered = []
    for match in matches:
        if not any(fp in match.lower() for fp in ['http', 'www', 'example']):
            filtered.append(match)
    return filtered

def extract_functions(text: str) -> List[str]:
    """Return a list of detected function names in the input."""
    return re.findall(FUNCTION_PATTERN, text, re.IGNORECASE)

def extract_classes(text: str) -> List[str]:
    """Return a list of detected class names in the input."""
    return re.findall(CLASS_PATTERN, text, re.IGNORECASE)

def extract_code_diffs(text: str) -> List[str]:
    """Return a list of detected code diff lines in the input."""
    lines = text.split('\n')
    diffs = [line for line in lines if re.match(CODE_DIFF_PATTERN, line)]
    return diffs

def extract_imports(text: str) -> List[str]:
    """Return a list of detected import statements."""
    return re.findall(IMPORT_PATTERN, text, re.IGNORECASE)

def extract_variables(text: str) -> List[str]:
    """Return a list of detected variable names."""
    return re.findall(VARIABLE_PATTERN, text)

def extract_urls(text: str) -> List[str]:
    """Return a list of detected URLs."""
    return re.findall(URL_PATTERN, text)

def extract_paths(text: str) -> List[str]:
    """Return a list of detected file paths."""
    return re.findall(PATH_PATTERN, text)

def extract_git_commands(text: str) -> List[str]:
    """Return a list of detected Git commands."""
    return re.findall(GIT_PATTERN, text, re.IGNORECASE)

def extract_python_commands(text: str) -> List[str]:
    """Return a list of detected Python-related commands."""
    return re.findall(PYTHON_PATTERN, text, re.IGNORECASE)

def extract_node_commands(text: str) -> List[str]:
    """Return a list of detected Node.js-related commands."""
    return re.findall(NODE_PATTERN, text, re.IGNORECASE)

def extract_docker_commands(text: str) -> List[str]:
    """Return a list of detected Docker-related commands."""
    return re.findall(DOCKER_PATTERN, text, re.IGNORECASE)

def context_entities(text: str) -> Dict[str, Any]:
    """Return a dict of all entities detected in text."""
    return {
        "filenames": extract_filenames(text),
        "functions": extract_functions(text),
        "classes": extract_classes(text),
        "diffs": extract_code_diffs(text),
        "imports": extract_imports(text),
        "variables": extract_variables(text),
        "urls": extract_urls(text),
        "paths": extract_paths(text),
        "git_commands": extract_git_commands(text),
        "python_commands": extract_python_commands(text),
        "node_commands": extract_node_commands(text),
        "docker_commands": extract_docker_commands(text)
    }

def inject_context(roast: str, text: str) -> str:
    """
    Replace placeholder tokens in roast with detected context from input.
    Supports:
        {file}, {function}, {class}, {diff}, {import}, {variable}, {url}, {path}
        {git}, {python}, {node}, {docker}
    """
    entities = context_entities(text)
    
    # Replace with first detected entity if available, else fallback text
    replacements = {
        "{file}": entities["filenames"][0] if entities["filenames"] else "mystery_file",
        "{function}": entities["functions"][0] if entities["functions"] else "do_stuff",
        "{class}": entities["classes"][0] if entities["classes"] else "CoolClass",
        "{diff}": entities["diffs"][0] if entities["diffs"] else "+nothing_changed",
        "{import}": entities["imports"][0] if entities["imports"] else "random_module",
        "{variable}": entities["variables"][0] if entities["variables"] else "some_var",
        "{url}": entities["urls"][0] if entities["urls"] else "http://example.com",
        "{path}": entities["paths"][0] if entities["paths"] else "/some/path",
        "{git}": entities["git_commands"][0] if entities["git_commands"] else "git commit",
        "{python}": entities["python_commands"][0] if entities["python_commands"] else "python script",
        "{node}": entities["node_commands"][0] if entities["node_commands"] else "node app",
        "{docker}": entities["docker_commands"][0] if entities["docker_commands"] else "docker run"
    }
    
    for placeholder, replacement in replacements.items():
        roast = roast.replace(placeholder, str(replacement))
    
    return roast

def get_context_summary(text: str) -> str:
    """Get a human-readable summary of detected context."""
    entities = context_entities(text)
    
    summary_parts = []
    
    if entities["filenames"]:
        summary_parts.append(f"files: {', '.join(entities['filenames'][:3])}")
    if entities["functions"]:
        summary_parts.append(f"functions: {', '.join(entities['functions'][:3])}")
    if entities["classes"]:
        summary_parts.append(f"classes: {', '.join(entities['classes'][:3])}")
    if entities["git_commands"]:
        summary_parts.append(f"git: {entities['git_commands'][0]}")
    if entities["python_commands"]:
        summary_parts.append(f"python: {entities['python_commands'][0]}")
    if entities["node_commands"]:
        summary_parts.append(f"node: {entities['node_commands'][0]}")
    if entities["docker_commands"]:
        summary_parts.append(f"docker: {entities['docker_commands'][0]}")
        
    if summary_parts:
        return f"Context detected: {' | '.join(summary_parts)}"
    else:
        return "No specific context detected"

def is_code_related(text: str) -> bool:
    """Check if the text appears to be code-related."""
    entities = context_entities(text)
    
    # Check if any code-related entities were found
    code_indicators = [
        entities["filenames"], entities["functions"], entities["classes"],
        entities["diffs"], entities["imports"], entities["variables"],
        entities["git_commands"], entities["python_commands"],
        entities["node_commands"], entities["docker_commands"]
    ]
    
    return any(entities for entities in code_indicators)

def get_roast_intensity(text: str) -> str:
    """Determine roast intensity based on context."""
    if is_code_related(text):
        entities = context_entities(text)
        
        # More complex code = more intense roasting
        complexity_score = (
            len(entities["functions"]) * 2 +
            len(entities["classes"]) * 3 +
            len(entities["imports"]) * 1 +
            len(entities["git_commands"]) * 2
        )
        
        if complexity_score > 10:
            return "feral"  # Very intense
        elif complexity_score > 5:
            return "wizard"  # Medium intense
        else:
            return "uwu"     # Soft roasting
    else:
        return "uwu"  # Default soft roasting 