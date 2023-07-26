$('.nav-pills .nav-item .nav-link').each(function() {
  console.log(window.location.pathname.split('/')[1].split('.')[0])
  if (window.location.pathname.split('/')[1].replace('.', '-').includes($(this).attr('id')) ) {
    $(this).addClass('active');
  }
})
