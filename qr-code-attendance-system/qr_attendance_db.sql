-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 10, 2024 at 12:56 AM
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
-- Database: `qr_attendance_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `attendance_id` int(11) NOT NULL,
  `student_id` varchar(11) DEFAULT NULL,
  `student_name` varchar(100) DEFAULT NULL,
  `section_id` int(5) NOT NULL,
  `subject_name` varchar(100) DEFAULT NULL,
  `time_slot` varchar(50) DEFAULT NULL,
  `attendance_date` date DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Present'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lecturers`
--

CREATE TABLE `lecturers` (
  `lecturer_id` varchar(10) NOT NULL,
  `lecturer_name` varchar(20) NOT NULL,
  `email` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lecturers`
--

INSERT INTO `lecturers` (`lecturer_id`, `lecturer_name`, `email`) VALUES
('LEC01', 'Ms Anusha', 'anusha@gmail.com'),
('LEC02', 'Ms Supriya', 'supriya@gmail.com'),
('LEC03', 'Dr Harivinod', 'harivinod@gmail.com'),
('LEC04', 'Ms Prajna', 'prajna@gmail.com'),
('LEC05', 'Ms Prithvi', 'prithvi@gmail.com'),
('LEC06', 'Dr Shrisha', 'shrisha@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `sections`
--

CREATE TABLE `sections` (
  `section_id` int(5) NOT NULL,
  `section_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sections`
--

INSERT INTO `sections` (`section_id`, `section_name`) VALUES
(1, 'Sec A'),
(2, 'Sec B'),
(3, 'Sec C');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `student_id` varchar(20) NOT NULL,
  `student_name` varchar(20) NOT NULL,
  `section_id` int(20) NOT NULL,
  `qr_code` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`student_id`, `student_name`, `section_id`, `qr_code`) VALUES
('4SO21CS001', 'Abhik ', 1, '4SO21CS001'),
('4SO21CS002', 'Abhinav', 1, '4SO21CS002'),
('4SO21CS003', 'Advaith', 1, '4SO21CS003'),
('4SO21CS004', 'Adwaithika', 1, '4SO21CS004'),
('4SO21CS005', 'Afreen', 1, '4SO21CS005'),
('4SO21CS006', 'Aju Thomas', 1, '4SO21CS006'),
('4SO21CS007', 'Akhil', 1, '4SO21CS007'),
('4SO21CS008', 'Akshaya', 1, '4SO21CS008'),
('4SO21CS009', 'Aldin', 1, '4SO21CS009'),
('4SO21CS010', 'Alita', 1, '4SO21CS010'),
('4SO21CS011', 'Alriya	', 1, '4SO21CS011'),
('4SO21CS012', 'Amisha', 1, '4SO21CS012'),
('4SO21CS013', 'Ancita', 1, '4SO21CS013'),
('4SO21CS014', 'Anjalita', 1, '4SO21CS014'),
('4SO21CS015', 'Anupama S', 1, '4SO21CS015'),
('4SO21CS016', 'Anuradha', 1, '4SO21CS016'),
('4SO21CS017', 'Anurag', 1, '4SO21CS017'),
('4SO21CS018', 'Aron', 1, '4SO21CS018'),
('4SO21CS019', 'Ashton', 1, '4SO21CS019'),
('4SO21CS020', 'Bharath', 1, '4SO21CS020'),
('4SO21CS021', 'Brian', 1, '4SO21CS021'),
('4SO21CS022', 'Chaithanya', 1, '4SO21CS022'),
('4SO21CS023', 'Darshith', 1, '4SO21CS023'),
('4SO21CS024', 'Delson Tellis', 1, '4SO21CS024'),
('4SO21CS031', 'Jessica S', 2, '4SO21CS031'),
('4SO21CS032', 'Jestan', 2, '4SO21CS032'),
('4SO21CS033', 'Jesvita', 2, '4SO21CS033'),
('4SO21CS034', 'Keerthana', 2, '4SO21CS034'),
('4SO21CS035', 'Kushi', 2, '4SO21CS035'),
('4SO21CS036', 'Laksha', 2, '4SO21CS036'),
('4SO21CS037', 'Layona', 2, '4SO21CS037'),
('4SO21CS038', 'Liba', 2, '4SO21CS038'),
('4SO21CS039', 'Lester', 2, '4SO21CS039'),
('4SO21CS040', 'Mareena', 2, '4SO21CS040'),
('4SO21CS041', 'Meghana', 2, '4SO21CS041'),
('4SO21CS042', 'Melisha', 2, '4SO21CS042'),
('4SO21CS043', 'Melson', 2, '4SO21CS043'),
('4SO21CS044', 'Mokshith', 2, '4SO21CS044'),
('4SO21CS045', 'Neema', 2, '4SO21CS045'),
('4SO21CS046', 'Nidhi', 2, '4SO21CS046'),
('4SO21CS047', 'Nishanth', 2, '4SO21CS047'),
('4SO21CS048', 'Pooja', 2, '4SO21CS048'),
('4SO21CS049', 'Prajna', 2, '4SO21CS049'),
('4SO21CS050', 'Prajwal', 2, '4SO21CS050'),
('4SO21CS051', 'Prasthuthi', 2, '4SO21CS051'),
('4SO21CS052', 'Pratham', 2, '4SO21CS052'),
('4SO21CS053', 'Prathibha', 2, '4SO21CS053'),
('4SO21CS054', 'Pratheek', 2, '4SO21CS054'),
('4SO21CS055', 'Prathiksha', 2, '4SO21CS055'),
('4SO21CS061', 'Radesh', 3, '4SO21CS061'),
('4SO21CS062', 'Raksha', 3, '4SO21CS062'),
('4SO21CS063', 'Ranjana', 3, '4SO21CS063'),
('4SO21CS064', 'Rashmith', 3, '4SO21CS064'),
('4SO21CS065', 'Reema', 3, '4SO21CS065'),
('4SO21CS066', 'Saksha', 3, '4SO21CS066'),
('4SO21CS067', 'Sakshi', 3, '4SO21CS067'),
('4SO21CS068', 'Samarth', 3, '4SO21CS068'),
('4SO21CS069', 'Sameeksha', 3, '4SO21CS069'),
('4SO21CS070', 'Samuel', 3, '4SO21CS070'),
('4SO21CS071', 'Samwin', 3, '4SO21CS071'),
('4SO21CS072', 'Tanisha', 3, '4SO21CS072'),
('4SO21CS073', 'Tryphena', 3, '4SO21CS073'),
('4SO21CS074', 'Tryphosa', 3, '4SO21CS074'),
('4SO21CS075', 'Vanesaa', 3, '4SO21CS075'),
('4SO21CS076', 'Vedika', 3, '4SO21CS076'),
('4SO21CS077', 'Veeyan', 3, '4SO21CS077'),
('4SO21CS078', 'Vinay', 3, '4SO21CS078'),
('4SO21CS079', 'Vinaya', 3, '4SO21CS079'),
('4SO21CS080', 'Vina', 3, '4SO21CS080'),
('4SO21CS081', 'Vinith', 3, '4SO21CS081'),
('4SO21CS082', 'Vivian', 3, '4SO21CS082'),
('4SO21CS083', 'Vivan', 3, '4SO21CS083'),
('4SO21CS084', 'Vyasa', 3, '4SO21CS085'),
('4SO21CS085', 'William', 3, '4SO21CS086');

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
  `subject_id` varchar(10) NOT NULL,
  `subject_name` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subjects`
--

INSERT INTO `subjects` (`subject_id`, `subject_name`) VALUES
('SUB01', 'AIML'),
('SUB02', 'DBMS'),
('SUB03', 'DSA'),
('SUB04', 'OOP'),
('SUB05', 'GO'),
('SUB06', 'NLP');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_attendance`
--

CREATE TABLE `tbl_attendance` (
  `USN_usn` varchar(10) NOT NULL,
  `student_name` varchar(20) NOT NULL,
  `course_section` varchar(20) NOT NULL,
  `date` date DEFAULT NULL,
  `time_in` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `Location` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_student`
--

CREATE TABLE `tbl_student` (
  `USN` varchar(10) NOT NULL,
  `student_name` varchar(255) NOT NULL,
  `course_section` varchar(255) NOT NULL,
  `generated_code` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `tbl_student`
--

INSERT INTO `tbl_student` (`USN`, `student_name`, `course_section`, `generated_code`) VALUES
('4S021CS021', 'Aishwarya ', 'CSE B', 'ZME2oUNrqA'),
('4SO21CS001', 'Anusha', 'CSE A', 'kjIOPJH77Y'),
('4SO21CS002', 'Amogh', 'CSE A', 'HAYHDJ87II'),
('4SO21CS003', 'Bhuvan', 'CSE A', 'IDUHgs667H'),
('4SO21CS004', 'Chaitra', 'CSE A', 'PLSYhs78JU'),
('4SO21CS005', 'Devika', 'CSE A', 'NDHDH990NS'),
('4SO21CS006', 'Havana', 'CSE A', 'ndhUUIbh76'),
('4SO21CS007', 'Ganesh', 'CSE A', 'PIubh765nH'),
('4SO21CS008', 'Karthik', 'CSE A', 'PLUYHB67M'),
('4SO21CS009', 'Pari', 'CSE A', 'QWERTYUI87'),
('4SO21CS010', 'Poornika', 'CSE A', 'POIUYT67RE'),
('4SO21CS011', 'Ruchita', 'CSE A', 'mnBVCXZ43S'),
('4SO21CS012', 'Shravan', 'CSE A', 'PLOKMNJIU7'),
('4SO21CS013', 'Shravani', 'CSE A', 'UHBVGYTF5R'),
('4SO21CS014', 'Varsha', 'CSE A', 'uYh67TFRDC'),
('4SO21CS022', 'Bhoomika', 'CSE B', 'PIYkAk6Zzk'),
('4SO21CS023', 'Chirag', 'CSE B', 'ABCkAk22RV'),
('4SO21CS024', 'Dheeraj', 'CSE B', 'JKD00IEUFJ'),
('4SO21CS025', 'Jesvita', 'CSE B', 'OEIRJ80FJE'),
('4SO21CS026', 'Keerthana', 'CSE B', 'HSHab780kJ'),
('4SO21CS027', 'Kushi', 'CSE B', 'PLmjVH99r5'),
('4SO21CS028', 'Laksha', 'CSE B', 'qwerHHY908'),
('4SO21CS029', 'Samantha', 'CSE B', 'WEnsbh78Iy'),
('4SO21CS030', 'Tryphena', 'CSE B', 'XCY87hCVG2'),
('4SO21CS031', 'Tryphosa', 'CSE B', 'p567yuivgf'),
('4SO21CS032', 'Urvashi', 'CSE B', 'PJHYDBJ88Y'),
('4SO21CS033', 'Virat', 'CSE B', 'TUWhd89YGF'),
('4SO21CS034', 'Xavier', 'CSE B', 'TAUbsh09uY'),
('4SO21CS041', 'Amrutha', 'CSE C', 'PLMKJ87UYT'),
('4SO21CS042', 'Bharath', 'CSE C', 'BDGTSY87HN'),
('4SO21CS043', 'Chaitanya', 'CSE C', 'YHGTFCVB76T'),
('4SO21CS044', 'Deepak', 'CSE C', 'UYTGH778JN'),
('4SO21CS045', 'Dheeraj', 'CSE C', 'IUYUIY98Kn'),
('4SO21CS046', 'Gowri', 'CSE C', 'IujhY76uh'),
('4SO21CS047', 'Jason', 'CSE C', 'HUYTGVBH78'),
('4SO21CS048', 'Jessica', 'CSE C', 'FFGHJUYT66Y'),
('4SO21CS049', 'Poorvi', 'CSE C', 'HU7YHGTRFD'),
('4SO21CS050', 'Prajwal', 'CSE C', 'huYHTGFR56'),
('4SO21CS051', 'Rahul', 'CSE C', 'RFCVGT76YH'),
('4SO21CS052', 'Riya', 'CSE C', 'NHSUIJKO88'),
('4SO21CS053', 'Sanjna', 'CSE C', 'FGYtryHB88'),
('4SO21CS054', 'Trisha', 'CSE C', '1Nd5eR9ghW');

-- --------------------------------------------------------

--
-- Table structure for table `timetable`
--

CREATE TABLE `timetable` (
  `timetable_id` varchar(20) NOT NULL,
  `lecturer_id` varchar(20) NOT NULL,
  `day_of_week` varchar(20) NOT NULL,
  `section_id` int(20) NOT NULL,
  `subject_id` varchar(20) NOT NULL,
  `time_start` time NOT NULL,
  `time_end` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `timetable`
--

INSERT INTO `timetable` (`timetable_id`, `lecturer_id`, `day_of_week`, `section_id`, `subject_id`, `time_start`, `time_end`) VALUES
('FRA01', 'LEC02', 'Friday', 1, 'SUB02', '09:00:00', '10:00:00'),
('FRA02', 'LEC01', 'Friday', 1, 'SUB01', '10:00:00', '11:00:00'),
('FRA03', 'LEC04', 'Friday', 1, 'SUB04', '11:00:00', '12:00:00'),
('FRA04', 'LEC05', 'Friday', 1, 'SUB05', '12:00:00', '01:00:00'),
('FRA05', 'LEC06', 'Friday', 1, 'SUB06', '02:00:00', '03:00:00'),
('FRA06', 'LEC03', 'Friday', 1, 'SUB03', '03:00:00', '04:00:00'),
('FRB01', 'LEC04', 'Friday', 2, 'SUB04', '09:00:00', '10:00:00'),
('FRB02', 'LEC05', 'Friday', 2, 'SUB05', '10:00:00', '11:00:00'),
('FRB03', 'LEC01', 'Friday', 2, 'SUB01', '11:00:00', '12:00:00'),
('FRB04', 'LEC06', 'Friday', 2, 'SUB06', '12:00:00', '01:00:00'),
('FRB05', 'LEC02', 'Friday', 2, 'SUB02', '02:00:00', '03:00:00'),
('FRB06', 'LEC04', 'Friday', 2, 'SUB04', '03:00:00', '04:00:00'),
('FRC01', 'LEC06', 'Friday', 3, 'SUB06', '09:00:00', '10:00:00'),
('FRC02', 'LEC03', 'Friday', 3, 'SUB03', '10:00:00', '11:00:00'),
('FRC03', 'LEC02', 'Friday', 3, 'SUB02', '11:00:00', '12:00:00'),
('FRC04', 'LEC03', 'Friday', 3, 'SUB03', '12:00:00', '01:00:00'),
('FRC05', 'LEC05', 'Friday', 3, 'SUB05', '02:00:00', '03:00:00'),
('FRC06', 'LEC01', 'Friday', 3, 'SUB01', '03:00:00', '04:00:00'),
('MOA01', 'LEC02', 'Monday', 1, 'SUB02', '09:00:00', '10:00:00'),
('MOA02', 'LEC04', 'Monday', 1, 'SUB04', '10:00:00', '11:00:00'),
('MOA03', 'LEC01', 'Monday', 1, 'SUB01', '11:00:00', '12:00:00'),
('MOA04', 'LEC03', 'Monday', 1, 'SUB03', '12:00:00', '01:00:00'),
('MOA05', 'LEC06', 'Monday', 1, 'SUB06', '02:00:00', '03:00:00'),
('MOA06', 'LEC05', 'Monday', 1, 'SUB05', '03:00:00', '04:00:00'),
('MOB01', 'LEC03', 'Monday', 2, 'SUB03', '09:00:00', '10:00:00'),
('MOB02', 'LEC05', 'Monday', 2, 'SUB05', '10:00:00', '11:00:00'),
('MOB03', 'LEC04', 'Monday', 2, 'SUB04', '11:00:00', '12:00:00'),
('MOB04', 'LEC06', 'Monday', 2, 'SUB06', '12:00:00', '01:00:00'),
('MOB05', 'LEC01', 'Monday', 2, 'SUB01', '02:00:00', '03:00:00'),
('MOB06', 'LEC02', 'Monday', 2, 'SUB02', '03:00:00', '04:00:00'),
('MOC01', 'LEC06', 'Monday', 3, 'SUB06', '09:00:00', '10:00:00'),
('MOC02', 'LEC06', 'Monday', 3, 'SUB06', '10:00:00', '11:00:00'),
('MOC03', 'LEC05', 'Monday', 3, 'SUB05', '11:00:00', '12:00:00'),
('MOC04', 'LEC01', 'Monday', 3, 'SUB01', '12:00:00', '01:00:00'),
('MOC05', 'LEC04', 'Monday', 3, 'SUB04', '02:00:00', '03:00:00'),
('MOC06', 'LEC03', 'Monday', 3, 'SUB03', '03:00:00', '04:00:00'),
('THA01', 'LEC03', 'Thursday', 1, 'SUB03', '09:00:00', '10:00:00'),
('THA02', 'LEC06', 'Thursday', 1, 'SUB06', '10:00:00', '11:00:00'),
('THA03', 'LEC02', 'Thursday', 1, 'SUB02', '11:00:00', '12:00:00'),
('THA04', 'LEC05', 'Thursday', 1, 'SUB05', '12:00:00', '01:00:00'),
('THA05', 'LEC01', 'Thursday', 1, 'SUB01', '02:00:00', '03:00:00'),
('THA06', 'LEC06', 'Thursday', 1, 'SUB06', '03:00:00', '04:00:00'),
('THB01', 'LEC01', 'Thursday', 2, 'SUB01', '09:00:00', '10:00:00'),
('THB02', 'LEC05', 'Thursday', 2, 'SUB05', '10:00:00', '11:00:00'),
('THB03', 'LEC03', 'Thursday', 2, 'SUB03', '11:00:00', '12:00:00'),
('THB04', 'LEC04', 'Thursday', 2, 'SUB04', '12:00:00', '01:00:00'),
('THB05', 'LEC06', 'Thursday', 2, 'SUB06', '02:00:00', '03:00:00'),
('THB06', 'LEC02', 'Thursday', 2, 'SUB02', '03:00:00', '04:00:00'),
('THC01', 'LEC02', 'Thursday', 3, 'SUB02', '09:00:00', '10:00:00'),
('THC02', 'LEC04', 'Thursday', 3, 'SUB04', '10:00:00', '11:00:00'),
('THC03', 'LEC01', 'Thursday', 3, 'SUB01', '11:00:00', '12:00:00'),
('THC04', 'LEC03', 'Thursday', 3, 'SUB03', '12:00:00', '01:00:00'),
('THC05', 'LEC05', 'Thursday', 3, 'SUB05', '02:00:00', '03:00:00'),
('THC06', 'LEC04', 'Thursday', 3, 'SUB04', '03:00:00', '04:00:00'),
('TUA01', 'LEC03', 'Tuesday', 1, 'SUB03', '09:00:00', '10:00:00'),
('TUA02', 'LEC01', 'Tuesday', 1, 'SUB01', '10:00:00', '11:00:00'),
('TUA03', 'LEC04', 'Tuesday', 1, 'SUB04', '11:00:00', '12:00:00'),
('TUA04', 'LEC05', 'Tuesday', 1, 'SUB05', '12:00:00', '01:00:00'),
('TUA05', 'LEC06', 'Tuesday', 1, 'SUB06', '02:00:00', '03:00:00'),
('TUA06', 'LEC03', 'Tuesday', 1, 'SUB03', '03:00:00', '04:00:00'),
('TUB01', 'LEC01', 'Tuesday', 2, 'SUB01', '09:00:00', '10:00:00'),
('TUB02', 'LEC05', 'Tuesday', 2, 'SUB05', '10:00:00', '11:00:00'),
('TUB03', 'LEC06', 'Tuesday', 2, 'SUB06', '11:00:00', '12:00:00'),
('TUB04', 'LEC01', 'Tuesday', 2, 'SUB01', '12:00:00', '01:00:00'),
('TUB05', 'LEC02', 'Tuesday', 2, 'SUB02', '02:00:00', '03:00:00'),
('TUB06', 'LEC04', 'Tuesday', 2, 'SUB04', '03:00:00', '04:00:00'),
('TUC01', 'LEC04', 'Tuesday', 3, 'SUB04', '09:00:00', '10:00:00'),
('TUC02', 'LEC06', 'Tuesday', 3, 'SUB06', '10:00:00', '11:00:00'),
('TUC03', 'LEC02', 'Tuesday', 3, 'SUB02', '11:00:00', '12:00:00'),
('TUC04', 'LEC03', 'Tuesday', 3, 'SUB03', '12:00:00', '01:00:00'),
('TUC05', 'LEC05', 'Tuesday', 3, 'SUB05', '02:00:00', '03:00:00'),
('TUC06', 'LEC01', 'Tuesday', 3, 'SUB01', '03:00:00', '04:00:00'),
('WEA01', 'LEC01', 'Wednesday', 1, 'SUB01', '09:00:00', '10:00:00'),
('WEA02', 'LEC02', 'Wednesday', 1, 'SUB02', '10:00:00', '11:00:00'),
('WEA03', 'LEC03', 'Wednesday', 1, 'SUB03', '11:00:00', '12:00:00'),
('WEA04', 'LEC04', 'Wednesday', 1, 'SUB04', '12:00:00', '01:00:00'),
('WEA05', 'LEC06', 'Wednesday', 1, 'SUB06', '02:00:00', '03:00:00'),
('WEA06', 'LEC05', 'Wednesday', 1, 'SUB05', '03:00:00', '04:00:00'),
('WEB01', 'LEC04', 'Wednesday', 2, 'SUB04', '09:00:00', '10:00:00'),
('WEB02', 'LEC06', 'Wednesday', 2, 'SUB06', '10:00:00', '11:00:00'),
('WEB03', 'LEC01', 'Wednesday', 2, 'SUB01', '11:00:00', '12:00:00'),
('WEB04', 'LEC02', 'Wednesday', 2, 'SUB02', '12:00:00', '01:00:00'),
('WEB05', 'LEC05', 'Wednesday', 2, 'SUB05', '02:00:00', '03:00:00'),
('WEB06', 'LEC03', 'Wednesday', 2, 'SUB03', '03:00:00', '04:00:00'),
('WEC01', 'LEC05', 'Wednesday', 3, 'SUB05', '09:00:00', '10:00:00'),
('WEC02', 'LEC03', 'Wednesday', 3, 'SUB03', '10:00:00', '11:00:00'),
('WEC03', 'LEC04', 'Wednesday', 3, 'SUB04', '11:00:00', '12:00:00'),
('WEC04', 'LEC05', 'Wednesday', 3, 'SUB05', '12:00:00', '01:00:00'),
('WEC05', 'LEC01', 'Wednesday', 3, 'SUB01', '02:00:00', '03:00:00'),
('WEC06', 'LEC02', 'Wednesday', 3, 'SUB02', '03:00:00', '04:00:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`attendance_id`),
  ADD KEY `section_id` (`section_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `lecturers`
--
ALTER TABLE `lecturers`
  ADD PRIMARY KEY (`lecturer_id`);

--
-- Indexes for table `sections`
--
ALTER TABLE `sections`
  ADD PRIMARY KEY (`section_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`student_id`),
  ADD UNIQUE KEY `qr_code` (`qr_code`),
  ADD KEY `fk_section` (`section_id`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`subject_id`);

--
-- Indexes for table `tbl_attendance`
--
ALTER TABLE `tbl_attendance`
  ADD UNIQUE KEY `USN_usn` (`USN_usn`);

--
-- Indexes for table `tbl_student`
--
ALTER TABLE `tbl_student`
  ADD PRIMARY KEY (`USN`);

--
-- Indexes for table `timetable`
--
ALTER TABLE `timetable`
  ADD PRIMARY KEY (`timetable_id`),
  ADD KEY `lecturer_id` (`lecturer_id`),
  ADD KEY `subject_id` (`subject_id`),
  ADD KEY `section_id` (`section_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `attendance_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`section_id`) REFERENCES `sections` (`section_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `student_id` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`);

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `fk_section` FOREIGN KEY (`section_id`) REFERENCES `sections` (`section_id`);

--
-- Constraints for table `timetable`
--
ALTER TABLE `timetable`
  ADD CONSTRAINT `lecturer_id` FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`lecturer_id`),
  ADD CONSTRAINT `section_id` FOREIGN KEY (`section_id`) REFERENCES `sections` (`section_id`),
  ADD CONSTRAINT `subject_id` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
