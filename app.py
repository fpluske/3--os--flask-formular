from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'chat-app-secret-key-2025'

# URL webhook aplikace
WEBHOOK_URL = "https://n8n.nrsn.eu/webhook-test/bcaacc70-c516-4056-9b76-63840ded30ec"

# Jednoduchá úschovna pro chat zprávy (v produkci by byla databáze)
chat_messages = []

@app.route('/')
def index():
    return render_template('chat.html', messages=chat_messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    global chat_messages
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        username = data.get('username', 'Anonym').strip()
        
        if not user_message:
            return jsonify({'error': 'Zpráva nemůže být prázdná'}), 400
        
        # Vytvoření objektu zprávy
        message_data = {
            'username': username,
            'message': user_message,
            'timestamp': datetime.now().isoformat(),
            'source': 'Flask Chat App'
        }
        
        # Přidání uživatelské zprávy do chatu
        user_msg_id = len(chat_messages)  # ID pro identifikaci zprávy
        chat_messages.append({
            'type': 'user',
            'username': username,
            'message': user_message,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'id': user_msg_id
        })
        
        # Přidání loading zprávy
        loading_msg_id = len(chat_messages)
        chat_messages.append({
            'type': 'loading',
            'username': 'System',
            'message': '⏳ Čekám na odpověď z webhook...',
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'id': loading_msg_id
        })
        
        # Odeslání do webhook aplikace
        webhook_response = None
        try:
            response = requests.post(
                WEBHOOK_URL,
                json=message_data,
                headers={'Content-Type': 'application/json'},
                timeout=(15, 600)  # (connection timeout, read timeout) - 15s připojení, 10 minut čtení
            )
            
            if response.status_code == 200:
                try:
                    webhook_response = response.json()
                except:
                    webhook_response = {'response': response.text}
            else:
                webhook_response = {
                    'error': f'HTTP {response.status_code}',
                    'message': 'Chyba při komunikaci s webhook'
                }
                
        except requests.exceptions.RequestException as e:
            webhook_response = {
                'error': 'Connection Error',
                'message': f'Nepodařilo se připojit k webhook: {str(e)}'
            }
        
        # Odebrání loading zprávy
        chat_messages = [msg for msg in chat_messages if msg.get('id') != loading_msg_id]
        
        # Přidání odpovědi webhook do chatu
        if webhook_response:
            if 'error' in webhook_response:
                chat_messages.append({
                    'type': 'error',
                    'username': 'System',
                    'message': f"❌ {webhook_response['message']}",
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'id': len(chat_messages)
                })
            else:
                # Pokud webhook vrátil strukturovanou odpověď
                response_text = webhook_response.get('message', 
                                                   webhook_response.get('response', 
                                                                      json.dumps(webhook_response, indent=2)))
                chat_messages.append({
                    'type': 'webhook',
                    'username': 'Webhook Bot',
                    'message': f"🤖 {response_text}",
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'raw_data': webhook_response,
                    'id': len(chat_messages)
                })
        
        return jsonify({
            'status': 'success',
            'message': 'Zpráva byla odeslána',
            'webhook_response': webhook_response
        })
        
    except Exception as e:
        return jsonify({'error': f'Chyba serveru: {str(e)}'}), 500

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    global chat_messages
    chat_messages = []
    return jsonify({'status': 'success', 'message': 'Chat byl vymazán'})

@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': chat_messages})

@app.route('/add_user_message', methods=['POST'])
def add_user_message():
    """Endpoint pro okamžité přidání uživatelské zprávy do chatu"""
    global chat_messages
    try:
        data = request.get_json()
        username = data.get('username', 'Anonym').strip()
        message = data.get('message', '').strip()
        
        if message:
            chat_messages.append({
                'type': 'user',
                'username': username,
                'message': message,
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'id': len(chat_messages)
            })
        
        return jsonify({'status': 'success', 'messages': chat_messages})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)