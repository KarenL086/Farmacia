
class carrito:
    def __init__(self, request):
        self.request =request
        self.session = request.session
        carrito = self.session["carrito"]
        if not carrito:
            self.session["carrito"]={}
            self.carrito = self.session["carrito"]
        else: 
            self.carrito = carrito

    def agregar(self,articulo):
        id = str(articulo.id)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "idarticulo" : articulo.idarticulo,
                "nombre":articulo.nombre,
                "acumulado":articulo.precio_venta,
                "cantidad" :1,
            }
    
    #def guardar_carrito(self):
        
         

        