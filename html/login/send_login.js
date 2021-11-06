
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
            credentials: 'include',
            headers: { 'Content-Type': 'application/json',
                        'Autorization':get_cookie("token")},
            body: jsonForm
        });
        
        // espera por la respuesta del servidor
        const respuesta = await response.json();
        if (respuesta['loged']==true){
            //document.cookie = response.headers["set-cookie"]
            if(respuesta['paciente']==true)
                window.location.replace("../paciente/paciente.html");
            else
                window.location.replace("../medico/medico.html");
        }
        else{
            window.location.replace("./login.html");
        }


        console.log(result);
    });
}

// espera a que la pagina se cargue por completo
document.addEventListener('DOMContentLoaded',()=>{
    post(ip+"/login")
})