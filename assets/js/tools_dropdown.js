$(document).on('click', '[id$="-tools-dropdown"]', function(event) {
    event.preventDefault();

    if (!$(this).hasClass('rotate-cw-180') && !$(this).hasClass('rotate-ccw-180')) {
        // fresh start, rotate-cw-180
        $(this).toggleClass('rotate-cw-180');
    } else {
        // used before, so rotate-ccw-180
        $(this).toggleClass('rotate-cw-180 rotate-ccw-180');
    };

    var dropdownName = $(this).attr('id').split("-")[0];
    var toolsDiv = $("#" + dropdownName + "-tools").get();
    var animationSpeed = 500;

    $(toolsDiv).slideToggle(animationSpeed);
});
