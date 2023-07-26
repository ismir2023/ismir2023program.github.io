$(document).ready(function() {
  var offset = $(':target').offset();
  var scrollto = offset.top - 150; // minus fixed header height
  $('html, body').animate({scrollTop:scrollto}, 0);
});
