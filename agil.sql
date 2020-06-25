-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : Dim 14 juin 2020 à 08:48
-- Version du serveur :  10.4.11-MariaDB
-- Version de PHP : 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `agil`
--

DELIMITER $$
--
-- Fonctions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `GetPrixCarburant` (`id` INT(2)) RETURNS DECIMAL(10,3) BEGIN
  DECLARE price DEC(10,3);
  IF ( id IS NOT NULL ) THEN
      SELECT PrixCarburant INTO price from Citerne join carburant using(idCarburant) where idCiterne = id LIMIT 1;
   END IF;
  IF ( price Is NULL ) THEN
  SET price = 0;
      END IF;
RETURN price;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `absence`
--

CREATE TABLE `absence` (
  `idAbsence` int(11) NOT NULL,
  `idEmp` int(11) NOT NULL,
  `idGroupe` int(11) NOT NULL,
  `idStation` int(11) NOT NULL,
  `DateAbsence` date NOT NULL DEFAULT current_timestamp(),
  `DescAbsence` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `absence`
--

INSERT INTO `absence` (`idAbsence`, `idEmp`, `idGroupe`, `idStation`, `DateAbsence`, `DescAbsence`) VALUES
(1, 1, 1, 2, '2020-06-10', 'Zzazazsqs'),
(2, 4, 2, 2, '2020-06-10', 'Absence'),
(4, 3, 3, 2, '2020-06-10', 'Sasaa'),
(5, 3, 3, 2, '2020-06-09', 'Asasasa'),
(7, 5, 2, 2, '2020-06-11', 'Saassa'),
(8, 4, 1, 2, '2020-06-11', 'Azazaa');

-- --------------------------------------------------------

--
-- Structure de la table `carburant`
--

CREATE TABLE `carburant` (
  `idCarburant` int(11) NOT NULL,
  `NomCarburant` varchar(255) NOT NULL,
  `PrixCarburant` double(10,3) NOT NULL CHECK (`PrixCarburant` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `carburant`
--

INSERT INTO `carburant` (`idCarburant`, `NomCarburant`, `PrixCarburant`) VALUES
(1, 'Essence super sans plomb', 2.065),
(2, 'Gasoil Super', 1.825),
(3, 'Gasoil', 1.570);

-- --------------------------------------------------------

--
-- Structure de la table `citerne`
--

CREATE TABLE `citerne` (
  `idCiterne` int(11) NOT NULL,
  `NomCiterne` varchar(255) NOT NULL,
  `VolumeCiterne` double(10,3) NOT NULL CHECK (`VolumeCiterne` >= 0),
  `Val_Act_Citerne` double(10,3) NOT NULL CHECK (`VolumeCiterne` >= `Val_Act_Citerne`),
  `Min_Val_Citerne` varchar(255) NOT NULL,
  `EtatCiterne` tinyint(1) NOT NULL DEFAULT 1 CHECK (`EtatCiterne` = 0 or `EtatCiterne` = 1),
  `idCarburant` int(11) NOT NULL,
  `idStation` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `citerne`
--

INSERT INTO `citerne` (`idCiterne`, `NomCiterne`, `VolumeCiterne`, `Val_Act_Citerne`, `Min_Val_Citerne`, `EtatCiterne`, `idCarburant`, `idStation`) VALUES
(1, 'C01', 10000.000, 10000.000, '10', 1, 1, 2),
(2, 'C02', 10000.000, 900.000, '10', 1, 2, 2),
(3, 'C03', 10000.000, 10000.000, '10', 1, 2, 2),
(4, 'C04', 1000.000, 1000.000, '10', 1, 3, 2),
(5, 'C05', 10000.000, 10000.000, '10', 1, 2, 2),
(6, 'C06', 100.000, 100.000, '10', 1, 2, 2);

-- --------------------------------------------------------

--
-- Structure de la table `citerne_has_pompe`
--

CREATE TABLE `citerne_has_pompe` (
  `id_citerne_has_pompe` int(11) NOT NULL,
  `idCiterne` int(11) NOT NULL,
  `idPompe` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `citerne_has_pompe`
--

INSERT INTO `citerne_has_pompe` (`id_citerne_has_pompe`, `idCiterne`, `idPompe`) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 4, 1),
(5, 2, 2),
(6, 3, 2),
(7, 1, 2),
(8, 1, 3),
(9, 3, 3);

-- --------------------------------------------------------

--
-- Structure de la table `comments`
--

CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL,
  `comment_subject` varchar(255) NOT NULL,
  `comment_date` datetime NOT NULL DEFAULT current_timestamp(),
  `comment_text` varchar(255) NOT NULL,
  `comment_status` tinyint(1) NOT NULL DEFAULT 1,
  `idUser` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `comments`
--

INSERT INTO `comments` (`comment_id`, `comment_subject`, `comment_date`, `comment_text`, `comment_status`, `idUser`) VALUES
(25, 'C2', '2020-06-14 06:12:16', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam', 1, 2),
(26, 'C2', '2020-06-14 06:12:21', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam', 1, 2),
(27, 'C2', '2020-06-14 08:19:32', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam', 1, 2),
(28, 'C2', '2020-06-14 08:19:36', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam', 1, 2),
(29, 'C2', '2020-06-14 08:19:39', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam', 1, 2),
(30, 'C2', '2020-06-14 08:19:41', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam', 1, 2),
(31, 'C2', '2020-06-14 08:19:49', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam', 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `conge`
--

CREATE TABLE `conge` (
  `idConge` int(11) NOT NULL,
  `idEmp` int(11) NOT NULL,
  `idGroupe` int(11) NOT NULL,
  `idTypeConge` int(11) NOT NULL,
  `idStation` int(11) NOT NULL,
  `DateDebConge` date NOT NULL DEFAULT current_timestamp(),
  `DateFinConge` date NOT NULL,
  `DescConge` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `conge`
--

INSERT INTO `conge` (`idConge`, `idEmp`, `idGroupe`, `idTypeConge`, `idStation`, `DateDebConge`, `DateFinConge`, `DescConge`) VALUES
(1, 3, 3, 2, 2, '2020-06-20', '2020-06-24', '211'),
(2, 5, 2, 3, 2, '2020-06-10', '2020-06-11', 'Sasasa'),
(3, 5, 2, 2, 2, '2020-06-11', '2020-06-12', 'Sasas');

-- --------------------------------------------------------

--
-- Structure de la table `delegation`
--

CREATE TABLE `delegation` (
  `idDelegation` int(11) NOT NULL,
  `nomDelegation` varchar(255) NOT NULL,
  `idVille` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `delegation`
--

INSERT INTO `delegation` (`idDelegation`, `nomDelegation`, `idVille`) VALUES
(1, 'Carthage', 1),
(2, 'La Médina', 1),
(3, 'Bab Bhar', 1),
(4, 'Bab Souika', 1),
(5, 'Omrane', 1),
(6, 'Omrane Supérieur', 1),
(7, 'Attahrir', 1),
(8, 'El Menzah', 1),
(9, 'Cité Alkhadhra', 1),
(10, 'Bardo', 1),
(11, 'Séjoumi', 1),
(12, 'Azzouhour', 1),
(13, 'Alhrairia', 1),
(14, 'Sidi Hsine', 1),
(15, 'Ouardia', 1),
(16, 'Kabaria', 1),
(17, 'Sidi Elbéchir', 1),
(18, 'Jebel Jelloud', 1),
(19, 'La Goulette', 1),
(20, 'Le Kram', 1),
(21, 'La Marsa', 1),
(22, 'Ariana Ville', 2),
(23, 'Soukra', 2),
(24, 'Raouède', 2),
(25, 'Kalâat Andalous', 2),
(26, 'Sidi Thabet', 2),
(27, 'Cité Attadhamon', 2),
(28, 'Mnihla', 2),
(29, 'Manouba', 3),
(30, 'Oued Ellil', 3),
(31, 'Tebourba', 3),
(32, 'Battan', 3),
(33, 'Jedaida', 3),
(34, 'Mornaguia', 3),
(35, 'Borj Amri', 3),
(36, 'Douar Hicher', 3),
(37, 'Ben Arous', 4),
(38, 'Nouvelle Médina', 4),
(39, 'Mourouj', 4),
(40, 'Hammam Lif', 4),
(41, 'Hammam Chatt', 4),
(42, 'Boumhel Bassatine', 4),
(43, 'Ezzahra', 4),
(44, 'Radès', 4),
(45, 'Megrine', 4),
(46, 'Mhamdia', 4),
(47, 'Fouchana', 4),
(48, 'Mornag', 4),
(49, 'Nabeul', 5),
(50, 'Dar Chaâbane Elfehri', 5),
(51, 'Béni Khiar', 5),
(52, 'Korba', 5),
(53, 'Menzel Temime', 5),
(54, 'Mida', 5),
(55, 'Kelibia', 5),
(56, 'Hammam Ghezaz', 5),
(57, 'Haouaria', 5),
(58, 'Takelsa', 5),
(59, 'Slimane', 5),
(60, 'Menzel Bouzelfa', 5),
(61, 'Béni Khalled', 5),
(62, 'Grombalia', 5),
(63, 'Bouârgoub', 5),
(64, 'Hammamet', 5),
(65, 'Bizerte Nord', 6),
(66, 'Jarzouna', 6),
(67, 'Bizerte Sud', 6),
(68, 'Sejnane', 6),
(69, 'Joumine', 6),
(70, 'Mateur', 6),
(71, 'Ghezala', 6),
(72, 'Menzel Bourguiba', 6),
(73, 'Tinja', 6),
(74, 'Utique', 6),
(75, 'Ghar El Melh', 6),
(76, 'Menzel Jemil', 6),
(77, 'El Alia', 6),
(78, 'Ras Jebel', 6),
(79, 'Zaghouan', 7),
(80, 'Zériba', 7),
(81, 'Bir Mecharga', 7),
(82, 'Fahs', 7),
(83, 'Nadhour', 7),
(84, 'Saouaf', 7),
(85, 'Sousse Ville', 8),
(86, 'Zaouia Ksiba Thrayat', 8),
(87, 'Sousse Ryadh', 8),
(88, 'Sousse Jawhara', 8),
(89, 'Sousse Sidi Abdelhamid', 8),
(90, 'Hammam sousse', 8),
(91, 'Akouda', 8),
(92, 'Kalâa Elkébira', 8),
(93, 'Sidi Bouali', 8),
(94, 'Hergla', 8),
(95, 'Enfidha', 8),
(96, 'Bouficha', 8),
(97, 'Koundar', 8),
(98, 'Sidi Elheni', 8),
(99, 'Msaken', 8),
(100, 'Kalâa Ességhira', 8),
(101, 'Monastir', 9),
(102, 'Ouerdanine', 9),
(103, 'Sahline', 9),
(104, 'Zéramdine', 9),
(105, 'Béni Hassan', 9),
(106, 'Jammel', 9),
(107, 'Benbla', 9),
(108, 'Moknine', 9),
(109, 'Bekalta', 9),
(110, 'Teboulba', 9),
(111, 'Ksar Helal', 9),
(112, 'Ksibet Medyouni', 9),
(113, 'Sayada', 9),
(114, 'Lamta', 9),
(115, 'Bouhjar', 9),
(116, 'Mahdia', 10),
(117, 'Boumerdes', 10),
(118, 'Ouled Chamekh', 10),
(119, 'Chorbane', 10),
(120, 'Hbira', 10),
(121, 'Souassi', 10),
(122, 'Eljem', 10),
(123, 'Chebba', 10),
(124, 'Malloulech', 10),
(125, 'Sidi Alouane', 10),
(126, 'Ksour Essef', 10),
(127, 'Sfax Ville', 11),
(128, 'Sfax Ouest', 11),
(129, 'Sakiet Ezzit', 11),
(130, 'Sakiet Eddaier', 11),
(131, 'Sfax sud', 11),
(132, 'Tina', 11),
(133, 'Agareb', 11),
(134, 'Jebeniana', 11),
(135, 'El Amra', 11),
(136, 'El Hencha', 11),
(137, 'Menzel chaker', 11),
(138, 'Ghraiba', 11),
(139, 'Bir Ali Ben Khelifa', 11),
(140, 'Sekhira', 11),
(141, 'Mahrès', 11),
(142, 'Kerkennah', 11),
(143, 'Béja nord', 12),
(144, 'Béja sud', 12),
(145, 'Amdoun', 12),
(146, 'Nefza', 12),
(147, 'Teboursouk', 12),
(148, 'Tibar', 12),
(149, 'Testour', 12),
(150, 'Goubellat', 12),
(151, 'Mejez El Bab', 12),
(152, 'Jendouba', 13),
(153, 'Jendouba Nord', 13),
(154, 'Boussalem', 13),
(155, 'Tabarka', 13),
(156, 'Ain Drahem', 13),
(157, 'Fernana', 13),
(158, 'Ghardimaou', 13),
(159, 'Oued Mliz', 13),
(160, 'Balta Bouaouene', 13),
(161, 'Kef Ouest', 14),
(162, 'Kef Est', 14),
(163, 'Nebeur', 14),
(164, 'Sakiet Sidi Youssef', 14),
(165, 'Tejerouine', 14),
(166, 'Kalâat sinane', 14),
(167, 'Kalâa El khasba', 14),
(168, 'Jerissa', 14),
(169, 'Gsour', 14),
(170, 'Dahmani', 14),
(171, 'Le Sers', 14),
(172, 'Siliana nord', 15),
(173, 'Siliana sud', 15),
(174, 'Bouarada', 15),
(175, 'Gâafour', 15),
(176, 'El Aroussa', 15),
(177, 'Le Krib', 15),
(178, 'Bourouis', 15),
(179, 'Makther', 15),
(180, 'Rouhia', 15),
(181, 'Kesra', 15),
(182, 'Bargou', 15),
(183, 'Kairouan Nord', 16),
(184, 'Kairouan Sud', 16),
(185, 'Chebika', 16),
(186, 'Sebikha', 16),
(187, 'Oueslatia', 16),
(188, 'Haffouz', 16),
(189, 'El Ala', 16),
(190, 'Hajeb El Ayoun', 16),
(191, 'Nasrallah', 16),
(192, 'Cherarda', 16),
(193, 'Bouhajla', 16),
(194, 'Sidi Bouzid Ouest', 17),
(195, 'Sidi Bouzid Est', 17),
(196, 'Jelma', 17),
(197, 'Sabbalet Ouled Askar', 17),
(198, 'Bir Hfay', 17),
(199, 'Sidi Ali Benôun', 17),
(200, 'Menzel Bouzayane', 17),
(201, 'Meknassi', 17),
(202, 'Souk Jedid', 17),
(203, 'Mezouna', 17),
(204, 'Regueb', 17),
(205, 'Ouled Haffouz', 17),
(206, 'Kasserine Nord', 18),
(207, 'Kasserine Sud', 18),
(208, 'Azzouhour', 18),
(209, 'Hassi ferid', 18),
(210, 'Sbitla', 18),
(211, 'Sbiba', 18),
(212, 'Jedliane', 18),
(213, 'El Ayoun', 18),
(214, 'Tela', 18),
(215, 'Hidra', 18),
(216, 'Foussana', 18),
(217, 'Feriana', 18),
(218, 'Mejel Bel Abbes', 18),
(219, 'Gabès ville', 19),
(220, 'Gabès ouest', 19),
(221, 'Gabès sud', 19),
(222, 'Ghannouch', 19),
(223, 'Metouia', 19),
(224, 'Menzel habib', 19),
(225, 'Hamma', 19),
(226, 'Matmata', 19),
(227, 'Matmata nouvelle', 19),
(228, 'Mareth', 19),
(229, 'Mednine Nord', 20),
(230, 'Mednine Sud', 20),
(231, 'Béni khedach', 20),
(232, 'Ben Guerdene', 20),
(233, 'Zazis', 20),
(234, 'Jerba Houmet Souk', 20),
(235, 'Jerba Midoun', 20),
(236, 'Jerba Ajim', 20),
(237, 'Sidi Makhlouf', 20),
(238, 'Gafsa Nord', 21),
(239, 'Sidi Aich', 21),
(240, 'El Ksar', 21),
(241, 'Gafsa Sud', 21),
(242, 'Moulares', 21),
(243, 'Redyef', 21),
(244, 'Métlaoui', 21),
(245, 'El Mdhilla', 21),
(246, 'El Guettar', 21),
(247, 'Belkhir', 21),
(248, 'Sned', 21),
(249, 'Tozeur', 22),
(250, 'Degueche', 22),
(251, 'Tameghza', 22),
(252, 'Nefta', 22),
(253, 'Hezoua', 22),
(254, 'Tataouine Nord', 23),
(255, 'Tataouine Sud', 23),
(256, 'Smar', 23),
(257, 'Bir Lahmer', 23),
(258, 'Ghomrassen', 23),
(259, 'Dhehiba', 23),
(260, 'Remada', 23),
(261, 'Kébili Sud', 24),
(262, 'Kébili Nord', 24),
(263, 'Souk El Ahad', 24),
(264, 'Douz nord', 24),
(265, 'Douz sud', 24),
(266, 'El Faouar', 24);

-- --------------------------------------------------------

--
-- Structure de la table `employee`
--

CREATE TABLE `employee` (
  `idEmp` int(11) NOT NULL,
  `codeEmp` varchar(255) NOT NULL,
  `cinEmp` varchar(255) NOT NULL,
  `nomEmp` varchar(255) NOT NULL,
  `prenomEmp` varchar(255) NOT NULL,
  `dateEmp` date NOT NULL,
  `telEmp` varchar(255) NOT NULL,
  `salEmp` double(10,3) NOT NULL CHECK (`salEmp` > 0),
  `idGroupe` int(11) NOT NULL,
  `idRole` int(11) NOT NULL,
  `idStation` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `employee`
--

INSERT INTO `employee` (`idEmp`, `codeEmp`, `cinEmp`, `nomEmp`, `prenomEmp`, `dateEmp`, `telEmp`, `salEmp`, `idGroupe`, `idRole`, `idStation`) VALUES
(1, 'Xlszllkze', '83839898', 'Xxxx', 'Xxxx', '2020-06-10', '22333323', 100.000, 2, 1, 2),
(2, 'Xxxx0932', '89898998', 'Cxcxcx', 'Cxcxcx', '2020-06-10', '31212211', 1200.000, 2, 1, 2),
(3, 'Bghdhde98', '89889900', 'Zszdd', 'Dzzdz', '2020-06-10', '12112122', 1222.000, 2, 1, 2),
(4, 'Helmzez', '09390493', 'Dedeas', 'Dedeas', '2020-06-10', '23232232', 1900.000, 1, 1, 2),
(5, 'Xlszllkze2', '23232323', 'Mehri', 'Sadik', '2020-06-10', '23242312', 1000.000, 1, 2, 2);

-- --------------------------------------------------------

--
-- Structure de la table `expenses`
--

CREATE TABLE `expenses` (
  `idExpenses` int(11) NOT NULL,
  `dateExpenses` date NOT NULL DEFAULT current_timestamp(),
  `catExpenses` varchar(255) NOT NULL,
  `descExpenses` varchar(255) NOT NULL,
  `amExpenses` double(10,3) NOT NULL CHECK (`amExpenses` >= 0),
  `idStation` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `expenses`
--

INSERT INTO `expenses` (`idExpenses`, `dateExpenses`, `catExpenses`, `descExpenses`, `amExpenses`, `idStation`) VALUES
(1, '2020-06-11', 'Xxx', 'Xxxxx', 12.000, 2),
(2, '2020-06-11', 'Xxx', 'Xxxx', 12.000, 2),
(3, '2020-06-11', 'Sss Sss', 'Sasa Sasa', 12.000, 2),
(4, '2020-06-11', 'Xxx', 'Xxxx', 12.000, 2),
(5, '2020-06-10', 'Xxxx', 'Vf Cdcd', 12.000, 2),
(6, '2020-06-11', 'Bxbxb', 'Bxbxbx', 10.000, 2),
(7, '2020-05-06', 'Defefe', 'Sadaef', 21.000, 2);

-- --------------------------------------------------------

--
-- Structure de la table `groupe`
--

CREATE TABLE `groupe` (
  `idGroupe` int(11) NOT NULL,
  `NomGroupe` varchar(255) NOT NULL,
  `HeureDebut` varchar(255) NOT NULL,
  `HeureFin` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `groupe`
--

INSERT INTO `groupe` (`idGroupe`, `NomGroupe`, `HeureDebut`, `HeureFin`) VALUES
(1, 'Groupe 1', '06:00', '14:00'),
(2, 'Groupe 2', '14:00', '22:00'),
(3, 'Groupe 3', '22:00', '06:00');

-- --------------------------------------------------------

--
-- Structure de la table `lavage`
--

CREATE TABLE `lavage` (
  `idLavage` int(11) NOT NULL,
  `TypeLavage` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `lavage`
--

INSERT INTO `lavage` (`idLavage`, `TypeLavage`) VALUES
(1, 'Lavage automatique'),
(2, 'Lavage à haute pression');

-- --------------------------------------------------------

--
-- Structure de la table `listuser`
--

CREATE TABLE `listuser` (
  `idListUser` int(11) NOT NULL,
  `objListUser` varchar(255) NOT NULL,
  `dateListUser` date NOT NULL DEFAULT current_timestamp(),
  `stateListUser` tinyint(1) NOT NULL DEFAULT 1,
  `delListUser` tinyint(1) NOT NULL DEFAULT 1,
  `idUser` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `loguser`
--

CREATE TABLE `loguser` (
  `idLoginHist` int(11) NOT NULL,
  `srcIp` varchar(255) NOT NULL,
  `dateAttempt` datetime NOT NULL DEFAULT current_timestamp(),
  `statusAttempt` tinyint(1) NOT NULL,
  `descAttempt` varchar(255) NOT NULL,
  `idUser` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `loguser`
--

INSERT INTO `loguser` (`idLoginHist`, `srcIp`, `dateAttempt`, `statusAttempt`, `descAttempt`, `idUser`) VALUES
(1, '127.0.0.1', '2020-06-10 18:43:03', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(2, '127.0.0.1', '2020-06-10 18:45:18', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(3, '127.0.0.1', '2020-06-10 19:45:25', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(4, '127.0.0.1', '2020-06-10 19:53:04', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(5, '127.0.0.1', '2020-06-10 19:54:59', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(6, '127.0.0.1', '2020-06-10 20:00:25', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(7, '127.0.0.1', '2020-06-10 20:01:04', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(8, '127.0.0.1', '2020-06-10 20:24:01', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(9, '127.0.0.1', '2020-06-10 20:25:09', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(10, '127.0.0.1', '2020-06-10 20:32:17', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(11, '127.0.0.1', '2020-06-10 21:32:56', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(12, '127.0.0.1', '2020-06-10 21:33:41', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(13, '127.0.0.1', '2020-06-10 21:35:29', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(14, '127.0.0.1', '2020-06-10 21:40:04', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(15, '127.0.0.1', '2020-06-10 21:41:37', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(16, '127.0.0.1', '2020-06-10 21:43:52', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(17, '127.0.0.1', '2020-06-10 21:50:31', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(18, '127.0.0.1', '2020-06-10 21:56:52', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(19, '127.0.0.1', '2020-06-10 21:57:34', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(20, '127.0.0.1', '2020-06-10 21:59:48', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(21, '127.0.0.1', '2020-06-10 22:01:10', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(22, '127.0.0.1', '2020-06-10 22:03:15', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(23, '127.0.0.1', '2020-06-10 22:19:38', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(24, '127.0.0.1', '2020-06-10 22:21:06', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(25, '127.0.0.1', '2020-06-10 22:27:09', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(26, '127.0.0.1', '2020-06-10 22:35:50', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(27, '127.0.0.1', '2020-06-10 22:56:32', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(28, '127.0.0.1', '2020-06-10 23:51:23', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(29, '127.0.0.1', '2020-06-10 23:56:58', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(30, '127.0.0.1', '2020-06-11 00:07:06', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(31, '127.0.0.1', '2020-06-11 00:38:41', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(32, '127.0.0.1', '2020-06-11 00:45:43', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(33, '127.0.0.1', '2020-06-11 00:59:58', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(34, '127.0.0.1', '2020-06-11 01:20:18', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(35, '127.0.0.1', '2020-06-11 03:39:54', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(36, '127.0.0.1', '2020-06-11 04:28:06', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(37, '127.0.0.1', '2020-06-11 15:59:49', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(38, '127.0.0.1', '2020-06-11 17:03:01', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(39, '127.0.0.1', '2020-06-11 17:32:19', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(40, '127.0.0.1', '2020-06-11 19:37:51', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(41, '127.0.0.1', '2020-06-11 19:38:03', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(42, '127.0.0.1', '2020-06-11 19:38:49', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(43, '127.0.0.1', '2020-06-11 19:39:16', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(44, '127.0.0.1', '2020-06-11 19:39:35', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(45, '127.0.0.1', '2020-06-11 19:41:24', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(46, '127.0.0.1', '2020-06-11 19:44:30', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(47, '127.0.0.1', '2020-06-11 19:46:54', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(48, '127.0.0.1', '2020-06-11 19:52:50', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(49, '127.0.0.1', '2020-06-11 19:53:52', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(50, '127.0.0.1', '2020-06-11 19:54:56', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 1),
(51, '127.0.0.1', '2020-06-11 20:22:34', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 2),
(52, '127.0.0.1', '2020-06-13 21:21:18', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(53, '127.0.0.1', '2020-06-13 21:21:28', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(54, '127.0.0.1', '2020-06-13 21:37:58', 0, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(55, '127.0.0.1', '2020-06-12 21:38:08', 0, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(56, '127.0.0.1', '2020-06-13 21:38:34', 0, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(57, '127.0.0.1', '2020-06-13 21:38:52', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(58, '127.0.0.1', '2020-06-13 21:40:34', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(59, '127.0.0.1', '2020-06-13 21:43:04', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(60, '127.0.0.1', '2020-06-13 21:47:20', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(61, '127.0.0.1', '2020-06-13 21:52:04', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(62, '127.0.0.1', '2020-06-13 21:53:28', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(63, '127.0.0.1', '2020-06-13 21:54:41', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(64, '127.0.0.1', '2020-06-13 21:55:49', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(65, '127.0.0.1', '2020-06-13 21:57:48', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(66, '127.0.0.1', '2020-06-13 22:00:05', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(67, '127.0.0.1', '2020-06-13 22:06:43', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(68, '127.0.0.1', '2020-06-13 22:09:15', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(69, '127.0.0.1', '2020-06-13 22:11:30', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(70, '127.0.0.1', '2020-06-13 22:13:10', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(71, '127.0.0.1', '2020-06-13 22:14:02', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(72, '127.0.0.1', '2020-06-13 22:24:43', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(73, '127.0.0.1', '2020-06-13 22:26:39', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(74, '127.0.0.1', '2020-06-13 22:33:39', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(75, '127.0.0.1', '2020-06-13 22:34:35', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(76, '127.0.0.1', '2020-06-13 22:35:17', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(77, '127.0.0.1', '2020-06-13 22:36:31', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(78, '127.0.0.1', '2020-06-13 23:18:07', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(79, '127.0.0.1', '2020-06-13 23:44:10', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(80, '127.0.0.1', '2020-06-14 00:45:42', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(81, '127.0.0.1', '2020-06-14 00:47:01', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(82, '127.0.0.1', '2020-06-14 01:17:44', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(83, '127.0.0.1', '2020-06-14 07:40:38', 0, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(84, '127.0.0.1', '2020-06-14 07:40:50', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2),
(85, '127.0.0.1', '2020-06-14 08:23:56', 1, 'windows Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 2);

-- --------------------------------------------------------

--
-- Structure de la table `pompe`
--

CREATE TABLE `pompe` (
  `idPompe` int(11) NOT NULL,
  `NomPompe` varchar(255) NOT NULL,
  `EtatPompe` tinyint(1) NOT NULL DEFAULT 1 CHECK (`EtatPompe` = 0 or `EtatPompe` = 1),
  `idStation` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `pompe`
--

INSERT INTO `pompe` (`idPompe`, `NomPompe`, `EtatPompe`, `idStation`) VALUES
(1, 'Pompe01', 1, 2),
(2, 'Pompe02', 1, 2),
(3, 'Pompe03', 1, 2),
(4, 'Pompe04', 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `recettecarburant`
--

CREATE TABLE `recettecarburant` (
  `idRecetteCarburant` int(11) NOT NULL,
  `idPompe` int(11) NOT NULL,
  `idCiterne` int(11) NOT NULL,
  `idVoie` int(11) NOT NULL,
  `idStation` int(11) NOT NULL,
  `idGroupe` int(11) NOT NULL,
  `DateCarb` date NOT NULL DEFAULT current_timestamp(),
  `indiceDeb` double(10,0) NOT NULL CHECK (`indiceDeb` >= 0),
  `indiceFin` double(10,0) NOT NULL CHECK (`indiceFin` >= `indiceDeb`),
  `prixLitre` double(10,3) NOT NULL CHECK (`prixLitre` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `recettecarburant`
--

INSERT INTO `recettecarburant` (`idRecetteCarburant`, `idPompe`, `idCiterne`, `idVoie`, `idStation`, `idGroupe`, `DateCarb`, `indiceDeb`, `indiceFin`, `prixLitre`) VALUES
(2, 1, 2, 1, 2, 2, '2020-06-13', 0, 100, 1.825),
(3, 1, 2, 1, 2, 1, '2020-06-14', 0, 9000, 1.825);

-- --------------------------------------------------------

--
-- Structure de la table `recettelavage`
--

CREATE TABLE `recettelavage` (
  `idRecetteLavage` int(11) NOT NULL,
  `MatriculeVoiture` varchar(255) NOT NULL,
  `Kilometrage` varchar(255) NOT NULL,
  `HeureDebut` varchar(255) NOT NULL,
  `HeureFin` varchar(255) NOT NULL,
  `DateLavage` date NOT NULL DEFAULT current_timestamp(),
  `PrixLavage` double(10,3) NOT NULL CHECK (`PrixLavage` > 0),
  `idLavage` int(11) NOT NULL,
  `idGroupe` int(11) NOT NULL,
  `idStation` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `recettelavage`
--

INSERT INTO `recettelavage` (`idRecetteLavage`, `MatriculeVoiture`, `Kilometrage`, `HeureDebut`, `HeureFin`, `DateLavage`, `PrixLavage`, `idLavage`, `idGroupe`, `idStation`) VALUES
(1, '121-TUN-2112', '122', '00:39', '00:40', '2020-06-11', 12.000, 1, 2, 2),
(2, '121-TUN-2112', '323', '00:40', '00:40', '2020-06-11', 12.000, 1, 1, 2),
(3, '121-TUN-2112', '131', '00:40', '00:40', '2020-06-11', 12.000, 1, 3, 2),
(4, '120-TUN-2112', '123', '00:40', '00:40', '2020-06-11', 12.000, 2, 1, 2),
(5, '120-TUN-2112', '123', '00:41', '00:41', '2020-06-10', 12.000, 2, 1, 2),
(6, '120-TUN-2112', '122', '00:43', '00:43', '2020-06-10', 12.000, 1, 2, 2),
(7, '120-TUN-2112', '12', '00:44', '00:44', '2020-06-11', 12.000, 1, 3, 2),
(8, '120-TUN-2112', '12', '00:46', '00:46', '2020-06-10', 12.000, 1, 3, 2),
(9, '120-TUN-2112', '12', '00:46', '00:46', '2020-06-11', 12.000, 1, 1, 2),
(10, '120-TUN-2112', '123', '00:46', '00:46', '2020-06-10', 12.000, 1, 1, 2),
(11, '120-TUN-2110', '12', '12:48', '12:48', '2020-06-11', 12.000, 1, 1, 2),
(12, '120-TUN-2110', '12', '00:48', '00:48', '2020-06-11', 12.000, 1, 2, 2),
(13, '120-TUN-2112', '12', '04:09', '04:09', '2020-06-11', 12.000, 1, 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `role`
--

CREATE TABLE `role` (
  `idRole` int(11) NOT NULL,
  `NomRole` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `role`
--

INSERT INTO `role` (`idRole`, `NomRole`) VALUES
(1, 'Pompiste'),
(2, 'Opérateur de station de lavage');

-- --------------------------------------------------------

--
-- Structure de la table `station`
--

CREATE TABLE `station` (
  `idStation` int(11) NOT NULL,
  `NomStation` varchar(255) NOT NULL,
  `AdrStation` varchar(255) NOT NULL,
  `idDelegation` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `station`
--

INSERT INTO `station` (`idStation`, `NomStation`, `AdrStation`, `idDelegation`) VALUES
(1, 'Station : Tunis', 'Cite Olympique', 8),
(2, 'Station : Hammam-lif', 'Gp1 Hammam-lif', 37);

-- --------------------------------------------------------

--
-- Structure de la table `typeconge`
--

CREATE TABLE `typeconge` (
  `idTypeConge` int(11) NOT NULL,
  `typeConge` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `typeconge`
--

INSERT INTO `typeconge` (`idTypeConge`, `typeConge`) VALUES
(1, ' Les congés payés'),
(2, ' Les congés pour événements familiaux'),
(3, 'Les congés liés à un enfant');

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `idUser` int(11) NOT NULL,
  `codeUser` varchar(255) NOT NULL,
  `roleUser` tinyint(1) NOT NULL DEFAULT 0,
  `cinUser` varchar(255) NOT NULL,
  `emailUser` varchar(255) NOT NULL,
  `nomUser` varchar(255) NOT NULL,
  `prenomUser` varchar(255) NOT NULL,
  `dateUser` date NOT NULL,
  `telUser` varchar(255) NOT NULL,
  `passUser` varchar(255) NOT NULL DEFAULT '$2b$12$VILP2t3.JdQzbSx4qZ7jn.8dzueDJYjx12pJMoj/4ORyFRzPHkFY6',
  `resetTokenUser` varchar(255) NOT NULL DEFAULT '''0''',
  `createCompte` date NOT NULL DEFAULT current_timestamp(),
  `expiryCompte` date NOT NULL,
  `nbrAttempts` int(1) NOT NULL DEFAULT 3 CHECK (`nbrAttempts` >= 0),
  `etatCompte` tinyint(1) NOT NULL DEFAULT 1 CHECK (`etatCompte` = 0 or `etatCompte` = 1),
  `idStation` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`idUser`, `codeUser`, `roleUser`, `cinUser`, `emailUser`, `nomUser`, `prenomUser`, `dateUser`, `telUser`, `passUser`, `resetTokenUser`, `createCompte`, `expiryCompte`, `nbrAttempts`, `etatCompte`, `idStation`) VALUES
(1, 'K0RUGW', 1, '14000087', 'sadek12@gmail.com', 'Sadek', 'Mehri', '1200-10-19', '12345678', '$2b$12$VILP2t3.JdQzbSx4qZ7jn.8dzueDJYjx12pJMoj/4ORyFRzPHkFY6', '0', '2020-04-23', '2020-07-03', 3, 1, 1),
(2, 'K0RUGWF', 0, '14000000', 'xxx@gmail.com', 'Jhonny', 'Sin', '2020-06-12', '14000000', '$2b$12$VILP2t3.JdQzbSx4qZ7jn.8dzueDJYjx12pJMoj/4ORyFRzPHkFY6', '0', '2020-05-02', '2020-07-09', 2, 1, 2),
(5, 'sklaklsa', 0, '90209109', 'salsas@gmaz.com', 'Jhonny', 'Sins', '2020-05-09', '20912910', '$2b$12$VILP2t3.JdQzbSx4qZ7jn.8dzueDJYjx12pJMoj/4ORyFRzPHkFY6', '0', '2020-05-09', '2020-07-09', 3, 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `ville`
--

CREATE TABLE `ville` (
  `idVille` int(11) NOT NULL,
  `NomVille` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `ville`
--

INSERT INTO `ville` (`idVille`, `NomVille`) VALUES
(2, 'Ariana'),
(12, 'Béja'),
(4, 'Ben Arous'),
(6, 'Bizerte'),
(19, 'Gabès'),
(21, 'Gafsa'),
(13, 'Jendouba'),
(16, 'Kairouan'),
(18, 'Kasserine'),
(24, 'Kébili'),
(14, 'Kef'),
(10, 'Mahdia'),
(3, 'Manouba'),
(20, 'Medenine'),
(9, 'Monastir'),
(5, 'Nabeul'),
(11, 'Sfax'),
(17, 'Sidi Bouzid'),
(15, 'Siliana'),
(8, 'Sousse'),
(23, 'Tataouine'),
(22, 'Tozeur'),
(1, 'Tunis'),
(7, 'Zaghouan');

-- --------------------------------------------------------

--
-- Structure de la table `voie`
--

CREATE TABLE `voie` (
  `idVoie` int(11) NOT NULL,
  `nomVoie` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `voie`
--

INSERT INTO `voie` (`idVoie`, `nomVoie`) VALUES
(1, 'Voie 1'),
(2, 'Voie 2');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `absence`
--
ALTER TABLE `absence`
  ADD PRIMARY KEY (`idAbsence`),
  ADD KEY `FK_Absence_Employee_Groupe` (`idGroupe`),
  ADD KEY `FK_Absence_Station` (`idStation`),
  ADD KEY `FK_Employee_Absence` (`idEmp`);

--
-- Index pour la table `carburant`
--
ALTER TABLE `carburant`
  ADD PRIMARY KEY (`idCarburant`);

--
-- Index pour la table `citerne`
--
ALTER TABLE `citerne`
  ADD PRIMARY KEY (`idCiterne`),
  ADD KEY `fk_Citerne_Carburant` (`idCarburant`),
  ADD KEY `fk_Citerne_Station` (`idStation`);

--
-- Index pour la table `citerne_has_pompe`
--
ALTER TABLE `citerne_has_pompe`
  ADD PRIMARY KEY (`id_citerne_has_pompe`),
  ADD KEY `fk_citerne_pompe` (`idCiterne`),
  ADD KEY `fk_pompe_citerne` (`idPompe`);

--
-- Index pour la table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_id`),
  ADD KEY `FK_CommentUser` (`idUser`);

--
-- Index pour la table `conge`
--
ALTER TABLE `conge`
  ADD PRIMARY KEY (`idConge`),
  ADD KEY `FK_Employee_Absence` (`idEmp`),
  ADD KEY `FK_Employee_Groupe_Absence` (`idGroupe`),
  ADD KEY `FK_Absence_Station` (`idStation`),
  ADD KEY `FK_TypeConge_Conge` (`idTypeConge`);

--
-- Index pour la table `delegation`
--
ALTER TABLE `delegation`
  ADD PRIMARY KEY (`idDelegation`),
  ADD KEY `FK_VilleDelegation` (`idVille`);

--
-- Index pour la table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`idEmp`),
  ADD UNIQUE KEY `codeEmp` (`codeEmp`),
  ADD UNIQUE KEY `cinEmp` (`cinEmp`),
  ADD KEY `FK_Employee_Groupe` (`idGroupe`),
  ADD KEY `FK_Employee_Role` (`idRole`),
  ADD KEY `FK_Employee_Station` (`idStation`);

--
-- Index pour la table `expenses`
--
ALTER TABLE `expenses`
  ADD PRIMARY KEY (`idExpenses`),
  ADD KEY `fk_expenses_Station` (`idStation`);

--
-- Index pour la table `groupe`
--
ALTER TABLE `groupe`
  ADD PRIMARY KEY (`idGroupe`);

--
-- Index pour la table `lavage`
--
ALTER TABLE `lavage`
  ADD PRIMARY KEY (`idLavage`);

--
-- Index pour la table `listuser`
--
ALTER TABLE `listuser`
  ADD PRIMARY KEY (`idListUser`) USING BTREE,
  ADD KEY `FK_UserList` (`idUser`) USING BTREE;

--
-- Index pour la table `loguser`
--
ALTER TABLE `loguser`
  ADD PRIMARY KEY (`idLoginHist`),
  ADD KEY `login_user` (`idUser`);

--
-- Index pour la table `pompe`
--
ALTER TABLE `pompe`
  ADD PRIMARY KEY (`idPompe`),
  ADD KEY `fk_Pompe_Station` (`idStation`);

--
-- Index pour la table `recettecarburant`
--
ALTER TABLE `recettecarburant`
  ADD PRIMARY KEY (`idRecetteCarburant`),
  ADD KEY `fk_RecetteCarburant_Station` (`idStation`),
  ADD KEY `fk_RecetteCarburant_Citerne` (`idCiterne`),
  ADD KEY `fk_RecetteCarburant_Groupe` (`idGroupe`),
  ADD KEY `fk_RecetteCarburant_Pompe` (`idPompe`),
  ADD KEY `fk_RecetteCarburant_Voie` (`idVoie`);

--
-- Index pour la table `recettelavage`
--
ALTER TABLE `recettelavage`
  ADD PRIMARY KEY (`idRecetteLavage`),
  ADD KEY `fk_RecetteLavage_Groupe` (`idGroupe`),
  ADD KEY `fk_RecetteLavage_Station` (`idStation`),
  ADD KEY `fk_recettelavage_Lavage` (`idLavage`);

--
-- Index pour la table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`idRole`);

--
-- Index pour la table `station`
--
ALTER TABLE `station`
  ADD PRIMARY KEY (`idStation`),
  ADD KEY `fk_Station_Delegation` (`idDelegation`);

--
-- Index pour la table `typeconge`
--
ALTER TABLE `typeconge`
  ADD PRIMARY KEY (`idTypeConge`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`idUser`),
  ADD UNIQUE KEY `codeUser` (`codeUser`) USING BTREE,
  ADD UNIQUE KEY `cinUser` (`cinUser`) USING BTREE,
  ADD UNIQUE KEY `telUser` (`telUser`) USING BTREE,
  ADD UNIQUE KEY `emailUser` (`emailUser`) USING BTREE,
  ADD KEY `FK_User_Station` (`idStation`) USING BTREE;

--
-- Index pour la table `ville`
--
ALTER TABLE `ville`
  ADD PRIMARY KEY (`idVille`),
  ADD UNIQUE KEY `NomVille` (`NomVille`);

--
-- Index pour la table `voie`
--
ALTER TABLE `voie`
  ADD PRIMARY KEY (`idVoie`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `absence`
--
ALTER TABLE `absence`
  MODIFY `idAbsence` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `carburant`
--
ALTER TABLE `carburant`
  MODIFY `idCarburant` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `citerne`
--
ALTER TABLE `citerne`
  MODIFY `idCiterne` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `citerne_has_pompe`
--
ALTER TABLE `citerne_has_pompe`
  MODIFY `id_citerne_has_pompe` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT pour la table `comments`
--
ALTER TABLE `comments`
  MODIFY `comment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT pour la table `conge`
--
ALTER TABLE `conge`
  MODIFY `idConge` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `delegation`
--
ALTER TABLE `delegation`
  MODIFY `idDelegation` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=267;

--
-- AUTO_INCREMENT pour la table `employee`
--
ALTER TABLE `employee`
  MODIFY `idEmp` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `expenses`
--
ALTER TABLE `expenses`
  MODIFY `idExpenses` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT pour la table `groupe`
--
ALTER TABLE `groupe`
  MODIFY `idGroupe` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `lavage`
--
ALTER TABLE `lavage`
  MODIFY `idLavage` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `listuser`
--
ALTER TABLE `listuser`
  MODIFY `idListUser` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `loguser`
--
ALTER TABLE `loguser`
  MODIFY `idLoginHist` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=86;

--
-- AUTO_INCREMENT pour la table `pompe`
--
ALTER TABLE `pompe`
  MODIFY `idPompe` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `recettecarburant`
--
ALTER TABLE `recettecarburant`
  MODIFY `idRecetteCarburant` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `recettelavage`
--
ALTER TABLE `recettelavage`
  MODIFY `idRecetteLavage` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT pour la table `role`
--
ALTER TABLE `role`
  MODIFY `idRole` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `station`
--
ALTER TABLE `station`
  MODIFY `idStation` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `typeconge`
--
ALTER TABLE `typeconge`
  MODIFY `idTypeConge` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `idUser` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `ville`
--
ALTER TABLE `ville`
  MODIFY `idVille` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT pour la table `voie`
--
ALTER TABLE `voie`
  MODIFY `idVoie` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `absence`
--
ALTER TABLE `absence`
  ADD CONSTRAINT `FK_Absence_Employee_Groupe` FOREIGN KEY (`idGroupe`) REFERENCES `groupe` (`idGroupe`),
  ADD CONSTRAINT `FK_Absence_Station` FOREIGN KEY (`idStation`) REFERENCES `station` (`idStation`),
  ADD CONSTRAINT `FK_Employee_Absence` FOREIGN KEY (`idEmp`) REFERENCES `employee` (`idEmp`);

--
-- Contraintes pour la table `citerne`
--
ALTER TABLE `citerne`
  ADD CONSTRAINT `fk_Citerne_Carburant` FOREIGN KEY (`idCarburant`) REFERENCES `carburant` (`idCarburant`),
  ADD CONSTRAINT `fk_Citerne_Station` FOREIGN KEY (`idStation`) REFERENCES `station` (`idStation`);

--
-- Contraintes pour la table `citerne_has_pompe`
--
ALTER TABLE `citerne_has_pompe`
  ADD CONSTRAINT `fk_citerne_pompe` FOREIGN KEY (`idCiterne`) REFERENCES `citerne` (`idCiterne`),
  ADD CONSTRAINT `fk_pompe_citerne` FOREIGN KEY (`idPompe`) REFERENCES `pompe` (`idPompe`);

--
-- Contraintes pour la table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `FK_CommentUser` FOREIGN KEY (`idUser`) REFERENCES `user` (`idUser`);

--
-- Contraintes pour la table `conge`
--
ALTER TABLE `conge`
  ADD CONSTRAINT `FK_Conge_Station` FOREIGN KEY (`idStation`) REFERENCES `station` (`idStation`),
  ADD CONSTRAINT `FK_Employee_Conge` FOREIGN KEY (`idEmp`) REFERENCES `employee` (`idEmp`),
  ADD CONSTRAINT `FK_Employee_Groupe_Absence` FOREIGN KEY (`idGroupe`) REFERENCES `groupe` (`idGroupe`),
  ADD CONSTRAINT `FK_TypeConge_Conge` FOREIGN KEY (`idTypeConge`) REFERENCES `typeconge` (`idTypeConge`);

--
-- Contraintes pour la table `delegation`
--
ALTER TABLE `delegation`
  ADD CONSTRAINT `FK_VilleDelegation` FOREIGN KEY (`idVille`) REFERENCES `ville` (`idVille`);

--
-- Contraintes pour la table `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `FK_Employee_Groupe` FOREIGN KEY (`idGroupe`) REFERENCES `groupe` (`idGroupe`),
  ADD CONSTRAINT `FK_Employee_Role` FOREIGN KEY (`idRole`) REFERENCES `role` (`idRole`),
  ADD CONSTRAINT `FK_Employee_Station` FOREIGN KEY (`idStation`) REFERENCES `station` (`idStation`);

--
-- Contraintes pour la table `expenses`
--
ALTER TABLE `expenses`
  ADD CONSTRAINT `fk_expenses_Station` FOREIGN KEY (`idStation`) REFERENCES `station` (`idStation`);

--
-- Contraintes pour la table `listuser`
--
ALTER TABLE `listuser`
  ADD CONSTRAINT `FK_UserList` FOREIGN KEY (`idUser`) REFERENCES `user` (`idUser`);

--
-- Contraintes pour la table `loguser`
--
ALTER TABLE `loguser`
  ADD CONSTRAINT `login_user` FOREIGN KEY (`idUser`) REFERENCES `user` (`idUser`);

--
-- Contraintes pour la table `pompe`
--
ALTER TABLE `pompe`
  ADD CONSTRAINT `fk_Pompe_Station` FOREIGN KEY (`idStation`) REFERENCES `station` (`idStation`);

--
-- Contraintes pour la table `recettecarburant`
--
ALTER TABLE `recettecarburant`
  ADD CONSTRAINT `fk_RecetteCarburant_Citerne` FOREIGN KEY (`idCiterne`) REFERENCES `citerne` (`idCiterne`),
  ADD CONSTRAINT `fk_RecetteCarburant_Groupe` FOREIGN KEY (`idGroupe`) REFERENCES `groupe` (`idGroupe`),
  ADD CONSTRAINT `fk_RecetteCarburant_Pompe` FOREIGN KEY (`idPompe`) REFERENCES `pompe` (`idPompe`),
  ADD CONSTRAINT `fk_RecetteCarburant_Station` FOREIGN KEY (`idStation`) REFERENCES `station` (`idStation`),
  ADD CONSTRAINT `fk_RecetteCarburant_Voie` FOREIGN KEY (`idVoie`) REFERENCES `voie` (`idVoie`);

--
-- Contraintes pour la table `recettelavage`
--
ALTER TABLE `recettelavage`
  ADD CONSTRAINT `fk_RecetteLavage_Groupe` FOREIGN KEY (`idGroupe`) REFERENCES `groupe` (`idGroupe`),
  ADD CONSTRAINT `fk_RecetteLavage_Station` FOREIGN KEY (`idStation`) REFERENCES `station` (`idStation`),
  ADD CONSTRAINT `fk_recettelavage_Lavage` FOREIGN KEY (`idLavage`) REFERENCES `lavage` (`idLavage`);

--
-- Contraintes pour la table `station`
--
ALTER TABLE `station`
  ADD CONSTRAINT `fk_Station_Delegation` FOREIGN KEY (`idDelegation`) REFERENCES `delegation` (`idDelegation`);

--
-- Contraintes pour la table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `FK_User_Station` FOREIGN KEY (`idStation`) REFERENCES `station` (`idStation`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
