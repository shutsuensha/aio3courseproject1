from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app import keyboards as kb
from app.database import requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привет! Добро пожаловать в магазин Sneakers Shop',
                         reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите бренд товара', reply_markup=await kb.catalog())


@router.callback_query(F.data == ('back_reply'))
async def category_items(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.edit_text('Назад')
    await callback.message.answer('Привет! Добро пожаловать в магазин Sneakers Shop',
                         reply_markup=kb.main)



@router.callback_query(F.data.startswith('category_'))
async def category_items(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.edit_text('Выберите товар')
    await callback.message.edit_reply_markup(reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data == ('back_catalog'))
async def category_items(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.edit_text('Выберите бренд товара')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog())



@router.callback_query(F.data.startswith('item_'))
async def item_card(callback: CallbackQuery):
    await callback.answer('Вы выбрали товар')
    item = await rq.get_item(callback.data.split('_')[1])
    items_basket = await rq.get_items_basket(callback.from_user.id, item.id)

    result = []
    result.append(f'Название: {item.name}\n')
    result.append(f'Описание: {item.description}\n')
    result.append(f'Цена: {item.price} руб\n')
    result.append(f'В корзине: {len(items_basket.all())} шт.')

    await callback.message.edit_text(''.join(result))
    await callback.message.edit_reply_markup(reply_markup=await kb.item_buttons(callback.data.split('_')[1], callback.data.split('_')[2]))


@router.callback_query(F.data.startswith('back_items_'))
async def item_card(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.edit_text('Выберите товар')
    await callback.message.edit_reply_markup(reply_markup=await kb.items(callback.data.split('_')[-1]))



@router.callback_query(F.data.startswith('basketplus_'))
async def item_basket(callback: CallbackQuery):
    await callback.answer('Товар добавлен в корзину!')
    await rq.set_item_basket(callback.from_user.id, callback.data.split('_')[1])

    item = await rq.get_item(callback.data.split('_')[1])
    items_basket = await rq.get_items_basket(callback.from_user.id, item.id)

    result = []
    result.append(f'Название: {item.name}\n')
    result.append(f'Описание: {item.description}\n')
    result.append(f'Цена: {item.price} руб\n')
    result.append(f'В корзине: {len(items_basket.all())} шт.')

    await callback.message.edit_text(''.join(result))
    await callback.message.edit_reply_markup(reply_markup=await kb.item_buttons(callback.data.split('_')[1], callback.data.split('_')[2]))


@router.callback_query(F.data.startswith('basketminus_'))
async def item_basket(callback: CallbackQuery):
    item = await rq.get_item(callback.data.split('_')[1])
    basket_item = await rq.get_item_basket(callback.from_user.id, item.id)

    if basket_item:
        await callback.answer('Товар удален из корзины!')
        await rq.delete_item_basket(callback.from_user.id, item.id)

        item = await rq.get_item(callback.data.split('_')[1])
        items_basket = await rq.get_items_basket(callback.from_user.id, item.id)

        result = []
        result.append(f'Название: {item.name}\n')
        result.append(f'Описание: {item.description}\n')
        result.append(f'Цена: {item.price} руб\n')
        result.append(f'В корзине: {len(items_basket.all())} шт.')

        await callback.message.edit_text(''.join(result))
        await callback.message.edit_reply_markup(reply_markup=await kb.item_buttons(callback.data.split('_')[1], callback.data.split('_')[2]))
    else:
        await callback.answer('Товара нету в корзине!')


@router.callback_query(F.data.startswith('mybasket_'))
async def item_basket(callback: CallbackQuery):
    await callback.answer('Корзина')
    my_items = await rq.get_my_basket(callback.from_user.id)
    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
        all_price += float(item.price)
        if item.name in items_data:
            items_data[item.name] = [items_data[item.name][0] + 1, items_data[item.name][1]]
        else:
            items_data[item.name] = [1, float(item.price)]

    result = []
    
    for name, cnt_price in items_data.items():
        result.append(f'{name} - {cnt_price[0]} x {cnt_price[1]} = {cnt_price[0] * cnt_price[1]}')

    result.append(f'\nResult: {all_price}')

    await callback.message.edit_text('\n'.join(result))
    await callback.message.edit_reply_markup(reply_markup=await kb.basket_buttons(callback.data.split('_')[1], callback.data.split('_')[2]))


@router.callback_query(F.data.startswith('back_buttons_'))
async def item_card(callback: CallbackQuery):
    await callback.answer('Назад')

    item = await rq.get_item(callback.data.split('_')[-2])
    items_basket = await rq.get_items_basket(callback.from_user.id, item.id)

    result = []
    result.append(f'Название: {item.name}\n')
    result.append(f'Описание: {item.description}\n')
    result.append(f'Цена: {item.price} руб\n')
    result.append(f'В корзине: {len(items_basket.all())} шт.')

    await callback.message.edit_text(''.join(result))
    await callback.message.edit_reply_markup(reply_markup=await kb.item_buttons(callback.data.split('_')[-2], callback.data.split('_')[-1]))



#можно переписать мб
@router.message(F.text == 'Корзина')
async def mybasket(message: Message):
    my_items = await rq.get_my_basket(message.from_user.id)
    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
        all_price += float(item.price)
        if item.name in items_data:
            items_data[item.name] = [items_data[item.name][0] + 1, items_data[item.name][1]]
        else:
            items_data[item.name] = [1, float(item.price)]

    result = []
    
    for name, cnt_price in items_data.items():
        result.append(f'{name} - {cnt_price[0]} x {cnt_price[1]} = {cnt_price[0] * cnt_price[1]}')

    result.append(f'\nResult: {all_price}')
    await message.answer('\n'.join(result))