# ************************************************************
# Sequel Pro SQL dump
# Version 3408
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.15)
# Database: poll
# Generation Time: 2013-01-16 09:53:06 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table ban
# ------------------------------------------------------------



# Dump of table group
# ------------------------------------------------------------

LOCK TABLES `group` WRITE;
/*!40000 ALTER TABLE `group` DISABLE KEYS */;

INSERT INTO `group` (`id`, `name`)
VALUES
	(1,'平台'),
	(2,'算法'),
	(3,'读书'),
	(4,'音乐'),
	(5,'电影'),
	(6,'社区'),
	(7,'公共技术'),
	(8,'同城'),
	(9,'商务'),
	(10,'安全'),
	(11,'移动'),
	(12,'阿尔法城'),
	(13,'广告平台'),
	(14,'前端'),
	(15,'内网'),
	(16,'数据分析');

/*!40000 ALTER TABLE `group` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table subject
# ------------------------------------------------------------

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;

INSERT INTO `subject` (`id`, `topic`, `deadline`, `creator`, `votetype`, `group`)
VALUES
	(1,'test','2013-01-11','pengzhefu',1,1),
	(2,'alive','2013-01-31','pengzhefu',0,1);

/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table vote
# ------------------------------------------------------------

LOCK TABLES `vote` WRITE;
/*!40000 ALTER TABLE `vote` DISABLE KEYS */;

INSERT INTO `vote` (`id`, `content`, `count`, `sid`)
VALUES
	(1,'a',0,1),
	(2,'b',0,1),
	(3,'c',0,1),
	(4,'c1',0,1),
	(5,'wow',2,2),
	(6,'iphone',0,2);

/*!40000 ALTER TABLE `vote` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
