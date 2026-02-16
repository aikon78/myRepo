"""
Script per verificare la configurazione dell'ambiente.

Esegui questo script dopo aver creato il Codespace per verificare che tutto sia configurato correttamente.
"""

import sys
import os


def check_python_version():
    """Verifica versione Python."""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        return True
    else:
        print("  ⚠️  Richiesto Python 3.8+")
        return False


def check_dependencies():
    """Verifica dipendenze installate."""
    required = [
        'openai',
        'anthropic',
        'langchain',
        'fastapi',
        'streamlit',
        'chromadb',
        'python-dotenv'
    ]

    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NON INSTALLATO")
            missing.append(package)

    return len(missing) == 0


def check_env_file():
    """Verifica presenza file .env."""
    if os.path.exists('.env'):
        print("✓ File .env trovato")

        # Verifica presenza API key
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv('MISTRAL_API_KEY')
        if api_key and api_key != 'your-mistral-api-key-here':
            print("✓ MISTRAL_API_KEY configurata")
            return True
        else:
            print("⚠️  MISTRAL_API_KEY non configurata in .env")
            return False
    else:
        print("✗ File .env non trovato")
        print("  Esegui: cp .env.example .env")
        print("  Poi modifica .env e aggiungi la tua API key")
        return False


def check_directories():
    """Verifica struttura directory."""
    dirs = ['src', 'data', 'tests', '.devcontainer']
    all_exist = True

    for d in dirs:
        if os.path.exists(d):
            print(f"✓ Directory {d}/")
        else:
            print(f"✗ Directory {d}/ non trovata")
            all_exist = False

    return all_exist


def main():
    """Esegue tutti i controlli."""
    print("=" * 60)
    print("🔍 VERIFICA CONFIGURAZIONE AMBIENTE AI AGENT")
    print("=" * 60)

    print("\n📦 Versione Python:")
    python_ok = check_python_version()

    print("\n📚 Dipendenze:")
    deps_ok = check_dependencies()

    print("\n⚙️  Configurazione:")
    env_ok = check_env_file()

    print("\n📁 Struttura:")
    dirs_ok = check_directories()

    print("\n" + "=" * 60)

    if python_ok and deps_ok and env_ok and dirs_ok:
        print("✅ TUTTO OK! Sei pronto per iniziare!")
        print("\nProva a eseguire:")
        print("  python src/simple_agent.py")
        print("  python src/agent.py")
        print("  streamlit run src/streamlit_app.py")
        return 0
    else:
        print("⚠️  Alcuni problemi rilevati. Controlla i messaggi sopra.")
        if not deps_ok:
            print("\nPer installare le dipendenze:")
            print("  pip install -r requirements.txt")
        if not env_ok:
            print("\nPer configurare l'ambiente:")
            print("  cp .env.example .env")
            print("  # Poi modifica .env con il tuo editor")
        return 1


if __name__ == "__main__":
    sys.exit(main())
