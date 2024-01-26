### get_storage_directory()
- **[000] test_get_storage_directory_000_nominal_valid_storage_directory**
  - Conditions: Nominal - Environment variable "STORAGE_DIRECTORY" is set and represents a valid directory
  - Result: Storage directory is returned
- **[001] test_get_storage_directory_001_anomalous_storage_directory_not_set**
  - Conditions: Anomalous - Environment variable "STORAGE_DIRECTORY" is not set
  - Result: EnvironmentError("The environment variable 'STORAGE_DIRECTORY' is not set")
- **[002] test_get_storage_directory_002_anomalous_storage_directory_does_not_exist**
  - Conditions: Anomalous - Environment variable "STORAGE_DIRECTORY" is set but does not exist
  - Result: FileNotFoundException("The path representent by environment variable 'STORAGE_DIRECTORY' does not exist")
- **[003] test_get_storage_directory_003_anomalous_storage_directory_is_not_dir**
  - Conditions: Anomalous - Environment variable "STORAGE_DIRECTORY" is set and exists, but is not a directory
  - Result: NotADirectoryError("The environment variable 'STORAGE_DIRECTORY' does not represent a directory")
  
### is_file_present()
- **[000] test_list_files_000_nominal_file_present**
  - Conditions: File is present
  - Result: True
- **[001] test_list_files_001_nominal_file_not_present**
  - Conditions: Nominal - File present in database and storage
  - Result: False