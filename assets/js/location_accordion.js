$(document).on('click', '[class^=world-dropdown]', function(event) {
    event.preventDefault();
    var world = $(this).attr('class');
    var world = world.split('world-dropdown-').pop();
    var location = '.world-locations-' + world;
    $(location).slideToggle('slow');
});