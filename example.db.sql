BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `monitor` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`negitive`	VARCHAR ( 5 ),
	`posivtive`	VARCHAR ( 5 ),
	`chat_id`	INTEGER,
	FOREIGN KEY(`chat_id`) REFERENCES `chats`(`messege_id`)
);
CREATE TABLE IF NOT EXISTS `data_table` (
	`index`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`first_name`	VARCHAR ( 256 ),
	`last_name`	VARCHAR ( 256 ),
	`email`	VARCHAR ( 75 ),
	`phone`	INT ( 10 ),
	`username`	VARCHAR ( 25 ),
	`password`	VARCHAR ( 16 ),
	`role`	INTEGER DEFAULT 1
);
INSERT INTO `data_table` VALUES (1,'Vivek','Murali','007jetfire@gmail.com',7022169336,'Redalert','$2b$12$GFQAx9271FJCgaGlaQg.YOdDgshKNiMwf4RTfw2kynah.OUtO6oYS',1);
CREATE TABLE IF NOT EXISTS `chats` (
	`messege_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`messege`	TEXT,
	`username`	TEXT
);
INSERT INTO `chats` VALUES (4,'Collection updates through tweets ','Redalert');
INSERT INTO `chats` VALUES (5,'Collection updates through tweets ','Redalert');
INSERT INTO `chats` VALUES (6,'Collection updates through tweets ','Redalert');
INSERT INTO `chats` VALUES (7,'Collection updates through tweets ','Redalert');
INSERT INTO `chats` VALUES (8,'Collection updates through tweets ','Redalert');
INSERT INTO `chats` VALUES (9,'Collection updates through tweets ','Redalert');
INSERT INTO `chats` VALUES (10,'Collection updates through tweets ','Redalert');
INSERT INTO `chats` VALUES (11,'Collection updates through tweets ','Redalert');
INSERT INTO `chats` VALUES (12,'Collection updates through tweets ','Redalert');
INSERT INTO `chats` VALUES (13,'testing out without old html........','Redalert');
INSERT INTO `chats` VALUES (14,'tweets about football','Redalert');
CREATE INDEX IF NOT EXISTS `ix_data_table_index` ON `data_table` (
	`index`
);
COMMIT;
