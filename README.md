# LabelMaker

A command-line utility for generating PDF labels for Dymo and Brother P-touch label printers.

## Overview

LabelMaker is a simple Python tool that generates PDF files formatted specifically for common label printers. It supports:
- Dymo label printers (using fixed size labels)
- Brother P-touch label printers (with dynamic width)
- Variable font sizes
- Multiple labels in a single PDF output

## Usage

```bash
python labelmaker.py [printer_type] [labels...] [options]
```

### Arguments

- `printer_type`: Either `dymo` or `ptouch`
- `labels`: One or more text strings for your labels

### Options

- `--size {S,M,L}`: Font size (Small, Medium, Large), defaults to Medium
- `--output FILENAME`: Output PDF filename, defaults to `labels.pdf`

### Examples

```bash
# Create a Dymo label with medium-sized text
python labelmaker.py dymo "Hello World"

# Create multiple P-touch labels with large text
python labelmaker.py ptouch "Label 1" "Label 2" "Label 3" --size L

# Specify a custom output filename
python labelmaker.py dymo "Custom Label" --output my_labels.pdf
```

## Features

- Dymo labels use a fixed size format (153x72)
- P-touch labels adjust width based on text content with fixed height
- Text is automatically centered on labels
- Supports three font size presets (Small, Medium, Large)

## Dependencies

- ReportLab: For PDF generation
- QRCode: For QR code functionality (imported but not fully implemented yet)
