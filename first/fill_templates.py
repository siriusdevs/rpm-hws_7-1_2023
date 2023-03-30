"""File with functions for filling pages."""
from config import COMPANY_TEMPLATE, PERSON_TEMPLATE
from view import dict_to_view
from db_utils import DbHandler


def company_template(record: dict) -> str:
    """Method fills company generation page by parsed data from API.

    Args:
        record: dict - dict of values in json format to show on page.

    Returns:
        str - formed company template with parsed data.
    """
    with open(COMPANY_TEMPLATE, "r") as template:
        record["contact"].pop("id")
        record["addresses"][0].pop("id")
        return template.read().format(name=record.get("name"), email=record.get("email"), vat=record.get("vat"), \
                                      phone=record.get("phone"), country=record.get("country"), \
                                      website=record.get("website"), contact=dict_to_view(record.get("contact")), \
                                      image=record.get("image"), address=dict_to_view(record.get("addresses")[0])
                                      )


def person_template(record: dict) -> str:
    """Method fills person generation page by parsed data from API.

    Args:
        record: dict - dict of values in json format to show on page.

    Returns:
        str - formed person template with parsed data.
    """
    with open(PERSON_TEMPLATE, "r") as template:
        record["address"].pop("id")
        put_data = {
            "fname": record.get("firstname"),
            "lname": record.get("lastname"),
            "email": record.get("email")
        }
        DbHandler.insert(put_data)
        return template.read().format(fname=record.get("firstname"), email=record.get("email"), \
                                      phone=record.get("phone"), lname=record.get("lastname"), \
                                      website=record.get("website"), birthday=record.get("birthday"), \
                                      gender=record.get("gender"), \
                                      image=record.get("image"), address=dict_to_view(record.get("address"))
                                      )
