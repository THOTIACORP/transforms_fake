from setuptools import setup, find_packages

setup(
    name='transforms_fake',
    version='0.1.0',
    packages=find_packages(),  # Isso busca a pasta transforms_fake com __init__.py
    install_requires=[
         "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "PyQt5>=5.15.0"
    ],
    entry_points={
        'console_scripts': [
            'transforms-fake=src.__main__:main'
        ],
    },
)
