from invoke import task

@task
def install(c):
    """Install dependencies"""
    c.run("pip install -r requirements.txt")

@task
def export(c):
    """Export dependencies"""
    c.run("pip freeze > requirements.txt")

@task
def test(c):
    """Run tests with pytest"""
    c.run("pytest -v")

@task
def docs(c):
    """Run MkDocs server"""
    c.run("mkdocs serve")
