-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 01, 2026 at 08:00 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `skilltrack`
--

-- --------------------------------------------------------

--
-- Table structure for table `profiles`
--

CREATE TABLE `profiles` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `college` varchar(100) DEFAULT NULL,
  `degree` varchar(100) DEFAULT NULL,
  `graduation_year` int(11) DEFAULT NULL,
  `linkedin` varchar(255) DEFAULT NULL,
  `github` varchar(255) DEFAULT NULL,
  `bio` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `profiles`
--

INSERT INTO `profiles` (`id`, `user_id`, `full_name`, `phone`, `college`, `degree`, `graduation_year`, `linkedin`, `github`, `bio`) VALUES
(1, 2, 'Sneha P', '123456789', 'IIT Bombay', 'Btech', 2022, 'snehbfh', 'heb3ibf3i', 'hello helohbf3rwuhuo3w'),
(2, 3, 'Kamal S', '12345654', 'IIT Madras', 'Mtech', 2020, 'snehbfh', 'https://kamu.com', 'hfb2bfwibfiwubf'),
(3, 4, 'sharvari Soh', '85789758232835', 'Shivraj College', 'MCA', 2021, 'bcejfbewifniu', 'eihfiuehf', 'nbfwibfieruhfeiuh'),
(4, 5, 'vishwa desai', '1132435465456', 'IIT B', 'btech', 2022, 'https://vd', 'https://dv', 'hello i am vishwa');

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `project_name` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `technology` varchar(100) DEFAULT NULL,
  `github_link` varchar(255) DEFAULT NULL,
  `demo_link` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`id`, `user_id`, `project_name`, `description`, `technology`, `github_link`, `demo_link`, `created_at`) VALUES
(1, 1, 'HelloWorld', 'engine that optimises flow', 'Python, JAva', 'https://github.com/Pavithra-Se', 'https://helloworl.com', '2026-06-27 00:48:57'),
(2, 2, 'CV engine', 'hbf3ihfb3iubfiu35b', 'flask', 'https://github.com/sneha', 'https://demo.com/sneha', '2026-06-27 01:03:02'),
(3, 3, 'school management', 'jefbwfbwbfjwhbfq2j4bf4bf4uwf', 'java', 'https://github.com/Pavithra-Se', 'https://hellschooll.com', '2026-06-27 01:11:41'),
(4, 4, 'abc', 'fbiwfiu34wn', 'rgn4wjng', 'https://bhebe.com', 'https://bbb.co', '2026-06-27 01:26:11'),
(5, 5, 'viswaproject', 'hellloooo', 'javascript,java', 'https://dfgrdgdre', 'https://fgdrg', '2026-06-27 21:16:08');

-- --------------------------------------------------------

--
-- Table structure for table `skills`
--

CREATE TABLE `skills` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `skill_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `skills`
--

INSERT INTO `skills` (`id`, `user_id`, `skill_name`) VALUES
(2, 1, 'coding'),
(4, 1, 'SRE'),
(5, 2, 'python'),
(6, 2, 'java'),
(7, 2, 'cloud'),
(9, 3, 'python'),
(11, 4, 'java'),
(13, 5, 'java');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `created_at`) VALUES
(1, 'sanikapurao', 'abc@email.com', 'scrypt:32768:8:1$n2s5eydJUbR7Paw8$bbd89941e5d1c3839b9ad11d12e23f05cabeb33b41fee51656078d188f5c3cc2b0f1ea67d5c2725bc2fb02c72e8453883445c105558d3f5af639138ad9e8c3f1', '2026-06-26 18:52:54'),
(2, 'sneha', 'pqr@email.com', 'scrypt:32768:8:1$MBtmgVBNnOed5aKv$94d7320de0ce3a89735e64ae940f59bc49db1409d699f9194068a3f37449ca93079aaf370f13cb31ca14ba35a96eaefdb3bcfdeda48fcf45bfbb724f8f5f0b06', '2026-06-26 19:30:12'),
(3, 'Kamal_Sohani', 'kamal@email.com', 'scrypt:32768:8:1$FrrQ3NFSll5BLTV5$b93e5f0f3afceee906dcc2d1bfbc6f6f7cf53a19673a53b5fc3a031dc491cddd0ed4892da8970ca592015f01af095a4c8795f49322751192e1ee4d7958dad9d3', '2026-06-26 19:37:28'),
(4, 'sharvari_sohani', 'sharu20@email.com', 'scrypt:32768:8:1$zkqyfGBSXRME4f0p$44413e833029891a70e88aee2e4a3d9eb63673647c2480c1d8a0e7a91be41c232cc1c5603b20c9806e74fa2cd248c0c93d8f297d199e4385f14b7d23cd0c44dc', '2026-06-26 19:46:08'),
(5, 'vishwa_desai', 'vd@email.com', 'scrypt:32768:8:1$J0z72T14AKJLSTkl$6366bf679359341d272ad05050c36ef6fe7fc34d46aeeafa8b3eade0bc61e7ea3903ae650d5daab89f3f93a2cee3d2f2ac0a9594bb29b5d4f7ede763174113ca', '2026-06-27 15:41:07');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `profiles`
--
ALTER TABLE `profiles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `skills`
--
ALTER TABLE `skills`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `profiles`
--
ALTER TABLE `profiles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `skills`
--
ALTER TABLE `skills`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `profiles`
--
ALTER TABLE `profiles`
  ADD CONSTRAINT `profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `projects`
--
ALTER TABLE `projects`
  ADD CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `skills`
--
ALTER TABLE `skills`
  ADD CONSTRAINT `skills_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
