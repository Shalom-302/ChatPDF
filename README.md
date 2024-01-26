# Chatbot PDF

Ce projet est une application web qui utilise le langage Python, le framework Streamlit et l'API de Gemini pour créer un chatbot capable de répondre aux questions des utilisateurs à partir de leurs fichiers PDF.

## Fonctionnalités

- Téléchargement de fichiers PDF
- Extraction et segmentation du texte des PDF
- Recherche de similarité entre la question de l'utilisateur et les segments de texte
- Génération de réponses avec le modèle d'IA Gemini Pro de Google
- Interface web interactive avec Streamlit

## Prérequis

Pour exécuter ce projet, vous devez avoir les éléments suivants :

- Python 3.11 ou supérieur
- Streamlit 1.2.0 ou supérieur
- Langchain 0.9.0 ou supérieur
- Une clé API de Gemini

## Installation

Pour installer ce projet, suivez ces étapes :

- Clonez le dépôt sur votre machine locale avec la commande `git clone https://github.com/<username>/chatbot-pdf.git`
- Accédez au dossier du projet avec la commande `cd chatbot-pdf`
- Installez les dépendances avec la commande `pip install -r requirements.txt`
- Créez un fichier `.streamlit/secrets.toml` et stockez votre clé API de Gemini sous la forme `GEMINI_API_KEY = "votre-clé-API"`
- Lancez l'application avec la commande `streamlit run main.py`

## Utilisation

Pour utiliser ce projet, vous devez :

- Télécharger vos fichiers PDF dans le menu latéral et cliquer sur le bouton "Soumettre et traiter"
- Attendre que l'application traite les fichiers PDF et crée un index de similarité
- Poser une question à partir des fichiers PDF dans le champ de texte
- Recevoir une réponse générée par le chatbot

## Licence

Ce projet est sous licence MIT. 
