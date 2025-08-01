import requests
import json
import os

VILLE = "Montpellier"
DATA_FILE = "logements_precedents.json"
URL = f"https://trouverunlogement.lescrous.fr/tools/flux/logements?ville={VILLE}"

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/TON_WEBHOOK_ICI"

def fetch_logements():
    try:
        resp = requests.get(URL)
        resp.raise_for_status()
        return [logement["titre"] for logement in resp.json()]
    except Exception as e:
        print("Erreur fetch:", e)
        return []

def charger_logements():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def sauvegarder_logements(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def envoyer_discord(messages):
    content = "**Nouveaux logements CROUS à " + VILLE + "**\n" + "\n".join(f"- {m}" for m in messages)
    payload = {"content": content}
    try:
        r = requests.post(https://discord.com/api/webhooks/1400741969264771163/Z4PKORkfjWnaEZgxAQYFSBtyMcKtqH0JN-cEbaFahBs9IdRBGUxMJfPgId-SyUYt0aFx, json=payload)
        if r.status_code != 204:
            print("Échec de l'envoi Discord :", r.status_code, r.text)
    except Exception as e:
        print("Erreur Discord :", e)

def main():
    print(f"🔍 Recherche de logements pour {VILLE}…")
    actuels = fetch_logements()
    precedents = charger_logements()
    nouveautes = [l for l in actuels if l not in precedents]
    if nouveautes:
        print(f"✅ {len(nouveautes)} nouveauté(s) :")
        for l in nouveautes:
            print("-", l)
        envoyer_discord(nouveautes)
        sauvegarder_logements(actuels)
    else:
        print("ℹ️ Aucun nouveau logement.")

if __name__ == "__main__":
    main()
