# Development Guide for Claude

## Running the Project

This project is managed with `uv`. Use the following command to run the script:

```bash
uv run labelmaker.py [arguments]
```

Example:
```bash
uv run labelmaker.py dymo "Test Label" --size M
```

## Basic Commands

- Run the script:
  ```bash
  uv run labelmaker.py [printer_type] [labels...] [options]
  ```

- Install dependencies:
  ```bash
  uv pip install -r requirements.txt
  ```
  
- Install in development mode:
  ```bash
  uv pip install -e .
  ```