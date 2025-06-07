from setuptools import setup, find_packages

setup(
    name='rato-generator',
    version='0.1.0',
    description='Gerador de ratos com fundo aleatório e máscaras',
    author='Seu Nome',
    author_email='seu@email.com',
    packages=find_packages(),
    install_requires=[
        'opencv-contrib-python',
        'numpy',
        'pillow',
        'matplotlib',
        'tqdm',
        'json5',
        'torchvision',
        'opencv-python',
        'scikit-learn',
        'plotly',
        'PyQt5',
        'PyQt5-tools',
        'fastapi',
        'uvicorn'
    ],
    entry_points={
        'console_scripts': [
            'rato-generator = rato_generator.gui:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9.13',
)
