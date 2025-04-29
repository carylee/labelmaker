import argparse
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_label_pdf(output_filename, text, font_size):
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

def calculate_text_width(text, font_size):
    # Create a temporary canvas to calculate text width
    test_pdf = BytesIO()
    test_canvas = canvas.Canvas(test_pdf)
    text_width = test_canvas.stringWidth(text, "Helvetica-Bold", font_size)
    
    return text_width

def main():
    # Setup argument parser for CLI
    parser = argparse.ArgumentParser(description='Generate a PDF label with dynamic text sizing for Brother P-Touch printers.')
    parser.add_argument('text', type=str, help='The text to print on the label.')
    parser.add_argument('--size', type=str, choices=['S', 'M', 'L'], default='M', help='Font size: S (Small), M (Medium), L (Large).')
    parser.add_argument('--output', type=str, default='label.pdf', help='The output filename for the generated PDF.')
    
    args = parser.parse_args()
    
    # Generate the label PDF with provided text, size, and output filename
    generate_label_pdf(args.output, args.text, args.size)
    
    print(f"PDF label generated: {args.output}")

if __name__ == '__main__':
    main()
