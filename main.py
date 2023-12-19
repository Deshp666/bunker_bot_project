import telebot
from telebot import types
import json
import time
import base64
import requests
from BunkerSpecifications_3qqwwe20 import *
from random import *
token = '6507525660:AAE_OXfad52Zr03ocCQOcLY__Ss1LcuSUzw'
bunker_bot = telebot.TeleBot(token)


class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models',
                                headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }
        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run',
                                 headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(
                self.URL + 'key/api/v1/text2image/status/' + request_id,
                headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            attempts -= 1
            time.sleep(delay)


def create_image(prompt: str, player_id: int):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '159666A951FB95BF93EE4EF25B2D6D45',
                        '6D8D2BF9E352CDA7C345D5D6C9D43EAB')
    model_id = api.get_model()
    uuid = api.generate(
        prompt,
        model_id)
    images = api.check_generation(uuid)
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    with open(f"{player_id}.jpg", "wb") as file:
        file.write(image_data)


def dict_to_str(dictionary: dict) -> str:
    formatted_string = ''
    for key, value in dictionary.items():
        formatted_string += f'    "{key}": "{value}",\n'
    formatted_string = formatted_string.rstrip(',\n')
    return formatted_string.replace('"', '')


def last_letter(number: int, word: str):
    converter = {
        'месяцы': ['месяцев', 'месяц', 'месяца'],
        'годы': ['лет', 'год', 'года'],
        'люди': ['человек', 'человек', 'человека']
    }
    if str(number)[-1] in ['0', '5', '6', '7', '8', '9'] or 11 <= number <= 20:
        return converter[word][0]
    elif str(number)[-1] == '1':
        return converter[word][1]
    else:
        return converter[word][2]


def make_role() -> dict:
    tier = 0
    while not 45 <= tier <= 55:
        fact_role_first = fact_role_second = 0
        movement_role_first = movement_role_second = 0

        tier = 0

        temp_age = randint(18, 80)
        temp_job_age = temp_age - randint(18, temp_age)
        temp_hobby_age = temp_age - randint(18, temp_age)
        age = f'{temp_age} {last_letter(temp_age, "годы")}'
        job_experience = f'{temp_job_age} {last_letter(temp_job_age, "годы")}'
        hobby_experience = f'{temp_hobby_age} {last_letter(temp_hobby_age, "годы")}'

        gender_role = choice(list(gender.keys()))
        tier += gender[gender_role]

        profession_role = choice(list(profession.keys()))
        tier += profession[profession_role]

        health_role = choice(list(health.keys()))
        health_stage_role = choice(list(health_stages.keys()))
        tier += health[health_role]
        tier += health_stages[health_stage_role]

        phobia_role = choice(list(phobia.keys()))
        tier += phobia[phobia_role]

        hobby_role = choice(list(hobby.keys()))
        tier += hobby[hobby_role]

        baggage_role = choice(list(baggage.keys()))
        tier += baggage[baggage_role]

        while fact_role_first == fact_role_second:
            fact_role_first = choice(list(fact.keys()))
            fact_role_second = choice(list(fact.keys()))
        tier += fact[fact_role_first]
        tier += fact[fact_role_second]

        while movement_role_first == movement_role_second:
            movement_role_first = choice(list(movement.keys()))
            movement_role_second = choice(list(movement.keys()))
        tier += movement[movement_role_first][0]
        tier += movement[movement_role_second][0]

    del profession[profession_role]
    if gender_role == 'Робот-андроид':
        del gender[gender_role]
        del healthRobot[health_role]
    else:
        del health[health_role]
    del phobia[phobia_role]
    del hobby[hobby_role]
    del baggage[baggage_role]
    del fact[fact_role_first]
    del fact[fact_role_second]
    del movement[movement_role_first]
    del movement[movement_role_second]

    return {
        'Возраст': age,
        'Пол': gender_role,
        'Профессия': profession_role,
        'Стаж профессии': job_experience,
        'Здоровье': health_role,
        'Стадия болезни (если применима)': health_stage_role,
        'Фобия': phobia_role,
        'Хобби': hobby_role,
        'Стаж хобби': hobby_experience,
        'Багаж': baggage_role,
        'Факт №1': fact_role_first,
        'Факт №2': fact_role_second,
        'Карта действия №1': movement_role_first,
        'Карта действия №2': movement_role_second,
        'Особенности': []
    }


class Game:
    round_converter = {
        4: ['first', 'skip', 'skip', 'kick', 'kick'],
        5: ['first', 'skip', 'kick', 'kick', 'kick'],
        6: ['first', 'skip', 'kick', 'kick', 'kick'],
        7: ['first', 'kick', 'kick', 'kick', 'kick'],
        8: ['first', 'kick', 'kick', 'kick', 'kick'],
        9: ['first', 'kick', 'kick', 'kick', 'kick_2'],
        10: ['first', 'kick', 'kick', 'kick', 'kick_2'],
        11: ['first', 'kick', 'kick', 'kick_2', 'kick_2'],
        12: ['first', 'kick', 'kick', 'kick_2', 'kick_2'],
        13: ['first', 'kick', 'kick_2', 'kick_2', 'kick_2'],
        14: ['first', 'kick', 'kick_2', 'kick_2', 'kick_2']
    }
    characteristic_converter = {
        'Профессия': profession,
        'Здоровье': health,
        'Фобия': phobia,
        'Хобби': hobby,
        'Багаж': baggage,
    }

    def __init__(self, player_list: list):
        self.player_list = player_list
        self.player_speak_time_sec = 2
        self.round_count = 0
        self.current_round = 1
        self.data = {
            'disaster': {},
            'bunker': {},
            'player_cards': {}
        }

    def make_bunker(self) -> dict:
        temp_bunker_time = randint(1, 73)
        bunker_time = f'Запасы питания на {temp_bunker_time} {last_letter(temp_bunker_time, "месяцы")}'
        bunker_area = f'Площадь бункера: {randrange(30, 405, 5)} кв.м.'
        bunker_slots = len(self.player_list) // 2 + 1

        return {
            'Время': bunker_time,
            'Площадь': bunker_area,
            'Слоты': bunker_slots,
            'Особенности': []
        }

    def make_disaster(self) -> dict:
        disaster = choice(disasters)
        population = f'Остаток населения {randint(10, 100)} %'
        destruction = f'Разрушение городов {randint(10, 100)} %'

        return {
            'Катастрофа': disaster,
            'Население': population,
            'Разрушение': destruction,
            'Особенности': []
        }

    def create_game(self):
        for player in self.player_list:
            self.data['player_cards'][player] = make_role()
        self.data['bunker'] = self.make_bunker()
        self.data['disaster'] = self.make_disaster()

    def play_movement_card(self, card: dict, user_id: int, card_marker: list, selected_player_first=None,
                           selected_player_second=None, selected_fact=None):
        if card_marker[0] == 'заменить':
            if card_marker[1] == 'себе':
                if card_marker[2] == 'рандом':
                    card_marker[2] = choice(list(self.characteristic_converter.keys()))
                new_characteristic = choice(list(self.characteristic_converter[card_marker[2]].keys()))
                self.data['player_cards'][user_id][card_marker[2]] = new_characteristic
                del self.characteristic_converter[card_marker[2]][new_characteristic]
            elif card_marker[1] == 'другому':
                if card_marker[2] == 'рандом':
                    card_marker[2] = choice(list(self.characteristic_converter.keys()))
                new_characteristic = choice(list(self.characteristic_converter[card_marker[2]].keys()))
                self.data['player_cards'][selected_player_first][card_marker[2]] = new_characteristic
                del self.characteristic_converter[card_marker[2]][new_characteristic]
            elif card_marker[1] == 'всем':
                if card_marker[2] == 'рандом':
                    card_marker[2] = choice(list(self.characteristic_converter.keys()))
                for player in self.player_list:
                    new_characteristic = choice(list(self.characteristic_converter[card_marker[2]].keys()))
                    self.data['player_cards'][player][card_marker[2]] = new_characteristic
                    del self.characteristic_converter[card_marker[2]][new_characteristic]
        if card_marker[0] == 'доп экстра':
            if card_marker[1] == 'бункер':
                self.data['bunker']['Особенности'].append(card)
                print(card)
            if card_marker[1] == 'себе':
                self.data['player_cards'][user_id]['Особенности'].append(card)
                print(f'Игрок {user_id} {card}')
        if card_marker[0] == 'узнать':
            if card_marker[1] == 'другому':
                if card_marker[2] == 'Факт':
                    print(self.data['player_cards'][selected_player_first][selected_fact])
                else:
                    print(self.data['player_cards'][selected_player_first][card_marker[2]])
        if card_marker[0] == 'доп характеристика':
            if card_marker[1] == 'любой':
                if card_marker[2] in ['Профессия', 'Хобби']:
                    new_characteristic = choice(list(self.characteristic_converter[card_marker[2]].keys()))
                    temp_characteristic_age = (
                            self.data['player_cards'][selected_player_first]['Возраст']
                            - randint(18, int(self.data['player_cards'][selected_player_first]['Возраст']))
                    )
                    new_characteristic_age = f'{temp_characteristic_age} {last_letter(temp_characteristic_age, "годы")}'
                    self.data['player_cards'][selected_player_first][card_marker[3]] = new_characteristic
                    self.data['player_cards'][selected_player_first][card_marker[4]] = new_characteristic_age

                elif card_marker[2] == 'Здоровье':
                    new_characteristic = choice(list(health.keys()))
                    new_characteristic_stage = choice(list(health_stages.keys()))
                    self.data['player_cards'][selected_player_first][card_marker[3]] = new_characteristic
                    self.data['player_cards'][selected_player_first][card_marker[4]] = new_characteristic_stage
                else:
                    new_characteristic = choice(list(self.characteristic_converter[card_marker[2]].keys()))
                    self.data['player_cards'][selected_player_first][card_marker[3]] = new_characteristic
        if card_marker[0] == 'поменяться':
            if card_marker[1] == 'с другим':
                self.data['player_cards'][selected_player_first][card_marker[2]], self.data['player_cards'][user_id][
                    card_marker[2]] = \
                    self.data['player_cards'][user_id][card_marker[2]], \
                    self.data['player_cards'][selected_player_first][card_marker[2]]
            if card_marker[1] == '2 игрока':
                (
                    self.data['player_cards'][selected_player_first][card_marker[2]],
                    self.data['player_cards'][selected_player_second][card_marker[2]]
                ) = (
                    self.data['player_cards'][selected_player_second][card_marker[2]],
                    self.data['player_cards'][selected_player_first][card_marker[2]]
                )

        if card_marker[0] == 'перемешать':
            shuffled_characteristics = []
            for player in self.player_list:
                shuffled_characteristics.append(self.data['player_cards'][player][card_marker[1]])
            for player in self.player_list:
                new_characteristic = choice(shuffled_characteristics)
                self.data['player_cards'][player][card_marker[1]] = new_characteristic
                shuffled_characteristics.remove(new_characteristic)
        if card_marker[0] == 'убрать профессию':
            self.data['player_cards'][selected_player_first]['Профессия'] = 'Безработный'
        if card_marker[0] == 'новая карта':
            self.data['player_cards'][selected_player_first] = make_role()

        for player_card in list(self.data['player_cards'][user_id].keys()):
            if self.data['player_cards'][user_id][player_card] == card:
                del self.data['player_cards'][user_id][player_card]


bunker_game = None
current_player = None
players_id = []
players_nicknames = {}
selected_player = None
current_card = None
selected_fact = None
first_selected_player = None
second_selected_player = None


def say_hello(message):
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton('Начать игру', callback_data='start_game')
    rules_button = types.InlineKeyboardButton('Правила', callback_data='rules', url="https://razvivashka.site/bunker/")
    markup.row(start_button)
    markup.add(rules_button)
    bunker_bot.send_message(message.chat.id, 'Привет! Я бот для ведения игры "Бункер". '
                                             'Перед началом игры, каждый участник должен нажать '
                                             'на мою аватарку и начать со мной диалог.', reply_markup=markup)


def return_button(markup) -> types.InlineKeyboardMarkup:
    button_return = types.InlineKeyboardButton('Назад', callback_data='return')
    return markup.add(button_return)


def one_more_time_button() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    one_more_time = types.InlineKeyboardButton('Начать заново', callback_data='start_game')
    markup = markup.add(one_more_time)
    return markup


def all_players_button(exception=False, second_player=False) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    if exception is False:
        for player in players_id:
            button_player = types.InlineKeyboardButton(players_nicknames[player], callback_data="!" + str(player))
            markup.add(button_player)
    else:
        if second_player:
            for player in players_id:
                button_player = types.InlineKeyboardButton(players_nicknames[player], callback_data="#" + str(player))
                markup.add(button_player)
        else:
            for player in players_id:
                if player != current_player:
                    button_player = types.InlineKeyboardButton(players_nicknames[player],
                                                               callback_data="!" + str(player))
                    markup.add(button_player)
    return markup


def start_game_message(message):
    markup = types.InlineKeyboardMarkup()
    take_part = types.InlineKeyboardButton('Принять участие', callback_data='id_registration')
    first_turn = types.InlineKeyboardButton('Первый раунд', callback_data='first_turn')
    markup.add(take_part)
    markup.add(first_turn)
    return_button(markup)
    bunker_bot.send_message(message.chat.id,
                            'Каждый игрок должен нажать на кнопку "Принять участие". '
                            'После того, как все игроки нажмут на кнопку, '
                            'кто-то должен нажать на кнопку "Первый ход"',
                            reply_markup=markup)


def round_buttons(round_count) -> types.InlineKeyboardMarkup:
    if round_count < 4:
        markup = types.InlineKeyboardMarkup()
        next_round = types.InlineKeyboardButton('Следующих ход', callback_data='next_round')
        end_game = types.InlineKeyboardButton('Завершить игру', callback_data='end_game')
        movement_card = types.InlineKeyboardButton('Карта действия', callback_data='movement_card')
        markup.add(movement_card)
        markup.add(next_round)
        markup.add(end_game)
        return markup
    elif round_count == 4:
        markup = types.InlineKeyboardMarkup()
        end_game = types.InlineKeyboardButton('Завершить игру', callback_data='end_game')
        movement_card = types.InlineKeyboardButton('Карта действия', callback_data='movement_card')
        markup.add(movement_card)
        markup.add(end_game)
        return markup


def first_or_second_buttons() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    first_button = types.InlineKeyboardButton('Карта действия 1', callback_data='first_card')
    second_button = types.InlineKeyboardButton('Карта действия 2', callback_data='second_card')
    markup.row(first_button, second_button)
    return markup


def facts_button() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    first_fact = types.InlineKeyboardButton('Факт №1', callback_data='first_fact')
    second_fact = types.InlineKeyboardButton('Факт №2', callback_data='second_fact')
    markup.row(first_fact, second_fact)
    return markup


def rounds_message(round_activity: str) -> str:
    if round_activity == 'kick':
        return 'На этом ходу вы должны открыть одну характеристику и выгнать одного игрока голосованием.'
    elif round_activity == 'kick_2':
        return 'На этом ходу вы должны открыть одну характеристику и выгнать двух игроков голосованием.'
    elif round_activity == 'skip':
        return 'На этом ходы вы должны рассказать одну свою характеристику.'
    elif round_activity == 'first':
        return 'На первом ходу вы должны рассказать про себя и открыть две характеристики.'


def characteristics_for_prompt(player_card: dict) -> str:
    player_age = player_card['Возраст']
    player_gender = player_card['Пол']
    player_profession = player_card['Профессия']
    player_health = player_card['Здоровье']
    player_characteristics = f'Возраст - {player_age}, Пол - {player_gender}, ' \
                             f'Профессия - {player_profession}, Здоровье - {player_health}'
    return player_characteristics


def card_creator(players_id: int | list[int]):
    for player_id in players_id:
        player_card = bunker_game.data['player_cards'][player_id]
        player_characteristics = characteristics_for_prompt(player_card)
        prompt = f"Сгенерируй в мультяшном стиле дисней 2д, {player_characteristics}"
        create_image(prompt, player_id)
        with open(f'{player_id}.jpg', 'rb') as avatar_photo:
            bunker_bot.send_photo(chat_id=player_id, photo=avatar_photo,
                                  caption=f"Ваша карточка:\n{dict_to_str(player_card)}")


@bunker_bot.message_handler(commands=['start'])
def hello(message):
    say_hello(message)
    bunker_bot.delete_message(message.chat.id, message.message_id)


@bunker_bot.callback_query_handler(
    func=lambda callback: callback.data in ('rules', 'start_game', 'id_registration', 'return')
)
def informational_messages(callback):
    global players_id
    if callback.data == 'start':
        say_hello(callback.message)
    elif callback.data == 'return':
        bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
        players_id = []
        say_hello(callback.message)
    elif callback.data == 'rules':
        bunker_bot.send_message(callback.from_user.id)
    elif callback.data == 'start_game':
        bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
        start_game_message(callback.message)
    elif callback.data == 'id_registration' and callback.from_user.id not in players_id:
        players_id.append(callback.from_user.id)
        players_nicknames[callback.from_user.id] = callback.from_user.username
        bunker_bot.send_message(callback.from_user.id, 'Вы зарегистрированы✅')
        print(players_id)


@bunker_bot.callback_query_handler(
    func=lambda callback: callback.data in ('first_turn', 'next_round', 'end_game')
)
def game_messages(callback):
    global bunker_game
    global players_id
    global players_nicknames
    one_round = 1
    final_round = 4
    end_game_round = 5
    if len(players_id) > 4:
        if bunker_game is None:
            bunker_game = Game(players_id)
            bunker_game.create_game()
        if callback.data == 'first_turn':
            bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
            card_creator(players_id)
            bunker_bot.send_message(callback.message.chat.id,
                                    f"Игра началась.\nВаш бункер:\n{dict_to_str(bunker_game.data['bunker'])}\n"
                                    f"Катастрофа:\n{dict_to_str(bunker_game.data['disaster'])}")
            # Нужно изменить с фёрст на бункер раунд каунт
            bunker_bot.send_message(callback.message.chat.id,
                                    f"Раунд №{bunker_game.current_round}\n{rounds_message('first')}",
                                    reply_markup=round_buttons(bunker_game.round_count))
            bunker_game.round_count += one_round
            bunker_game.current_round += one_round
        elif callback.data == 'next_round' and bunker_game.round_count < final_round:
            bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
            bunker_bot.send_message(callback.message.chat.id,
                                    f"Раунд №{bunker_game.current_round}\n{rounds_message('kick')}",
                                    reply_markup=round_buttons(bunker_game.round_count))
            bunker_game.round_count += one_round
            bunker_game.current_round += one_round
        elif bunker_game.round_count == final_round:
            bunker_bot.send_message(callback.message.chat.id,
                                    f"Раунд №{bunker_game.current_round}\nВ этом раунде решиться, "
                                    f"кто пройдет в бункер и выживет!\n{rounds_message('kick')}",
                                    reply_markup=round_buttons(bunker_game.round_count))
            bunker_game.round_count += one_round
            bunker_game.current_round += one_round
            bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
        elif callback.data == 'end_game':
            bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
            if bunker_game.round_count < final_round:
                bunker_bot.send_message(callback.message.chat.id, f"Игра завершена досрочно.")
                bunker_game = None
                players_id = []
                start_game_message(callback.message)
            elif bunker_game.round_count == end_game_round:
                bunker_game = None
                players_id = []
                bunker_bot.send_message(callback.message.chat.id,
                                        f"Игра окончена! Спасибо, что провели игру с нашим ботом.\nХотите еще?",
                                        reply_markup=one_more_time_button())
    else:
        bunker_bot.send_message(callback.message.chat.id, 'Недостаточное количество игроков.')


@bunker_bot.callback_query_handler(func=lambda callback: (
        callback.data in ('movement_card', 'first_card', 'second_card', 'first_fact', 'second_fact') or
        callback.data[0] in ('!', '#')
    ))
def movement_card_processing(callback):
    global current_player, first_selected_player, second_selected_player, selected_player
    global current_card
    global selected_fact
    global bunker_game
    next_message = 1
    another_button = all_players_button(exception=True)
    any_button = all_players_button()
    second_player_button = all_players_button(exception=True, second_player=True)
    if callback.data == 'movement_card':
        current_player = callback.from_user.id
        bunker_bot.send_message(callback.message.chat.id, 'Выберите карту действия:',
                                reply_markup=first_or_second_buttons())
    elif callback.data == 'first_card':
        current_card = 'Карта действия №1'
        bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'second_card':
        current_card = 'Карта действия №2'
        bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'first_fact':
        selected_fact = 'Факт №1'
    elif callback.data == 'second_fact':
        selected_fact = 'Факт №2'

    if current_card is not None:
        if movement2[bunker_game.data['player_cards'][current_player][current_card]][1][1] == 'другому' or \
                movement2[bunker_game.data['player_cards'][current_player][current_card]][1][0] == 'убрать профессию':
            bunker_bot.send_message(callback.message.chat.id, 'Выберите игрока', reply_markup=another_button)
            if callback.data[0] == '!':
                selected_player = int(callback.data.replace('!', ''))
                bunker_game.play_movement_card(bunker_game.data['player_cards'][current_player][current_card],
                                               current_player,
                                               movement2[
                                                   bunker_game.data['player_cards'][current_player][current_card]][1],
                                               selected_player)
                bunker_bot.send_message(selected_player,
                                        f"Ваша новая карточка:"
                                        f"\n{dict_to_str(bunker_game.data['player_cards'][selected_player])}")
                current_card = None
                selected_fact = None
                bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
                bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id + next_message)

        elif movement2[bunker_game.data['player_cards'][current_player][current_card]][1][1] == 'другому' and \
                movement2[bunker_game.data['player_cards'][current_player][current_card]][1][0] == 'узнать':
            bunker_bot.send_message(callback.message.chat.id, 'Выберите игрока', reply_markup=another_button)
            if callback.data[0] == '!':
                selected_player = int(callback.data.replace('!', ''))
                if movement2[bunker_game.data['player_cards'][current_player][current_card]][1][2] == 'Факт':
                    bunker_bot.send_message(callback.message.chat.id, 'Выберите факт', reply_markup=facts_button())
                    bunker_bot.send_message(current_player,
                                            f"Факт выбранного игрока:"
                                            f"\n{bunker_game.data['player_cards'][selected_player][selected_fact]}")
                    current_card = None
                    selected_fact = None
                    bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
                    bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id + next_message)
                else:
                    characteristic = bunker_game.data['player_cards'][selected_player][
                        movement2[bunker_game.data['player_cards'][current_player][current_card][1][2]]]
                    bunker_bot.send_message(current_player,
                                            f"Характеристика выбранного игрока:"
                                            f"\n{bunker_game.data['player_cards'][selected_player][characteristic]}")
                    current_card = None
                    selected_fact = None
                    bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
                    bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id + next_message)

        elif movement2[bunker_game.data['player_cards'][current_player][current_card]][1][1] == 'себе':
            bunker_game.play_movement_card(bunker_game.data['player_cards'][current_player][current_card],
                                           current_player,
                                           movement2[bunker_game.data['player_cards'][current_player][current_card]][1])
            bunker_bot.send_message(current_player,
                                    f"Ваша новая карточка:"
                                    f"\n{dict_to_str(bunker_game.data['player_cards'][current_player])}")
            current_card = None
            selected_fact = None
            bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
            bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id + next_message)

        elif movement2[bunker_game.data['player_cards'][current_player][current_card]][1][1] == 'всем' or \
                movement2[bunker_game.data['player_cards'][current_player][current_card]][1][0] == 'всем' or\
                movement2[bunker_game.data['player_cards'][current_player][current_card]][1][0] == 'перемешать':
            bunker_game.play_movement_card(bunker_game.data['player_cards'][current_player][current_card],
                                           current_player,
                                           movement2[bunker_game.data['player_cards'][current_player][current_card]][1])
            for player_id in players_id:
                bunker_bot.send_message(player_id,
                                        f"Ваша новая карточка:"
                                        f"\n{dict_to_str(bunker_game.data['player_cards'][player_id])}")
            current_card = None
            selected_fact = None
            bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)

        elif movement2[bunker_game.data['player_cards'][current_player][current_card]][1][1] == 'бункер':
            bunker_game.play_movement_card(bunker_game.data['player_cards'][current_player][current_card],
                                           current_player,
                                           movement2[bunker_game.data['player_cards'][current_player][current_card]][1])
            bunker_bot.send_message(callback.message.chat.id,
                                    f"Ваш новый бункер:\n{dict_to_str(bunker_game.data['bunker'])}")
            current_card = None
            selected_fact = None

        elif movement2[bunker_game.data['player_cards'][current_player][current_card]][1][1] == 'любой':
            bunker_bot.send_message(callback.message.chat.id, 'Выберите игрока', reply_markup=any_button)
            if callback.data[0] == '!':
                selected_player = int(callback.data.replace('!', ''))
                bunker_game.play_movement_card(bunker_game.data['player_cards'][current_player][current_card],
                                               current_player,
                                               movement2[
                                                   bunker_game.data['player_cards'][current_player][current_card]][1],
                                               selected_player)
                bunker_bot.send_message(selected_player,
                                        f"Ваша новая карточка:"
                                        f"\n{dict_to_str(bunker_game.data['player_cards'][selected_player])}")
                bunker_bot.send_message(current_player,
                                        f"Ваша карточка:"
                                        f"\n{dict_to_str(bunker_game.data['player_cards'][current_player])}")
                current_card = None
                selected_fact = None
                bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
                bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id + next_message)
        elif movement2[bunker_game.data['player_cards'][current_player][current_card]][1][0] == 'новая карта':
            bunker_bot.send_message(callback.message.chat.id, 'Выберите игрока', reply_markup=any_button)
            bunker_game.play_movement_card(bunker_game.data['player_cards'][current_player][current_card],
                                           current_player,
                                           movement2[
                                               bunker_game.data['player_cards'][current_player][current_card]][1],
                                           selected_player)
            card_creator(selected_player)
            bunker_bot.send_message(current_player,
                                    f"Ваша карточка:"
                                    f"\n{dict_to_str(bunker_game.data['player_cards'][current_player])}")
            if callback.data[0] == '!':
                selected_player = int(callback.data.replace('!', ''))

        elif movement2[bunker_game.data['player_cards'][current_player][current_card]][1][1] == 'с другим':
            bunker_bot.send_message(callback.message.chat.id, 'Выберите игрока', reply_markup=another_button)
            if callback.data[0] == '!':
                selected_player = int(callback.data.replace('!', ''))
                bunker_game.play_movement_card(bunker_game.data['player_cards'][current_player][current_card],
                                               current_player,
                                               movement2[
                                                   bunker_game.data['player_cards'][current_player][current_card]][1],
                                               selected_player)
                bunker_bot.send_message(selected_player,
                                        f"Ваша новая карточка:"
                                        f"\n{dict_to_str(bunker_game.data['player_cards'][selected_player])}")
                bunker_bot.send_message(current_player,
                                        f"Ваша новая карточка:"
                                        f"\n{dict_to_str(bunker_game.data['player_cards'][current_player])}")
                current_card = None
                selected_fact = None
                bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
                bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id + next_message)

        elif movement2[bunker_game.data['player_cards'][current_player][current_card]][1][1] == '2 игрока':
            bunker_bot.send_message(callback.message.chat.id,
                                    'Выберите первого игрока, если хотите выбрать себя, то выберите сейчас.',
                                    reply_markup=any_button)
            if callback.data[0] == '!':
                first_selected_player = int(callback.data.replace('!', ''))
                bunker_bot.send_message(callback.message.chat.id, 'Выберите втрого игрока',
                                        reply_markup=second_player_button)
            if callback.data[0] == '#':
                second_selected_player = int(callback.data.replace('#', ''))
            bunker_game.play_movement_card(bunker_game.data['player_cards'][current_player][current_card],
                                           current_player,
                                           movement2[
                                               bunker_game.data['player_cards'][current_player][current_card]][1],
                                           first_selected_player, second_selected_player)
            bunker_bot.send_message(first_selected_player,
                                    f"Ваша новая карточка:"
                                    f"\n{dict_to_str(bunker_game.data['player_cards'][first_selected_player])}")
            bunker_bot.send_message(second_selected_player,
                                    f"Ваша новая карточка:"
                                    f"\n{dict_to_str(bunker_game.data['player_cards'][second_selected_player])}")
            current_card = None
            selected_fact = None
            bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id)
            bunker_bot.delete_message(callback.message.chat.id, callback.message.message_id + next_message)


if __name__ == '__main__':
    bunker_bot.infinity_polling()
