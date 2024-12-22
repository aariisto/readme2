-- Créer un utilisateur nommé 'user_velib' avec un mot de passe 'saevelib'
CREATE USER 'user_velib'@'localhost' IDENTIFIED BY 'saevelib';

-- privilèges sur la table stations (uniquement SELECT)
GRANT SELECT ON sae_velib.stations TO 'user_velib'@'localhost';

-- privilèges sur la table velo (uniquement SELECT)
GRANT SELECT ON sae_velib.velo TO 'user_velib'@'localhost';

-- privilèges sur la table reservations (SELECT, INSERT)
GRANT SELECT, INSERT ON sae_velib.reservations TO 'user_velib'@'localhost';

-- privilèges sur la table recherches (SELECT, DELETE, INSERT)
GRANT SELECT, DELETE, INSERT ON sae_velib.recherches TO 'user_velib'@'localhost';

-- privilèges sur la table users (SELECT, UPDATE, INSERT)
GRANT SELECT, UPDATE, INSERT ON sae_velib.users TO 'user_velib'@'localhost';

GRANT SELECT ON sae_velib.recherches_vue TO 'user_velib'@'localhost';

GRANT SELECT ON sae_velib.reservations_vue TO 'user_velib'@'localhost';
-- Appliquer les modifications
FLUSH PRIVILEGES;