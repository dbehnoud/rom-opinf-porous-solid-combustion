# ROM-UQ-Porous_Solid-Combustion

This repo implements a reduced-order modeling (ROM) and uncertainty quantification (UQ) framework for reactive multi-species flows using Operator Inference. This project builds on concepts from [rom-operator-inference-Python3](https://github.com/Willcox-Research-Group/rom-operator-inference-Python3), a library for operator inference-based model reduction.

## Features

- POD-based ROMs with polynomial operators (Const, Linear, Quad, Cubic)
- Parametric ROM support (AffineLinearOperator)
- Custom Euler lifters for specific volume & molar conversion
- Monte Carlo UQ (Gaussian perturbations)


## Structure

- `src/` - Python modules
- `README.md` - Overview and instructions
- `data/` - Data folder 

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.rom_builder import train_rom
from src.data_loader import load_snapshots
...
```

## License

GNU GENERAL PUBLIC LICENSE
