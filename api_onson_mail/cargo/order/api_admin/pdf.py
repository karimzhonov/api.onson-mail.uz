import os
from contrib.pdf import generate_pdf
from contrib.qrcode import generate_qrcode
from cargo.models import User


def generate_invoices(orders):
    orders_html = [__generate_invoice_html(order) for order in orders]
    orders_html = [
        f"<tr>{''.join(orders_html[i: i + 2] if len(orders_html[i: i + 2]) == 2 else [*orders_html[i: i + 2], '<td></td>'])}</tr>"
        for i in range(0, len(orders_html), 2)]
    html = f"""
    <html>
    <head>
    <style type="text/css">
        @import url('https://github.com/justrajdeep/fonts/blob/master/Times%20New%20Roman.ttf');

        * { 
            font-family: 'Times New Roman'; 
        }
    </style>
    </head>
    <body style="width: 100px">
    {''.join(orders_html)}
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


def __generate_invoice_html(order):
    qrcode = generate_qrcode(order.id)
    phones = ", ".join(list(User.objects.filter(clients__in=[order.client]).values_list("user__phone", flat=True)))
    products = _generate_products(order.products)
    return f"""
<table width="100%" border="1" cellspacing="0" cellpadding="5">
    <tr>
        <td colspan="7">"KARGO"</td>
        <td/>
        <td colspan="7">"EXSPRES"</td>
    </tr>
    <tr>
        <td colspan="3" rowspan="6">INVOICE №</td>
        <td colspan="4" rowspan="6">{order.number}</td>
    </tr>
    <tr/>
    <tr>
        <td colspan="2">Отправител:</td>
        <td colspan="7">PARVINA</td>
        <td colspan="1">САИД</td>
        <td colspan="5" rowspan="5">{order.parts.number}</td>
    </tr>
    <tr>
        <td colspan="2">Тел. Номер отправителя:</td>
        <td colspan="7"></td>
        <td colspan="1">ТЕЛ: +905539210873</td>
    </tr>
    <tr>
        <td colspan="2"></td>
        <td colspan="7"></td>
        <td colspan="1">Офис: +905051164320</td>
    </tr>
    <tr>
        <td colspan="2">Получатель:</td>
        <td colspan="8">{order.client.fio}</td>
    </tr>
    <tr>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
    </tr>
    <tr>
        <td colspan="2">Адрес получателя:</td>
        <td colspan="8">{order.client.address}</td>
    </tr>
    <tr>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
    </tr>
    <tr>
        <td colspan="2">Паспорт получателя:</td>
        <td colspan="3">{order.client.passport}</td>
        <td colspan="5">{order.client.pnfl}</td>
    </tr>
    <tr>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
    </tr>
    <tr>
        <td colspan="2">Тел. номер получателя:</td>
        <td colspan="8">{phones}</td>
    </tr>
    <tr>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
    </tr>
    <tr>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
        <td colspan="1"></td>
    </tr>
    {products}
</table>
"""


def  _generate_products(products: dict):
    data = list(products.values())
    html = []
    for i in range(50):
        try:
            product = data[i]
        except IndexError:
            product = {}
        html.append(f"""
            <td colspan="1">{i+1 if product.get('name') else ''}</td>
            <td colspan="1">{product.get('name', '')}</td>
            <td colspan="1">{product.get('count_product', '')}</td>
            <td colspan="1"></td>
            <td colspan="1"></td>
            <td colspan="1">{product.get('price_per_product', '')}</td>
            <td colspan="1">{product.get('total_price', '')}</td>
        """)
    left = html[:25]
    right = html[25:]
    table = []
    for (l, r) in zip(left, right):
        table.append(f"""
            <tr>            
            {l}<td colspan="1"></td>{r}
            </tr>
        """)
    return "".join(table)
    

