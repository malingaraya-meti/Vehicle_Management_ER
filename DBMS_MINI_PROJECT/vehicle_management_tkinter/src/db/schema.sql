CREATE TABLE IF NOT EXISTS Customer (
    Customer_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(15),
    Address TEXT
);

CREATE TABLE IF NOT EXISTS Vehicle (
    Vehicle_ID INT AUTO_INCREMENT PRIMARY KEY,
    Brand VARCHAR(50) NOT NULL,
    Model VARCHAR(50) NOT NULL,
    Year INT,
    Price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS Sale (
    Sale_ID INT AUTO_INCREMENT PRIMARY KEY,
    Customer_ID INT,
    Vehicle_ID INT,
    Sales_Executive_ID INT,
    Date_of_Sale DATE NOT NULL,
    Quantity INT NOT NULL,
    Offer VARCHAR(50),
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
);

CREATE TABLE IF NOT EXISTS Payment (
    Payment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Sale_ID INT,
    Amount DECIMAL(10, 2) NOT NULL,
    Payment_Mode VARCHAR(30),
    Payment_Status VARCHAR(30),
    FOREIGN KEY (Sale_ID) REFERENCES Sale(Sale_ID)
);

CREATE TABLE IF NOT EXISTS Services (
    Service_ID INT AUTO_INCREMENT PRIMARY KEY,
    Vehicle_ID INT,
    Service_Date DATE NOT NULL,
    Delivery_Date DATE,
    Service_Status VARCHAR(30) DEFAULT 'Pending',
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
);