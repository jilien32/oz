CREATE DATABASE myanimal;
USE myanimal;

CREATE TABLE IF NOT EXISTS `myanimal`.`PetOwners` (
  `ownerID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(45) NOT NULL,
  `contact` VARCHAR(45) NULL
  );

CREATE TABLE IF NOT EXISTS `myanimal`.`Pets` (
  `petID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `ownerID` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `species` VARCHAR(45) NULL,
  `breed` VARCHAR(45) NULL,
FOREIGN KEY (`ownerID`) REFERENCES `myanimal`.`PetOwners` (`ownerID`)
);

CREATE TABLE IF NOT EXISTS `myanimal`.`Rooms` (
  `roomID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `roomNumber` INT NULL UNIQUE,
  `roomType` VARCHAR(45) NULL,
  `pricePerNight` DECIMAL(10,2) NOT NULL
  );

CREATE TABLE IF NOT EXISTS `myanimal`.`Reservations` (
  `reservationID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `petID` INT NOT NULL,
  `roomID` INT NOT NULL,
  `startDate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `endDate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (`petID`) REFERENCES `myanimal`.`Pets` (`petID`),
FOREIGN KEY (`roomID`) REFERENCES `myanimal`.`Rooms` (`roomID`)
);

CREATE TABLE IF NOT EXISTS `myanimal`.`Services` (
  `serviceID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `reservationID` INT NOT NULL,
  `serviceName` VARCHAR(45) NULL,
  `servicePrice` DECIMAL(10,2) NULL,
FOREIGN KEY (`reservationID`) REFERENCES `myanimal`.`Reservations` (`reservationID`)
);