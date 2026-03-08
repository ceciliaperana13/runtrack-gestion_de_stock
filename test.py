import mysql.connector

# Connexion directe
db = mysql.connector.connect(
    host="10.10.10.117",
    user="student",
    password="MotDePasseSolide", 
    database="qui_est_ce"
)

cursor = db.cursor()


cursor.execute(f"SELECT p.nom AS personnage, GROUP_CONCAT(a.nom ORDER BY a.nom) AS attributs FROM personnages p JOIN personnage_attribut pa ON p.id = pa.id_personnage JOIN attributs a ON pa.id_attribut = a.id GROUP BY p.id ORDER BY RAND() LIMIT 1;")

result = cursor.fetchall()
print(result)

cursor.close()
db.close()