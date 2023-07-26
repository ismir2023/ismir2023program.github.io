import glob
import os
from bs4 import BeautifulSoup
import pandas as pd
# from PyPDF2 import PdfFileReader, PdfFileWriter
from pdfrw import PdfReader, PdfWriter, IndirectPdfDict
from titlecase import titlecase

folder_stem = "CameraReadys" # substring contained in the name of the folder extracted from the camera-ready archive exported from CMT
xls = "CameraReadyPapers.xml" # as directly exported from CMT, won't work if opened and overwritten by Excel or LibreOffice
pdf_file_prefix = "ISMIR2020-LBD-" # expecting as complete filename pattern: ISMIR2020-LBD-<id>-<abstract/poster>.pdf
pdf_subject_paper = 'Extended Abstracts for the Late-Breaking Demo Session of the 21st International Society for Music Information Retrieval Conference (ISMIR), Montréal, Canada, 2020.'
pdf_subject_poster = 'Posters for the Late-Breaking Demo Session of the 21st International Society for Music Information Retrieval Conference (ISMIR), Montréal, Canada, 2020.'

# Derived from https://github.com/pandas-dev/pandas/issues/11503#issuecomment-661899368

def convert_to_xlsx(xls):
    with open(xls) as xml_file:
        soup = BeautifulSoup(xml_file.read(), 'xml')
        for sheet in soup.findAll('Worksheet'):
            sheet_as_list = []
            for row in sheet.findAll('Row'):
                cells = row.findAll('Cell')
                if len(cells)>1:
                    sheet_as_list.append([cell.Data.text if cell.Data else '' for cell in cells])
            return pd.DataFrame(sheet_as_list[1:len(sheet_as_list)],columns=sheet_as_list[0])
meta = convert_to_xlsx(xls)

ids=pd.Index(meta['Paper ID'])

def abbreviations(word, **kwargs):
    if word.upper() in ('MIREX'):
        return word.upper()

pdfs = glob.glob('*'+folder_stem+'*'+os.sep+'*.pdf');
for pdf in pdfs:
    filename = pdf.split(os.sep)[1].split('.pdf')[0];
    idtype = filename.split(pdf_file_prefix)[1];
    id = idtype.split('-')[0]
    type = idtype.split('-')[1]
    subject = pdf_subject_paper
    if type == 'poster':
        subject = pdf_subject_poster
    loc = ids.get_loc(id)
    authors = meta['Author Names'][loc]
    title = meta['Paper Title'][loc]
    titlecased = titlecase(title, callback=abbreviations)
    #print(id,type,authors,'->',titlecased);#authors

    # https://stackoverflow.com/questions/46849733/change-metadata-of-pdf-file-with-pypdf2

    # fin = open(pdf, 'rb')
    # reader = PdfFileReader(fin)
    # writer = PdfFileWriter()
    # writer.appendPagesFromReader(reader)
    # metadata = reader.getDocumentInfo()
    # # metadata = metadata.replace("'", "’")
    # try:
    #     writer.addMetadata(metadata)
    # except Exception:
    #     print(id,type,authors,'->',titlecased);#authors
    #     print(metadata)
    #     print(x.Info)
    #     print(metadata.producer,x.Info.Producer)
    #     print(metadata.creator,x.Info.Creator)
    #     # print(metadata.author,x.Info.Author)
    #     pass
    # print(metadata)
    # Write your custom metadata here:
    # writer.addMetadata({
    #     '/Author': authors,
    #     '/Title': titlecased,
    #     '/Subject': subject
    # })
    # fout = open(pdf, 'ab') #ab is append binary; if you do wb, the file will append blank pages
    # # writer.write(fout)
    # fin.close()
    # fout.close()

    ## Note: pypdf2 failed to parse metadata for a dozen of ISMIR LBD PDF files, hence the switch to pdfrw with 1 failed PDF

    trailer = PdfReader(pdf)
    print(id,type)
    toprint=False
    if trailer.Info == None:
        print('Could not parse PDF metadata, re-creating.')
        trailer.Info = IndirectPdfDict()
    trailer.Info.Author = authors
    trailer.Info.Title = titlecased
    trailer.Info.Subject = subject
    PdfWriter(pdf, trailer=trailer).write()

