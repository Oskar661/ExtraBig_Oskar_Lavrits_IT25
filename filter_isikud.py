import csv
from datetime import datetime

# ==================================
# SIIN SAAB OTSITAVAT KUUPÄEVA MUUTA
# ==================================
TARGET_DAY = 27     # Päev
TARGET_MONTH = 1    # Kuu (jaanuar)
# ==================================


def parse_date(date_str):
    """
    Teisendab kuupäeva datetime objektiks.
    Toetatud formaadid:
    - AAAA-KK-PP
    - PP.KK.AAAA
    Kui kuupäev puudub või on vale, tagastab None
    """
    if not date_str:
        return None

    date_str = date_str.strip()

    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            return None


def format_date(date_obj):
    """
    Vormindab kuupäeva Eesti formaati PP.KK.AAAA
    """
    if not date_obj:
        return ""
    return date_obj.strftime("%d.%m.%Y")


def calculate_age(birth, death):
    """
    Arvutab vanuse surma hetkel
    Ainult siis, kui sünni- ja surmakuupäev on olemas
    """
    if not birth or not death:
        return ""

    years = death.year - birth.year
    months = death.month - birth.month
    days = death.day - birth.day

    if days < 0:
        months -= 1
        days += 30  # lihtsustatud arvestus

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


with open(input_file, encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    header = next(reader)

    # Lisame uue veeru päisesse
    header.append("Vanus")

    result_rows = []

    for row in reader:
        # EELDUS:
        # veerg 2 = sünnikuupäev
        # veerg 3 = surmakuupäev
        birth_date = parse_date(row[2])
        death_date = parse_date(row[3])

        include = False
        age = ""

        # Kontroll: sündinud 27.01
        if birth_date and birth_date.day == TARGET_DAY and birth_date.month == TARGET_MONTH:
            include = True

        # Kontroll: surnud 27.01
        if death_date and death_date.day == TARGET_DAY and death_date.month == TARGET_MONTH:
            include = True

            # Vanust arvutame ainult siis, kui sünnikuupäev on olemas
            age = calculate_age(birth_date, death_date)

        if include:
            # Vormindame kuupäevad Eesti formaati
            row[2] = format_date(birth_date)
            row[3] = format_date(death_date)

            # Lisame vanuse veeru
            row.append(age)

            result_rows.append(row)


with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(header)
    writer.writerows(result_rows)


print("Valmis! Fail 'tulemus.csv' on loodud.")
