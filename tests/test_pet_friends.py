from api import PetFriends
from settings import valid_email, valid_password, other_email, other_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого: сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить имя, тип и возраст первого элемента
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# *****************************************************************************
# Еще 10+ тестов для задания 19.7.2
# *****************************************************************************
def test_successful_add_new_pet_without_photo(name='Матроскин', animal_type='кот обычный',
                                              age='5'):
    """Проверяем, что можно добавить питомца без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_photo(pet_photo='images/cat1.jpg'):
    """Проверяем возможность обновления фото питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить фото первого элемента
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == my_pets['pets'][0]['name']
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_unsuccessful_get_api_key_for_valid_user(email='true@mail.ru', password='pass'):
    """ Проверяем что запрос api ключа возвращает статус 403 и в результате содержатся
    слова 403 Forbidden"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert '403 Forbidden' in result


def test_successful_add_new_pet_with_empty_data_without_photo(name='', animal_type='',
                                                              age=''):
    """Проверяем, что можно добавить питомца с пустыми данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_successful_add_new_pet_with_incorrect_data_without_photo(name='11', animal_type='222',
                                                                  age='старый'):
    """Проверяем, что можно добавить питомца с некорректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_successful_add_new_pet_with_identical_data_without_photo(name='11',
                                                                  animal_type='222',
                                                                  age='старый'):
    """Проверяем, что можно добавить питомца с идентичными данными"""
    test_successful_add_new_pet_with_incorrect_data_without_photo(name, animal_type, age)


def test_unsuccessful_update_self_incorrect_pet_photo(pet_photo='images/cat1.txt'):
    """Проверяем, что при попытке обновить фото в некорректном формате,
     операция завершается ошибкой"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить фото первого элемента
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 500, что-то пошло не так на сервере
        assert status == 500
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_unsuccessful_delete_self_pet_empty_id(pet_id = ''):
    """Проверяем возможность удаления питомца с пустым id,
    в результате будет получена ошибка 404"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    #  Проверяем, что в списке питомцев нет id удаляемого питомца
    assert pet_id not in my_pets.values()

    # Отправляем запрос на удаление с пустым id
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус ответа равен 404
    assert status == 404
    assert '404 Not Found' in _


def test_unsuccessful_delete_self_pet_incorrect_id(pet_id = 'абвгдеёжз1234567890'):
    """Проверяем возможность удаления питомца с некорректным id,
    однако ошибки не происходит"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    #  Проверяем, что в списке питомцев нет id удаляемого питомца
    assert pet_id not in my_pets.values()

    # Отправляем запрос на удаление с некорректным id
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус ответа равен 200
    assert status == 200


def test_unsuccessful_update_self_pet_photo_incorrect_id(pet_id = '',
                                                         pet_photo='images/cat1.jpg'):
    """Проверяем возможность обновления информации о питомце с пустым id,
    в результате будет получена ошибка 404"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.update_pet_photo(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа = 404
    assert status == 404
    assert '404 Not Found' in result


def test_unsuccessful_update_self_pet_info_incorrect_id(pet_id = '',
                                                        name='Мурзик',
                                                        animal_type='Котэ',
                                                        age=5):
    """Проверяем возможность обновления информации о питомце с пустым id,
    в результате будет получена ошибка 404"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    # Проверяем что статус ответа = 404
    assert status == 404
    assert '404 Not Found' in result


def test_successful_update_other_pet_info(name='свой среди чужих',
                                          animal_type='наш кот',
                                          age=11):
    """Проверяем возможность обновления информации о питомце,
    созданного другим пользователем"""

    # Получаем ключ other_auth_key, auth_key и запрашиваем список чужих питомцев
    _, other_auth_key = pf.get_api_key(other_email, other_password)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, other_pets = pf.get_list_of_pets(other_auth_key, "my_pets")

    # Проверяем - если список питомцев другого пользователя пустой, то добавляем нового и повторно запрашиваем список
    if len(other_pets['pets']) == 0:
        pf.add_new_pet(other_auth_key, "чужой кот", "и правда кот", "77", "images/cat1.jpg")
        _, other_pets = pf.get_list_of_pets(other_auth_key, "my_pets")

    # Пробуем обновить имя, тип и возраст первого элемента
    status, result = pf.update_pet_info(auth_key, other_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name


def test_successful_delete_other_pet():
    """Проверяем возможность удаления информации о питомце,
    созданного другим пользователем"""

    # Получаем ключ other_auth_key, auth_key и запрашиваем список чужих питомцев
    _, other_auth_key = pf.get_api_key(other_email, other_password)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, other_pets = pf.get_list_of_pets(other_auth_key, "my_pets")

    # Проверяем - если список питомцев другого пользователя пустой, то добавляем нового и повторно запрашиваем список
    if len(other_pets['pets']) == 0:
        pf.add_new_pet(other_auth_key, "чужой кот", "и правда кот", "77", "images/cat1.jpg")
        _, other_pets = pf.get_list_of_pets(other_auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = other_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список питомцев другого пользователя
    _, other_pets = pf.get_list_of_pets(other_auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in other_pets.values()
