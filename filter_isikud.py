import csv
import os
from datetime import datetime

# ==================================
# SIIN SAAB OTSITAVAT KUUPÄEVA MUUTA
# ==================================
TARGET_DAY = 27     # Päev
TARGET_MONTH = 1    # Kuu (jaanuar)
# ==================================


def parse_date(date_str):
    """Teisendab kuupäeva datetime objektiks"""
    if not date_str:
        return None

    date_str = date_str.strip()

    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass

    return None


def format_date(date_obj):
    """Vormindab kuupäeva Eesti formaati PP.KK.AAAA"""
    if not date_obj:
        return ""
    return date_obj.strftime("%d.%m.%Y")


def calculate_age(birth, death):
    """Arvutab vanuse surma hetkel (a, k, p)"""
    if not birth or not death:
        return ""

    years = death.year - birth.year
    months = death.month - birth.month
    days = death.day - birth.day

    if days < 0:
        months -= 1
        days += 30

    if months < 0:
        years -= 1
        months += 12

    return f"{years} a {months} k {days} p"


# =========================
# FAILIDE NIMED
# =========================
input_file = "2023-03-08_IT22_ExtraBig.csv"
output_file = "tulemus.csv"
# =========================


# =========================
# FAILI OLEMASOLU KONTROLL
# =========================
if not os.path.exists(input_file):
    print(f"VIGA: CSV faili ei leitud: '{input_file}'")
    print("Kontrolli, et fail on samas kaustas kui .py fail.")
    exit()
# =========================


print(f"Otsin isikuid kuupäevaga {TARGET_DAY:02d}.{TARGET_MONTH:02d}\n")

birth_count = 0   # mitu sünniaega leiti
death_count = 0   # mitu surmaaega leiti
total_count = 0   # mitu rida faili kirjutati

with open(input_file, encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    header = next(reader)

    # Lisame uue veeru
    header.append("Vanus")
    result_rows = []

    for row in reader:
        # ÕIGED VEERUD SINU FAILIS:
        # index 3  = Sünniaeg
        # index 11 = Surmaaeg
        birth_date = parse_date(row[3])
        death_date = parse_date(row[11])

        found_birth = False
        found_death = False
        age = ""

        # -------- SÜNNIAEG --------
        if birth_date and birth_date.day == TARGET_DAY and birth_date.month == TARGET_MONTH:
            found_birth = True
            birth_count += 1

        # -------- SURMAAEG --------
        if death_date and death_date.day == TARGET_DAY and death_date.month == TARGET_MONTH:
            found_death = True
            death_count += 1
            age = calculate_age(birth_date, death_date)

        if found_birth or found_death:
            total_count += 1

            # Vormindame kuupäevad Eesti formaati
            row[3] = format_date(birth_date)
            row[11] = format_date(death_date)

            # Lisame vanuse veeru
            row.append(age)

            result_rows.append(row)


with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(header)
    writer.writerows(result_rows)


# =========================
# TULEMUSTE VÄLJUND
# =========================
print(f"Sünniaegu leiti: {birth_count}")
print(f"Surmaaegu leiti: {death_count}")
print(f"Kokku kirjutati faili: {total_count} rida")
print(f"Tulemus salvestatud faili '{output_file}'.")
