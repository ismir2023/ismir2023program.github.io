# import csv
# in_csv = '../ISMIR-2022-Miniconf-Data/sitedata/papers.csv'
#
# csv_reader = csv.reader(open(in_csv), delimiter=',')
# words = next(csv_reader)
#
# cnt =0
# for words in csv_reader:
#     uid = words[0]
#     print(uid)
#     cnt+=1
# print(cnt)


import os
import shutil

in_dir = '/Users/jyotsna//Downloads/poster'
out_dir = '/Users/jyotsna//Downloads/poster_pdf'

for filename in os.listdir(in_dir):
    out_filename = '{}.pdf'.format(filename)
    print(out_filename, filename)
    shutil.copyfile(os.path.join(in_dir, filename), os.path.join(out_dir, out_filename))



# import csv
# import gdown
# in_csv = '../ISMIR-2022-Miniconf-Data/sitedata/papers.csv'
#
# csv_reader = csv.reader(open(in_csv), delimiter=',')
# words = next(csv_reader)
# thumbnail_ind = words.index('poster_pdf')
#
# cnt =0
# for words in csv_reader:
#
#     thumbnail_url = words[thumbnail_ind]
#     print(thumbnail_url)
#     gdown.download(thumbnail_url.replace('/open?', '/uc?'), output='/Users/jyotsna/Downloads/poster_pdf/{}'.format(words[0]), quiet=False)
#
