-- MySQL dump 10.13  Distrib 8.3.0, for macos14.2 (arm64)
--
-- Host: rc1b-2xmunoaqhipsaggs.mdb.yandexcloud.net    Database: exam
-- ------------------------------------------------------
-- Server version	8.0.35-27

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'f303b099-fb54-11ee-9bef-d00de17a9904:1-5378118';

--
-- Table structure for table `book_covers`
--

DROP TABLE IF EXISTS `book_covers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_covers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) NOT NULL,
  `mime_type` varchar(255) NOT NULL,
  `md5_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_covers`
--

LOCK TABLES `book_covers` WRITE;
/*!40000 ALTER TABLE `book_covers` DISABLE KEYS */;
INSERT INTO `book_covers` VALUES (5,'img_2.png','image/png','0cc5e121c28b79cb4c200ee4bb8d012e'),(6,'master.webp','image/webp','8491ca6031c7ebeab13bd29d24b3d066'),(7,'master.webp','image/webp','8491ca6031c7ebeab13bd29d24b3d066'),(10,'onegin.webp','image/webp','2db3a6543279968968171f32939a584e'),(12,'onegin.webp','image/webp','2db3a6543279968968171f32939a584e'),(13,'onegin.webp','image/webp','2db3a6543279968968171f32939a584e');
/*!40000 ALTER TABLE `book_covers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_genres`
--

DROP TABLE IF EXISTS `book_genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_genres` (
  `book_id` int NOT NULL,
  `genre_id` int NOT NULL,
  PRIMARY KEY (`book_id`,`genre_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `book_genres_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `book_genres_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_genres`
--

LOCK TABLES `book_genres` WRITE;
/*!40000 ALTER TABLE `book_genres` DISABLE KEYS */;
INSERT INTO `book_genres` VALUES (17,1),(10,2),(12,2),(10,5),(12,5);
/*!40000 ALTER TABLE `book_genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `year` int NOT NULL,
  `publisher` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `pages` int NOT NULL,
  `cover_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cover_id` (`cover_id`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`cover_id`) REFERENCES `book_covers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (10,'1','1',2001,'1','1',1,5),(12,'Мастер и Маргарита','Роман «Мастер и Маргарита» – это, безусловно, главное произведение, классика ХХ века, Михаила Афанасьевича Булгакова. Автор работал над ним более десяти лет, вплоть до последних дней своей жизни. Только спустя четверть века эта великая книга пришла к читателю – поистине символическая судьба для русской литературы!\r\n\r\nВ начале преданный полному забвению, затем изданный в журнале и ставший полузапрещенным, роман активно распространялся в «самиздате» и, наконец, стал самым массовым культовым произведением современной России, включенным даже в школьную программу.\r\n\r\nВ самом современном сегодня формате аудиокниги вечный роман обретает новое звучание.',1967,'Издательство','Михаил Булгаков',99999,7),(17,'Евгений Онегин','Одно из самых значительных произведений русской литературы\r\n\r\n\"Евгений Онегин\" (1823-1831) – одно из самых значительных произведений русской литературы.\r\n\r\nПронзительная любовная история, драматические повороты сюжета, тонкий психологизм персонажей, детальное описание быта и нравов той эпохи (не случайно Белинский назвал роман «энциклопедией русской жизни») – в этом произведении, как в зеркале, отразилась вся русская жизнь. «Евгений Онегин» никогда не утратит своей актуальности, и даже спустя два века мы поражаемся точности и верности «ума холодных наблюдений и сердца горестных замет» великого русского поэта.',1823,'ООО \"Издательство «АСТ», 2022','Александр Пушкин',400,13);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (1,'Adventure'),(2,'Comedy'),(6,'Fantasy'),(5,'Horror'),(4,'Musical');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `book_id` int NOT NULL,
  `user_id` int NOT NULL,
  `rating` int NOT NULL,
  `text` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `book_id` (`book_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (8,17,1,5,'Очень хорошая книга. Советую все почитать, купить, иииииииииииииииииииииииииииииииии','2024-06-15 15:38:44');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin','Superuser with full access'),(2,'moderator','Can edit book data and moderate reviews'),(3,'user','Can leave reviews');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','admin_l','admin_f','admin_m',1),(2,'user','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','user','user','user',3),(3,'moderator','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','moderator','moderator','moderator',2);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-16 15:51:20
