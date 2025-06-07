from setuptools import setup, find_packages

setup(
    name='transforms_fake',
    version='0.1.0',
    packages=find_packages(),  # Isso busca a pasta transforms_fake com __init__.py
    install_requires=[
        'fastapi', 'json5', 'matplotlib', 'numpy', 'opencv-contrib-python',
        'opencv-python', 'pillow', 'plotly', 'PyQt5', 'PyQt5-tools',
        'scikit-learn', 'torchvision', 'tqdm', 'uvicorn'
    ],
    entry_points={
        'console_scripts': [
            'transforms-fake=transforms_fake.__main__:main'
        ],
    },
)
