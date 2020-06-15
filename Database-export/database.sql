-- MySQL dump 10.17  Distrib 10.3.17-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	10.3.17-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Notes`
--

DROP TABLE IF EXISTS `Notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Notes` (
  `idNotes` int(11) NOT NULL,
  `NoteName` varchar(8) NOT NULL,
  PRIMARY KEY (`idNotes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Notes`
--

LOCK TABLES `Notes` WRITE;
/*!40000 ALTER TABLE `Notes` DISABLE KEYS */;
INSERT INTO `Notes` VALUES (1,'Pause'),(21,'A0'),(22,'A#0'),(23,'B0'),(24,'C1'),(25,'C#1'),(26,'D1'),(27,'D#1'),(28,'E1'),(29,'F1'),(30,'F#1'),(31,'G1'),(32,'G#1'),(33,'A1'),(34,'A#1'),(35,'B1'),(36,'C2'),(37,'C#2'),(38,'D2'),(39,'D#2'),(40,'E2'),(41,'F2'),(42,'F#2'),(43,'G2'),(44,'G#2'),(45,'A2'),(46,'A#2'),(47,'B2'),(48,'C3'),(49,'C#3'),(50,'D3'),(51,'D#3'),(52,'E3'),(53,'F3'),(54,'F#3'),(55,'G3'),(56,'G#3'),(57,'A3'),(58,'A#3'),(59,'B3'),(60,'C4'),(61,'C#4'),(62,'D4'),(63,'D#4'),(64,'E4'),(65,'F4'),(66,'F#4'),(67,'G4'),(68,'G#4'),(69,'A4'),(70,'A#4'),(71,'B4'),(72,'C5'),(73,'C#5'),(74,'D5'),(75,'D#5'),(76,'E5'),(77,'F5'),(78,'F#5'),(79,'G5'),(80,'G#5'),(81,'A5'),(82,'A#5'),(83,'B5'),(84,'C6'),(85,'C#6'),(86,'D6'),(87,'D#6'),(88,'E6'),(89,'F6'),(90,'F#6'),(91,'G6'),(92,'G#6'),(93,'A6'),(94,'A#6'),(95,'B6'),(96,'C7'),(97,'C#7'),(98,'D7'),(99,'D#7'),(100,'E7'),(101,'F7'),(102,'F#7'),(103,'G7'),(104,'G#7'),(105,'A7'),(106,'A#7'),(107,'B7'),(108,'C8'),(109,'C#8'),(110,'D8'),(111,'D#8'),(112,'E8'),(113,'F8'),(114,'F#8'),(115,'G8'),(116,'G#8'),(117,'A8'),(118,'A#8'),(119,'B8'),(120,'C9'),(121,'C#9'),(122,'D9'),(123,'D#9'),(124,'E9'),(125,'F9'),(126,'F#9'),(127,'G9');
/*!40000 ALTER TABLE `Notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PlaySession`
--

DROP TABLE IF EXISTS `PlaySession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PlaySession` (
  `idPlaySession` int(11) NOT NULL AUTO_INCREMENT,
  `trackName` varchar(45) NOT NULL,
  `duratiion` time NOT NULL,
  `datum` datetime NOT NULL,
  `keyId` int(11) NOT NULL,
  `backtrackInterval` float NOT NULL,
  PRIMARY KEY (`idPlaySession`),
  KEY `fk_PlaySession_key1_idx` (`keyId`),
  CONSTRAINT `fk_PlaySession_key1` FOREIGN KEY (`keyId`) REFERENCES `key` (`idkey`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PlaySession`
--

LOCK TABLES `PlaySession` WRITE;
/*!40000 ALTER TABLE `PlaySession` DISABLE KEYS */;
INSERT INTO `PlaySession` VALUES (1,'Game of Thrones','00:00:31','2020-06-10 16:05:45',2,0.59),(13,'NewSong','00:00:06','2020-06-12 18:17:44',6,0.279486),(14,'Short Song','00:00:04','2020-06-13 22:05:59',1,1),(15,'Nieuw liedje','00:00:06','2020-06-15 15:16:50',8,0.141029),(16,'Abc','00:00:06','2020-06-15 16:04:18',1,1),(17,'PlayTest','00:00:05','2020-06-15 19:04:56',8,1),(18,'NewPlayTest','00:00:06','2020-06-15 19:07:59',8,1);
/*!40000 ALTER TABLE `PlaySession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PlayedNotes`
--

DROP TABLE IF EXISTS `PlayedNotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PlayedNotes` (
  `idPlayedNotes` int(11) NOT NULL AUTO_INCREMENT,
  `noteduration` float NOT NULL,
  `idPlaySession` int(11) NOT NULL,
  `idNotes` int(11) NOT NULL,
  PRIMARY KEY (`idPlayedNotes`),
  KEY `fk_PlayedNotes_PlaySession_idx` (`idPlaySession`),
  KEY `fk_PlayedNotes_Notes1_idx` (`idNotes`),
  CONSTRAINT `fk_PlayedNotes_Notes` FOREIGN KEY (`idNotes`) REFERENCES `Notes` (`idNotes`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_PlayedNotes_PlaySession` FOREIGN KEY (`idPlaySession`) REFERENCES `PlaySession` (`idPlaySession`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=173 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PlayedNotes`
--

LOCK TABLES `PlayedNotes` WRITE;
/*!40000 ALTER TABLE `PlayedNotes` DISABLE KEYS */;
INSERT INTO `PlayedNotes` VALUES (131,0.63,13,1),(132,0.75,13,60),(133,0.02,13,1),(134,0.86,13,61),(135,0.03,13,1),(136,0.75,13,65),(137,0.21,13,1),(138,1.49,13,60),(139,1.27,14,1),(140,0.6,14,60),(141,0,14,1),(142,0.6,14,62),(143,0.03,14,1),(144,0.6,14,60),(145,1.17,15,1),(146,0.68,15,64),(147,0.07,15,1),(148,0.8,15,66),(149,0.1,15,1),(150,0.39,15,67),(151,0.05,15,1),(152,0.14,15,66),(153,0.02,15,1),(154,0.96,15,64),(155,1.18,16,1),(156,0.84,16,60),(157,0.01,16,1),(158,0.85,16,62),(159,0.02,16,1),(160,0.76,16,60),(161,1.1,17,1),(162,0.86,17,71),(163,0.02,17,1),(164,0.82,17,72),(165,0.14,17,1),(166,0.55,17,70),(167,3.6,18,1),(168,0.46,18,71),(169,0.02,18,1),(170,0.74,18,72),(171,0.07,18,1),(172,0.48,18,71);
/*!40000 ALTER TABLE `PlayedNotes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `key`
--

DROP TABLE IF EXISTS `key`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `key` (
  `idkey` int(11) NOT NULL,
  `keyName` varchar(100) NOT NULL,
  `Leadinst` int(11) NOT NULL,
  `Backinst` int(11) NOT NULL,
  `idNote1` int(11) NOT NULL,
  `idNote2` int(11) NOT NULL,
  `idNote3` int(11) NOT NULL,
  `idNote4` int(11) NOT NULL,
  `idNote5` int(11) NOT NULL,
  `idNote6` int(11) NOT NULL,
  `idNote7` int(11) NOT NULL,
  `idNote8` int(11) NOT NULL,
  PRIMARY KEY (`idkey`),
  KEY `fk_key_Notes1_idx` (`idNote1`),
  KEY `fk_key_Notes2_idx` (`idNote2`),
  KEY `fk_key_Notes3_idx` (`idNote3`),
  KEY `fk_key_Notes4_idx` (`idNote4`),
  KEY `fk_key_Notes5_idx` (`idNote5`),
  KEY `fk_key_Notes6_idx` (`idNote6`),
  KEY `fk_key_Notes7_idx` (`idNote7`),
  KEY `fk_key_Notes8_idx` (`idNote8`),
  CONSTRAINT `fk_key_Notes1` FOREIGN KEY (`idNote1`) REFERENCES `Notes` (`idNotes`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_key_Notes2` FOREIGN KEY (`idNote2`) REFERENCES `Notes` (`idNotes`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_key_Notes3` FOREIGN KEY (`idNote3`) REFERENCES `Notes` (`idNotes`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_key_Notes4` FOREIGN KEY (`idNote4`) REFERENCES `Notes` (`idNotes`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_key_Notes5` FOREIGN KEY (`idNote5`) REFERENCES `Notes` (`idNotes`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_key_Notes6` FOREIGN KEY (`idNote6`) REFERENCES `Notes` (`idNotes`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_key_Notes7` FOREIGN KEY (`idNote7`) REFERENCES `Notes` (`idNotes`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_key_Notes8` FOREIGN KEY (`idNote8`) REFERENCES `Notes` (`idNotes`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `key`
--

LOCK TABLES `key` WRITE;
/*!40000 ALTER TABLE `key` DISABLE KEYS */;
INSERT INTO `key` VALUES (1,'CMajor',1,1,60,62,64,65,67,69,71,72),(2,'Aminor',42,42,57,59,60,62,64,65,67,69),(3,'Dmajor',29,18,62,64,66,67,69,71,73,74),(4,'CMajor Pentatonic',19,19,60,62,64,67,69,72,74,76),(5,'Aminor Pentatonic',14,92,57,60,62,64,67,69,72,81),(6,'C Miyako-Bushi',77,79,60,61,65,67,68,72,73,77),(7,'D Persian',86,101,62,63,66,67,69,70,73,74),(8,'E Hungarian minor',75,89,64,66,67,70,71,72,75,76);
/*!40000 ALTER TABLE `key` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-15 19:49:00
