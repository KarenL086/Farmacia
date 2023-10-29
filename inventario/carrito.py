class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"]={}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito
    
    def agregar(self, articulo, inventario):
        id = str(articulo.idarticulo)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "idarticulo": articulo.idarticulo,
                "nombre": articulo.nombre,
                "precio_venta": float(articulo.precio_venta),
                "acumulado": float(articulo.precio_venta),
                "cantidad": 1,
            }
        else:
            if self.carrito[id]["cantidad"] < inventario:
                self.carrito[id]["cantidad"]+=1
                self.carrito[id]["acumulado"]=float(self.carrito[id]["acumulado"])+float(articulo.precio_venta)           
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"]=self.carrito
        self.session.modified = True

    def eliminar(self, articulo):
        id = str(articulo.idarticulo)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, articulo):
        id = str(articulo.idarticulo)
        if id in self.carrito.keys():
           self.carrito[id]["cantidad"]-=1
           self.carrito[id]["acumulado"] = float(self.carrito[id]["acumulado"])-float(articulo.precio_venta)
           if self.carrito[id]["cantidad"]<=0: self.eliminar(articulo)
           self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"]={}
        self.session.modified = True 