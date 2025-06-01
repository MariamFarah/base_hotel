# 🏨 Application de Gestion d’Hôtel - Mini Projet Base de Données

 Réalisé par : Mariam Farah & Aya Lahrayri
 Encadré par : Pr. Zahir — Licence MIP S4

 # Objectif

Créer une application web complète pour la gestion des réservations dans un hôtel, à partir d’un MCD donné.  
Le projet est divisé en deux grandes parties :

- 1. Création de la base de données** avec SQLite (via un script Python)
- 2. Développement d’une interface interactive avec Streamlit**

---

# Technologies utilisées

 Python 3    : Langage principal 
 SQLite      : Système de base de données local 
 Streamlit   : Création de l’interface web 
 pandas      : Manipulation des tableaux de données 



#Structure du projet

📁 project-hotel/
├── app.py # Interface Streamlit
├── init_db.py # Script de création de la base de données
├── projet_hotel.db # Base de données SQLite générée
├── README.md # Ce fichier


# Base de données

Les tables suivantes sont utilisées :
- Client
- Hotel
- Chambre
- TypeChambre
- Prestation
- Reservation
- Evaluation
- ReservationChambre




# 📂 Menu de l'application
  
   ACCEUIL
  
Affiche deux indicateurs :
 Nombre total de clients
 Nombre total de réservations
Utilise des composants st.metric() pour donner une vue synthétique.

 LISTE DES RESEVATIONS
 
Montre toutes les réservations enregistrées.
Affiche :
Le nom du client
La date de début et date de fin
L'ID de la réservation
Données extraites avec une jointure Reservation ⨝ Client.


 LISTE DES CLIENTS 
 
Affiche tous les clients présents dans la base.
Données affichées : nom, adresse, ville, email, téléphone…


LISTE DES CHAMBRES

Montre toutes les chambres avec :
Numéro, étage, balcon, type de chambre
Prix par nuit
Ville de l'hôtel
Données issues de jointures avec TypeChambre et Hotel.


LISTE DES CHAMBRES DISPONIBLES (info)

Permet de sélectionner deux dates.
Affiche toutes les chambres (sans vérification réelle de disponibilité).
Affichage informatif seulement car il n'y a pas de lien direct Reservation ↔ Chambre dans le MCD de base.


 AJOUTER UN CLIENT
 
Formulaire interactif avec : Nom, adresse, ville, code postal, email, téléphone
Enregistre le client dans la table Client.


 AJOUTER UNE RESERVATION
 
Formulaire permettant :
De choisir un client existant
De saisir une période
De sélectionner plusieurs chambres à associer à cette réservation
Utilise la table d’association ReservationChambre pour gérer la relation n:n.


 VOIR LES PRESTATIONS
 
Affiche toutes les prestations disponibles dans l’hôtel (ex : Spa, petit-déjeuner, parking…)
Données tirées de la table Prestation.


MODIFIER/SUPPRIMER UN CLIENT

Permet de :
Modifier les données d’un client
Supprimer définitivement un client de la base


MODIFIER/SUPPRIMER UNE RESERVATION

Permet de :
Modifier les dates ou le client d’une réservation
Supprimer une réservation existante
