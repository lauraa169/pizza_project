-- ======================
-- Discounts (10)
-- ======================
INSERT INTO Discount (Discount_Code, Percent, Redeemed) VALUES
(1001,10,0),(1002,15,1),(1003,20,0),(1004,5,1),
(1005,25,0),(1006,30,1),(1007,12,0),(1008,18,0),
(1009,8,1),(1010,22,0);

-- ======================
-- Customers (10)
-- ======================
INSERT INTO Customer (Customer_Name, Customer_Surname, Birth_Date, Customer_Address, Customer_Postal_Code, Credit_Card, Customer_Email, Phone_Number, Pizzas_Ordered) VALUES
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

-- ======================
-- Staff (10)
-- ======================
INSERT INTO Staff (Name, Surname, Bank_Account, Liscence, Postal_Code, Availability) VALUES
('Mark','Taylor','BA12345',1,'10001',1),
('Lucy','Green','BA67890',2,'10002',1),
('Paul','White','BA54321',3,'10003',1),
('Anna','King','BA98765',4,'10001',1),
('Tom','Evans','BA19283',5,'10002',0),
('Rachel','Scott','BA45678',6,'10003',1),
('James','Lee','BA22222',7,'10001',1),
('Maria','Hall','BA33333',8,'10002',1),
('David','Young','BA44444',9,'10003',1),
('Sophia','Clark','BA55555',10,'10001',1);

-- ======================
-- Menu_Item (30 items: 10 pizzas, 10 drinks, 10 desserts)
-- ======================
-- Pizzas
INSERT INTO Menu_Item (Item_Name, Item_Price) VALUES
('Margherita',8.50),('Pepperoni',9.50),('Hawaiian',10.00),('BBQ Chicken',11.00),
('Veggie Supreme',9.00),('Four Cheese',10.50),('Meat Feast',12.00),('Spicy Veggie',9.50),
('Seafood Special',13.00),('Mushroom Delight',9.00);

-- Drinks
INSERT INTO Menu_Item (Item_Name, Item_Price) VALUES
('Cola',2.50),('Orange Juice',3.00),('Lemonade',2.20),('Iced Tea',2.80),
('Beer',4.00),('Red Wine',5.50),('Water',1.50),('Energy Drink',3.50),
('Apple Juice',3.00),('Whiskey',6.50);

-- Desserts
INSERT INTO Menu_Item (Item_Name, Item_Price) VALUES
('Ice Cream',3.50),('Cheesecake',4.00),('Brownie',3.00),('Tiramisu',4.50),
('Apple Pie',3.80),('Chocolate Cake',4.20),('Panna Cotta',3.90),('Donut',2.50),
('Fruit Salad',3.20),('Cupcake',2.80);

-- ======================
-- Drinks (reference Menu_Item)
-- ======================
INSERT INTO Drink (Drink_ID, Drink_Name, Drink_Price, "18+") VALUES
(11,'Cola',2.50,0),(12,'Orange Juice',3.00,0),(13,'Lemonade',2.20,0),(14,'Iced Tea',2.80,0),
(15,'Beer',4.00,1),(16,'Red Wine',5.50,1),(17,'Water',1.50,0),(18,'Energy Drink',3.50,0),
(19,'Apple Juice',3.00,0),(20,'Whiskey',6.50,1);

-- ======================
-- Desserts (reference Menu_Item)
-- ======================
INSERT INTO Dessert (Dessert_ID, Dessert_Name, Dessert_Price) VALUES
(21,'Ice Cream',3.50),(22,'Cheesecake',4.00),(23,'Brownie',3.00),(24,'Tiramisu',4.50),
(25,'Apple Pie',3.80),(26,'Chocolate Cake',4.20),(27,'Panna Cotta',3.90),(28,'Donut',2.50),
(29,'Fruit Salad',3.20),(30,'Cupcake',2.80);

-- ======================
-- Ingredients (10)
-- ======================
INSERT INTO Ingredient (Ingredient_Name, Price, Vegetarian_Ingredient, Vegan_Ingredient) VALUES
('Cheese',1.00,1,0),('Tomato Sauce',0.50,1,1),('Pepperoni',1.50,0,0),
('Ham',1.50,0,0),('Chicken',1.80,0,0),('Mushrooms',1.20,1,1),
('Onions',0.80,1,1),('Bell Peppers',0.90,1,1),('Olives',1.00,1,1),('Shrimp',2.50,0,0);

-- ======================
-- Pizzas (10, reference Menu_Item)
-- ======================
INSERT INTO Pizza (Pizza_ID, Pizza_Name, Vegetarian_Pizza, Vegan_Pizza, Size, Pizza_Price) VALUES
(1,'Margherita',1,0,1,8.50),(2,'Pepperoni',0,0,1,9.50),(3,'Hawaiian',0,0,1,10.00),
(4,'BBQ Chicken',0,0,1,11.00),(5,'Veggie Supreme',1,1,1,9.00),(6,'Four Cheese',1,0,1,10.50),
(7,'Meat Feast',0,0,1,12.00),(8,'Spicy Veggie',1,1,1,9.50),(9,'Seafood Special',0,0,1,13.00),
(10,'Mushroom Delight',1,1,1,9.00);

-- ======================
-- Pizza_Ingredient (10 sample)
-- ======================
INSERT INTO Pizza_Ingredient (Pizza_ID, Ingredient_ID) VALUES
(1,1),(1,2),(2,1),(2,3),(3,1),(3,4),(4,1),(4,5),(5,2),(5,6);

-- ======================
-- Orders (10)
-- ======================
INSERT INTO "Order" (Customer_ID, Delivery_Person, Discount_Code, Order_Address, Order_Postal_Code, Order_Time, Order_Price, Delivered) VALUES
(1,1,1001,'123 Main St','10001','2025-01-01 18:00:00',25,1),
(2,2,1002,'456 Park Ave','10002','2025-01-02 19:30:00',40,0),
(3,3,NULL,'789 Broadway','10003','2025-01-03 20:00:00',30,1),
(4,4,1004,'12 River Rd','10001','2025-01-04 18:45:00',22,1),
(5,5,1005,'45 Hill St','10002','2025-01-05 21:15:00',28,0),
(6,6,NULL,'78 Lake Ave','10003','2025-01-06 17:30:00',35,1),
(7,7,1007,'90 Oak Ln','10001','2025-01-07 20:20:00',42,1),
(8,8,1008,'22 Pine St','10002','2025-01-08 19:10:00',18,0),
(9,9,1009,'34 Maple Dr','10003','2025-01-09 18:40:00',50,1),
(10,10,1010,'56 Birch Blvd','10001','2025-01-10 21:00:00',60,1);

-- ======================
-- Order_Item (10 sample)
-- ======================
INSERT INTO Order_Item (Order_ID, Item_ID, Quantity) VALUES
(1,1,2),(1,11,1),(2,3,1),(2,15,2),(3,5,1),(4,6,2),(5,7,1),(6,8,2),(7,9,1),(10,10,3);
