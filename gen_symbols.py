"""
Generate dynamic markdown pages for the symbols module.
"""

import sys
import inspect
from pathlib import Path
import mkdocs_gen_files

# Add the src directory to the path so we can import codechembook
# This is necessary because mkdocs-gen-files runs before mkdocs builds
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

# Import the modules we want to document
from codechembook.symbols import chem, greek, math, script, typography

modules = {
    "chem": chem,
    "greek": greek,
    "math": math,
    "script": script,
    "typography": typography,
}

for mod_name, mod in modules.items():
    doc_path = f"symbols/{mod_name}.md"
    
    # Extract comments from the source file
    comments = {}
    if hasattr(mod, '__file__') and mod.__file__:
        with open(mod.__file__, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '#' in line:
                    code_part, comment_part = line.split('#', 1)
                    code_part = code_part.strip()
                    # Check if the code part is an assignment to a variable
                    if '=' in code_part or ':' in code_part:
                        var_name = code_part.split(':')[0].split('=')[0].strip()
                        if var_name:
                            comments[var_name] = comment_part.strip()
    
    with mkdocs_gen_files.open(doc_path, "w") as fd:
        print(f"# {mod_name.capitalize()}", file=fd)
        print("", file=fd)
        
        # Add the module docstring if it exists
        if mod.__doc__:
            print(mod.__doc__.strip(), file=fd)
            print("", file=fd)
            
        print("## Available Symbols", file=fd)
        print("", file=fd)
        
        # Table Header
        print("| Description | Symbol | Variable Name | Python Code |", file=fd)
        print("|:---|:---:|:---|:---|", file=fd)
        
        # Get all variables in the module that don't start with an underscore
        variables = [(name, value) for name, value in inspect.getmembers(mod) 
                     if not name.startswith("_") and not inspect.ismodule(value) and not inspect.isfunction(value) and not inspect.isclass(value)]
        
        # Write rows
        for name, value in variables:
            description = comments.get(name, "")
            # We want to display the visual representation of the symbol.
            safe_value = str(value).replace("\n", " ").replace("|", "\\|")
            python_code = f"`from codechembook.symbols.{mod_name} import {name}`"
            print(f"| {description} | {safe_value} | `{name}` | {python_code} |", file=fd)
