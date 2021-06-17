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
    RFID_Code integer PRIMARY KEY,
    Synced bool NOT NULL
);

CREATE TABLE IF NOT EXISTS Pilot
(
    PilotID        integer,
    RFID_Code      integer,
    Nachname       varchar(20) NOT NULL,
    Vorname        varchar(20) NOT NULL,
    Eintrittsdatum date        NOT NULL,

    Nutzername     varchar(20),
    Passwort       varchar(200),

    Ist_Admin      bool DEFAULT FALSE,
    Token          varchar(20) NOT NULL,
    Synced bool NOT NULL,



-- ok so?!
    PRIMARY KEY (PilotID),
    FOREIGN KEY (RFID_Code) references RFID_Ausweis (RFID_Code) ON DELETE SET NULL,
    UNIQUE (RFID_Code),
    UNIQUE (Nutzername),
    UNIQUE (Token)
);

CREATE TABLE IF NOT EXISTS Flugsession
(
    SessionID      integer,
    PilotID        integer,
    GastID         integer,
    Startzeit      datetime NOT NULL,
    Endzeit        datetime,
    -- Not NULL sinnvoll?!
    Ist_Flugleiter bool     NOT NULL,

    PRIMARY KEY (SessionID),
--     TODO
    FOREIGN KEY (PilotID) REFERENCES Pilot (PilotID) ON DELETE SET NULL,
--     TODO 2
    FOREIGN KEY (GastID) REFERENCES Gast (GastID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Gast
(
    GastID   integer,
    Gastname varchar(20) NOT NULL,
    Freitext varchar(100),

    PRIMARY KEY (GastID)
);

-- initialen admin erzeugen
INSERT INTO Pilot(Nachname, Vorname, Eintrittsdatum, Nutzername, Ist_Admin, Token, Synced) VALUES ('admin', 'admin', date(), 'admin', true, '2568695077352081093', true);
