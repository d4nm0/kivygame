<h1 align="center">ChatBot propulsé par Google Home 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
  <img src="https://img.shields.io/badge/npm-%3E%3D5.5.0-blue.svg" />
  <img src="https://img.shields.io/badge/node-%3E%3D9.3.0-blue.svg" />


</p>

> Création d'un chatbot avec google assistant / Google Home



### 🏠 [Homepage](https://gitlab.com/chatbotleans45/chatbotleans#readme)

## Prerequis

- npm >=5.5.0
- node >=9.3.0
- ngrock

## Création


- Se rendre sur le lien suivant : https://console.actions.google.com/
- Télécharger g actions ici : https://developers.google.com/actions/tools/gactions-cli
- Déplacer le fichier télécharger dans votre projet
- Exécuter la commande suivante en vous plaçant dans votre répertoire de projet : ``chmod +x gactions``
- Puis ``./gactions init`` pour créer un fichier action.json qui servira à définir les caractéristiques de notre projet. 
- Assurer vous ensuite que nodejs est bien installé, pour cela : ``nodejs -v``
- Rendez vous ensuite sur : https://ngrok.com/ puis télécharger l’outil
- Une fois installé et placé dans le dossier du projet : ``./ngrock http 3000``
- Dans votre projet ouvrez le fichier action.json
- Dans le fichier remplacer le vide dans url pas l’adresse https donné précédent au lancement de ngrok
- Rentrer ensuite la commande suivante : ``./gactions update --action_package action.json --project PROJECT_IDv (Remplacer PROJECT_ID par le votre, vous pouvez le trouver dans votre page “action on google”, cliquer sur les 3 petits points puis “Project Settings”)
- Cette commande devrait vous proposez un lien, cliquer dessus et connecter vous avec votre compte google. Vous devriez obtenir un clé.
- Copie/Coller la dans l’invité de commande. 
- Si tout ce passe bien, un fichier “creds.data” devrait être créer.
- Il ne reste ensuite plus qu’a créer le fichier index.js
## Author

👤 **Dan Monceau**
👤 **Nicolas Bauder**
👤 **Quentin Patras**
👤 **Joffrey Girard**
