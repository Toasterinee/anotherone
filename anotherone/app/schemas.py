# -*- coding: utf-8 -*-
from pydantic import BaseModel, constr, validator
from fastapi import Form
import re

class ApplicationForm(BaseModel):
    full_name: constr(min_length=2, max_length=100)
    phone: constr(min_length=10, max_length=15)
    message: constr(min_length=1, max_length=500)
    agreement: bool

    @validator("phone")
    def validate_phone(cls, v):
        if not re.match(r"^\+?\d{10,15}$", v):
            raise ValueError("Неверный формат номера телефона")
        return v

    @validator("full_name")
    def validate_full_name(cls, v):
        if not re.match(r"^[a-zA-Zа-яА-Я\s-]+$", v):
            raise ValueError("ФИО должно содержать только буквы, пробелы или дефисы")
        return v

    @validator("agreement")
    def validate_agreement(cls, v):
        if not v:
            raise ValueError("Необходимо согласиться с условиями")
        return v