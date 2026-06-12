def get_severity(percentage):

    if percentage <= 20:
        return "Low"

    elif percentage <= 50:
        return "Medium"

    elif percentage <= 80:
        return "High"

    return "Critical"


def get_severity_score(severity):

    severity_mapping = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4
    }

    return severity_mapping.get(severity, 0)