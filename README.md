# Postafon | developed by Eren Koçakgöl

**Postafon**, interneti günlük olarak tarayarak haberleri çekerek otomatik olarak OpenAI API'si ile haberleri yeniden yazarak veritabanına kaydeden Momentum AI ile sinerjik olarak çalışan şablon bir web uygulaması, güçlü ve esnek bir yazılımdır. Kullanımı kolay ve entegre edilebilir özellikler sunar.

## Bu Yazılımın,

- **Özellik 1:** Front-End'i Bootstrap,
- **Özellik 2:** Back-End'i Django,
- **Özellik 3:** Database'i SQLite3,
- ve saf emeğim ile yazılmıştır. 

## Kurulum

Postafon'a başlamak için bu depoyu klonlayın ve gerekli bağımlılıkları yükleyin:

git clone https://github.com/erenkocakgol/postafon.com.git
cd Postafon.com
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
gunicorn -c gconfig.py

