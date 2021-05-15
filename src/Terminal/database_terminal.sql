-- important
PRAGMA FOREIGN_KEYS = ON;

CREATE TABLE IF NOT EXISTS RFID_Ausweis
(
    RFID_Code integer PRIMARY KEY
);

-- keine PilotID, stattdessen: ROWID
CREATE TABLE IF NOT EXISTS Pilot
(
    RFID_Code      integer,
    Nachname       varchar(20) NOT NULL,
    Vorname        varchar(20) NOT NULL,
    Eintrittsdatum date        NOT NULL,
    Ist_Aktiv      bool,

-- TODO
    FOREIGN KEY (RFID_Code) references RFID_Ausweis (RFID_Code) ON DELETE SET NULL,
    UNIQUE (RFID_Code)
);

-- keine SessionID, stattdessen: ROWID
CREATE TABLE IF NOT EXISTS Flugsession
(
    -- Not NULL sinnvoll?! TODO
    PilotID        integer,
    Startzeit      date NOT NULL,
    Endzeit        date,
    -- Not NULL sinnvoll?!
    Ist_Flugleiter bool NOT NULL DEFAULT FALSE,

--     TODO
    FOREIGN KEY (PilotID) REFERENCES Pilot (ROWID) ON DELETE SET NULL
);