let allLBDs = [];
const allKeys = {
    authors: [],
    keywords: [],
    session: [],
    titles: [],
}
const filters = {
    authors: null,
    keywords: null,
    session: null,
    title: null,
};

let render_mode = 'compact';
let uniqueSessions = null;

let release_day = $('#release-day').data()['name'];
let browse_paper_buttons = $('#browse-buttons').data()['name'];

let slack_svg =  `<svg style="display: inline-block; width: 23px;" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="75 75 150 150" style="enable-background:new 0 0 270 270;" xml:space="preserve">
<style type="text/css">
	.st0{fill:#FFFFFF;}
</style>
<g>
	<g>
		<path class="st0" d="M99.4,151.2c0,7.1-5.8,12.9-12.9,12.9s-12.9-5.8-12.9-12.9c0-7.1,5.8-12.9,12.9-12.9h12.9V151.2z"/>
		<path class="st0" d="M105.9,151.2c0-7.1,5.8-12.9,12.9-12.9s12.9,5.8,12.9,12.9v32.3c0,7.1-5.8,12.9-12.9,12.9
			s-12.9-5.8-12.9-12.9C105.9,183.5,105.9,151.2,105.9,151.2z"/>
	</g>
	<g>
		<path class="st0" d="M118.8,99.4c-7.1,0-12.9-5.8-12.9-12.9s5.8-12.9,12.9-12.9s12.9,5.8,12.9,12.9v12.9H118.8z"/>
		<path class="st0" d="M118.8,105.9c7.1,0,12.9,5.8,12.9,12.9s-5.8,12.9-12.9,12.9H86.5c-7.1,0-12.9-5.8-12.9-12.9
			s5.8-12.9,12.9-12.9C86.5,105.9,118.8,105.9,118.8,105.9z"/>
	</g>
	<g>
		<path class="st0" d="M170.6,118.8c0-7.1,5.8-12.9,12.9-12.9c7.1,0,12.9,5.8,12.9,12.9s-5.8,12.9-12.9,12.9h-12.9V118.8z"/>
		<path class="st0" d="M164.1,118.8c0,7.1-5.8,12.9-12.9,12.9c-7.1,0-12.9-5.8-12.9-12.9V86.5c0-7.1,5.8-12.9,12.9-12.9
			c7.1,0,12.9,5.8,12.9,12.9V118.8z"/>
	</g>
	<g>
		<path class="st0" d="M151.2,170.6c7.1,0,12.9,5.8,12.9,12.9c0,7.1-5.8,12.9-12.9,12.9c-7.1,0-12.9-5.8-12.9-12.9v-12.9H151.2z"/>
		<path class="st0" d="M151.2,164.1c-7.1,0-12.9-5.8-12.9-12.9c0-7.1,5.8-12.9,12.9-12.9h32.3c7.1,0,12.9,5.8,12.9,12.9
			c0,7.1-5.8,12.9-12.9,12.9H151.2z"/>
	</g>
</g>
</svg>
`

const persistor = new Persistor('Mini-Conf-LBDs');

const updateCards = (lbds) => {
    const storedLBDs = persistor.getAll();
    lbds.forEach(
      openreview => {
          openreview.content.read = storedLBDs[openreview.id] || false
      })

    const readCard = (iid, new_value) => {
        persistor.set(iid, new_value);
        // storedLBDs[iid] = new_value ? 1 : null;
        // Cookies.set('lbds-selected', storedLBDs, {expires: 365});
    }

    const all_mounted_cards = d3.select('.cards')
      .selectAll('.myCard', openreview => openreview.id)
      .data(lbds, d => d.number)
      .join('div')
      .attr('class', 'myCard col-xs-6 col-md-4')
      .html(card_html)

    all_mounted_cards.select('.card-title')
      .on('click', function (d) {
          const iid = d.id;
          all_mounted_cards.filter(d => d.id === iid)
            .select(".checkbox-paper").classed('selected', function () {
              const new_value = true;//!d3.select(this).classed('not-selected');
              readCard(iid, new_value);
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

/* Randomize array in-place using Durstenfeld shuffle algorithm */
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

    // console.log(f_test, filters, "--- f_test, filters");
    if (f_test.length === 0) updateCards(allLBDs)
    else {
        const fList = allLBDs.filter(
          d => {
              let i = 0, pass_test = true;
              while (i < f_test.length && pass_test) {
                  if (f_test[i][0] === 'titles') {
                      pass_test &= d.content['title'].toLowerCase()
                        .indexOf(f_test[i][1].toLowerCase()) > -1;

                  } else {
                      pass_test &= d.content[f_test[i][0]].indexOf(
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
        d3.select('#session_name').text(urlSession);
        d3.select('.session_notice').classed('d-none', null);
        return true;
    } else {
        filters['session'] = null
        d3.select('.session_notice').classed('d-none', true);
        return false;
    }
}

/**
 * START here and load JSON.
 */
const start = () => {
    const urlFilter = getUrlParameter("filter") || 'titles';
    setQueryStringParameter("filter", urlFilter);
    updateFilterSelectionBtn(urlFilter)


    d3.json('lbds.json').then(lbds => {
        console.log(lbds, "--- lbds");

//        shuffleArray(lbds);

        allLBDs = lbds;
        calcAllKeys(allLBDs, allKeys);
        uniqueSessions = [...new Set(allKeys['session'])];
        uniqueSessions = uniqueSessions.sort((a,b) => a - b);
        console.log(uniqueSessions);
        populateSessionSelect(uniqueSessions);
        setTypeAhead(urlFilter,
          allKeys, filters, render);
        updateCards(allLBDs)


        const urlSearch = getUrlParameter("search");
        const urlSession = getUrlParameter("session");
        // console.log(urlSession);
        if (urlSession !== '') {
          document.getElementById("session-select").value = urlSession;
          setQueryStringParameter("session", urlSession);
          filters["session"] = urlSession;
          render();
        }
        // if ((urlSearch !== '') || updateSession()) {
        if (urlSearch !== '') {
            filters[urlFilter] = urlSearch;
            $('.typeahead_all').val(urlSearch);
            render();
        }


    }).catch(e => console.error(e))
}


/**
 * EVENTS
 * **/

function sessionSearch() {
  let select = document.getElementById("session-select").value;
  setQueryStringParameter("session", select);
  render();
}
// d3.selectAll('#session-select option').on('click', function() {
//     console.log('selected');
//     const me = d3.select(this);
//
// })

d3.selectAll('.filter_option input').on('click', function () {
    const me = d3.select(this)

    const filter_mode = me.property('value');
    setQueryStringParameter("filter", filter_mode);
    setQueryStringParameter("search", '');
    // setQueryStringParameter("session", '');
    updateFilterSelectionBtn(filter_mode);


    setTypeAhead(filter_mode, allKeys, filters, render);
    render();
})

d3.selectAll('.remove_session').on('click', () => {
    setQueryStringParameter("session", '');
    render();

})

d3.selectAll('.render_option input').on('click', function () {
    const me = d3.select(this);
    render_mode = me.property('value');

    render();
})

d3.select('.reshuffle').on('click', () => {
    shuffleArray(allLBDs);

    render();
})

/**
 * CARDS
 */

const keyword = kw => `<a href="lbds.html?filter=keywords&search=${kw}"
                       class="text-secondary text-decoration-none">${kw.toLowerCase()}</a>`

const card_image = (openreview, show) => {
    if (show) return ` <center><img class="lazy-load-img cards_img" data-src="static/images/lbd/thumbnails/${openreview.content.thumbnail_link}" width="80%"/></center>`
    else return ''
}

const card_detail = (openreview, show) => {
    if (show)
        return `
     <div class="pp-card-header">
        <p class="card-text"> ${openreview.content.TLDR}</p>`
    // +    `<p class="card-text"><span class="font-weight-bold">Keywords:</span>
    //         ${openreview.content.keywords.map(keyword).join(', ')}
    //     </p>`
    +`</div>
`
    else return ''
}

const card_time_small = (openreview, show) => {
    const cnt = openreview.content;
    return show ? `
<!--    <div class="pp-card-footer">-->
    <div class="text-center" style="margin-top: 10px;">
    ${cnt.session.filter(s => s.match(/.*[0-9]/g)).map(
      (s, i) => `<a class="card-subtitle text-muted" href="?session=${encodeURIComponent(
        s)}">${s.replace('Session ', '')}</a> ${card_live(
        cnt.session_links[i])} ${card_cal(openreview, i)} `).join(', ')}
    </div>
<!--    </div>-->
    ` : '';
}

const card_icon_video = icon_video(16);
const card_icon_cal = icon_cal(16);

const card_live = (link) => `<a class="text-muted" href="${link}">${card_icon_video}</a>`
const card_cal = (openreview, i) => `<a class="text-muted" href="webcal://iclr.github.io/iclr-images/calendars/lbd_${openreview.forum}.${i}.ics">${card_icon_cal}</a>`

// const card_time_detail = (openreview, show) => {
//     const cnt = openreview.content;
//     return show ? `
// <!--    <div class="pp-card-footer">-->
//     <div class="text-center text-monospace small" style="margin-top: 10px;">
//     ${cnt.session.filter(s => s.match(/.*[0-9]/g))
//       .map((s, i) => `${s} ${cnt.session_times[i]} ${card_live(cnt.session_links[i])}   `)
//       .join('<br>')}
//     </div>
// <!--    </div>-->
//     ` : '';
// }

//language=HTML
const card_html = openreview => {
    var button = ''
    if (release_day >= openreview.content.day && browse_paper_buttons) {
      button += '<div class="text-right"><a class="btn btn-primary slack-btn mt-3 mb-3" href="'
      button += ''
      button += openreview.content.channel_url + '">'
      button += slack_svg
      button += openreview.content.channel_name + '</a></div>'
    }
    return `
        <a href="lbd_${openreview.id}.html"><div class="pp-card pp-mode-` + render_mode + ` ">
            <div class="pp-card-header">
            <div class="checkbox-paper ${openreview.content.read ? 'selected' : ''}" style="display: block;position: absolute; bottom:35px;left: 35px;">✓</div>
            <h5 class="card-title text-muted" align="center">  L${openreview.content.session[0][0]}-${openreview.position}: ${openreview.content.title} </h5>
            <h6 class="card-subtitle text-muted" align="center"> ${openreview.content.authors.join(', ')} </h6>
                ${card_image(openreview, render_mode !== 'list')}
                ` + button +
                `</div>
                ${card_detail(openreview, (render_mode === 'detail'))}

        </div></a>`
}