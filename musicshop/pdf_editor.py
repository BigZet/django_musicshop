from fpdf import FPDF


def create_test_pdf():
    pdf = FPDF()
    pdf.compress = False
    pdf.add_page()
    pdf.set_font('Arial', '', 14)
    pdf.ln(10)
    pdf.write(5, 'hello world')
    pdf.output('1.pdf')