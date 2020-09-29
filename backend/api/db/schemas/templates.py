from __future__ import annotations
from typing import List, Optional, Union, Any
from datetime import datetime
from pydantic import BaseModel, Json


class TemplateItem(BaseModel):
    id: int
    type: int
    title: str
    name: str
    platform: str
    description: Optional[str]
    logo: Optional[str]
    image: str
    notes: Optional[str]
    categories: Optional[List[str]] = []
    restart_policy: Optional[str]
    ports: Optional[List] = []
    volumes: Optional[List] = []
    env: Optional[List] = []
    devices: Optional[List] = []
    labels: Optional[List] = []
    sysctls: Optional[List] = []
    cap_add: Optional[List] = []

    class Config:
        orm_mode = True


### TEMPLATE ####


class TemplateBase(BaseModel):
    title: str
    url: str

    class Config:
        orm_mode = True


class TemplateRead(TemplateBase):
    id: int
    updated_at: datetime
    created_at: datetime


class TemplateItems(TemplateRead):
    items: List[TemplateItem] = []

    class Config:
        orm_mode = True


### TEMPLATES END ###

### TEMPLATE VARIABLES ###


class TemplateVariables(BaseModel):
    variable: str
    replacement: str

    class Config:
        orm_mode = True


class ReadTemplateVariables(TemplateVariables):
    id: int


### Export/Import ###


class Import_Export(BaseModel):
    templates: List[TemplateItems] = []
    variables: List[ReadTemplateVariables] = []


TemplateItems.update_forward_refs()


class Compose(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ComposeDL(Compose):
    description: Optional[str]
    url: Optional[str]


class ComposeWrite(Compose):
    content: Optional[Any]


class ReadCompose(Compose):
    path: str
    description: Optional[str]
    url: Optional[str]
