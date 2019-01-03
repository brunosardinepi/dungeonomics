$(document).on("click", ".asset-type", function (event) {
    event.preventDefault();

    var asset_type = $(this).text();

    // empty col2
    $("#col2-contents-ul").html("");

    // remove bold font from asset types
    $("#col1-contents").find("a").removeClass("font-weight-bold");

    // set the bold font for the active asset type
    $(this).addClass("font-weight-bold");

    // get the assets with this type
    $.ajax({
        url: '/srd/assets?asset_type=' + asset_type,
        data: {},
        success: function (data) {

// not sure if i'll need this when there are hundreds of srd assets...
            // empty the col2 ul if it's a new asset type
//            if (!$("#col2-contents-ul").hasClass(asset_type)) {
//                console.log("new class");
//                $("#col2-contents-ul").removeClass();
//                $("#col2-contents-ul").addClass("contents_list " + asset_type);
//                $("#col2-contents-ul").html("");
//            } else {
//                console.log("already has this class");
//            }

            // check each li in the returned data/html
            $.each($(data).find("li"), function(key, value) {
                // get the li id and replace "add" with "remove"
                var id = $(value).attr("id").replace("add", "remove");
                // check if "remove-asset-pk" exists
                if ($("#" + id).length > 0) {
                    // this must be in col4's import list, so hide when adding to col2
                    $(value).hide();
                }

                // add the li to col2
                $("#col2-contents-ul").append(value);
            });
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

    // update the tools link
    $.ajax({
        url: '/srd/tools-update?col=3&action=add',
        data: {},
        success: function (data) {
            $("#col3-tools").html(data);

            // update col3-tools with the asset pk
            $("#col3-tools").find("a").attr("id", "col3-tools-asset-" + asset_pk);
        }
    });
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

function removeAsset(asset, asset_pk) {
    // remove the asset from col4
    asset.remove();

    // show the asset in col2
    $("#add-asset-" + asset_pk).show();

    // update the tools link
    $.ajax({
        url: '/srd/tools-update?col=3&action=remove',
        data: {},
        success: function (data) {
            $("#col3-tools").html(data);

            // update col3-tools with the asset pk
            $("#col3-tools").find("a").attr("id", "col3-tools-asset-" + asset_pk);
        }
    });
}

$(document).on("click", ".remove-asset", function (event) {
    event.preventDefault();

    var asset = $(this).parent();
    var asset_pk = asset.attr("id").split("remove-asset-")[1];

    removeAsset(asset, asset_pk);
});

$(document).on("click", ".remove-asset-from-tools > span", function (event) {
    event.preventDefault();

    var asset_pk = $(this).parents("a").attr("id").split("col3-tools-asset-")[1];
    var asset = $("#col4-contents-ul").find("#remove-asset-" + asset_pk);

    removeAsset(asset, asset_pk);
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

            // add the asset name to col3
            $("#col3-tools-dropdown").prev("span").text(asset_name);

            // show the asset stats
            $("#col3-contents").html(data);
        }
    });
});

$(document).on("click", "#select-all > span", function (event) {
    event.preventDefault();

    // find all the li in #col2-contents-ul
    $.each($("#col2-contents-ul").find("li"), function(key, value) {
        var asset = $(value);
        var asset_pk = asset.attr("id").split("add-asset-")[1];

        // add them to import list
        addAsset(asset, asset_pk);
    });
});

$(document).on("click", "#remove-all > span", function (event) {
    event.preventDefault();

    // find all the li in #col4-contents-ul
    $.each($("#col4-contents-ul").find("li"), function(key, value) {
        var asset = $(value);
        var asset_pk = asset.attr("id").split("remove-asset-")[1];

        // remove them from import list
        removeAsset(asset, asset_pk);
    });
});
