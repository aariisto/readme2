import requests
import mysql.connector

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",  # Remplace par ton hôte
    user="root",  # Remplace par ton utilisateur de base de données
    password="yannel",  # Remplace par ton mot de passe
    database="user"  # Remplace par le nom de ta base de données
)
cursor = conn.cursor(dictionary=True)

# URL de l'API
url_api = "http://localhost:5000/stations"

# Requête à l'API pour récupérer les données JSON
response = requests.get(url_api)  # Envoi d'une requête GET à l'API
stations = response.json()  # Conversion de la réponse en format JSON

# Variables pour compter les insertions et les mises à jour
nbInsertion = 0
nbUpdate = 0

# Parcourir chaque station dans les données JSON
for station in stations:
    station_id = station['station_id']  # Récupérer l'ID de la station
    lat = station['lat']  # Récupérer la latitude
    lon = station['lon']  # Récupérer la longitude
    name = station['name']  # Récupérer le nom de la station

    # Vérifier si la station existe déjà dans la base de données
    cursor.execute("SELECT COUNT(*) FROM stations WHERE station_id = %s", (station_id,))
    result = cursor.fetchone()

    if result['COUNT(*)'] == 0:  # Si la station n'existe pas
        try:
            # Insérer une nouvelle station dans la base de données
            cursor.execute(
                "INSERT INTO stations (station_id, lat, lon, station) VALUES (%s, %s, %s, %s)",
                (station_id, lat, lon, name)
            )
            nbInsertion += 1  # Incrémenter le compteur d'insertion
        except mysql.connector.IntegrityError as e:
            # Gérer une erreur d'intégrité
            print(f"Erreur d'insertion pour la station ID {station_id}: {e}")
    else:
        # Si la station existe, récupérer ses données actuelles
        cursor.execute("SELECT lat, lon, station FROM stations WHERE station_id = %s", (station_id,))
        donner = cursor.fetchone()

        # Comparer les données actuelles avec les nouvelles données
        current_lat = donner['lat']
        current_lon = donner['lon']
        current_name = donner['station']

        # Si les données ont changé, mettre à jour la base de données
        if current_lat != lat or current_lon != lon or current_name != name:
            try:
                cursor.execute(
                    "UPDATE stations SET lat = %s, lon = %s, station = %s WHERE station_id = %s",
                    (lat, lon, name, station_id)
                )
                print("current info :", current_lat, "/// new info : ", lat)
                nbUpdate += 1  # Incrémenter le compteur de mises à jour
            except mysql.connector.Error as e:
                # Gérer une erreur lors de la mise à jour
                print(f"Erreur de mise à jour pour la station ID {station_id}: {e}")

# Validation de la transaction (sauvegarde des modifications)
conn.commit()

# Affichage des résultats
print("Insertion des stations terminée.\n")
print("Nombre d'insertion: ", nbInsertion, "\n")
print("Nombre de changement: ", nbUpdate)

# Fermer la connexion à la base de données
cursor.close()
conn.close()
