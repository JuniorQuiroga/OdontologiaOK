// espera a que la pagina se cargue por completo
document.addEventListener('DOMContentLoaded',()=>{
    let x = document.cookie;   //leemos las cookies
    let cookies =x.split(";"); //las separamos
    
    cookies.forEach(cookie => { //recorrer el array de cookies
        if(cookie.split("=")[0] !="uuid") //si esta seteado local a true
            window.location.replace("http://3.15.139.183/login/login.html");
    })
})