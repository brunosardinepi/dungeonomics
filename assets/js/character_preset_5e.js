var presetOptions = {
    addButtonID: 'add-button',
    addClass: 'add-row', // name of the class that has the add button
    formPrefix: 'attribute_set',
    rowClass: 'formset-row', // name of the div for each form in formset
};

function createPresetRowHTML(formPrefix, attribute) {
    // create the html for a new form row
    var formsetName = formPrefix + '-' + totalForms + '-name';
    var formsetID = formPrefix + '-' + totalForms + '-id';
    var formsetValue = formPrefix + '-' + totalForms + '-value';

    var formRowTemplate = '<div class="form-row formset-row" id="row-' + totalForms + '">';
    formRowTemplate += '<div class="form-group col-lg-4">';
    formRowTemplate += '<label for="' + formsetName + '">Attribute name</label>';
    formRowTemplate += '<input type="hidden" name="' + formsetID + '" id="' + formsetID + '">';
    formRowTemplate += '<input type="text" name="' + formsetName + '" value="' + attribute + '" class="form-control ui-autocomplete-input" maxlength="255" id="id_' + formsetName + '" autocomplete="off">';
    formRowTemplate += '</div>';
    formRowTemplate += '<div class="form-group col-lg-7">';
    formRowTemplate += '<label for="id_' + formsetValue + '">Value</label>';
    formRowTemplate += '<input type="text" name="' + formsetValue + '" class="form-control" maxlength="255" id="id_' + formsetValue + '">';
    formRowTemplate += '</div>';
    formRowTemplate += '<div class="form-group col-lg-1 col-delete align-self-end text-right ' + presetOptions.addClass + '" id="col-delete-' + totalForms + '">';
    formRowTemplate += '<a href="" id="delete-' + totalForms + '">';
    formRowTemplate += deleteButtonHTML;
    formRowTemplate += '</a>'
    formRowTemplate += '</div>';
    formRowTemplate += '</div>';

    return formRowTemplate;
}

$(document).on("click", "#character-preset-5e", function(event) {
    event.preventDefault();

    // add the d&d 5e fields to the end of the formset
    attributes.sort();
    $.each(attributes, function(index, value){
        var formRowTemplate = createPresetRowHTML(presetOptions.formPrefix, value);
        $(".formset-row").last().after(formRowTemplate);

        // attach autocomplete to the new form's "name" input
        $(".formset-row").last().find("[id^=id_attribute_set]").autocomplete({
            source: suggestedAttributes,
        });

        // update the total-forms value
        totalForms++;
        updateTotalForms();
    });

    // remove the add button from where it is
    deleteAddButton();

    // and add it to the new end row
    createAddButton();

    // add to notes field
    var notes = "<p><strong>Bonds</strong></p><p>None</p>";
    notes += "<p><strong>Flaws</strong></p><p>None</p>";
    notes += "<p><strong>Ideals</strong></p><p>None</p>";
    notes += "<p><strong>Personality</strong></p><p>None</p>";
//    notes += "<p><strong></strong></p><p>None</p>";
    notes += "<hr><h3>Equipment</h3><p>None</p>";
    notes += "<hr><h3>Feats</h3><p>None</p>";
    notes += "<hr><h3>Proficiences</h3><p>None</p>";
    notes += "<hr><h3>Skills</h3><p>None</p>";
    notes += "<hr><h3>Spells</h3><p>None</p>";
//    notes += "<h3></h3><p>None</p>";
    tinyMCE.get("id_notes").setContent(notes);
});
