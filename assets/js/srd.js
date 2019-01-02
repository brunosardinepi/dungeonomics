$(document).on("click", ".asset-type", function (event) {
    event.preventDefault();

    var asset_type = $(this).text();

    // get the assets with this type
    $.ajax({
        url: '/srd/assets?asset_type=' + asset_type,
        data: {},
        success: function (data) {
            $("#col2-contents").html(data);
        }
    });
});

function addAsset(asset, asset_pk) {
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
}

$(document).on("click", ".add-asset", function (event) {
    event.preventDefault();

    var asset = $(this).parent();
    var asset_pk = asset.attr("id").split("add-asset-")[1];

    addAsset(asset, asset_pk);
});

$(document).on("click", ".add-asset-from-tools > span", function (event) {
    event.preventDefault();

    var asset_pk = $(this).parents("a").attr("id").split("col3-tools-asset-")[1];
    var asset = $("#col2-contents-ul").find("#add-asset-" + asset_pk);

    addAsset(asset, asset_pk);
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

$(document).on("click", ".asset", function (event) {
    event.preventDefault();

    var id = $(this).attr("id");
    var asset_type = id.split("-")[0];
    var asset_pk = id.split("-")[1];
    var asset_name = $(this).find("span").text();

    $.ajax({
        url: '/srd/asset?asset_type=' + asset_type + '&pk=' + asset_pk,
        data: {},
        success: function (data) {
            // update col3-tools with the asset pk
            $("#col3-tools").find("a").attr("id", "col3-tools-asset-" + asset_pk);

            // add the asset name to the character stats
            $("#col3-tools-dropdown").prev("span").text(asset_name);

            // show the character stats
            $("#col3-contents").html(data);
        }
    });
});
