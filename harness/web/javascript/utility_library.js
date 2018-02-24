"use-strict";
/*
Generic utility methods used for development.
*/

utility_library = {}

utility_library.alert_object = function(o){
    /* Used to print all the key: value properties
    of an object (non recursive) as an alert.
    */
    var template_string = "";
    _.forEach(o, function(value, key){
        template_string += key;
        template_string += ": ";
        template_string += value;
        template_string += "\n";
    });
    alert(template_string);
};
