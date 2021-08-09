document.getElementById('sidebar-collapse-button').addEventListener('click', function(event){
  event.preventDefault()
  var sidebar = document.getElementById('sidebar-collapse');
  if (sidebar.classList.contains('d-none')) {
    sidebar.classList.remove('d-none');
    sidebar.classList.add('show');
  } else {
    sidebar.classList.remove('show');
    sidebar.classList.add('d-none');
  };
});

