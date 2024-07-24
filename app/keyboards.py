from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.requests import get_categories, get_items

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
                                     [KeyboardButton(text='Корзина')],
                                     [KeyboardButton(text='Поиск товара')],
                                     [KeyboardButton(text='Конткаты')]],
                                     resize_keyboard=True,
                                     one_time_keyboard=True,
                                     input_field_placeholder='Выберите действие...'
                                     ) 



async def item_buttons(item_id, category_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Моя корзина', callback_data=f'mybasket_{item_id}_{category_id}')],
        [InlineKeyboardButton(text='-1', callback_data=f'basketminus_{item_id}_{category_id}'),
         InlineKeyboardButton(text='+1', callback_data=f'basketplus_{item_id}_{category_id}')],
        [InlineKeyboardButton(text='Назад', callback_data=f'back_items_{item_id}_{category_id}')]])
    return keyboard



async def basket_buttons(item_id, category_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data=f'back_buttons_{item_id}_{category_id}')]])
    return keyboard


async def catalog():
    all_categories = await get_categories()

    keyboard = InlineKeyboardBuilder()

    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))

    keyboard = keyboard.adjust(2).as_markup()
    keyboard = keyboard.inline_keyboard
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='back_reply')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keyboard

async def items(category_id):
    all_items = await get_items(category_id)
    keyboard = InlineKeyboardBuilder()
    
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}_{category_id}'))
        
    keyboard = keyboard.adjust(2).as_markup()
    keyboard = keyboard.inline_keyboard
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='back_catalog')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keyboard
