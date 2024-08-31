import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

def main():
  """
  Cette fonction est le point d'entrée principal de l'application Streamlit.
  """
  #Titre et sous-titre
  st.title('Application de catégorisation des PRO (Product Categorization Application)')
  st.subheader('Auteur: Yaya Diabagaté')

  # Gestion des erreurs pour les fichiers de données manquants
  try:
    data = pd.read_csv('analyse_donnees/DB/donn_int_bk.csv')
  except FileNotFoundError:
    st.error("Error: 'donn_int_bk.csv' fichier introuvable.")
    return

  # Menu déroulant de sélection des fonctionnalités
  feature_names = list(data.columns)
  feature_names.remove("destination")  # Supprimer la colonne cible
  selected_feature = st.selectbox("Sélectionnez la fonctionnalité à visualiser", feature_names)

  # Exploration des données
  st.write("**Résumé des données**")
  st.write(data.describe())

  # Visualisation des données
  st.write("**Visualisation des données**")
  st.line_chart(data[selected_feature])

  # Modèle de Machine Learning

  X = data.drop("destination", axis=1)  # Features
  y = data["destination"]              # Target variable

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

  clf = DecisionTreeClassifier()
  clf.fit(X_train, y_train)

  # Section de prédiction
  st.write("**Prédiction de produit**")
  new_product = {}
  for feature in feature_names:
    new_product[feature] = st.text_input(f"Entrez une valeur pour {feature}")

  if st.button("Prédire"):
    # Convertir la saisie utilisateur en DataFrame
    new_data = pd.DataFrame([new_product])

    # Faire une prédiction
    prediction = clf.predict(new_data)[0]
    st.write(f"Le(s) intrant(s) organique(s) le(s) plus récommandé(s): {prediction}")

#   Evaluation (hidden for now)
#   print("Accuracy:", accuracy_score(y_test, y_pred))
#   print(classification_report(y_test, y_pred))

if __name__ == '__main__':
  main()