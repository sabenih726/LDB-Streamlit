import re
from helpers import clean_text, format_date, split_birth_place_date

def extract_sktt(text):
    nik = re.search(r'NIK/Number of Population Identity\s*:\s*(\d+)', text)
    name = re.search(r'Nama/Name\s*:\s*([\w\s]+)', text)
    gender = re.search(r'Jenis Kelamin/Sex\s*:\s*(MALE|FEMALE)', text)
    birth_place_date = re.search(r'Tempat/Tgl Lahir\s*:\s*([\w\s,0-9-]+)', text)
    nationality = re.search(r'Kewarganegaraan/Nationality\s*:\s*([\w\s]+)', text)
    occupation = re.search(r'Pekerjaan/Occupation\s*:\s*([\w\s]+)', text)
    address = re.search(r'Alamat/Address\s*:\s*([\w\s,./-]+)', text)
    kitab_kitas = re.search(r'Nomor KITAP/KITAS Number\s*:\s*([\w-]+)', text)
    expiry_date = re.search(r'Berlaku Hingga s.d/Expired date\s*:\s*([\d-]+)', text)
    birth_place, birth_date = split_birth_place_date(birth_place_date.group(1)) if birth_place_date else (None, None)
    return {
        "NIK": nik.group(1) if nik else None,
        "Name": clean_text(name.group(1), is_name_or_pob=True) if name else None,
        "Jenis Kelamin": gender.group(1) if gender else None,
        "Place of Birth": clean_text(birth_place, is_name_or_pob=True) if birth_place else None,
        "Date of Birth": birth_date,
        "Nationality": clean_text(nationality.group(1)) if nationality else None,
        "Occupation": clean_text(occupation.group(1)) if occupation else None,
        "Address": clean_text(address.group(1)) if address else None,
        "KITAS/KITAP": clean_text(kitab_kitas.group(1)) if kitab_kitas else None,
        "Passport Expiry": format_date(expiry_date.group(1)) if expiry_date else None,
        "Jenis Dokumen": "SKTT"
    }

def extract_evln(text):
    data = {
        "Name": "",
        "Place of Birth": "",
        "Date of Birth": "",
        "Passport No": "",
        "Passport Expiry": "",
        "Jenis Dokumen": "EVLN"
    }
    for line in text.split("\n"):
        if re.search(r"(?i)\bName\b|\bNama\b", line):
            parts = line.split(":")
            if len(parts) > 1:
                data["Name"] = clean_text(parts[1], is_name_or_pob=True)
        elif re.search(r"(?i)\bPlace of Birth\b|\bTempat Lahir\b", line):
            parts = line.split(":")
            if len(parts) > 1:
                data["Place of Birth"] = clean_text(parts[1], is_name_or_pob=True)
        elif re.search(r"(?i)\bDate of Birth\b|\bTanggal Lahir\b", line):
            match = re.search(r"(\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4})", line)
            if match:
                data["Date of Birth"] = format_date(match.group(1))
        elif re.search(r"(?i)\bPassport No\b", line):
            match = re.search(r"\b([A-Z0-9]+)\b", line)
            if match:
                data["Passport No"] = match.group(1)
        elif re.search(r"(?i)\bPassport Expiry\b", line):
            match = re.search(r"(\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4})", line)
            if match:
                data["Passport Expiry"] = format_date(match.group(1))
    return data