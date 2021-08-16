$("#autonumber").on('click', function(event) {
  event.preventDefault();
  var count = 1;
  $(".autonumber-order").each(function() {
    $(this).val(count);
    count++;
  });
});
