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
from codechembook.symbols import chem, chemformula, elements, greek, math, script, typesettingHTML, typography

modules = {
    "chem": chem,
    "chemformula": chemformula,
    "elements": elements,
    "greek": greek,
    "math": math,
    "script": script,
    "typesettingHTML": typesettingHTML,
    "typography": typography,
}

for mod_name, mod in modules.items():
    doc_path = f"symbols/{mod_name}.md"
    
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
        print("| Symbol | Variable Name | Python Code |", file=fd)
        print("|:---:|:---|:---|", file=fd)
        
        # Get all variables in the module that don't start with an underscore
        variables = [(name, value) for name, value in inspect.getmembers(mod) 
                     if not name.startswith("_") and not inspect.ismodule(value) and not inspect.isfunction(value) and not inspect.isclass(value)]
        
        # Write rows
        for name, value in variables:
            # We want to display the visual representation of the symbol.
            # If it's a string, it's typically a unicode character.
            # In markdown we can just print the character.
            # To be safe against weird characters breaking the table, we might need to handle newlines.
            safe_value = str(value).replace("\n", " ").replace("|", "\\|")
            python_code = f"`from codechembook.symbols.{mod_name} import {name}`"
            print(f"| {safe_value} | `{name}` | {python_code} |", file=fd)
