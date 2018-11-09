var options = {
    addButtonID: 'add-button',
    addClass: 'add-row', // name of the class that has the add button
    formPrefix: 'attribute_set',
    rowClass: 'formset-row', // name of the div for each form in formset
};

var totalForms = parseInt($('#id_' + options.formPrefix + '-TOTAL_FORMS').val());
var initialForms = $('#id_' + options.formPrefix + '-INITIAL_FORMS').val();
var minNumForms = $('#id_' + options.formPrefix + '-MIN_NUM_FORMS').val();
var maxNumForms = $('#id_' + options.formPrefix + '-MAX_NUM_FORMS').val();

var deleteButtonHTML = '<span class="fa-stack" style="vertical-align: top;"><i class="fas fa-square fa-stack-2x text-danger"></i><i class="far fa-trash-alt fa-stack-1x fa-inverse"></i></span>';
var addButtonHTML = '<span class="fa-stack" style="vertical-align: top;"><i class="fas fa-square fa-stack-2x text-success"></i><i class="far fa-plus fa-stack-1x fa-inverse"></i></span>';

function createRowHTML(formPrefix) {
    // create the html for a new form row
    var formsetName = formPrefix + '-' + totalForms + '-name';
    var formsetID = formPrefix + '-' + totalForms + '-id';
    var formsetValue = formPrefix + '-' + totalForms + '-value';

    var formRowTemplate = '<div class="form-row formset-row" id="row-' + totalForms + '">';
    formRowTemplate += '<div class="form-group col-lg-4">';
    formRowTemplate += '<label for="' + formsetName + '">Attribute name</label>';
    formRowTemplate += '<input type="hidden" name="' + formsetID + '" id="' + formsetID + '">';
    formRowTemplate += '<input type="text" name="' + formsetName + '" class="form-control ui-autocomplete-input" maxlength="255" id="id_' + formsetName + '" autocomplete="off">';
    formRowTemplate += '</div>';
    formRowTemplate += '<div class="form-group col-lg-7">';
    formRowTemplate += '<label for="id_' + formsetValue + '">Value</label>';
    formRowTemplate += '<input type="text" name="' + formsetValue + '" class="form-control" maxlength="255" id="id_' + formsetValue + '">';
    formRowTemplate += '</div>';
    formRowTemplate += '<div class="form-group col-lg-1 col-delete align-self-end text-right ' + options.addClass + '" id="col-delete-' + totalForms + '">';
    formRowTemplate += '<a href="" id="delete-' + totalForms + '">';
    formRowTemplate += deleteButtonHTML;
    formRowTemplate += '</a>'
    formRowTemplate += '</div>';
    formRowTemplate += '</div>';

    return formRowTemplate;
}

function updateTotalForms() {
    // <input type="hidden" name="tableoption_set-TOTAL_FORMS" value="4" id="id_tableoption_set-TOTAL_FORMS">
    $('#id_' + options.formPrefix + '-TOTAL_FORMS').val(totalForms);
}

function createAddButton() {
    // find the last row of the formset and add the "add" button
    var html = '<a href="" id="' + options.addButtonID + '">';
    html += addButtonHTML;
    html += '</a>';
    $(".formset-row").last().find("." + options.addClass).append(html);
}

function createDeleteButton() {
    // add a delete button to all existing rows
    for (i = 0; i < totalForms; i++) {
        var html = '<a href="" id="delete-' + i + '">';
        html += deleteButtonHTML;
        html += '</a>';
        $("#col-delete-" + i).append(html);
    }
}

function deleteAddButton() {
    $("#" + options.addButtonID).remove();
}

function hideRow(counter) {
    $("#row-" + counter).hide();
}

// remove all checkboxes from default formset
$('input:checkbox').hide();

createDeleteButton();
createAddButton();

$(document).on("click", "#add-button", function(event) {
    event.preventDefault();

    // add a new form for the formset
    var formRowTemplate = createRowHTML(options.formPrefix);
    $(".formset-row").last().after(formRowTemplate);

    // attach autocomplete to the new form's "name" input
    $(".formset-row").last().find("[id^=id_attribute_set]").autocomplete({
        source: suggestedAttributes,
    });

    // update the total-forms value
    totalForms++;
    updateTotalForms();

    // remove the add button from where it is
    deleteAddButton();

    // and add it to the new end row
    createAddButton();
});

$(document).on("click", "[id^=delete-]", function(event) {
    event.preventDefault();

    // find the id number
    var counter = $(this).attr('id').split("delete-")[1];

    // hide the row with the corresponding id number
    hideRow(counter);

    // check the "delete" checkbox
    $('#id_' + options.formPrefix + '-' + counter + '-DELETE').prop('checked', true);

    // remove the add button from where it is
    deleteAddButton();

    // and add it to the new end row
    createAddButton();
});
