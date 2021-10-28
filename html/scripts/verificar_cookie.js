// espera a que la pagina se cargue por completo
function get_cookie(nombre){
    let x = document.cookie;   //leemos las cookies
    let cookies =x.split(";"); //las separamos
    
    let galle = null;

    cookies.forEach(galletita => { //recorrer el array de cookies
        console.log(galletita)
        if(galletita.split("=")[0] ==nombre) //si esta seteado local a true
            galle = galletita.split("=")[1];
    })
    return galle;
}
// null => login
// 

function x(){
    token = get_cookie("token")
    if(token == null){
        window.location.replace("/login/login.html")
    }
    else{
        const response = fetch("http://3.15.139.183:5000/sarasa",{
            headers: {
                'Autorization':token}
            }
            );
        
        // convierte la informacion recibida en Json
        var data = response.json();
    
    
        // genera opciones con los datos recibidos
        return(data);
    }
}