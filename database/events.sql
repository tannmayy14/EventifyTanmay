USE Eventify;


-- --------------------------------------------------------------------------------------------------------

CREATE TABLE `event_type` (
  `type_id` int(10) NOT NULL,
  `type_title` text NOT NULL
);

ALTER TABLE `event_type`
  ADD PRIMARY KEY (`type_id`);

ALTER TABLE `event_type`
  MODIFY `type_id` int(10) NOT NULL AUTO_INCREMENT;

INSERT INTO `event_type` (`type_id`, `type_title`) VALUES
(1, 'MOSAIC'),
(2, 'IRIS'),
(3, 'IGNITRA'),
(4, 'ASSOCIATIONS'),
(5, 'HACKATHONS'),
(6, 'DEPARTMENT');

-- -----------------------------------------------------------------------------------------------------

CREATE TABLE `location`(
  `location_id` int(10) NOT NULL,
  `location_name` varchar(100) NOT NULL
);

ALTER TABLE `location`
  ADD PRIMARY KEY (`location_id`);

ALTER TABLE `location`
  MODIFY `location_id` int(10) NOT NULL AUTO_INCREMENT;


INSERT INTO `location` (`location_name`) VALUES
('SFIT Auditorium'),
('SEMINAR HALL'),
('SFIT Ground'),
('QUADRANGLE'),
('DEPARTMENT LAB'),
('DEPARTMENT CLASSROOM');

-- ------------------------------------------------------------------------------------------------------------


CREATE TABLE `branch`(
  `branch_id` int(10) NOT NULL,
  `branch_name` varchar(30) NOT NULL
);


ALTER TABLE `branch`
  ADD PRIMARY KEY (`branch_id`);

ALTER TABLE `branch`
  MODIFY `branch_id` int(10) NOT NULL AUTO_INCREMENT;


INSERT INTO `branch` (`branch_name`) VALUES
('CMPN'),
('ELEC'),
('EXTC'),
('INFT'),
('MECH');
-- ----------------------------------------------------------------------------------------------------------

CREATE TABLE `events` (
  `event_id` int(100) NOT NULL,
  `event_title` varchar(100) NOT NULL,
  `event_price` int(20) NOT NULL,
  `participants` int(100) NOT NULL,
  `type_id` int(10) NOT NULL,
  `location_id` int(10) NOT NULL,
  `date` DATE NOT NULL
);


ALTER TABLE `events`
  ADD PRIMARY KEY (`event_id`);


ALTER TABLE `events`
  ADD FOREIGN KEY (`type_id`) REFERENCES event_type(`type_id`)
  ON DELETE CASCADE;
--
ALTER TABLE `events`
  ADD FOREIGN KEY (`location_id`) REFERENCES location(`location_id`);

--
ALTER TABLE `events`
  MODIFY `event_id` int(100) NOT NULL AUTO_INCREMENT;
--
-- location_id IS FOREIGN KEY

-- Dumping data for table `events`
--

INSERT INTO `events` (`event_id`, `event_title`, `event_price`, `participants`, `type_id`,`location_id`,`date`) VALUES
(1, 'Colloquim', 50, 4, 6,5,'2024-03-22'),
(2, 'HACKX', 500, 2, 5,5,'2023-09-21'),
(3, 'GLOW FOOTBALL', 50, 1, 3,6,'2023-10-01'),
(4, 'RE-KINDLE', 0, 2, 4,4,'2024-02-05'),
(5, 'DJ NIGHT', 300, 1, 2,4,'2024-02-11'),
(6, 'ROBOCON', 50, 1, 1,1,'2023-10-03');


-- ---------------------------------------------------------------------------------------


CREATE TABLE `participants` (
  `p_id` int(10) NOT NULL,
  `event_id` int(10) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `email` varchar(300) NOT NULL,
  `mobile` char(10) NOT NULL,
  `college` varchar(300) NOT NULL,
  `branch_id` int(10) NOT NULL
);

ALTER TABLE `participants`
  ADD PRIMARY KEY (`p_id`);


ALTER TABLE `participants`
  ADD FOREIGN KEY (`event_id`) REFERENCES events(`event_id`) 
  ON DELETE CASCADE;

ALTER TABLE `participants`
  ADD FOREIGN KEY (`branch_id`) REFERENCES branch(`branch_id`);
  
ALTER TABLE `participants`
  MODIFY `p_id` int(10) NOT NULL AUTO_INCREMENT;



-- -----------------------------------------------------------------------------




CREATE TABLE `admin`(
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
);

INSERT INTO `admin` VALUES
('Admin1','password1'),
('Admin2','password2');

-- --------------------------------------------------------------------------------