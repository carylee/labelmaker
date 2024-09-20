import argparse
import re
import qrcode
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from PIL import Image

def generate_dymo_label(pdf, text):
    # Label size for Dymo 30336 in landscape mode: 2-1/8" x 1"
    width, height = landscape((153, 72))  # 2-1/8" x 1" in points

    # Determine optimal font size
    font_size = determine_font_size(text, width, height)

    # Set font and size
    pdf.setFont("Helvetica-Bold", font_size)

    # Calculate text width for centering
    text_width = pdf.stringWidth(text, "Helvetica-Bold", font_size)

    # Draw the text at the center of the label
    pdf.drawString((width - text_width) / 2, (height - font_size) / 2, text)

    # Finalize this page
    pdf.showPage()

def generate_ptouch_label(pdf, text, font_size, has_qr_code=False):
    font_sizes = {'S': 8, 'M': 12, 'L': 18}  # Font sizes in points
    font_size = font_sizes.get(font_size.upper(), 12)  # Default to medium if not specified

    text_width = calculate_text_width(text, font_size) + 10  # Add a bit of padding

    qr_code_width = 0
    qr_padding = 10  # Space between text and QR code
    if has_qr_code:
        qr_code_width = 40 + qr_padding

    total_width = text_width + qr_code_width  # Calculate total width including QR code

    # Set a new page with the calculated width and fixed height
    pdf.setPageSize((total_width, 12 * mm))

    # Set font and size
    pdf.setFont("Helvetica-Bold", font_size)

    # Center the text vertically
    text_y = (12 * mm - font_size) / 2  # Center the text vertically

    # Draw the text
    pdf.drawString(5, text_y, text)  # Start drawing 5 points from the left for padding

    # If QR code needs to be added, do not finalize the page here
    if not has_qr_code:
        pdf.showPage()

def determine_font_size(text, width, height):
    # Start with a large font size and decrease until it fits the label
    font_size = 72  # Start with a large font size (1 inch)
    min_font_size = 6  # Define a minimum font size

    # Test font size by reducing until the text fits within the label width
    while font_size > min_font_size:
        text_width = calculate_text_width(text, font_size)
        if text_width <= width - 10:  # Adjust for some padding
            break
        font_size -= 1

    return max(font_size, min_font_size)

def calculate_text_width(text, font_size):
    # Create a temporary canvas to calculate text width
    test_pdf = BytesIO()
    test_canvas = canvas.Canvas(test_pdf)
    text_width = test_canvas.stringWidth(text, "Helvetica-Bold", font_size)
    return text_width

def add_qr_code_to_pdf(pdf, url, text_width, total_width):
    # Assuming the total width has accounted for the QR code
    qr_size = 40  # Size of the QR code, adjust if necessary for aesthetics
    qr_padding = 10  # Padding between text and QR code

    # Generate a QR code for the URL
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Use ImageReader to convert the BytesIO image to something ReportLab can use
    qr_image_reader = ImageReader(img_byte_arr)

    # Position the QR code to the right of the text
    qr_code_x = text_width + qr_padding  # Calculate the x position
    qr_code_y = (12 * mm - qr_size) / 2  # Center the QR code vertically

    # Insert the QR code into the PDF
    pdf.drawImage(qr_image_reader, x=qr_code_x, y=qr_code_y, width=qr_size, height=qr_size)

    # Finalize the page
    pdf.showPage()

def is_url(string):
    # Regex to check if a string contains a URL
    url_regex = re.compile(r'(https?://[^\s]+)')
    return url_regex.search(string)

def main():
    # Setup argument parser for CLI
    parser = argparse.ArgumentParser(description='Generate a multi-page PDF label for either Dymo or Brother P-Touch printers.')
    parser.add_argument('printer', choices=['dymo', 'ptouch'], help='Specify which printer you are using: dymo or ptouch.')
    parser.add_argument('labels', nargs='+', type=str, help='The labels to print. Multiple labels can be provided, each generating a new page.')
    parser.add_argument('--size', type=str, choices=['S', 'M', 'L'], default='M', help='Font size for Brother P-Touch: S (Small), M (Medium), L (Large).')
    parser.add_argument('--output', type=str, default='labels.pdf', help='The output filename for the generated PDF.')

    args = parser.parse_args()

    # Convert the font size string (S/M/L) to an actual font size in points
    font_sizes = {'S': 8, 'M': 12, 'L': 18}
    font_size = font_sizes.get(args.size.upper(), 12)  # Default to medium if not specified

    # Create a PDF canvas
    pdf = canvas.Canvas(args.output)

    # Generate labels for each text input
    for label in args.labels:
        url_match = is_url(label)
        if url_match:
            # Extract the URL and text before it
            url = url_match.group(0)
            text = label.replace(url, '').strip()

            # Calculate text width and total width
            text_width = calculate_text_width(text, font_size)
            qr_code_width = 40 + 10  # QR code width plus padding
            total_width = text_width + qr_code_width  # Total width including QR code

            # Generate the label with text and QR code
            if args.printer == 'dymo':
                generate_dymo_label(pdf, text)
            elif args.printer == 'ptouch':
                generate_ptouch_label(pdf, text, args.size, has_qr_code=True)
                # Add the QR code for the URL next to the text
                add_qr_code_to_pdf(pdf, url, text_width, total_width)

        else:
            # Just generate the text label if no URL is found
            if args.printer == 'dymo':
                generate_dymo_label(pdf, label)
            elif args.printer == 'ptouch':
                generate_ptouch_label(pdf, label, args.size, has_qr_code=False)

    # Save the PDF
    pdf.save()

    print(f"PDF with multiple labels generated: {args.output}")

if __name__ == '__main__':
    main()
