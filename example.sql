BEGIN TRANSACTION;
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
INSERT INTO `data_table` VALUES (1,'Vivek','Murali','007jetfire@gmail.com',7022169336,'Redalert','$2b$12$LHMRxMCJs6V7hbXrDboEZeont93rnCd8VvOhzBqHJDKmhNZm1a45S',1);
CREATE INDEX IF NOT EXISTS `ix_data_table_index` ON `data_table` (
	`index`
);
COMMIT;
