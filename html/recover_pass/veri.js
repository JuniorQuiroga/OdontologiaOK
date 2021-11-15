async function post(url){
    const postData = document.getElementById("form");
    //agarra data de los inputs y los convierte en JSON para enviarlos con fetch en forma de post
    postData.addEventListener('submit',async function(e){
        e.preventDefault();
        const response = await fetch(url,{
            mode: 'cors',
            method: 'PUT'});
        
        // toma los datos de las entradas del formulario y las conviete en JSON
        
        // espera por la respuesta del servidor
        const result = await response.json();
        console.log(result);
        alert("Se cambio bien");
    });
}
document.addEventListener('DOMContentLoaded',()=>{
    const postData = document.getElementById("form");
    //agarra data de los inputs y los convierte en JSON para enviarlos con fetch en forma de post
    postData.addEventListener('submit',async function(e){
        e.preventDefault();
        var contra1= document.getElementById("contrasenia").value;
        var contra2= document.getElementById("contrasenia2").value;
        
        if(contra1==contra2){
            if(document.getElementById("codigo").value==get_cookie("mail").split(",")[1]){
                //const formData = new FormData(postData).entries()
                //const jsonForm = JSON.stringify(Object.fromEntries(formData))
                post(ip+"/cambiar/"+get_cookie("mail").split(",")[0]+"_"+contra1)
                
                // construye una peticion con el metodo POST y envia el JSON generado como cuerpo
            }
            else{
                alert("Codigo incorrecto");
            }
        }
        else{
            alert("Las contrasenias no coinciden");
        }
        }
    )
}
)
