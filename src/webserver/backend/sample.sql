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
-- temp
    FOREIGN KEY (RFID_Code) references RFID_Ausweis (RFID_Code) ON DELETE SET NULL,
    UNIQUE (RFID_Code)
);

-- test values
INSERT INTO RFID_Ausweis (RFID_Code)
VALUES (1);
INSERT INTO RFID_Ausweis (RFID_Code)
VALUES (2);

INSERT INTO Pilot(Pilot_ID, RFID_Code, Nachname, Vorname, Eintrittsdatum, Ist_Aktiv) VALUES (1,1,'Mustermann', 'Max', CURRENT_TIMESTAMP, 1);
INSERT INTO Pilot(Pilot_ID, RFID_Code, Nachname, Vorname, Eintrittsdatum, Ist_Aktiv) VALUES (2,2,'Mustermann', 'Maria', CURRENT_TIMESTAMP, 1);