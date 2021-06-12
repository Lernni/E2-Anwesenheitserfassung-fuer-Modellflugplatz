-- important
PRAGMA FOREIGN_KEYS = ON;

CREATE TABLE IF NOT EXISTS RFID_Ausweis
(
    RFID_Code integer PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Pilot
(
    PilotID        integer,
    RFID_Code      integer,
    Token          varchar(20),

-- TODO
    PRIMARY KEY (PilotID),
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
    Ist_Flugleiter bool NOT NULL DEFAULT FALSE,
    Synced         bool NOT NULL DEFAULT FALSE,

    PRIMARY KEY (SessionID),
--     TODO
    FOREIGN KEY (PilotID) REFERENCES Pilot (PilotID) ON DELETE SET NULL
);