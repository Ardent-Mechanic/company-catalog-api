"""Расширенные тестовые данные: 15 зданий, 25 организаций, ~35 видов деятельности до 3 уровня

Revision ID: ed05973640b0
Revises: 1fe7879d23ef
Create Date: 2026-02-20 14:58:23.226608
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import logging

revision: str = "ed05973640b0"
down_revision: Union[str, Sequence[str], None] = "1fe7879d23ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

logger = logging.getLogger("alembic.runtime.migration")


def upgrade() -> None:
    logger.info(f"=== APPLYING {revision} ===  расширенные тестовые данные")

    conn = op.get_bind()

    # ─── 1. Деятельности (дерево до 3 уровня) ──────────────────────────────────────
    activity_parents = {
        # level 0
        "Еда и напитки": None,
        "Медицина и здоровье": None,
        "Авто и транспорт": None,
        "Красота и уход": None,
        "Образование": None,
        "Дом и ремонт": None,
        "IT и связь": None,
    }

    activity_children = {
        # level 1
        "Рестораны и кафе": "Еда и напитки",
        "Продуктовые магазины": "Еда и напитки",
        "Медицинские центры": "Медицина и здоровье",
        "Стоматологии": "Медицина и здоровье",
        "Автосервисы": "Авто и транспорт",
        "Шиномонтаж": "Авто и транспорт",
        "Автомойки": "Авто и транспорт",
        "Парикмахерские": "Красота и уход",
        "Салоны красоты": "Красота и уход",
        "Ногтевые студии": "Красота и уход",
        "Детские сады": "Образование",
        "Автошколы": "Образование",
        "Ремонт квартир": "Дом и ремонт",
        "Сантехника и электрика": "Дом и ремонт",
        "Веб-разработка": "IT и связь",
        "SEO и реклама": "IT и связь",
    }

    activity_grandchildren = {
        # level 2
        "Пиццерии": "Рестораны и кафе",
        "Суши и роллы": "Рестораны и кафе",
        "Кофейни": "Рестораны и кафе",
        "СТО грузовых авто": "Автосервисы",
        "Детейлинг авто": "Автосервисы",
        "Наращивание ресниц": "Салоны красоты",
        "Лазерная эпиляция": "Салоны красоты",
        "Массажные салоны": "Салоны красоты",
        "Курсы английского": "Образование",
        "Танцевальные студии": "Образование",
    }

    activity_id_map = {}

    # 1. Вставляем все корневые и промежуточные без parent_id
    for name in list(activity_parents.keys()) + list(activity_children.keys()) + list(activity_grandchildren.keys()):
        res = conn.execute(
            sa.text("INSERT INTO activity (name, parent_id) VALUES (:name, NULL) RETURNING id"),
            {"name": name}
        )
        row = res.fetchone()
        if not row:
            raise ValueError(f"Не удалось создать activity: {name}")
        activity_id_map[name] = row[0]

    # 2. Проставляем parent_id
    for child, parent in {**activity_children, **activity_grandchildren}.items():
        if parent not in activity_id_map:
            raise ValueError(f"Родитель {parent} не найден для {child}")
        conn.execute(
            sa.text("UPDATE activity SET parent_id = :pid WHERE id = :cid"),
            {"pid": activity_id_map[parent], "cid": activity_id_map[child]}
        )

    # ─── 2. Здания (15) ─────────────────────────────────────────────────────────────
    buildings = [
        {"address": "ул. Ленина, 1, Москва",          "lat": 55.7558, "lon": 37.6173},
        {"address": "пр. Мира, 15 к1",                 "lat": 55.7772, "lon": 37.6321},
        {"address": "ул. Тверская, 22 стр. 3",        "lat": 55.7635, "lon": 37.6056},
        {"address": "ул. Профсоюзная, 104",           "lat": 55.6612, "lon": 37.5064},
        {"address": "Кутузовский пр., 48",            "lat": 55.7240, "lon": 37.5160},
        {"address": "ул. Новый Арбат, 11",            "lat": 55.7522, "lon": 37.5881},
        {"address": "Ленинский пр., 45",              "lat": 55.6925, "lon": 37.5390},
        {"address": "ул. Большая Дмитровка, 7/5",     "lat": 55.7618, "lon": 37.6134},
        {"address": "ул. Маросейка, 10/1",            "lat": 55.7591, "lon": 37.6347},
        {"address": "ул. Сретенка, 25 стр. 1",        "lat": 55.7719, "lon": 37.6320},
        {"address": "ул. Мясницкая, 35",              "lat": 55.7710, "lon": 37.6502},
        {"address": "Волгоградский пр., 42 к2",       "lat": 55.7421, "lon": 37.6845},
        {"address": "ул. Земляной Вал, 33",           "lat": 55.7488, "lon": 37.6531},
        {"address": "ул. Пречистенка, 19",            "lat": 55.7442, "lon": 37.5940},
        {"address": "ул. Остоженка, 30/7",            "lat": 55.7371, "lon": 37.6005},
    ]

    building_ids = []
    for b in buildings:
        res = conn.execute(
            sa.text("INSERT INTO building (address, latitude, longitude) VALUES (:a, :lat, :lon) RETURNING id"),
            {"a": b["address"], "lat": b["lat"], "lon": b["lon"]}
        )
        row = res.fetchone()
        if not row:
            raise ValueError(f"Не удалось создать здание: {b['address']}")
        building_ids.append(row[0])

    # ─── 3. Организации (25) ────────────────────────────────────────────────────────
    organizations = [
        {"name": "ПиццаЧас 24",      "b": 0, "acts": ["Пиццерии", "Рестораны и кафе", "Доставка еды"],          "phones": ["+7(495)100-20-30", "+7(926)777-11-22"]},
        {"name": "Tokyo Roll",       "b": 1, "acts": ["Суши и роллы", "Рестораны и кафе"],                     "phones": ["+7(495)333-44-55"]},
        {"name": "Гастроном №1",     "b": 2, "acts": ["Продуктовые магазины"],                                 "phones": ["+7(499)123-45-67"]},
        {"name": "МедЭксперт",       "b": 3, "acts": ["Медицинские центры", "Стоматологии"],                   "phones": ["+7(495)777-00-11", "+7(495)777-00-12"]},
        {"name": "Грузовик Сервис",  "b": 4, "acts": ["СТО грузовых авто", "Автосервисы"],                     "phones": ["+7(926)555-22-11"]},
        {"name": "Detail King",      "b": 5, "acts": ["Детейлинг авто", "Автомойки"],                          "phones": ["+7(495)888-99-00"]},
        {"name": "Шины Экспресс",    "b": 6, "acts": ["Шиномонтаж", "Автосервисы"],                            "phones": ["+7(499)222-33-44"]},
        {"name": "Lash & Brow",      "b": 7, "acts": ["Наращивание ресниц", "Салоны красоты", "Лазерная эпиляция"], "phones": ["+7(495)555-66-77"]},
        {"name": "Drive School",     "b": 8, "acts": ["Автошколы"],                                            "phones": ["+7(495)999-88-77"]},
        {"name": "Солнышко 365",     "b": 9, "acts": ["Детские сады"],                                         "phones": ["+7(499)111-22-33"]},
        {"name": "Coffee & Croissant","b": 10,"acts": ["Кофейни", "Рестораны и кафе"],                         "phones": ["+7(495)200-30-40"]},
        {"name": "Smile Dental",     "b": 11,"acts": ["Стоматологии", "Медицинские центры"],                   "phones": ["+7(495)600-70-80"]},
        {"name": "Relax & SPA",      "b": 12,"acts": ["Массажные салоны", "Салоны красоты"],                   "phones": ["+7(495)300-40-50"]},
        {"name": "English House",    "b": 13,"acts": ["Курсы английского", "Образование"],                     "phones": ["+7(499)400-50-60"]},
        {"name": "Fix Master",       "b": 14,"acts": ["Ремонт квартир", "Сантехника и электрика"],             "phones": ["+7(495)900-10-20"]},
        {"name": "Pixel Craft",      "b": 0, "acts": ["Веб-разработка", "SEO и реклама"],                     "phones": ["+7(926)111-22-33"]},
        {"name": "Family Clinic",    "b": 1, "acts": ["Медицинские центры"],                                   "phones": ["+7(495)222-33-44"]},
        {"name": "Auto Shine",       "b": 2, "acts": ["Автомойки", "Детейлинг авто"],                          "phones": ["+7(499)333-44-55"]},
        {"name": "Beauty Queen",     "b": 3, "acts": ["Парикмахерские", "Салоны красоты"],                     "phones": ["+7(495)444-55-66"]},
        {"name": "Little Genius",    "b": 4, "acts": ["Детские сады"],                                         "phones": ["+7(926)555-66-77"]},
        {"name": "Speed Pizza",      "b": 5, "acts": ["Пиццерии", "Доставка еды"],                             "phones": ["+7(495)666-77-88"]},
        {"name": "Tech Support 24",  "b": 6, "acts": ["IT и связь", "Веб-разработка"],                         "phones": ["+7(499)777-88-99"]},
        {"name": "Nails & Lashes",   "b": 7, "acts": ["Ногтевые студии", "Наращивание ресниц"],                "phones": ["+7(495)888-99-00"]},
        {"name": "Pro Drive",        "b": 8, "acts": ["Автошколы", "Образование"],                             "phones": ["+7(926)999-00-11"]},
        {"name": "Здоровье Плюс",    "b": 9, "acts": ["Медицинские центры", "Стоматологии", "Массажные салоны"],"phones": ["+7(495)111-22-33", "+7(926)222-33-44"]},
    ]

    for org in organizations:
        bid = building_ids[org["b"]]

        res = conn.execute(
            sa.text("INSERT INTO organization (name, building_id) VALUES (:n, :bid) RETURNING id"),
            {"n": org["name"], "bid": bid}
        )
        row = res.fetchone()
        if not row:
            raise ValueError(f"Не удалось создать организацию: {org['name']}")
        oid = row[0]

        # телефоны
        for ph in org["phones"]:
            conn.execute(
                sa.text("INSERT INTO phone_number (phone, organization_id) VALUES (:p, :oid)"),
                {"p": ph, "oid": oid}
            )

        # виды деятельности
        for act_name in org["acts"]:
            if act_name in activity_id_map:
                conn.execute(
                    sa.text("""
                        INSERT INTO organization_activity (organization_id, activity_id)
                        VALUES (:oid, :aid)
                        ON CONFLICT DO NOTHING
                    """),
                    {"oid": oid, "aid": activity_id_map[act_name]}
                )
            else:
                logger.warning(f"Вид деятельности не найден: {act_name} для {org['name']}")


def downgrade() -> None:
    logger.warning(f"=== REVERTING {revision} ===")
    op.execute("DELETE FROM organization_activity")
    op.execute("DELETE FROM phone_number")
    op.execute("DELETE FROM organization")
    op.execute("DELETE FROM building")
    op.execute("DELETE FROM activity")