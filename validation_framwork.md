## Validation Check 1: Null Values

- Checks for missing values in the dataset
- important because having incomplete records can affect reporting and analytics
- If validation fails, a warning message will be outputted

## Validation Check 2: Duplicate Records

- Checks for duplicate weather observations
- Duplicate observations con distort metrics and reporting
- If validation fails, a warning message will be outputted

## Valdiation Check 3: Humidity Check Range

- Checks if humidity value is within an observeable range
- Invalid humidity range will cause invalid recommendations
- If validation failes, a warning message will be outputted

**If all checks are successful, "Validation complete" will be outputted**
