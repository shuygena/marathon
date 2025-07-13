from gigachat import GigaChat

with GigaChat(
    credentials="ключ",
    verify_ssl_certs=False) as giga:
    response = giga.chat("Какая задача была данна финалистам конкурса Цифровой марафон 2024. Напомнинаю, что сейчас идёт конкурс 2025")
    print(response.choices[0].message.content)