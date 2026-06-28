import joblib
import imaplib
import email
import time
from email.header import decode_header

model = joblib.load("spam_model_n1.pkl")
vectorizer = joblib.load("vector.pkl")

def is_spam(text):
    if text is None:
        return "not spam"
    if not isinstance(text, str):
        text = str(text)
    if text.strip() == "":
        return "not spam"
    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0][1]
    print(prob)
    return pred

# gmail sync

mail = imaplib.IMAP4_SSL('imap.gmail.com') # или другой сервер
mail.login('shoxmamurjonov02@gmail.com', 'jxsu tegx ogkd minr')
mail.select("INBOX")
result, data = mail.uid('search', None, 'SEEN')
latest_uid = data[0].split()[-1]
# print(mail.list())
# Получаем тему и отправителя для письма с UID 123
res, msg_data = mail.uid('fetch', latest_uid, '(BODY.PEEK[])')
for response_part in msg_data:
    if isinstance(response_part, tuple):
        # Парсим сырые байты в объект сообщения
        msg = email.message_from_bytes(response_part[1])

        # Декодируем заголовок (Тему)
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        print(f"Тема: {subject}")

        # Извлекаем текст письма
        if msg.is_multipart():
            # email_text = msg.get_payload(decode=True)
            # result = is_spam(email_text)
            # if result == "spam":
            #     print("🚨 СПАМ")
            # else:
            #     print("✅ Норм письмо")
            for part in msg.walk():
                if part.get_content_type() == "text/plain":  # берем только текст
                    email_text = part.get_payload(decode=True).decode()
                    full_text = subject + " " + email_text
                    result = is_spam(full_text)
                    print("text:", email_text)
                    if result == "spam":
                        print("🚨 СПАМ")
                    else:
                        print("✅ Норм письмо")
        else:
            print(msg.get_payload(decode=True).decode())

# print("Скрипт запущен...")
# while True:
#     process_emails()
#     time.sleep(30)