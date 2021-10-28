

// Standard javascript function to clear all the options in an HTML select element
// In this method, you just provide the form name and dropdown box name
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
    select.addEventListener('change',
    
    // llama a la api y pide los doctores que coincidan con la especialidad
    function(){
        ClearOptionsAlt("form","medico");
        campo_vacio("medico")
        // guarda la id de la opcion seleccionada 
        var selectedOption = this.options[select.selectedIndex];
        
        // llamamos a la api pasando como codigo la id de especilidad seleccionada
        // devuelve id y nombres de los medicos de la especialidad seleccionada
        get_data(ip+"/get_medico/"+selectedOption.value+"").then(
            data => gen_options(data,"medico")
            )
            //genera opciones para medico segun lo recibido
        });
    }
    
    
    
    function anio(){
        var fecha = new Date();
        var anio = fecha.getFullYear();
        
        ClearOptionsAlt("form","anio");
        campo_vacio("anio")
        
        // crea las opciones de año
        for(var i= 0;i<2;i++){
            // crea una opcion y le asigna los valores recibidos
            var opcion = document.createElement("option");
            opcion.value = anio+i;
            opcion.text = anio+i;
            
            // busca la lista de seleccion
            var element = document.getElementById("anio");
            
            // agrega una nueva opcion a la lista de seleccion
            element.add(opcion,null);
        }
    }
    
    function mes(){
        var fecha = new Date();
        var mes = fecha.getMonth();
        
        
        // agarra el select de año
        var select = document.getElementById('anio');
        
        // agrega un listener de cambio -> cuando el valor cambia ejecuta la funcion
        select.addEventListener('change',
        
        // genera las opciones dependiendo del año anteriormente elegido
        function(){
            //limpia la lista
            ClearOptionsAlt("form","mes");
            
            // guarda el año de la opcion seleccionada 
            var anio = this.options[select.selectedIndex];
            
            campo_vacio("mes")
            //si el año es el actual genera los meses desde el actual al fin de año
            if(anio.value == fecha.getFullYear()){
                for(var i=mes+1; i<13 ;i++){
                    var opcion = document.createElement("option");
                    opcion.value = i;
                    opcion.text = i;
                    
                    // busca la lista de seleccion
                    var element = document.getElementById("mes");
                    
                    // agrega una nueva opcion a la lista de seleccion
                    element.add(opcion,null);
                }
                
            }
            // sino genera todos los meses
            else{
                for(var i=1; i<13 ;i++){
                    var opcion = document.createElement("option");
                    opcion.value = i;
                    opcion.text = i;
                    
                    // busca la lista de seleccion
                    var element = document.getElementById("mes");
                    
                    // agrega una nueva opcion a la lista de seleccion
                    element.add(opcion,null);
                }
            }
            //genera opciones para medico segun lo recibido
        });
        
    }   
    
    function dia(){
        
        // agarra el select de mes
        var select = document.getElementById('mes');
        
        
        // agrega un listener de cambio -> cuando el valor cambia ejecuta la funcion
        select.addEventListener('change',
        
        // genera las opciones dependiendo del año anteriormente elegido
        function(){
            ClearOptionsAlt("form","dia");
            campo_vacio("dia")
            //limpia la lista
            
            // guarda el valor de año
            var anio_s = document.getElementById('anio');
            
            // guarda el año de la opcion seleccionada 
            var mes = this.options[select.selectedIndex];
            var a = anio_s.value;
            
            // si el mes es febrero tiene 28 dias, biciesto para descansos
            if(mes.value == 2){
                for(var i=1; i<29 ;i++){
                    var f = new Date(a, mes.value-1, i);
                    var d = f.toDateString();
                    
                    if(!(d.includes("Sat") || d.includes("Sun"))){
                        var opcion = document.createElement("option");
                        opcion.value = i;
                        opcion.text = i;
                        
                        // busca la lista de seleccion
                        var element = document.getElementById("dia");
                        
                        // agrega una nueva opcion a la lista de seleccion
                        element.add(opcion,null);
                    }
                }
            }
            else{
                // si el mes es uno de estos es menor a 31
                if(mes.value == 4 || mes.value == 6 || mes.value == 9 || mes.value == 11){
                    for(var i=1; i<31 ;i++){
                        
                        var f = new Date(a, mes.value-1, i);
                        var d = f.toDateString();
                        
                        if(!(d.includes("Sat") || d.includes("Sun"))){
                            var opcion = document.createElement("option");
                            opcion.value = i;
                            opcion.text = i;
                            
                            // busca la lista de seleccion
                            var element = document.getElementById("dia");
                            
                            // agrega una nueva opcion a la lista de seleccion
                            element.add(opcion,null);
                        }
                        
                    }
                }
                else{
                    for(var i=1; i<32 ;i++){
                        var f = new Date(a, mes.value-1, i);
                        var d = f.toDateString();
                        
                        if(!(d.includes("Sat") || d.includes("Sun"))){
                            var opcion = document.createElement("option");
                            opcion.value = i;
                            opcion.text = i;
                            
                            // busca la lista de seleccion
                            var element = document.getElementById("dia");
                            
                            // agrega una nueva opcion a la lista de seleccion
                            element.add(opcion,null);
                        }
                    }
                }
            }
        });
        
    }
    
    function hora(){
        var anio_s = document.getElementById('anio').value;
        var mes_s = document.getElementById('mes').value;
        var dia_s = document.getElementById('dia').value;
        
        var medico_s = document.getElementById('medico');
        var med = medico_s.options[medico_s.selectedIndex].value;
        
        ClearOptionsAlt("form","hora");
        campo_vacio("hora")
    

    var string = ""+anio_s+"-"+mes_s+"-"+dia_s+"-"+med+"";
    
    get_data(ip+"/get_hora/"+string+"").then(
        data => gen_options(data,"hora")
        )
        
        /*
        //crea una opcion por cada hora dispobile
        var opcion = document.createElement("option");
        opcion.value = hora;
        opcion.text = hora;
        
        // busca la lista de seleccion
        var element = document.getElementById("hora");
        
        // agrega una nueva opcion a la lista de seleccion
        element.add(opcion,null)    
    }
    */   
}




// espera a que la pagina se cargue por completo
document.addEventListener('DOMContentLoaded',()=>{
    campo_vacio("especialidad")
    
    get_data(ip+"/get_especialidad").then(
        data_especialidad => gen_options(data_especialidad,"especialidad")
    );

    
    get_medico()
    
    med =document.getElementById("medico")
    med.addEventListener('change',
    function gen_date(){
        anio();
        mes();
        dia();
    });
    
    d =document.getElementById("dia")
    d.addEventListener('change',
    function gen_dia(){ 
        hora() 
    });

})//conceptualmente esta mal, pero nos sirve para lo que hacemos.


