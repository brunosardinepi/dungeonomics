$("#autonumber").on('click', function(event) {
  event.preventDefault();
  var count = 1;
  $(".autonumber-order").each(function() {
    console.log($(this).val());
    $(this).val(count);
    count++;
  });
});
