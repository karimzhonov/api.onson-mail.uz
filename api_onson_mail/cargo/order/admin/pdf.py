import os

from contrib.pdf import generate_pdf
from contrib.qrcode import generate_qrcode

def generate_invoices(orders):
    orders_html = [_generate_invoice_html(order) for order in orders]
    orders_html = [f"<tr>{''.join(orders_html[i: i+2] 
                                  if len(orders_html[i: i+2]) == 2 
                                  else [*orders_html[i: i+2], '<td></td>'])}</tr>"
                   for i in range(0, len(orders_html), 2)]
    html = f"""
    <html>
    <body style="width: 100px">
    <table width="100%" border="1" cellspacing="0" cellpadding="5">
        {''.join(orders_html)}
    </table>
    </body>
    </html>
    """
    return generate_pdf(html)


def _generate_invoice_html(order):
    qrcode = generate_qrcode(order.id)
    return f"""
    <td>
        <h1>Track number: {order.number}</h1>
        <h1>Name: {order.name}</h1>
        <h1>FIO: {order.client.fio}</h1>
        <h1>PINFL: {order.client.pnfl}</h1>
        <h1>Passport: {order.client.passport}</h1>
        <h1>Country: {order.parts.country.name}</h1>
        <h1>Weight: {order.weight}</h1>
        <img src="data:image/png;base64,{qrcode}" style="width: 200px"/>
    </td>
    """