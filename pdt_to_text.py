# https://docs.mistral.ai/capabilities/document/ 

from mistralai import Mistral
# from PyPDF2 import PdfReader
import pdfplumber
from tools import get_time_string


def convert_mistral_pdf(api_key, file):
    try:
        # api_key = os.environ["MISTRAL_API_KEY"]
        client = Mistral(api_key=api_key)
        uploaded_pdf = client.files.upload(
            file={
                "file_name": file,
                "content": open(file, "rb"),
            },
            purpose="ocr"
        )  

        signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

        ocr_response = client.ocr.process(
            model="mistral-ocr-2503",
            document={
                "type": "document_url",
                "document_url": signed_url.url,
            }
        )

        client.files.delete(file_id=uploaded_pdf.id)
        return ocr_response.pages[0].markdown

    except Exception as e:
        # raise ValueError(f"Error reading file {file_path}: {str(e)}")
        print(f"Error: {str(e)}")
        return None


def convert_PdfReader_pdf(file_path):
    try:
        text = ''

        # with open(file, "rb") as pdf_file:
        #     pdf_reader = PdfReader(pdf_file)
        #     for page_num in range(len(pdf_reader.pages)):
        #         page = pdf_reader.pages[page_num]
        #         text += page.extract_text()

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        return text
    
    except Exception as e:
        # raise ValueError(f"Error reading PDF file {file}: {str(e)}")
        print(f"Error reading PDF file {pdf}: {str(e)}")
        return None
    


def convert_pdf_to_text(filePath, userId, aiMode=True):
    
    TOKEN_MISTRAL = ''
    with open("config/mistral.txt", "r", encoding="utf-8") as file:
        TOKEN_MISTRAL = file.read()

    result = ''
    fileWay = ''

    if aiMode:
        result = convert_mistral_pdf(TOKEN_MISTRAL, filePath)

    if result:
        fileWay = 'media/pdf2md__{}__{}.md'.format(userId, get_time_string())
    else:
        result = convert_PdfReader_pdf(filePath)

        
    if result:
        fileWay = 'media/pdf2txt__{}__{}.txt'.format(userId, get_time_string())

        
    if not result:
        # return None
        raise ValueError(f"Convert fail")
    

    with open(fileWay, "w", encoding="utf-8") as file:
        file.write(result)
        print('PDF успешно конвертирован!')

    return fileWay


