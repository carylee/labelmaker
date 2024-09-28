import argparse
import re
import qrcode
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_label(pdf, label_type, text, font_size, url=None):
    if label_type == 'dymo':
        generate_dymo_label(pdf, text, font_size)
    else:
        generate_ptouch_label(pdf, text, font_size, bool(url))
    
    if url:
        add_qr_code_to_pdf(pdf, url, text, font_size)

def generate_dymo_label(pdf, text, font_size):
    width, height = landscape((153, 72))
    set_pdf_page_size(pdf, width, height)
    draw_text_centered(pdf, text, width, height, font_size)

def generate_ptouch_label(pdf, text, font_size, has_qr_code):
    text_width = calculate_text_width(text, font_size) + 10
    height = 12 * mm
    width = text_width + (50 if has_qr_code else 0)
    set_pdf_page_size(pdf, width, height)
    draw_text(pdf, text, 5, (height - font_size) / 2, font_size)

def set_pdf_page_size(pdf, width, height):
    pdf.setPageSize((width, height))

def draw_text_centered(pdf, text, width, height, font_size):
    text_width = calculate_text_width(text, font_size)
    draw_text(pdf, text, (width - text_width) / 2, (height - font_size) / 2, font_size)
    pdf.showPage()

def draw_text(pdf, text, x, y, font_size):
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.drawString(x, y, text)

def add_qr_code_to_pdf(pdf, url, text, font_size):
    text_width = calculate_text_width(text, font_size)
    qr_size = 40
    qr_x = text_width + 10
    qr_y = (12 * mm - qr_size) / 2
    qr_image = generate_qr_code_image(url, qr_size)
    pdf.drawImage(qr_image, x=qr_x, y=qr_y, width=qr_size, height=qr_size)
    pdf.showPage()

def generate_qr_code_image(url, size):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return ImageReader(img_byte_arr)

def calculate_text_width(text, font_size):
    test_pdf = BytesIO()
    test_canvas = canvas.Canvas(test_pdf)
    return test_canvas.stringWidth(text, "Helvetica-Bold", font_size)

def is_url(string):
    url_regex = re.compile(r'(https?://[^\s]+)')
    return url_regex.search(string)

def main():
    parser = argparse.ArgumentParser(description='Generate a multi-page PDF label for Dymo or Brother P-Touch printers.')
    parser.add_argument('printer', choices=['dymo', 'ptouch'], help='Specify which printer to use.')
    parser.add_argument('labels', nargs='+', type=str, help='Labels to print, each generating a new page.')
    parser.add_argument('--size', type=str, choices=['S', 'M', 'L'], default='M', help='Font size: S, M, L.')
    parser.add_argument('--output', type=str, default='labels.pdf', help='Output filename.')
    args = parser.parse_args()

    font_sizes = {'S': 8, 'M': 12, 'L': 18}
    font_size = font_sizes[args.size.upper()]

    pdf = canvas.Canvas(args.output)
    for label in args.labels:
        url_match = is_url(label)
        url = url_match.group(0) if url_match else None
        text = label.replace(url, '').strip() if url else label
        generate_label(pdf, args.printer, text, font_size, url)
    pdf.save()
    print(f"PDF with multiple labels generated: {args.output}")

if __name__ == '__main__':
    main()

