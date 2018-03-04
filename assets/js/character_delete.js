$(document).on('click', '#player-delete', function() {
    return confirm("Are you sure you want to delete this player? It will be gone forever!")
});

$(document).on('click', '#monster-delete', function() {
    return confirm("Are you sure you want to delete this monster? It will be gone forever!")
});

$(document).on('click', '#npc-delete', function() {
    return confirm("Are you sure you want to delete this NPC? It will be gone forever!")
});