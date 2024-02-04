# remove_expired_files()

### remove_expired_files()
- **[000] test_remove_expired_files_000_nominal_no_expired_files_in_database**
  - Conditions: There is a file present in the database, but it is not expired
  - Result: Nothing happens
- **[001] test_remove_expired_files_001_nominal_expired_file_in_db_and_storage**
  - Conditions: There is an expired file present in the database
  - Result: Expired file is removed from database and storage
- **[002]test_remove_expired_files_002_anomalous_expired_file_in_db_and_not_storage**
  - Condtions: There is an expired file present in the database, but its file is missing in storage
  - Result: Expired file metadata is removed form database

### get_orphaned_files()
- **[000] test_get_orphaned_files_000_no_orphaned_files**
  - Conditions: File in db and storage
  - Result: orphaned_files == []
- **[001] test_get_orphaned_files_001_one_orphaned_file**
  - Conditions: File not in db, but in storage
  - Result: orphaned_files == ["abcdefgh.jpeg"]
  
### remove_orphaned_files()
- **[000] test_remove_orphaned_files_000_one_orphaned_file**
  - Conditions: One oprhaned file
  - Result: File removed