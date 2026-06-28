import os
import ast

def extract_api_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except Exception:
            return None

    module_doc = ast.get_docstring(tree) or ""
    
    classes = []
    functions = []
    
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_doc = ast.get_docstring(node) or "No documentation provided."
            methods = []
            for n in node.body:
                if isinstance(n, ast.FunctionDef):
                    # Skip private methods except __init__
                    if n.name.startswith('_') and n.name != '__init__':
                        continue
                    method_doc = ast.get_docstring(n) or "No documentation provided."
                    args = [a.arg for a in n.args.args]
                    methods.append({
                        "name": n.name,
                        "args": args,
                        "doc": method_doc
                    })
            classes.append({
                "name": node.name,
                "doc": class_doc,
                "methods": methods
            })
        elif isinstance(node, ast.FunctionDef):
            if node.name.startswith('_'):
                continue
            func_doc = ast.get_docstring(node) or "No documentation provided."
            args = [a.arg for a in node.args.args]
            functions.append({
                "name": node.name,
                "args": args,
                "doc": func_doc
            })
            
    return {
        "module_doc": module_doc,
        "classes": classes,
        "functions": functions
    }

def generate_markdown(file_path, api_info):
    if not api_info['classes'] and not api_info['functions']:
        return "" # Don't append empty API docs
        
    md = f"\n## API Reference: `{os.path.basename(file_path)}`\n\n"
    if api_info['module_doc']:
        md += f"{api_info['module_doc']}\n\n"
    
    if api_info['classes']:
        md += "### Classes\n\n"
        for cls in api_info['classes']:
            md += f"#### `class {cls['name']}`\n"
            md += f"{cls['doc']}\n\n"
            if cls['methods']:
                md += "**Methods:**\n\n"
                for m in cls['methods']:
                    args_str = ", ".join(m['args'])
                    doc_first_line = m['doc'].split(chr(10))[0] if m['doc'] else ""
                    md += f"- **`{m['name']}({args_str})`**: {doc_first_line}\n"
                md += "\n"
                
    if api_info['functions']:
        md += "### Functions\n\n"
        for func in api_info['functions']:
            args_str = ", ".join(func['args'])
            md += f"#### `def {func['name']}({args_str})`\n"
            md += f"{func['doc']}\n\n"
            
    return md

# Mapping of directories to the markdown files they should append to
mapping = {
    "pulse_engine": "pulse_engine.md",
    "job_layer": "job_layer.md",
    "big_algo_engine": "big_algo_engine.md",
    "qml": "qml_module.md",
    "sha256": "sha256_module.md",
    "examples": "dashboard.md",
    "utils": "api_reference.md",
    "algorithm_blocks": "algorithm_blocks.md"
}

file_mapping = {
    "core/main_10qubit_design.py": "hardware_layer.md",
    "core/klayout_quantum_processor.py": "hardware_layer.md",
    "core/qpu_os.py": "os_layer.md",
    "core/quantum_gates.py": "os_layer.md",
    "core/quantum_processor_simulation.py": "simulation_verification.md",
    "core/quantum_processor_verification.py": "simulation_verification.md",
    "core/config.py": "configuration.md",
    "dashboard.py": "dashboard.md",
    "run_pipeline.py": "getting_started.md"
}

def main():
    docs_dir = "docs"
    
    print("Generating deep documentation...")
    appended_files = 0
    
    for root, dirs, files in os.walk("."):
        if "venv" in root or ".git" in root or "scripts" in root or docs_dir in root or "build" in root or "__pycache__" in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file).replace("\\", "/")
                # remove leading ./
                if path.startswith("./"):
                    path = path[2:]
                
                # Determine which markdown file to append to
                md_filename = file_mapping.get(path)
                if not md_filename:
                    # try by folder
                    folder = path.split("/")[0]
                    md_filename = mapping.get(folder)
                    
                if md_filename:
                    api_info = extract_api_info(path)
                    if api_info:
                        md_content = generate_markdown(path, api_info)
                        
                        if md_content.strip():
                            md_path = os.path.join(docs_dir, md_filename)
                            if os.path.exists(md_path):
                                with open(md_path, "a", encoding="utf-8") as f:
                                    f.write("\n---\n")
                                    f.write(md_content)
                                appended_files += 1
                                print(f"Appended {path} -> {md_filename}")

    print(f"Deep documentation complete! Appended {appended_files} module references.")

if __name__ == "__main__":
    main()
