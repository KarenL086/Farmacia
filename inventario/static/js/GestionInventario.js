(function(){

    const biEliminacion= document.querySelectorAll(".biEliminacion")

    biEliminacion.forEach(i =>{
        i.addEventListener("click", (e)=>{
            const confirmacion=confirm('¿Estas seguro que quieres eliminar este item?');
            if(!confirmacion){
                e.preventDefault();
            }
        });
    });
    
})();



