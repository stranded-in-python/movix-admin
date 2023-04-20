import uuid
from dataclasses import dataclass, field, fields
from datetime import datetime


# Mixins
@dataclass
class TimeStampsMixin:
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        if not isinstance(self.created_at, datetime):
            self.created_at = datetime.strptime(self.created_at + '00', '%Y-%m-%d %H:%M:%S.%f%z')
        if not isinstance(self.updated_at, datetime):
            self.updated_at = datetime.strptime(self.updated_at + '00', '%Y-%m-%d %H:%M:%S.%f%z')

@dataclass
class IdsMixin:
    id: uuid.UUID = field(default_factory=uuid.uuid4)


# Main classes
@dataclass
class FilmWork(IdsMixin, TimeStampsMixin):
    title: str = field(default='')
    description: str = field(default='')
    creation_date : datetime = field(default='')
    file_path: str = field(default='')
    rating: float = field(default=0.0)
    type: str = field(default='')
    

@dataclass
class Genre(IdsMixin, TimeStampsMixin):
    name: str = field(default='')
    description: str = field(default='')


@dataclass
class GenreFilmWork(IdsMixin):
    film_work_id: str = field(default='')
    genre_id: str = field(default='')
    created_at: datetime = field(default='')


@dataclass
class Person(IdsMixin, TimeStampsMixin):
    full_name: str = field(default='')


@dataclass
class PersonFilmWork(IdsMixin):
    film_work_id: str = field(default='')
    person_id: str = field(default='')
    role: str = field(default='')
    created_at: datetime = field(default='')


def class_from_args(className, argDict):
    fieldSet = {f.name for f in fields(className) if f.init}
    filteredArgDict = {k : v for k, v in argDict.items() if k in fieldSet}
    return className(**filteredArgDict)


