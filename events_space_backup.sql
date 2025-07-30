-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: events_space
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_verification`
--

DROP TABLE IF EXISTS `account_verification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_verification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `verification_token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` timestamp NOT NULL,
  `is_used` tinyint(1) DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `verification_token` (`verification_token`),
  KEY `ix_account_verification` (`deleted_at`),
  KEY `ix_account_verification_token` (`verification_token`),
  KEY `fk_accountverification_user` (`user_id`),
  CONSTRAINT `fk_accountverification_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_verification`
--

LOCK TABLES `account_verification` WRITE;
/*!40000 ALTER TABLE `account_verification` DISABLE KEYS */;
INSERT INTO `account_verification` VALUES (10,19,'4f693fb8-082d-4ea1-8d98-45a0735c1f60','2025-07-27 22:04:45',0,'2025-07-28 00:04:44','2025-07-28 00:04:44',NULL);
/*!40000 ALTER TABLE `account_verification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity_log`
--

DROP TABLE IF EXISTS `activity_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `target` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ip_address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `additional_data` json DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_activity_log` (`action`,`deleted_at`),
  KEY `fk_activitylog_user` (`user_id`),
  CONSTRAINT `fk_activitylog_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=421 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_log`
--

LOCK TABLES `activity_log` WRITE;
/*!40000 ALTER TABLE `activity_log` DISABLE KEYS */;
INSERT INTO `activity_log` VALUES (1,1,'USER_LOGIN','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 18:28:29','2025-07-27 18:28:29',NULL),(2,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 18:28:29','2025-07-27 18:28:29',NULL),(3,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:28:33','2025-07-27 18:28:33',NULL),(4,1,'VIEW_ORG_UNITS','jkumwenda@gmail.com','127.0.0.1','\"Get all org units\"','2025-07-27 18:28:35','2025-07-27 18:28:35',NULL),(5,1,'VIEW_ORG_UNITS','jkumwenda@gmail.com','127.0.0.1','\"Get all org units\"','2025-07-27 18:31:40','2025-07-27 18:31:40',NULL),(6,1,'ADD_ORG_UNIT','jkumwenda@gmail.com','127.0.0.1','\"ECSA-HC\"','2025-07-27 18:32:14','2025-07-27 18:32:14',NULL),(7,1,'VIEW_ORG_UNITS','jkumwenda@gmail.com','127.0.0.1','\"Get all org units\"','2025-07-27 18:32:14','2025-07-27 18:32:14',NULL),(8,1,'VIEW_ORG_UNITS','jkumwenda@gmail.com','127.0.0.1','\"Get all org units\"','2025-07-27 18:32:39','2025-07-27 18:32:39',NULL),(9,1,'ADD_EVENT','jkumwenda@gmail.com','127.0.0.1','\"15ᵗʰ Best Practices Forum & 31ˢᵗ DJCC Meeting\"','2025-07-27 18:36:46','2025-07-27 18:36:46',NULL),(10,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:36:46','2025-07-27 18:36:46',NULL),(11,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:37:05','2025-07-27 18:37:05',NULL),(12,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 18:37:08','2025-07-27 18:37:08',NULL),(13,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 18:37:19','2025-07-27 18:37:19',NULL),(14,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 18:40:22','2025-07-27 18:40:22',NULL),(15,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 18:40:47','2025-07-27 18:40:47',NULL),(16,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 18:45:41','2025-07-27 18:45:41',NULL),(17,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 18:45:47','2025-07-27 18:45:47',NULL),(18,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:45:48','2025-07-27 18:45:48',NULL),(19,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 18:45:49','2025-07-27 18:45:49',NULL),(20,1,'DOWNLOAD_PARTICIPANTS','jkumwenda@gmail.com','127.0.0.1','\"Downloaded participants for event 15 with filter paid=all\"','2025-07-27 18:45:58','2025-07-27 18:45:58',NULL),(21,1,'DOWNLOAD_PARTICIPANTS','jkumwenda@gmail.com','127.0.0.1','\"Downloaded participants for event 15 with filter paid=true\"','2025-07-27 18:46:00','2025-07-27 18:46:00',NULL),(22,1,'DOWNLOAD_BADGES','jkumwenda@gmail.com','127.0.0.1','\"Downloaded participant badges for event 15 with filter paid=true\"','2025-07-27 18:46:06','2025-07-27 18:46:06',NULL),(23,1,'DOWNLOAD_PARTICIPANTS','jkumwenda@gmail.com','127.0.0.1','\"Downloaded participants for event 15 with filter paid=false\"','2025-07-27 18:46:17','2025-07-27 18:46:17',NULL),(24,1,'DOWNLOAD_BADGES','jkumwenda@gmail.com','127.0.0.1','\"Downloaded participant badges for event 15 with filter paid=all\"','2025-07-27 18:46:39','2025-07-27 18:46:39',NULL),(25,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 18:46:49','2025-07-27 18:46:49',NULL),(26,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 18:46:50','2025-07-27 18:46:50',NULL),(27,1,'UPDATE_USER','jkumwenda@gmail.com','127.0.0.1','\"Update user id 1\"','2025-07-27 18:46:54','2025-07-27 18:46:54',NULL),(28,1,'UPDATE_USER','jkumwenda@gmail.com','127.0.0.1','\"Update user id 1\"','2025-07-27 18:46:54','2025-07-27 18:46:54',NULL),(29,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 18:46:54','2025-07-27 18:46:54',NULL),(30,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 18:46:57','2025-07-27 18:46:57',NULL),(31,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:47:01','2025-07-27 18:47:01',NULL),(32,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 18:47:03','2025-07-27 18:47:03',NULL),(33,1,'DOWNLOAD_BADGES','jkumwenda@gmail.com','127.0.0.1','\"Downloaded participant badges for event 15 with filter paid=all\"','2025-07-27 18:47:06','2025-07-27 18:47:06',NULL),(34,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 18:48:01','2025-07-27 18:48:01',NULL),(35,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 18:48:06','2025-07-27 18:48:06',NULL),(36,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 18:48:11','2025-07-27 18:48:11',NULL),(37,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:48:12','2025-07-27 18:48:12',NULL),(38,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 18:48:14','2025-07-27 18:48:14',NULL),(39,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 18:48:43','2025-07-27 18:48:43',NULL),(40,1,'ADD_EVENT','jkumwenda@gmail.com','127.0.0.1','15','2025-07-27 18:49:08','2025-07-27 18:49:08',NULL),(41,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 18:49:08','2025-07-27 18:49:08',NULL),(42,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 18:49:10','2025-07-27 18:49:10',NULL),(43,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 18:49:12','2025-07-27 18:49:12',NULL),(44,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:49:25','2025-07-27 18:49:25',NULL),(45,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 18:49:27','2025-07-27 18:49:27',NULL),(46,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:49:43','2025-07-27 18:49:43',NULL),(47,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 18:49:45','2025-07-27 18:49:45',NULL),(48,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 18:49:46','2025-07-27 18:49:46',NULL),(49,1,'VIEW_ORG_UNITS','jkumwenda@gmail.com','127.0.0.1','\"Get all org units\"','2025-07-27 18:49:48','2025-07-27 18:49:48',NULL),(50,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 18:49:49','2025-07-27 18:49:49',NULL),(51,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 18:49:49','2025-07-27 18:49:49',NULL),(52,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 18:50:05','2025-07-27 18:50:05',NULL),(53,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:50:09','2025-07-27 18:50:09',NULL),(54,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 18:50:29','2025-07-27 18:50:29',NULL),(55,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:51:41','2025-07-27 18:51:41',NULL),(56,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:51:46','2025-07-27 18:51:46',NULL),(57,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:51:46','2025-07-27 18:51:46',NULL),(58,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:51:47','2025-07-27 18:51:47',NULL),(59,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:51:49','2025-07-27 18:51:49',NULL),(60,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 18:52:21','2025-07-27 18:52:21',NULL),(61,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 18:52:24','2025-07-27 18:52:24',NULL),(62,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 18:55:18','2025-07-27 18:55:18',NULL),(63,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:00:13','2025-07-27 19:00:13',NULL),(64,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:00:16','2025-07-27 19:00:16',NULL),(65,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:00:32','2025-07-27 19:00:32',NULL),(66,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:01:59','2025-07-27 19:01:59',NULL),(67,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 19:01:59','2025-07-27 19:01:59',NULL),(68,1,'VIEW_ORG_UNITS','jkumwenda@gmail.com','127.0.0.1','\"Get all org units\"','2025-07-27 19:01:59','2025-07-27 19:01:59',NULL),(69,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:02:01','2025-07-27 19:02:01',NULL),(70,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:02:11','2025-07-27 19:02:11',NULL),(71,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:06:24','2025-07-27 19:06:24',NULL),(72,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:08:16','2025-07-27 19:08:16',NULL),(73,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 19:17:33','2025-07-27 19:17:33',NULL),(74,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:17:34','2025-07-27 19:17:34',NULL),(75,1,'VIEW_ORG_UNITS','jkumwenda@gmail.com','127.0.0.1','\"Get all org units\"','2025-07-27 19:17:34','2025-07-27 19:17:34',NULL),(76,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:17:34','2025-07-27 19:17:34',NULL),(77,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:17:47','2025-07-27 19:17:47',NULL),(78,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:19:40','2025-07-27 19:19:40',NULL),(79,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:27:20','2025-07-27 19:27:20',NULL),(80,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:27:26','2025-07-27 19:27:26',NULL),(81,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:33:21','2025-07-27 19:33:21',NULL),(82,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:38:16','2025-07-27 19:38:16',NULL),(83,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:46:03','2025-07-27 19:46:03',NULL),(84,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 36 and associated permissions\"','2025-07-27 19:46:03','2025-07-27 19:46:03',NULL),(85,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:46:09','2025-07-27 19:46:09',NULL),(86,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:48:37','2025-07-27 19:48:37',NULL),(87,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 19:52:35','2025-07-27 19:52:35',NULL),(88,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 20:00:24','2025-07-27 20:00:24',NULL),(89,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 20:00:32','2025-07-27 20:00:32',NULL),(90,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 20:03:58','2025-07-27 20:03:58',NULL),(91,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 20:14:37','2025-07-27 20:14:37',NULL),(92,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 20:15:42','2025-07-27 20:15:42',NULL),(93,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 20:23:31','2025-07-27 20:23:31',NULL),(94,1,'DOWNLOAD_BADGES','jkumwenda@gmail.com','127.0.0.1','\"Downloaded participant badges for event 15 with filter paid=all\"','2025-07-27 20:23:35','2025-07-27 20:23:35',NULL),(95,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 20:25:23','2025-07-27 20:25:23',NULL),(96,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 20:38:53','2025-07-27 20:38:53',NULL),(97,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 20:39:00','2025-07-27 20:39:00',NULL),(98,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 20:39:06','2025-07-27 20:39:06',NULL),(99,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 20:39:09','2025-07-27 20:39:09',NULL),(100,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 20:39:11','2025-07-27 20:39:11',NULL),(101,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 20:39:13','2025-07-27 20:39:13',NULL),(102,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 20:39:16','2025-07-27 20:39:16',NULL),(103,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 20:39:19','2025-07-27 20:39:19',NULL),(104,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:05:38','2025-07-27 21:05:38',NULL),(105,1,'VIEW_ORG_UNITS','jkumwenda@gmail.com','127.0.0.1','\"Get all org units\"','2025-07-27 21:05:39','2025-07-27 21:05:39',NULL),(106,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:05:39','2025-07-27 21:05:39',NULL),(107,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:06:08','2025-07-27 21:06:08',NULL),(108,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:09:31','2025-07-27 21:09:31',NULL),(109,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 21:09:32','2025-07-27 21:09:32',NULL),(110,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 21:09:33','2025-07-27 21:09:33',NULL),(111,1,'VIEW_ORG_UNITS','jkumwenda@gmail.com','127.0.0.1','\"Get all org units\"','2025-07-27 21:09:33','2025-07-27 21:09:33',NULL),(112,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:09:34','2025-07-27 21:09:34',NULL),(113,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:09:49','2025-07-27 21:09:49',NULL),(114,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:10:44','2025-07-27 21:10:44',NULL),(115,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:10:46','2025-07-27 21:10:46',NULL),(116,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:11:05','2025-07-27 21:11:05',NULL),(117,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:11:07','2025-07-27 21:11:07',NULL),(118,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:11:08','2025-07-27 21:11:08',NULL),(119,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:11:09','2025-07-27 21:11:09',NULL),(120,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:11:42','2025-07-27 21:11:42',NULL),(121,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:12:51','2025-07-27 21:12:51',NULL),(122,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:13:02','2025-07-27 21:13:02',NULL),(123,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:14:18','2025-07-27 21:14:18',NULL),(124,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:14:18','2025-07-27 21:14:18',NULL),(125,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:15:31','2025-07-27 21:15:31',NULL),(126,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:17:55','2025-07-27 21:17:55',NULL),(127,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:18:01','2025-07-27 21:18:01',NULL),(128,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:20:17','2025-07-27 21:20:17',NULL),(129,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:20:21','2025-07-27 21:20:21',NULL),(130,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:20:23','2025-07-27 21:20:23',NULL),(131,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:20:25','2025-07-27 21:20:25',NULL),(132,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:20:49','2025-07-27 21:20:49',NULL),(133,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:22:07','2025-07-27 21:22:07',NULL),(134,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:22:08','2025-07-27 21:22:08',NULL),(135,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:22:10','2025-07-27 21:22:10',NULL),(136,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:22:12','2025-07-27 21:22:12',NULL),(137,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:22:14','2025-07-27 21:22:14',NULL),(138,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:22:39','2025-07-27 21:22:39',NULL),(139,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:22:51','2025-07-27 21:22:51',NULL),(140,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:22:52','2025-07-27 21:22:52',NULL),(141,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:22:52','2025-07-27 21:22:52',NULL),(142,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:23:09','2025-07-27 21:23:09',NULL),(143,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:23:09','2025-07-27 21:23:09',NULL),(144,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:23:10','2025-07-27 21:23:10',NULL),(145,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:23:37','2025-07-27 21:23:37',NULL),(146,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:24:11','2025-07-27 21:24:11',NULL),(147,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:24:14','2025-07-27 21:24:14',NULL),(148,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:24:15','2025-07-27 21:24:15',NULL),(149,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:24:15','2025-07-27 21:24:15',NULL),(150,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:24:26','2025-07-27 21:24:26',NULL),(151,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:24:55','2025-07-27 21:24:55',NULL),(152,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:24:57','2025-07-27 21:24:57',NULL),(153,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 1 and associated permissions\"','2025-07-27 21:26:11','2025-07-27 21:26:11',NULL),(154,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:26:25','2025-07-27 21:26:25',NULL),(155,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:31:51','2025-07-27 21:31:51',NULL),(156,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:32:00','2025-07-27 21:32:00',NULL),(157,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:32:04','2025-07-27 21:32:04',NULL),(158,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:32:06','2025-07-27 21:32:06',NULL),(159,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:32:21','2025-07-27 21:32:21',NULL),(160,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:34:10','2025-07-27 21:34:10',NULL),(161,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:38:16','2025-07-27 21:38:16',NULL),(162,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:38:17','2025-07-27 21:38:17',NULL),(163,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:38:20','2025-07-27 21:38:20',NULL),(164,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:38:20','2025-07-27 21:38:20',NULL),(165,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:38:33','2025-07-27 21:38:33',NULL),(166,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:40:14','2025-07-27 21:40:14',NULL),(167,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:40:58','2025-07-27 21:40:58',NULL),(168,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:41:37','2025-07-27 21:41:37',NULL),(169,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:42:55','2025-07-27 21:42:55',NULL),(170,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:44:01','2025-07-27 21:44:01',NULL),(171,1,'USER_LOGIN','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 21:45:20','2025-07-27 21:45:20',NULL),(172,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 21:45:20','2025-07-27 21:45:20',NULL),(173,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:45:22','2025-07-27 21:45:22',NULL),(174,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:45:24','2025-07-27 21:45:24',NULL),(175,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:45:29','2025-07-27 21:45:29',NULL),(176,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:45:52','2025-07-27 21:45:52',NULL),(177,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 21:45:59','2025-07-27 21:45:59',NULL),(178,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:46:10','2025-07-27 21:46:10',NULL),(179,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 21:46:12','2025-07-27 21:46:12',NULL),(180,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:46:14','2025-07-27 21:46:14',NULL),(181,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:53:49','2025-07-27 21:53:49',NULL),(182,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:53:51','2025-07-27 21:53:51',NULL),(183,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:57:46','2025-07-27 21:57:46',NULL),(184,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 21:57:49','2025-07-27 21:57:49',NULL),(185,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 22:08:09','2025-07-27 22:08:09',NULL),(186,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 22:14:05','2025-07-27 22:14:05',NULL),(187,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 22:15:32','2025-07-27 22:15:32',NULL),(188,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:28:25','2025-07-27 22:28:25',NULL),(189,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:28:25','2025-07-27 22:28:25',NULL),(190,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 22:28:36','2025-07-27 22:28:36',NULL),(192,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 22:34:40','2025-07-27 22:34:40',NULL),(193,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:42:29','2025-07-27 22:42:29',NULL),(194,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:42:32','2025-07-27 22:42:32',NULL),(195,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:42:51','2025-07-27 22:42:51',NULL),(196,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:42:53','2025-07-27 22:42:53',NULL),(197,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:42:56','2025-07-27 22:42:56',NULL),(198,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:43:00','2025-07-27 22:43:00',NULL),(199,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:43:11','2025-07-27 22:43:11',NULL),(200,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:43:15','2025-07-27 22:43:15',NULL),(201,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:43:17','2025-07-27 22:43:17',NULL),(202,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:43:19','2025-07-27 22:43:19',NULL),(203,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 22:45:31','2025-07-27 22:45:31',NULL),(204,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:45:48','2025-07-27 22:45:48',NULL),(205,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:46:14','2025-07-27 22:46:14',NULL),(206,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:46:23','2025-07-27 22:46:23',NULL),(207,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 22:47:56','2025-07-27 22:47:56',NULL),(208,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 22:48:02','2025-07-27 22:48:02',NULL),(209,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:48:15','2025-07-27 22:48:15',NULL),(210,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:49:58','2025-07-27 22:49:58',NULL),(211,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:50:15','2025-07-27 22:50:15',NULL),(212,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:50:15','2025-07-27 22:50:15',NULL),(213,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:50:24','2025-07-27 22:50:24',NULL),(214,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:50:25','2025-07-27 22:50:25',NULL),(215,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:50:26','2025-07-27 22:50:26',NULL),(216,1,'RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"58440d78-e17a-44ea-8ee6-88f863f45484\"','2025-07-27 22:51:01','2025-07-27 22:51:01',NULL),(217,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:51:35','2025-07-27 22:51:35',NULL),(218,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:51:42','2025-07-27 22:51:42',NULL),(219,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 22:55:17','2025-07-27 22:55:17',NULL),(220,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:56:37','2025-07-27 22:56:37',NULL),(221,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 22:56:41','2025-07-27 22:56:41',NULL),(222,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 22:57:13','2025-07-27 22:57:13',NULL),(223,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 22:57:17','2025-07-27 22:57:17',NULL),(224,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 22:59:54','2025-07-27 22:59:54',NULL),(225,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:07:55','2025-07-27 23:07:55',NULL),(226,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:07:55','2025-07-27 23:07:55',NULL),(227,1,'USER_LOGIN','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 23:08:03','2025-07-27 23:08:03',NULL),(228,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:08:03','2025-07-27 23:08:03',NULL),(229,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:08:11','2025-07-27 23:08:11',NULL),(230,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 23:08:13','2025-07-27 23:08:13',NULL),(231,1,'DOWNLOAD_PARTICIPANTS','jkumwenda@gmail.com','127.0.0.1','\"Downloaded participants for event 15 with filter paid=all\"','2025-07-27 23:08:16','2025-07-27 23:08:16',NULL),(232,1,'DOWNLOAD_PARTICIPANTS','jkumwenda@gmail.com','127.0.0.1','\"Downloaded participants for event 15 with filter paid=true\"','2025-07-27 23:08:18','2025-07-27 23:08:18',NULL),(233,1,'DOWNLOAD_BADGES','jkumwenda@gmail.com','127.0.0.1','\"Downloaded participant badges for event 15 with filter paid=true\"','2025-07-27 23:08:21','2025-07-27 23:08:21',NULL),(234,1,'DOWNLOAD_BADGES','jkumwenda@gmail.com','127.0.0.1','\"Downloaded participant badges for event 15 with filter paid=all\"','2025-07-27 23:08:24','2025-07-27 23:08:24',NULL),(235,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 23:09:49','2025-07-27 23:09:49',NULL),(236,1,'RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"c1cda6a1-0694-45b8-a5bb-296882943012\"','2025-07-27 23:10:10','2025-07-27 23:10:10',NULL),(237,1,'USER_RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 23:12:24','2025-07-27 23:12:24',NULL),(238,1,'RESET_PASSWORD','jkumwenda@gmail.com','127.0.0.1','\"9b32b112-a814-424a-8766-8b6389b29f8f\"','2025-07-27 23:12:43','2025-07-27 23:12:43',NULL),(239,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:13:40','2025-07-27 23:13:40',NULL),(240,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:13:41','2025-07-27 23:13:41',NULL),(241,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 23:13:42','2025-07-27 23:13:42',NULL),(242,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:13:48','2025-07-27 23:13:48',NULL),(243,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:13:52','2025-07-27 23:13:52',NULL),(244,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 23:13:53','2025-07-27 23:13:53',NULL),(245,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-27 23:13:58','2025-07-27 23:13:58',NULL),(246,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:14:01','2025-07-27 23:14:01',NULL),(247,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:14:03','2025-07-27 23:14:03',NULL),(248,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:16:25','2025-07-27 23:16:25',NULL),(249,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:18:09','2025-07-27 23:18:09',NULL),(250,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:18:27','2025-07-27 23:18:27',NULL),(251,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:18:30','2025-07-27 23:18:30',NULL),(252,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:18:30','2025-07-27 23:18:30',NULL),(253,1,'USER_LOGIN','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 23:18:46','2025-07-27 23:18:46',NULL),(254,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:18:47','2025-07-27 23:18:47',NULL),(255,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:18:48','2025-07-27 23:18:48',NULL),(256,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:18:50','2025-07-27 23:18:50',NULL),(257,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:18:51','2025-07-27 23:18:51',NULL),(258,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:18:51','2025-07-27 23:18:51',NULL),(259,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:19:07','2025-07-27 23:19:07',NULL),(260,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:19:23','2025-07-27 23:19:23',NULL),(261,1,'VIEW_ROLE','jkumwenda@gmail.com','127.0.0.1','\"View role id 1 and associated permissions\"','2025-07-27 23:19:24','2025-07-27 23:19:24',NULL),(262,1,'VIEW_PERMISSIONS','jkumwenda@gmail.com','127.0.0.1','\"Get all permissions\"','2025-07-27 23:19:24','2025-07-27 23:19:24',NULL),(263,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:19:31','2025-07-27 23:19:31',NULL),(264,1,'VIEW_ROLE','jkumwenda@gmail.com','127.0.0.1','\"View role id 1 and associated permissions\"','2025-07-27 23:19:36','2025-07-27 23:19:36',NULL),(265,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 23:19:37','2025-07-27 23:19:37',NULL),(266,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:21:26','2025-07-27 23:21:26',NULL),(267,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:23:58','2025-07-27 23:23:58',NULL),(268,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:25:15','2025-07-27 23:25:15',NULL),(269,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:25:18','2025-07-27 23:25:18',NULL),(270,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:25:25','2025-07-27 23:25:25',NULL),(271,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:26:31','2025-07-27 23:26:31',NULL),(272,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:26:32','2025-07-27 23:26:32',NULL),(273,1,'VIEW_PERMISSIONS','jkumwenda@gmail.com','127.0.0.1','\"Get all permissions\"','2025-07-27 23:26:34','2025-07-27 23:26:34',NULL),(274,1,'VIEW_ROLE','jkumwenda@gmail.com','127.0.0.1','\"View role id 18 and associated permissions\"','2025-07-27 23:26:34','2025-07-27 23:26:34',NULL),(275,1,'VIEW_ROLE','jkumwenda@gmail.com','127.0.0.1','\"View role id 18 and associated permissions\"','2025-07-27 23:26:50','2025-07-27 23:26:50',NULL),(276,1,'VIEW_PERMISSIONS','jkumwenda@gmail.com','127.0.0.1','\"Get all permissions\"','2025-07-27 23:26:50','2025-07-27 23:26:50',NULL),(277,1,'VIEW_PERMISSIONS','jkumwenda@gmail.com','127.0.0.1','\"Get all permissions\"','2025-07-27 23:26:52','2025-07-27 23:26:52',NULL),(278,1,'VIEW_ROLE','jkumwenda@gmail.com','127.0.0.1','\"View role id 18 and associated permissions\"','2025-07-27 23:26:52','2025-07-27 23:26:52',NULL),(279,1,'VIEW_PERMISSIONS','jkumwenda@gmail.com','127.0.0.1','\"Get all permissions\"','2025-07-27 23:27:08','2025-07-27 23:27:08',NULL),(280,1,'VIEW_ROLE','jkumwenda@gmail.com','127.0.0.1','\"View role id 18 and associated permissions\"','2025-07-27 23:27:08','2025-07-27 23:27:08',NULL),(281,1,'VIEW_ROLE','jkumwenda@gmail.com','127.0.0.1','\"View role id 18 and associated permissions\"','2025-07-27 23:27:12','2025-07-27 23:27:12',NULL),(282,1,'VIEW_PERMISSIONS','jkumwenda@gmail.com','127.0.0.1','\"Get all permissions\"','2025-07-27 23:27:12','2025-07-27 23:27:12',NULL),(283,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:27:14','2025-07-27 23:27:14',NULL),(284,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:27:15','2025-07-27 23:27:15',NULL),(285,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:27:18','2025-07-27 23:27:18',NULL),(286,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:27:21','2025-07-27 23:27:21',NULL),(287,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:27:22','2025-07-27 23:27:22',NULL),(288,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:27:23','2025-07-27 23:27:23',NULL),(289,1,'USER_LOGIN','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 23:28:12','2025-07-27 23:28:12',NULL),(290,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:28:14','2025-07-27 23:28:14',NULL),(291,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:30:34','2025-07-27 23:30:34',NULL),(292,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:30:46','2025-07-27 23:30:46',NULL),(293,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:30:48','2025-07-27 23:30:48',NULL),(294,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 18 and associated permissions\"','2025-07-27 23:32:33','2025-07-27 23:32:33',NULL),(295,1,'UPDATE_USER','jkumwenda@gmail.com','127.0.0.1','\"Update user id 18\"','2025-07-27 23:32:43','2025-07-27 23:32:43',NULL),(296,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:32:43','2025-07-27 23:32:43',NULL),(297,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:33:19','2025-07-27 23:33:19',NULL),(298,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:34:44','2025-07-27 23:34:44',NULL),(299,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:34:45','2025-07-27 23:34:45',NULL),(300,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:34:48','2025-07-27 23:34:48',NULL),(301,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:34:49','2025-07-27 23:34:49',NULL),(302,1,'VIEW_ROLE','jkumwenda@gmail.com','127.0.0.1','\"View role id 1 and associated permissions\"','2025-07-27 23:34:54','2025-07-27 23:34:54',NULL),(303,1,'VIEW_PERMISSIONS','jkumwenda@gmail.com','127.0.0.1','\"Get all permissions\"','2025-07-27 23:34:54','2025-07-27 23:34:54',NULL),(304,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:36:45','2025-07-27 23:36:45',NULL),(305,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:36:53','2025-07-27 23:36:53',NULL),(306,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:39:16','2025-07-27 23:39:16',NULL),(307,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:39:29','2025-07-27 23:39:29',NULL),(308,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:39:31','2025-07-27 23:39:31',NULL),(309,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:39:39','2025-07-27 23:39:39',NULL),(310,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:41:56','2025-07-27 23:41:56',NULL),(311,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 23:41:56','2025-07-27 23:41:56',NULL),(312,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:42:07','2025-07-27 23:42:07',NULL),(313,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 23:42:07','2025-07-27 23:42:07',NULL),(314,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:42:35','2025-07-27 23:42:35',NULL),(315,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 23:42:35','2025-07-27 23:42:35',NULL),(316,1,'USER_LOGIN','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 23:45:25','2025-07-27 23:45:25',NULL),(317,1,'USER_LOGIN','jkumwenda@gmail.com','127.0.0.1','\"jkumwenda@gmail.com\"','2025-07-27 23:48:02','2025-07-27 23:48:02',NULL),(318,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 23:48:14','2025-07-27 23:48:14',NULL),(319,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:48:14','2025-07-27 23:48:14',NULL),(320,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:54:34','2025-07-27 23:54:34',NULL),(321,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 23:54:34','2025-07-27 23:54:34',NULL),(322,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:54:36','2025-07-27 23:54:36',NULL),(323,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:54:37','2025-07-27 23:54:37',NULL),(324,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 23:54:37','2025-07-27 23:54:37',NULL),(325,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 23:54:43','2025-07-27 23:54:43',NULL),(326,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:54:43','2025-07-27 23:54:43',NULL),(327,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:56:11','2025-07-27 23:56:11',NULL),(328,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 23:56:12','2025-07-27 23:56:12',NULL),(329,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:56:13','2025-07-27 23:56:13',NULL),(330,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:56:15','2025-07-27 23:56:15',NULL),(331,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 23:56:15','2025-07-27 23:56:15',NULL),(332,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:56:16','2025-07-27 23:56:16',NULL),(333,1,'VIEW_ROLES','jkumwenda@gmail.com','127.0.0.1','\"Get all roles\"','2025-07-27 23:56:18','2025-07-27 23:56:18',NULL),(334,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:56:18','2025-07-27 23:56:18',NULL),(335,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:56:22','2025-07-27 23:56:22',NULL),(336,1,'VIEW_USER','jkumwenda@gmail.com','127.0.0.1','\"View user id 1 and associated permissions\"','2025-07-27 23:56:26','2025-07-27 23:56:26',NULL),(337,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:56:27','2025-07-27 23:56:27',NULL),(338,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:56:30','2025-07-27 23:56:30',NULL),(339,1,'VIEW_USERS','jkumwenda@gmail.com','127.0.0.1','\"Get all users\"','2025-07-27 23:56:37','2025-07-27 23:56:37',NULL),(340,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:56:45','2025-07-27 23:56:45',NULL),(341,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:56:50','2025-07-27 23:56:50',NULL),(342,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:56:52','2025-07-27 23:56:52',NULL),(343,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-27 23:59:56','2025-07-27 23:59:56',NULL),(344,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:00:18','2025-07-28 00:00:18',NULL),(345,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:00:25','2025-07-28 00:00:25',NULL),(346,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:00:54','2025-07-28 00:00:54',NULL),(347,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:00:57','2025-07-28 00:00:57',NULL),(348,19,'USER_REGISTER','jkumwewewewewenda@gmail.com','127.0.0.1','\"jkumwewewewewenda@gmail.com\"','2025-07-28 00:04:44','2025-07-28 00:04:44',NULL),(349,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:06:39','2025-07-28 00:06:39',NULL),(350,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:06:41','2025-07-28 00:06:41',NULL),(351,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:06:42','2025-07-28 00:06:42',NULL),(352,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:06:43','2025-07-28 00:06:43',NULL),(353,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-28 00:06:44','2025-07-28 00:06:44',NULL),(354,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:06:53','2025-07-28 00:06:53',NULL),(355,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:06:53','2025-07-28 00:06:53',NULL),(356,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:06:55','2025-07-28 00:06:55',NULL),(357,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:10:26','2025-07-28 00:10:26',NULL),(358,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:10:29','2025-07-28 00:10:29',NULL),(359,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:10:29','2025-07-28 00:10:29',NULL),(360,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:10:29','2025-07-28 00:10:29',NULL),(361,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:10:30','2025-07-28 00:10:30',NULL),(362,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:10:30','2025-07-28 00:10:30',NULL),(363,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:10:30','2025-07-28 00:10:30',NULL),(364,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:10:31','2025-07-28 00:10:31',NULL),(365,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:11:20','2025-07-28 00:11:20',NULL),(366,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:11:22','2025-07-28 00:11:22',NULL),(367,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:11:26','2025-07-28 00:11:26',NULL),(368,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:11:28','2025-07-28 00:11:28',NULL),(369,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:11:28','2025-07-28 00:11:28',NULL),(370,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:11:29','2025-07-28 00:11:29',NULL),(371,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:11:29','2025-07-28 00:11:29',NULL),(372,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:11:29','2025-07-28 00:11:29',NULL),(373,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:11:29','2025-07-28 00:11:29',NULL),(374,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:11:30','2025-07-28 00:11:30',NULL),(375,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:11:41','2025-07-28 00:11:41',NULL),(376,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:12:57','2025-07-28 00:12:57',NULL),(377,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:08','2025-07-28 00:13:08',NULL),(378,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:10','2025-07-28 00:13:10',NULL),(379,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:11','2025-07-28 00:13:11',NULL),(380,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:12','2025-07-28 00:13:12',NULL),(381,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:12','2025-07-28 00:13:12',NULL),(382,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:12','2025-07-28 00:13:12',NULL),(383,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:13','2025-07-28 00:13:13',NULL),(384,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:13','2025-07-28 00:13:13',NULL),(385,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:13','2025-07-28 00:13:13',NULL),(386,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:14','2025-07-28 00:13:14',NULL),(387,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:14','2025-07-28 00:13:14',NULL),(388,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:14','2025-07-28 00:13:14',NULL),(389,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:15','2025-07-28 00:13:15',NULL),(390,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:26','2025-07-28 00:13:26',NULL),(391,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:28','2025-07-28 00:13:28',NULL),(392,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:28','2025-07-28 00:13:28',NULL),(393,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:29','2025-07-28 00:13:29',NULL),(394,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:29','2025-07-28 00:13:29',NULL),(395,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:29','2025-07-28 00:13:29',NULL),(396,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:29','2025-07-28 00:13:29',NULL),(397,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:29','2025-07-28 00:13:29',NULL),(398,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:29','2025-07-28 00:13:29',NULL),(399,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:13:59','2025-07-28 00:13:59',NULL),(400,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:14:01','2025-07-28 00:14:01',NULL),(401,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-28 00:14:02','2025-07-28 00:14:02',NULL),(402,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:14:04','2025-07-28 00:14:04',NULL),(403,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:14:05','2025-07-28 00:14:05',NULL),(404,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:14:08','2025-07-28 00:14:08',NULL),(405,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:14:09','2025-07-28 00:14:09',NULL),(406,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:14:12','2025-07-28 00:14:12',NULL),(407,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:14:14','2025-07-28 00:14:14',NULL),(408,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:14:16','2025-07-28 00:14:16',NULL),(409,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:14:17','2025-07-28 00:14:17',NULL),(410,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:14:17','2025-07-28 00:14:17',NULL),(411,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:14:17','2025-07-28 00:14:17',NULL),(412,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:15:05','2025-07-28 00:15:05',NULL),(413,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:15:06','2025-07-28 00:15:06',NULL),(414,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:15:14','2025-07-28 00:15:14',NULL),(415,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:15:15','2025-07-28 00:15:15',NULL),(416,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-28 00:15:19','2025-07-28 00:15:19',NULL),(417,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:15:21','2025-07-28 00:15:21',NULL),(418,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-28 00:15:22','2025-07-28 00:15:22',NULL),(419,1,'VIEW_EVENT','None','127.0.0.1','\"View event id 15 and associated permissions\"','2025-07-28 00:15:29','2025-07-28 00:15:29',NULL),(420,1,'VIEW_EVENTS','None','127.0.0.1','\"Get all events\"','2025-07-28 00:15:40','2025-07-28 00:15:40',NULL);
/*!40000 ALTER TABLE `activity_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `country` (
  `id` int NOT NULL AUTO_INCREMENT,
  `country` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `short_code` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `country` (`country`),
  UNIQUE KEY `short_code` (`short_code`),
  KEY `ix_country_country` (`country`),
  KEY `ix_country_short_code` (`short_code`),
  KEY `ix_country_deleted_at` (`country`,`deleted_at`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country`
--

LOCK TABLES `country` WRITE;
/*!40000 ALTER TABLE `country` DISABLE KEYS */;
INSERT INTO `country` VALUES (1,'Tanzania','TZ','2025-05-22 18:51:47','2025-07-27 18:17:49','2025-07-27 18:17:49'),(2,'Mauritius','MU','2025-06-06 07:29:10','2025-07-27 18:17:49','2025-07-27 18:17:49');
/*!40000 ALTER TABLE `country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `document`
--

DROP TABLE IF EXISTS `document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `document` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `document_type` varchar(255) NOT NULL,
  `file_type` varchar(200) NOT NULL,
  `file_name` text NOT NULL,
  `name` text NOT NULL,
  `path` text NOT NULL,
  `access_level` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_document_event` (`event_id`),
  KEY `ix_document` (`document_type`,`deleted_at`),
  CONSTRAINT `fk_document_event` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document`
--

LOCK TABLES `document` WRITE;
/*!40000 ALTER TABLE `document` DISABLE KEYS */;
INSERT INTO `document` VALUES (5,15,'ProgrammeBooklet','application/vnd.openxmlformats-officedocument.wordprocessingml.document','ECSA TLO modelling workshop (1).docx','Programme','uploads/event/documents/15_20250727184843_6c81fd19/ECSA TLO modelling workshop (1).docx','Public','2025-07-27 18:48:43','2025-07-27 18:48:43',NULL);
/*!40000 ALTER TABLE `document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `org_unit_id` int NOT NULL,
  `country_id` int NOT NULL,
  `event` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `theme` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `start_date` timestamp(6) NOT NULL,
  `end_date` timestamp(6) NOT NULL,
  `location` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `deleted_at` timestamp(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_event_user` (`user_id`),
  KEY `fk_event_org_unit` (`org_unit_id`),
  KEY `fk_event_country` (`country_id`),
  CONSTRAINT `fk_event_country` FOREIGN KEY (`country_id`) REFERENCES `country` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_event_org_unit` FOREIGN KEY (`org_unit_id`) REFERENCES `org_unit` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_event_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (15,1,22,2,'15ᵗʰ Best Practices Forum & 31ˢᵗ DJCC Meeting','Enhancing Health Systems for Equity, Resilience, and Sustainability','A platform where countries showcase tested innovations that have improved health outcomes. Abstracts, panel discussions, and best practice presentations are central.','2025-08-04 21:00:00.000000','2025-08-06 21:00:00.000000','Mauritius, Port Louis','2025-07-27 18:36:46.522190','2025-07-27 18:36:46.522190',NULL);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `link`
--

DROP TABLE IF EXISTS `link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `link` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `link` text NOT NULL,
  `name` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `event_id` (`event_id`),
  KEY `ix_document` (`link`(255),`deleted_at`),
  CONSTRAINT `link_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `link`
--

LOCK TABLES `link` WRITE;
/*!40000 ALTER TABLE `link` DISABLE KEYS */;
INSERT INTO `link` VALUES (1,15,'https://test.link.com/','Pictures','2025-07-27 18:49:08','2025-07-27 18:49:08',NULL);
/*!40000 ALTER TABLE `link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `org_unit`
--

DROP TABLE IF EXISTS `org_unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `org_unit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `type` enum('project','department','college','secretariat','other') NOT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `org_unit`
--

LOCK TABLES `org_unit` WRITE;
/*!40000 ALTER TABLE `org_unit` DISABLE KEYS */;
INSERT INTO `org_unit` VALUES (22,'ECSA-HC','secretariat','The East, Central and Southern Africa Health Community (ECSA-HC) is an intergovernmental regional health organization. It brings together countries in East, Central, and Southern Africa to collaborate on improving health systems and addressing shared health challenges.','2025-07-27 18:32:14','2025-07-27 18:32:14',NULL);
/*!40000 ALTER TABLE `org_unit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_reset`
--

DROP TABLE IF EXISTS `password_reset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_reset` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `reset_token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` timestamp NOT NULL,
  `is_used` tinyint(1) DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reset_token` (`reset_token`),
  KEY `ix_password_reset` (`deleted_at`),
  KEY `ix_password_reset_reset_token` (`reset_token`),
  KEY `fk_passwordreset_user` (`user_id`),
  CONSTRAINT `fk_passwordreset_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_reset`
--

LOCK TABLES `password_reset` WRITE;
/*!40000 ALTER TABLE `password_reset` DISABLE KEYS */;
INSERT INTO `password_reset` VALUES (1,1,'58440d78-e17a-44ea-8ee6-88f863f45484','2025-07-27 23:08:09',1,'2025-07-27 22:08:09','2025-07-27 22:51:01',NULL),(2,1,'c1cda6a1-0694-45b8-a5bb-296882943012','2025-07-27 20:55:17',1,'2025-07-27 22:55:17','2025-07-27 23:10:10',NULL),(3,1,'9b32b112-a814-424a-8766-8b6389b29f8f','2025-07-27 21:12:24',1,'2025-07-27 23:12:24','2025-07-27 23:12:43',NULL);
/*!40000 ALTER TABLE `password_reset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `registration_id` int NOT NULL,
  `payment_date` timestamp NOT NULL,
  `payment_method` enum('Cash','Mpesa','Bank_Transfer','Card') COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_reference` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_amount` decimal(10,2) NOT NULL,
  `payment_status` enum('Pending','Completed') COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_receipt` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_payment_id` (`id`),
  KEY `payment_registration_id_fkey` (`registration_id`),
  CONSTRAINT `payment_registration_id_fkey` FOREIGN KEY (`registration_id`) REFERENCES `registration` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `permission` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission_code` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `system_code` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `permission` (`permission`),
  UNIQUE KEY `permission_code` (`permission_code`),
  KEY `ix_permission` (`permission`,`deleted_at`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES (1,'Add User','ADD_USER','EVENTS_SPACE','2025-05-22 09:15:14','2025-05-22 09:15:14',NULL),(2,'View User','VIEW_USER','EVENTS_SPACE','2025-05-22 09:15:14','2025-05-22 09:15:14',NULL),(3,'Update User','UPDATE_USER','EVENTS_SPACE','2025-05-22 09:15:14','2025-05-22 09:15:14',NULL),(4,'Delete User','DELETE_USER','EVENTS_SPACE','2025-05-22 09:15:14','2025-05-22 09:15:14',NULL),(5,'View Roles','VIEW_ROLE','EVENTS_SPACE','2025-05-22 09:15:32','2025-05-22 09:15:32',NULL),(6,'Add Role','ADD_ROLE','EVENTS_SPACE','2025-05-22 09:15:32','2025-05-22 09:15:32',NULL),(7,'Update Role','UPDATE_ROLE','EVENTS_SPACE','2025-05-22 09:15:32','2025-05-22 09:15:32',NULL),(8,'Delete Role','DELETE_ROLE','EVENTS_SPACE','2025-05-22 09:15:32','2025-05-22 09:15:32',NULL),(9,'View Permission','VIEW_PERMISSION','EVENTS_SPACE','2025-05-22 09:15:48','2025-05-22 09:15:48',NULL),(10,'Add Permission','ADD_PERMISSION','EVENTS_SPACE','2025-05-22 09:15:48','2025-05-22 09:15:48',NULL),(11,'Update Permission','UPDATE_PERMISSION','EVENTS_SPACE','2025-05-22 09:15:48','2025-05-22 09:15:48',NULL),(12,'Delete Permission','DELETE_PERMISSION','EVENTS_SPACE','2025-05-22 09:15:48','2025-05-22 09:15:48',NULL),(13,'View Organisation Unit','VIEW_ORG_UNIT','EVENTS_SPACE','2025-05-22 11:37:07','2025-05-22 11:37:07',NULL),(14,'Add Organisation Unit','ADD_ORG_UNIT','EVENTS_SPACE','2025-05-22 11:37:07','2025-05-22 11:37:07',NULL),(15,'Update Organisation Unit','UPDATE_ORG_UNIT','EVENTS_SPACE','2025-05-22 11:37:07','2025-05-22 11:37:07',NULL),(16,'Delete Organisation Unit','DELETE_ORG_UNIT','EVENTS_SPACE','2025-05-22 11:37:07','2025-05-22 11:37:07',NULL),(17,'View Event','VIEW_EVENT','EVENTS_SPACE','2025-05-22 11:55:40','2025-05-22 11:55:40',NULL),(18,'Add Event','ADD_EVENT','EVENTS_SPACE','2025-05-22 11:55:40','2025-05-22 11:55:40',NULL),(19,'Update Event','UPDATE_EVENT','EVENTS_SPACE','2025-05-22 11:55:40','2025-05-22 11:55:40',NULL),(20,'Delete Event','DELETE_EVENT','EVENTS_SPACE','2025-05-22 11:55:40','2025-05-22 11:55:40',NULL),(21,'Admin Events Dashboard','ADMIN_DASHBOARD','EVENTS_SPACE','2025-07-27 15:24:33','2025-07-27 15:24:33',NULL);
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `event_id` int NOT NULL,
  `participation_role` enum('secretariat','delegate','speaker','sponsor','moderator','participant','student','exibitor','world','other_africa','member_state','moh') NOT NULL,
  `paid` tinyint(1) NOT NULL DEFAULT '0',
  `registered_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_event_registration` (`user_id`,`event_id`),
  KEY `fk_registration_event` (`event_id`),
  CONSTRAINT `fk_registration_event` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  CONSTRAINT `fk_registration_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration`
--

LOCK TABLES `registration` WRITE;
/*!40000 ALTER TABLE `registration` DISABLE KEYS */;
INSERT INTO `registration` VALUES (36,1,15,'secretariat',0,'2025-07-27 18:45:15','2025-07-27 18:45:15','2025-07-27 18:45:15',NULL);
/*!40000 ALTER TABLE `registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role` (`role`),
  KEY `ix_role` (`role`,`deleted_at`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'User','Default user role ','2025-05-22 09:23:47','2025-07-27 18:17:49','2025-07-27 18:17:49'),(2,'Administrator','Administrator','2025-05-22 09:38:31','2025-05-22 09:38:31',NULL);
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permission`
--

DROP TABLE IF EXISTS `role_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_id` int NOT NULL,
  `permission_id` int NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_id_permission_id` (`role_id`,`permission_id`),
  KEY `ix_role_permission` (`role_id`,`permission_id`,`deleted_at`),
  KEY `fk_rolepermission_permission` (`permission_id`),
  CONSTRAINT `fk_rolepermission_permission` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_rolepermission_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permission`
--

LOCK TABLES `role_permission` WRITE;
/*!40000 ALTER TABLE `role_permission` DISABLE KEYS */;
INSERT INTO `role_permission` VALUES (2,2,2,'2025-05-22 09:39:52','2025-05-22 09:39:52',NULL),(3,2,3,'2025-05-22 09:39:52','2025-05-22 09:39:52',NULL),(4,2,4,'2025-05-22 09:39:52','2025-05-22 09:39:52',NULL),(5,2,5,'2025-05-22 09:39:52','2025-05-22 09:39:52',NULL),(6,2,6,'2025-05-22 09:39:53','2025-05-22 09:39:53',NULL),(7,2,7,'2025-05-22 09:39:53','2025-05-22 09:39:53',NULL),(8,2,8,'2025-05-22 09:39:53','2025-05-22 09:39:53',NULL),(9,2,9,'2025-05-22 09:39:53','2025-05-22 09:39:53',NULL),(10,2,10,'2025-05-22 09:39:53','2025-05-22 09:39:53',NULL),(11,2,11,'2025-05-22 09:39:53','2025-05-22 09:39:53',NULL),(12,2,12,'2025-05-22 09:39:53','2025-05-22 09:39:53',NULL),(13,2,13,'2025-05-22 11:37:40','2025-05-22 11:37:40',NULL),(14,2,14,'2025-05-22 11:37:40','2025-05-22 11:37:40',NULL),(15,2,15,'2025-05-22 11:37:40','2025-05-22 11:37:40',NULL),(16,2,16,'2025-05-22 11:37:40','2025-05-22 11:37:40',NULL),(17,2,17,'2025-05-22 11:56:07','2025-05-22 11:56:07',NULL),(18,2,18,'2025-05-22 11:56:07','2025-05-22 11:56:07',NULL),(20,2,20,'2025-05-22 11:56:07','2025-05-22 11:56:07',NULL),(23,1,2,'2025-06-09 18:36:30','2025-06-09 18:36:30',NULL),(26,1,5,'2025-06-09 18:40:26','2025-06-09 18:40:26',NULL),(27,1,3,'2025-06-09 18:49:32','2025-06-09 18:49:32',NULL),(28,1,4,'2025-06-09 18:49:33','2025-06-09 18:49:33',NULL),(31,1,20,'2025-06-09 18:56:27','2025-06-09 18:56:27',NULL),(32,2,19,'2025-06-09 19:40:10','2025-06-09 19:40:10',NULL),(35,2,21,'2025-07-27 15:28:44','2025-07-27 15:28:44',NULL),(36,2,1,'2025-07-27 15:45:36','2025-07-27 15:45:36',NULL);
/*!40000 ALTER TABLE `role_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `lastname` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hashed_password` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `verified` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email` (`email`),
  KEY `ix_user` (`deleted_at`,`email`,`phone`,`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Joel','Kumwenda','+265984065368','jkumwenda@gmail.com','$2b$12$F0kmMYHMxb78HoFsF01pte.WAzcFO.ajoZFJQoSKm4cMXC5Cvn8F2',0,'2025-05-22 09:35:13','2025-07-27 23:12:43','2025-07-27 18:17:49'),(19,'Joel','Kumwenda','09840653613','jkumwewewewewenda@gmail.com','$2b$12$SVf9HsSobMSMuZaHIEBjtOW.9s31tjLkStI7zxH7Z2KE8liOXNg3e',0,'2025-07-28 00:04:44','2025-07-28 00:04:44',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_photo`
--

DROP TABLE IF EXISTS `user_photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_photo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `path` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_user_photo` (`user_id`,`deleted_at`),
  CONSTRAINT `fk_user_photo_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_photo`
--

LOCK TABLES `user_photo` WRITE;
/*!40000 ALTER TABLE `user_photo` DISABLE KEYS */;
INSERT INTO `user_photo` VALUES (6,1,'uploads/picture/profile_picture/1_20250727145849_93099cef/319fa92a543c3f84725b135f6817050a.jpeg','2025-07-27 14:58:49','2025-07-27 14:58:49',NULL);
/*!40000 ALTER TABLE `user_photo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile`
--

DROP TABLE IF EXISTS `user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_profile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `country_id` int NOT NULL,
  `title` varchar(10) NOT NULL,
  `middle_name` varchar(100) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `position` varchar(255) DEFAULT NULL,
  `organisation` varchar(255) NOT NULL,
  `profession` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_country` (`country_id`),
  KEY `ix_user_profile` (`user_id`,`deleted_at`),
  CONSTRAINT `fk_country` FOREIGN KEY (`country_id`) REFERENCES `country` (`id`),
  CONSTRAINT `fk_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile`
--

LOCK TABLES `user_profile` WRITE;
/*!40000 ALTER TABLE `user_profile` DISABLE KEYS */;
INSERT INTO `user_profile` VALUES (1,1,1,'Mr','','Male','2025-06-19 16:24:08','2025-07-27 18:46:54',NULL,'Position','ECSA-HC','Software Dev');
/*!40000 ALTER TABLE `user_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_role`
--

DROP TABLE IF EXISTS `user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `role_id` int NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_role_id` (`user_id`,`role_id`),
  KEY `ix_user_role` (`user_id`,`role_id`,`deleted_at`),
  KEY `fk_userrole_role` (`role_id`),
  CONSTRAINT `fk_userrole_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `fk_userrole_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_role`
--

LOCK TABLES `user_role` WRITE;
/*!40000 ALTER TABLE `user_role` DISABLE KEYS */;
INSERT INTO `user_role` VALUES (2,1,2,'2025-05-22 09:40:08','2025-05-22 09:40:08',NULL),(12,1,1,'2025-07-27 23:56:16','2025-07-27 23:56:16',NULL),(13,19,1,'2025-07-28 00:04:44','2025-07-28 00:04:44',NULL);
/*!40000 ALTER TABLE `user_role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-28  4:15:09
