import os
import sys
import fitz  # PyMuPDF
from PIL import Image
import io

def extract_images_from_pdf(pdf_path, output_folder, image_format="png"):
    """
    Extract all images from a PDF and save them in the specified folder.
    
    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Directory to save the extracted images.
        image_format (str): Image file format (e.g., 'png', 'jpg').
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found.")
        return

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Initialize image counter
    image_counter = 0

    # Extract images using PyMuPDF
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            
            # Convert to RGB if not already
            pix = fitz.Pixmap(doc, xref)
            if pix.n >= 4:  # CMYK or RGBA
                pix = fitz.Pixmap(fitz.csRGB, pix)
            
            # Save as RGB image
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            image_path = os.path.join(output_folder, f"page{page_num+1}_img{img_index+1}.{image_format}")
            image.save(image_path, format=image_format.upper())
            print(f"Saved: {image_path}")
            image_counter += 1

    if image_counter == 0:
        print("No images found in the PDF.")
    else:
        print(f"Successfully extracted {image_counter} images.")

if __name__ == "__main__":
    # Command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python extract_images.py <pdf_path> <output_folder> <image_format>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_folder = sys.argv[2]
    image_format = sys.argv[3].lower()

    # Validate image format
    if image_format not in ["png", "jpg", "jpeg", "bmp"]:
        print("Error: Unsupported image format. Supported formats: png, jpg, jpeg, bmp.")
        sys.exit(1)

    # Extract images
    extract_images_from_pdf(pdf_path, output_folder, image_format)