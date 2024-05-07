-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 07, 2024 at 02:38 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rpll`
--

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `nama` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `level` enum('1','2') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `nama`, `username`, `email`, `password`, `level`) VALUES
(9, 'Syamsul Maarip', '227006014', 'syamsulmaarip@gmail.com', '02', '1'),
(10, 'arip', 'arip02', 'arip@gmail.com', '7c4a8d09ca3762af61e59520943dc26494f8941b', '1'),
(11, 'syamsul', 'syamsul', 'syamsul12@gmail.com', '7c222fb2927d828af22f592134e8932480637c0d', '1'),
(12, 'Syamsul', 'jurnal', 'jurnal@gmail.com', 'f7c3bc1d808e04732adf679965ccc34ca7ae3441', '1');

-- --------------------------------------------------------

--
-- Table structure for table `tugas`
--

CREATE TABLE `tugas` (
  `mata_kuliah` varchar(255) DEFAULT NULL,
  `tenggat_waktu` datetime DEFAULT NULL,
  `partisipan` varchar(50) DEFAULT NULL,
  `sks` int(11) DEFAULT NULL,
  `tingkat_kesulitan` varchar(50) DEFAULT NULL,
  `jenis_tugas` varchar(50) DEFAULT NULL,
  `id_tugas` int(11) NOT NULL,
  `id_user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tugas`
--

INSERT INTO `tugas` (`mata_kuliah`, `tenggat_waktu`, `partisipan`, `sks`, `tingkat_kesulitan`, `jenis_tugas`, `id_tugas`, `id_user`) VALUES
('kalkulus', '2023-12-15 06:57:00', 'individu', 1, 'mudah', 'paper', 53, 9),
('Sistem Digital', '2024-02-04 23:59:00', 'individu', 3, 'sulit', 'projek', 56, 10),
('Aljabar', '2024-01-28 08:00:00', 'kelompok', 3, 'sulit', 'jurnal', 57, 10),
('PBO', '2024-01-20 22:00:00', 'kelompok', 3, 'sedang', 'projek', 58, 10),
('IMK', '2024-01-20 22:00:00', 'individu', 2, 'mudah', 'quizz', 59, 10),
('RPL', '2024-01-19 23:59:00', 'kelompok', 3, 'sulit', 'projek', 60, 10),
('Arsitektur dan Organisasi', '2024-01-23 16:00:00', 'kelompok', 3, 'sulit', 'projek', 61, 10),
('Pemrograman Sistem', '2024-02-03 23:59:00', 'individu', 3, 'sedang', 'rangkuman', 62, 10),
('Statistika', '2024-01-26 23:59:00', 'individu', 2, 'mudah', 'esai', 63, 10),
('Matematika Distrit', '2024-01-29 20:30:00', 'individu', 3, 'sedang', 'quizz', 64, 10),
('Basis Data', '2024-01-28 08:00:00', 'kelompok', 3, 'sedang', 'quizz', 65, 10),
('Mamtematika', '2023-12-30 14:39:00', 'kelompok', 3, 'sedang', 'esai', 66, 11),
('Kalkulus I', '2023-12-29 14:40:00', 'individu', 2, 'mudah', 'rangkuman', 67, 11),
('Astronomi', '2024-01-01 14:42:00', 'individu', 3, 'sulit', 'projek', 68, 11),
('Ajabar', '2023-12-29 14:46:00', 'individu', 3, 'sedang', 'paper', 69, 11),
('Laprak Bubut ii', '2023-12-29 07:00:00', 'individu', 1, 'sedang', 'rangkuman', 70, 11),
('PPT agama', '2023-12-30 23:59:00', 'individu', 1, 'sedang', 'jurnal', 71, 11),
('English Class Formasi', '2023-12-29 16:00:00', 'individu', 1, 'mudah', 'rangkuman', 72, 11),
('Sistem Digital', '2024-02-04 23:59:00', 'individu', 3, 'sulit', 'projek', 73, 12),
('Aljabar', '2024-01-28 08:00:00', 'kelompok', 3, 'sulit', 'jurnal', 74, 12),
('PBO', '2024-01-20 22:00:00', 'kelompok', 3, 'sedang', 'projek', 75, 12),
('IMK', '2024-01-20 22:00:00', 'individu', 2, 'mudah', 'quizz', 76, 12),
('RPL', '2024-01-19 23:00:00', 'kelompok', 3, 'mudah', 'esai', 77, 12),
('ARKOM', '2024-01-23 16:00:00', 'kelompok', 3, 'sulit', 'projek', 78, 12),
('Pemrograman Sistem', '2024-02-03 23:59:00', 'individu', 3, 'sedang', 'rangkuman', 79, 12),
('Statistika', '2024-01-26 23:59:00', 'individu', 2, 'mudah', 'esai', 80, 12),
('Matematika Diskrit', '2024-01-29 20:30:00', 'individu', 3, 'sedang', 'quizz', 81, 12),
('Basis Data', '2024-01-28 08:00:00', 'kelompok', 3, 'mudah', 'projek', 82, 12);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `register`
--
ALTER TABLE `register`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tugas`
--
ALTER TABLE `tugas`
  ADD PRIMARY KEY (`id_tugas`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `register`
--
ALTER TABLE `register`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `tugas`
--
ALTER TABLE `tugas`
  MODIFY `id_tugas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=83;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
