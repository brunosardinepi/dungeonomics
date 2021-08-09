$("#autonumber-chapters").on('click', function(event) {
  event.preventDefault();
  console.log("hello");
  var count = 1;
  $(".chapter-order").each(function() {
    console.log($(this).val());
    $(this).val(count);
    count++;
  });
});
