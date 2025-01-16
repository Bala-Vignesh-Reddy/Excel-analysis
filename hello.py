import pandas as pd
from PyPDF2 import PdfReader
import re
import requests
from io import BytesIO
import google.generativeai as gemini
from dotenv import load_dotenv
import os
load_dotenv()

gemini.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = gemini.GenerativeModel('gemini-1.5-flash')

def pdf_extraction(url):
    try:
        if not url or not isinstance(url, str):
            return "Invalid url"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        pdf_bytes = BytesIO(response.content)
        pdf_reader = PdfReader(pdf_bytes)

        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        if not text.strip():
            return "No text found in the PDF."

        return text
    except Exception as e:
        print(f"Error fetching or processing PDF: {e}")
        return None
        # for page_num in range(len(pdf_reader.pages)):
        #     text += pdf_reader.pages[page_num].extract_text()

        # extract info..
        # pattern = r"{}".format(target_keyword) + r"[\s\S]*?[\.\n]"
    #     pattern = rf"{re.escape(target_keyword)}[\s\S]*?[\.\n]"
    #     matches = re.findall(pattern, text)

    #     if matches:
    #         extracted_info = matches[0].replace(target_keyword, "").strip()
    #         return extracted_info
    #     else:
    #         return "Keyword not found" 
    # except requests.exceptions.RequestException as e:
    #     print(f"Error processing {url}: {e}")
    #     return "Error fetchine pdf" 
    # except Exception as e:
    #     print(f"Error processing {url}: {e}")
    #     return "error processing pdf"
    
def query_gemini(text, user_prompt):
    try:
        combined_input = f"{text}\n\n{user_prompt} Do not provide any other information"
        response = model.generate_content(combined_input)

        if not response.text.strip() or "not found" in response.text.lower():
            return None

        return response.text
    except Exception as e:
        print(f"Error querying gemini api: {e}")
        return None


def main():
    excel_path = "test.xlsx"
    try:
        df = pd.read_excel(excel_path)
        if 'resumelink' not in df.columns:
            print("resumelink not found")
            return
        
        user_prompt = input("Enter info:")
        if not user_prompt.strip():
            print("Keyword cannot be empty")
            return

        def process_row(url):
            if not url:
                return "Invalid URL"
            pdf_text = pdf_extraction(url)
            if pdf_text:
                return query_gemini(pdf_text, user_prompt)
            return "Error processing pdf"

        # df[user_prompt] = df['resumelink'].apply(lambda x: pdf_extraction(x, target_keyword))
        df[user_prompt] = df['resumelink'].apply(process_row)
        df.to_excel('output.xlsx', index=False)
        print(f"Processing complete.. results saved.. ")
    except FileNotFoundError:
        print("excel file not found")
    except Exception as e:
        print(f"unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
