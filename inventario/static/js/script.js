function agregar_producto(idarticulo){
    $.ajax({
        url: "/agregar/" + idarticulo,
        method: "get",
        dataType: "json",
        success: function(response){
            console.log(response);
            $("#tabla_car").html(response.nuevo_html_de_tabla);
        },
        error: function(error){
            console.log(error);}
    })
}

$(document).ready(function(){
});

$('.agregar-producto').click(function() {
    var idarticulo = $(this).data('idarticulo');
    agregar_producto(idarticulo);
});