import openai
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from openai.types import (
    ChatModel,
    FunctionParameters,
    ResponseFormatJSONObject,
    ResponseFormatJSONSchema,
    ResponseFormatText,
    ErrorObject,
    FunctionDefinition
)



openai.api_key = 'Your API KEY'
bot = TeleBot('Your API KEY FROM Tg')

def answer(question):
    try:
        response = openai.ChatCompletion.create(
            model=" ",   #insert model here
            messages=[
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

def generatePic(text):
    try:
        response = openai.Image.create(
            prompt=text,
            n=1,
            size="1024x1024",
            model=" "  #Insert model here
        )
        return response['data'][0]['url']
    except Exception as e:
        return f"Error: {str(e)}"

def main_menu_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    #gpt4 = KeyboardButton("Answer question🤓")
    #dalle = KeyboardButton("Generate picture🖼")
    #kb.add(gpt4, dalle)
    return kb

def cancel_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = KeyboardButton("Cancel❌")
    kb.add(cancel)
    return kb

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome! Choose an option:", reply_markup=main_menu_kb())

@bot.message_handler(func=lambda message: message.text == "Answer question🤓")
def ask_question(message):
    bot.send_message(message.chat.id, "Please enter your question:")
    bot.register_next_step_handler(message, process_question)

def process_question(message):
    question = message.text
    answer_text = answer(question)
    bot.send_message(message.chat.id, answer_text, reply_markup=cancel_kb())

@bot.message_handler(func=lambda message: message.text == "Generate picture🖼")
def ask_prompt(message):
    bot.send_message(message.chat.id, "Please enter the description for the picture:")
    bot.register_next_step_handler(message, process_prompt)

def process_prompt(message):
    prompt = message.text
    picture_url = generatePic(prompt)
    if "Error" in picture_url:
        bot.send_message(message.chat.id, picture_url, reply_markup=cancel_kb())
    else:
        bot.send_photo(message.chat.id, picture_url, reply_markup=cancel_kb())

@bot.message_handler(func=lambda message: message.text == "Cancel❌")
def cancel_action(message):
    bot.send_message(message.chat.id, "Action canceled.", reply_markup=main_menu_kb())

bot.polling()