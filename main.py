from pdfToCsvForm import *
from dotenv import load_dotenv
import os, time
import math


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('API_KEY')
    max_tokens = os.getenv('MAX_TOKENS')
    pdf_path = 'data1.pdf'
    csv_path = 'file_result.csv'
    txt_path = 'form_csv.txt'
    doc_path = 'document.docx'

    pattern_pdf = r"(Câu \d+:.+?)(?=(Câu \d+:)|$)"

    format = """Trích xuất toàn bộ nội dung các câu trên thành dạng câu hỏi và các đáp án với định dạng như sau, không được có chuỗi "Câu hỏi:" ở đầu:
Nội dung toàn bộ câu hỏi không được tóm tắt|Answer A| Answer B|Answer C|Answer D"""

    path = pdf_path
    if path.endswith(".pdf"):
        content_extract = read_pdf(path)
    elif path.endswith(".docx") or path.endswith(".doc"):
        content_extract = read_docx(path)

    quest_option = get_question_options(content_extract, pattern_pdf)
    # sep = "\n"
    # aaa = sep.join(quest_option)
    # print_to_txt(content_extract, 'abc.txt')
    str_formated_csv = ""
    for j in range(0, len(quest_option)):
        try:
            quest_op = format_text(format=format, text=quest_option[j], api_key=api_key)
            str_formated_csv += quest_op + "\n"
        except:
            time.sleep(3)
            j -= 1  
            continue

    str_reformat = reformat_form_csv(str_formated_csv)
    print_to_txt(str_reformat, 'form_csv.txt')

    convert_txt_to_csv()
    