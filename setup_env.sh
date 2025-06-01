#!/bin/bash
set -e

echo "==[ Virtuele Python omgeving creëren ]=="
python3 -m venv venv
source venv/bin/activate

echo "==[ Python dependencies installeren ]=="
pip install --upgrade pip
pip install flask flask-cors pybit python-dotenv

echo "==[ Bybit API config voorbeeld aanmaken (.env) ]=="
if [ ! -f backend/.env ]; then
mkdir -p backend
cat <<EOT > backend/.env
BYBIT_API_KEY=JOUW_API_KEY_HIER
BYBIT_API_SECRET=JOUW_SECRET_HIER
BYBIT_ACCOUNT_TYPE=UNIFIED # Of CONTRACT als je dat gebruikt
EOT
echo "==> Vul nu backend/.env in met jouw echte keys!"
fi

echo "==[ Installatie voltooid ]=="
