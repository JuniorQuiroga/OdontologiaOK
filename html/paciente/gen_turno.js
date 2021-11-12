function ClearOptionsAlt(FormName, SelectName)
{
    document.forms[FormName].elements[SelectName].options.length = 0;
}


// funcion que llama a la api para pedir informacion 
async function get_data(url) {
    // almacenar data de la api 
    // await = esperar a una respuesta, solo async
    const response = await fetch(url,{
                                mode: 'cors'});
    
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

//cuando detecta un cambio en el select al seleccionar una opcion hace algo
function get_medico() {
    // agarra el select
    var select = document.getElementById('especialidad');
    // agrega un listener de cambio -> cuando el valor cambia ejecuta la funcion
    select.addEventListener('change', function(){
        document.getElementById("medico").disabled = false
        // llama a la api y pide los doctores que coincidan con la especialidad
       
            ClearOptionsAlt("form","medico");
            campo_vacio("medico")
            // guarda la id de la opcion seleccionada 
            var selectedOption = this.options[select.selectedIndex];
            
            // llamamos a la api pasando como codigo la id de especilidad seleccionada
            // devuelve id y nombres de los medicos de la especialidad seleccionada
            get_data(ip+"/get_medico/"+selectedOption.value+"").then(
                data => 
                    gen_options(data,"medico")
                )
                //genera opciones para medico segun lo recibido
            });
    
}

// espera a que la pagina se cargue por completo
document.addEventListener('DOMContentLoaded',()=>{
    
    campo_vacio("especialidad");

    get_data(ip+"/get_especialidad").then(
        data_especialidad => gen_options(data_especialidad,"especialidad")
    );

    get_medico();
    medico = document.getElementById("medico")
    medico.addEventListener("change",function(){
        document.getElementById('hora').value=0;
        document.getElementById("datepicker").disabled = false;
        document.getElementById("datepicker").value = "";

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

        $("#datepicker").on("change", function(e) {
            var medico_s = document.getElementById('medico');
            if (medico_s.value != ""){
                var fecha = document.getElementById('datepicker');
                var med = medico_s.options[medico_s.selectedIndex].value;
        
                get_data(ip+"/get_hora/"+fecha.value+"-"+med).then(
                data => gen_options(data,"hora")
                )

                document.getElementById("hora").disabled = false;
            }else{
                alert("seleccione un medico");
            }
        });
    })
})