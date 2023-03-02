from pdfToCsvForm import *
from dotenv import load_dotenv
import os, time
import math


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('API_KEY')
    pdf_path = 'data1.pdf'


    format = """Chuyển toàn bộ nội dung các câu trên thành dạng câu hỏi và các đáp án với định dạng như sau và không xuống dòng ở cuối câu, không có cụm "Câu :" ở đầu:
Nội dung câu hỏi|Answer A| Answer B|Answer C|Answer D"""

    content_extract = read_pdf('data1.pdf')
    quest_option = get_question_options(content_extract)
    # sep = "\n"
    # aaa = sep.join(quest_option)
    # print_to_txt(aaa, 'abc.txt')

    str_formated_csv = ""


    for j in range(0, len(quest_option)):
        try:
            quest_op = format_text(format=format, text=quest_option[j], api_key=api_key)
            str_formated_csv += quest_op + "\n"
        except:
            time.sleep(3)
            j -= 1  
            continue
    
    print_to_txt(str_formated_csv, 'abc.txt')

    # Xóa dòng trắng rồi ghi vào file txt
    str_reformat = reformat_form_csv(str_formated_csv)
    print_to_txt(str_reformat, 'form_csv.txt')

    # # abc
    convert_txt_to_csv()
    