import os
import tempfile
import shutil
import zipfile
import io
import pdfplumber
import pandas as pd

from extractors import (
    extract_sktt,
    extract_evln,
    extract_itas,
    extract_itk,
    extract_notifikasi,
    extract_dkptka_info  # ✅ tambahkan ini
)
from helpers import generate_new_filename

def process_pdfs(uploaded_files, doc_type, use_name, use_passport):
    all_data = []
    renamed_files = {}
    temp_dir = tempfile.mkdtemp()

    for uploaded_file in uploaded_files:
        pdf_bytes = uploaded_file.read()
        pdf_stream = io.BytesIO(pdf_bytes)

        # === DKPTKA: panggil fungsi khusus dengan path file sementara ===
        if doc_type == "DKPTKA":
            # Simpan sementara file ke disk agar bisa dibuka oleh extract_dkptka_info
            temp_pdf_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_pdf_path, "wb") as f:
                f.write(pdf_bytes)
            extracted_data = extract_dkptka_info(temp_pdf_path)
        else:
            with pdfplumber.open(pdf_stream) as pdf:
                texts = [page.extract_text() for page in pdf.pages if page.extract_text()]
                full_text = "\n".join(texts)

            if doc_type == "SKTT":
                extracted_data = extract_sktt(full_text)
            elif doc_type == "EVLN":
                extracted_data = extract_evln(full_text)
            elif doc_type == "ITAS":
                extracted_data = extract_itas(full_text)
            elif doc_type == "ITK":
                extracted_data = extract_itk(full_text)
            elif doc_type == "Notifikasi":
                extracted_data = extract_notifikasi(full_text)
            else:
                extracted_data = {}

        all_data.append(extracted_data)
        new_filename = generate_new_filename(extracted_data, use_name, use_passport)

        temp_file_path = os.path.join(temp_dir, new_filename)
        with open(temp_file_path, 'wb') as f:
            f.write(pdf_bytes)

        renamed_files[uploaded_file.name] = {'new_name': new_filename, 'path': temp_file_path}

    df = pd.DataFrame(all_data)
    excel_path = os.path.join(temp_dir, "Hasil_Ekstraksi.xlsx")
    df.to_excel(excel_path, index=False)

    zip_path = os.path.join(temp_dir, "Renamed_Files.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_info in renamed_files.values():
            zipf.write(file_info['path'], arcname=file_info['new_name'])

    return df, excel_path, renamed_files, zip_path, temp_dir
