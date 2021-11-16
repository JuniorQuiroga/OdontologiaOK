function ClearOptionsAlt(FormName, SelectName)
{
    document.forms[FormName].elements[SelectName].options.length = 0;
}


// funcion que llama a la api para pedir informacion 
async function get_data(url) {
    // almacenar data de la api 
    // await = esperar a una respuesta, solo async
    const response = await fetch(url,{
                                mode: 'cors',
                                credentials: 'include',
                                headers: { 'Content-Type': 'application/json',
                                            'Authorization':token},
                        });
    
    // convierte la informacion recibida en Json
    var data = await response.json();
    
    console.log(data);

    // genera opciones con los datos recibidos
    return(data);
}

// crea las opciones para la seleccion
function gen_options(data,seleccion){
    var element = document.getElementById(seleccion);

    // recorre la informacion por clave y valor
    Object.entries(data).forEach(([key, value]) => {
        
        // crea una opcion y le asigna los valores recibidos
        var opcion = document.createElement("option");
        opcion.value = value.id; 
        opcion.text = value.nombre;

        // busca la lista de seleccion
        
        // agrega una nueva opcion a la lista de seleccion
        element.add(opcion,null);
    });
}


function campo_vacio(campo){
    // crea una opcion y le asigna los valores recibidos
    var opcion = document.createElement("option");
    opcion.value = null;
    opcion.text = "";

    var element = document.getElementById(campo);
    element.add(opcion,null);
}

// NO GENERALES -----------------------------------------------------------------------

// espera a que la pagina se cargue por completo
document.addEventListener('DOMContentLoaded',()=>{

    dni = document.getElementById("dni");
    dni.addEventListener("change",function(){
        document.getElementById('hora').value=0;
        document.getElementById("datepicker").disabled = false;
        document.getElementById("datepicker").value = "";

        $("#datepicker").datepicker({
            dateFormat: "yy-mm-dd",
            
            //desactiva los fines de semana
            beforeShowDay: $.datepicker.noWeekends, 
            minDate: 0, //minimo
            maxDate: "+6M", //maximo
    
            changeMonth: true,
            changeYear: true
        });

        $("#datepicker").on("change", function(e) {
            var fecha = document.getElementById('datepicker').value;
    
            get_data(ip+"/get_hora/"+fecha).then(
                data => gen_options(data,"hora")
            )

            document.getElementById("hora").disabled = false;
        });
    })
})