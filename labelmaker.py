"""
LabelMaker - A command-line utility for generating PDF labels for label printers.

This script generates PDF files formatted for Dymo and Brother P-touch label printers
with customizable text and font sizes.
"""
import argparse
from typing import Dict, List, Literal, Optional, Union
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from io import BytesIO

# Constants
FONT_NAME = "Helvetica"
FONT_SIZES: Dict[str, int] = {'S': 8, 'M': 12, 'L': 18}

# Label Types
LabelType = Literal['dymo', 'ptouch']


class Label:
    """Base class for all label types."""
    
    def __init__(self, text: str, font_size: int):
        """
        Initialize a label with text and font size.
        
        Args:
            text: Text content for the label
            font_size: Font size for the text
        """
        self.text = text
        self.font_size = font_size
        
    def generate(self, pdf: canvas.Canvas) -> None:
        """
        Generate the label on the provided canvas.
        
        Args:
            pdf: ReportLab canvas object
        """
        raise NotImplementedError("Subclasses must implement generate()")
    
    def calculate_text_width(self) -> float:
        """
        Calculate the width of text with the given font and size.
        
        Returns:
            Width of the text in points
        """
        test_pdf = BytesIO()
        test_canvas = canvas.Canvas(test_pdf)
        test_canvas.setFont(FONT_NAME, self.font_size)
        return test_canvas.stringWidth(self.text, FONT_NAME, self.font_size)
    
    @staticmethod
    def draw_text_centered(pdf: canvas.Canvas, text: str, width: float, height: float, font_size: int) -> None:
        """
        Draw text centered on the current page.
        
        Args:
            pdf: ReportLab canvas object
            text: Text content to draw
            width: Width of the page
            height: Height of the page
            font_size: Font size for the text
        """
        pdf.setFont(FONT_NAME, font_size)
        text_width = pdf.stringWidth(text, FONT_NAME, font_size)
        x = (width - text_width) / 2
        y = (height - font_size) / 2
        pdf.drawString(x, y, text)
        pdf.showPage()


class DymoLabel(Label):
    """Label type for Dymo label printers."""
    
    WIDTH = 153
    HEIGHT = 72
    
    def generate(self, pdf: canvas.Canvas) -> None:
        """
        Generate a label specifically formatted for Dymo label printers.
        
        Args:
            pdf: ReportLab canvas object
        """
        width, height = landscape((self.WIDTH, self.HEIGHT))
        pdf.setPageSize((width, height))
        self.draw_text_centered(pdf, self.text, width, height, self.font_size)


class PTouchLabel(Label):
    """Label type for Brother P-touch label printers."""
    
    HEIGHT = 12 * mm
    PADDING = 10
    
    def generate(self, pdf: canvas.Canvas) -> None:
        """
        Generate a label specifically formatted for Brother P-touch label printers.
        
        Args:
            pdf: ReportLab canvas object
        """
        text_width = self.calculate_text_width() + self.PADDING
        width = text_width
        pdf.setPageSize((width, self.HEIGHT))
        self.draw_text_centered(pdf, self.text, width, self.HEIGHT, self.font_size)


class LabelMaker:
    """Main class for creating and managing label generation."""
    
    def __init__(self, output_file: str = 'labels.pdf'):
        """
        Initialize LabelMaker with output file.
        
        Args:
            output_file: Path to save the generated PDF file
        """
        self.output_file = output_file
        self.pdf = canvas.Canvas(output_file)
        self.labels: List[Label] = []
    
    def add_label(self, label_type: LabelType, text: str, font_size: int) -> None:
        """
        Add a label to be generated.
        
        Args:
            label_type: Type of label ('dymo' or 'ptouch')
            text: Text content for the label
            font_size: Font size for the text
        """
        if label_type == 'dymo':
            label = DymoLabel(text, font_size)
        else:
            label = PTouchLabel(text, font_size)
        self.labels.append(label)
    
    def generate_pdf(self) -> None:
        """Generate PDF file with all added labels."""
        for label in self.labels:
            label.generate(self.pdf)
        self.pdf.save()
        print(f"PDF with {len(self.labels)} labels generated: {self.output_file}")


def main() -> None:
    """Parse command-line arguments and generate label PDFs."""
    parser = argparse.ArgumentParser(description='Generate PDF labels for printers.')
    parser.add_argument('printer', choices=['dymo', 'ptouch'], help='Specify the printer type.')
    parser.add_argument('labels', nargs='+', help='Labels to print.')
    parser.add_argument('--size', choices=['S', 'M', 'L'], default='M', help='Font size: S, M, L.')
    parser.add_argument('--output', default='labels.pdf', help='Output PDF filename.')
    args = parser.parse_args()

    font_size = FONT_SIZES[args.size.upper()]
    label_maker = LabelMaker(args.output)
    
    for label_text in args.labels:
        label_maker.add_label(args.printer, label_text, font_size)
    
    label_maker.generate_pdf()


if __name__ == '__main__':
    main()