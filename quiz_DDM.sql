--get all attributes of participants to populate Players table
SELECT * FROM Participants;

--remove participant
DELETE FROM Participants WHERE participant_id = :participant_id;

--add NEW player
INSERT INTO Participants(first_name, last_name, password)
VALUES(:participant_id, :first_name, :last_name, :password)
