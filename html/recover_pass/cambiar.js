async function post(postURL){
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
        console.log(result);
       // window.location.replace("../login/login.html");
    });
}

document.addEventListener('DOMContentLoaded',()=>{
    post(ip+"/cambiar")}
    )