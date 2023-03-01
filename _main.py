from pdfToCsvForm import format_text, add2csv, read_pdf, get_question_options
from dotenv import load_dotenv
import os, time

def handle(text):
    table = [[],[],[],[],[]]
    arr = text.split('|')
    for i in range(5): 
        table[i].append(arr[i])
    add2csv(filename='file.csv', col1=table[0], col2=table[1], col3=table[2], col4=table[3], col5=table[4])


if '__name__' == '__main__':

    pdf = read_pdf('data1.pdf')
    quests = get_question_options(pdf)
    
    for index in range(0, len(quests)):
        try:
            handle(quests[index])
        except:
            time.sleep(secs=30)
            index -= 1
            continue
