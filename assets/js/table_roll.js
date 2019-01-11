$(document).on('click', '[id^="roll-button-"]', function(event) {
    event.preventDefault();

    var table_pk = $(this).attr("id").split("roll-button-")[1];

    $.ajax({
        url: '/tables/roll/',
        data: {
            'pk': table_pk,
        },
        dataType: 'json',
        success: function(data){
            var highlightClass = "list-group-item-success";
            // clear any previous rolls and wait 500 ms
            $("li[class^='option-']").removeClass(highlightClass).delay(500).queue(function(next){
                // set new roll class
                $(".option-" + data.pk).addClass(highlightClass);
                next();
            });
        }
    });
});
