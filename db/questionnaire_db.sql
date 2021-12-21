-- MySQL dump 10.13  Distrib 8.0.11, for Win64 (x86_64)
--
-- Host: localhost    Database: questionnaire
-- ------------------------------------------------------
-- Server version	8.0.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `answer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `value` varchar(1024) NOT NULL,
  `prepared` tinyint(1) NOT NULL,
  `count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `answer_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer`
--

LOCK TABLES `answer` WRITE;
/*!40000 ALTER TABLE `answer` DISABLE KEYS */;
INSERT INTO `answer` VALUES (39,0,'Вариант ответа 1 для вопроса 1',1,0),(40,0,'Вариант ответа 2 для вопроса 1',1,0),(41,0,'Вариант ответа 1 для вопроса 2',1,0),(42,0,'Ответ в виде текста (вариант 1), вопрос 3',1,0),(43,0,'Вариант ответа 1 для вопроса 3',1,0),(44,0,'я пипиастр',1,0),(45,0,'ты тоже пипидастр',1,0),(46,0,'Опишите себя как фурри-фаша:',1,0),(47,0,'нинада',1,0),(48,0,'да',1,0),(49,0,'нет',1,0),(50,0,'За Путина',1,0),(51,0,'Да',1,0),(52,0,'Конечно',1,0),(53,0,'Без вариантов',1,0),(54,0,'ответ',1,0),(55,0,'нинада',1,0),(56,42,'Варианта ответа 1 вопроса 1 теста 1',1,1),(57,43,'Вариант ответа 1 вопроса 2 теста 1 ',1,1),(58,43,'Вариант ответа 2 вопроса 2 теста 1',1,0),(59,43,'Вариант ответа 2 вопроса 2 теста 1',1,0),(60,43,'Вариант ответа 3 вопроса 2 теста 1',1,0),(61,43,'Вариант ответа 4 вопроса 2 теста 1',1,0),(62,44,'Вариант ответа 1 вопроса  3 теста 1',1,0),(63,44,'Вариант ответа 2 вопроса  3 теста 1',1,1),(64,44,'Вариант ответа 3 вопроса  3 теста 1',1,1),(65,44,'Вариант ответа 4 вопроса  3 теста 1',1,0),(66,44,'Вариант ответа 5 вопроса  3 теста 1',1,1),(67,42,'ну да я сделал тест, класс, текстовый ответ',0,0);
/*!40000 ALTER TABLE `answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `test_id` int(11) NOT NULL,
  `title` varchar(64) NOT NULL,
  `text` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `test_id` (`test_id`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `type` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `question_ibfk_2` FOREIGN KEY (`test_id`) REFERENCES `test` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (30,1,7,'Заголовок вопроса 1','Текст вопроса 1'),(31,1,7,'Заголовок вопроса 2','Текст вопроса 2'),(32,3,7,'Заголовок вопроса 3','Никакого текста вопроса не будет'),(33,2,7,'Еще один вопрос (4)',NULL),(34,1,8,'Тестовый вопрос','Да будет так или не так'),(35,3,8,'Ты фурри-фаш?',NULL),(36,2,9,'Я странный','авпвыап выап ывало пр Доаб даба даб'),(37,1,10,'Да или нет?',NULL),(38,2,11,'За Путина?',NULL),(39,1,12,'Тест','Не хочу писать текст'),(40,3,19,'Тестовый вопрос',NULL),(41,3,20,'Вопрос 1 теста 1','Текста вопроса 1 теста 1'),(42,3,22,'Вопрос 1 теста 1','Текста вопроса 1 теста 1'),(43,1,22,'Вопрос 2 теста 1','Текст вопроса 2 теста 1'),(44,2,22,'Вопрос 3 теста 1',NULL);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `result`
--

DROP TABLE IF EXISTS `result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `result` (
  `answer_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  KEY `answer_id` (`answer_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `result_ibfk_1` FOREIGN KEY (`answer_id`) REFERENCES `answer` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `result_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result`
--

LOCK TABLES `result` WRITE;
/*!40000 ALTER TABLE `result` DISABLE KEYS */;
INSERT INTO `result` VALUES (67,18),(57,18),(58,18),(59,18),(60,18),(61,18),(62,18),(63,18),(64,18),(65,18);
/*!40000 ALTER TABLE `result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `author_id` int(11) NOT NULL,
  `creation_date` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `test_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES (7,'Тест1',12,'2021-11-22'),(8,'Ещё один тест',12,'2021-11-23'),(9,'Бляб я тесты создаю АаааАА',13,'2021-11-23'),(10,'Насколько процентов Вы фурри-фаш?',14,'2021-11-23'),(11,'Голосование за Путина',15,'2021-11-23'),(12,'Новый тест',16,'2021-11-23'),(19,'Ещё один новый тест',16,'2021-11-23'),(20,'Тест 1',17,'2021-12-21'),(22,'Тест 1 (новый)',17,'2021-12-21');
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type`
--

DROP TABLE IF EXISTS `type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `min_variants` tinyint(3) unsigned NOT NULL,
  `max_variants` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type`
--

LOCK TABLES `type` WRITE;
/*!40000 ALTER TABLE `type` DISABLE KEYS */;
INSERT INTO `type` VALUES (1,'Выбор одного варианта',2,16),(2,'Выбор нескольких вариантов',1,16),(3,'Ответ в виде текста',1,1);
/*!40000 ALTER TABLE `type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `sex` char(3) NOT NULL,
  `date_of_birth` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (12,'Автор1','МУЖ','2021-12-11'),(13,'ёБи4','МУЖ','1488-12-22'),(14,'stalker_','МУЖ','1986-04-26'),(15,'Путин В.В.','МУЖ','1952-10-07'),(16,'vika','ЖЕН','2001-10-08'),(17,'аноним1','МУЖ','2004-01-01'),(18,'test_respondent','Mal','2000-11-11');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-21 15:38:24
