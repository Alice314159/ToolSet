
from PyPDF2 import PdfReader, PdfWriter

def process_pdf(input_pdf_path, output_pdf_path, password=None):
    # Open the input PDF
    with open(input_pdf_path, "rb") as input_file:
        # Create a PDF reader object
        reader = PdfReader(input_file)

        # If the PDF is encrypted, attempt to decrypt it
        if reader.is_encrypted:
            if password is not None:
                try:
                    reader.decrypt(password)
                except Exception as e:
                    print(f"Error decrypting PDF: {e}")
                    return
            else:
                print("PDF is encrypted. Please provide a password.")
                return

        # Create a PDF writer object
        writer = PdfWriter()

        # Loop through all the pages in the input PDF
        for page in reader.pages:
            # Add each page to the writer object
            writer.add_page(page)

        # Write the contents to a new PDF
        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)

# Example usage
input_pdf_path = "pwd.pdf"
output_pdf_path = "output.pdf"
password = "***"  # Replace with the actual password or set to None if not needed
process_pdf(input_pdf_path, output_pdf_path, password)

