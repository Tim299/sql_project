# Create & select database
CREATE DATABASE pos_system;
USE pos_system;

# Create tables
CREATE TABLE Orders
(
    orderID INT NOT NULL,
    orderDate DATE,
    PRIMARY KEY (orderID)
);

CREATE TABLE Item
(
    itemID INT NOT NULL, 
    name VARCHAR(128),
    price INT, 
    stock INT, 
    itemType VARCHAR(32),
    PRIMARY KEY (itemID)
);

CREATE TABLE OrderItem
(
    orderID INT NOT NULL, 
    itemID INT NOT NULL, 
    subtotal INT, 
    FOREIGN KEY (orderID) REFERENCES Orders(orderID),
    FOREIGN KEY (itemID) REFERENCES Item(itemID)
);

# Insert products into Item table
INSERT INTO Item (itemID, name, price, stock, itemType)
VALUES 
(1, "Hawaii", 99, 0, "Pizza"),
(2, "Cola", 19, 0, "Drink");

# Trigger for applying friday discount on pizzas
DELIMITER //

CREATE TRIGGER orderitem_insert_trigger
BEFORE INSERT ON OrderItem
FOR EACH ROW
BEGIN
    DECLARE is_pizza INT;
    DECLARE is_friday INT;

    -- Check if the inserted item is a pizza
    SELECT COUNT(*) INTO is_pizza
    FROM Item
    WHERE itemID = NEW.itemID AND itemType = 'pizza';

    -- Check if the current day is Friday (day of the week: 6)
    SELECT IF(DAYOFWEEK(CURRENT_DATE()) = 6, 1, 0) INTO is_friday;

    -- Decrease the price temporarily by 20% if it's a pizza on Friday
    IF is_pizza = 1 AND is_friday = 1 THEN
        SET NEW.subtotal = NEW.subtotal * 0.8;
    ELSE
        SET NEW.subtotal = 99;
    END IF;
END //

DELIMITER ;

# Procedure for adding items to the customer's cart
CREATE PROCEDURE AddToCart (addItemID INT, addItemPrice INT, addOrderID INT)
BEGIN
    INSERT INTO OrderItem (orderID, itemID, subtotal)
    VALUES (addOrderID, addItemID, addItemPrice);
    UPDATE Item SET stock = stock - 1 WHERE itemID = addItemID;
END;
