CREATE DATABASE  IF NOT EXISTS `library_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `library_db`;
-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: library_db
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `book_id` int NOT NULL AUTO_INCREMENT,
  `book_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `author` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `publisher` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `total_copies` int NOT NULL DEFAULT '1',
  `available_copies` int NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`book_id`),
  CONSTRAINT `chk_available_copies` CHECK (((`available_copies` >= 0) and (`available_copies` <= `total_copies`))),
  CONSTRAINT `chk_total_copies` CHECK ((`total_copies` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (1,'Concepts of Physics','H C Verma','Physics','Bharati Bhawan',5,4,'2026-11-08 18:48:22'),(2,'Mathematics Class 12','R D Sharma','Mathematics','Dhanpat Rai',4,4,'2026-11-08 18:48:22'),(3,'Organic Chemistry','Morrison and Boyd','Chemistry','Pearson',3,3,'2026-11-08 18:48:22'),(4,'Computer Science with Python','Sumita Arora','Computer Science','Dhanpat Rai',6,6,'2026-11-08 18:48:22'),(5,'Wings of Fire','A P J Abdul Kalam','Biography','Universities Press',2,2,'2026-11-08 18:48:22');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fines`
--

DROP TABLE IF EXISTS `fines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fines` (
  `fine_id` int NOT NULL AUTO_INCREMENT,
  `issue_id` int NOT NULL,
  `fine_type` enum('LATE','DAMAGE') COLLATE utf8mb4_unicode_ci NOT NULL,
  `fine_amount` decimal(10,2) NOT NULL,
  `fine_date` date NOT NULL,
  `payment_status` enum('PENDING','PAID') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDING',
  `payment_date` date DEFAULT NULL,
  `remarks` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`fine_id`),
  KEY `fk_fine_issue` (`issue_id`),
  CONSTRAINT `fk_fine_issue` FOREIGN KEY (`issue_id`) REFERENCES `issue_records` (`issue_id`),
  CONSTRAINT `chk_fine_amount` CHECK ((`fine_amount` > 0)),
  CONSTRAINT `chk_payment_date` CHECK ((((`payment_status` = _utf8mb4'PENDING') and (`payment_date` is null)) or ((`payment_status` = _utf8mb4'PAID') and (`payment_date` is not null))))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fines`
--

LOCK TABLES `fines` WRITE;
/*!40000 ALTER TABLE `fines` DISABLE KEYS */;
INSERT INTO `fines` VALUES (1,1,'LATE',3.00,'2026-11-11','PAID','2026-11-09','Three days late','2026-11-08 18:53:21'),(2,1,'DAMAGE',50.00,'2026-11-11','PENDING',NULL,'Book returned in damaged condition','2026-11-08 18:53:21');
/*!40000 ALTER TABLE `fines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issue_records`
--

DROP TABLE IF EXISTS `issue_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `issue_records` (
  `issue_id` int NOT NULL AUTO_INCREMENT,
  `request_id` int DEFAULT NULL,
  `user_id` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `book_id` int NOT NULL,
  `issue_date` date NOT NULL,
  `loan_days` int NOT NULL DEFAULT '7',
  `due_date` date NOT NULL,
  `return_date` date DEFAULT NULL,
  `status` enum('ISSUED','RETURNED') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ISSUED',
  `return_condition` enum('GOOD','DAMAGED') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`issue_id`),
  UNIQUE KEY `request_id` (`request_id`),
  KEY `fk_issue_user` (`user_id`),
  KEY `fk_issue_book` (`book_id`),
  CONSTRAINT `fk_issue_book` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`),
  CONSTRAINT `fk_issue_request` FOREIGN KEY (`request_id`) REFERENCES `issue_requests` (`request_id`),
  CONSTRAINT `fk_issue_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `chk_loan_days` CHECK ((`loan_days` in (7,15))),
  CONSTRAINT `chk_return_date` CHECK ((((`status` = _utf8mb4'ISSUED') and (`return_date` is null)) or ((`status` = _utf8mb4'RETURNED') and (`return_date` is not null))))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issue_records`
--

LOCK TABLES `issue_records` WRITE;
/*!40000 ALTER TABLE `issue_records` DISABLE KEYS */;
INSERT INTO `issue_records` VALUES (1,NULL,'TCH1001',5,'2026-11-01',7,'2026-11-08','2026-11-11','RETURNED','DAMAGED','2026-11-08 18:51:44'),(2,1,'STU1001',1,'2026-11-09',15,'2026-11-24',NULL,'ISSUED',NULL,'2026-11-09 11:42:35'),(3,3,'12B23',4,'2026-11-09',7,'2026-11-16','2026-11-09','RETURNED','GOOD','2026-11-09 12:10:13');
/*!40000 ALTER TABLE `issue_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issue_requests`
--

DROP TABLE IF EXISTS `issue_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `issue_requests` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `book_id` int NOT NULL,
  `request_date` date NOT NULL,
  `status` enum('PENDING','APPROVED','REJECTED','ISSUED','CANCELLED') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDING',
  `remarks` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`request_id`),
  KEY `fk_request_user` (`user_id`),
  KEY `fk_request_book` (`book_id`),
  CONSTRAINT `fk_request_book` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`),
  CONSTRAINT `fk_request_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issue_requests`
--

LOCK TABLES `issue_requests` WRITE;
/*!40000 ALTER TABLE `issue_requests` DISABLE KEYS */;
INSERT INTO `issue_requests` VALUES (1,'STU1001',1,'2026-11-01','APPROVED','Physics reference book','2026-11-08 18:51:32'),(2,'STU1002',4,'2026-11-02','PENDING','Required for computer studies','2026-11-08 18:51:32'),(3,'12B23',4,'2026-11-09','APPROVED',NULL,'2026-11-09 12:09:41');
/*!40000 ALTER TABLE `issue_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('STUDENT','TEACHER','LIBRARIAN') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'STUDENT',
  `joining_date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('101','Sanjay','Sharma','ss@gmail.com','1234567890','db4734a417db8a285f109dce7f43415b:2e66d78e33a781ac7350a68a327065a2bec2ff649adf4426781ad2f38288b2a1','LIBRARIAN','2026-11-09','2026-11-09 10:26:30'),('12B23','Ojasi','Kushagra','ok@gmail.com','0987654321','9f5d06e4198988aaa21297b606bd0a82:9ed858eebbf61afc3ca5141ad40bff9f5b39a4240e506a67c512842966d0599b','STUDENT','2026-11-09','2026-11-09 10:32:48'),('LIB1001','Neha','Singh','neha@example.com','9876543213','DEMO_HASH_4','LIBRARIAN','2026-04-01','2026-11-08 18:47:04'),('STU1001','Aarav','Sharma','aarav@example.com','9876543210','DEMO_HASH_1','STUDENT','2026-04-01','2026-11-08 18:47:04'),('STU1002','Ananya','Verma','ananya@example.com','9876543211','DEMO_HASH_2','STUDENT','2026-04-02','2026-11-08 18:47:04'),('TCH1001','Rahul','Mehta','rahul@example.com','9876543212','DEMO_HASH_3','TEACHER','2026-04-03','2026-11-08 18:47:04');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-09 17:51:46
