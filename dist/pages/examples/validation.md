## [Validation Pattern](#validation-pattern-1)

Validate an object before saving, showing feedback on invalid fields:

```
CREATE MICROFLOW Sales.ACT_SaveCustomer
FOLDER 'Customer'
BEGIN
  DECLARE $Customer Sales.Customer;
  DECLARE $IsValid Boolean = true;

  -- Validate required fields
  IF $Customer/Name = empty THEN
    VALIDATION FEEDBACK $Customer/Name MESSAGE 'Name is required';
    SET $IsValid = false;
  END IF;

  IF $Customer/Email = empty THEN
    VALIDATION FEEDBACK $Customer/Email MESSAGE 'Email is required';
    SET $IsValid = false;
  END IF;

  -- Check for duplicate email
  IF $IsValid THEN
    RETRIEVE $Existing FROM Sales.Customer
      WHERE Email = $Customer/Email
      LIMIT 1;
    IF $Existing != empty THEN
      VALIDATION FEEDBACK $Customer/Email MESSAGE 'A customer with this email already exists';
      SET $IsValid = false;
    END IF;
  END IF;

  -- Save only if valid
  IF $IsValid THEN
    COMMIT $Customer;
    CLOSE PAGE;
  END IF;
END;

```