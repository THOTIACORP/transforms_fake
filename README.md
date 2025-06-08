# transforms_fake

A Python library for generating realistic synthetic images to train segmentation models in a smart, simple way.

[![PyPI version](https://img.shields.io/badge/version-0.1.0-blue)](https://pypi.org/project/transforms-fake/)
[![License](https://img.shields.io/badge/license-GNU-green)](https://github.com/THOTIACORP/transforms_fake/blob/main/LICENSE)
[![Status](https://img.shields.io/badge/status-development-yellow)](https://github.com/THOTIACORP/transforms_fake)

## Overview

`transforms_fake` automatically generates new labeled images and masks from existing annotated datasets. Unlike traditional augmentation libraries, which only transform existing data, this library creates entirely new training examples by intelligently extracting and repositioning objects with their corresponding masks.

**Key innovation**: context-aware object insertion that maintains a realistic appearance while expanding the diversity of the dataset.

## Features

- **Instance-aware copy and paste**: extract objects using segmentation masks
- **Contextual transformations**: rotation, scaling, and inversion with mask preservation
- **Insertion between images**: place objects from one image into different backgrounds
- **Automatic mask updates**: maintains segmentation labels with pixel-perfect accuracy
- **Framework integration**: compatible with PyTorch and FastAI workflows
- **Dataset export**: generate ready-to-use training datasets

## Installation

```bash
pip install transforms_fake
```

For the latest development version:

```bash
pip install git+https://github.com/THOTIACORP/transforms_fake.git
```

## Quick start

```python
from transforms_fake.main import main

# Basic usage
main()
```

## Dataset structure

Organize your data as follows:

```
dataset/
├── images/
│   ├── image1.png
│   └── image2.png
└── masks/
    ├── image1_mask.png
    └── image2_mask.png
```

## How it works

1. **Input processing**: Loads images with corresponding segmentation masks
2. **Instance detection**: Identifies individual objects within the masks
3. **Object extraction**: Isolates objects using the mask boundaries
4. **Contextual placement**: Inserts objects into new locations with transformations
5. **Mask synchronization**: Updates the segmentation masks to match the new object positions

## Comparison with existing tools

### vs. Albumentations

| Feature                              | Albumentations | transforms_fake |
| ------------------------------------ | -------------- | --------------- |
| Traditional augmentation             | ✅             | ✅              |
| Synthetic instance generation        | ❌             | ✅              |
| Individual object manipulation       | ❌             | ✅              |
| Copy and paste with mask recognition | ❌             | ✅              |

### vs. Other augmentation tools

- **Traditional libraries** modify existing pixels
- **transforms_fake** creates new object arrangements while preserving realism
- Designed specifically for segmentation tasks that require diversity at the instance level

## Use cases

- **Medical images**: augment rare cases of pathologies
- **Object detection**: augment variations in object occurrence
- **Segmentation**: generate diverse object arrangements
- **Small datasets**: multiply training examples contextually

## Requirements

- Python 3.7+
- PIL/Pillow for image processing
- NumPy for matrix operations
- Compatible with PyTorch and FastAI

## Contributions

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branches
3. Submit pull requests with clear descriptions
4. Report bugs via issues on GitHub

## License

GNU General Public License v3.0 - See [LICENSE](LICENSE) for details.

## Contact

**THOTIACORP**

- GitHub: [@THOTIACORP](https://github.com/THOTIACORP)
- Email: founder@thotiacorp.com.br

## Authors

- [Peres; RB](https://www.linkedin.com/in/ronnei-borges/)
- [Borges; CA](https://www.linkedin.com/in/cesar-augusto-dev-br/)
