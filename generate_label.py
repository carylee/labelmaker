import argparse
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_label_pdf(output_filename, text):
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

def main():
    # Setup argument parser for CLI
    parser = argparse.ArgumentParser(description='Generate a PDF label with dynamic text sizing.')
    parser.add_argument('text', type=str, help='The text to print on the label.')
    parser.add_argument('--output', type=str, default='label.pdf', help='The output filename for the generated PDF.')
    
    args = parser.parse_args()
    
    # Generate the label PDF with provided text and output filename
    generate_label_pdf(args.output, args.text)
    
    print(f"PDF label generated: {args.output}")

if __name__ == '__main__':
    main()

