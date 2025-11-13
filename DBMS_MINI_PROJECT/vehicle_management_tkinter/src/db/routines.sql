DROP TRIGGER IF EXISTS trg_before_payment_insert;
DROP TRIGGER IF EXISTS trg_after_sale_insert;
DROP TRIGGER IF EXISTS trg_after_service_update;
DROP FUNCTION IF EXISTS get_total_payment;
DROP PROCEDURE IF EXISTS sp_CustomerPurchases;
DROP PROCEDURE IF EXISTS sp_AddSale;

CREATE TRIGGER trg_before_payment_insert
BEFORE INSERT ON Payment
FOR EACH ROW
BEGIN
  IF NEW.Amount >= 100000 THEN
    SET NEW.Payment_Status = 'Completed';
  ELSE
    SET NEW.Payment_Status = 'Pending';
  END IF;
END;

CREATE TABLE IF NOT EXISTS Sale_Log (
  Log_ID INT AUTO_INCREMENT PRIMARY KEY,
  Sale_ID INT,
  Log_Message VARCHAR(255),
  Log_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_after_sale_insert
AFTER INSERT ON Sale
FOR EACH ROW
BEGIN
  INSERT INTO Sale_Log (Sale_ID, Log_Message)
  VALUES (NEW.Sale_ID, CONCAT('New sale recorded for Vehicle_ID ', NEW.Vehicle_ID, ' by Exec ', NEW.Sales_Executive_ID));
END;

ALTER TABLE Services ADD COLUMN IF NOT EXISTS Service_Status VARCHAR(30) DEFAULT 'Pending';

CREATE TRIGGER trg_after_service_update
AFTER UPDATE ON Services
FOR EACH ROW
BEGIN
  IF NEW.Delivery_Date IS NOT NULL THEN
    UPDATE Services SET Service_Status = 'Completed' WHERE Service_ID = NEW.Service_ID;
  END IF;
END;

CREATE FUNCTION get_total_payment(p_vehicle_id INT)
RETURNS DECIMAL(12,2)
DETERMINISTIC
BEGIN
  DECLARE v_total DECIMAL(12,2) DEFAULT 0.00;
  SELECT IFNULL(SUM(p.Amount),0.00) INTO v_total
  FROM Payment p
  JOIN Sale s ON p.Sale_ID = s.Sale_ID
  WHERE s.Vehicle_ID = p_vehicle_id;
  RETURN v_total;
END;

CREATE PROCEDURE sp_CustomerPurchases(IN p_cust INT)
BEGIN
  SELECT c.Customer_ID, c.Name AS Customer, v.Vehicle_ID, v.Brand, s.Date_of_Sale, s.Offer
  FROM Sale s
  JOIN Customer c ON s.Customer_ID = c.Customer_ID
  JOIN Vehicles v ON s.Vehicle_ID = v.Vehicle_ID
  WHERE c.Customer_ID = p_cust;
END;

CREATE PROCEDURE sp_AddSale(
  IN p_customer_id INT,
  IN p_vehicle_id INT,
  IN p_sales_exec_id INT,
  IN p_target VARCHAR(50),
  IN p_quantity INT,
  IN p_offer VARCHAR(50),
  IN p_amount DECIMAL(12,2),
  IN p_payment_mode VARCHAR(30)
)
BEGIN
  INSERT INTO Sale (Sale_ID, Customer_ID, Vehicle_ID, Sales_Executive_ID, Target, Date_of_Sale, Quantity, Offer)
  VALUES (NULL, p_customer_id, p_vehicle_id, p_sales_exec_id, p_target, CURDATE(), p_quantity, p_offer);

  SET @last_sale_id = LAST_INSERT_ID();
  INSERT INTO Payment (Sale_ID, Payment_sequence_no, Amount, Payment_Mode, Payment_Method, Payment_Status, Loan, Cash)
  VALUES (@last_sale_id, 1, p_amount, p_payment_mode, 'Online', NULL, 'No', p_amount);
END;