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
  - Result: ValueError("The environment variable 'SECRET_KEY' is an empty string")
- **[003] test_get_secret_key_003_anomalous_secret_key_is_too_short**
  - Conditions: environment variable "SECRET_KEY" is a string that is < 256 bits (64 characters) long
  - Result: ValueError("Secret key must be at least 256 bits (64 hexadecimal characters) long")

### generate_jwt()
- **[009] test_generate_jwt_000_anomalous_no_username**
  - Conditions: No username provided
  - Result: ValueError("\<username\> is None")
- **[001] test_generate_jwt_001_anomalous_username_is_not_a_string**
  - Conditions: Provided username is an integer, not a string
  - Result: TypeError("\<username\> must be of type \<class 'int'\>, not \<class 'int'\>")