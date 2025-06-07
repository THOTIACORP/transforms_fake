from setuptools import setup, find_packages

setup(
    name="transforms-fake",
    version="1.0.0",
    author="Seu Nome",
    author_email="seu.email@exemplo.com", 
    description="Uma biblioteca para gerar variações de imagens",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "PyQt5>=5.15.0"
    ],
    entry_points={
        "console_scripts": [
            "transforms-fake-gui=transforms_fake.gui:main",
        ],
    },
)