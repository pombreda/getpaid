function update_sequence(field, field_suffix, dep_suffix){
    var dep_field_id = field.id.substr(0, field_suffix.length) + dep_suffix;
    var dep_field = document.getElementById(dep_field_id);

    alert(dep_field);
}
