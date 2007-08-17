
inits = new Array();

function addInit(fun){
    var next = inits.length;
    inits[next] = fun;
}

function processInits(){
    for (i = 0; i < inits.length; i++){
        inits[i]();
    }
}

function getXMLHttpRequest() {
    if (window.XMLHttpRequest){
        ret = new XMLHttpRequest();
    }else if (window.ActiveXObject){
        ret = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return ret;
}

var http_request = getXMLHttpRequest();

function get_states_from_country(field, field_suffix, dep_suffix){
    var country = field.options[field.selectedIndex].value;
    var url = "@@states-ajax?country=" + country;
    http_request.open("GET", url, true);
    http_request.onreadystatechange = function(){
                                            update_callback(field.id, field_suffix, dep_suffix);
                                      };
    http_request.send(null);
}

function update_sequence(field_id, field_suffix, dep_suffix, response){
    var dep_field_id = field_id.substr(0, field_id.length - field_suffix.length) + dep_suffix;
    var dep_field = document.getElementById(dep_field_id);
    var dep_value = dep_field.options[dep_field.selectedIndex].value;

    var state_options = '';
    for (var i = 0; i < response.length; i++){
        if (dep_value == response[i][0])
            state_options += "<option value=\"" + response[i][0] + " selected=\"selected\">" + response[i][1] + "</option>\n";
        else
            state_options += "<option value=\"" + response[i][0] + "\">" + response[i][1] + "</option>\n";
    }

    dep_field.innerHTML = state_options;
}

function update_callback(field_id, field_suffix, dep_suffix){
   if (http_request.readyState == 4){
        var response = http_request.responseText;
        response = eval(response);
        update_sequence(field_id, field_suffix, dep_suffix, response);
    }
}

