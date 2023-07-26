import csv


def registration_stats(in_csv):
    csv_reader = csv.reader(open(in_csv), delimiter=',')
    words = next(csv_reader)
    ticket_choice_ind = words.index('Ticket_Name')
    author_choice_ind = words.index('How are you planning to attend ISMIR 2022 ?')
    country_ind = words.index('Country')

    morntut_choice_ind = words.index('Select the morning session tutorial you wish to attend')
    noontut_choice_ind = words.index('Select the afternoon session tutorial you wish to attend')
    tut_counters = {
        '1':{
            'Full': {'Virtually':0, 'In-person':0, 'Undecided': 0},
            'Student': {'Virtually':0, 'In-person':0, 'Undecided': 0}
        },
        '2': {
            'Full': {'Virtually': 0, 'In-person': 0, 'Undecided': 0},
            'Student': {'Virtually': 0, 'In-person': 0, 'Undecided': 0}
        },
        '3': {
            'Full': {'Virtually': 0, 'In-person': 0, 'Undecided': 0},
            'Student': {'Virtually': 0, 'In-person': 0, 'Undecided': 0}
        },
        '4': {
            'Full': {'Virtually': 0, 'In-person': 0, 'Undecided': 0},
            'Student': {'Virtually': 0, 'In-person': 0, 'Undecided': 0}
        },
        '5': {
            'Full': {'Virtually': 0, 'In-person': 0, 'Undecided': 0},
            'Student': {'Virtually': 0, 'In-person': 0, 'Undecided': 0}
        },
        '6': {
            'Full': {'Virtually': 0, 'In-person': 0, 'Undecided': 0},
            'Student': {'Virtually': 0, 'In-person': 0, 'Undecided': 0}
        }
    }
    tmp_counters = {
        'Full': {'Virtually':0, 'In-person':0, 'Undecided': 0},
        'Student': {'Virtually':0, 'In-person':0, 'Undecided': 0}
    }
    country_counters = {}
    reg_counters = {
        'Full': {'Virtually':0, 'In-person':0, 'Undecided': 0},
        'Student': {'Virtually':0, 'In-person':0, 'Undecided': 0}
    }
    for words in csv_reader:
        ticket_choice = words[ticket_choice_ind]
        author_choice = words[author_choice_ind]
        country_choice = words[country_ind]
        country_counters[country_choice] = tmp_counters

        morn_tut_ind, noon_tut_ind = 0, 0
        if words[morntut_choice_ind] != 'NA':
            morn_tut_ind = words[morntut_choice_ind][3]
        if words[noontut_choice_ind] != 'NA':
            noon_tut_ind = words[noontut_choice_ind][3]
        # if morn_tut_ind or noon_tut_ind:
        #     embed()
        if 'Full' in ticket_choice:
            if 'or' in ticket_choice:
                if 'Virtual' in author_choice:
                    reg_counters['Full']['Virtually'] += 1
                    country_counters[country_choice]['Full']['Virtually'] += 1
                    if morn_tut_ind:
                        tut_counters[morn_tut_ind]['Full']['Virtually'] += 1
                    if noon_tut_ind:
                        tut_counters[noon_tut_ind]['Full']['Virtually'] += 1
                elif 'In-person' in author_choice:
                    reg_counters['Full']['In-person'] += 1
                    country_counters[country_choice]['Full']['In-person'] += 1
                    if morn_tut_ind:
                        tut_counters[morn_tut_ind]['Full']['In-person'] += 1
                    if noon_tut_ind:
                        tut_counters[noon_tut_ind]['Full']['In-person'] += 1

                elif 'Undecided' in author_choice:
                    reg_counters['Full']['Undecided'] += 1
                    country_counters[country_choice]['Full']['Undecided'] += 1
                    if morn_tut_ind:
                        tut_counters[morn_tut_ind]['Full']['Undecided'] += 1
                    if noon_tut_ind:
                        tut_counters[noon_tut_ind]['Full']['Undecided'] += 1
                else:
                    print('Unknown author_choice: {}'.format(author_choice))

            elif 'Virtual' in ticket_choice:
                reg_counters['Full']['Virtually'] += 1
                country_counters[country_choice]['Full']['Virtually'] += 1
                if morn_tut_ind:
                    tut_counters[morn_tut_ind]['Full']['Virtually'] += 1
                if noon_tut_ind:
                    tut_counters[noon_tut_ind]['Full']['Virtually'] += 1
            elif 'In-person' in ticket_choice:
                reg_counters['Full']['In-person'] += 1
                country_counters[country_choice]['Full']['In-person'] += 1
                if morn_tut_ind:
                    tut_counters[morn_tut_ind]['Full']['In-person'] += 1
                if noon_tut_ind:
                    tut_counters[noon_tut_ind]['Full']['In-person'] += 1
            else:
                print('Unknown ticket_choice: {}'.format(ticket_choice))

        elif 'Student' in ticket_choice:

            if 'or' in ticket_choice:
                if 'Virtual' in author_choice:
                    reg_counters['Student']['Virtually'] += 1
                    country_counters[country_choice]['Student']['Virtually'] += 1
                    if morn_tut_ind:
                        tut_counters[morn_tut_ind]['Student']['Virtually'] += 1
                    if noon_tut_ind:
                        tut_counters[noon_tut_ind]['Student']['Virtually'] += 1
                elif 'In-person' in author_choice:
                    reg_counters['Student']['In-person'] += 1
                    country_counters[country_choice]['Student']['In-person'] += 1
                    if morn_tut_ind:
                        tut_counters[morn_tut_ind]['Student']['In-person'] += 1
                    if noon_tut_ind:
                        tut_counters[noon_tut_ind]['Student']['In-person'] += 1

                elif 'Undecided' in author_choice:
                    reg_counters['Student']['Undecided'] += 1
                    country_counters[country_choice]['Student']['Undecided'] += 1
                    if morn_tut_ind:
                        tut_counters[morn_tut_ind]['Student']['Undecided'] += 1
                    if noon_tut_ind:
                        tut_counters[noon_tut_ind]['Student']['Undecided'] += 1

                else:
                    print('Unknown author_choice: {}'.format(author_choice))

            elif 'Virtual' in ticket_choice:
                reg_counters['Student']['Virtually'] += 1
                country_counters[country_choice]['Student']['Virtually'] += 1
                if morn_tut_ind:
                    tut_counters[morn_tut_ind]['Student']['Virtually'] += 1
                if noon_tut_ind:
                    tut_counters[noon_tut_ind]['Student']['Virtually'] += 1

            elif 'In-person' in ticket_choice:
                reg_counters['Student']['In-person'] += 1
                country_counters[country_choice]['Student']['In-person'] += 1
                if morn_tut_ind:
                    tut_counters[morn_tut_ind]['Student']['In-person'] += 1
                if noon_tut_ind:
                    tut_counters[noon_tut_ind]['Student']['In-person'] += 1

            else:
                print('Unknown ticket_choice: {}'.format(ticket_choice))
        else:
            print('Unknown ticketchoice: {}'.format(ticket_choice))



    # from IPython import embed
    # embed()

    print('ISMIR Registrations Summary')
    print('Total registered: {} [{}: full, {}: student]'.format(
        reg_counters['Full']['In-person']+reg_counters['Student']['In-person'] + reg_counters['Full']['Virtually']+reg_counters['Student']['Virtually'] + reg_counters['Full']['Undecided']+reg_counters['Student']['Undecided'],
        reg_counters['Full']['In-person']+reg_counters['Full']['Virtually']+reg_counters['Full']['Undecided'],
        reg_counters['Student']['In-person']+reg_counters['Student']['Virtually']+reg_counters['Student']['Undecided']
    ))
    print('Total physical: {} [{}: full, {}: student]'.format(
        reg_counters['Full']['In-person']+reg_counters['Student']['In-person'],
        reg_counters['Full']['In-person'],
        reg_counters['Student']['In-person']))

    print('Total virtual: {} [{}: full, {}: student]'.format(
        reg_counters['Full']['Virtually']+reg_counters['Student']['Virtually'],
        reg_counters['Full']['Virtually'],
        reg_counters['Student']['Virtually']))

    print('Total undecided: {} [{}: full, {}: student]'.format(
        reg_counters['Full']['Undecided']+reg_counters['Student']['Undecided'],
        reg_counters['Full']['Undecided'],
        reg_counters['Student']['Undecided']))

    print('\n\n')
    print('Tutorials Registrations Summary')
    for tut_ind in tut_counters:
        print()
        print('Tutorial: {}'.format(tut_ind))
        # print(tut_counters[tut_ind])
        print('\tTotal registered {}: \n\tFull - {}, Student - {}'.format(
            tut_counters[tut_ind]['Full']['In-person']+tut_counters[tut_ind]['Student']['In-person'] + tut_counters[tut_ind]['Full']['Virtually']+tut_counters[tut_ind]['Student']['Virtually'] + tut_counters[tut_ind]['Full']['Undecided']+tut_counters[tut_ind]['Student']['Undecided'],
            tut_counters[tut_ind]['Full']['In-person']+tut_counters[tut_ind]['Full']['Virtually']+tut_counters[tut_ind]['Full']['Undecided'],
            tut_counters[tut_ind]['Student']['In-person']+tut_counters[tut_ind]['Student']['Virtually']+tut_counters[tut_ind]['Student']['Undecided']

        ))
        print('\tPhysical - {}, Virtual - {}, Undecided - {}'.format(
            tut_counters[tut_ind]['Full']['In-person']+tut_counters[tut_ind]['Student']['In-person'],
            tut_counters[tut_ind]['Full']['Virtually'] + tut_counters[tut_ind]['Student']['Virtually'],
            tut_counters[tut_ind]['Full']['Undecided'] + tut_counters[tut_ind]['Student']['Undecided'],

        ))


if __name__ == "__main__":
    in_csv = '../miniconf-data/sitedata/__23rd_International_Society_for_Music_Information_Retrieval_Conference_(ISMIR_2022)__Registration_Data.csv'
    registration_stats(in_csv=in_csv)
