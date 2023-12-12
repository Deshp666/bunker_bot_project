# import telebot
# from telebot import types
# from BunkerSpecifications_3qqwwe20 import *
# from random import *
# import time
#
# def last_letter(number: int, word: str):
#     converter = {
#         'месяцы': ['месяцев', 'месяц', 'месяца'],
#         'годы': ['лет', 'год', 'года'],
#         'люди': ['человек', 'человек', 'человека']
#     }
#     if str(number)[-1] in ['0', '5', '6', '7', '8', '9'] or 11 <= number <= 20:
#         return converter[word][0]
#     elif str(number)[-1] == '1':
#         return converter[word][1]
#     else:
#         return converter[word][2]
#
# def make_role() -> dict:
#     tier = 0
#     while not 45 <= tier <= 55:
#         factRole_1 = factRole_2 = 0
#         movementRole_1 = movementRole_2 = 0
#
#         tier = 0
#
#         temp_age = randint(18, 80)
#         temp_job_age = temp_age - randint(18, temp_age)
#         temp_hobby_age = temp_age - randint(18, temp_age)
#         age = f'{temp_age} {last_letter(temp_age, "годы")}'
#         job_experience = f'{temp_job_age} {last_letter(temp_job_age, "годы")}'
#         hobby_experience = f'{temp_hobby_age} {last_letter(temp_hobby_age, "годы")}'
#
#         genderRole = choice(list(gender.keys()))
#         tier += gender[genderRole]
#
#         professionRole = choice(list(profession.keys()))
#         tier += profession[professionRole]
#
#         """
#         if genderRole == 'Робот-андроид':
#             healthRole = choice(list(healthRobot.keys()))
#             health_stageRole = 0
#             tier += healthRobot[healthRole]
#         else:
#         """
#         healthRole = choice(list(health.keys()))
#         health_stageRole = choice(list(health_stages.keys()))
#         tier += health[healthRole]
#         tier += health_stages[health_stageRole]
#
#         phobiaRole = choice(list(phobia.keys()))
#         tier += phobia[phobiaRole]
#
#         hobbyRole = choice(list(hobby.keys()))
#         tier += hobby[hobbyRole]
#
#         baggageRole = choice(list(baggage.keys()))
#         tier += baggage[baggageRole]
#
#         while factRole_1 == factRole_2:
#             factRole_1 = choice(list(fact.keys()))
#             factRole_2 = choice(list(fact.keys()))
#         tier += fact[factRole_1]
#         tier += fact[factRole_2]
#
#         while movementRole_1 == movementRole_2:
#             movementRole_1 = choice(list(movement.keys()))
#             movementRole_2 = choice(list(movement.keys()))
#         tier += movement[movementRole_1][0]
#         tier += movement[movementRole_2][0]
#
#     del profession[professionRole]
#     if genderRole == 'Робот-андроид':
#         del gender[genderRole]
#         del healthRobot[healthRole]
#     else:
#         del health[healthRole]
#     del phobia[phobiaRole]
#     del hobby[hobbyRole]
#     del baggage[baggageRole]
#     del fact[factRole_1]
#     del fact[factRole_2]
#     del movement[movementRole_1]
#     del movement[movementRole_2]
#
#     return {
#         'Возраст': age,
#         'Пол': genderRole,
#         'Профессия': professionRole,
#         'Стаж профессии': job_experience,
#         'Здоровье': healthRole,
#         'Стадия болезни (если применима)': health_stageRole,
#         'Фобия': phobiaRole,
#         'Хобби': hobbyRole,
#         'Стаж хобби': hobby_experience,
#         'Багаж': baggageRole,
#         'Факт №1': factRole_1,
#         'Факт №2': factRole_2,
#         'Карта действия №1': movementRole_1,
#         'Карта действия №2': movementRole_2,
#         'Особенности': []
#     }
#
# card = make_role()
# print(card)
# # def dict_to_str(dictionary: dict) -> str:
# #     formatted_string = ''
# #     for key, value in dictionary.items():
# #         formatted_string += f'    "{key}": "{value}",\n'
# #     formatted_string = formatted_string.rstrip(',\n')
# #     # while '"' in formatted_string or "'" in formatted_string:
# #     #     formatted_string.replace("'", "").replace('"', '')
# #     return formatted_string.replace('"', '')
# #
# # print(dict_to_str(card))
s = f"123f"