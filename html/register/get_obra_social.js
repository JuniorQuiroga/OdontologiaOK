// funcion que llama a la api para pedir informacion 
async function get_social(url) {
    // almacenar data de la api 
    // await = esperar a una respuesta, solo async
    const response = await fetch(url,{
                                mode: 'cors'});
    
    // convierte la informacion recibida en Json
    var data = await response.json();
    
    console.log(data);

    // genera opciones con los datos recibidos
    gen_options(data);
}

// crea las opciones para la seleccion de la obra social 
function gen_options(data){
    // recorre la informacion por clave y valor
    Object.entries(data).forEach(([key, value]) => {
        
        // crea una opcion y le asigna los valores recibidos
        var opcion = document.createElement("option");
        opcion.value = value.idObraSocial;
        opcion.text = value.nombre;

        // busca la lista de seleccion
        var element = document.getElementById("obra_social");
        
        // agrega una nueva opcion a la lista de seleccion
        element.add(opcion,null);
    });
}

// espera a que la pagina se cargue por completo
document.addEventListener('DOMContentLoaded',()=>{
    let x = document.cookie;   //leemos las cookies
    let cookies =x.split(";"); //las separamos
    let local =false;

    cookies.forEach(cookie => { //recorrer el array de cookies
        if(cookie.split("=")[0] =="local" && cookie.split("=")[1]=="true") //si esta seteado local a true
            local=true; 
    })
    if(local)
        get_social("http://localhost:5000/get_social") //usamos la cookie para correr backend local     
    else 
        get_social("http://3.15.139.183:5000/get_social") //corre con local
    // llama la api para pedir los datos  
})//conceptualmente esta mal, pero nos sirve para lo que hacemos.


