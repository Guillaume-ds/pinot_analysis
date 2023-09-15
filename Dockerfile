# Utilisez une image de base Python
FROM python:3.10.9

# Copiez le code de votre application dans le conteneur
COPY . /app

# Définissez le répertoire de travail
WORKDIR /app

# Installez les dépendances
RUN pip install -r requirements.txt

# Exposez le port sur lequel Streamlit fonctionne (par défaut 8501)
EXPOSE 8501

# Commande pour exécuter votre application Streamlit
CMD ["streamlit", "run", "pinot_analysis.py"]