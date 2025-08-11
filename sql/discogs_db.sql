-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: localhost    Database: discogs_db
-- ------------------------------------------------------
-- Server version	8.0.29-0ubuntu0.20.04.3

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
-- Table structure for table `RecordItem`
--

DROP TABLE IF EXISTS `RecordItem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RecordItem` (
  `row_id` int NOT NULL AUTO_INCREMENT,
  `release_id` int NOT NULL,
  `item_id` bigint NOT NULL,
  `available` tinyint DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `adjusted_price` decimal(8,2) DEFAULT NULL,
  `media_condition` varchar(50) DEFAULT NULL,
  `sleeve_condition` varchar(50) DEFAULT NULL,
  `details` varchar(1000) DEFAULT NULL,
  `avg_rating` decimal(4,1) DEFAULT NULL,
  `num_ratings` int DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`row_id`)
) ENGINE=InnoDB AUTO_INCREMENT=606 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RecordItem`
--

LOCK TABLES `RecordItem` WRITE;
/*!40000 ALTER TABLE `RecordItem` DISABLE KEYS */;
INSERT INTO `RecordItem` VALUES (581,7771,1874319559,0,'https://www.discogs.com/sell/item/1874319559',14.81,'Very Good (VG)','Good Plus (G+)','SLEEVE HAS SOME SIGNS OF AGE AND STICKER DAMAGE. RECORD HAS SOME LIGHT SURFACE SCRATCHES',100.0,36,'United Kingdom','2022-05-07 09:25:43',NULL),(582,7771,1845862036,1,'https://www.discogs.com/sell/item/1845862036',24.00,'Very Good (VG)','Very Good (VG)','Vinyl has some light scuffs. Cover has wear and spine wear. Original inner sleeve',99.8,1772,'United States','2022-05-07 09:25:44',NULL),(583,7771,1896000116,1,'https://www.discogs.com/sell/item/1896000116',64.93,'Very Good Plus (VG+)','Very Good Plus (VG+)','Record has hairline surface marks and plays perfectly. Cover has minimal shelfwear. Picture inner sleeve included. Buy with confidence from a trusted and honest seller. Low priced, quick worldwide delivery.',99.9,22520,'United Kingdom','2022-05-07 09:25:44',NULL),(584,7771,1693606999,1,'https://www.discogs.com/sell/item/1693606999',45.78,'Very Good Plus (VG+)','Very Good (VG)','no OBI, with BOOKLET...sleeve: foxing',100.0,34819,'Germany','2022-05-07 09:25:44',NULL),(585,7771,1797475003,1,'https://www.discogs.com/sell/item/1797475003',51.04,'Very Good Plus (VG+)','Very Good (VG)','No OBI, with BOOKLET (foxing). Vinyl professionally washed with Gläss Vinyl Cleaner Pro and playgraded; plays solid EX. Sleeve has hardly any wear/ringwear, but is quite foxed.',100.0,34819,'Germany','2022-05-07 09:25:44',NULL),(586,7771,1607561269,1,'https://www.discogs.com/sell/item/1607561269',34.97,'Very Good (VG)','Good Plus (G+)','Media- some light scratches and scuffs, some surface noise. Sleeve- staining and creases on front cover, one inch split in spine, small tear top right corner, printed inner sleeve included.',100.0,29,'Canada','2022-05-07 09:25:44',NULL),(587,7771,587604441,1,'https://www.discogs.com/sell/item/587604441',77.78,'Near Mint (NM or M-)','Near Mint (NM or M-)','ASK FOR AVAILABILITY * IN SHRINK * FEEL FREE TO ASK FOR YOUR DISCOUNT',98.6,444,'Mexico','2022-05-07 09:25:44',NULL),(588,7771,1664913940,1,'https://www.discogs.com/sell/item/1664913940',47.50,'Near Mint (NM or M-)','Very Good Plus (VG+)','Vinyl is NM, light sleeve mark and light crackle towards beginning first song side A, no other playback issues. Tested!! Very Nice!! Original Inner sleeve is NM, little mark, Original Cover is VG+++, light wear. Very Nice!! No 501 on back of cover, but sa',100.0,58,'United States','2022-05-07 09:25:45',NULL),(589,7771,1850269426,1,'https://www.discogs.com/sell/item/1850269426',43.99,'Very Good Plus (VG+)','Very Good Plus (VG+)','Record has some creases and light marks, play is solid VG+, light surface noise present in between songs. Jacket is in excellent condition (EX), printed inner sleeve included also in great condition.',100.0,95,'Canada','2022-05-07 09:25:45',NULL),(590,7771,1963117748,1,'https://www.discogs.com/sell/item/1963117748',28.99,'Very Good Plus (VG+)','Very Good (VG)','Purple translucent vinyl, cover has light staining/discolor in areas, still is nice and intact, printed inner included.',100.0,1923,'United States','2022-05-07 09:25:45',NULL),(591,7771,1855539952,1,'https://www.discogs.com/sell/item/1855539952',36.65,'Very Good Plus (VG+)','Very Good Plus (VG+)','',100.0,48,'Germany','2022-05-07 09:25:45',NULL),(592,7771,1922456300,1,'https://www.discogs.com/sell/item/1922456300',48.43,'Near Mint (NM or M-)','Very Good Plus (VG+)','EX RECORD, FEW FAINT SCUFFS, OIS LIGHT COVERWEAR',100.0,2490,'Denmark','2022-05-07 09:25:45',NULL),(593,7771,1907299187,1,'https://www.discogs.com/sell/item/1907299187',22.99,'Very Good (VG)','Very Good (VG)','LP is a strong VG with some light marks, but has great luster and plays more VG+ than not. OG inner sleeve included. Outer Sleeve is VG with general wear, some subtle staining and two old price stickers on the front.',100.0,9104,'United States','2022-05-07 09:25:45',NULL),(594,7771,1938552221,1,'https://www.discogs.com/sell/item/1938552221',33.99,'Very Good Plus (VG+)','Very Good Plus (VG+)','LP is VG++ and looks great! OG inner sleeve included. Outer sleeve is VG+ with light wear. CLASSIC JAMZZZ',100.0,9104,'United States','2022-05-07 09:25:46',NULL),(595,7771,1657703710,1,'https://www.discogs.com/sell/item/1657703710',76.73,'Very Good Plus (VG+)','Very Good Plus (VG+)','COMES WITH ORIGINAL 1983 RUSH SIGNALS TOUR BOOK! in great condition with a few superficial scuffs. WITH printed inner sleeve. I have much more Rush/rock/prog for sale!',99.8,4438,'Netherlands','2022-05-07 09:25:46',NULL),(596,7771,411617680,1,'https://www.discogs.com/sell/item/411617680',33.68,'Near Mint (NM or M-)','Very Good Plus (VG+)','small sticker at corner',99.6,2106,'Spain','2022-05-07 09:25:47',NULL),(597,7771,1723292452,1,'https://www.discogs.com/sell/item/1723292452',66.67,'Very Good (VG)','Very Good Plus (VG+)','Sort after pressing..this vinyl has signs of play but is clean and bright. Original labels and inner, no letter from record company, master disk on run out.',100.0,561,'United Kingdom','2022-05-07 09:25:47',NULL),(598,7771,1738198930,1,'https://www.discogs.com/sell/item/1738198930',21.05,'Very Good (VG)','Very Good Plus (VG+)','With Printed Inner Sleeve',100.0,1426,'Germany','2022-05-07 09:25:47',NULL),(599,7771,1952187608,1,'https://www.discogs.com/sell/item/1952187608',12.50,'Very Good (VG)','Very Good Plus (VG+)','small edge warp on vinyl causes a light woosh on intros to first song on both sidees. Sleeve has a small stain on spine edge, light bends in open edge, og inner excellent, sleeve in anti-static inner. #2',99.6,268,'United States','2022-05-07 09:25:48',NULL),(600,7771,1960943576,0,'https://www.discogs.com/sell/item/1960943576',13.68,'Very Good Plus (VG+)','Very Good Plus (VG+)','',96.3,27,'Italy','2022-05-07 09:25:48',NULL),(601,7771,1771006468,1,'https://www.discogs.com/sell/item/1771006468',44.99,'Very Good Plus (VG+)','Very Good Plus (VG+)','Pretty clean all around. Some age and shelf wear. $5 unlimited US shipping',99.7,12561,'United States','2022-05-07 09:25:48',NULL),(602,7771,1880375203,1,'https://www.discogs.com/sell/item/1880375203',56.70,'Very Good Plus (VG+)','Very Good Plus (VG+)','top copy, minor wear',99.8,14986,'United Kingdom','2022-05-07 09:25:48',NULL),(603,7771,1919753639,1,'https://www.discogs.com/sell/item/1919753639',25.00,'Very Good Plus (VG+)','Very Good (VG)','Strong VG Sleeve has corner dings, ring rub and some dings and faint staining along opening and bottom seam. Includes VG+ original printed inner sleeve.',100.0,11536,'United States','2022-05-07 09:25:48',NULL),(604,7771,1916886521,1,'https://www.discogs.com/sell/item/1916886521',23.50,'Very Good (VG)','Very Good (VG)','',100.0,2,'United States','2022-05-07 09:25:48',NULL),(605,7771,1959145955,1,'https://www.discogs.com/sell/item/1959145955',24.99,'Very Good Plus (VG+)','Very Good Plus (VG+)','',100.0,825,'United States','2022-05-07 09:25:49',NULL);
/*!40000 ALTER TABLE `RecordItem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `WatchList`
--

DROP TABLE IF EXISTS `WatchList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `WatchList` (
  `row_id` int NOT NULL AUTO_INCREMENT,
  `master_id` int NOT NULL,
  `master_url` varchar(200) DEFAULT NULL,
  `artist` varchar(100) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `formats` varchar(100) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `country` varchar(200) DEFAULT NULL,
  `desired_price` decimal(8,2) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_updated` datetime DEFAULT NULL,
  `date_scraped` datetime DEFAULT NULL,
  PRIMARY KEY (`row_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `WatchList`
--

LOCK TABLES `WatchList` WRITE;
/*!40000 ALTER TABLE `WatchList` DISABLE KEYS */;
/*!40000 ALTER TABLE `WatchList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token`
--

DROP TABLE IF EXISTS `token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token` (
  `token` varchar(40) DEFAULT NULL,
  `token_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token`
--

LOCK TABLES `token` WRITE;
/*!40000 ALTER TABLE `token` DISABLE KEYS */;
INSERT INTO `token` VALUES ('fqWyaZkdhwcPUoKeAdHaROvEutibOjNqHkBgNNlV','2022-05-05 15:21:57');
/*!40000 ALTER TABLE `token` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

CREATE TABLE `ScrapeQueue` (
  `row_id` int NOT NULL AUTO_INCREMENT,
  `batch_id` int NOT NULL,
  `master_id` int NOT NULL,
  status varchar(20),
  `date_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`row_id`)
);


-- Dump completed on 2022-05-08 22:43:21
