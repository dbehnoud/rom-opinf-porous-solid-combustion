# 🔥 ROM-UQ-Combustion

This repo implements a reduced-order modeling (ROM) and uncertainty quantification (UQ) framework for reactive multi-species flows using Operator Inference.

## Features

- POD-based ROMs with polynomial operators (Const, Linear, Quad, Cubic)
- Parametric ROM support (AffineLinearOperator)
- Custom Euler lifters for specific volume & molar conversion
- Monte Carlo UQ (Gaussian perturbations)
- Visualization and L2 error analysis

## Structure

- `src/` - Python modules
- `README.md` - Overview and instructions
- `caseBflatUQ/` - Data folder (not included)

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

MIT