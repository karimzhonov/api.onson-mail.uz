from io import BytesIO
from xhtml2pdf import pisa
from rest_framework.exceptions import ValidationError


def generate_pdf(html):
    result = pisa.CreatePDF(html, dest=BytesIO())
    if result.err:
        raise ValidationError('Error generating PDF: %s' % result.err, 'pdf')
    return result.dest.getvalue()
