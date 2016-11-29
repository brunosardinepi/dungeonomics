$('.order').sortable({
    filter: '.new',
    onEnd: function (evt) {
        var itemEl = evt.item;
        var oldIndex = evt.oldIndex;
        var newIndex = evt.newIndex;
    },
    onUpdate: function (evt) {
        $.each($(evt.item).parent().find('.item'), function(index, item) {
            $(item).find('[name$="order"]').val(index);
        });
    }
});