-- Discounts (10)
INSERT INTO `Discount` (Discount_Code, Percent, Redeemed) VALUES
(1001, 10, FALSE), (1002, 15, TRUE), (1003, 20, FALSE), (1004, 5, TRUE),
(1005, 25, FALSE), (1006, 30, TRUE), (1007, 12, FALSE), (1008, 18, FALSE),
(1009, 8, TRUE), (1010, 22, FALSE);

-- Customers (10)
INSERT INTO `Customer` (Customer_Name, Customer_Surname, Birth_Date, Customer_Address, Customer_Postal_Code, Credit_Card, Customer_Email, Phone_Number, Pizzas_Ordered) VALUES
('John','Doe','1990-05-15','123 Main St','10001',1234567890123456,'john@example.com',1112223333,5),
('Jane','Smith','1985-08-22','456 Park Ave','10002',9876543210987654,'jane@example.com',2223334444,3),
('Alice','Brown','2000-01-10','789 Broadway','10003',1111222233334444,'alice@example.com',3334445555,7),
('Bob','Johnson','1992-03-18','12 River Rd','10001',5555444433332222,'bob@example.com',4445556666,2),
('Emily','Davis','1995-11-25','45 Hill St','10002',4444333322221111,'emily@example.com',5556667777,4),
('Chris','Wilson','1988-07-30','78 Lake Ave','10003',6666777788889999,'chris@example.com',6667778888,6),
('Sophia','Martinez','1999-02-14','90 Oak Ln','10001',7777888899990000,'sophia@example.com',7778889999,8),
('Liam','Anderson','1993-09-12','22 Pine St','10002',8888999900001111,'liam@example.com',8889990000,1),
('Olivia','Taylor','1997-12-01','34 Maple Dr','10003',9999000011112222,'olivia@example.com',9990001111,3),
('Ethan','Harris','1989-04-09','56 Birch Blvd','10001',2222111133334444,'ethan@example.com',1011121314,9);

-- Staff (10, incl. delivery persons)
INSERT INTO `Staff` (Name, Surname, Bank_Account, Liscence, Postal_Code, Availability) VALUES
('Mark','Taylor','BA12345',1,'10001',TRUE),
('Lucy','Green','BA67890',2,'10002',TRUE),
('Paul','White','BA54321',3,'10003',TRUE),
('Anna','King','BA98765',4,'10001',TRUE),
('Tom','Evans','BA19283',5,'10002',FALSE),
('Rachel','Scott','BA45678',6,'10003',TRUE),
('James','Lee','BA22222',7,'10001',TRUE),
('Maria','Hall','BA33333',8,'10002',TRUE),
('David','Young','BA44444',9,'10003',TRUE),
('Sophia','Clark','BA55555',10,'10001',TRUE);

-- Orders (10)
INSERT INTO `Order` (Customer_ID, Delivery_Person, Discount_Code, Order_Address, Order_Postal_Code, Order_Time, Order_Price, Delivered) VALUES
(1,1,1001,'123 Main St','10001','2025-01-01 18:00:00',25,TRUE),
(2,2,1002,'456 Park Ave','10002','2025-01-02 19:30:00',40,FALSE),
(3,3,NULL,'789 Broadway','10003','2025-01-03 20:00:00',30,TRUE),
(4,4,1004,'12 River Rd','10001','2025-01-04 18:45:00',22,TRUE),
(5,5,1005,'45 Hill St','10002','2025-01-05 21:15:00',28,FALSE),
(6,6,NULL,'78 Lake Ave','10003','2025-01-06 17:30:00',35,TRUE),
(7,7,1007,'90 Oak Ln','10001','2025-01-07 20:20:00',42,TRUE),
(8,8,1008,'22 Pine St','10002','2025-01-08 19:10:00',18,FALSE),
(9,9,1009,'34 Maple Dr','10003','2025-01-09 18:40:00',50,TRUE),
(10,10,1010,'56 Birch Blvd','10001','2025-01-10 21:00:00',60,TRUE);

-- Drinks (10)
INSERT INTO `Drink` (Drink_Name, Drink_Price, `18+`) VALUES
('Cola',2.50,FALSE),('Orange Juice',3.00,FALSE),('Lemonade',2.20,FALSE),
('Iced Tea',2.80,FALSE),('Beer',4.00,TRUE),('Red Wine',5.50,TRUE),
('Water',1.50,FALSE),('Energy Drink',3.50,FALSE),('Apple Juice',3.00,FALSE),
('Whiskey',6.50,TRUE);

-- Desserts (10)
INSERT INTO `Dessert` (Dessert_Name, Dessert_Price) VALUES
('Ice Cream',3.50),('Cheesecake',4.00),('Brownie',3.00),('Tiramisu',4.50),
('Apple Pie',3.80),('Chocolate Cake',4.20),('Panna Cotta',3.90),('Donut',2.50),
('Fruit Salad',3.20),('Cupcake',2.80);

-- Order_Extras (10)
INSERT INTO `Order_Extras` (Order_ID, Drink_ID, Dessert_ID, `+18`) VALUES
(1,1,1,FALSE),(2,2,2,FALSE),(3,3,3,FALSE),(4,4,4,FALSE),
(5,5,5,TRUE),(6,6,6,TRUE),(7,7,7,FALSE),(8,8,8,FALSE),
(9,9,9,FALSE),(10,10,10,TRUE);

-- Ingredients (10)
INSERT INTO `Ingredient` (Ingredient_ID, Ingredient_Name, Price, Vegetarian_Ingredient, Vegan_Ingredient) VALUES
(1,'Cheese',1.00,TRUE,FALSE),(2,'Tomato Sauce',0.50,TRUE,TRUE),
(3,'Pepperoni',1.50,FALSE,FALSE),(4,'Ham',1.50,FALSE,FALSE),
(5,'Chicken',1.80,FALSE,FALSE),(6,'Mushrooms',1.20,TRUE,TRUE),
(7,'Onions',0.80,TRUE,TRUE),(8,'Bell Peppers',0.90,TRUE,TRUE),
(9,'Olives',1.00,TRUE,TRUE),(10,'Shrimp',2.50,FALSE,FALSE);

-- Pizzas (10)
INSERT INTO `Pizza` (Pizza_Name, Vegetarian_Pizza, Vegan_Pizza, Size) VALUES
('Margherita',TRUE,FALSE,TRUE),('Pepperoni',FALSE,FALSE,TRUE),
('Hawaiian',FALSE,FALSE,TRUE),('BBQ Chicken',FALSE,FALSE,TRUE),
('Veggie Supreme',TRUE,TRUE,TRUE),('Four Cheese',TRUE,FALSE,TRUE),
('Meat Feast',FALSE,FALSE,TRUE),('Spicy Veggie',TRUE,TRUE,TRUE),
('Seafood Special',FALSE,FALSE,TRUE),('Mushroom Delight',TRUE,TRUE,TRUE);

-- Pizza_Ingredient (at least 10)
INSERT INTO `Pizza_Ingredient` (Pizza_ID, Ingredient_ID) VALUES
(1,1),(1,2),(2,1),(2,2),(2,3),(3,1),(3,2),(3,4),(4,1),(4,2),
(4,5),(5,2),(5,6),(5,7),(5,8),(6,1),(6,2),(6,6),(7,1),(7,2);

-- Order_Pizza (10)
INSERT INTO `Order_Pizza` (Order_ID, Pizza_ID, Quantity) VALUES
(1,1,2),(1,2,1),(2,3,1),(2,4,2),(3,5,1),(4,6,2),(5,7,1),
(6,8,2),(7,9,1),(10,10,3);
