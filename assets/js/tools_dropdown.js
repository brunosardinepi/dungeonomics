$(document).on('click', '[id$="-tools-dropdown"]', function(event) {
    event.preventDefault();

    var dropdownName = $(this).attr('id').split("-")[0];
    var toolsDiv = $("#" + dropdownName + "-tools").get();
    var animationSpeed = 400;

    $(toolsDiv).slideToggle(animationSpeed);
});
