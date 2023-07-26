let allIndustry = [];
const allKeys = {
    session: [],
}
const filters = {
    session: null,
};


const updateCards = (papers) => {

    const all_mounted_cards = d3.select('.industry-cards')
      .selectAll('.myCard', openreview => openreview.uid)
      .data(papers, d => d.number)
      .join('div')
      .attr('class', 'myCard col-12 col-sm-6 col-md-4')
      .html(card_html)

    all_mounted_cards.select('.card-title')
      .on('click', function (d) {
          const iid = d.id;
          all_mounted_cards.filter(d => d.id === iid)
            .select(".checkbox-paper").classed('selected', function () {
              const new_value = true;//!d3.select(this).classed('not-selected');
              // readCard(iid, new_value);
              return new_value;
          })
      })

    all_mounted_cards.select(".checkbox-paper")
      .on('click', function (d) {
          const iid = d.id;
          const new_value = !d3.select(this).classed('selected');
          readCard(iid, new_value);
          d3.select(this).classed('selected', new_value)
      })


    lazyLoader();
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        const temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

const render = () => {
    const f_test = [];

    updateSession();

    Object.keys(filters)
      .forEach(k => {filters[k] ? f_test.push([k, filters[k]]) : null})

    console.log(f_test, filters, "--- f_test, filters");
    if (f_test.length === 0) updateCards(allIndustry)
    else {
        const fList = allIndustry.filter(
          d => {
              let i = 0, pass_test = true;
              while (i < f_test.length && pass_test) {
                  if (f_test[i][0] === 'titles') {
                      pass_test &= d.content['title'].toLowerCase()
                        .indexOf(f_test[i][1].toLowerCase()) > -1;

                  } else {
                      pass_test &= d[f_test[i][0]].indexOf(
                        f_test[i][1]) > -1
                  }
                  i++;
              }
              return pass_test;
          });
        // console.log(fList, "--- fList");
        updateCards(fList)
    }
    // console.log([...new Set(allKeys['session_name'])]);
}


const start = () => {
    const urlFilter = getUrlParameter("session");
    setQueryStringParameter("session", urlFilter);
    updateFilterSelectionBtn(urlFilter)

    d3.json('industry.json').then(industry => {
        console.log(industry, "--- industry");

//        shuffleArray(industry);
        //
        allIndustry = industry;
        calcAllKeysSimple(allIndustry, allKeys);
        uniqueSessions = [...new Set(allKeys['session'])];
        uniqueSessions = uniqueSessions.sort((a,b) => a - b);
        // console.log(uniqueSessions);
        render();

    }).catch(e => console.error(e))
}

const updateFilterSelectionBtn = value => {
    d3.selectAll('.filter_option label')
      .classed('active', function () {
          const v = d3.select(this).select('input').property('value')
          return v === value;
      })
    // sessionSearch();
}

const updateSession = () => {
    const urlSession = getUrlParameter("session");
    if (urlSession) {
        filters['session'] = urlSession
        return true;
    } else {
        filters['session'] = null
        return false;
    }
}

d3.selectAll('.filter_option input').on('click', function () {
    const me = d3.select(this)

    const filter_mode = me.property('value');
    setQueryStringParameter("session", filter_mode);
    updateFilterSelectionBtn(filter_mode);
    render();
})

const card_html = openreview => {
    if (openreview.session == 'Platinum'){
        return `<div class="industry-card m-4 text-center">
          <a href="industry_${openreview.uid}.html" class="image-wrapper mb-3" style="display: flex; align-items: center; justify-content: center;">
            <img style="max-width: 100%;" src="static/images/sponsors/${openreview.uid}.png" />
          </a>
          <h3><a href="industry_${openreview.uid}.html">${openreview.company}</a></h3>
          </div>`
      }
    if (openreview.session == 'Gold'){
        return `<div class="industry-card m-4 text-center">
          <a href="industry_${openreview.uid}.html" class="image-wrapper mb-3" style="display: flex; align-items: center; justify-content: center;">
            <img style="max-width: 60%;" src="static/images/sponsors/${openreview.uid}.png" />
          </a>
          <h3><a href="industry_${openreview.uid}.html">${openreview.company}</a></h3>

          </div>`
      }
    if (openreview.session == 'Silver'){
        return `<div class="industry-card m-4 text-center">
          <a href="industry_${openreview.uid}.html" class="image-wrapper mb-3" style="display: flex; align-items: center; justify-content: center;">
            <img style="max-width: 50%;" src="static/images/sponsors/${openreview.uid}.png" />
          </a>
          <h3><a href="industry_${openreview.uid}.html">${openreview.company}</a></h3>
          </div>`
      }

}



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
