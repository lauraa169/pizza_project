DROP TABLE IF EXISTS Discount;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS `Order`;
DROP TABLE IF EXISTS Drink;
DROP TABLE IF EXISTS Dessert;
DROP TABLE IF EXISTS Order_Extras;
DROP TABLE IF EXISTS Ingredient;
DROP TABLE IF EXISTS Pizza;
DROP TABLE IF EXISTS Pizza_Ingredient;
DROP TABLE IF EXISTS Order_Pizza;

CREATE TABLE Discount (
  `Discount_Code` BIGINT,
  `Percent` BIGINT CHECK (`Percent` >= 0 AND `Percent` <= 100),
  `Redeemed` BOOLEAN NOT NULL,
  PRIMARY KEY (`Discount_Code`)
);

CREATE TABLE `Customer` (
  `Customer_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Customer_Name` TEXT NOT NULL,
  `Customer_Surname` TEXT NOT NULL,
  `Birth_Date` DATE NOT NULL,
  `Customer_Address` TEXT NOT NULL,
  `Customer_Postal_Code` TEXT NOT NULL,
  `Credit_Card` BIGINT NOT NULL,
  `Customer_Email` TEXT NOT NULL,
  `Phone_Number` BIGINT NOT NULL,
  `Pizzas_Ordered` INT NOT NULL
);

CREATE TABLE `Staff` (
  `Staff_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Name` TEXT NOT NULL,
  `Surname` TEXT NOT NULL,
  `Bank_Account` TEXT NOT NULL,
  `Liscence` INT NOT NULL,
  `Postal_Code` TEXT NOT NULL,
  `Availability` BOOLEAN NOT NULL
);

CREATE TABLE `Order` (
  `Order_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Customer_ID` BIGINT NOT NULL,
  `Delivery_Person` BIGINT NOT NULL,
  `Discount_Code` BIGINT,
  `Order_Address` TEXT NOT NULL,
  `Order_Postal_Code` TEXT NOT NULL,
  `Order_Time` DATETIME NOT NULL,
  `Order_Price` BIGINT NOT NULL,
  `Delivered` BOOLEAN NOT NULL,
  FOREIGN KEY (`Discount_Code`) REFERENCES `Discount`(`Discount_Code`),
  FOREIGN KEY (`Customer_ID`) REFERENCES `Customer` (`Customer_ID`),
  FOREIGN KEY (`Delivery_Person`) REFERENCES `Staff` (`Staff_ID`)
  );

CREATE TABLE `Drink` (
  `Drink_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Drink_Name` TEXT NOT NULL,
  `Drink_Price` DECIMAL(5,2) NOT NULL,
  `18+` BOOLEAN NOT NULL
);

CREATE TABLE `Dessert` (
  `Dessert_ID` INTEGER PRIMARY KEY AUTOINCREMENT ,
  `Dessert_Name` TEXT NOT NULL,
  `Dessert_Price` DECIMAL(5,2) NOT NULL
);

CREATE TABLE `Order_Extras` (
  `Order_ID` BIGINT NOT NULL,
  `Drink_ID` BIGINT NOT NULL,
  `Dessert_ID` BIGINT NOT NULL,
  `+18` BOOLEAN NOT NULL,
  FOREIGN KEY(`Order_ID`) REFERENCES `Order` (`Order_ID`),
  FOREIGN KEY (`Drink_ID`) REFERENCES `Drink`(`Drink_ID`),
  FOREIGN KEY (`Dessert_ID`) REFERENCES `Dessert`(`Dessert_ID`)
);

CREATE TABLE `Ingredient` (
  `Ingredient_ID` INTEGER PRIMARY KEY AUTOINCREMENT ,
  `Ingredient_Name` TEXT NOT NULL,
  `Price` DECIMAL(5,2) NOT NULL, 
  `Vegetarian_Ingredient` BOOLEAN NOT NULL,
  `Vegan_Ingredient` BOOLEAN NOT NULL
);

CREATE TABLE `Pizza` (
  `Pizza_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Pizza_Name` TEXT NOT NULL,
  `Vegetarian_Pizza` BOOLEAN NOT NULL,
  `Vegan_Pizza` BOOLEAN NOT NULL,
  `Size` BOOLEAN NOT NULL
);

CREATE TABLE `Pizza_Ingredient` (
  `Pizza_ID` BIGINT NOT NULL,
  `Ingredient_ID` BIGINT NOT NULL,
  FOREIGN KEY (`Pizza_ID`) REFERENCES `Pizza` (`Pizza_ID`),
  FOREIGN KEY (`Ingredient_ID`) REFERENCES `Ingredient` (`Ingredient_ID`)
);

CREATE TABLE `Order_Pizza` (
  `Order_ID` BIGINT NOT NULL,
  `Pizza_ID` BIGINT NOT NULL,
  `Quantity` INT NOT NULL,
  FOREIGN KEY (`Order_ID`) REFERENCES `Order` (`Order_ID`),
  FOREIGN KEY (`Pizza_ID`) REFERENCES `Pizza` (`Pizza_ID`)
);






