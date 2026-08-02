<p align="center">
  <img src="assets/logo.png" width="90" alt="EMM-Essence logo">
</p>

<h1 align="center">EMM-Essence</h1>

**EMM-Essence** (*Energy Market Model Essence*) is an open-source energy market model implemented in Python using Pyomo. It provides a compact, transparent, and extensible framework for electricity market modeling with optional sector coupling.

Unlike many research models, EMM-Essence is designed to detect input and configuration errors before optimization starts. Comprehensive validation of input data and preprocessing helps identify inconsistencies early, making model development more reliable and significantly reducing debugging effort.

## Features

* Welfare-maximizing energy market optimization
* Multi-region and multi-period modeling
* Conventional and renewable generation
* Storage technologies and demand-side flexibility
* Capacity expansion planning
* Imports, exports, and interregional trade
* Carbon pricing
* CSV-based input data
* Comprehensive input validation
* Extensive automated test suite

## Technology

EMM-Essence is built with **Python**, **Pyomo**, **NumPy**, and **pandas**. Gurobi is currently supported as the optimization solver, with support for open-source solvers planned.

## Installation

### 1. Install uv

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

On Windows, run in PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart PowerShell after the installation.

### 2. Install EMMEssence

```bash
git clone https://github.com/SEBA5T1AN/emm-essence.git
cd emm-essence
uv sync --locked --no-dev
```

### 3. Run EMMEssence

```bash
uv run emmessence
```

A valid Gurobi license is required to solve optimization models.

## Testing

```bash
uv run pytest
```

## Example

A minimal working example with sample input data is included to demonstrate the complete workflow from data validation and model construction to optimization and result export.

## Contributing

Contributions, bug reports, feature requests, and suggestions are welcome.

## License

EMM-Essence is released under the MIT License.
