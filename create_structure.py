from pathlib import Path
FILES = [
    Path('app/__init__.py'),
    Path('app/main.py'),
    Path('app/config.py'),
    Path('app/schemas.py'),
    Path('app/agent/__init__.py'),
    Path('app/agent/tools.py'),
    Path('app/agent/graph.py'),
    Path('ui/streamlit_app.py'),
    Path('requirements.txt'),
    Path('.env.example'),
    Path('.gitignore'),
    Path('.dockerignore'),
    Path('Dockerfile'),
    Path('compose.yaml'),
    Path('README.md'),
]
for file_path in FILES:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)
print('Project structure created successfully.')
for path in sorted(FILES):
    print(path)