$(document).on("click", ".asset-type", function (event) {
    // prevent the click
    event.preventDefault();

    // get the asset type
    var asset_type = $(this).text();

    // get the assets with this type
    $.ajax({
        url: '/characters/srd/assets?asset_type=' + asset_type,
        data: {},
        success: function (data) {
            $("#col2-contents").html(data);
        }
    });

});
