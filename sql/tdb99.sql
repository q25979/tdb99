# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.6.43)
# Database: test
# Generation Time: 2019-07-14 05:51:46 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table admin_user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `admin_user`;

CREATE TABLE `admin_user` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` varchar(36) NOT NULL,
  `uid` varchar(32) NOT NULL,
  `password` varchar(256) NOT NULL,
  `role` smallint(6) NOT NULL,
  `locked` smallint(6) NOT NULL,
  `token` varchar(256) DEFAULT NULL,
  `permission` text,
  `parent_id` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `admin_user_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `admin_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `admin_user` WRITE;
/*!40000 ALTER TABLE `admin_user` DISABLE KEYS */;

INSERT INTO `admin_user` (`created_at`, `updated_at`, `id`, `uid`, `password`, `role`, `locked`, `token`, `permission`, `parent_id`)
VALUES
	('2019-07-14 13:24:57','2019-07-14 13:27:05','00000000-0000-0000-0000-000000000000','admin','pbkdf2:sha256:50000$isgYCksk$b699b4c75cb2d0f0d8e662ce8531e92f1c88ec0bb0335b82ace6203b52cb2ca3',1,0,'eyJhbGciOiJIUzI1NiIsImlhdCI6MTU2MzA4MjAyNSwiZXhwIjoxNTk0NjE4MDI1fQ.eyJpZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCJ9.V2SmaIFlrRf_wKuAJvTyMPNDCh--Yrr6l2aRDcE2hEU',NULL,NULL);

/*!40000 ALTER TABLE `admin_user` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table alembic_version
# ------------------------------------------------------------

DROP TABLE IF EXISTS `alembic_version`;

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;

INSERT INTO `alembic_version` (`version_num`)
VALUES
	('5caf53f195fa');

/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table assets
# ------------------------------------------------------------

DROP TABLE IF EXISTS `assets`;

CREATE TABLE `assets` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `total_balance` decimal(24,8) NOT NULL,
  `community_balance` decimal(24,8) NOT NULL,
  `transaction_balance` decimal(24,8) NOT NULL,
  `grand_total_balance` decimal(24,8) NOT NULL,
  `community_today_balance` decimal(24,8) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `assets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `assets` WRITE;
/*!40000 ALTER TABLE `assets` DISABLE KEYS */;

INSERT INTO `assets` (`created_at`, `updated_at`, `id`, `user_id`, `total_balance`, `community_balance`, `transaction_balance`, `grand_total_balance`, `community_today_balance`)
VALUES
	('2019-07-14 13:42:04','2019-07-14 13:42:04','904dd867-aafa-4553-83e8-ff25a353adcd','8725814f-ec9e-4987-8bc8-12d160592825',0.00000000,0.00000000,0.00000000,0.00000000,0.00000000),
	('2019-07-14 13:24:57','2019-07-14 13:40:58','b167f2fa-4490-4aae-8346-036c6d7fcc1e','00000000-0000-0000-0000-000000000000',10000.00000000,9500.00000000,10000.00000000,10000.00000000,0.00000000);

/*!40000 ALTER TABLE `assets` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table assets_balance_record
# ------------------------------------------------------------

DROP TABLE IF EXISTS `assets_balance_record`;

CREATE TABLE `assets_balance_record` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(36) NOT NULL,
  `current_amount` decimal(24,8) NOT NULL,
  `delta_amount` decimal(24,8) NOT NULL,
  `assets_type` smallint(6) NOT NULL,
  `record_type` int(11) NOT NULL,
  `details` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `assets_balance_record_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `assets_balance_record` WRITE;
/*!40000 ALTER TABLE `assets_balance_record` DISABLE KEYS */;

INSERT INTO `assets_balance_record` (`created_at`, `updated_at`, `id`, `user_id`, `current_amount`, `delta_amount`, `assets_type`, `record_type`, `details`)
VALUES
	('2019-07-14 13:29:13','2019-07-14 13:29:13',1,'00000000-0000-0000-0000-000000000000',10000.00000000,10000.00000000,1,2,'{\"message\": \"\\u7ba1\\u7406\\u5458\\uff1aadmin\"}'),
	('2019-07-14 13:29:22','2019-07-14 13:29:22',2,'00000000-0000-0000-0000-000000000000',10000.00000000,10000.00000000,2,2,'{\"message\": \"\\u7ba1\\u7406\\u5458\\uff1aadmin\"}'),
	('2019-07-14 13:29:34','2019-07-14 13:29:34',3,'00000000-0000-0000-0000-000000000000',10000.00000000,10000.00000000,4,2,'{\"message\": \"\\u7ba1\\u7406\\u5458\\uff1aadmin\"}'),
	('2019-07-14 13:40:58','2019-07-14 13:40:58',4,'00000000-0000-0000-0000-000000000000',9500.00000000,-500.00000000,2,8,'{\"message\": \"\\u6302\\u5355\\u51bb\\u7ed3\"}');

/*!40000 ALTER TABLE `assets_balance_record` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table buy_order
# ------------------------------------------------------------

DROP TABLE IF EXISTS `buy_order`;

CREATE TABLE `buy_order` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(36) NOT NULL,
  `side` smallint(6) NOT NULL,
  `number` varchar(16) NOT NULL,
  `amount` decimal(24,8) NOT NULL,
  `status` smallint(6) DEFAULT NULL,
  `details` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `buy_order_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `buy_order` WRITE;
/*!40000 ALTER TABLE `buy_order` DISABLE KEYS */;

INSERT INTO `buy_order` (`created_at`, `updated_at`, `id`, `user_id`, `side`, `number`, `amount`, `status`, `details`)
VALUES
	('2019-07-14 13:45:32','2019-07-14 13:45:32',1,'8725814f-ec9e-4987-8bc8-12d160592825',1,'1563083132555759',500.00000000,1,'{}');

/*!40000 ALTER TABLE `buy_order` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table captcha_pin_code
# ------------------------------------------------------------

DROP TABLE IF EXISTS `captcha_pin_code`;

CREATE TABLE `captcha_pin_code` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `pin_code_signature` varchar(256) NOT NULL,
  `try_times` smallint(6) DEFAULT NULL,
  `id` varchar(36) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table check_order_status_task
# ------------------------------------------------------------

DROP TABLE IF EXISTS `check_order_status_task`;

CREATE TABLE `check_order_status_task` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` smallint(6) DEFAULT NULL,
  `processed_at` datetime DEFAULT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `check_order_status_task_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table confirm_order
# ------------------------------------------------------------

DROP TABLE IF EXISTS `confirm_order`;

CREATE TABLE `confirm_order` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sell_user_id` varchar(36) NOT NULL,
  `buy_user_id` varchar(36) NOT NULL,
  `amount` decimal(24,8) NOT NULL,
  `status` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `buy_user_id` (`buy_user_id`),
  KEY `sell_user_id` (`sell_user_id`),
  CONSTRAINT `confirm_order_ibfk_1` FOREIGN KEY (`buy_user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `confirm_order_ibfk_2` FOREIGN KEY (`sell_user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table crypto_currency
# ------------------------------------------------------------

DROP TABLE IF EXISTS `crypto_currency`;

CREATE TABLE `crypto_currency` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `currency_code` varchar(20) NOT NULL,
  `erc20_token` smallint(6) NOT NULL,
  `usd_price` decimal(24,8) NOT NULL,
  `sequence` smallint(6) NOT NULL,
  `init_block_number` int(11) NOT NULL,
  `indexed_block_number` int(11) NOT NULL,
  `start_price` decimal(24,8) NOT NULL,
  `percent_change_1h` decimal(24,8) NOT NULL,
  `percent_change_24h` decimal(24,8) NOT NULL,
  `percent_change_7d` decimal(24,8) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `currency_code` (`currency_code`,`erc20_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `crypto_currency` WRITE;
/*!40000 ALTER TABLE `crypto_currency` DISABLE KEYS */;

INSERT INTO `crypto_currency` (`created_at`, `updated_at`, `id`, `currency_code`, `erc20_token`, `usd_price`, `sequence`, `init_block_number`, `indexed_block_number`, `start_price`, `percent_change_1h`, `percent_change_24h`, `percent_change_7d`)
VALUES
	('2019-07-14 13:24:57','2019-07-14 13:51:40',1,'BTC',0,11255.70537220,0,0,0,0.00000000,0.00000000,0.00000000,0.00000000),
	('2019-07-14 13:24:57','2019-07-14 13:51:40',2,'USDT',0,1.00092604,0,0,0,0.00000000,0.00000000,0.00000000,0.00000000),
	('2019-07-14 13:24:57','2019-07-14 13:51:40',3,'ETH',0,267.12616118,0,0,0,0.00000000,0.00000000,0.00000000,0.00000000),
	('2019-07-14 13:24:57','2019-07-14 13:51:40',4,'LTC',0,100.38417502,0,0,0,0.00000000,0.00000000,0.00000000,0.00000000),
	('2019-07-14 13:24:57','2019-07-14 13:51:40',5,'EOS',0,4.71833515,0,0,0,0.00000000,0.00000000,0.00000000,0.00000000),
	('2019-07-14 13:24:57','2019-07-14 13:51:41',6,'ETC',0,6.55134821,0,0,0,0.00000000,0.00000000,0.00000000,0.00000000),
	('2019-07-14 13:24:57','2019-07-14 13:51:41',7,'DASH',0,140.28753276,0,0,0,0.00000000,0.00000000,0.00000000,0.00000000),
	('2019-07-14 13:24:57','2019-07-14 13:51:40',8,'BSV',0,150.66914029,0,0,0,0.00000000,0.00000000,0.00000000,0.00000000),
	('2019-07-14 13:24:57','2019-07-14 13:51:40',9,'XRP',0,0.33041626,0,0,0,0.00000000,0.00000000,0.00000000,0.00000000),
	('2019-07-14 13:24:57','2019-07-14 13:51:41',10,'DOGE',0,0.00322088,0,0,0,0.00000000,0.00000000,0.00000000,0.00000000);

/*!40000 ALTER TABLE `crypto_currency` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table currency
# ------------------------------------------------------------

DROP TABLE IF EXISTS `currency`;

CREATE TABLE `currency` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usd_price` decimal(24,8) NOT NULL,
  `transaction_cnt` int(11) DEFAULT NULL,
  `today_transaction_amount` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `currency` WRITE;
/*!40000 ALTER TABLE `currency` DISABLE KEYS */;

INSERT INTO `currency` (`created_at`, `updated_at`, `id`, `usd_price`, `transaction_cnt`, `today_transaction_amount`)
VALUES
	('2019-07-14 13:24:57','2019-07-14 13:24:57',1,0.20000000,0,0);

/*!40000 ALTER TABLE `currency` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table currency_price_record
# ------------------------------------------------------------

DROP TABLE IF EXISTS `currency_price_record`;

CREATE TABLE `currency_price_record` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_price` decimal(24,8) NOT NULL,
  `delta_price` decimal(24,8) NOT NULL,
  `transaction_cnt` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `currency_price_record` WRITE;
/*!40000 ALTER TABLE `currency_price_record` DISABLE KEYS */;

INSERT INTO `currency_price_record` (`created_at`, `updated_at`, `id`, `current_price`, `delta_price`, `transaction_cnt`)
VALUES
	('2019-07-07 13:24:57','2019-07-14 13:24:57',1,0.20000000,0.00000000,0),
	('2019-07-08 13:24:57','2019-07-14 13:24:57',2,0.20000000,0.00000000,0),
	('2019-07-09 13:24:57','2019-07-14 13:24:57',3,0.20000000,0.00000000,0),
	('2019-07-10 13:24:57','2019-07-14 13:24:57',4,0.20000000,0.00000000,0),
	('2019-07-11 13:24:57','2019-07-14 13:24:57',5,0.20000000,0.00000000,0),
	('2019-07-12 13:24:57','2019-07-14 13:24:57',6,0.20000000,0.00000000,0),
	('2019-07-13 13:24:57','2019-07-14 13:24:57',7,0.20000000,0.00000000,0);

/*!40000 ALTER TABLE `currency_price_record` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table daily_schedule_task
# ------------------------------------------------------------

DROP TABLE IF EXISTS `daily_schedule_task`;

CREATE TABLE `daily_schedule_task` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` smallint(6) DEFAULT NULL,
  `processed_at` datetime DEFAULT NULL,
  `timestamp` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table email_pin_code
# ------------------------------------------------------------

DROP TABLE IF EXISTS `email_pin_code`;

CREATE TABLE `email_pin_code` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `pin_code_signature` varchar(256) NOT NULL,
  `try_times` smallint(6) DEFAULT NULL,
  `id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table fiat_currency
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fiat_currency`;

CREATE TABLE `fiat_currency` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country` varchar(60) NOT NULL,
  `country_code` varchar(20) NOT NULL,
  `currency` varchar(60) NOT NULL,
  `currency_code` varchar(20) NOT NULL,
  `usd_rate` decimal(24,8) NOT NULL,
  `sequence` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `country_code` (`country_code`,`currency_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `fiat_currency` WRITE;
/*!40000 ALTER TABLE `fiat_currency` DISABLE KEYS */;

INSERT INTO `fiat_currency` (`created_at`, `updated_at`, `id`, `country`, `country_code`, `currency`, `currency_code`, `usd_rate`, `sequence`)
VALUES
	('2019-07-14 13:24:57','2019-07-14 13:24:57',1,'中华人民共和国','CN','人民币元','CNY',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',2,'中国香港','HK','港元','HKD',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',3,'中国台湾','TW','台湾元','TWD',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',4,'英国','GB','英镑','GBP',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',5,'美国','US','美元','USD',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',6,'法国','FR','欧元','EUR',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',7,'德国','DE','欧元','EUR',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',8,'日本','JP','日元','JPY',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',9,'阿拉伯联合酋长国','AE','阿联酋 迪拉姆','AED',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',10,'泰国','TH','泰铢','THB',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',11,'俄罗斯','RU','俄罗斯卢布','RUB',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',12,'加拿大','CA','加拿大元','CAD',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',13,'韩国','KR','韩元','KRW',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',14,'马来西亚','MY','马来西亚林吉特','MYR',0.00000000,0),
	('2019-07-14 13:24:57','2019-07-14 13:24:57',15,'新加坡','SG','新加坡元','SGD',0.00000000,0);

/*!40000 ALTER TABLE `fiat_currency` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table login_info
# ------------------------------------------------------------

DROP TABLE IF EXISTS `login_info`;

CREATE TABLE `login_info` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `client_ip` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `login_info_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `login_info` WRITE;
/*!40000 ALTER TABLE `login_info` DISABLE KEYS */;

INSERT INTO `login_info` (`created_at`, `updated_at`, `id`, `user_id`, `client_ip`)
VALUES
	('2019-07-14 13:39:38','2019-07-14 13:39:38','81a65e6b-bfa2-4805-9fa7-84bfb3171810','00000000-0000-0000-0000-000000000000','127.0.0.1'),
	('2019-07-14 13:43:08','2019-07-14 13:43:08','f9b7ab86-c7f5-4f6e-b2f7-4c4ec4bbcdb6','8725814f-ec9e-4987-8bc8-12d160592825','127.0.0.1');

/*!40000 ALTER TABLE `login_info` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table match_order
# ------------------------------------------------------------

DROP TABLE IF EXISTS `match_order`;

CREATE TABLE `match_order` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sell_user_id` varchar(36) NOT NULL,
  `buy_user_id` varchar(36) NOT NULL,
  `sell_order_id` int(11) NOT NULL,
  `buy_order_id` int(11) NOT NULL,
  `sell_number` varchar(16) NOT NULL,
  `buy_number` varchar(16) NOT NULL,
  `payment_amount` decimal(24,8) NOT NULL,
  `payment_amount_usdt` decimal(24,8) NOT NULL,
  `proof_img` text,
  `current_price` decimal(24,8) NOT NULL,
  `payment_id` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `buy_number` (`buy_number`),
  UNIQUE KEY `sell_number` (`sell_number`),
  KEY `buy_order_id` (`buy_order_id`),
  KEY `buy_user_id` (`buy_user_id`),
  KEY `payment_id` (`payment_id`),
  KEY `sell_order_id` (`sell_order_id`),
  KEY `sell_user_id` (`sell_user_id`),
  CONSTRAINT `match_order_ibfk_1` FOREIGN KEY (`buy_order_id`) REFERENCES `order` (`id`),
  CONSTRAINT `match_order_ibfk_2` FOREIGN KEY (`buy_user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `match_order_ibfk_3` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`id`),
  CONSTRAINT `match_order_ibfk_4` FOREIGN KEY (`sell_order_id`) REFERENCES `order` (`id`),
  CONSTRAINT `match_order_ibfk_5` FOREIGN KEY (`sell_user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `match_order` WRITE;
/*!40000 ALTER TABLE `match_order` DISABLE KEYS */;

INSERT INTO `match_order` (`created_at`, `updated_at`, `id`, `sell_user_id`, `buy_user_id`, `sell_order_id`, `buy_order_id`, `sell_number`, `buy_number`, `payment_amount`, `payment_amount_usdt`, `proof_img`, `current_price`, `payment_id`)
VALUES
	('2019-07-14 13:47:48','2019-07-14 13:47:48',1,'00000000-0000-0000-0000-000000000000','8725814f-ec9e-4987-8bc8-12d160592825',1,2,'1563082825378559','1563083132555759',700.00000000,99.79856657,'[]',0.20000000,NULL);

/*!40000 ALTER TABLE `match_order` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table match_order_task
# ------------------------------------------------------------

DROP TABLE IF EXISTS `match_order_task`;

CREATE TABLE `match_order_task` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` smallint(6) DEFAULT NULL,
  `order_cnt` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `match_order_task` WRITE;
/*!40000 ALTER TABLE `match_order_task` DISABLE KEYS */;

INSERT INTO `match_order_task` (`created_at`, `updated_at`, `id`, `status`, `order_cnt`)
VALUES
	('2019-07-14 13:45:49','2019-07-14 13:47:43',1,1,2);

/*!40000 ALTER TABLE `match_order_task` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table news
# ------------------------------------------------------------

DROP TABLE IF EXISTS `news`;

CREATE TABLE `news` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `details` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table order
# ------------------------------------------------------------

DROP TABLE IF EXISTS `order`;

CREATE TABLE `order` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(36) NOT NULL,
  `number` varchar(16) NOT NULL,
  `amount` decimal(24,8) NOT NULL,
  `status` smallint(6) NOT NULL,
  `match_order_id` int(11) DEFAULT NULL,
  `priority` smallint(6) DEFAULT NULL,
  `side` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `side` (`side`,`number`),
  KEY `user_id` (`user_id`),
  KEY `match_order_id` (`match_order_id`),
  CONSTRAINT `order_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `order_ibfk_3` FOREIGN KEY (`match_order_id`) REFERENCES `match_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;

INSERT INTO `order` (`created_at`, `updated_at`, `id`, `user_id`, `number`, `amount`, `status`, `match_order_id`, `priority`, `side`)
VALUES
	('2019-07-14 13:40:26','2019-07-14 13:47:48',1,'00000000-0000-0000-0000-000000000000','1563082825378559',500.00000000,2,1,0,2),
	('2019-07-14 13:45:32','2019-07-14 13:47:48',2,'8725814f-ec9e-4987-8bc8-12d160592825','1563083132555759',500.00000000,2,1,0,1);

/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table order_old
# ------------------------------------------------------------

DROP TABLE IF EXISTS `order_old`;

CREATE TABLE `order_old` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(36) NOT NULL,
  `match_user_id` varchar(36) DEFAULT NULL,
  `number` varchar(16) NOT NULL,
  `amount` decimal(24,8) NOT NULL,
  `hold_amount` decimal(24,8) NOT NULL,
  `fee` decimal(24,8) NOT NULL,
  `status` smallint(6) NOT NULL,
  `payment_amount` decimal(24,8) NOT NULL,
  `match_at` datetime DEFAULT NULL,
  `proof_img` text,
  `current_price` decimal(24,8) NOT NULL,
  `payment_id` varchar(36) DEFAULT NULL,
  `details` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`),
  KEY `match_user_id` (`match_user_id`),
  KEY `payment_id` (`payment_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `order_old_ibfk_1` FOREIGN KEY (`match_user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `order_old_ibfk_2` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`id`),
  CONSTRAINT `order_old_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table payment
# ------------------------------------------------------------

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `bank` varchar(128) DEFAULT NULL,
  `card_number` varchar(64) DEFAULT NULL,
  `wechat` varchar(64) DEFAULT NULL,
  `alipay` varchar(64) DEFAULT NULL,
  `address` varchar(64) DEFAULT NULL,
  `alipay_image` varchar(512) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `remark` varchar(64) DEFAULT NULL,
  `type` smallint(6) NOT NULL,
  `wechat_image` varchar(512) DEFAULT NULL,
  `invalid` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table recommend_schedule_task
# ------------------------------------------------------------

DROP TABLE IF EXISTS `recommend_schedule_task`;

CREATE TABLE `recommend_schedule_task` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` smallint(6) DEFAULT NULL,
  `processed_at` datetime DEFAULT NULL,
  `user_id` varchar(36) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `recommend_schedule_task_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `recommend_schedule_task` WRITE;
/*!40000 ALTER TABLE `recommend_schedule_task` DISABLE KEYS */;

INSERT INTO `recommend_schedule_task` (`created_at`, `updated_at`, `id`, `status`, `processed_at`, `user_id`)
VALUES
	('2019-07-14 13:42:04','2019-07-14 13:42:04',1,0,NULL,'8725814f-ec9e-4987-8bc8-12d160592825');

/*!40000 ALTER TABLE `recommend_schedule_task` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table register_schedule_task
# ------------------------------------------------------------

DROP TABLE IF EXISTS `register_schedule_task`;

CREATE TABLE `register_schedule_task` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` smallint(6) DEFAULT NULL,
  `processed_at` datetime DEFAULT NULL,
  `user_id` varchar(36) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `register_schedule_task_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `register_schedule_task` WRITE;
/*!40000 ALTER TABLE `register_schedule_task` DISABLE KEYS */;

INSERT INTO `register_schedule_task` (`created_at`, `updated_at`, `id`, `status`, `processed_at`, `user_id`)
VALUES
	('2019-07-14 13:24:57','2019-07-14 13:24:57',1,0,NULL,'00000000-0000-0000-0000-000000000000'),
	('2019-07-14 13:42:04','2019-07-14 13:42:04',2,0,NULL,'8725814f-ec9e-4987-8bc8-12d160592825');

/*!40000 ALTER TABLE `register_schedule_task` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table sell_order
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sell_order`;

CREATE TABLE `sell_order` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(36) NOT NULL,
  `status` smallint(6) DEFAULT NULL,
  `details` varchar(255) DEFAULT NULL,
  `amount` decimal(24,8) NOT NULL,
  `number` varchar(16) NOT NULL,
  `side` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `sell_order_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `sell_order` WRITE;
/*!40000 ALTER TABLE `sell_order` DISABLE KEYS */;

INSERT INTO `sell_order` (`created_at`, `updated_at`, `id`, `user_id`, `status`, `details`, `amount`, `number`, `side`)
VALUES
	('2019-07-14 13:40:26','2019-07-14 13:40:58',1,'00000000-0000-0000-0000-000000000000',1,'{}',500.00000000,'1563082825378559',2);

/*!40000 ALTER TABLE `sell_order` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table setting
# ------------------------------------------------------------

DROP TABLE IF EXISTS `setting`;

CREATE TABLE `setting` (
  `name` varchar(50) NOT NULL,
  `value` text NOT NULL,
  `title` text NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `setting` WRITE;
/*!40000 ALTER TABLE `setting` DISABLE KEYS */;

INSERT INTO `setting` (`name`, `value`, `title`, `description`)
VALUES
	('general_option','{\"evaluation_reward_amount\": 200, \"lebo_price\": \"0.2\", \"lebo_change_price_cnt\": 2500, \"lebo_price_step\": \"0.001\", \"recommend_reward_amount\": [200, 150, 100, 50, 30, 25, 20, 15, 10, 5], \"transaction_allow_amount\": 3000, \"sell_amount\": 500, \"sell_people\": 500, \"buy_people\": 500, \"buy_count\": 3, \"sell_count\": 3, \"order_fee_rate\": \"0.0\", \"contact_us\": \"1234567890\", \"buy_sell_free_amount\": 100, \"buy_sell_rate\": \"0.03\", \"transaction_free_generation\": 3, \"transaction_free_amount\": 5, \"transaction_time_begin\": [\"09:00\", \"13:00\"], \"transaction_time_end\": [\"12:00\", \"18:00\"], \"exchange_amount_min\": 500, \"exchange_amount_max\": 5000, \"community_node_cnt\": [314, 400, 600], \"community_total_balance\": [100000, 200000, 300000], \"community_transaction_day_cnt\": 10, \"community_sponsor_cnt\": [10, 20, 30], \"community_line_cnt\": [2, 3, 4], \"community_line_people_cnt\": 100, \"qr_host\": \"http://qr.99lebo.com\", \"community_dividend_rate\": \"0.01\", \"community_transaction_fee_rate\": \"0.05\", \"community_free_amount\": 5, \"community_free_generation\": 10, \"order_status_change_time\": 2, \"match_order_cnt\": 0, \"dollar2rmb\": \"7.0\"}','常规选项','{\"evaluation_reward_amount\": \"\\u6d4b\\u8bc4\\u5956\\u52b1\\uff08\\u7f8e\\u5143\\uff09\", \"lebo_price\": \"\\u4e50\\u5b9d\\u521d\\u59cb\\u4ef7\\u683c\\uff08\\u7f8e\\u5143\\uff09\", \"lebo_change_price_cnt\": \"\\u4e50\\u5b9d\\u4ef7\\u683c\\u53d8\\u5316\\u7684\\u4ea4\\u6613\\u7b14\\u6570\\uff08\\u7b14\\uff09\", \"lebo_price_step\": \"\\u4e50\\u5b9d\\u4ef7\\u683c\\u53d8\\u5316\\u6b65\\u8fdb\\uff08\\u7f8e\\u5143\\uff09\", \"recommend_reward_amount\": \"\\u6bcf\\u4ee3\\u63a8\\u8350\\u4eba\\u83b7\\u5f97\\u5956\\u52b1\\uff08\\u4e2a\\uff09\", \"transaction_allow_amount\": \"\\u8fbe\\u5230\\u8be5\\u4e2a\\u6570\\u5141\\u8bb8\\u4ea4\\u6613\\uff08\\u4e2a\\uff09\", \"sell_amount\": \"\\u4e00\\u6b21\\u7684\\u5356\\u5355\\u6570\\u91cf\\uff08\\u4e2a\\uff09\", \"sell_people\": \"\\u4e00\\u5929\\u53ef\\u6302\\u5356\\u5355\\u4eba\\u6570\\uff08\\u4eba\\uff09\", \"buy_people\": \"\\u4e00\\u5929\\u53ef\\u6302\\u4e70\\u5355\\u4eba\\u6570\\uff08\\u4eba\\uff09\", \"buy_count\": \"\\u4e00\\u4eba\\u4e00\\u5929\\u6700\\u591a\\u7684\\u4e70\\u5165\\u5355\\u6570\\uff08\\u5355\\uff09\", \"sell_count\": \"\\u4e00\\u4eba\\u4e00\\u5929\\u6700\\u591a\\u7684\\u5356\\u51fa\\u5355\\u6570\\uff08\\u5355\\uff09\", \"order_fee_rate\": \"\\u8ba2\\u5355\\u624b\\u7eed\\u8d39\\u7387\", \"contact_us\": \"\\u8054\\u7cfb\\u6211\\u4eec\", \"buy_sell_free_amount\": \"\\u4e70\\u5356\\u5404\\u4e00\\u5355\\u65f6\\u91ca\\u653e\\u4e2a\\u6570\", \"buy_sell_rate\": \"\\u4e70\\u5356\\u5404\\u4e00\\u5355\\u65f6\\u7684\\u624b\\u7eed\\u8d39\\u7387\", \"transaction_free_generation\": \"\\u4ea4\\u6613\\u52a0\\u901f\\u91ca\\u653e\\u4ee3\\u6570\", \"transaction_free_amount\": \"\\u4ea4\\u6613\\u52a0\\u901f\\u91ca\\u653e\\u6570\\u91cf\", \"transaction_time_begin\": \"\\u4ea4\\u6613\\u5f00\\u59cb\\u65f6\\u95f4\", \"transaction_time_end\": \"\\u4ea4\\u6613\\u7ed3\\u675f\\u65f6\\u95f4\", \"exchange_amount_min\": \"\\u5151\\u6362\\u7684\\u6700\\u5c0f\\u6570\\u91cf\", \"exchange_amount_max\": \"\\u5151\\u6362\\u7684\\u6700\\u5927\\u6570\\u91cf\", \"community_node_cnt\": \"\\u793e\\u533a\\u8282\\u70b9\\u9636\\u6bb5\\u5bf9\\u5e94\\u6570\\u91cf\", \"community_total_balance\": \"\\u793e\\u533a\\u8282\\u70b9\\u9636\\u6bb5\\u5bf9\\u5e94\\u603b\\u8d44\\u4ea7\", \"community_transaction_day_cnt\": \"\\u793e\\u533a\\u8282\\u70b9\\u8fde\\u7eed\\u4ea4\\u6613\\u5929\\u6570\", \"community_sponsor_cnt\": \"\\u793e\\u533a\\u8282\\u70b9\\u9636\\u6bb5\\u5bf9\\u5e94\\u6240\\u9700\\u76f4\\u63a8\\u7528\\u6237\\u6570\", \"community_line_cnt\": \"\\u793e\\u533a\\u8282\\u70b9\\u9636\\u6bb5\\u5bf9\\u5e94\\u6240\\u9700\\u7ebf\\u6570\", \"community_line_people_cnt\": \"\\u793e\\u533a\\u8282\\u70b9\\u7ebf\\u5bf9\\u5e94\\u7528\\u6237\\u6570\", \"qr_host\": \"\\u63a8\\u8350\\u6ce8\\u518c\\u5730\\u5740\", \"community_dividend_rate\": \"\\u793e\\u533a\\u8282\\u70b9\\u5206\\u7ea2\\u6bd4\\u7387\", \"community_transaction_fee_rate\": \"\\u793e\\u533a\\u8282\\u70b9\\u8f6c\\u8d26\\u624b\\u7eed\\u8d39\", \"community_free_amount\": \"\\u793e\\u533a\\u8282\\u70b9\\u4ea4\\u6613\\u52a0\\u901f\\u91ca\\u653e\\u4e2a\\u6570\", \"community_free_generation\": \"\\u793e\\u533a\\u8282\\u70b9\\u4ea4\\u6613\\u52a0\\u901f\\u91ca\\u653e\\u4ee3\\u6570\", \"order_status_change_time\": \"\\u8ba2\\u5355\\u72b6\\u6001\\u53d8\\u5316\\u65f6\\u95f4(h)\", \"match_order_cnt\": \"\\u8ba2\\u5355\\u5339\\u914d\\u6570\\u91cf\", \"dollar2rmb\": \"\\u7f8e\\u5143\\u5151\\u4eba\\u6c11\\u5e01\\u6c47\\u7387\"}');

/*!40000 ALTER TABLE `setting` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table sms_pin_code
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sms_pin_code`;

CREATE TABLE `sms_pin_code` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `pin_code_signature` varchar(256) NOT NULL,
  `try_times` smallint(6) DEFAULT NULL,
  `id` varchar(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `id` varchar(36) NOT NULL,
  `uid` varchar(32) DEFAULT NULL,
  `country_code` varchar(16) DEFAULT NULL,
  `mobile` varchar(16) DEFAULT NULL,
  `login_email` varchar(100) DEFAULT NULL,
  `password` varchar(256) NOT NULL,
  `security_password` varchar(256) DEFAULT NULL,
  `token` varchar(256) DEFAULT NULL,
  `source` varchar(64) DEFAULT NULL,
  `locked` smallint(6) DEFAULT NULL,
  `avatar` varchar(512) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `gender` smallint(6) DEFAULT NULL,
  `sponsor_id` varchar(36) DEFAULT NULL,
  `active` smallint(6) DEFAULT NULL,
  `left_id` int(11) DEFAULT NULL,
  `right_id` int(11) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `allow_transaction` int(11) DEFAULT NULL,
  `wechat` varchar(64) DEFAULT NULL,
  `nickname` varchar(64) DEFAULT NULL,
  `transaction_level` int(11) DEFAULT NULL,
  `buy_order_cnt` int(11) DEFAULT NULL,
  `continuous_buy_cnt` int(11) DEFAULT NULL,
  `is_community_node` smallint(6) DEFAULT NULL,
  `today_have_transaction` smallint(6) DEFAULT NULL,
  `team_qualified_cnt` int(11) DEFAULT NULL,
  `order_mobile` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login_email` (`login_email`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `uid` (`uid`),
  KEY `sponsor_id` (`sponsor_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`sponsor_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;

INSERT INTO `user` (`created_at`, `updated_at`, `id`, `uid`, `country_code`, `mobile`, `login_email`, `password`, `security_password`, `token`, `source`, `locked`, `avatar`, `name`, `gender`, `sponsor_id`, `active`, `left_id`, `right_id`, `state`, `allow_transaction`, `wechat`, `nickname`, `transaction_level`, `buy_order_cnt`, `continuous_buy_cnt`, `is_community_node`, `today_have_transaction`, `team_qualified_cnt`, `order_mobile`)
VALUES
	('2019-07-14 13:24:57','2019-07-14 13:39:38','00000000-0000-0000-0000-000000000000','root',NULL,'13288888888',NULL,'pbkdf2:sha256:50000$e3jMXbdK$83d8361de7f27e9afbe1a3bc8b92065c3272030a1711558344df1acdb8cf6830','pbkdf2:sha256:50000$1x4XxZ4q$016e58aa39e537595cfa80ef6d28fb1bf0653cd60787eef0e8a9c4ce06e5b69f','eyJhbGciOiJIUzI1NiIsImlhdCI6MTU2MzA4Mjc3OCwiZXhwIjoxNTYzNTE0Nzc4fQ.eyJpZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCJ9.rO4eTTGoBPGlQNxKmVGbujqgjLDwgEY9m9YT-GFGnrg','',0,NULL,NULL,0,NULL,1,1,2,1,1,NULL,NULL,2,0,0,0,0,0,NULL),
	('2019-07-14 13:42:04','2019-07-14 13:45:11','8725814f-ec9e-4987-8bc8-12d160592825','xgb564282','','13750097201',NULL,'pbkdf2:sha256:50000$59Pcf3w1$152cfe6583f109a2efd9b7a986e513bbd70ad9bd368980cd3d2aa076fb1e8f86','pbkdf2:sha256:50000$ePq6HIix$aefe04aa1a88ddceba20bfcfbc2aac0e7373034246da3d9692865dd2b02940cb','eyJhbGciOiJIUzI1NiIsImlhdCI6MTU2MzA4Mjk4NywiZXhwIjoxNTYzNTE0OTg3fQ.eyJpZCI6Ijg3MjU4MTRmLWVjOWUtNDk4Ny04YmM4LTEyZDE2MDU5MjgyNSJ9.jvhSqy8qdRNQcgB7IBwTuIBwNzZOLbx5PrWWRZHC_yg','',0,NULL,NULL,0,'00000000-0000-0000-0000-000000000000',1,0,0,2,1,NULL,NULL,2,0,0,0,0,0,NULL);

/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
