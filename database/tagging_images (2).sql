-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 07, 2024 at 10:25 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hackthon`
--

-- --------------------------------------------------------

--
-- Table structure for table `tagging_images`
--

CREATE TABLE `tagging_images` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `tag_numbers` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`tag_numbers`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tagging_images`
--

INSERT INTO `tagging_images` (`id`, `name`, `photo`, `tag_numbers`) VALUES
(94, 'jaswanth', 'photos/WhatsApp Image 2024-06-03 at 15.22.21 (1).jpeg', '10'),
(95, 'jaswanth', 'photos/WhatsApp Image 2024-06-03 at 15.22.21 (2).jpeg', '10'),
(96, 'jaswanth', 'photos/WhatsApp Image 2024-06-03 at 15.22.21.jpeg', '10'),
(97, 'jaswanth', 'photos/WhatsApp Image 2024-06-03 at 15.22.22.jpeg', '10'),
(98, 'jaswanth', 'photos/photos_pexels-thgusstavo-1933873 (5).jpg', '10'),
(99, 'jaswanth', 'photos/photos_photos_pexels-danxavier-1239291 (1).jpg', '10'),
(100, 'jaswanth', 'photos/photos_photos_pexels-photo-614810 (7).jpeg', '10'),
(101, 'jaswanth', 'photos/photos_WhatsApp Image 2024-04-19 at 23.21.26_2caae3bb.jpg', '10'),
(102, 'jaswanth', 'photos/muj (1).jpg', '10'),
(103, 'jaswanth', 'photos/muj2 (1).jpg', '10'),
(104, 'jaswanth', 'photos/muj2.jpg', '10'),
(105, 'jaswanth', 'photos/photos_jaswanth.jpg', '10'),
(106, 'jaswanth', 'photos/WhatsApp Image 2024-06-03 at 15.22.19 - Copy.jpeg', '10'),
(107, 'jaswanth', 'photos/WhatsApp Image 2024-06-03 at 15.22.19 (1) - Copy.jpeg', '10'),
(108, 'jaswanth', 'photos/WhatsApp Image 2024-06-03 at 15.22.19 (1).jpeg', '10'),
(109, 'jaswanth', 'photos/WhatsApp Image 2024-06-03 at 15.22.19.jpeg', '10'),
(111, 'jaswanth', 'photos/photos_WhatsApp Image 2024-04-19 at 23.21.26_2caae3bb.jpg', '10'),
(112, 'jaswanth', 'static/photos/Blood-sediment-test-tubes-red-blood-cells1.jpg', '10'),
(113, 'reddy', 'static/photos/Synthesis-lipoprotein-complexes-intestine-liver-blood-plasma.jpg', '11'),
(114, 'reddy', 'photos/School-children-wearing-school-uniforms.jpg', '11');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tagging_images`
--
ALTER TABLE `tagging_images`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tagging_images`
--
ALTER TABLE `tagging_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=115;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
