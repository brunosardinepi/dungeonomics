$(document).on('click', '#world-delete', function() {
    return confirm("Are you sure you want to delete this world? It, and all its locations, will be gone forever!")
});

$(document).on('click', '#location-delete', function() {
    return confirm("Are you sure you want to delete this location? It will be gone forever!")
});