import argparse
import re
import qrcode
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_label(pdf, label_type, text, font_size):
    if label_type == 'dymo':
        generate_dymo_label(pdf, text, font_size)
    else:
        generate_ptouch_label(pdf, text, font_size)

def generate_dymo_label(pdf, text, font_size):
    width, height = landscape((153, 72))  # Use predefined label size
    pdf.setPageSize((width, height))
    draw_text_centered(pdf, text, width, height, font_size)

def generate_ptouch_label(pdf, text, font_size):
    text_width = calculate_text_width(text, font_size) + 10  # Padding
    height = 12 * mm  # Fixed height
    width = text_width
    pdf.setPageSize((width, height))
    draw_text_centered(pdf, text, width, height, font_size)

def draw_text_centered(pdf, text, width, height, font_size):
    pdf.setFont("Helvetica", font_size)  # Changed to Helvetica for simplicity
    text_width = pdf.stringWidth(text, "Helvetica", font_size)
    x = (width - text_width) / 2
    y = (height - font_size) / 2
    pdf.drawString(x, y, text)
    pdf.showPage()

def calculate_text_width(text, font_size):
    test_pdf = BytesIO()
    test_canvas = canvas.Canvas(test_pdf)
    test_canvas.setFont("Helvetica", font_size)
    return test_canvas.stringWidth(text, "Helvetica", font_size)

def main():
    parser = argparse.ArgumentParser(description='Generate PDF labels for printers.')
    parser.add_argument('printer', choices=['dymo', 'ptouch'], help='Specify the printer type.')
    parser.add_argument('labels', nargs='+', help='Labels to print.')
    parser.add_argument('--size', choices=['S', 'M', 'L'], default='M', help='Font size: S, M, L.')
    parser.add_argument('--output', default='labels.pdf', help='Output PDF filename.')
    args = parser.parse_args()

    font_sizes = {'S': 8, 'M': 12, 'L': 18}
    font_size = font_sizes[args.size.upper()]

    pdf = canvas.Canvas(args.output)
    for label in args.labels:
        generate_label(pdf, args.printer, label, font_size)
    pdf.save()
    print(f"PDF with multiple labels generated: {args.output}")

if __name__ == '__main__':
    main()
