CREATE DATABASE IF NOT EXISTS mydb;

USE mydb;

CREATE TABLE IF NOT EXISTS `imges` (
  `idimges` INT NOT NULL AUTO_INCREMENT,
  `url` VARCHAR(500) NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`idimges`)
);

CREATE TABLE IF NOT EXISTS `count` (
  `idcounter` INT NOT NULL AUTO_INCREMENT,
  `counter` INT NOT NULL,
  PRIMARY KEY (`idcounter`)
);

-- Insert an initial value for the counter
INSERT INTO `count` (`counter`) VALUES (0);

-- Insert image URLs and names
INSERT INTO `imges` (url, name) 
VALUES 
  ("https://www.chipublib.org/wp-content/uploads/sites/3/2022/09/36079964425_7b3042d5e1_k.jpg", "eminem"),
  ("https://i.scdn.co/image/ab6761610000e5eba00b11c129b27a88fc72f36b", "eminem"),
  ("https://ih1.redbubble.net/image.3270018746.5019/flat,750x,075,f-pad,750x1000,f8f8f8.jpg", "eminem"),
  ("https://www.aestheticwalldecor.com/cdn/shop/files/eminem-rap-rolling-stone-magazine-wall-art-poster-aesthetic-wall-decor.jpg?v=1692556007", "eminem");
