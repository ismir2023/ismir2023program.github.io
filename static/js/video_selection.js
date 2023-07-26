fetch('https://youtube.com', {mode: 'no-cors'}).then(r=>{
  // YOUTUBE EMBED
  console.log('youtube is reachable');
  var embed = $('#yt-id').data()['name'];
  $('#video .video-container').append(`
    <div class="aspect-ratio yt-container">
      <iframe class="video-stream" src="https://www.youtube.com/embed/${embed}" width="560" height="315" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>

    `)
  console.log($('#yt-id').data()['name']);
  // $('.yt-container iframe').attr('src', "https://www.youtube.com/embed/" + $('#yt-id').data()['name']);

  })
  .catch(e=>{
    // BB EMBED
    console.log('youtube is not there');
    var embed = $('#bb-id').data()['name'];
    $('#video .video-container').append(`
      <div class="aspect-ratio bb-container">
        <iframe class="video-stream" src="//player.bilibili.com/player.html?bvid=${embed}&page=1" frameborder="no" framespacing="0" allowfullscreen width="550" height="281"> </iframe>
      </div>
      `)
    });
