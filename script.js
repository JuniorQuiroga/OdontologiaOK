//const url = "http://3.15.139.183:5000/especialidades/";
const url = "http://192.168.1.107:5000/especialidades/";




//const url = "https://employeedetails.free.beeceptor.com/my/api/path";

//funcion asincronica que obtiene la info de la api y la muestra por consola
async function getapi(url) {
    // almacenar data de la api 
    // await = esperar a una respuesta, solo async
    const response = await fetch(url,{
                                mode: 'cors'});
    
    // convierte la info en Json
    var data = await response.json();

    //muestra la data por consola
    console.log(data);
    
    if (response) {
        hideloader();
    }
    show(data);
}


//llama a la funcion para recibir los datos de especialidades de la base de datos
getapi(url);

//algo que hace como una pantalla de carga creo
function hideloader() {
    document.getElementById('loading').style.display = 'none';
}

// define la estructura de la tabla
function show(data) {
    let tab = 
        `<tr>
          <th>idEspecialidad</th>
          <th>nombre</th>
         </tr>`;
    
    console.log(data.especialidades);
    
    // recorre cada elemento de la seccion "especialidades" del Json "data" 
    for (let r of Object(data.especialidades)) {

        // agrega una nueva fila
        //con los datos recogidos en cada columna
        //<tr> = filas
        //<td> = columnas
        tab += `<tr> 
        <td>${r.idEspecialidad} </td>
        <td>${r.nombre}</td>         
        </tr>`;
    }

    // Setting innerHTML as tab variable
    document.getElementById("especialidades").innerHTML = tab;
}