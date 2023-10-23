
def total_carrito(request):
    total = 0.00
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                total += float(value["acumulado"])
                total = round(total, 2)
    return {"total_carrito": total}