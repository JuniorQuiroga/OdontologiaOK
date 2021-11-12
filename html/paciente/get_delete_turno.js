// crea las opciones para la seleccion
function gen_options(data,seleccion){
    var element = document.getElementById(seleccion);

    // recorre la informacion por clave y valor
    Object.entries(data).forEach(([key, value]) => {
        
        var opcion = document.createElement("option");
        if(value.ocupado == "1")
            opcion.disabled = true
        // crea una opcion y le asigna los valores recibidos
        opcion.value = value.id; 
        opcion.text = value.nombre;

        // busca la lista de seleccion
        
        // agrega una nueva opcion a la lista de seleccion
        element.add(opcion,null);
    });
}

// funcion que llama a la api para pedir informacion 
async function request_api(url,metodo) {
    // almacenar data de la api 
    // await = esperar a una respuesta, solo async
    const response = await fetch(url,{
        mode: 'cors',
        method: metodo,
        credentials: 'include',
        headers: {  'Content-Type': 'application/json',
                    //'Autorization':
                    'Autorization':token
                }
        });
    
    // convierte la informacion recibida en Json
    var data = await response.json();
    
    console.log(data)
    // genera opciones con los datos recibidos
    return data;
}

function openForm(event) {
    document.getElementById("myForm").style.display = "block";
    var fila = document.getElementById(event.parentNode.parentNode.id);
    var turno = fila.cells[0].textContent;
    const postData = document.getElementById("form");
    
    $("#datepicker").on("change", function() {
        var fecha = document.getElementById('datepicker').value;
        request_api(ip+"/get_horas_modificar/"+turno+"_"+fecha).then(data => {
            gen_options(data,"hora")
        })
        document.getElementById("hora").disabled = false;
    });
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}


function mostrar_turnos(data){
    console.log(data);
    let tabla = 
        `<tr>
          <th>idTurno</th>
          <th>Fecha</th>
          <th>Motivo</th>
          <th>Requisitos</th>
          <th>Editar</th>
          <th>Cancelar</th>
         </tr>`;
    
    var i=0
    // recorre cada elemento de la seccion "especialidades" del Json "data" 
    for (let fila of Object(data)) {
        fecha = new Date(fila.fecha.slice(0,-4))
        
        tabla+=`<tr id="${i}">
                    <td>${fila.idTurno}</td>
                    <td>${fecha.getDate()} ${fecha.getMonth()+1} ${fecha.getFullYear()} ${fecha.getHours()}:${fecha.getMinutes()}</td>
                    <td>${fila.motivo}</td>
                    <td>${fila.requisitos}</td>
                    <td>
                        <input type="button" value="editar" onclick="openForm(this)"/>
                    </td>
                    <td>
                        <input type="button" value="cancelar" onclick="cancelar_turno(this)"/>
                    </td>         
                </tr>`;
        i+=1
        }
    document.getElementById("turnos").innerHTML = tabla;
}


//espera a que cargue la pagina para mostrar los turnos

document.addEventListener('DOMContentLoaded',()=>{
    $(function(){
        $("#datepicker").datepicker({
            dateFormat: "yy-mm-dd",
            
            //desactiva los fines de semana
            beforeShowDay: $.datepicker.noWeekends, 
            minDate: 0, //minimo
            maxDate: "+6M", //maximo
    
            changeMonth: true,
            changeYear: true
        });
    }
    );

    request_api(ip+"/get_turno_paciente","get").then(
        data => mostrar_turnos(data)
    )
})