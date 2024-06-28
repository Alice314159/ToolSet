from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(paths, output):
    pdf_writer = PdfWriter()

    for path in paths:
        pdf_reader = PdfReader(path)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

    with open(output, 'wb') as out:
        pdf_writer.write(out)

if __name__ == '__main__':
    # List of PDF files to merge
    paths = ["E:\\01_code\\ToolSet\\hw14.pdf", "E:\\01_code\\ToolSet\\hw15.pdf", "E:\\01_code\\ToolSet\\MEEN612_Final_Project.pdf"]
    # Output merged PDF
    output = 'merged.pdf'
    merge_pdfs(paths, output)
