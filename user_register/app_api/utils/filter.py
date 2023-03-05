"""Filter"""
from app_api import db

from sqlalchemy import and_, or_
import math


def filter_one(model, field, _id):
    """filter one object"""

    obj = db.session.query(model).filter(field == _id).first()
    return obj


def filter_all_by_one(model, field, _id):
    """filter all objects with respect to field"""

    obj = db.session.query(model).filter(field == _id).all()
    return obj


def filter_in(model, obj_lis):
    """filter all objects in a list of ids"""

    objects = db.session.query(model).filter(model.id.in_(obj_lis)).all()
    return objects


def filter_all(model):
    """filter all objects"""

    objects = db.session.query(model).filter(model.is_delete == False).all()
    return objects


def model_filter(cls, filter):
    """model all in one field filter"""
    form = filter.get("value", None)
    operation = filter.get("opr", None)
    paging = filter.get("paging", {})
    columns = filter.get("columns", "id")
    page, per_page, offset = get_pages(paging)
    filters = []
    for col in form:
        sqlalchemybinaryexpression = getattr(cls, col) == form[col]
        filters.append(sqlalchemybinaryexpression)
    if operation == "eq":
        query = (
            db.session.query(cls)
            .where(
                and_(*filters),
            )
            .order_by(cls.id.desc())
            .offset(offset)
            .limit(per_page)
            .all()
        )
        count = (
            db.session.query(cls)
            .where(
                and_(*filters),
            )
            .count()
        )
        return object_paginate(
            data=query,
            count=count,
            page=page,
            per_page=per_page,
            offset=offset,
            columns=columns,
        )
    if operation == "or":
        query = (
            db.session.query(cls)
            .where(
                or_(*filters),
            )
            .order_by(cls.id.desc())
            .all()
        )
        return query


def get_pages(page_info):
    """function for get pages"""
    page = int(page_info.get("page", 1))
    per_page = int(page_info.get("per_page", 10))
    offset = page * per_page - per_page
    return page, per_page, offset


def object_paginate(**kwargs):
    """function for pagination"""
    if "data" in kwargs:
        total = math.ceil(kwargs["count"] / kwargs["per_page"])
        next_page = (
            kwargs["page"] + 1
            if kwargs["offset"] + kwargs["per_page"] < kwargs["count"]
            else None
        )
        previous = kwargs["page"] - 1 if kwargs["page"] > 1 else None
        result = dict(
            next=next_page,
            previous=previous,
            current=kwargs["page"],
            total=total,
            columns=kwargs["columns"],
            items=kwargs["data"],
            count=kwargs["count"],
        )
        return result
    return []
