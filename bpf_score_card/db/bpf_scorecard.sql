-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Aug 04, 2026 at 04:40 PM
-- Server version: 8.0.40
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bpf_scorecard`
--

CREATE DATABASE IF NOT EXISTS `bpf_scorecard` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `bpf_scorecard`;

-- --------------------------------------------------------

--
-- Table structure for table `administrators`
--

CREATE TABLE `administrators` (
  `id` bigint UNSIGNED NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `email` varchar(190) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `last_login_at` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `administrators`
--

INSERT INTO `administrators` (`id`, `full_name`, `email`, `password_hash`, `is_active`, `last_login_at`, `created_at`, `updated_at`) VALUES
(1, 'emmanuel mnjowe', 'emnjowe@ecsahc.org', '$2y$10$PypiEtJSCcM2P944dPDV.uKjvPbViCVbJPul6A3fDXHec26l2ZbN2', 1, '2026-08-04 19:27:59', '2026-08-04 15:52:50', '2026-08-04 16:27:59');

-- --------------------------------------------------------

--
-- Table structure for table `criteria`
--

CREATE TABLE `criteria` (
  `id` smallint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `display_order` smallint UNSIGNED NOT NULL DEFAULT '0',
  `weight_percent` decimal(5,2) NOT NULL DEFAULT '20.00',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ;

--
-- Dumping data for table `criteria`
--

INSERT INTO `criteria` (`id`, `name`, `description`, `display_order`, `weight_percent`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Relevance and significance', 'Alignment with the Forum theme; importance of the health issue addressed', 1, 15.00, 1, '2026-08-04 11:09:20', '2026-08-04 11:09:20'),
(2, 'Innovation and originality', 'Novelty of the intervention, approach or application', 2, 15.00, 1, '2026-08-04 11:09:20', '2026-08-04 11:09:20'),
(3, 'Technical and methodological quality', 'Clarity of objectives, appropriateness of methods and reliability of evidence', 3, 20.00, 1, '2026-08-04 11:09:20', '2026-08-04 11:09:20'),
(4, 'Results and demonstrated impact', 'Clear findings, measurable outcomes and contribution to health improvement', 4, 20.00, 1, '2026-08-04 11:09:20', '2026-08-04 11:09:20'),
(5, 'Scalability and sustainability', 'Potential for replication, institutionalisation and sustained implementation', 5, 10.00, 1, '2026-08-04 11:09:20', '2026-08-04 11:09:20'),
(6, 'Quality of presentation', 'Logical structure, clarity, effective use of visuals and adherence to time', 6, 10.00, 1, '2026-08-04 11:09:20', '2026-08-04 11:09:20'),
(7, 'Response to questions', 'Accuracy, confidence and depth of responses during discussion', 7, 10.00, 1, '2026-08-04 11:09:20', '2026-08-04 11:09:20');

-- --------------------------------------------------------

--
-- Table structure for table `judges`
--

CREATE TABLE `judges` (
  `id` bigint UNSIGNED NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `judges`
--

INSERT INTO `judges` (`id`, `email`, `created_at`, `updated_at`) VALUES
(1, 'emnjowe@ecsahc.org', '2026-08-04 09:01:06', '2026-08-04 09:01:06'),
(2, 'emmanuelmnjowe@gmail.com', '2026-08-04 09:04:01', '2026-08-04 09:04:01'),
(3, 'smyeni@ecsahc.org', '2026-08-04 14:43:31', '2026-08-04 14:43:31'),
(4, 'bmushi@ecsahc.org', '2026-08-04 14:43:31', '2026-08-04 14:43:31'),
(5, 'chris@ecsahc.org', '2026-08-04 14:43:31', '2026-08-04 14:43:31'),
(6, 'uletawo@ecsahc.org', '2026-08-04 14:43:31', '2026-08-04 14:43:31');

-- --------------------------------------------------------

--
-- Table structure for table `poster_criteria`
--

CREATE TABLE `poster_criteria` (
  `id` int UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `display_order` int UNSIGNED NOT NULL,
  `weight_percent` decimal(5,2) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `poster_criteria`
--

INSERT INTO `poster_criteria` (`id`, `name`, `description`, `display_order`, `weight_percent`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Relevance and significance', 'Alignment with the Forum theme and importance of the subject', 1, 15.00, 1, '2026-08-04 11:57:44', '2026-08-04 11:57:44'),
(2, 'Scientific and technical quality', 'Clear objectives, sound methods and credible findings', 2, 20.00, 1, '2026-08-04 11:57:44', '2026-08-04 11:57:44'),
(3, 'Innovation and originality', 'Novelty and added value of the practice or intervention', 3, 15.00, 1, '2026-08-04 11:57:44', '2026-08-04 11:57:44'),
(4, 'Results and demonstrated impact', 'Evidence of effectiveness and clearly presented outcomes', 4, 20.00, 1, '2026-08-04 11:57:44', '2026-08-04 11:57:44'),
(5, 'Poster organisation and visual design', 'Readability, logical flow, appropriate graphics and balanced use of text', 5, 15.00, 1, '2026-08-04 11:57:44', '2026-08-04 11:57:44'),
(6, 'Scalability and applicability', 'Potential for adaptation, replication and sustainability', 6, 10.00, 1, '2026-08-04 11:57:44', '2026-08-04 11:57:44'),
(7, 'Presenter engagement', 'Ability to explain the poster clearly and respond to questions', 7, 5.00, 1, '2026-08-04 11:57:44', '2026-08-04 11:57:44');

-- --------------------------------------------------------

--
-- Table structure for table `poster_score_items`
--

CREATE TABLE `poster_score_items` (
  `id` bigint UNSIGNED NOT NULL,
  `score_id` bigint UNSIGNED NOT NULL,
  `criterion_id` int UNSIGNED NOT NULL,
  `score_value` decimal(5,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `poster_score_items`
--

INSERT INTO `poster_score_items` (`id`, `score_id`, `criterion_id`, `score_value`, `created_at`, `updated_at`) VALUES
(1, 6, 1, 45.00, '2026-08-04 13:16:11', '2026-08-04 13:16:11'),
(2, 6, 2, 35.00, '2026-08-04 13:16:11', '2026-08-04 13:16:11'),
(3, 6, 3, 34.00, '2026-08-04 13:16:11', '2026-08-04 13:16:11'),
(4, 6, 4, 35.00, '2026-08-04 13:16:11', '2026-08-04 13:16:11'),
(5, 6, 5, 35.00, '2026-08-04 13:16:11', '2026-08-04 13:16:11'),
(6, 6, 6, 32.00, '2026-08-04 13:16:11', '2026-08-04 13:16:11'),
(7, 6, 7, 100.00, '2026-08-04 13:16:11', '2026-08-04 13:16:11'),
(8, 7, 1, 42.00, '2026-08-04 13:20:07', '2026-08-04 13:20:07'),
(9, 7, 2, 100.00, '2026-08-04 13:20:07', '2026-08-04 13:20:07'),
(10, 7, 3, 100.00, '2026-08-04 13:20:07', '2026-08-04 13:20:07'),
(11, 7, 4, 12.00, '2026-08-04 13:20:07', '2026-08-04 13:20:07'),
(12, 7, 5, 13.00, '2026-08-04 13:20:07', '2026-08-04 13:20:07'),
(13, 7, 6, 13.00, '2026-08-04 13:20:07', '2026-08-04 13:20:07'),
(14, 7, 7, 100.00, '2026-08-04 13:20:07', '2026-08-04 13:20:07'),
(15, 10, 1, 34.00, '2026-08-04 14:07:16', '2026-08-04 14:07:16'),
(16, 10, 2, 43.00, '2026-08-04 14:07:16', '2026-08-04 14:07:16'),
(17, 10, 3, 100.00, '2026-08-04 14:07:16', '2026-08-04 14:07:16'),
(18, 10, 4, 10.00, '2026-08-04 14:07:16', '2026-08-04 14:07:16'),
(19, 10, 5, 32.00, '2026-08-04 14:07:16', '2026-08-04 14:07:16'),
(20, 10, 6, 22.00, '2026-08-04 14:07:16', '2026-08-04 14:07:16'),
(21, 10, 7, 43.00, '2026-08-04 14:07:16', '2026-08-04 14:07:16'),
(22, 11, 1, 46.00, '2026-08-04 14:08:42', '2026-08-04 14:08:42'),
(23, 11, 2, 36.00, '2026-08-04 14:08:42', '2026-08-04 14:08:42'),
(24, 11, 3, 100.00, '2026-08-04 14:08:42', '2026-08-04 14:08:42'),
(25, 11, 4, 36.00, '2026-08-04 14:08:42', '2026-08-04 14:08:42'),
(26, 11, 5, 36.00, '2026-08-04 14:08:42', '2026-08-04 14:08:42'),
(27, 11, 6, 36.00, '2026-08-04 14:08:42', '2026-08-04 14:08:42'),
(28, 11, 7, 100.00, '2026-08-04 14:08:42', '2026-08-04 14:08:42'),
(29, 13, 1, 54.00, '2026-08-04 14:16:23', '2026-08-04 14:16:23'),
(30, 13, 2, 85.00, '2026-08-04 14:16:23', '2026-08-04 14:16:23'),
(31, 13, 3, 98.00, '2026-08-04 14:16:23', '2026-08-04 14:16:23'),
(32, 13, 4, 45.00, '2026-08-04 14:16:23', '2026-08-04 14:16:23'),
(33, 13, 5, 42.00, '2026-08-04 14:16:23', '2026-08-04 14:16:23'),
(34, 13, 6, 85.00, '2026-08-04 14:16:23', '2026-08-04 14:16:23'),
(35, 13, 7, 78.00, '2026-08-04 14:16:23', '2026-08-04 14:16:23'),
(36, 14, 1, 54.00, '2026-08-04 14:16:55', '2026-08-04 14:16:55'),
(37, 14, 2, 85.00, '2026-08-04 14:16:55', '2026-08-04 14:16:55'),
(38, 14, 3, 98.00, '2026-08-04 14:16:55', '2026-08-04 14:16:55'),
(39, 14, 4, 54.00, '2026-08-04 14:16:55', '2026-08-04 14:16:55'),
(40, 14, 5, 45.00, '2026-08-04 14:16:55', '2026-08-04 14:16:55'),
(41, 14, 6, 100.00, '2026-08-04 14:16:55', '2026-08-04 14:16:55'),
(42, 14, 7, 45.00, '2026-08-04 14:16:55', '2026-08-04 14:16:55'),
(43, 16, 1, 36.00, '2026-08-04 14:23:47', '2026-08-04 14:23:47'),
(44, 16, 2, 65.00, '2026-08-04 14:23:47', '2026-08-04 14:23:47'),
(45, 16, 3, 100.00, '2026-08-04 14:23:47', '2026-08-04 14:23:47'),
(46, 16, 4, 35.00, '2026-08-04 14:23:47', '2026-08-04 14:23:47'),
(47, 16, 5, 64.00, '2026-08-04 14:23:47', '2026-08-04 14:23:47'),
(48, 16, 6, 65.00, '2026-08-04 14:23:47', '2026-08-04 14:23:47'),
(49, 16, 7, 100.00, '2026-08-04 14:23:47', '2026-08-04 14:23:47');

-- --------------------------------------------------------

--
-- Stand-in structure for view `presentation_score_summary`
-- (See below for the actual view)
--
CREATE TABLE `presentation_score_summary` (
`average_score` decimal(6,2)
,`institution` varchar(255)
,`maximum_score` decimal(5,2)
,`minimum_score` decimal(5,2)
,`number_of_judges` bigint
,`presentation_title` varchar(500)
,`presenter_id` bigint unsigned
,`presenter_name` varchar(255)
,`subtheme_id` tinyint unsigned
,`subtheme_name` varchar(255)
);

-- --------------------------------------------------------

--
-- Table structure for table `presenters`
--

CREATE TABLE `presenters` (
  `id` bigint UNSIGNED NOT NULL,
  `subtheme_id` tinyint UNSIGNED NOT NULL,
  `presenter_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `institution` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `presentation_title` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `presentation_type` enum('oral','poster') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'oral',
  `abstract_text` text COLLATE utf8mb4_unicode_ci,
  `display_order` smallint UNSIGNED NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `presenters`
--

INSERT INTO `presenters` (`id`, `subtheme_id`, `presenter_name`, `institution`, `presentation_title`, `presentation_type`, `abstract_text`, `display_order`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 1, 'Bongani Dube', 'NERCHA', 'Eswatini HIV Estimates 2025: Winning the Battle on People Acquiring HIV in Eswatini by 2030: Spectrum\'s AIM and Naomi Models.', 'oral', NULL, 1, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(2, 1, 'Uwumuryango Prisca', 'Rwanda Biomedical Center', 'Five-Year Surveillance of Transfusion-Transmissible Infections Among Voluntary Blood Donors in Kigali, Rwanda (2019-2023)', 'oral', NULL, 2, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(3, 1, 'Ally Hussein', 'Tanzania Field Epidemiology and Laboratory Training Program', 'Strengthening public health surveillance at points of entry: A Tanzanian case study of FETP-Frontline adaptation', 'oral', NULL, 3, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(4, 1, 'Marceline Finda', 'Managing Director, African Conversations Initiative; Research Scientist, Ifakara Health Institute', 'Advancing regional preparedness for gene-drive mosquitoes for malaria control in Africa', 'oral', NULL, 4, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(5, 1, 'Rifat Hossain', 'Global Policy Reporting/Health Policy Watch', 'Breaking the Outbreak Cycle: A Standing, Sovereign Health-Intelligence Capability for the ECSA Region', 'oral', NULL, 5, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(6, 2, 'Mbuso Zwane', 'Ministry of Health', 'Deployment to Inclusion: Lessons from Building a National Health Information Exchange on Open Standards in Eswatini', 'oral', NULL, 1, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(7, 2, 'Ayebare Timothy', 'ECSA-HC', 'Engineering a Continent-Scale Digital SLIPTA Platform under HEPRR: ECSA-HC\'s Multi-Tenant Web Application for Standardised Laboratory Accreditation and Universal Health Coverage Diagnostic Quality', 'oral', NULL, 2, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(8, 2, 'Ireen Hakasenke', 'Palladium Data.FI, Eswatini', 'Leveraging National EMR (CMIS) Enhancements to Enable Monitoring and Rapid Scale-Up of Lenacapavir Delivery in Eswatini\'s Differentiated PrEP Program.', 'oral', NULL, 3, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(9, 2, 'Davie Simwaba', 'ZNPHI', 'Digitising Points of Entry for IHR Core-Capacity Compliance in Zambia: ZNPHI\'s Nationwide Deployment of an Explainable-AI Traveller-Screening Platform under HEPRR', 'oral', NULL, 4, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(10, 2, 'Benedette Otieno', 'Palladium / Ministry of Health', 'Optimizing HIV Programming in Eswatini through a Machine Learning Model that Predicts ART Treatment Interruption', 'oral', NULL, 5, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(11, 2, 'Fredros Okumu', 'University of Glasgow', 'VectorGrid-Africa: building a regional mosquito surveillance and early-warning system for health security in ECSA', 'oral', NULL, 6, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(12, 3, 'Siniketiwe Zwane', 'Ministry of Health/ Eswatini National Nutrition Council', 'Breaking Barriers: Culturally Tailored Male Engagement for Early Childhood Development and Nutrition in Eswatini', 'oral', NULL, 1, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(13, 3, 'Lemmy Mabuga', 'The East, Central, and Southern Africa College of Nursing and Midwifery', 'Unlocking Africa\'s Demographic Dividend: Proceedings of the 2026 ECSA Regional Youth Summit on Sexual and Reproductive Health', 'oral', NULL, 2, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(14, 3, 'Prof. Bellington Vwalika', NULL, 'East, Central and Southern Africa College of Obstetrics and Gynaecology Community of Practice Position Statement on Sexual and Reproductive Health and Rights', 'oral', NULL, 3, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(15, 3, 'Ntombifuthi Ginindza', 'Ministry of Health', 'Eswatini Global School-based Student Health Survey (GSHS) 2025', 'oral', NULL, 4, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(16, 3, 'Shannon Ahumuza', 'Babies and Mothers Alive Foundation', 'Effect of Family-Oriented Dialogues on the Uptake of Postpartum Family Planning Methods among Adolescent Mothers in Rakai District, Uganda.', 'oral', NULL, 5, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(17, 4, 'ECSACONM', 'ECSACONM', 'The Collegiate Model: A Regional Best Practice for Specialist Training', 'oral', NULL, 1, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(18, 4, 'COSECSA', 'COSECSA', 'Health Workforce Needs and the Contribution of ECSA-CHS Colleges', 'oral', NULL, 2, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(19, 4, 'COECSA', 'COECSA', 'Accreditation of Training Facilities: Ensuring Quality and Standardization', 'oral', NULL, 3, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(20, 4, 'COSECSA', 'COSECSA', 'Digital Transformation in Specialist Training: E-Learning, E-Logbooks and E-Portfolios', 'oral', NULL, 4, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(21, 4, 'COECSA', 'COECSA', 'Quality Assurance Systems for Maintaining Regional Standards', 'oral', NULL, 5, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(22, 4, 'COSECSA', 'COSECSA', 'Regional Examination and Assessment Systems', 'oral', NULL, 6, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(23, 4, 'ECSACONM', 'ECSACONM', 'Research, Innovation, Mentorship and Regional Knowledge Exchange', 'oral', NULL, 7, 1, '2026-08-04 09:57:54', '2026-08-04 09:57:54'),
(24, 1, 'Filex Otieno', 'Kakamega County General Hospital', 'Effects of Antimicrobial Stewardship Interventions at a Level 5 Referral Hospital in Western Kenya: Analysis from Repeated Point Prevalence Surveys Conducted Between 2021–2025', 'oral', NULL, 1, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(25, 1, 'Enock Musungwini', 'Pangaea Zimbabwe', 'From Climate Action to One Health Intelligence: Multisectoral Task Teams Strengthening Climate-Health Resilience and AMR Preparedness in Rural Zimbabwe', 'oral', NULL, 2, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(26, 1, 'Jonathan Mayito', 'International Centre for Antimicrobial Resistance Solutions (ICARS)', 'Behaviourally Informed and Local Context-Tailored Stewardship to Optimize Antibiotic Use in Bloodstream and Urinary Tract Infections: Antimicrobial Stewardship Lessons from Zambia and Malawi', 'oral', NULL, 3, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(27, 1, 'Deborah Kamanga', 'Ministry of Health, Antimicrobial Resistance Coordinating Centre', 'Surveillance of Antifungal Resistance in Candida albicans Isolates from Vulvovaginal Candidiasis Patients in Malawi', 'oral', NULL, 4, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(28, 1, 'Joseph Chizimu', 'Zambia National Public Health Institute', 'Diagnostic Stewardship Trends and Antimicrobial Resistance Profiles of Bacteria Isolated in Zambia: A Five-Year Retrospective Study (2020–2024)', 'oral', NULL, 5, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(29, 1, 'Néhémie Nzoyikorera', 'National Public Health Institute, Ministry of Public Health, Burundi', 'Molecular Characterization of Extended-Spectrum Beta-Lactamase-Producing Enterobacterales Causing Urinary Tract Infections in Burundi', 'oral', NULL, 6, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(30, 5, 'Mabvuto Sinkala', 'National Health Insurance Management Authority (NHIMA)', 'Innovative Partnerships for Sustainable Health Financing and UHC: Lessons from NHIMA\'s Pilot Targeting Poor and Vulnerable Households in Zambia', 'oral', NULL, 1, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(31, 5, 'Clarence Bonaventure', 'The Benjamin William Mkapa Foundation', 'Financing Community Health Workers for Sustainability: Lessons from Tanzania\'s Transition Towards Institutionalized Community Health Financing', 'oral', NULL, 2, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(32, 5, 'Sandile Malambe', 'CHAI', 'Implementing a Digital Expenditure Tracking Tool to Strengthen Public Financial Management in Eswatini\'s Ministry of Health', 'oral', NULL, 3, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(33, 5, 'Nanyondo Aminah', 'FREO2 Foundation', 'From 51% Functionality to 96% Uptime: Government Adoption of a Private-Sector Oxygen-as-a-Service Innovation in Uganda', 'oral', NULL, 4, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(34, 5, 'Bindeeba Stephenson Dedrix', 'FREO2', 'The Investment Case for Bedside Oxygen-as-a-Service: Reducing Referrals, Cylinder Dependence and Recurrent Costs in Uganda', 'oral', NULL, 5, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(35, 5, 'Faith Nekabari Nfii', 'VillageReach', 'From Beneficiaries to Budget Shapers: Institutionalizing Community Co-Leadership for Sustainable Health Financing in Africa', 'oral', NULL, 6, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(36, 6, 'Sindy Matse', 'Ministry of Health', 'Lenacapavir PrEP Implementation in Eswatini: Early Lessons from Africa\'s First National Long-Acting Injectable HIV Prevention Programme', 'oral', NULL, 1, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(37, 6, 'Michael Muthamia', 'Jhpiego', 'From County Innovation to National Scale: Leveraging Heat-Stable Carbetocin to Advance Maternal Health Outcomes in Kenya', 'oral', NULL, 2, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(38, 6, 'Mashudu Mthethwa', 'Health Systems Trust', 'Documenting What Works: A National Repository of Good Practices for Health System Learning and Scale-Up in South Africa', 'oral', NULL, 3, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(39, 6, 'Menard Chihana', 'GOAL 3', 'The Neonatal Mortality Impact of the IMPALA Continuous Patient Monitoring and Decision Support System in Two NICUs in Malawi', 'oral', NULL, 4, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(40, 6, 'Shehnaz Alidina', 'University of Saskatchewan', 'Building Learning Health Systems in Tanzania: A National Assessment of Organizational Learning Capacity', 'oral', NULL, 5, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(41, 6, 'Rene Loewenson & Victor Nyamandi', 'TARSC/Regional Network for Equity in Health in East and Southern Africa (EQUINET)', 'Implementing the 2024 RHMC Resolution: Key Findings from Progress in Institutionalising and Implementing Health Impact Assessment in the Region', 'oral', NULL, 6, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(42, 7, 'Celani Nkambule', 'CHAI Eswatini', 'Healing the Whole Person: Integrating Mental Health and Psychosocial Support into HIV Care as a Pathway to Sustainable Treatment Outcomes in Eswatini', 'oral', NULL, 1, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(43, 7, 'Lorraine Murphy', 'Health Service Executive', 'Building Sustainable Quality Improvement Capacity Through Country-Led Partnership: Lessons from Tanzania', 'oral', NULL, 2, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(44, 7, 'Lindiwe Gumede', 'University of Johannesburg', 'Negotiating Allopathic and Traditional Health Knowledge: Allopathic Medicine Practitioners\' Accounts of Traditional Medicine Disclosure in Gauteng, South Africa', 'oral', NULL, 3, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(45, 7, 'Emmanuel Kowero', 'The Benjamin William Mkapa Foundation', 'Strengthening Quality of Care and Patient Safety in Clubfoot Management in Tanzania: Lessons from a National Integrated Quality Improvement Model', 'oral', NULL, 4, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(46, 7, 'Kaushik Ramaiya', 'Shree Hindu Mandal Hospital', 'Integrated Community-Based Care versus Facility-Based Integrated Care for People Living with HIV, Diabetes or Hypertension in Sub-Saharan Africa (INTE-COMM): A Multi-Country Cluster-Randomised Trial', 'oral', NULL, 5, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(47, 7, 'Japhet Daud', NULL, 'Transforming PrEP Monitoring Through a Real-Time Digital THPS Analytics System (TAS): Lessons from Tanzania Health Promotion Support (THPS) in Kigoma, Pwani, Shinyanga and Tanga Regions in Tanzania', 'oral', NULL, 6, 1, '2026-08-04 10:06:46', '2026-08-04 10:06:46'),
(48, 1, 'Yohannes Dugasa Feyisa', 'East, Central and Southern Africa Health Community (ECSA-HC)', 'Progress in Public Health Emergency Operations Centre Functionality: A Comparative Baseline and Endline Assessment in Burundi, Rwanda, and São Tomé and Príncipe', 'poster', NULL, 1, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(49, 1, 'Mohamed Mohamed', 'ECSA-HC', 'Strengthening IHR Core Capacities through Joint External Evaluation: Comparative Lessons from HEPRR-Supported Countries in the ECSA Region', 'poster', NULL, 2, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(50, 1, 'Benedict Pius Mushi', 'ECSA-HC', 'Multi-country Assessment of the Implementation of the International Health Regulations (2005) Core Capacities at High Volume International Airports in the East, West and Horn of African Region', 'poster', NULL, 3, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(51, 1, 'Thabile Luhlanga', 'Ministry of Health', 'Analysis of Screened Immunization Status Among Under-Five Children by Community Health Volunteers in Three Regions in Eswatini (2023–2024)', 'poster', NULL, 4, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(52, 1, 'Engy Saleh', 'Busara', 'Exploring Patient Demand and Pharmacist Provision of Antimicrobials in Kenya', 'poster', NULL, 5, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(53, 1, 'Chikwanda Chileshe', 'Zambia Public Health Institute – Antimicrobial Resistance Coordinating Committee', 'From Development to Implementation: Lessons Learned from Animal Health Standard Treatment Guidelines in Zambia', 'poster', NULL, 6, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(54, 1, 'Mike Nundwe', 'Zambia National Public Health Institute', 'Genomic Analysis of Fluoroquinolone-Resistant Shigella Species at the University Teaching Hospital in Lusaka, Zambia', 'poster', NULL, 7, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(55, 1, 'Loveness Sakalimbwe', 'Zambia National Public Health Institute', 'Trends in Antimicrobial Stewardship Implementation Scores Following Participation in the TEACH AMS ECHO Program Among Provincial Hospitals in Zambia', 'poster', NULL, 8, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(56, 2, 'Phetsile Ndabandaba', 'Palladium Data for Implementation', 'Strengthening CMIS–LIS Interoperability to Reduce Laboratory Turnaround Time: A Multi-Level Quality Improvement Approach in Eswatini', 'poster', NULL, 1, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(57, 2, 'Simbarashe Chiripashi', 'Palladium / Ministry of Health', 'Embedding Patient Safety into a National EMR: Locally Driven ART Regimen Validation in Eswatini\'s CMIS', 'poster', NULL, 2, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(58, 3, 'Sindisiwe Mnisi', 'University of Eswatini (BNSc), Lomahasha Clinic', 'Long-Acting Reversible Contraceptive Use Among Young Women in Eswatini', 'poster', NULL, 1, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(59, 3, 'Khetsiwe Maseko', 'University of Eswatini', 'Factors Associated with Viral Load Non-Suppression Among Adolescents in HIV Management Facilities in Eswatini', 'poster', NULL, 2, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(60, 5, 'Trymore Shoko', 'Midlands Diabetes Interest Group (MidDIG)', 'Impact-Driven Grassroots Partnerships and Task-Shifting: Pathways to Sustainable Diabetes Care', 'poster', NULL, 1, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(61, 5, 'Remmy Moshi', 'The Benjamin William Mkapa Foundation', 'Leveraging Private Sector Investment to Strengthen Human Resources for Health: Lessons from the Mkapa Fellows Scholarship Programme in Tanzania', 'poster', NULL, 2, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(62, 5, 'Zulisile Zulu', 'meo@malaria.org.sz', 'Mid-Term Review of Eswatini\'s National Malaria Elimination Strategic Plan 2024–2028: Progress, Gaps and Mitigation Strategies Towards Eswatini Free Malaria', 'poster', NULL, 3, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(63, 5, 'Blessing Mnguni', 'Ministry of Health, Eswatini', 'Strengthening Access to Medical Oxygen in Eswatini: Infrastructure Investments, Market Shaping, and Sustainable Health System Transformation', 'poster', NULL, 4, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(64, 5, 'Joyce Sibanda', 'Brave Hearts of Eswatini', 'Bridging Traditional and Modern Healthcare: Engaging Traditional Healers in Tuberculosis Case Detection in Eswatini', 'poster', NULL, 5, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(65, 6, 'Eban Saria', 'Ifakara Health Institute', 'Subnational Malaria Response Gaps: An Interactive Dashboard for Priority Setting in Eastern Africa', 'poster', NULL, 1, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(66, 6, 'Themba Matsebula', 'Young Heroes Organisation', 'Triple Elimination in Focus: Disparities and Missed Opportunities in HIV, Syphilis, and Hepatitis B Testing Among Lactating Young Mothers in Eswatini', 'poster', NULL, 2, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(67, 6, 'Mohamed Bahari', 'Ministry of Health, Songea Regional Referral Hospital, Ruvuma, Tanzania and Tanzania Monitoring and Evaluation Consultancy Chamber (TanMECC), Dodoma, Tanzania', 'Strengthening Monitoring and Evaluation Systems in Tanzania: Evidence from TanMECC\'s Multi-Intervention Approach', 'poster', NULL, 3, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(68, 6, 'Phumzile Kunene', 'Ministry of Health', 'Integrating HPV Vaccination into Teen Club Services to Improve Uptake Among Girls Living with HIV in Eswatini: Lessons from a Quality Improvement Initiative', 'poster', NULL, 4, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(69, 7, 'Bhekiwe Shongwe', 'Clinton Health Access Initiative (CHAI)', 'Integrating HPV Vaccine into Routine Immunization of Adolescents Living with HIV: Eliminating Vaccine Stigma by Improving Demand Creation and Strengthening Healthcare Workers\' Capacity', 'poster', NULL, 1, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(70, 7, 'Ntombifuthi Ginindza', 'Ministry of Health', 'From Awareness to Action: Scaling Up Diabetes Education, Screening, and Complication Management in Eswatini', 'poster', NULL, 2, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(71, 7, 'James Kengia', 'Prime Minister\'s Office Regional Administration and Local Government (PMORALG), Dodoma, Tanzania', 'Strengthening Health Care Leadership and Management Through a Bundled Intervention: Documenting Experiences from Two Rural Tanzanian Districts', 'poster', NULL, 3, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34'),
(72, 7, 'Lomanono Ngidie', 'AIDS Healthcare Foundation', 'Clinical Outcomes of Rapid Same-Day Treatment Initiation Among Patients Presenting with Advanced HIV Disease and Positive Urinary Lipoarabinomannan (TB-LAM) at AHF Matsapha Clinic, Eswatini', 'poster', NULL, 4, 1, '2026-08-04 12:08:34', '2026-08-04 12:08:34');

-- --------------------------------------------------------

--
-- Table structure for table `scores`
--

CREATE TABLE `scores` (
  `id` bigint UNSIGNED NOT NULL,
  `judge_id` bigint UNSIGNED NOT NULL,
  `presenter_id` bigint UNSIGNED NOT NULL,
  `overall_score` decimal(5,2) NOT NULL,
  `comments` text COLLATE utf8mb4_unicode_ci,
  `submitted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ;

--
-- Dumping data for table `scores`
--

INSERT INTO `scores` (`id`, `judge_id`, `presenter_id`, `overall_score`, `comments`, `submitted_at`, `updated_at`) VALUES
(3, 1, 7, 65.20, NULL, '2026-08-04 10:50:46', '2026-08-04 10:50:46'),
(4, 2, 7, 47.50, NULL, '2026-08-04 10:54:52', '2026-08-04 10:54:52'),
(5, 2, 6, 66.65, NULL, '2026-08-04 11:19:13', '2026-08-04 11:19:13'),
(6, 2, 69, 39.30, NULL, '2026-08-04 13:16:11', '2026-08-04 13:16:11'),
(7, 2, 50, 51.95, NULL, '2026-08-04 13:20:07', '2026-08-04 13:20:07'),
(8, 2, 30, 62.80, NULL, '2026-08-04 13:55:34', '2026-08-04 13:55:34'),
(9, 2, 1, 66.10, NULL, '2026-08-04 14:01:12', '2026-08-04 14:01:12'),
(10, 2, 53, 39.85, NULL, '2026-08-04 14:07:16', '2026-08-04 14:07:16'),
(11, 2, 65, 50.30, NULL, '2026-08-04 14:08:42', '2026-08-04 14:08:42'),
(12, 1, 9, 58.25, NULL, '2026-08-04 14:15:45', '2026-08-04 14:15:45'),
(13, 1, 55, 67.50, NULL, '2026-08-04 14:16:23', '2026-08-04 14:16:23'),
(14, 1, 50, 69.60, NULL, '2026-08-04 14:16:55', '2026-08-04 14:16:55'),
(15, 1, 29, 67.45, NULL, '2026-08-04 14:23:22', '2026-08-04 14:23:22'),
(16, 1, 64, 61.50, NULL, '2026-08-04 14:23:47', '2026-08-04 14:23:47'),
(17, 1, 1, 66.85, NULL, '2026-08-04 16:38:27', '2026-08-04 16:38:27');

-- --------------------------------------------------------

--
-- Table structure for table `score_items`
--

CREATE TABLE `score_items` (
  `id` bigint UNSIGNED NOT NULL,
  `score_id` bigint UNSIGNED NOT NULL,
  `criterion_id` smallint UNSIGNED NOT NULL,
  `score_value` decimal(5,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ;

--
-- Dumping data for table `score_items`
--

INSERT INTO `score_items` (`id`, `score_id`, `criterion_id`, `score_value`, `created_at`, `updated_at`) VALUES
(1, 3, 1, 100.00, '2026-08-04 10:50:46', '2026-08-04 10:50:46'),
(2, 3, 2, 100.00, '2026-08-04 10:50:46', '2026-08-04 10:50:46'),
(3, 3, 3, 34.00, '2026-08-04 10:50:46', '2026-08-04 10:50:46'),
(4, 3, 4, 54.00, '2026-08-04 10:50:46', '2026-08-04 10:50:46'),
(5, 3, 5, 43.00, '2026-08-04 10:50:46', '2026-08-04 10:50:46'),
(6, 4, 1, 43.00, '2026-08-04 10:54:52', '2026-08-04 10:54:52'),
(7, 4, 2, 34.00, '2026-08-04 10:54:52', '2026-08-04 10:54:52'),
(8, 4, 3, 34.00, '2026-08-04 10:54:52', '2026-08-04 10:54:52'),
(9, 4, 4, 100.00, '2026-08-04 10:54:52', '2026-08-04 10:54:52'),
(10, 4, 5, 43.00, '2026-08-04 10:54:52', '2026-08-04 10:54:52'),
(11, 5, 1, 45.00, '2026-08-04 11:19:13', '2026-08-04 11:19:13'),
(12, 5, 2, 56.00, '2026-08-04 11:19:13', '2026-08-04 11:19:13'),
(13, 5, 3, 100.00, '2026-08-04 11:19:13', '2026-08-04 11:19:13'),
(14, 5, 4, 61.00, '2026-08-04 11:19:13', '2026-08-04 11:19:13'),
(15, 5, 5, 46.00, '2026-08-04 11:19:13', '2026-08-04 11:19:13'),
(16, 5, 6, 100.00, '2026-08-04 11:19:13', '2026-08-04 11:19:13'),
(17, 5, 7, 47.00, '2026-08-04 11:19:13', '2026-08-04 11:19:13'),
(18, 8, 1, 43.00, '2026-08-04 13:55:34', '2026-08-04 13:55:34'),
(19, 8, 2, 43.00, '2026-08-04 13:55:34', '2026-08-04 13:55:34'),
(20, 8, 3, 100.00, '2026-08-04 13:55:34', '2026-08-04 13:55:34'),
(21, 8, 4, 100.00, '2026-08-04 13:55:34', '2026-08-04 13:55:34'),
(22, 8, 5, 10.00, '2026-08-04 13:55:34', '2026-08-04 13:55:34'),
(23, 8, 6, 46.00, '2026-08-04 13:55:34', '2026-08-04 13:55:34'),
(24, 8, 7, 43.00, '2026-08-04 13:55:34', '2026-08-04 13:55:34'),
(25, 9, 1, 100.00, '2026-08-04 14:01:12', '2026-08-04 14:01:12'),
(26, 9, 2, 52.00, '2026-08-04 14:01:12', '2026-08-04 14:01:12'),
(27, 9, 3, 100.00, '2026-08-04 14:01:12', '2026-08-04 14:01:12'),
(28, 9, 4, 53.00, '2026-08-04 14:01:12', '2026-08-04 14:01:12'),
(29, 9, 5, 2.00, '2026-08-04 14:01:12', '2026-08-04 14:01:12'),
(30, 9, 6, 25.00, '2026-08-04 14:01:12', '2026-08-04 14:01:12'),
(31, 9, 7, 100.00, '2026-08-04 14:01:12', '2026-08-04 14:01:12'),
(32, 12, 1, 54.00, '2026-08-04 14:15:45', '2026-08-04 14:15:45'),
(33, 12, 2, 25.00, '2026-08-04 14:15:45', '2026-08-04 14:15:45'),
(34, 12, 3, 65.00, '2026-08-04 14:15:45', '2026-08-04 14:15:45'),
(35, 12, 4, 85.00, '2026-08-04 14:15:45', '2026-08-04 14:15:45'),
(36, 12, 5, 54.00, '2026-08-04 14:15:45', '2026-08-04 14:15:45'),
(37, 12, 6, 45.00, '2026-08-04 14:15:45', '2026-08-04 14:15:45'),
(38, 12, 7, 65.00, '2026-08-04 14:15:45', '2026-08-04 14:15:45'),
(39, 15, 1, 45.00, '2026-08-04 14:23:22', '2026-08-04 14:23:22'),
(40, 15, 2, 100.00, '2026-08-04 14:23:22', '2026-08-04 14:23:22'),
(41, 15, 3, 54.00, '2026-08-04 14:23:22', '2026-08-04 14:23:22'),
(42, 15, 4, 54.00, '2026-08-04 14:23:22', '2026-08-04 14:23:22'),
(43, 15, 5, 65.00, '2026-08-04 14:23:22', '2026-08-04 14:23:22'),
(44, 15, 6, 76.00, '2026-08-04 14:23:22', '2026-08-04 14:23:22'),
(45, 15, 7, 100.00, '2026-08-04 14:23:22', '2026-08-04 14:23:22'),
(46, 17, 1, 85.00, '2026-08-04 16:38:27', '2026-08-04 16:38:27'),
(47, 17, 2, 90.00, '2026-08-04 16:38:27', '2026-08-04 16:38:27'),
(48, 17, 3, 65.00, '2026-08-04 16:38:27', '2026-08-04 16:38:27'),
(49, 17, 4, 32.00, '2026-08-04 16:38:27', '2026-08-04 16:38:27'),
(50, 17, 5, 56.00, '2026-08-04 16:38:27', '2026-08-04 16:38:27'),
(51, 17, 6, 98.00, '2026-08-04 16:38:27', '2026-08-04 16:38:27'),
(52, 17, 7, 58.00, '2026-08-04 16:38:27', '2026-08-04 16:38:27');

-- --------------------------------------------------------

--
-- Table structure for table `subthemes`
--

CREATE TABLE `subthemes` (
  `id` tinyint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `display_order` tinyint UNSIGNED NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `subthemes`
--

INSERT INTO `subthemes` (`id`, `name`, `display_order`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Health Security', 1, 1, '2026-08-03 21:30:41', '2026-08-04 09:23:40'),
(2, 'Digital Innovation', 2, 1, '2026-08-03 21:30:41', '2026-08-03 21:30:41'),
(3, 'Demographic Dividend', 3, 1, '2026-08-03 21:30:41', '2026-08-03 21:30:41'),
(4, 'Global Health Diplomacy', 4, 0, '2026-08-03 21:30:41', '2026-08-04 09:12:49'),
(5, 'Sustainable Financing', 5, 1, '2026-08-03 21:30:41', '2026-08-03 21:30:41'),
(6, 'Innovation, Health Research & Development', 6, 1, '2026-08-03 21:30:41', '2026-08-03 21:30:41'),
(7, 'Quality of Care & Patient Safety', 7, 1, '2026-08-03 21:30:41', '2026-08-03 21:30:41');

-- --------------------------------------------------------

--
-- Structure for view `presentation_score_summary`
--
DROP TABLE IF EXISTS `presentation_score_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `presentation_score_summary`  AS SELECT `p`.`id` AS `presenter_id`, `p`.`presenter_name` AS `presenter_name`, `p`.`institution` AS `institution`, `p`.`presentation_title` AS `presentation_title`, `st`.`id` AS `subtheme_id`, `st`.`name` AS `subtheme_name`, count(`s`.`id`) AS `number_of_judges`, round(avg(`s`.`overall_score`),2) AS `average_score`, round(min(`s`.`overall_score`),2) AS `minimum_score`, round(max(`s`.`overall_score`),2) AS `maximum_score` FROM ((`presenters` `p` join `subthemes` `st` on((`st`.`id` = `p`.`subtheme_id`))) left join `scores` `s` on((`s`.`presenter_id` = `p`.`id`))) GROUP BY `p`.`id`, `p`.`presenter_name`, `p`.`institution`, `p`.`presentation_title`, `st`.`id`, `st`.`name` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `administrators`
--
ALTER TABLE `administrators`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_administrators_email` (`email`);

--
-- Indexes for table `criteria`
--
ALTER TABLE `criteria`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_criteria_name` (`name`),
  ADD KEY `idx_criteria_active_order` (`is_active`,`display_order`);

--
-- Indexes for table `judges`
--
ALTER TABLE `judges`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_judges_email` (`email`);

--
-- Indexes for table `poster_criteria`
--
ALTER TABLE `poster_criteria`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `poster_score_items`
--
ALTER TABLE `poster_score_items`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_poster_score_criterion` (`score_id`,`criterion_id`),
  ADD KEY `fk_poster_score_items_criterion` (`criterion_id`);

--
-- Indexes for table `presenters`
--
ALTER TABLE `presenters`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_presenters_subtheme` (`subtheme_id`),
  ADD KEY `idx_presenters_active_order` (`subtheme_id`,`is_active`,`display_order`);

--
-- Indexes for table `scores`
--
ALTER TABLE `scores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_scores_judge_presenter` (`judge_id`,`presenter_id`),
  ADD KEY `idx_scores_presenter` (`presenter_id`),
  ADD KEY `idx_scores_submitted_at` (`submitted_at`);

--
-- Indexes for table `score_items`
--
ALTER TABLE `score_items`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_score_items_score_criterion` (`score_id`,`criterion_id`),
  ADD KEY `idx_score_items_criterion` (`criterion_id`);

--
-- Indexes for table `subthemes`
--
ALTER TABLE `subthemes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_subthemes_name` (`name`),
  ADD KEY `idx_subthemes_active_order` (`is_active`,`display_order`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `administrators`
--
ALTER TABLE `administrators`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `criteria`
--
ALTER TABLE `criteria`
  MODIFY `id` smallint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `judges`
--
ALTER TABLE `judges`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `poster_criteria`
--
ALTER TABLE `poster_criteria`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `poster_score_items`
--
ALTER TABLE `poster_score_items`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- AUTO_INCREMENT for table `presenters`
--
ALTER TABLE `presenters`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT for table `scores`
--
ALTER TABLE `scores`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `score_items`
--
ALTER TABLE `score_items`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `subthemes`
--
ALTER TABLE `subthemes`
  MODIFY `id` tinyint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `poster_score_items`
--
ALTER TABLE `poster_score_items`
  ADD CONSTRAINT `fk_poster_score_items_criterion` FOREIGN KEY (`criterion_id`) REFERENCES `poster_criteria` (`id`),
  ADD CONSTRAINT `fk_poster_score_items_score` FOREIGN KEY (`score_id`) REFERENCES `scores` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `presenters`
--
ALTER TABLE `presenters`
  ADD CONSTRAINT `fk_presenters_subtheme` FOREIGN KEY (`subtheme_id`) REFERENCES `subthemes` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Constraints for table `scores`
--
ALTER TABLE `scores`
  ADD CONSTRAINT `fk_scores_judge` FOREIGN KEY (`judge_id`) REFERENCES `judges` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_scores_presenter` FOREIGN KEY (`presenter_id`) REFERENCES `presenters` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Constraints for table `score_items`
--
ALTER TABLE `score_items`
  ADD CONSTRAINT `fk_score_items_criterion` FOREIGN KEY (`criterion_id`) REFERENCES `criteria` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_score_items_score` FOREIGN KEY (`score_id`) REFERENCES `scores` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
