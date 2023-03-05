from __future__ import annotations
from sqlalchemy.exc import IntegrityError
import re
from app_api import db


def global_save(table, update_dictionary: dict):
    """save function"""
    for col_name in table.__table__.columns.keys():
        if col_name in update_dictionary:
            setattr(table, col_name, update_dictionary[col_name])
    try:
        db.session.add(table)
        db.session.commit()
    except IntegrityError as err:
        print(err, "err")
        pattern = re.compile(r"\((.*?)\)")
        regex = re.findall(pattern, str(err.orig))
        return {
            "status": "Failed",
            "message": [
                {
                    "field": [regex[0]],
                    "error_code": "E0004",
                    "message": "Already Exists, Please Choose another!",
                }
            ],
        }, 400
    return table
