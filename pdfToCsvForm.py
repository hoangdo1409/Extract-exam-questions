import re
import openai
import csv
import pandas as pd
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
# Đầu vào là đề thi hóa với định dạng pdf
# Trích xuất dữ liệu từ file pdf (pdfminer) và đưa vào file txt

def read_pdf(pdf_path):
    output_string = StringIO()
    with open(pdf_path, 'rb') as in_file:
        res_mgr = PDFResourceManager()
        device = TextConverter(res_mgr, output_string, codec='utf-8')
        interpreter = PDFPageInterpreter(res_mgr, device)

        for page in PDFPage.get_pages(in_file, check_extractable=True):
            interpreter.process_page(page)
        text = output_string.getvalue()

    return text

# Lấy ra câu hỏi và đáp án từ dữ liệu đã trích xuất
def get_question_options(text: str) -> list[str]:
    pattern = r"(Câu \d+:.+?)(?=(Câu \d+:)|$)"
    matches = re.findall(pattern, text, re.DOTALL)

    list_quest_op = []

    for match in matches:
        questions_options = match[0].strip()
        list_quest_op.append(questions_options)
    return list_quest_op

# Chuyển câu hỏi và đáp án về dạng csv: quest| A. ans | B. ans | C. ans | D. ans
def format_text(format: str, text: str, api_key, max_tokens=3473) -> str:
    openai.api_key = (api_key)
    prompt = text + format

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.02,
        max_tokens=max_tokens,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return response.choices[0].text
# Xóa các dòng trắng thừa
def reformat_form_csv(str_formated_csv: str) -> str:
    lines = str_formated_csv.split("\n")
    lines = [line for line in lines if len(line) != 0]

    # Chuyển lại thành chuỗi
    str_after_del_blank = "\n".join(lines)
    return str_after_del_blank.strip()


def print_to_txt(text, path_file) -> None:
    with open(path_file, 'w', encoding='utf-8', errors='ignore') as txt_file:
        txt_file.write(text)

def convert_txt_to_csv():
    f = open('form_csv.txt', 'r', encoding='utf-8')
    quest = []
    op1 = []
    op2 = []
    op3 = []
    op4 = []
    for line in f:
        quest_and_op = line.split("|")
        quest.append(quest_and_op[0])
        op1.append(quest_and_op[1])
        op2.append(quest_and_op[2])
        op3.append(quest_and_op[3])
        op4.append(quest_and_op[4])

    df = pd.DataFrame({
        'Câu Hỏi': quest,
        'Đáp án 1': op1,
        'Đáp án 2': op2,
        'Đáp án 3': op3,
        'Đáp án 4': op4            
    })
    df.to_csv('file_result.csv', index=False, encoding='utf-8')
