import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter

def extract_page_number(page):
    # Define the coordinates of the bottom right corner
    x0, y0, x1, y1 = page.rect.width - 100, page.rect.height - 50, page.rect.width, page.rect.height
    # Extract text from this area
    page_number_text = page.get_text("text", clip=fitz.Rect(x0, y0, x1, y1))
    return page_number_text.strip()

def find_last_matching_page(pdf_path):
    document = fitz.open(pdf_path)
    last_page_index = []
    last_pagenumber = " "
    for i in range(len(document)):
        page = document.load_page(i)
        page_number = extract_page_number(page)
        print("page_number = ",page_number)
        if last_pagenumber == " ":
            last_pagenumber = page_number

        if page_number != last_pagenumber:
            last_page_index.append(i-1)
        last_pagenumber = page_number
    last_page_index.append(i)
    document.close()
    print("last_page_index = ",last_page_index)
    return last_page_index

def save_page_as_pdf(pdf_path, page_index, output_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for i in page_index:
        print("add pages ",i)
        writer.add_page(reader.pages[i])

    with open(output_path, 'wb') as outfile:
        writer.write(outfile)

# Example usage
pdf_path = 'F:\\00_Course\\RL\\RL_lecture\\L16-17-SAC-TD3.pdf'
last_matching_index = find_last_matching_page(pdf_path)

if last_matching_index is not None:
    output_path = 'F:\\00_Course\\RL\\RL_lecture\\L16-17-print.pdf'
    save_page_as_pdf(pdf_path, last_matching_index, output_path)
    print(f"Page saved: {output_path}")
else:
    print("No matching page found.")

