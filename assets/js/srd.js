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

$(document).on("click", ".add-asset", function (event) {
    // prevent the click
    event.preventDefault();

    // get the asset
    var asset = $(this).parent();

    // store the asset's pk
    var asset_pk = asset.attr("id").split("add-asset-")[1];

    // clone the asset for use in col4
    var new_asset = asset.clone();

    // hide the asset in col2
    asset.hide();

    // find the child 'a' element
    var icon = new_asset.find("a").first();

    // replace the plus icon with a minus icon
    icon.html('<i class="fas fa-fw fa-lg fa-minus-square"></i>');

    // change from "add-asset" class to "remove-asset" class
    icon.addClass("remove-asset");
    icon.removeClass("add-asset");

    // replace the id on the asset clone
    new_asset.attr("id", "remove-asset-" + asset_pk);

    // add the asset to col4
    $("#col4-contents-ul").append(new_asset);
});

$(document).on("click", ".remove-asset", function (event) {
    // prevent the click
    event.preventDefault();

    // get the asset
    var asset = $(this).parent();

    // store the asset's pk
    var asset_pk = asset.attr("id").split("remove-asset-")[1];

    // remove the asset from col4
    asset.remove();

    // show the asset in col2
    $("#add-asset-" + asset_pk).show();
});
