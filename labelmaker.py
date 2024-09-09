import argparse
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_dymo_label(output_filename, text):
    # Label size for Dymo 30336 in landscape mode: 2-1/8" x 1"
    width, height = landscape((153, 72))  # 2-1/8" x 1" in points
    
    # Create a PDF canvas
    pdf = canvas.Canvas(output_filename, pagesize=(width, height))
    
    # Determine optimal font size
    font_size = determine_font_size(text, width, height)
    
    # Set font and size
    pdf.setFont("Helvetica-Bold", font_size)
    
    # Calculate text width for centering
    text_width = pdf.stringWidth(text, "Helvetica-Bold", font_size)
    
    # Draw the text at the center of the label
    pdf.drawString((width - text_width) / 2, (height - font_size) / 2, text)
    
    # Finalize the PDF
    pdf.showPage()
    pdf.save()

def generate_ptouch_label(output_filename, text, font_size):
    # Define font sizes based on S/M/L input
    font_sizes = {'S': 8, 'M': 12, 'L': 18}  # Font sizes in points
    font_size = font_sizes.get(font_size.upper(), 12)  # Default to medium if not specified
    
    # Calculate the width needed for the text
    width = calculate_text_width(text, font_size) + 10  # Add a bit of padding
    
    # Set the height to 12mm (about 34 points)
    height = 12 * mm
    
    # Create a PDF canvas with dynamic width and fixed height
    pdf = canvas.Canvas(output_filename, pagesize=(width, height))
    
    # Set font and size
    pdf.setFont("Helvetica-Bold", font_size)
    
    # Calculate text width and height for centering
    text_width = pdf.stringWidth(text, "Helvetica-Bold", font_size)
    text_height = font_size  # Approximation, as the font size is roughly the height
    
    # Draw the text centered vertically on the label
    text_y = (height - text_height + 4) / 2  # Improved vertical centering
    pdf.drawString(5, text_y, text)  # Start drawing 5 points from the left for padding
    
    # Finalize the PDF
    pdf.showPage()
    pdf.save()

def determine_font_size(text, width, height):
    # Start with a large font size and decrease until it fits the label
    font_size = 72  # Start with a large font size (1 inch)
    min_font_size = 6  # Define a minimum font size
    
    # Test font size by reducing until the text fits within the label width
    while font_size > min_font_size:
        test_pdf = BytesIO()
        test_canvas = canvas.Canvas(test_pdf)
        text_width = test_canvas.stringWidth(text, "Helvetica-Bold", font_size)
        
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

def main():
    # Setup argument parser for CLI
    parser = argparse.ArgumentParser(description='Generate a PDF label for either Dymo or Brother P-Touch printers.')
    parser.add_argument('printer', choices=['dymo', 'ptouch'], help='Specify which printer you are using: dymo or ptouch.')
    parser.add_argument('text', type=str, help='The text to print on the label.')
    parser.add_argument('--size', type=str, choices=['S', 'M', 'L'], default='M', help='Font size for Brother P-Touch: S (Small), M (Medium), L (Large).')
    parser.add_argument('--output', type=str, default='label.pdf', help='The output filename for the generated PDF.')
    
    args = parser.parse_args()
    
    # Generate label based on the printer type
    if args.printer == 'dymo':
        generate_dymo_label(args.output, args.text)
    elif args.printer == 'ptouch':
        generate_ptouch_label(args.output, args.text, args.size)
    
    print(f"PDF label generated: {args.output}")

if __name__ == '__main__':
    main()
