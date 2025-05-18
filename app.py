import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Connexion à la base SQLite
def get_connection():
    return sqlite3.connect("projet_hotel.db")

# Personnalisation de l'interface avec CSS
st.set_page_config(page_title="Gestion Hôtel", page_icon="🏨", layout="wide")
st.markdown(
    '''
    <style>
        body {
            background-color: #F4C2C2;
            color: #333333;
        }
        .main {
            background-color: #FAF9F6;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3 {
            color: #A3D2CA;
        }
        .stButton button {
            background-color: #D4AF37;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        .stButton button:hover {
            background-color: #c09f2e;
        }
        .stSidebar {
            background-color: #FAF9F6;
        }
         <div style='text-align: center;'>
        <img src='hotelLogo.png' width='300'/>
        </div>
    </style>
    ''',
    unsafe_allow_html=True
)

# Titre et bannière
st.title(" Gestion de l’Hôtel")
st.markdown("Bienvenue dans l'application de gestion des réservations de chambres !")

# Menu
menu = st.sidebar.selectbox("📂 Menu", [
    " Accueil",
    " Liste des réservations",
    " Liste des clients",
    " Liste des chambres",
    " Liste des chambres disponibles (info)",
    " Ajouter un client",
    " Ajouter une réservation",
    " Voir les prestations",
    " Modifier/Supprimer un client",
    " Modifier/Supprimer une réservation",
])

conn = get_connection()
cursor = conn.cursor()

# 1. Accueil
if menu == " Accueil":
    st.subheader(" Statistiques")
    c1, c2 = st.columns(2)
    nb_clients = cursor.execute("SELECT COUNT(*) FROM Client").fetchone()[0]
    nb_reservations = cursor.execute("SELECT COUNT(*) FROM Reservation").fetchone()[0]
    with c1:
        st.metric("Nombre de clients", nb_clients)
    with c2:
        st.metric("Nombre de réservations", nb_reservations)

# 2. Voir les réservations
elif menu == " Liste des réservations":
    df = pd.read_sql_query("""
        SELECT R.idReservation, C.nomComplet, R.dateDebut, R.dateFin
        FROM Reservation R
        JOIN Client C ON R.idClient = C.idClient
    """, conn)
    st.subheader(" Réservations")
    st.dataframe(df.style.highlight_max(axis=0, color='lightblue'))

# 3. Voir les clients
elif menu == " Liste des clients":
    df = pd.read_sql_query("SELECT * FROM Client", conn)
    st.subheader(" Liste des clients")
    st.dataframe(df)

# 4. Voir les chambres
elif menu == " Liste des chambres":
    df = pd.read_sql_query("""
        SELECT CH.idChambre, CH.numero, CH.etage, CH.balcon,
               TC.libelle AS type, TC.prixParNuit, H.ville AS hotel
        FROM Chambre CH
        JOIN TypeChambre TC ON CH.idTypeChambre = TC.idTypeChambre
        JOIN Hotel H ON CH.idHotel = H.idHotel
    """, conn)
    st.subheader(" Liste des chambres")
    st.dataframe(df)

# 5. Chambres disponibles (info seulement)
elif menu == " Liste des chambres disponibles (info)":
    st.subheader(" Recherche de chambres disponibles")
    date_debut = st.date_input("📅 Date d'arrivée", date.today())
    date_fin = st.date_input("📅 Date de départ", date.today())
    st.warning("⚠️ Recherche informative uniquement. Aucune relation chambre-réservation dans le MCD original.")
    df = pd.read_sql_query("""
        SELECT CH.idChambre, CH.numero, CH.etage,
               TC.libelle AS type, TC.prixParNuit, H.ville
        FROM Chambre CH
        JOIN TypeChambre TC ON CH.idTypeChambre = TC.idTypeChambre
        JOIN Hotel H ON CH.idHotel = H.idHotel
    """, conn)
    st.dataframe(df)

# 6. Ajouter un client
elif menu == " Ajouter un client":
    st.subheader(" Ajouter un nouveau client")
    with st.form("form_client"):
        nom = st.text_input("Nom complet")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.number_input("Code postal", step=1)
        email = st.text_input("Email")
        telephone = st.text_input("Téléphone")
        submitted = st.form_submit_button("Ajouter")
        if submitted:
            cursor.execute("""
                INSERT INTO Client (nomComplet, adresse, ville, codePostal, email, telephone)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nom, adresse, ville, code_postal, email, telephone))
            conn.commit()
            st.success(f"✅ Client {nom} ajouté avec succès.")

# 7. Ajouter une réservation
elif menu == " Ajouter une réservation":
    st.subheader(" Ajouter une nouvelle réservation")
    clients = cursor.execute("SELECT idClient, nomComplet FROM Client").fetchall()
    client_dict = {f"{nom} (ID {id})": id for (id, nom) in clients}

    chambres = cursor.execute("SELECT idChambre, numero FROM Chambre").fetchall()
    chambre_dict = {f"Chambre {num} (ID {id})": id for (id, num) in chambres}

    with st.form("form_reservation"):
        client_choisi = st.selectbox("Client", list(client_dict.keys()))
        date_debut = st.date_input("Date de début")
        date_fin = st.date_input("Date de fin")
        chambres_choisies = st.multiselect("Chambres", list(chambre_dict.keys()))
        submitted = st.form_submit_button("Ajouter réservation")
        if submitted:
            id_client = client_dict[client_choisi]
            cursor.execute("""
                INSERT INTO Reservation (dateDebut, dateFin, idClient)
                VALUES (?, ?, ?)
            """, (date_debut, date_fin, id_client))
            id_reservation = cursor.lastrowid
            for chambre in chambres_choisies:
                id_chambre = chambre_dict[chambre]
                cursor.execute("""
                    INSERT INTO ReservationChambre (idReservation, idChambre)
                    VALUES (?, ?)
                """, (id_reservation, id_chambre))
            conn.commit()
            st.success("✅ Réservation ajoutée avec chambres associées.")

# 8. Voir les prestations
elif menu == " Voir les prestations":
    st.subheader(" Liste des prestations proposées")
    df = pd.read_sql_query("SELECT * FROM Prestation", conn)
    st.dataframe(df)

# 9. Modifier/Supprimer un client
elif menu == " Modifier/Supprimer un client":
    st.subheader(" Modifier ou Supprimer un client")
    clients = cursor.execute("SELECT idClient, nomComplet FROM Client").fetchall()
    choix = {f"{nom} (ID {id})": id for id, nom in clients}
    selected = st.selectbox("Sélectionner un client", list(choix.keys()))

    if selected:
        id_client = choix[selected]
        client_data = cursor.execute("SELECT * FROM Client WHERE idClient = ?", (id_client,)).fetchone()
        nom = st.text_input("Nom complet", client_data[6])
        adresse = st.text_input("Adresse", client_data[1])
        ville = st.text_input("Ville", client_data[2])
        code_postal = st.number_input("Code postal", value=client_data[3])
        email = st.text_input("Email", client_data[4])
        telephone = st.text_input("Téléphone", client_data[5])

        col1, col2 = st.columns(2)
        if col1.button("✅ Modifier"):
            cursor.execute("""
                UPDATE Client SET nomComplet=?, adresse=?, ville=?, codePostal=?, email=?, telephone=?
                WHERE idClient=?
            """, (nom, adresse, ville, code_postal, email, telephone, id_client))
            conn.commit()
            st.success("Client mis à jour avec succès.")

        if col2.button("🗑️ Supprimer"):
            cursor.execute("DELETE FROM Client WHERE idClient = ?", (id_client,))
            conn.commit()
            st.success("Client supprimé.")

# 10. Modifier/Supprimer une réservation
elif menu == " Modifier/Supprimer une réservation":
    st.subheader(" Modifier ou Supprimer une réservation")
    reservations = cursor.execute("""
        SELECT R.idReservation, C.nomComplet
        FROM Reservation R JOIN Client C ON R.idClient = C.idClient
    """).fetchall()

    choix = {f"Réservation {id} - {nom}": id for id, nom in reservations}
    selected = st.selectbox("Sélectionner une réservation", list(choix.keys()))

    if selected:
        id_res = choix[selected]
        res_data = cursor.execute("SELECT dateDebut, dateFin, idClient FROM Reservation WHERE idReservation = ?", (id_res,)).fetchone()
        date_debut = st.date_input("Date de début", pd.to_datetime(res_data[0]))
        date_fin = st.date_input("Date de fin", pd.to_datetime(res_data[1]))

        clients = cursor.execute("SELECT idClient, nomComplet FROM Client").fetchall()
        client_dict = {f"{nom} (ID {id})": id for id, nom in clients}
        client_nom = [k for k, v in client_dict.items() if v == res_data[2]][0]
        selected_client = st.selectbox("Client", list(client_dict.keys()), index=list(client_dict.keys()).index(client_nom))

        col1, col2 = st.columns(2)
        if col1.button("✅ Modifier"):
            cursor.execute("""
                UPDATE Reservation SET dateDebut=?, dateFin=?, idClient=?
                WHERE idReservation=?
            """, (date_debut, date_fin, client_dict[selected_client], id_res))
            conn.commit()
            st.success("Réservation modifiée.")

        if col2.button("🗑️ Supprimer"):
            cursor.execute("DELETE FROM Reservation WHERE idReservation = ?", (id_res,))
            conn.commit()
            st.success("Réservation supprimée.")



conn.close()