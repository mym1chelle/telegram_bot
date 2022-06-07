from importlib.metadata import entry_points
from aiogram.dispatcher.filters.state import StatesGroup, State

class AddItems(StatesGroup):
    enter_name = State()
    enter_price = State()
    enter_description = State()
    enter_category_code = State()
    enter_category_name = State()
    enter_subcategory_code = State()
    enter_subcategory_name = State()