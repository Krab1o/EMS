"""Add default entities

Revision ID: e9bf9acf9cc0
Revises: 3e3eaf2a7333
Create Date: 2024-04-12 15:47:35.871249+00:00

"""
from datetime import datetime, timedelta

import sqlalchemy as sa
from alembic import op
from ems.adapters.database.tables import (
    clubs,
    event_types,
    events,
    institutions,
    places,
    users,
)

# revision identifiers, used by Alembic.
revision = 'e9bf9acf9cc0'
down_revision = '2598b8ffc54a'
branch_labels = None
depends_on = None

institution_data = [
    {
        # "id": 1,
        "title": "КНиИТ",
        "description": "Факультет компьютерных наук и информационных технологий",
    },
    {
        # "id": 2,
        "title": "Психологический факультет",
        "description": None,
    },
]

user_data = [
    {
        # "id": 1,
        "last_name": "Иванов",
        "first_name": "Иван",
        "middle_name": "Иванович",
        "institution_id": 1,
        "course": None,
        "group": None,
        "role": "admin",
        "telegram": "ivanov_ivan",
        "vk": "ivanov_ivan_vk",
        "phone_number": "+79001234567",
        "email": "admin@example.com",
        "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
        "created_at": datetime.now(),
    },
    {
        # "id": 2,
        "last_name": "Петров",
        "first_name": "Пётр",
        "middle_name": "Петрович",
        "institution_id": 1,
        "course": 3,
        "group": 351,
        "role": "user",
        "telegram": "petya_pet",
        "vk": "petya_pet_vk",
        "phone_number": "+79001333777",
        "email": "user@example.com",
        "password": "04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb",
        "created_at": datetime.now(),
    }
]

event_type_data = [
    {
        # "id": 1,
        "title": "Образовательные мероприятия",
        "description": "Семинары, лекции, мастер-классы",
    },
    {
        # "id": 2,
        "title": "Культурные мероприятия",
        "description": "Выставки искусства, музыкальные фестивали",
    },
    {
        # "id": 3,
        "title": "Профессиональные мероприятия",
        "description": "Карьерные ярмарки, семинары по карьере",
    },
    {
        # "id": 4,
        "title": "Спортивные мероприятия",
        "description": "Соревнования по спорту",
    },
    {
        # "id": 5,
        "title": "Тематические мероприятия",
        "description": "Мероприятия по актуальным темам",
    },
]

d = timedelta(seconds=1)
created_at = datetime.now() - d * 11 
place_data = [
    {
        # "id": 1,
        "title": "Аудитория 310",
        "floor": 3,
        "institution_id": 1,
        "created_at": created_at + d,
    },
    {
        # "id": 2,
        "title": "Аудитория 101",
        "floor": 1,
        "institution_id": 2,
        "created_at": created_at + 2 * d,
    },
    {
        # "id": 3,
        "title": "Актовый зал X корпуса",
        "floor": 1,
        "institution_id": None,
        "created_at": created_at + 3 * d,
    },
    {
        # "id": 4,
        "title": 'Природный парк "Кумысная поляна"',
        "floor": None,
        "institution_id": None,
        "created_at": created_at + 4 * d,
    },
    {
        # "id": 5,
        "title": "Актовый зал XII корпуса",
        "floor": None,
        "institution_id": None,
        "created_at": created_at + 5 * d,
    },
]

d = timedelta(seconds=1)
created_at = datetime.now() - d * 11 
event_data = [
    {
        # "id": 1,
        "title": "Хакатон",
        "description": "Мероприятие по программированию",
        "cover_id": None,
        "status": "on_review",
        "datetime": datetime.fromisoformat("2024-05-15 10:00:00+04"),
        "dateend": datetime.fromisoformat("2024-05-17 18:00:00+04"),
        "creator_id": 1,
        "voted_yes": 0,
        "voted_no": 0,
        "type_id": 1,
        "place_id": 1,
        "created_at": created_at + d
    },
    {
        # "id": 2,
        "title": "Студвесна",
        "description": "Встреча нового учебного года",
        "cover_id": None,
        "status": "on_poll",
        "datetime": datetime.fromisoformat("2024-09-01 12:00:00+04"),
        "dateend": datetime.fromisoformat("2024-09-01 20:00:00+04"),
        "creator_id": 2,
        "voted_yes": 0,
        "voted_no": 0,
        "type_id": 2,
        "place_id": 3,
        "created_at": created_at + d * 2
    },
    {
        # "id": 3,
        "title": "Кинопоказ",
        "description": "Проекция фильма для студентов",
        "cover_id": None,
        "status": "on_review",
        "datetime": datetime.fromisoformat("2024-10-15 20:00:00+04"),
        "dateend": datetime.fromisoformat("2024-10-15 22:00:00+04"),
        "creator_id": 1,
        "voted_yes": 0,
        "voted_no": 0,
        "type_id": 3,
        "place_id": 1,
        "created_at": created_at + d * 3 
    },
    {
        # "id": 4,
        "title": "Квест для первокурсников",
        "description": "Интерактивная игра для новичков",
        "cover_id": None,
        "status": "on_poll",
        "datetime": datetime.fromisoformat("2024-09-15 18:00:00+04"),
        "dateend": datetime.fromisoformat("2024-09-15 22:00:00+04"),
        "creator_id": 2,
        "voted_yes": 0,
        "voted_no": 0,
        "type_id": 4,
        "place_id": 4,
        "created_at": created_at + d * 4
    },
    {
        # "id": 5,
        "title": "День рождения факультета",
        "description": "Празднование дня рождения факультета",
        "cover_id": None,
        "status": "on_poll",
        "datetime": datetime.fromisoformat("2024-11-15 16:00:00+04"),
        "dateend": datetime.fromisoformat("2024-11-15 20:00:00+04"),
        "creator_id": 1,
        "voted_yes": 0,
        "voted_no": 0,
        "type_id": 5,
        "place_id": 3,
        "created_at": created_at + d * 5
    },
    {
        # "id": 6,
        "title": "Утро добрым бывает",
        "description": "Благотворительный проект",
        "cover_id": None,
        "status": "on_poll",
        "datetime": datetime.fromisoformat("2024-04-15 09:00:00+04"),
        "dateend": datetime.fromisoformat("2024-04-15 10:00:00+04"),
        "creator_id": 2,
        "voted_yes": 0,
        "voted_no": 0,
        "type_id": 1,
        "place_id": 4,
        "created_at": created_at + d * 6 
    },
    {
        # "id": 7,
        "title": "Встреча с работодателями",
        "description": "Серия встреч с представителями компаний",
        "cover_id": None,
        "status": "on_poll",
        "datetime": datetime.fromisoformat("2024-06-15 15:00:00+04"),
        "dateend": datetime.fromisoformat("2024-06-15 18:00:00+04"),
        "creator_id": 1,
        "voted_yes": 0,
        "voted_no": 0,
        "type_id": 2,
        "place_id": 1,
        "created_at": created_at + d * 7
    },
    {
        # "id": 8,
        "title": "День открытых дверей",
        "description": "День, когда студенты могут посетить университет",
        "cover_id": None,
        "status": "on_poll",
        "datetime": datetime.fromisoformat("2024-09-20 10:00:00+04"),
        "dateend": datetime.fromisoformat("2024-09-20 12:00:00+04"),
        "creator_id": 2,
        "voted_yes": 0,
        "voted_no": 0,
        "type_id": 3,
        "place_id": 5,
        "created_at": created_at + d * 8
    },
    {
        # "id": 9,
        "title": "Олимпиада",
        "description": "Соревнования по различным дисциплинам",
        "cover_id": None,
        "status": "on_poll",
        "datetime": datetime.fromisoformat("2024-12-15 10:00:00+04"),
        "dateend": datetime.fromisoformat("2024-12-16 12:00:00+04"),
        "creator_id": 1,
        "voted_yes": 0,
        "voted_no": 0,
        "type_id": 4,
        "place_id": 1,
        "created_at": created_at + d * 9
    },
    {
        # "id": 10,
        "title": "Концерт",
        "description": "Музыкальное мероприятие",
        "cover_id": None,
        "status": "on_poll",
        "datetime": datetime.fromisoformat("2024-11-20 16:00:00+04"),
        "dateend": datetime.fromisoformat("2024-11-20 18:00:00+04"),
        "creator_id": 2,
        "voted_yes": 0,
        "voted_no": 0,
        "type_id": 5,
        "place_id": 3,
        "created_at": created_at + d * 10
    },
    {
        # "id": 11,
        "title": "Репетиция",
        "description": "Подготовка к концерту",
        "cover_id": None,
        "status": "on_poll",
        "datetime": datetime.fromisoformat("2024-11-18 18:00:00+04"),
        "dateend": datetime.fromisoformat("2024-11-18 19:00:00+04"),
        "creator_id": 1,
        "voted_yes": 0,
        "voted_no": 0,
        "type_id": 1,
        "place_id": 5,
        "created_at": created_at + d * 11
    }
]

d = timedelta(seconds=1)
created_at = datetime.now() - d * 5
club_data = [
    {
        # "id": 1,
        "title": "Клуб разработки",
        "description": "Секция для студентов, интересующихся разработкой программного обеспечения и технологиями.",
        "telegram": "club_programming",
        "vk": "club_programming_vk",
        "youtube": "channel_programming",
        "rutube": "channel_programming_rutube",
        "tiktok": "club_programming_tiktok",
        "created_at": created_at + d,
    },
    {
        # "id": 2,
        "title": "Клуб робототехники",
        "description": "Секция для студентов, заинтересованных в робототехнике и робототехнических проектах.",
        "telegram": "club_robotics",
        "vk": "club_robotics_vk",
        "youtube": "channel_robotics",
        "rutube": "channel_robotics_rutube",
        "tiktok": "club_robotics_tiktok",
        "created_at": created_at + d * 2,
    },
    {
        # "id": 3,
        "title": "Клуб искусства и дизайна",
        "description": "Секция для студентов, стремящихся к творчеству в области искусства и дизайна.",
        "telegram": "club_art_design",
        "vk": "club_art_design_vk",
        "youtube": "channel_art_design",
        "rutube": "channel_art_design_rutube",
        "tiktok": "club_art_design_tiktok",
        "created_at": created_at + d * 3,
    },
    {
        # "id": 4,
        "title": "Клуб науки и исследований",
        "description": "Секция для студентов, желающих участвовать в научных исследованиях и проектах.",
        "telegram": "club_science_research",
        "vk": "club_science_research_vk",
        "youtube": "channel_science_research",
        "rutube": "channel_science_research_rutube",
        "tiktok": "club_science_research_tiktok",
        "created_at": created_at + d * 4,
    },
    {
        # "id": 5,
        "title": "Клуб экологии и устойчивого развития",
        "description": "Секция для студентов, заинтересованных в экологических вопросах и устойчивом развитии.",
        "telegram": "club_ecology",
        "vk": "club_ecology_vk",
        "youtube": "channel_ecology",
        "rutube": "channel_ecology_rutube",
        "tiktok": "club_ecology_tiktok",
        "created_at": created_at + d * 5,
    }
]

def upgrade():
    op.bulk_insert(institutions, institution_data)
    op.bulk_insert(users, user_data)
    op.bulk_insert(event_types, event_type_data)
    op.bulk_insert(places, place_data)
    op.bulk_insert(events, event_data)
    op.bulk_insert(clubs, club_data)


def downgrade():
    pass
