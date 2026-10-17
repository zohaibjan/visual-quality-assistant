import os, tempfile
import pandas as pd

STAGE = os.getenv("STAGE_NAME")

def list_staged_files(session):
    rows = session.sql(f"LIST {STAGE}").collect()
    return [os.path.basename(r['name']).replace(".gz", "") for r in rows]

def download_file(session, filename):
    tmp = tempfile.mkdtemp()
    session.file.get(f"{STAGE}/{filename}", tmp)
    return os.path.join(tmp, filename)

def wait_for_file(session, filename, retries=10, delay=1):
    import time
    for _ in range(retries):
        if filename in list_staged_files(session):
            return True
        time.sleep(delay)
    return False