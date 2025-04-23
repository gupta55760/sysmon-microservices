# sysmon_sdk

![Build](https://github.com/gupta55760/sysmon-sdk/actions/workflows/python-tests.yml/badge.svg)
![Coverage](coverage.svg)

A lightweight Python system monitoring SDK and CLI...


A lightweight Python system monitoring SDK and CLI that communicates with a background daemon process via Unix Domain Sockets (UDS). It lets users query system metrics like CPU and memory, and control the daemon using simple CLI commands.

---

## 🚀 Features

- 🔧 Multithreaded daemon to monitor CPU and memory usage
- 📡 Client-server communication over Unix domain sockets
- 🧪 Test coverage with `pytest`, `pytest-cov`
- 🖥 Simple CLI interface: `status`, `metrics`, `shutdown`
- 🔐 PID file support and graceful shutdown

---

## 📦 Installation (from PyPI)

You can install the package from **PyPI** using:

```bash
pip install sysmon-sdk
```


## 📦 Installation (from TestPyPI)

You can install the package from **TestPyPI** using:

```bash
pip install --index-url https://test.pypi.org/simple/ sysmon-sdk
```

> ⚠️ Make sure `psutil` is installed if not already. You can run:  
> `pip install psutil`

---

## 🧑‍💻 Usage

First, run the daemon (this runs in the background):

```bash
python -m sysmon_sdk.daemon
```

Then use the CLI commands:

```bash
sysmon status     # Check daemon status
sysmon metrics    # View current CPU and memory usage
sysmon shutdown   # Gracefully shut down the daemon
```

---

## 🛠 Developer Setup

Clone the repository and install locally:

```bash
git clone https://github.com/YOUR_USERNAME/sysmon-sdk.git
cd sysmon-sdk
pip install .
```

To run the CLI directly from source:

```bash
python -m sysmon_sdk.cli status
```

---

## 🧪 Running Tests

Run all unit and integration tests:

```bash
pytest
```

To get test coverage:

```bash
pytest --cov=sysmon_sdk --cov-report=html
open htmlcov/index.html
```

To run all tests and generate coverage reports with daemon:

```bash
./test_runner.sh
```

---

## 📁 Project Structure

```
sysmon_sdk/
├── cli.py         # CLI entry point
├── core.py        # Client-side socket interaction
├── daemon.py      # Multithreaded background process
├── config.py      # Loads socket path/config
├── config.json    # Optional config file
```

---

## 📜 License

This project is licensed under the MIT License.  
Feel free to use, modify, and distribute.

---
