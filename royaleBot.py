#!/usr/bin/python3
#-*- codign: utf-8 -*-
import requests, json, time, telepot
from pprint import pprint
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

bot = telepot.Bot('TOKEN')

headers = {"auth": "DEVELOPER KEY FROM api.cr-api.com"}

profileUrl = 'http://api.cr-api.com/player/'

def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	global words
	words = msg['text'].split()

	if words[0] == '/profile':
		if len(words) > 1:
			pprint('Buscando perfil del jugador: ' + str(words))
			profile_request = requests.get(profileUrl + str(words[1]), headers=headers)
			pprint(str(profile_request.status_code))

			if profile_request.status_code == 200:
				profile = profile_request.json()
				if('error' not in profile):
					pprint('Perfil de jugador encontrado.')
					supermagical = profile['chestCycle']['superMagical']
					legendary = profile['chestCycle']['legendary']
					epic = profile['chestCycle']['epic']
					giant = profile['chestCycle']['giant']
					magic = profile['chestCycle']['magical']
					upcomingChests = profile['chestCycle']['upcoming']
					currentDeck = profile['currentDeck']

					global keyboard
					keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Actualizar', callback_data='press')],])

					global text
					text = str('👤 *Name:* ' + profile['name'] + '\n'
					+ '👥 *Clan:* ' + profile['clan']['name'] + '\n'
					+ '🏆 *Trophies:* ' + str(profile['trophies']) + '\n'
					+ '🔝 *Trophies record:* ' + str(profile['stats']['maxTrophies']) + '\n'
					+ '⚔️ *Arena:* ' + profile['arena']['name'] + '\n'
					+ '🎁 *Total donations:* ' + str(profile['stats']['totalDonations'])
					+ '\n\n'
					+ '*Chest cycle: *\n'
					+ '- Next chests: '
					+ upcomingChests[0] + ', '
					+ upcomingChests[1] + ', '
					+ upcomingChests[2] + ', '
					+ upcomingChests[3]
					+ '\n\n'
					+ '- Giant: ' + str(giant) + '\n'
					+ '- Magic: ' + str(magic) + '\n'
					+ '- Epic: ' + str(epic) + '\n'
					+ '- Legendary: ' + str(legendary) + '\n'
					+ '- Supermagical: ' + str(supermagical)
					+ '\n\n'
					+ '*Current deck:* ' + '\n'
					+ '- *' + currentDeck[0]['name'] + '* (' + str(currentDeck[0]['level']) + ')\n'
		 			+ '- *' + currentDeck[1]['name'] + '* (' + str(currentDeck[1]['level']) + ')\n'
		 			+ '- *' + currentDeck[2]['name'] + '* (' + str(currentDeck[2]['level']) + ')\n'
		 			+ '- *' + currentDeck[3]['name'] + '* (' + str(currentDeck[3]['level']) + ')\n'
		 			+ '- *' + currentDeck[4]['name'] + '* (' + str(currentDeck[4]['level']) + ')\n'
		 			+ '- *' + currentDeck[5]['name'] + '* (' + str(currentDeck[5]['level']) + ')\n'
		 			+ '- *' + currentDeck[6]['name'] + '* (' + str(currentDeck[6]['level']) + ')\n'
		 			+ '- *' + currentDeck[7]['name'] + '* (' + str(currentDeck[7]['level']) + ')\n' + '\n'
					+ 'Deck link: ' + profile['deckLink'])

					global sent
					sent = bot.sendMessage(msg['chat']['id'], text, parse_mode='Markdown', reply_markup=keyboard)
				else:
					bot.sendMessage(msg['chat']['id'], 'Ha ocurrido un error, vuelve a intentarlo mas tarde.🙏', parse_mode='Markdown')
			else:
				bot.sendMessage(msg['chat']['id'], 'Ha ocurrido un error, vuelve a intentarlo mas tarde.🙏', parse_mode='Markdown')

		else:
			bot.sendMessage(msg['chat']['id'], 'También necesito saber el TAG del perfil que quieres ver. Escribe /profile TAG. \n*Ejemplo:* /profile 2r8v8u2j',
							parse_mode='Markdown')
	elif words[0] == '/start':
		bot.sendMessage(msg['chat']['id'],
						'¡¡BIENVENIDO!!😁\nPara ver información sobre un jugador escribe:\n/profile TAG. \n\n*Ejemplo:* /profile 2r8v8u2j',
							parse_mode='Markdown')

def on_callback_query(msg):
	query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
	pprint('Obteniendo ciclo de cofres.')

	pprint('Buscando perfil del jugador: ' + str(words))
	profile_request = requests.get(profileUrl + str(words[1]), headers=headers)
	pprint(str(profile_request.status_code))

	if profile_request.status_code == 200:
		profile = profile_request.json()
		if('error' not in profile):
			pprint('Perfil de jugador encontrado.')
			supermagical = profile['chestCycle']['superMagical']
			legendary = profile['chestCycle']['legendary']
			epic = profile['chestCycle']['epic']
			giant = profile['chestCycle']['giant']
			magic = profile['chestCycle']['magical']
			upcomingChests = profile['chestCycle']['upcoming']

			pprint('Editando mensaje')

			new_text = str('👤 *Name:* ' + profile['name'] + '\n'
			+ '👥 *Clan:* ' + profile['clan']['name'] + '\n'
			+ '🏆 *Trophies:* ' + str(profile['trophies']) + '\n'
			+ '🔝 *Trophies record:* ' + str(profile['stats']['maxTrophies']) + '\n'
			+ '⚔️ *Arena:* ' + profile['arena']['name'] + '\n'
			+ '🎁 *Total donations:* ' + str(profile['stats']['totalDonations'])
			+ '\n\n'
			+ '*Chest cycle: *\n'
			+ '- Next chests: '
			+ upcomingChests[0] + ', '
			+ upcomingChests[1] + ', '
			+ upcomingChests[2] + ', '
			+ upcomingChests[3]
			+ '\n\n'
			+ '- Giant: ' + str(giant) + '\n'
			+ '- Magic: ' + str(magic) + '\n'
			+ '- Epic: ' + str(epic) + '\n'
			+ '- Legendary: ' + str(legendary) + '\n'
			+ '- Supermagical: ' + str(supermagical)
			+ '\n\n'
			+ '*Current deck:* ' + '\n'
			+ '- ' + profile['currentDeck'][0]['name'] + ' -> level ' + profile['currentDeck'][0]['level'] + '\n'
			+ '- ' + profile['currentDeck'][1]['name'] + ' -> level ' + profile['currentDeck'][1]['level'] + '\n'
			+ '- ' + profile['currentDeck'][2]['name'] + ' -> level ' + profile['currentDeck'][2]['level'] + '\n'
			+ '- ' + profile['currentDeck'][3]['name'] + ' -> level ' + profile['currentDeck'][3]['level'] + '\n'
			+ '- ' + profile['currentDeck'][4]['name'] + ' -> level ' + profile['currentDeck'][4]['level'] + '\n'
			+ '- ' + profile['currentDeck'][5]['name'] + ' -> level ' + profile['currentDeck'][5]['level'] + '\n'
			+ '- ' + profile['currentDeck'][6]['name'] + ' -> level ' + profile['currentDeck'][6]['level'] + '\n'
			+ '- ' + profile['currentDeck'][7]['name'] + ' -> level ' + profile['currentDeck'][7]['level'])

			if new_text != text:
				message, code, data = bot.editMessageText(telepot.message_identifier(sent), new_text, parse_mode='Markdown', reply_markup=keyboard)
				bot.answerCallbackQuery(query_id, text='Datos actualizados! 👍')
			else:
				bot.answerCallbackQuery(query_id, text='Los datos ya estan actualizados.')

		else:
			bot.answerCallbackQuery(query_id, 'Ha ocurrido un error, vuelve a intentarlo mas tarde.🙏')
	else:
		bot.answerCallbackQuery(query_id, 'Ha ocurrido un error, vuelve a intentarlo mas tarde.🙏')


MessageLoop(bot, {'chat': on_chat_message,
				'callback_query': on_callback_query}).run_as_thread()

while 1:
	time.sleep(10)
