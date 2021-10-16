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
    // llama la api para pedir los datos
    get_social("http://192.168.1.107:5000/get_social")
})