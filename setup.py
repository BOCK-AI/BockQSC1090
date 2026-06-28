from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="bockqsc1090",
    version="1.0.0",
    description="Full-stack quantum system compiler for a 10-qubit processor",
    author="BOCK-AI",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "run-pipeline=bockqsc1090.run_pipeline:main",
        ]
    },
)
