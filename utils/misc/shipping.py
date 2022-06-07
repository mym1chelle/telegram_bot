# варианты возможных доставок

from aiogram import types

POST_REGULAR_SHIPPING = types.ShippingOption(
    id='post_reg',
    title='Почта России',
    prices=[
        types.LabeledPrice(
        label='Стандартная упаковка',
        amount=0
        ),
        types.LabeledPrice(
        label='Почтой Росии',
        amount=150_00
        )
    ]
)

POST_FAST_SHIPPING = types.ShippingOption(
    id='post_fast',
    title='DHL',
    prices=[
        types.LabeledPrice(
        label='Высокопрочная упаковка',
        amount=100_00
        ),
        types.LabeledPrice(
        label='Доставка курьером – в течении часа',
        amount=300_00)
    ]
)

PICKUP_SHIPPING = types.ShippingOption(
    id='pickup',
    title='Самовывоз',
    prices=[
        types.LabeledPrice(
        label='Самовывоз из магазина',
        amount=0)
    ]
)