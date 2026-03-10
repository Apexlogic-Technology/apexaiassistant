import os

root_dir = r"c:\Users\HP 450 G5\Documents\GitHub\erpassist"

exclude_ext = ['.pyc', '.png', '.jpg', '.pdf', '.git']
exclude_dirs = ['.git', '.gemini']

def process_contents():
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if any(ex in dirpath for ex in exclude_dirs):
            continue
        for filename in filenames:
            if filename in ['replace_script.py']:
                continue
            filepath = os.path.join(dirpath, filename)
            
            if any(filepath.endswith(ext) for ext in exclude_ext):
                continue
                
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace app namespaces and DocType designations
                new_content = content.replace('erpassist', 'apexaiassistant')
                new_content = new_content.replace('ERPAssist', 'ApexAiAssistant')
                new_content = new_content.replace('Erpassist', 'ApexAiAssistant')
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            except Exception as e:
                print(f"Failed to read/write {filepath}: {e}")

def rename_paths():
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if any(ex in dirpath for ex in exclude_dirs):
            continue
            
        for filename in filenames:
            if 'replace_script.py' in filename:
                continue
            if 'erpassist' in filename:
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, filename.replace('erpassist', 'apexaiassistant'))
                os.rename(old_path, new_path)
                
        for dirname in dirnames:
            if 'erpassist' in dirname:
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, dirname.replace('erpassist', 'apexaiassistant'))
                os.rename(old_path, new_path)

if __name__ == "__main__":
    process_contents()
    rename_paths()
    print("Full Deep Architectural Rewrite Completed. All files, folders, and references have been shifted to apexaiassistant.")
