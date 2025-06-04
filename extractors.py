import re
import pdfplumber
from helpers import clean_text, format_date, split_birth_place_date

# ========================= Ekstraksi SKTT =========================
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

# ========================= Ekstraksi EVLN =========================
def extract_evln(text):
    data = {
        "Name": "",
        "Place of Birth": "",
        "Date of Birth": "",
        "Passport No": "",
        "Passport Expiry": "",
        "Jenis Dokumen": "EVLN"
    }

    lines = text.split("\n")

    # Cari nama berdasarkan sapaan seperti Dear Mr./Ms.
    for i, line in enumerate(lines):
        if re.search(r"Dear\s+(Mr\.|Ms\.|Sir|Madam)?", line, re.IGNORECASE):
            if i + 1 < len(lines):
                name_candidate = lines[i + 1].strip()
                if 3 < len(name_candidate) < 50:
                    if 'clean_text' in globals():
                        data["Name"] = clean_text(name_candidate, is_name_or_pob=True)
                    else:
                        data["Name"] = re.sub(r'[^A-Z ]', '', name_candidate.upper())
            break

    # Parsing baris lain
    for line in lines:
        if not data["Name"] and re.search(r"(?i)\bName\b|\bNama\b", line):
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

# ========================= Ekstraksi ITAS =========================
def extract_itas(text):
    data = {}

    name_match = re.search(r"([A-Z\s]+)\nPERMIT NUMBER", text)
    data["Name"] = name_match.group(1).strip() if name_match else None

    permit_match = re.search(r"PERMIT NUMBER\s*:\s*([A-Z0-9-]+)", text)
    data["Permit Number"] = permit_match.group(1) if permit_match else None

    expiry_match = re.search(r"STAY PERMIT EXPIRY\s*:\s*([\d/]+)", text)
    data["Stay Permit Expiry"] = format_date(expiry_match.group(1)) if expiry_match else None

    place_date_birth_match = re.search(r"Place / Date of Birth\s*.*:\s*([A-Za-z\s]+)\s*/\s*([\d-]+)", text)
    if place_date_birth_match:
        place = place_date_birth_match.group(1).strip()
        date = place_date_birth_match.group(2).strip()
        data["Place & Date of Birth"] = f"{place}, {format_date(date)}"
    else:
        data["Place & Date of Birth"] = None

    passport_match = re.search(r"Passport Number\s*: ([A-Z0-9]+)", text)
    data["Passport Number"] = passport_match.group(1) if passport_match else None

    passport_expiry_match = re.search(r"Passport Expiry\s*: ([\d-]+)", text)
    data["Passport Expiry"] = format_date(passport_expiry_match.group(1)) if passport_expiry_match else None

    nationality_match = re.search(r"Nationality\s*: ([A-Z]+)", text)
    data["Nationality"] = nationality_match.group(1) if nationality_match else None

    gender_match = re.search(r"Gender\s*: ([A-Z]+)", text)
    data["Gender"] = gender_match.group(1) if gender_match else None

    address_match = re.search(r"Address\s*:\s*(.+)", text)
    data["Address"] = address_match.group(1).strip() if address_match else None

    occupation_match = re.search(r"Occupation\s*:\s*(.+)", text)
    data["Occupation"] = occupation_match.group(1).strip() if occupation_match else None

    guarantor_match = re.search(r"Guarantor\s*:\s*(.+)", text)
    data["Guarantor"] = guarantor_match.group(1).strip() if guarantor_match else None

    data["Jenis Dokumen"] = "ITAS"

    return data

# ========================= Ekstraksi ITK =========================
def extract_itk(text):
    # Struktur sama dengan ITAS, bisa direuse tapi saya buatkan terpisah untuk fleksibilitas
    data = {}

    name_match = re.search(r"([A-Z\s]+)\nPERMIT NUMBER", text)
    data["Name"] = name_match.group(1).strip() if name_match else None

    permit_match = re.search(r"PERMIT NUMBER\s*:\s*([A-Z0-9-]+)", text)
    data["Permit Number"] = permit_match.group(1) if permit_match else None

    expiry_match = re.search(r"STAY PERMIT EXPIRY\s*:\s*([\d/]+)", text)
    data["Stay Permit Expiry"] = format_date(expiry_match.group(1)) if expiry_match else None

    place_date_birth_match = re.search(r"Place / Date of Birth\s*.*:\s*([A-Za-z\s]+)\s*/\s*([\d-]+)", text)
    if place_date_birth_match:
        place = place_date_birth_match.group(1).strip()
        date = place_date_birth_match.group(2).strip()
        data["Place & Date of Birth"] = f"{place}, {format_date(date)}"
    else:
        data["Place & Date of Birth"] = None

    passport_match = re.search(r"Passport Number\s*: ([A-Z0-9]+)", text)
    data["Passport Number"] = passport_match.group(1) if passport_match else None

    passport_expiry_match = re.search(r"Passport Expiry\s*: ([\d-]+)", text)
    data["Passport Expiry"] = format_date(passport_expiry_match.group(1)) if passport_expiry_match else None

    nationality_match = re.search(r"Nationality\s*: ([A-Z]+)", text)
    data["Nationality"] = nationality_match.group(1) if nationality_match else None

    gender_match = re.search(r"Gender\s*: ([A-Z]+)", text)
    data["Gender"] = gender_match.group(1) if gender_match else None

    address_match = re.search(r"Address\s*:\s*(.+)", text)
    data["Address"] = address_match.group(1).strip() if address_match else None

    occupation_match = re.search(r"Occupation\s*:\s*(.+)", text)
    data["Occupation"] = occupation_match.group(1).strip() if occupation_match else None

    guarantor_match = re.search(r"Guarantor\s*:\s*(.+)", text)
    data["Guarantor"] = guarantor_match.group(1).strip() if guarantor_match else None

    data["Jenis Dokumen"] = "ITK"

    return data

# ========================= Ekstraksi Notifikasi =========================
def extract_notifikasi(text):
    data = {
        "Nomor Keputusan": "",
        "Nama TKA": "",
        "Tempat/Tanggal Lahir": "",
        "Kewarganegaraan": "",
        "Alamat Tempat Tinggal": "",
        "Nomor Paspor": "",
        "Jabatan": "",
        "Lokasi Kerja": "",
        "Berlaku": ""
    }

    def find(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    nomor_keputusan_match = re.search(r"NOMOR\s+([A-Z0-9./-]+)", text, re.IGNORECASE)
    data["Nomor Keputusan"] = nomor_keputusan_match.group(1).strip() if nomor_keputusan_match else ""

    data["Nama TKA"] = find(r"Nama TKA\s*:\s*(.*)")
    data["Tempat/Tanggal Lahir"] = find(r"Tempat/Tanggal Lahir\s*:\s*(.*)")
    data["Kewarganegaraan"] = find(r"Kewarganegaraan\s*:\s*(.*)")
    data["Alamat Tempat Tinggal"] = find(r"Alamat Tempat Tinggal\s*:\s*(.*)")
    data["Nomor Paspor"] = find(r"Nomor Paspor\s*:\s*(.*)")
    data["Jabatan"] = find(r"Jabatan\s*:\s*(.*)")
    data["Lokasi Kerja"] = find(r"Lokasi Kerja\s*:\s*(.*)")

    valid_match = re.search(
        r"Berlaku\s*:?\s*(\d{2}[-/]\d{2}[-/]\d{4})\s*(?:s\.?d\.?|sampai dengan)?\s*(\d{2}[-/]\d{2}[-/]\d{4})",
        text, re.IGNORECASE)
    if not valid_match:
        valid_match = re.search(
            r"Tanggal Berlaku\s*:?\s*(\d{2}[-/]\d{2}[-/]\d{4})\s*s\.?d\.?\s*(\d{2}[-/]\d{2}[-/]\d{4})",
            text, re.IGNORECASE)

    if valid_match:
        start_date = format_date(valid_match.group(1))
        end_date = format_date(valid_match.group(2))
        data["Berlaku"] = f"{start_date} - {end_date}"

    return data

# ========================= Ekstraksi DKPTKA =========================
def extract_dkptka_info(full_text):
    def safe_search(pattern, text, group=1):
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(group).strip() if match else None

    def clean_multiline_text(text):
        """Clean and format multi-line text"""
        if not text:
            return None
        # Remove extra whitespace and normalize line breaks
        cleaned = re.sub(r'\s+', ' ', text.strip())
        return cleaned

    try:
        # Extract company name - multiple patterns to handle different formats
        company_name = None
        
        # Pattern 1: Look for quoted company name with PT
        company_match = re.search(r'"([^"]*PT[^"]*)"', full_text, re.IGNORECASE)
        if company_match:
            company_name = company_match.group(1).strip()
        
        # Pattern 2: Look for company name at the beginning, before "Alamat"
        if not company_name:
            # Try to find company name in the structured format
            company_match = re.search(r'(?:VIRTUE\s+DRAGON\s+NICKEL\s+INDUSTRY\s+PT\.?|[A-Z\s]+PT\.?)', full_text)
            if company_match:
                company_name = company_match.group(0).strip()
        
        # Pattern 3: Extract from the document structure (before address)
        if not company_name:
            # Look for the pattern where company name appears before "2. Alamat"
            company_match = re.search(r'"([^"]*VIRTUE[^"]*)"', full_text, re.IGNORECASE)
            if company_match:
                company_name = company_match.group(1).strip()
        
        # Pattern 4: Last resort - look for any text before "Alamat :"
        if not company_name:
            company_match = re.search(r'([A-Z][A-Z\s]*PT\.?[A-Z\s]*)\s*(?=.*Alamat\s*:)', full_text, re.IGNORECASE)
            if company_match:
                company_name = company_match.group(1).strip()

        # Extract address - handle multi-line format
        address_match = re.search(r'Alamat\s*:\s*(.*?)(?=\d+\.\s*Nomor\s+Telepon|III\.)', full_text, re.DOTALL | re.IGNORECASE)
        address = clean_multiline_text(address_match.group(1)) if address_match else None

        # Extract phone number
        phone = safe_search(r"Nomor\s+Telepon\s*:\s*([^\n]+)", full_text)

        # Extract email
        email = safe_search(r"Email\s*:\s*([^\n]+)", full_text)

        # Extract TKA name
        tka_name = safe_search(r"Nama\s+TKA\s*:\s*([^\n]+)", full_text)

        # Extract birth place and date
        birth_info = safe_search(r"Tempat\s*/?\s*Tgl?\s*Lahir\s*:\s*([^\n]+)", full_text)

        # Extract passport number
        passport = safe_search(r"Nomor\s+Paspor\s*:\s*([^\n]+)", full_text)

        # Extract position/job title
        position = safe_search(r"Jabatan\s*:\s*([^\n]+)", full_text)

        # Extract Kanim
        kanim = safe_search(r"Kanim\s+Perpanjangan\s+ITAS/ITAP\s*:\s*([^\n]+)", full_text)

        # Extract work location
        work_location = safe_search(r"Lokasi\s+Kerja\s*:\s*([^\n]+)", full_text)

        # Extract duration
        duration = safe_search(r"Jangka\s+Waktu\s*:\s*([^\n]+)", full_text)

        # Extract account number
        account_no = safe_search(r"No\s+Rekening\s*:\s*([^\n]+)", full_text)

        # Extract DKPTKA amount
        dkptka_amount = safe_search(r"DKPTKA\s+yang\s+dibayarkan\s*:\s*([^\n]+)", full_text)

        result = {
            "Nama Pemberi Kerja": company_name,
            "Alamat": address,
            "No Telepon": phone,
            "Email": email,
            "Nama TKA": tka_name,
            "Tempat/Tanggal Lahir": birth_info,
            "Nomor Paspor": passport,
            "Jabatan": position,
            "Kanim": kanim,
            "Lokasi Kerja": work_location,
            "Jangka Waktu": duration,
            "No Rekening": account_no,
            "DKPTKA": dkptka_amount,
            "Jenis Dokumen": "DKPTKA"
        }

        # Clean up any remaining formatting issues
        for key, value in result.items():
            if isinstance(value, str):
                # Remove multiple spaces and clean up formatting
                result[key] = re.sub(r'\s+', ' ', value.strip()) if value else None

    except Exception as e:
        result = {"Error": f"Data tidak lengkap atau format tidak sesuai: {str(e)}"}

    return result
