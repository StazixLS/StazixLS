from datetime import date, timedelta

def easter_date(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    month = (h + l - 7*m + 114) // 31
    day = ((h + l - 7*m + 114) % 31) + 1
    return date(year, month, day)

def _jde_to_date(jde):
    jde += 0.5
    Z = int(jde)
    F = jde - Z
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - alpha // 4
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)
    day = B - D - int(30.6001 * E) + F
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715
    return date(year, month, int(day))

def equinox_solstice(year, season):
    """season: 0=March equinox, 1=June solstice, 2=Sept equinox, 3=Dec solstice.
    Meeus low-precision algorithm, accurate to well within a day - good enough
    to know which season we're actually in, per-year, not a fixed calendar date."""
    Y = (year - 2000) / 1000
    if season == 0:
        jde0 = 2451623.80984 + 365242.37404*Y + 0.05169*Y**2 - 0.00411*Y**3 - 0.00057*Y**4
    elif season == 1:
        jde0 = 2451716.56767 + 365241.62603*Y + 0.00325*Y**2 + 0.00888*Y**3 - 0.00030*Y**4
    elif season == 2:
        jde0 = 2451810.21715 + 365242.01767*Y - 0.11575*Y**2 + 0.00337*Y**3 + 0.00078*Y**4
    else:
        jde0 = 2451900.05952 + 365242.74049*Y - 0.06223*Y**2 - 0.00823*Y**3 + 0.00032*Y**4
    return _jde_to_date(jde0)

def nth_weekday(year, month, weekday, n):
    """weekday: Monday=0 .. Sunday=6. n=1 for first, 2 for second, -1 for last."""
    if n > 0:
        d = date(year, month, 1)
        offset = (weekday - d.weekday()) % 7
        return d + timedelta(days=offset + 7 * (n - 1))
    else:
        if month == 12:
            d = date(year, 12, 31)
        else:
            d = date(year, month + 1, 1) - timedelta(days=1)
        offset = (d.weekday() - weekday) % 7
        return d - timedelta(days=offset)

# Chinese New Year: lunar calendar, published years in advance - a lookup
# table is the standard practical approach (no clean closed-form formula).
CNY_DATES = {
    2024: (2, 10), 2025: (1, 29), 2026: (2, 17), 2027: (2, 6), 2028: (1, 26),
    2029: (2, 13), 2030: (2, 3), 2031: (1, 23), 2032: (2, 11), 2033: (1, 31),
    2034: (2, 19), 2035: (2, 8), 2036: (1, 28), 2037: (2, 15),
}

def chinese_new_year(year):
    if year in CNY_DATES:
        m, d = CNY_DATES[year]
        return date(year, m, d)
    return date(year, 2, 5)  # rough fallback for out-of-table years

def get_theme(d=None):
    d = d or date.today()
    m, day = d.month, d.day
    y = d.year
    easter = easter_date(y)

    def within(target, span=1):
        return abs((d - target).days) <= span

    def within_md(month_, day_, span=1):
        return within(date(y, month_, day_), span)

    # --- movable feasts relative to Easter ---
    if within(easter, 4):
        return "easter"
    if within(easter - timedelta(days=47), 1):
        return "mardi_gras"
    if within(easter + timedelta(days=39), 1):
        return "ascension"
    pentecost = easter + timedelta(days=49)
    if within(pentecost, 1):
        return "pentecost"

    # --- lunar ---
    if within(chinese_new_year(y), 2) or within(chinese_new_year(y - 1), 2):
        return "chinese_new_year"

    # --- fixed-date holidays ---
    if within_md(1, 6, 0):
        return "epiphany"
    if within_md(2, 2, 0):
        return "candlemas"
    if within_md(2, 14, 1):
        return "valentines"
    if within_md(5, 1, 1):
        return "labor_day"
    if within_md(5, 8, 1):
        return "ve_day"
    if within_md(6, 21, 1):
        return "music_day"
    if within_md(7, 14, 1):
        return "bastille_day"
    if within_md(8, 15, 1):
        return "assumption"
    if m == 10 and day >= 24:
        return "halloween"
    if m == 11 and day == 1:
        return "toussaint"
    if within_md(11, 11, 1):
        return "armistice"
    if m == 12 and day >= 14:
        return "christmas"
    if m == 1 and 1 <= day <= 5:
        return "newyear"

    # --- Mother's/Father's day (French rule) ---
    mothers = nth_weekday(y, 5, 6, -1)  # last Sunday of May
    if mothers == pentecost:
        mothers = nth_weekday(y, 6, 6, 1)  # bumped to first Sunday of June
    if within(mothers, 0):
        return "mothers_day"
    fathers = nth_weekday(y, 6, 6, 3)  # third Sunday of June
    if within(fathers, 0):
        return "fathers_day"

    # --- astronomical seasons, computed per-year (not fixed calendar dates) ---
    spring_start = equinox_solstice(y, 0)
    summer_start = equinox_solstice(y, 1)
    autumn_start = equinox_solstice(y, 2)
    winter_start = equinox_solstice(y, 3)
    if spring_start <= d < summer_start:
        return "spring"
    if summer_start <= d < autumn_start:
        return "summer"
    if autumn_start <= d < winter_start:
        return "autumn"
    return "winter"
