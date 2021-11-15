function get_cookie(nombre){
    var x = document.cookie;   //leemos las cookies
    var cookies =x.split(";"); //las separamos
    
    for(var i=0;i<cookies.length;i++){
        if(cookies[i].split("=")[0]==nombre){
            return cookies[i].split("=")[1];
        }
    }

    /*
    var galle = null;
    
    cookies.forEach(galletita => { //recorrer el array de cookies
        if(galletita.split("=")[0] == nombre) //si esta seteado local a true
        galle = galletita.split("=")[1];
        console.log(galletita.split("=")[1])
        return galletita.split("=")[1];
    })
    */
}