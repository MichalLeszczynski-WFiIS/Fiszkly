$(document).ready(function() {
    console.log("ready")
    $("#toggle-category").click(function() {
        console.log($("#category").attr("disabled"))
        $("#category").prop("disabled", function(index, value) { return !value;})
    });
});