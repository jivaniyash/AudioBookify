import pytesseract
from pdf2image import convert_from_path
from gtts import gTTS
import io
import os

def pre_checks(input_file_path: str):
    '''takes in input file path & returns text file path'''

    # check if input file does not exists in the given directory
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"File not Found: {input_file_path}")
    
    file_extension = input_file_path.split(".")[-1]  # .jpeg, .jpg, .png, .pdf, etc

    text_file_path = input_file_path.replace(file_extension, "") + ".txt"
    audio_file_path = input_file_path.replace(file_extension, "") + ".mp3"   

    # checks if text_file already exists
    if os.path.exists(text_file_path):
        raise FileExistsError(f"Text File already exists: {text_file_path}")

    # checks if audio_file already exists
    if os.path.exists(audio_file_path):
        raise FileExistsError(f"Audio File already exists: {audio_file_path}")
    
    return text_file_path, audio_file_path


def process_image(input_file_path: str, text_file_path: str):
    ''' takes in image file path & text file path and runs OCR algorithm / hits api endpoint '''

    # Perform OCR on the page image
    text = pytesseract.image_to_string(input_file_path)

    # Append the extracted text to the overall text
    extracted_text += text

    with io.open(text_file_path, "w") as file: # store text for future use
        file.writelines(extracted_text)
    
    return extracted_text


def process_pdf(input_file_path: str, text_file_path: str):
    # takes in pdf file path, runs pdf_processer & creates a new text file in the same directory
    # Convert each page of the PDF into an image
    pages = convert_from_path(input_file_path)

    # Initialize an empty string to store the extracted text
    extracted_text = ""

    # Iterate over each page and perform OCR
    for page in pages:
        # Perform OCR on the page image
        text = pytesseract.image_to_string(page)
        
        # Append the extracted text to the overall text
        extracted_text += text

    
    with io.open(text_file_path, "w") as file: # store text for future use
        file.writelines(extracted_text)
    
    return extracted_text


def convert_text_audio(text_file_path: str, audio_file_path):
    # takes in text file path, runs audio_processer & creates a new audio file in the same directory
    # Initialize Text-to-Speech (TTS) engine
    tts = gTTS(text=text_file_path, lang='en')

    # Save the audio to a file
    tts.save(audio_file_path)

    print(f"Audiobook saved to {audio_file_path}")
