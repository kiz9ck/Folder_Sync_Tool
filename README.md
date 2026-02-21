# Folder Synchronization Tool

A lightweight, robust command-line tool for one-way folder synchronization, written purely in Python using only standard libraries. 

## Features
* **One-way Sync**: Ensures the replica folder perfectly matches the source folder.
* **MD5 Hashing**: Uses chunked MD5 hashing (8KB chunks) to accurately detect file modifications without running into memory limits on large files.
* **Deep Directory Support**: Safely handles nested directories (uses bottom-up traversal for safe deletions).
* **Logging**: Outputs operations to both console and a specified log file.
* **Zero Dependencies**: Built entirely with Python's Standard Library (no `requirements.txt` needed).

## Usage

Run the script via command line using the following syntax:

```bash
python sync.py <source_path> <replica_path> <interval_seconds> <amount_of_syncs> <log_file_path>
```

**Example:**
```bash
python sync.py ./source ./replica 60 5 sync.log
```