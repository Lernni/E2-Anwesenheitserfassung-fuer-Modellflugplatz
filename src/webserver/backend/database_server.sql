-- important
PRAGMA FOREIGN_KEYS = ON;

-- Wird jemals ein Pilot/Gast gelöscht?! => wenn ja, dann siehe TODO
-- Stand jetzt: Piloten/ Gäste können gelöscht werden --> Eintrag wird zu NULL
-- Stand Datenmodell --> PilotID darf nicht NULL sein

-- doku:

-- Piloten haben kein Recht auf Löschung der Daten, (stimmen dem zu bei Eintritt in den Verein)
--
-- Löschung von Daten wahrscheinlich nach 2 Jahren

CREATE TABLE IF NOT EXISTS RFID_Ausweis
(
    RFID_Code integer PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Pilot
(
    Pilot_ID       integer,
    RFID_Code      integer,
    Nachname       varchar(20) NOT NULL,
    Vorname        varchar(20) NOT NULL,
    Eintrittsdatum date        NOT NULL,
    Ist_Aktiv      bool,
    Nutzername     varchar(20),
--     integer, da kein hex datentyp
    Passwort       integer,
    Ist_Admin      bool DEFAULT FALSE,

    PRIMARY KEY (Pilot_ID),
-- ok so?!
    FOREIGN KEY (RFID_Code) references RFID_Ausweis (RFID_Code) ON DELETE SET NULL,
    UNIQUE (RFID_Code)
);

CREATE TABLE IF NOT EXISTS Flugsession
(
    SessionID      integer,
    -- Not NULL sinnvoll?! TODO
    PilotID        integer,
    GastID         int,
    Startzeit      date NOT NULL,
    Endzeit        date,
    -- Not NULL sinnvoll?!
    Ist_Flugleiter bool NOT NULL,

    PRIMARY KEY (SessionID),
--     TODO
    FOREIGN KEY (PilotID) REFERENCES Pilot (Pilot_ID) ON DELETE SET NULL,
--     TODO 2
    FOREIGN KEY (GastID) REFERENCES Gast (GastID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Gast
(
    GastID   integer,
    Vorname  varchar(20) NOT NULL,
    Nachname varchar(20) NOT NULL,
    Freitext varchar(100),

    PRIMARY KEY (GastID)
);


-- -- test values
-- INSERT INTO RFID_Ausweis (RFID_Code)
-- VALUES (1);
-- INSERT INTO RFID_Ausweis (RFID_Code)
-- VALUES (2);
--
-- INSERT INTO Pilot(Pilot_ID, RFID_Code, Nachname, Vorname, Eintrittsdatum, Ist_Aktiv)
-- VALUES (1, 1, 'Mustermann', 'Max', CURRENT_TIMESTAMP, 1);
-- INSERT INTO Pilot(Pilot_ID, RFID_Code, Nachname, Vorname, Eintrittsdatum, Ist_Aktiv)
-- VALUES (2, 2, 'Mustermann', 'Maria', CURRENT_TIMESTAMP, 1);