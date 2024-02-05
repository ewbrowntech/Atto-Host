# tokens

### get_secret_key()
- **[000] test_get_secret_key_000_nominal_secret_key**
  - Conditions: Environment variable "SECRET_KEY" is set as a string
  - Result: Secret key string returned
- **[001] test_get_secret_key_001_anomalous_no_secret_key**
  - Conditions: Environment variable "SECRET_KEY" is not set
  - Result: EnvironmentVariable("The environment variable 'SECRET_KEY' is not set")
- **[002] test_get_secret_key_002_anomalous_secret_key_is_empty_string**
  - Conditions: Environment variable "SECRET_KEY" is an empty string
  - Result: ValueError("The environmet variable 'SECRET_KEY' is None")

### generate_jwt()
- **[000] test_generate_jwt_000**
- **[000] test_generate_jwt_001_anomalous_no_username**
- **[000] test_generate_jwt_002_anomalous_no_secret_key**
- **[000] test_generate_jwt_003**