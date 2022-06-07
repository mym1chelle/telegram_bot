def converter(number):
    """Функция изменяет формат записи чисел из 10.00 в 10_00"""
    new_number = str(number).replace('.', '_')
    return new_number