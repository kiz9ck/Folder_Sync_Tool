import os
import shutil
import hashlib
import logging
import time
import sys


def setup_logger(log_file):
    logger = logging.getLogger("sync_logger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        chunk = f.read(8192)
        while chunk:
            hasher.update(chunk)
            chunk = f.read(8192)
    return hasher.hexdigest()


def sync(source, replica, logger):
    for root, dirs, files in os.walk(source):
        rel_path = os.path.relpath(root, source)
        replica_root = os.path.join(replica, rel_path)
        if not os.path.exists(replica_root):
            os.makedirs(replica_root)
            logger.info(f"Created directory: {replica_root}")
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_root, file)
            if not os.path.exists(replica_file) or get_file_hash(
                source_file
            ) != get_file_hash(replica_file):
                shutil.copy2(source_file, replica_file)
                logger.info(f"Copied new file: {source_file} to {replica_file}")
    for root, dirs, files in os.walk(replica, topdown=False):
        rel_path = os.path.relpath(root, replica)
        source_root = os.path.join(source, rel_path)

        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_root, file)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                logger.info(f"Deleted file: {replica_file}")

        for dir in dirs:
            replica_dir = os.path.join(root, dir)
            source_dir = os.path.join(source_root, dir)
            if not os.path.exists(source_dir):
                shutil.rmtree(replica_dir)
                logger.info(f"Deleted directory: {replica_dir}")


def main():
    if len(sys.argv) != 6:
        print("Usage: python sync.py <source> <replica> <interval> <amount> <log_file>")
        return

    source = sys.argv[1]
    replica = sys.argv[2]
    log_file = sys.argv[5]
    
    logger = setup_logger(log_file)
    
    if not os.path.isdir(source):
        logger.Error(f"Error: there is no '{source}' directory")
        return

    if os.path.abspath(source) == os.path.abspath(replica):
        logger.Error("Eror: <source> and <replica> can't be the same path")
        return

    if os.path.exists(replica) and not os.path.isdir(replica):
        logger.Error(f"Error: '{replica} is a file not a directory'")
        return

    try:
        interval = float(sys.argv[3])
        amount = int(sys.argv[4])
    except ValueError:
        logger.Error("Error: <interval> and <amount> must be digits")
        return
    if interval < 0:
        logger.error("Error: <interval> must be positive number")
        return
    if amount <= 0:
        logger.Error("Error: <amount> must be greater than 0")
        return

    for i in range(amount):
        logger.info("Synchronization")
        try:
            sync(source, replica, logger)
        except PermissionError as e:
            logger.Error("Error: enexpected error")
            return
        if i < amount - 1:
            time.sleep(interval)


if __name__ == "__main__":
    main()
