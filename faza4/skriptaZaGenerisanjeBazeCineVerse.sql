-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema cineverse
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `cineverse` ;

-- -----------------------------------------------------
-- Schema cineverse
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cineverse` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `cineverse` ;

-- -----------------------------------------------------
-- Table `cineverse`.`nalog`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`nalog` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`nalog` (
  `idNal` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NOT NULL,
  `korisnickoIme` VARCHAR(45) NOT NULL,
  `lozinka` VARCHAR(45) NOT NULL,
  `uloga` VARCHAR(1) NOT NULL DEFAULT 'Z',
  PRIMARY KEY (`idNal`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `korisnickoIme_UNIQUE` (`korisnickoIme` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`admin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`admin` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`admin` (
  `idAdm` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idAdm`),
  CONSTRAINT `admin_idAdm_fk`
    FOREIGN KEY (`idAdm`)
    REFERENCES `cineverse`.`nalog` (`idNal`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`film`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`film` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`film` (
  `idFil` INT NOT NULL AUTO_INCREMENT,
  `naziv` VARCHAR(45) NOT NULL,
  `originalniNaziv` VARCHAR(45) NOT NULL,
  `trajanje` INT NOT NULL,
  `pocetakPrikazivanja` DATE NOT NULL,
  `reziseri` VARCHAR(100) NOT NULL,
  `glumci` VARCHAR(150) NOT NULL,
  `kratakSadrzaj` VARCHAR(150) NOT NULL,
  `radnja` VARCHAR(500) NOT NULL,
  `ocenaIMDB` FLOAT NOT NULL DEFAULT '0',
  `ocenaKorisnika` FLOAT NOT NULL DEFAULT '0',
  `slika` BLOB NOT NULL,
  PRIMARY KEY (`idFil`),
  UNIQUE INDEX `idFil_UNIQUE` (`idFil` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`zanr`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`zanr` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`zanr` (
  `idZan` INT NOT NULL AUTO_INCREMENT,
  `naziv` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idZan`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`ima_zanr`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`ima_zanr` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`ima_zanr` (
  `idFil` INT NOT NULL,
  `idZan` INT NOT NULL,
  PRIMARY KEY (`idFil`, `idZan`),
  INDEX `ima_zanr_idZan_fk_idx` (`idZan` ASC) VISIBLE,
  CONSTRAINT `ima_zanr_idFil_fk`
    FOREIGN KEY (`idFil`)
    REFERENCES `cineverse`.`film` (`idFil`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `ima_zanr_idZan_fk`
    FOREIGN KEY (`idZan`)
    REFERENCES `cineverse`.`zanr` (`idZan`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`korisnik`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`korisnik` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`korisnik` (
  `idKor` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idKor`),
  CONSTRAINT `korisnik_idKor_fk`
    FOREIGN KEY (`idKor`)
    REFERENCES `cineverse`.`nalog` (`idNal`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`ocenjuje`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`ocenjuje` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`ocenjuje` (
  `idKor` INT NOT NULL,
  `idFil` INT NOT NULL,
  `ocena` INT NOT NULL,
  PRIMARY KEY (`idKor`, `idFil`),
  INDEX `ocenjuje_idFil_fk_idx` (`idFil` ASC) VISIBLE,
  CONSTRAINT `ocenjuje_idFil_fk`
    FOREIGN KEY (`idFil`)
    REFERENCES `cineverse`.`film` (`idFil`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `ocenjuje_idKor_fk`
    FOREIGN KEY (`idKor`)
    REFERENCES `cineverse`.`korisnik` (`idKor`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`predlaze`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`predlaze` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`predlaze` (
  `idKor` INT NOT NULL,
  `idFil` INT NOT NULL,
  PRIMARY KEY (`idKor`, `idFil`),
  INDEX `predlaze_idFil_fk_idx` (`idFil` ASC) VISIBLE,
  CONSTRAINT `predlaze_idFil_fk`
    FOREIGN KEY (`idFil`)
    REFERENCES `cineverse`.`film` (`idFil`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `predlaze_idKor_fk`
    FOREIGN KEY (`idKor`)
    REFERENCES `cineverse`.`korisnik` (`idKor`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`sala`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`sala` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`sala` (
  `idSal` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idSal`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`termin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`termin` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`termin` (
  `idTer` INT NOT NULL AUTO_INCREMENT,
  `termin` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`idTer`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`projekcija`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`projekcija` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`projekcija` (
  `idPro` INT NOT NULL AUTO_INCREMENT,
  `idFil` INT NOT NULL,
  `idSal` INT NOT NULL,
  `idTer` INT NOT NULL,
  `datum` DATE NOT NULL,
  PRIMARY KEY (`idPro`),
  INDEX `projekcija_idFil_fk_idx` (`idFil` ASC) VISIBLE,
  INDEX `prokekcija_idSal_fk_idx` (`idSal` ASC) VISIBLE,
  INDEX `projekcija_idTerl_fk_idx` (`idTer` ASC) VISIBLE,
  CONSTRAINT `projekcija_idFil_fk`
    FOREIGN KEY (`idFil`)
    REFERENCES `cineverse`.`film` (`idFil`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `projekcija_idSal_fk`
    FOREIGN KEY (`idSal`)
    REFERENCES `cineverse`.`sala` (`idSal`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `projekcija_idTerl_fk`
    FOREIGN KEY (`idTer`)
    REFERENCES `cineverse`.`termin` (`idTer`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`sediste`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`sediste` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`sediste` (
  `idSed` INT NOT NULL,
  `idSal` INT NOT NULL,
  `red` INT NOT NULL,
  `kolona` VARCHAR(1) NOT NULL,
  PRIMARY KEY (`idSed`),
  INDEX `sediste_idSal_fk_idx` (`idSal` ASC) VISIBLE,
  CONSTRAINT `sediste_idSal_fk`
    FOREIGN KEY (`idSal`)
    REFERENCES `cineverse`.`sala` (`idSal`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`rezervacija`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`rezervacija` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`rezervacija` (
  `idRez` INT NOT NULL AUTO_INCREMENT,
  `idKor` INT NOT NULL,
  `idPro` INT NOT NULL,
  `idSed` INT NOT NULL,
  PRIMARY KEY (`idRez`),
  INDEX `rezervacija_idKor_fk_idx` (`idKor` ASC) VISIBLE,
  INDEX `rezervacija_idPro_fk_idx` (`idPro` ASC) VISIBLE,
  INDEX `rezervacija_idSed_idx` (`idSed` ASC) VISIBLE,
  CONSTRAINT `rezervacija_idKor_fk`
    FOREIGN KEY (`idKor`)
    REFERENCES `cineverse`.`korisnik` (`idKor`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `rezervacija_idPro_fk`
    FOREIGN KEY (`idPro`)
    REFERENCES `cineverse`.`projekcija` (`idPro`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `rezervacija_idSed_fk`
    FOREIGN KEY (`idSed`)
    REFERENCES `cineverse`.`sediste` (`idSed`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`watchlist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`watchlist` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`watchlist` (
  `idKor` INT NOT NULL,
  `idFil` INT NOT NULL,
  PRIMARY KEY (`idKor`, `idFil`),
  INDEX `watchlist_idFil_fk_idx` (`idFil` ASC) VISIBLE,
  CONSTRAINT `watchlist_idFil_fk`
    FOREIGN KEY (`idFil`)
    REFERENCES `cineverse`.`film` (`idFil`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `watchlist_idKor_fk`
    FOREIGN KEY (`idKor`)
    REFERENCES `cineverse`.`korisnik` (`idKor`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `cineverse`.`zahtev`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cineverse`.`zahtev` ;

CREATE TABLE IF NOT EXISTS `cineverse`.`zahtev` (
  `idZah` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idZah`),
  CONSTRAINT `zahtev_idZah_fk`
    FOREIGN KEY (`idZah`)
    REFERENCES `cineverse`.`nalog` (`idNal`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
