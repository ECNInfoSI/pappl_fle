<?php
// Connexion à la base de données
$pdo = new PDO(
    "mysql:host=localhost;dbname=app_fle;charset=utf8mb4",
    "root",
    ""
);

// Requête SQL pour récupérer les noms et prénoms
$requete = $pdo->query("SELECT nom, prenom FROM utilisateur");

// Affichage des résultats
while ($utilisateur = $requete->fetch(PDO::FETCH_ASSOC)) {
    echo htmlspecialchars($utilisateur['nom']) . " "
       . htmlspecialchars($utilisateur['prenom']) . "<br>";
}
?>