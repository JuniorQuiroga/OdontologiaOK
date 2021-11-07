// funcion que llama a la api para pedir informacion 
async function pedir_turnos(url) {
    // almacenar data de la api 
    // await = esperar a una respuesta, solo async
    const response = await fetch(url,{
        mode: 'cors',
        method: 'get',
        credentials: 'include',
        headers: {  'Content-Type': 'application/json',
                    'Autorization':get_cookie("token")
                }
        });
    
    // convierte la informacion recibida en Json
    var data = await response.json();
    
    console.log(data)
    // genera opciones con los datos recibidos
    return data;
}

async function cancelar_turno(event){
    console.log(event.parentNode.parentNode.id);
    fila = document.getElementById(event.parentNode.parentNode.id);
    fecha = fila.cells[0].textContent.split(" ");
    
    var string = fecha[0]+"-"+fecha[1]+"-"+fecha[2]+";"+fecha[3]

    const response = await fetch(ip+"/cancelar_turno_paciente/"+string,{
        mode: 'cors',
        method: 'delete',
        credentials: 'include',
        headers:{'Content-Type': 'application/json',
        'Autorization':get_cookie("token")
            }
        }
    );
    if (response != null){
        window.location.replace("./paciente.html");
    }
};
    /*
    var rowId = e.target.parentNode.parentNode.id;
    //this gives id of tr whose button was clicked
    var dat = document.getElementById(rowId).querySelectorAll(".row-data"); 
    /*returns array of all elements with 
    console.log(rowId+" "+dat);
    
    var name = dat[0].innerHTML;
    var age = dat[1].innerHTML;
    
});

var data = await response.json();
console.log(data)

   "row-data" class within the row with given id
*/


function mostrar_turnos(data){
    let tabla = 
        `<tr>
          <th>Fecha</th>
          <th>Motivo</th>
          <th>Requisitos</th>
          <th>Editar</th>
          <th>Cancelar</th>
         </tr>`;
    
    var i=0
    // recorre cada elemento de la seccion "especialidades" del Json "data" 
    for (let fila of Object(data)) {
        fecha = new Date(fila.fecha)
        
        tabla+=`<tr id="${i}">
                    <td>${fecha.getDay()} ${fecha.getMonth()} ${fecha.getFullYear()} ${fecha.getHours()}:${fecha.getMinutes()}</td>
                    <td>${fila.motivo}</td>
                    <td>${fila.requisitos}</td>
                    <td>editar</td>         
                    <td>
                        <input type="button" value="cancelar" onclick="cancelar_turno(this)"/>
                    </td>         
                </tr>`;
        i+=1
        }

    document.getElementById("turnos").innerHTML = tabla;
}

document.addEventListener('DOMContentLoaded',()=>{
    pedir_turnos(ip+"/get_turno_paciente").then(
        data => mostrar_turnos(data)
    )

})