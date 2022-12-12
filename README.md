# AUTOMATISATION D’UN PIPELINE avec Apache Airflow

L'architecture de ce pipeline est comme suit.
![image](https://user-images.githubusercontent.com/60548808/207005674-145cd77e-d3a9-4ba7-b7f0-46f891c94b2d.png)

## 1. Installation du docker et Docker compose 
Avant de commencer, si vous n’avez jamais travaillé avec docker et docker compose, vous devriez prendre un moment pour se familiariser et installer l’environnement Docker car vous devez exécuter Airflow sur Docker.
On suit ces étapes pour installer les outils nécessaires :
•	Vous installez Docker Community Edition (CE) sur votre poste de travail. Selon votre système d’exploitation.
•	L’environnement est bien installé sur votre Desktop.
 
![image](https://user-images.githubusercontent.com/60548808/207005909-b9b2e506-b030-4f35-bf09-cac4e920179d.png)

•	Vous tapez la commande suivante « docker –version » pour afficher la version de docker :

 ![image](https://user-images.githubusercontent.com/60548808/207005943-fe9c5d60-08b1-4901-996e-05b50003735f.png)

•	Vous créez un dossier sur votre ordinateur nommé ‘’airflow-hive’’ et vous devrez créer un fichier docker-compose.yaml sur votre dossier ‘’airflow-hive‘’ pour déployer Airflow sur Docker Compose.
 ![image](https://user-images.githubusercontent.com/60548808/207005971-3d3705e0-59b9-4ec2-8735-c8df1476d240.png)

•	Lorsque vous ouvrez le fichier docker-compose.yml sur l’outil Visual studio code, vous trouvez le code suivant : 
![image](https://user-images.githubusercontent.com/60548808/207006005-6a9f68d3-9aa0-4b57-86f8-75f0c4a87445.png)
 
•	Ce fichier contient plusieurs définitions de service :
    - airflow-scheduler : le planificateur surveille toutes les tâches et tous les DAG, puis déclenche le Instances des tâches une fois leurs dépendances terminées.
    - airflow-webserver : le serveur web est disponible à l’adresse. Http://localhost:8080
    - airflow-worker : le travailleur qui exécute les tâches données par le planificateur.
    - airflow-init : le service d’initialisation.
    - Postgres : la base de données.
    - redis : le redis-broker qui transfère les messages du planificateur au travailleur.
    
## 2. Installation de l’environnement Airflow sur docker :
Avant de démarrer Airflow pour la première fois, vous devez préparer votre environnement, c’est-à-dire créer les nécessaires fichiers, répertoires et initialiser la base de données.
### - La création des répertoires nécessaires :
Sur l’invite de commande, vous tapez les commandes suivantes :
•	Dans le fichier ‘’airflow-hive‘’, vous créez les trois dossiers (dags, logs et plugins) avec la commande « mkdir dags logs plugins » et vous affichez son contenu avec la commande  « dir ».
 ![image](https://user-images.githubusercontent.com/60548808/207006253-5b170be1-caa5-4bae-8d00-277303a373ee.png)

### - L’initialisation de la base de données :
•	Sur tous les systèmes d’exploitation, vous devez exécuter des migrations de bases de données et créer le premier compte utilisateur. Pour ce faire, vous exécutez la commande suivante « docker compose up airflow-init » :
 ![image](https://user-images.githubusercontent.com/60548808/207006367-17d11820-6601-4693-9ad9-09e255e4766b.png)

•	Une fois l’initialisation terminée, vous devez voir un message comme celui-ci :
 ![image](https://user-images.githubusercontent.com/60548808/207006557-eb587fd8-f84a-41e4-adf7-f2cd1ab1ad8a.png)

•	Le compte est créé avec le login et le mot de passe : airflow airflow.

### - L’Airflow en cours d’exécution :
•	Vous pouvez maintenant démarrer tous les services, en tapant la commande « docker-compose up ».
 ![image](https://user-images.githubusercontent.com/60548808/207006708-b95a94e2-ee08-4212-a0c3-d5f7982d29d9.png)

•	Dans un deuxième terminal, vous pouvez vérifier l’état des conteneurs et vous assurer qu’aucun conteneur n’est dans un état malsain, en tapant la commande « docker ps »
 ![image](https://user-images.githubusercontent.com/60548808/207006748-59d3d71a-1cbd-4d75-b14a-54bd7df7bd13.png)

•	Dans le Docker Desktop, le container est bien créé.
 ![image](https://user-images.githubusercontent.com/60548808/207006782-1f22529a-33bb-4994-ad9d-a04928e3a3a2.png)

•	Sur votre navigateur web, vous ouvrez un nouvel onglet et vous tapez Localhost:8080/login/   et vous se connectez au compte.
 ![image](https://user-images.githubusercontent.com/60548808/207006808-2185d1c5-e2c8-48b8-ba09-780b70b2aa43.png)

•	Apres la connexion, vous pouvez commencer à expérimenter avec les DAG.
 ![image](https://user-images.githubusercontent.com/60548808/207006835-8b5ff062-8d83-4e06-a45d-e0cdd518b5d6.png)

## 3. L’installation d’Apache hive sur docker :
•	Vous trouvez sur GitHub un projet sur l’url https://github.com/big-data-europe/docker-hive, puis vous téléchargez ce dossier.
 ![image](https://user-images.githubusercontent.com/60548808/207006890-e66f0f53-8daf-424e-8f88-f126a232e3fb.png)

•	Vous sélectionnez les fichiers de ce dossier importé et vous les copiez dans le dossier airflow-hive, ainsi vous copiez le contenu du docker-compose de hive dans le docker-compose du airflow-hive.
 ![image](https://user-images.githubusercontent.com/60548808/207006918-8a3ab744-84f9-4c51-a9a7-d8d4ea2123c3.png)

•	Le fichier docker-compose.yml contient le code suivant :
![image](https://user-images.githubusercontent.com/60548808/207006940-bb5eb9da-0497-416a-b6a6-87610a382185.png)
 
•	Vous tapez la commande « docker compose up –d » pour créer et démarrer tous les services requis par notre cluster Hive.
 ![image](https://user-images.githubusercontent.com/60548808/207007112-d00e42a8-4273-4148-aea4-a19bf4f01fee.png)

•	Les nœuds sont bien installés.
![image](https://user-images.githubusercontent.com/60548808/207007388-5b091285-7df4-4517-9d0b-b9c6964b54b6.png)

•	Vous tapez la commande « docker container ls » pour Répertorier les conteneurs.
![image](https://user-images.githubusercontent.com/60548808/207007415-6107d5c2-f70f-4a26-9818-0506ff19af61.png)
 

Pour vérifier que Hive marche bien : 
•	Vous tapez la commande « docker exec –it airflow-hive-hive-server- 1 » pour se connecter au serveur hive.
•	Vous tapez la commande « show databases » : afficher le répertoire les bases de données sur le serveur.
 ![image](https://user-images.githubusercontent.com/60548808/207007458-1e535746-19af-4394-bf01-d66114f257a5.png)

•	Maintenant dans le dossier dags on ajoute un fichier ourDag.py comme suit.
 ![image](https://user-images.githubusercontent.com/60548808/207007490-393fa901-111c-4449-9c4b-187acfb6bfdf.png)

•	Pour se connecter à hive on crée la fonction suivante
 ![image](https://user-images.githubusercontent.com/60548808/207007524-814afa66-1708-4b2d-b1bd-91e945735908.png)

•	On définit la fonction extract_transform afin d’extraire les données de l’API yahoo Finance et on les  stocke dans une liste (stocks_prices) pour faire des transformations (Supression des redondances, ...)
 ![image](https://user-images.githubusercontent.com/60548808/207007610-558f3325-9a38-4cdc-a855-de716097a27e.png)

•	La fonction load est créé pour stocker les données après transformation dans une table sous hive
 ![image](https://user-images.githubusercontent.com/60548808/207007636-34a1eac4-258d-489a-8c6b-9cb16fa03ea5.png)

•	Maintenant vous ajouter une fonction où vous utilisez Spark SQL pour accéder et traiter les données  et vous ajoutez quelques indicateurs (MACD, SMA, CMA).
 ![image](https://user-images.githubusercontent.com/60548808/207007671-4cc6d27f-d3c5-4fe5-835a-088479bf6756.png)
 ![image](https://user-images.githubusercontent.com/60548808/207007693-e14a0c60-5257-4f08-8c1c-82f791e72277.png)

•	Ensuite on instancie le dag avec ses paramètres
 ![image](https://user-images.githubusercontent.com/60548808/207007724-8e8a747d-8c8a-4384-a6b4-18dabd39bda6.png)

•	Ici on fait appel aux fonctions déjà créées de chargement, traitement et de visualisation, ensuite on hiérarchise les tâches.
-	Hiérarchie des tâches : Il s’agit du dernier composant du DAG et il est utilisé pour spécifier l’ordre selon lequel vous souhaitez qu’Airflow exécute les tâches
 ![image](https://user-images.githubusercontent.com/60548808/207007848-3e7bad72-7c39-4528-920b-20b8ab55e704.png)

•	Voilà le dag est bien créé avec les différentes tâches.
  ![image](https://user-images.githubusercontent.com/60548808/207007884-99919ffe-475e-40ac-aa1a-07a6a70def70.png)
![image](https://user-images.githubusercontent.com/60548808/207007906-d04065ae-e88d-4c14-a9fe-f26af90ec92d.png)

•	Apres l’exécution, les données de l’API yahoo Finance son stockées et transférées dans une liste (stocks_prices)  avec sucées.
 ![image](https://user-images.githubusercontent.com/60548808/207007929-e642ba1a-ed07-4d0d-8df5-c13fbd6d6abe.png)

•	Les données sont stockées après la transformation dans une table sous hive avec sucées
 ![image](https://user-images.githubusercontent.com/60548808/207007952-6454be73-bca3-43c3-87c6-40a514eb54da.png)

•	Pour le calcul de la moyenne mobile cumulative, nous utiliserons la fonction dataframe.expanding(). Cette méthode nous donne la valeur cumulée de notre fonction d’agrégation (moyenne dans ce cas) 
 ![image](https://user-images.githubusercontent.com/60548808/207007976-67c833cd-df0d-4775-a9b0-5841cdb82789.png)

•	Ce bout de code permet de calculer La convergence/divergence des moyennes mobiles
 ![image](https://user-images.githubusercontent.com/60548808/207007999-a1591a0e-fe9e-4f8f-b2c9-08136e9b1aba.png)

•	Pour calculer de la moyenne mobile simple (SMA), nous utiliserons la fonction mean() pour calculer la moyenne .
 ![image](https://user-images.githubusercontent.com/60548808/207008021-a6df7d28-cbff-4f6f-a764-c9404dcfd89b.png)

•	On ajoute maintenant dans le dossier dags ce fichier vis.py qui permet d’afficher les graphes avec Streamlit.
 ![image](https://user-images.githubusercontent.com/60548808/207008086-a3fe4439-509e-490a-a931-f09d252f8eaa.png)
 ![image](https://user-images.githubusercontent.com/60548808/207008118-be46e964-26df-443a-9543-c287005dcb7d.png)

•	Dans le fichier ourDag.py, nous utilisons le BashOperator pour lancer l’application Streamlit dans le dag
 ![image](https://user-images.githubusercontent.com/60548808/207008151-de3cd2d6-3aec-4ccf-8065-5d5349475a4d.png)

Maintenant lorsque le DAG s’exécute, à l’aide de Streamlit, nous ouvrons un nouvel onglet avec le numéro de port de Streamlit (8501) et nous obtenons les visualisations suivantes.
 ![image](https://user-images.githubusercontent.com/60548808/207008171-b0c1ae80-fc0e-4420-ad6d-cc9c1b3246d7.png)
![image](https://user-images.githubusercontent.com/60548808/207008189-b546290b-db4f-4830-ba55-0758fe393cab.png)
 



## Références

-	Qu'est-ce qu'un pipeline data
-	Apache Airflow : qu'est-ce que c'est et comment l'utiliser ? (datascientest.com)
-	Architecture Overview — Airflow Documentation (apache.org)
-	Migrating from Apache Oozie to Apache Airflow
-	Comparaison entre Apache Oozie et Apache Airflow

```
    docker-compose up -d
```




## Contributors
* Hasnaa HASBI
* Oumaima BENRHENNOU
* Chaimaa NOUGOUM
