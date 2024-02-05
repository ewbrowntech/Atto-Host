# users/
### register() [POST users/register]
- **[000] test_register_000_nominal**
  - Conditions: Unique username and password provided
  - Result: User {username} created
- **[001] test_register_001_anomalous_no_username_provided**
  - Conditions: Password provided, but no username provided
  - Result: {Pydantic error}
- **[002] test_register_002_anomalous_no_password_provided**
  - Conditions: Username provided, but no password provided
  - Result: {Pydantic error}
- **[003] test_register_003_anomalous_username_taken**
  - Conditions: Non-unique username already registered
  - Result: HTTP 400 - Username {username} is already taken