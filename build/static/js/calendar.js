function make_cal(name) {

    // console.log(location.search, "--- location.search");

    const current_tz = getUrlParameter('tz') || moment.tz.guess();
    const tzNames = [...moment.tz.names()];
    console.log(current_tz);
    let localStart = 8 // 08:00 local for checking which opening event to center the calendar on
    let startOffsets = [0,0]

    const setupTZSelector = () => {
        const tzOptons = d3.select('#tzOptions')
        tzOptons.selectAll('option').data(tzNames)
          .join('option')
          .attr('data-tokens', d => d.split("/").join(" "))
          .text(d => d)
        $('.selectpicker')
          .selectpicker('val', current_tz)
          .on('changed.bs.select',
            function (e, clickedIndex, isSelected, previousValue) {
                new_tz = tzNames[clickedIndex]
                window.open(window.location.pathname+'?tz='+new_tz, '_self');
            })

    }

    setupTZSelector();

    // requires moments.js
    const enumerateDaysBetweenDates = function (startDate, endDate) {
        const dates = [];

        // console.log(startDate, endDate, "--- startDate, endDate");

        const currDate = moment(startDate);
        const lastDate = moment(endDate);

        dates.push(currDate.clone());
        while (currDate.add(1, 'days').diff(lastDate) < 0) {
            // console.log(currDate, "--- currDate");
            dates.push(currDate.clone());
        }

        dates.push(lastDate);
        return dates;
    };


    $.get('serve_config.json').then(config => {
        $.get(name).then(events => {
            const scroll_ref1 = config.opening_ref_title_1;
            const scroll_ref2 = config.opening_ref_title_2;

            const all_cals = [];
            const timezoneName = current_tz;

            const min_date = d3.min(events.map(e => e.start));
            var min_hours = d3.min(events.map(e => moment(e.start).tz(timezoneName).hours())) -1;
            var max_hours = d3.max(events.map(e => moment(e.end).tz(timezoneName).hours())) +1;
            if(min_hours < 0 || max_hours > 24) {
                min_hours = 0;
                max_hours = 24;
            }
            // console.log(min_hours, max_hours);
            const Calendar = tui.Calendar;
            const calendar = new Calendar('#calendar', {
                defaultView: 'week',
                isReadOnly: true,
                // useDetailPopup: true,
                taskView: false,
                scheduleView: ['time'],
                usageStatistics: false,
                // useDetailPopup: true,
                week: {
                    // workweek: !config.calendar["sunday_friday"],
                    daynames: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                    startDayOfWeek: 0,
                    // hourStart: min_hours,
                    // hourEnd: max_hours,
                    // narrowWeekend: true,
                },
                timezones: [{
                    timezoneOffset: -moment.tz.zone(timezoneName)
                      .utcOffset(moment(min_date)),
                    displayLabel: timezoneName,
                    tooltip: timezoneName
                }],
                theme: {
                  'week.dayname.height': '42px',
                  'week.timegridOneHour.height': '68px',
                  // 'week.dayGridSchedule.height': '100px',
                },
                // timezones: [{
                //     getTimezoneOffset: 540,
                //     displayLabel: 'a',
                //     tooltip: timezoneName
                // }],
                template: {
                    monthDayname: function (dayname) {
                        return '<span class="calendar-week-dayname-name">' + dayname.label + '</span>';
                    },
                    timegridDisplayPrimaryTime: function (time) {
                      // var meridiem = time.hour < 12 ? 'am' : 'pm';
                      var hour = time.hour < 10 ? `0${time.hour}` : time.hour;
                      var min = time.minutes === 0 ? '00' : time.minutes;
                      return hour + ':' + min;
                    },
                    time: function (schedule) {
                        var class_name=""
                        if (schedule.title == scroll_ref1) {
                          startOffsets[0] = parseInt(moment(schedule.start.getTime())
                            .tz(timezoneName)
                            .format('HH')) + parseInt(moment(schedule.start.getTime())
                            .tz(timezoneName)
                            .format('mm')) / 60 - localStart;
                          class_name = 'openingA';
                          // console.log(startOffsets);
                        } else if (schedule.title == scroll_ref2) {
                          startOffsets[1] = parseInt(
                            moment(schedule.start.getTime())
                            .tz(timezoneName)
                            .format('HH')) + parseInt(
                            moment(schedule.start.getTime())
                            .tz(timezoneName)
                            .format('mm')) / 60 - localStart;
                          class_name = 'openingB';
                          // console.log(startOffsets);
                        }
                        return `<strong class=${class_name}>` + moment(schedule.start.getTime())
                          .tz(timezoneName)
                          .format('HH:mm') + '</strong> ' + schedule.title;
                    },
                    milestone: function (schedule) {
                        return '<span class="calendar-font-icon ic-milestone-b"></span> <span style="background-color: ' + schedule.bgColor + '"> M: ' + schedule.title + '</span>';
                    },
                    weekDayname: function (model) {
                        const parts = model.renderDate.split('-');
                        return '<span class="tui-full-calendar-dayname-name"> ' + parts[1] + '/' + parts[2] + '</span>&nbsp;&nbsp;<span class="tui-full-calendar-dayname-name">' + model.dayName + '</span>';
                    },
                },
            });
            calendar.setDate(Date.parse(min_date));
            calendar.createSchedules(events);
            calendar.on({
                'clickSchedule': function (e) {
                    const s = e.schedule;
                    if (s.location.length > 0) {
                        window.open(s.location, '_self');
                    }
                },
            })

            all_cals.push(calendar);

            const cols = config.calendar.colors;
            if (cols) {
                const cals = [];
                Object.keys(cols).forEach(k => {
                    const v = cols[k];
                    cals.push({
                        id: k,
                        name: k,
                        bgColor: v,
                    })
                })

                calendar.setCalendars(cals);

            }


            const week_dates = enumerateDaysBetweenDates(
              calendar.getDateRangeStart().toDate(),
              calendar.getDateRangeEnd().toDate())

            const c_sm = d3.select('#calendar_small')
            let i = 0
            for (const day of week_dates) {
                c_sm.append('div').attr('id', 'cal__' + i);
                const cal = new Calendar('#cal__' + i, {
                    defaultView: 'day',
                    isReadOnly: true,
                    // useDetailPopup: true,
                    taskView: false,
                    scheduleView: ['time'],
                    usageStatistics: false,

                    timezones: [{
                        timezoneOffset: -moment.tz.zone(timezoneName)
                          .utcOffset(moment(min_date)),
                        displayLabel: timezoneName,
                        tooltip: timezoneName
                    }],
                })

                cal.setDate(day.toDate());
                cal.createSchedules(events);
                cal.on({
                    'clickSchedule': function (e) {
                        const s = e.schedule;
                        if (s.location.length > 0) {

                            if (s.location.split("-")[0] === 'tab') {
                              var location = s.location.split("|");
                              $('.nav-pills .nav-item .nav-link').eq(location[1]).trigger('click');
                              $(`#tab-${location[1]} #day .${location[location.length - 1]}`)[0].scrollIntoView();
                              $('html')[0].scrollTop -= 150;
                            } else {
                              window.open(s.location, '_blanket');
                            }
                        }
                    },
                })

                all_cals.push(cal);
                const cols = config.calendar.colors;
                if (cols) {
                    const cals = [];
                    Object.keys(cols).forEach(k => {
                        const v = cols[k];
                        cals.push({
                            id: k,
                            name: k,
                            bgColor: v,
                        })
                    })

                    cal.setCalendars(cals);

                }

                i++;

                // console.log(day.format(), "--- day");
            }

            // console.log(week_dates.map(d => d.format()), "--- week_dates ");


            const resize = async function (cal) {
                await cal.render(true);
                // d3.selectAll('.tui-full-calendar-vlayout-area').attr('style',null);
            }

            $(window).on('resize', _.debounce(function () {
                all_cals.forEach(c => resize(c));
            }, 100));
            calendar.on('afterRenderSchedule', function() {
              // console.log(startOffsets);
              var scrollTo = null;
              var topPos = 0;
              const contain = $('.tui-full-calendar-timegrid-container');

              if (startOffsets[0] < -3 || startOffsets[0] >= 11) {
                scrollTo = $('.openingB').parents('.tui-full-calendar-time-date-schedule-block');
                topPos = scrollTo[0].offsetTop;
              }
              else {
                scrollTo = $('.openingA').parents('.tui-full-calendar-time-date-schedule-block');
                topPos = scrollTo[0].offsetTop;
              }
              contain.scrollTop(topPos - 20);
            });
            // d3.selectAll('.tui-full-calendar-vlayout-area').attr('style',null);
        })

    })
}

$(window).ready(function() {

})
