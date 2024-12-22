import os
from PIL import Image
from fpdf import FPDF

def convert_images_to_pdf(input_folder, output_file):
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(('webp', 'jpeg', 'jpg', 'png'))]
    images.sort()

    # Define PDF settings for US Letter size (8.5 x 11 inches)
    pdf = FPDF(orientation='P', unit='in', format='Letter')
    page_width, page_height = 8.5, 11  # US Letter page size in inches

    # Define margins and space between images in inches
    margin = 0.5  # 1 inch margin
    space_between_images = 0.5  # 0.5 inch between images

    # Calculate available width and height for images
    available_width = page_width - 2 * margin - space_between_images
    available_height = page_height - 2 * margin - space_between_images

    # Image size (2 images horizontally, 2 images vertically)
    img_width = available_width / 2
    img_height = available_height / 2

    for i, image_file in enumerate(images):
        # Open image
        img_path = os.path.join(input_folder, image_file)
        img = Image.open(img_path)
        
        # Convert image to RGB if it is in webp or has an alpha channel
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Calculate the position in the 2x2 grid with margin and space between images
        if i % 4 == 0:
            pdf.add_page()  # Add new page every 4 images

        col = i % 2
        row = i % 4 // 2
        x = margin + col * (img_width + space_between_images)
        y = margin + row * (img_height + space_between_images)

        # Resize image to fit in the 2x2 grid with margins
        img.thumbnail((img_width * 300, img_height * 300), Image.LANCZOS)  # Size in pixels (300 DPI for printing)
        temp_image_path = f"temp_{i}.jpg"
        img.save(temp_image_path, "JPEG")

        # Add the image to the PDF
        pdf.image(temp_image_path, x=x, y=y, w=img_width, h=img_height)
        os.remove(temp_image_path)  # Delete temporary image file

    # Output the final PDF
    pdf.output(output_file)

# Define input folder containing images and output PDF file path
input_folder = "input_folder/"
output_file = "output.pdf"

# Convert images to PDF with 4 images per page, with 1-inch page margins and 0.5-inch spacing between images on US Letter size
convert_images_to_pdf(input_folder, output_file)
