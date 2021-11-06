// funcion que llama a la api para pedir informacion 
async function pedir_turnos(url) {
    // almacenar data de la api 
    // await = esperar a una respuesta, solo async
    const response = await fetch(url,{
                                mode: 'cors'});
    
    // convierte la informacion recibida en Json
    var data = await response.json();

    // genera opciones con los datos recibidos
    return data;
}



function mostrar_turnos(data){
    let tabla = 
        `<tr>
          <th>Fecha</th>
          <th>Motivo</th>
          <th>Requisitos</th>
          <th>Editar</th>
          <th>Cancelar</th>
         </tr>`;
    
    
    // recorre cada elemento de la seccion "especialidades" del Json "data" 
    for (let fila of Object(data)) {

        // agrega una nueva fila
        //con los datos recogidos en cada columna
        //<tr> = filas
        //<td> = columnas
        tabla += `<tr> 
        <td>${fila.fecha} </td>
        <td>${fila.motivo}</td>         
        <td>${fila.requisitos}</td>         
        <td>editar</td>         
        <td>cancelar</td>         
        </tr>`;
    }

}

document.addEventListener('DOMContentLoaded',()=>{
    pedir_turnos(ip+"/get_turno_paciente").then(
        data => mostrar_turnos(data)
    )

})