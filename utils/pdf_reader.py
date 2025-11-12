
from pypdf import PdfReader

reader = PdfReader("grok_report.pdf")
number_of_pages = len(reader.pages)

page = reader.pages[0]
print(page)
text = page.extract_text()
print(text)

