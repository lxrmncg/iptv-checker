import telebot
import requests,json
from telebot import types
from flask import Flask, request
import os
from datetime import datetime
import traceback

TOKEN =  os.environ['TOKEN']


bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands={"start"})
def start(message):
	cid = message.chat.id
	bot.send_message(cid,"Hola!\nEste bot te permitirá comprobar el estado de tus listas mediante la API de Xtream Codes.\nPara comprobar tu lista tan solo tienes que enviarme el enlace y yo te mostraré toda la información\n\nBot desarrollado por @APLEONI\nhttps://github.com/adrianpaniagualeon/iptv-checker")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
	try:
		numero_streams = 0
		cid = message.chat.id
		url = message.text
		url =  url.replace('get.php','panel_api.php')
		respuesta = requests.get(url)
		open('respuesta.json', 'wb').write(respuesta.content)
		f = open('respuesta.json')
		json_file = json.load(f)
		json_str = json.dumps(json_file)
		resp = json.loads(json_str)
		username = resp['user_info']['username']
		password = resp['user_info']['password']
		status  = resp['user_info']['status']

		expire_dates = resp['user_info']['exp_date']
		if (expire_dates != None):
			expire_date = datetime.fromtimestamp(int(expire_dates))

			expirate =True

			expire_year = expire_date.strftime("%Y")
			expire_month = expire_date.strftime("%m")
			expire_day = expire_date.strftime("%d")
		else:
			expirate = False

		creates_dates = resp['user_info']['created_at']
		create_date = datetime.fromtimestamp(int(creates_dates))
		create_year = create_date.strftime("%Y")
		create_month = create_date.strftime("%m")
		create_day = create_date.strftime("%d")

		a_connections = resp['user_info']['active_cons']
		m_conections = resp['user_info']['max_connections']

		if (expirate == True):
			mensaje ="Esta es la información de tu lista ⬇️\n\n🟢 Estado: "+status+"\n👤 Usuario: "+username+"\n🔑 Contraseña: "+password+"\n📅 Fecha de Caducidad: "+str(expire_day)+"-"+str(expire_month)+"-"+str(expire_year)+"\n📅 Fecha de Creación: "+str(create_day)+"-"+str(create_month)+"-"+str(create_year)+"\n👥 Conexiones activas: "+a_connections+"\n👥 Conexiones máximas: "+m_conections+"\n\n🤖: @iptv_checker_bot"
		else:
			mensaje ="Esta es la información de tu lista ⬇️\n\n🟢 Estado: "+status+"\n👤 Usuario: "+username+"\n🔑 Contraseña: "+password+"\n📅 Fecha de Caducidad: Nunca\n📅 Fecha de Creación: "+str(create_day)+"-"+str(create_month)+"-"+str(create_year)+"\n👥 Conexiones activas: "+a_connections+"\n👥 Conexiones máximas: "+m_conections+"\n\n🤖: @iptv_checker_bot"
	except:
		mensaje= "No he podido obtener la información de este enlace. Prueba con otro"
		
	bot.reply_to(message, mensaje)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200


@server.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url='https://iptv-checker-adrian.herokuapp.com/' + TOKEN)
	return "!", 200

if __name__ == "__main__":
	server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
