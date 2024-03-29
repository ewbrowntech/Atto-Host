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
- **[002] test_upload_file_002_anomalous_disallowed_mimetype**
  - Conditions: File is of a disallowed type
  - Result: HTTP 422 - "File type not allowed"
- **[003] test_upload_file_003_anomalous_disallowed_extension**
  - Conditions: File is of a disallowed type
  - Result: HTTP 422 - "File type not allowed"
- **[004] test_upload_file_004_anomalous_oversized_file**
  - Conditions: File size is over the allowed size
  - Result: HTTP 422 - "File is larger than the allowed size of 100MB"

### remove_all_files() [DELETE files/]
- **[000] test_remove_all_files_000_nominal_no_files_present**
  - Conditions: No files present in database or storage
  - Result: HTTP 204 - No content
- **[001] test_remove_all_files_001_nominal_files_present**
  - Conditions: File present in database and storage
  - Result: HTTP 204 - No Content - File removed from database and storage
- **[002] test_remove_all_files_002_anomalous_file_in_db_and_not_in_storage**
  - Conditions: File present in database, but not in storage
  - Result: HTTP 204 - No Content - File removed from database
- **[003] test_remove_all_files_003_anomalous_file_not_in_db_and_in_storage**
  - Conditions: File present not in database, but is in storage
  - Result: HTTP 204 - No Content - File removed from storage
- **[004] test_remove_all_files_004_anomalous_user_not_admin**
  - Conditions: User is not an admin
  - Result: HTTP 403 - Forbidden

### view_file() [GET files/<file_id>]
- **[000] test_view_file_000_nominal**
  - Conditions: File object present and file present in storage
  - Result: HTTP 200 - \<file object\>
- **[001] test_view_file_001_anomalous_nonexistent_file**
  - Conditions: File object not present in database
  - Result: HTTP 404 - File not found
- **[002] test_view_file_002_anomalous_file_missing_in_storage**
  - Conditions: File object present in database but file itself not in storage
  - Result: HTTP 200 - [{"fileAvailable": false}]
<!-- - **[003] test_view_file_003_anomalous_invalid_permissions**
  - Conditions: User attempts to access privated file without the necessary permissions -->

### remove_file() [DELETE files/<file_id>]
- **[000] test_remove_file_000_nominal_file_present_owner**
  - Conditions: File object present and file present in storage, request is from file owner
  - Result: HTTP 204 - No content
- **[000] test_remove_file_001_nominal_file_present_admin**
  - Conditions: File object present and file present in storage, request is from admin
  - Result: HTTP 204 - No content
- **[002] test_remove_file_002_anomalous_nonexistent_file**
  - Conditions: File object is not present in database
  - Result: HTTP 404 - File not found
- **[003] test_remove_file_003_anomalous_file_missing_in_storage**
  - Conditions: File object in database but file itself not in storage
  - Result: HTTP 204 - No content
- **[004] test_remove_file_004_anomalous_file_insufficient_priveledges**
  - Conditions: The requester is neither the file owner nor an admin
  - Result: HTTP 403 - "The current user is not authorized to perform this action"

### download_file() [GET files/<file_id>/download]
- **[000] test_download_file_000_nominal_public_file**
  - Conditions: File object present and file present in storage
  - Result: HTTP 200 - \<File Download\>
- **[001] test_download_file_001_anomalous_nonexistent_file**
  - Conditions: File object is not present in database
  - Result: HTTP 404 - File not found
- **[002] test_download_file_002_anomalous_file_missing_in_storage**
  - Conditions: File object in database but file itself not in storage
  - Result: HTTP 404 - The requested file metadata exists, but the file binary was not found in storage
- **[003] test_download_file_003_anomalous_exceeded_rate_limit**
  - Conditions: 4 requests made, exceeding limit of 3 requests per minute
  - Result: HTTP 429 - Rate limit exceeded
<!-- - **[004] test_download_file_004_anomalous_invalid_permissions**
  - Conditions: User attempts to access privated file without the necessary permissions
  - Result: HTTP 403 - Insufficient permissions -->