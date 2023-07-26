$('.poster-buttons button').on('click', function() {
  var target = $(this).attr('data-target');
  $(this).siblings().removeClass('active');
  if ($(target).hasClass('show')) {
    $(target).addClass('show');
  } else {
    $('.collapse.show').removeClass('show');
  }
});

$('.fullscreen-button').on('click', function() {
  fullscreen($(this).next('.fullscreen-iframe')[0])
})
// var button = document.querySelector('#fullscreen-button');
//
// button.addEventListener('click', fullscreen);
// when you are in fullscreen, ESC and F11 may not be trigger by keydown listener.
// so don't use it to detect exit fullscreen
document.addEventListener('keydown', function (e) {
  console.log('key press' + e.keyCode);
});
// detect enter or exit fullscreen mode
document.addEventListener('webkitfullscreenchange', fullscreenChange);
document.addEventListener('mozfullscreenchange', fullscreenChange);
document.addEventListener('fullscreenchange', fullscreenChange);
document.addEventListener('MSFullscreenChange', fullscreenChange);

function fullscreen(frame) {
  // check if fullscreen mode is available
  if (document.fullscreenEnabled ||
    document.webkitFullscreenEnabled ||
    document.mozFullScreenEnabled ||
    document.msFullscreenEnabled) {

    // which element will be fullscreen
    // var iframe = document.querySelector('#fullscreen-iframe');
    // Do fullscreen
    if (frame.requestFullscreen) {
      frame.requestFullscreen();
    } else if (frame.webkitRequestFullscreen) {
      frame.webkitRequestFullscreen();
    } else if (frame.mozRequestFullScreen) {
      frame.mozRequestFullScreen();
    } else if (frame.msRequestFullscreen) {
      frame.msRequestFullscreen();
    }
  }
  else {
    document.querySelector('.error').innerHTML = 'Your browser is not supported';
  }
}

function fullscreenChange() {
  if (document.fullscreenEnabled ||
       document.webkitIsFullScreen ||
       document.mozFullScreen ||
       document.msFullscreenElement) {
    console.log('enter fullscreen');
  }
  else {
    console.log('exit fullscreen');
  }
  // force to reload iframe once to prevent the iframe source didn't care about trying to resize the window
  // comment this line and you will see
  var iframe = document.querySelector('iframe');
  iframe.src = iframe.src;
}


$("#fullscreen-iframe button#presentationMode").css('display', 'none !important');

$(window).ready(function() {
  $('.poster-buttons button').first().trigger("click");
})
