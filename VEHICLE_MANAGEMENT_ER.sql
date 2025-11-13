-- ===========================================================
--  VEHICLE MANAGEMENT SYSTEM - FULL DATABASE SETUP
-- ===========================================================

-- 1️⃣ CREATE DATABASE AND USE IT
DROP DATABASE IF EXISTS Vehicle_Management_ER;
CREATE DATABASE Vehicle_Management_ER;
USE Vehicle_Management_ER;

-- ===========================================================
-- 2️⃣ TABLE CREATION
-- ===========================================================

CREATE TABLE Showroom (
    Showroom_ID INT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Manager_Sales_Executive_ID INT UNIQUE
);

CREATE TABLE Address (
    Address_ID INT,
    Showroom_ID INT,
    City VARCHAR(50),
    State VARCHAR(50),
    Pincode VARCHAR(10),
    PRIMARY KEY (Address_ID, Showroom_ID),
    FOREIGN KEY (Showroom_ID) REFERENCES Showroom(Showroom_ID) ON DELETE CASCADE
);

CREATE TABLE Customer (
    Customer_ID INT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Aadhar_No VARCHAR(20) UNIQUE,
    Phone_No VARCHAR(15),
    Email_ID VARCHAR(50),
    DOB DATE,
    Age INT
);

CREATE TABLE Sales_Executive (
    Sales_Executive_ID INT PRIMARY KEY,
    FName VARCHAR(50) NOT NULL,
    LName VARCHAR(50),
    Phone VARCHAR(15),
    Email VARCHAR(50) UNIQUE,
    Designation VARCHAR(100),
    Showroom_ID INT NOT NULL,
    Supervisor_ID INT,
    FOREIGN KEY (Showroom_ID) REFERENCES Showroom(Showroom_ID),
    FOREIGN KEY (Supervisor_ID) REFERENCES Sales_Executive(Sales_Executive_ID)
);

ALTER TABLE Showroom ADD CONSTRAINT fk_showroom_manager
FOREIGN KEY (Manager_Sales_Executive_ID) REFERENCES Sales_Executive(Sales_Executive_ID);

CREATE TABLE Vehicles (
    Vehicle_ID INT PRIMARY KEY,
    Type VARCHAR(50),
    Colour VARCHAR(30),
    Cost DECIMAL(10,2),
    Brand VARCHAR(50),
    Number_Plate VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE Features (
    Engine_ID INT PRIMARY KEY,
    Fuel_Type VARCHAR(30),
    Safety VARCHAR(50),
    Mileage VARCHAR(20),
    Vehicle_ID INT UNIQUE,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicles(Vehicle_ID) ON DELETE CASCADE
);

CREATE TABLE Tax (
    Tax_ID INT PRIMARY KEY,
    Vehicle_ID INT UNIQUE,
    Vehicle_Tax DECIMAL(10,2),
    Road_Tax DECIMAL(10,2),
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicles(Vehicle_ID) ON DELETE CASCADE
);

CREATE TABLE Insurance (
    Insurance_ID INT PRIMARY KEY,
    Vehicle_ID INT UNIQUE,
    Customer_ID INT NOT NULL,
    Policy_No VARCHAR(30) UNIQUE,
    Bank VARCHAR(100),
    Family_Details VARCHAR(200),
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicles(Vehicle_ID) ON DELETE CASCADE,
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)
);

CREATE TABLE Sale (
    Sale_ID INT PRIMARY KEY,
    Customer_ID INT NOT NULL,
    Vehicle_ID INT UNIQUE NOT NULL,
    Sales_Executive_ID INT,
    Target VARCHAR(50),
    Date_of_Sale DATE,
    Quantity INT,
    Offer VARCHAR(50),
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicles(Vehicle_ID),
    FOREIGN KEY (Sales_Executive_ID) REFERENCES Sales_Executive(Sales_Executive_ID)
);

CREATE TABLE Payment (
    Sale_ID INT NOT NULL,
    Payment_sequence_no INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Payment_Mode VARCHAR(30),
    Payment_Method VARCHAR(30),
    Payment_Status VARCHAR(30),
    Loan VARCHAR(30),
    Cash DECIMAL(10,2),
    Cheque_No VARCHAR(30),
    PRIMARY KEY (Sale_ID, Payment_sequence_no),
    FOREIGN KEY (Sale_ID) REFERENCES Sale(Sale_ID) ON DELETE CASCADE
);

CREATE TABLE Services (
    Service_ID INT PRIMARY KEY,
    Customer_ID INT NOT NULL,
    Vehicle_ID INT NOT NULL,
    Price DECIMAL(10,2),
    Issue VARCHAR(100),
    Entry_Date DATE,
    General_Service VARCHAR(100),
    Customer_Approval VARCHAR(10),
    Delivery_Date DATE,
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicles(Vehicle_ID)
);

CREATE TABLE Appointment (
    Appointment_ID INT,
    Customer_ID INT NOT NULL,
    Showroom_ID INT NOT NULL,
    Vehicle_ID INT NOT NULL,
    Appointment_Date DATE NOT NULL,
    Appointment_Time TIME,
    Purpose VARCHAR(255),
    PRIMARY KEY (Appointment_ID, Customer_ID, Showroom_ID, Vehicle_ID),
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
    FOREIGN KEY (Showroom_ID) REFERENCES Showroom(Showroom_ID),
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicles(Vehicle_ID)
);

-- ===========================================================
-- 3️⃣ INSERT SAMPLE DATA
-- ===========================================================

INSERT INTO Showroom (Showroom_ID, Name, Manager_Sales_Executive_ID) VALUES
(1, 'Elite Motors', NULL),
(2, 'City Wheels', NULL),
(3, 'Star Automobiles', NULL),
(4, 'Metro Cars', NULL);

INSERT INTO Address VALUES
(101, 1, 'Bengaluru', 'Karnataka', '560001'),
(102, 2, 'Mysuru', 'Karnataka', '570001'),
(103, 3, 'Hubli', 'Karnataka', '580020'),
(104, 4, 'Mangalore', 'Karnataka', '575001');

INSERT INTO Customer VALUES
(201, 'Arjun Rao', '123456789012', '9876543210', 'arjun@example.com', '1995-04-10', 30),
(202, 'Sneha Patil', '234567890123', '9876501234', 'sneha@example.com', '1998-07-22', 27),
(203, 'Rahul Jain', '345678901234', '8765432109', 'rahul@example.com', '1992-02-15', 33),
(204, 'Meena Joshi', '456789012345', '9123456780', 'meena@example.com', '1989-09-18', 36);

INSERT INTO Sales_Executive VALUES
(1001, 'Ramesh', 'Kumar', '9870000001', 'ramesh.k@example.com', 'Showroom Manager', 1, NULL),
(1002, 'Suresh', 'N', '9870000002', 'suresh.n@example.com', 'Salesperson', 1, 1001),
(1003, 'Anita', 'Rao', '9870000003', 'anita.r@example.com', 'Showroom Manager', 2, NULL),
(1004, 'Pooja', 'S', '9870000004', 'pooja.s@example.com', 'Salesperson', 2, 1003),
(1005, 'Manoj', 'Shetty', '9870000005', 'manoj.s@example.com', 'Showroom Manager', 3, NULL),
(1006, 'Rahul', 'G', '9870000006', 'rahul.g@example.com', 'Salesperson', 3, 1005),
(1007, 'Deepak', 'Naik', '9870000007', 'deepak.n@example.com', 'Showroom Manager', 4, NULL),
(1008, 'Kavya', 'R', '9870000008', 'kavya.r@example.com', 'Salesperson', 4, 1007);

UPDATE Showroom SET Manager_Sales_Executive_ID = 1001 WHERE Showroom_ID = 1;
UPDATE Showroom SET Manager_Sales_Executive_ID = 1003 WHERE Showroom_ID = 2;
UPDATE Showroom SET Manager_Sales_Executive_ID = 1005 WHERE Showroom_ID = 3;
UPDATE Showroom SET Manager_Sales_Executive_ID = 1007 WHERE Showroom_ID = 4;

INSERT INTO Vehicles VALUES
(301, 'SUV', 'Black', 1500000.00, 'Toyota', 'KA01AB1234'),
(302, 'Sedan', 'White', 1200000.00, 'Honda', 'KA02CD5678'),
(303, 'Hatchback', 'Red', 800000.00, 'Hyundai', 'KA03EF9101'),
(304, 'Bike', 'Blue', 120000.00, 'Yamaha', 'KA04GH1112');

INSERT INTO Features VALUES
(301, 'Petrol', 'Airbags, ABS', '12 kmpl', 301),
(302, 'Diesel', 'Airbags, ABS, EBD', '15 kmpl', 302),
(303, 'Petrol', 'Airbags', '18 kmpl', 303),
(304, 'Petrol', 'Disc Brakes', '40 kmpl', 304);

INSERT INTO Tax VALUES
(401, 301, 50000.00, 15000.00),
(402, 302, 40000.00, 12000.00),
(403, 303, 30000.00, 10000.00),
(404, 304, 8000.00, 2000.00);

INSERT INTO Insurance VALUES
(501, 301, 201, 'POL12345', 'SBI Bank', 'Spouse & 2 Kids'),
(502, 302, 202, 'POL67890', 'HDFC Bank', 'Single'),
(503, 303, 203, 'POL24680', 'ICICI Bank', 'Parents Covered'),
(504, 304, 204, 'POL13579', 'Axis Bank', 'No Family Coverage');

INSERT INTO Sale VALUES
(601, 201, 301, 1002, 'Monthly Target', '2025-01-12', 1, '5% Discount'),
(602, 202, 302, 1004, 'Quarterly Target', '2025-02-05', 1, 'Free Accessories'),
(603, 203, 303, 1006, 'Annual Target', '2025-03-08', 1, '10% Discount'),
(604, 204, 304, 1008, 'Monthly Target', '2025-04-15', 1, 'Helmet Free');

INSERT INTO Payment VALUES
(601, 1, 1450000.00, 'Online', 'NetBanking', 'Completed', 'No', 0.00, NULL),
(602, 1, 1100000.00, 'Offline', 'Cheque', 'Pending', 'Yes', 0.00, 'CHQ56789'),
(603, 1, 720000.00, 'Online', 'UPI', 'Completed', 'No', 0.00, NULL),
(604, 1, 120000.00, 'Offline', 'Cash', 'Completed', 'No', 120000.00, NULL);

INSERT INTO Services VALUES
(801, 201, 301, 5000.00, 'Engine Oil Change', '2025-05-01', 'Full Service', 'Yes', '2025-05-03'),
(802, 202, 302, 3000.00, 'Brake Issue', '2025-05-04', 'Brake Service', 'Yes', '2025-05-06'),
(803, 203, 303, 1500.00, 'Tyre Check', '2025-05-07', 'Basic Service', 'No', NULL),
(804, 204, 304, 2000.00, 'Clutch Adjustment', '2025-05-10', 'General Checkup', 'Yes', '2025-05-12');

INSERT INTO Appointment VALUES
(901, 201, 1, 301, '2025-06-01', '10:00:00', 'Routine Checkup'),
(902, 202, 2, 302, '2025-06-05', '14:30:00', 'Service Booking'),
(903, 203, 3, 303, '2025-06-08', '11:00:00', 'Consultation'),
(904, 204, 4, 304, '2025-06-12', '09:00:00', 'Inspection');

-- ===========================================================
-- 4️⃣ FUNCTIONS
-- ===========================================================
DELIMITER $$

CREATE FUNCTION GetTotalPaymentBySale(sale_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT IFNULL(SUM(Amount), 0)
    INTO total
    FROM Payment
    WHERE Sale_ID = sale_id;
    RETURN total;
END $$

CREATE FUNCTION GetAgeCategory(cust_age INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE category VARCHAR(20);
    IF cust_age < 25 THEN
        SET category = 'Young';
    ELSEIF cust_age BETWEEN 25 AND 50 THEN
        SET category = 'Middle-aged';
    ELSE
        SET category = 'Senior';
    END IF;
    RETURN category;
END $$

CREATE FUNCTION GetTotalTax(v_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total_tax DECIMAL(10,2);
    SELECT (Vehicle_Tax + Road_Tax)
    INTO total_tax
    FROM Tax
    WHERE Vehicle_ID = v_id;
    RETURN IFNULL(total_tax, 0);
END $$
DELIMITER ;

-- ===========================================================
-- 5️⃣ TRIGGERS
-- ===========================================================
DELIMITER $$

CREATE TRIGGER before_customer_insert
BEFORE INSERT ON Customer
FOR EACH ROW
BEGIN
    IF NEW.DOB IS NOT NULL THEN
        SET NEW.Age = TIMESTAMPDIFF(YEAR, NEW.DOB, CURDATE());
    END IF;
END $$

CREATE TRIGGER after_sale_insert
AFTER INSERT ON Sale
FOR EACH ROW
BEGIN
    UPDATE Vehicles
    SET Colour = CONCAT(Colour, ' (Sold)')
    WHERE Vehicle_ID = NEW.Vehicle_ID;
END $$

CREATE TABLE Payment_Log (
    Log_ID INT AUTO_INCREMENT PRIMARY KEY,
    Sale_ID INT,
    Deleted_Amount DECIMAL(10,2),
    Deleted_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER after_payment_delete
AFTER DELETE ON Payment
FOR EACH ROW
BEGIN
    INSERT INTO Payment_Log (Sale_ID, Deleted_Amount)
    VALUES (OLD.Sale_ID, OLD.Amount);
END $$
DELIMITER ;

-- ===========================================================
-- 6️⃣ PROCEDURES
-- ===========================================================
DELIMITER $$

CREATE PROCEDURE AddCustomer (
    IN p_id INT,
    IN p_name VARCHAR(50),
    IN p_aadhar VARCHAR(20),
    IN p_phone VARCHAR(15),
    IN p_email VARCHAR(50),
    IN p_dob DATE
)
BEGIN
    INSERT INTO Customer (Customer_ID, Name, Aadhar_No, Phone_No, Email_ID, DOB, Age)
    VALUES (p_id, p_name, p_aadhar, p_phone, p_email, p_dob, TIMESTAMPDIFF(YEAR, p_dob, CURDATE()));
END $$

CREATE PROCEDURE GetShowroomSalesSummary(IN showroom_id INT)
BEGIN
    SELECT s.Sale_ID, c.Name AS Customer_Name, v.Brand, v.Type, s.Date_of_Sale, s.Offer
    FROM Sale s
    JOIN Customer c ON s.Customer_ID = c.Customer_ID
    JOIN Vehicles v ON s.Vehicle_ID = v.Vehicle_ID
    JOIN Sales_Executive se ON s.Sales_Executive_ID = se.Sales_Executive_ID
    WHERE se.Showroom_ID = showroom_id;
END $$

CREATE PROCEDURE DeleteCustomer(IN cust_id INT)
BEGIN
    DELETE FROM Insurance WHERE Customer_ID = cust_id;
    DELETE FROM Services WHERE Customer_ID = cust_id;
    DELETE FROM Appointment WHERE Customer_ID = cust_id;
    DELETE FROM Sale WHERE Customer_ID = cust_id;
    DELETE FROM Customer WHERE Customer_ID = cust_id;
END $$
DELIMITER ;

-- ===========================================================
-- ✅ END OF DATABASE SCRIPT
-- ===========================================================


CREATE USER IF NOT EXISTS 'vm_user'@'localhost' IDENTIFIED BY 'vm_password';

GRANT SELECT
ON Vehicle_Management_ER.* TO 'vm_user'@'localhost';

GRANT EXECUTE ON FUNCTION Vehicle_Management_ER.GetTotalPaymentBySale TO 'vm_user'@'localhost';
GRANT EXECUTE ON FUNCTION Vehicle_Management_ER.GetAgeCategory TO 'vm_user'@'localhost';
GRANT EXECUTE ON FUNCTION Vehicle_Management_ER.GetTotalTax TO 'vm_user'@'localhost';

GRANT TRIGGER ON Vehicle_Management_ER.* TO 'vm_user'@'localhost';

FLUSH PRIVILEGES;

SHOW GRANTS FOR 'vm_user'@'localhost';


SELECT c.Customer_ID, c.Name, c.Phone_No
FROM customer c
WHERE c.Customer_ID IN (
    SELECT s.Customer_ID
    FROM sale s
    WHERE s.Quantity * (
        SELECT v.Cost
        FROM vehicles v
        WHERE v.Vehicle_ID = s.Vehicle_ID
    ) > 100000
);


CREATE USER IF NOT EXISTS 'vm_admin'@'localhost' IDENTIFIED BY 'Admin@123';
GRANT ALL PRIVILEGES ON Vehicle_Management_ER.* TO 'vm_admin'@'localhost' WITH GRANT OPTION;


