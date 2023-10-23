(function(){

    const biEditar= document.querySelectorAll(".biEditar")

    biEditar.forEach(i =>{
        i.addEventListener("click", (e)=>{
            const confirmacion=confirm('¿Seguro/a que quieres editar la contraseña?');
            if(!confirmacion){
                e.preventDefault();
            }
        });
    });
    
})();