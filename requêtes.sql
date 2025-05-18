--a. Affichage de la liste des réservations avec le nom du client et la ville de l’hôtel résérvé.
SELECT R.idReservation, C.nomComplet, R.dateDebut, R.dateFin
FROM Reservation R
JOIN Client C ON R.idClient = C.idClient;

--b. Affichage des clients qui habitent à Paris.
SELECT *FROM Client WHERE ville='Paris';

--c. le nombre de réservations faites par chaque client.
SELECT C.nomComplet, COUNT(*) AS nbRes
FROM Client C
JOIN Reservation R ON C.idClient = R.idClient
GROUP BY C.nomComplet;

--d. Donner le nombre de chambres pour chaque type de chambre.
SELECT TC.libelle, COUNT(CH.idChambre) AS nbChambres
FROM TypeChambre TC
JOIN Chambre CH ON TC.idTypeChambre = CH.idTypeChambre
GROUP BY TC.libelle;

--e. Affichage de la liste des chambres qui ne sont pas réservées pour une période donnée (entre deux dates saisies par l’utilisateur).

-- la colonne seule
ALTER TABLE Reservation
ADD idChambre INT;

--  la contrainte de clé étrangère
ALTER TABLE Reservation
ADD CONSTRAINT fk_reservation_chambre 
FOREIGN KEY (idChambre) REFERENCES Chambre(idChambre);


SELECT * FROM Chambre
WHERE idChambre NOT IN (
    SELECT idChambre FROM Reservation
    WHERE NOT (
        dateFin < '2025-07-01' OR dateDebut > '2025-07-10'
    )
);


