# 📘 Guida a GitHub Codespaces

## Cos'è GitHub Codespaces?

GitHub Codespaces è un ambiente di sviluppo completo che gira nel cloud. È come avere VS Code con tutto configurato, accessibile dal browser!

## 🌟 Vantaggi per Sviluppare Agenti AI

1. **Configurazione Zero**: Tutto è già installato (Python, librerie, extensions)
2. **Potenza Cloud**: Non serve un computer potente, tutto gira su server GitHub
3. **Accessibile Ovunque**: Lavora dal browser, da qualsiasi dispositivo
4. **Consistente**: Stesso ambiente per tutti nel team
5. **Economico**: 60 ore gratis al mese per account personali!

## 🚀 Come Usare il Codespace

### Avviare il Codespace

1. Vai sulla repository GitHub
2. Clicca "Code" → "Codespaces" → "Create codespace"
3. Aspetta ~2 minuti per la creazione
4. Il Codespace si apre automaticamente!

### Prima Volta

Quando il Codespace si avvia per la prima volta:
- Carica l'immagine Docker (Python 3.11)
- Installa le extensions VS Code
- Esegue `pip install -r requirements.txt` (automatico!)

Vedi il progresso nel terminale integrato.

### Interfaccia

Il Codespace è praticamente VS Code:
- **Explorer** (Ctrl+Shift+E): Vedi i file
- **Search** (Ctrl+Shift+F): Cerca nel codice  
- **Source Control** (Ctrl+Shift+G): Git integrato
- **Terminal** (Ctrl+`): Terminale Linux integrato
- **Extensions**: Tutto già installato!

### Lavorare con i File

Tutto funziona come VS Code locale:
- Apri file dall'Explorer
- Usa Ctrl+P per cercare file velocemente
- Modifica, salva (Ctrl+S)
- I cambiamenti sono automaticamente nel Codespace

### Usare il Terminale

Il terminale è un vero terminale Linux:
```bash
# Esegui Python
python src/agent.py

# Installa pacchetti
pip install nuovo-pacchetto

# Usa git
git status
git add .
git commit -m "messaggio"
```

### Port Forwarding (Importante!)

Quando avvii un server (es. Streamlit, FastAPI), il Codespace:
- Rileva automaticamente la porta (8000, 8501, etc.)
- Crea un URL pubblico temporaneo
- Ti chiede se vuoi aprirlo

Esempio:
```bash
streamlit run src/streamlit_app.py
```
→ Si apre automaticamente in una nuova tab!

Per vedere le porte attive:
- Clicca sulla tab "PORTS" in basso
- Vedi tutte le porte forwarded
- Puoi renderle pubbliche o private

## ⚙️ Configurazione (.devcontainer)

Il file `.devcontainer/devcontainer.json` controlla:

```json
{
  "name": "AI Agent Development",
  "image": "mcr.microsoft.com/devcontainers/python:1-3.11-bullseye",
  
  // Extensions VS Code installate automaticamente
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "github.copilot",
        // ...
      ]
    }
  },
  
  // Comando eseguito dopo la creazione
  "postCreateCommand": "pip install -r requirements.txt",
  
  // Porte da forwardare
  "forwardPorts": [8000, 8501]
}
```

## 💡 Tips & Tricks

### 1. GitHub Copilot

Il Codespace ha già Copilot attivato! Usa:
- Inizia a scrivere e Copilot suggerisce
- Scrivi un commento `# fai questo` e Copilot genera il codice
- Ctrl+Enter per vedere più suggerimenti

### 2. Salvataggio Automatico

I file si salvano automaticamente, ma i cambiamenti sono solo nel Codespace finché non fai commit.

### 3. Git Workflow

```bash
# Vedi cosa hai modificato
git status

# Aggiungi tutti i cambiamenti
git add .

# Commit
git commit -m "Descrizione modifiche"

# Push su GitHub
git push
```

Oppure usa la UI di VS Code (icona Source Control).

### 4. Multiple Terminals

Apri più terminali contemporaneamente:
- Clicca "+" nella tab del terminale
- Utile per avere: server in un terminale, comandi in un altro

### 5. Debugging Python

Hai il debugger integrato:
- Metti breakpoint (click a sinistra del numero di riga)
- F5 per avviare il debug
- Ispeziona variabili, step-through, etc.

### 6. Estensioni Utili

Già installate:
- **Python**: IntelliSense, linting, debugging
- **Pylance**: Type checking avanzato
- **Jupyter**: Notebook support
- **Copilot**: AI pair programming
- **Docker**: Gestione container

### 7. Gestione Secrets

NON committare API keys! Usa sempre `.env`:
```bash
# .env è in .gitignore
echo "OPENAI_API_KEY=sk-xxx" > .env
```

Il Codespace legge il file `.env` ma non viene committato su GitHub.

### 8. Personalizzazione

Cambia tema, shortcuts, settings come in VS Code normale:
- Ctrl+, per le impostazioni
- I settings sono specifici per questo Codespace

## 💰 Costi e Limiti

### Account Gratuito
- 120 core-hours al mese (gratis!)
- ~60 ore con 2-core machine
- ~30 ore con 4-core machine

### Come Ottimizzare
1. **Ferma il Codespace** quando non lo usi:
   - Si ferma automaticamente dopo 30 min di inattività
   - O manualmente: Code → Stop Codespace

2. **Elimina Codespaces** vecchi che non usi:
   - Vai su https://github.com/codespaces
   - Delete dei Codespaces non necessari

3. **Usa machine più piccole**: 2-core è sufficiente per AI agents

### Monitorare l'Uso
- https://github.com/settings/billing
- Vedi ore usate questo mese
- Imposta limiti di spesa

## 🔧 Comandi Utili

### Gestione Codespace

```bash
# Ricostruisci il container (se cambi .devcontainer)
Ctrl+Shift+P → "Codespaces: Rebuild Container"

# Ferma il Codespace
Ctrl+Shift+P → "Codespaces: Stop Current Codespace"

# Connetti da VS Code Desktop
Ctrl+Shift+P → "Codespaces: Open in VS Code Desktop"
```

### Troubleshooting

```bash
# Re-installa dipendenze
pip install -r requirements.txt --force-reinstall

# Pulisci cache Python
find . -type d -name __pycache__ -exec rm -r {} +

# Verifica configurazione
python check_setup.py
```

## 🆘 Problemi Comuni

### "Codespace creation failed"
- Riprova dopo qualche minuto
- Controlla la connessione internet
- Verifica il tuo account GitHub

### "Port forwarding not working"
- Verifica che il server sia in ascolto su 0.0.0.0 (non 127.0.0.1)
- Controlla la tab PORTS
- Clicca su "Refresh" nella tab Ports

### "Slow performance"
- Usa una machine più grande (Settings → Machine type)
- Ferma processi pesanti non necessari
- Riavvia il Codespace

### "Extensions not working"
- Rebuild container: Ctrl+Shift+P → "Rebuild Container"
- Verifica `.devcontainer/devcontainer.json`

## 📱 Codespaces su Mobile

Sì, puoi usare Codespaces anche da tablet o smartphone!

1. Vai su github.com dal browser mobile
2. Apri la repository
3. Code → Codespaces → Create/Open
4. Usa una tastiera Bluetooth per un'esperienza migliore

## 🔐 Sicurezza

- **API Keys**: Mai committare, usa sempre `.env`
- **Secrets**: Usa GitHub Secrets per CI/CD
- **Porte**: Di default le porte sono private (solo per te)
- **Files**: Solo tu hai accesso al tuo Codespace

## 📚 Risorse

- [Documentazione Ufficiale](https://docs.github.com/en/codespaces)
- [Pricing](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces)
- [VS Code Keybindings](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-linux.pdf)

## 🎯 Best Practices

1. ✅ **Ferma il Codespace** quando hai finito
2. ✅ **Fai commit** spesso
3. ✅ **Usa .env** per secrets
4. ✅ **Monitora l'uso** mensile
5. ✅ **Elimina Codespaces** vecchi
6. ✅ **Usa .gitignore** per file grandi

---

Happy Coding nel Cloud! ☁️🚀
