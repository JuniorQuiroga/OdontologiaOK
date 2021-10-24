async function post(postURL){
    // agarra el formulario y lo guarda en una variable
    const postData = document.getElementById("form");
    //agarra data de los inputs y los convierte en JSON para enviarlos con fetch en forma de post
    postData.addEventListener('submit',async function(e){
        e.preventDefault();
        
        // toma los datos de las entradas del formulario y las conviete en JSON
        const formData = new FormData(postData).entries()
        const jsonForm = JSON.stringify(Object.fromEntries(formData))
        
        // construye una peticion con el metodo POST y envia el JSON generado como cuerpo
        const response = await fetch(postURL,{
            mode: 'cors',
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: jsonForm
        });
        
        // espera por la respuesta del servidor
        const result = await response.json();
        if (result['loged']==true)
            window.location.replace("./logueadoPaciente.html");

        console.log(result);
    });
}

// espera a que la pagina se cargue por completo
document.addEventListener('DOMContentLoaded',()=>{
    /*
    let x = document.cookie;   //leemos las cookies
    let cookies =x.split(";"); //las separamos
    let local =false;

    cookies.forEach(cookie => { //recorrer el array de cookies
        if(cookie.split("=")[0] =="local" && cookie.split("=")[1]=="true") //si esta seteado local a true
            local=true; 
    })
    if(local)
    else 
    post("http://3.15.139.183:5000/login") //corre con local
    */
    post("http://localhost:5000/login") //usamos la cookie para correr backend local     
    })