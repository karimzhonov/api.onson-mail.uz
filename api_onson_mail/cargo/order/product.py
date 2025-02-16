import json
import random

from django.conf import settings


with open(settings.BASE_DIR / "cargo/order/jsons/products.json", "r", encoding="utf-8") as file:
    products = json.load(file)


def generate_cart(price, counts=[1]):
    total_price = 0
    product_counts = {}

    if price > 20:
        d = generate_cart(price // 2, counts=[3, 4, 5, 6, 7])
        product_counts = d.get('product_counts')
        total_price = d.get('total_price')


    # Отбираем только товары, цена которых меньше или равна общей сумме
    affordable_products = [p for p in products if p["price"] <= (price / len(counts))]
    if not affordable_products:
        return "Нет товаров, подходящих по цене."
    
   
    
    while total_price < price:
        product = random.choice(affordable_products)
        if total_price + product["price"] <= price:
            count = random.choice(counts)
            total_price += product["price"] * count
            if product["name"] in product_counts:
                product_counts[product["name"]]["count_product"] += count
                product_counts[product["name"]]["total_price"] += product["price"] * count
            else:
                product_counts[product["name"]] = {
                    "product": product["name"],
                    "count_product": count,
                    "price_per_product": product["price"],
                    "total_price": product["price"] * count
                }
    
    return {"product_counts": product_counts, "total_price": total_price}
