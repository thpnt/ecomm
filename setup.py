from setuptools import setup, find_packages

# Read the requirements from requirements.txt
def read_requirements():
    with open('requirements.txt', 'r') as f:
        return f.read().splitlines()

setup(
    name="project_repo",
    version="0.1",
    packages=find_packages(),
    install_requires=read_requirements(),  # Add dependencies here if needed
)