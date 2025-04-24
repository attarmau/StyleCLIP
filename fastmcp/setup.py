from setuptools import setup, find_packages

setup(
    name='fastmcp',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic',
        'python-multipart',
        'pillow',
        'torch',
        'transformers',
        'sentence-transformers',
        'motor',
        'python-dotenv'
    ]
)
