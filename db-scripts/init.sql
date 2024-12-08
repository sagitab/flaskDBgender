CREATE TABLE IF NOT EXISTS `imges` (
  `idimges` INT NOT NULL AUTO_INCREMENT,
  `url` VARCHAR(500) NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`idimges`)
);

INSERT INTO `imges` (url, name) 
VALUES 
  ("https://www.chipublib.org/wp-content/uploads/sites/3/2022/09/36079964425_7b3042d5e1_k.jpg", "eminem");
