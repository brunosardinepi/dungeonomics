$("[id$='-search']").on("input", function() {
  const search = $(this).val().toLowerCase();
  const type = $(this).attr("data-type");
  $(`#${type}-list`).find('li > a').each(function() {
    const name = $(this).text().toString().toLowerCase();
//    if (name.is(`:contains(${search})`)) {
    if (name.indexOf(search) >= 0) {
      $(this).parent('li').removeClass("hidden");
    } else {
      $(this).parent('li').addClass("hidden");
    };
  });
});
