-- important
PRAGMA FOREIGN_KEYS = ON;

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
    Startzeit      date NOT NULL,
    Endzeit        date,
    -- Not NULL sinnvoll?!
    Ist_Flugleiter bool NOT NULL,

    PRIMARY KEY (SessionID),
--     TODO
    FOREIGN KEY (PilotID) REFERENCES Pilot (Pilot_ID) ON DELETE SET NULL
);