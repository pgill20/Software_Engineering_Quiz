--
-- Table structure for table `Participants`
--
DROP TABLE IF EXISTS `Participants`;
CREATE TABLE `Participants` (
  `participant_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
	PRIMARY KEY (`participant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
--
-- Populating data for the table `Players`
--
INSERT INTO `Participants` (`first_name`, `last_name`, `password`) VALUES
('Lebron', 'James', 'dunking'),
('Stephen', 'Curry', 'shooting');