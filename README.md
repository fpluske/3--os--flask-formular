# Flask Chat s Webhook

Real-time chat aplikace komunikující s n8n webhook systémem.

## Funkcionality

- **🔥 Real-time Chat** - Interaktivní chat rozhraní
- **🤖 Webhook Integration** - Komunikace s n8n webhook aplikací
- **📱 Responzivní Design** - Moderní chat UI s Bootstrap 5
- **💬 Zprávy v reálném čase** - Okamžité zobrazení odpovědí
- **🛠️ Raw Data View** - Zobrazení surových JSON odpovědí
- **⚡ Error Handling** - Robustní zpracování chyb
- **🗑️ Clear Chat** - Možnost vymazání celého chatu
- **👤 Custom Username** - Vlastní jméno pro každou zprávu

## Instalace a spuštění

1. **Aktivace virtuálního prostředí:**
   ```bash
   source .venv/bin/activate
   ```

2. **Instalace závislostí:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Spuštění aplikace:**
   ```bash
   python app.py
   ```

4. **Otevření v prohlížeči:**
   ```
   http://localhost:5000
   ```

## Webhook Konfigurace

Aplikace je nakonfigurována pro komunikaci s n8n webhook:

**URL:** `https://n8n.nrsn.eu/webhook-test/bcaacc70-c516-4056-9b76-63840ded30ec`

### Odesílaná data do webhook:
```json
{
    "username": "Jméno uživatele",
    "message": "Text zprávy", 
    "timestamp": "2025-09-24T10:30:45",
    "source": "Flask Chat App"
}
```

### Chat aplikace najdeš na:
```
http://localhost:5000
```

## Struktura projektu

```
flask-formular/
├── app.py                 # Hlavní aplikační soubor
├── requirements.txt       # Závislosti projektu
├── templates/            # HTML šablony
│   └── chat.html         # Chat rozhraní
└── .venv/                # Virtuální prostředí
```

## Použité technologie

- **Python 3.x**
- **Flask** - Webový framework
- **Requests** - HTTP knihovna pro komunikaci s webhook
- **Jinja2** - Template engine
- **Bootstrap 5** - CSS framework
- **HTML5/CSS3**

## Další možnosti rozšíření

Chat aplikaci můžete rozšířit o:
- 💾 **Databázi** (SQLAlchemy) pro trvalé uložení zpráv
- 👥 **Multi-user support** s autentifikací
- 📎 **Přílohy** - odesílání souborů přes webhook
- 🔔 **Notifikace** při nové zprávě
- 🎨 **Customizace** - témata, emotikony
- 📊 **Analytics** - statistiky chatu
- 🔒 **Šifrování** zpráv
- 🌐 **WebSockets** pro real-time komunikaci bez refreshu