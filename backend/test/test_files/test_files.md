# files/

### list_files() [GET files/]
- **[000] test_list_files_000_nominal_no_files_present**
  - Conditions: Nominal - No files present in database or storage 
  - Result: HTTP 200 - []
- **[001] test_list_files_001_nominal_file_in_db_and_storage**
  - Conditions: Nominal - File present in database and storage
  - Result: HTTP 200 - [{"fileAvailable": true}]
- **[002] test_list_files_002_anomalous_file_in_db_and_not_in_storage**
  - Conditions: Anomalous - File present in database but not in storage
  - Result: HTTP 200 - [{"fileAvailable": false}]
- **[003] test_list_files_003_anomalous_file_not_in_db_and_in_storage**
  - Conditions: Anomalous - File present in storage but not in database
  - Result: HTTP 200 - []

### upload_file() [POST files/]
- **[000] test_upload_file_000_nominal**
  - Conditions: File of valid type included in request
  - Result: HTTP 200 - [\{file object\}]
- **[001] test_upload_file_001_anomalous_no_file_included**
  - Conditions: No file included in request
  - Result: HTTP 400 - "No file was received with the request"
- **[002] test_upload_file_000_disallowed_mimetype**
  - Conditions: File is of a disallowed type
  - Result: HTTP 400 - "File type not allowed"
- **[003] test_upload_file_000_oversized_file**
- **[004]**


### remove_all_files() [DELETE files/]
### view_file() [GET files/<file_id>]
### remove_file() [DELETE files/<file_id>]
### download_file() [GET files/<file_id>/download]