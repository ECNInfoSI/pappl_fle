# Centrale App FLE — intégration HTML/CSS

Pages statiques issues des maquettes Figma. Uniquement la partie visuelle, sans aucun JS.
Les endroits où le back intervient sont signalés par des commentaires `<!-- BACK : … -->`.

## Fichiers

| Maquette | Page |
|---|---|
| 01 Connexion | `index.html` |
| 02 Menu principal | `accueil.html` |
| 03 Mes exercices — liste | `exercices.html` |
| 04 / 04b Détail + suppression | `exercice-detail.html` (modale : `exercice-detail.html#confirmer-suppression`) |
| 05 Choix du type | `exercice-nouveau.html` |
| 06a–d Éditeurs | `exercice-edition-qcm.html`, `-texte-a-trous.html`, `-vrai-faux.html`, `-association.html` |
| 07 Mes sujets | `sujets.html` |
| 08 Détail d'un sujet | `sujet-detail.html` |
| 09 Composition | `sujet-composition.html` |
| 10 Import / Export | `import-export.html` |
| 11 Conflits | `import-conflits.html` |
| 12 Paramètres | `parametres.html` |
| 13 Admin comptes | `admin-comptes.html` |

`css/style.css` regroupe les variables (couleurs, rayons…), le layout et les composants.
Le header et la sidebar sont copiés dans chaque page : à factoriser dans un gabarit côté back.
Pour marquer la page courante, posez `.is-active` sur le lien de la sidebar.

## Éléments complexes en HTML/CSS pur (déjà faits)

- **Segmented control** (Élève/Correction, PDF/HTML, Vrai/Faux) : radios masqués + `input:checked + span`.
- **Menu ⋮** : `<details>/<summary>`. Il ne se ferme pas quand on clique ailleurs (ça demande un peu de JS).
- **Aperçu au survol** (liste des exercices) : popover caché, affiché via `:hover` / `:focus-within`. Le contenu est vide, c'est au back de le remplir.
- **Modale de suppression** : `:target`. Le lien `#confirmer-suppression` l'ouvre, `#` la ferme. Alternative en JS : `<dialog>.showModal()`.
- **Cartes de choix du type** : `<label>` + radio caché, styles via `:has(input:checked)`.
- **Bonne réponse QCM / choix de conflit en gras** : `:has(input:checked)`.
- **Zone de dépôt / bouton « Importer »** : `<label>` qui enveloppe un `<input type="file">`, donc le clic ouvre le sélecteur de fichiers.
- **Trait rouge des associations** : simple décor CSS, chaque ligne correspond à une paire.
- **Selects** : `<select>` natifs restylés (chevron en SVG).

## Laissé à faire (JS ou back), signalé en commentaire dans les pages

- Éditeur **texte à trous** : création et retrait de trous à partir de la sélection, sérialisation.
- **Glisser-déposer** pour réordonner (questions, affirmations, paires, exercices d'un sujet).
- Boutons **« + Ajouter … »** (question, réponse, affirmation, paire) et suppression de lignes.
- **Composition d'un sujet** : ajouter/retirer depuis la banque, filtres, total des points.
- **« Tout sélectionner »**, compteur « Exporter N exercices », boutons « Tout ignorer/copier/remplacer ».
- Glisser-déposer de fichier sur la zone de dépôt.
- Filtre de niveau multiple (la maquette montre « A2, B1 ») : pour l'instant c'est un `<select>` simple.
