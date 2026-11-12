"""Run the official eval with bounded transport retries; no grading changes."""
import os
from pathlib import Path
import runpy
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'evals'))
for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines():
    if line.startswith('GEMINI_API_KEY='):
        os.environ['GEMINI_API_KEY'] = line.split('=', 1)[1].strip()
original_open = urllib.request.urlopen

def patient_open(*args, **kwargs):
    kwargs['timeout'] = 180
    for attempt in range(3):
        try:
            return original_open(*args, **kwargs)
        except (OSError, urllib.error.URLError) as exc:
            code = getattr(exc, 'code', None)
            retryable = code in (429, 500, 502, 503, 504) or (code is None and isinstance(exc, (TimeoutError, urllib.error.URLError)))
            print(f'Transport: {type(exc).__name__}, HTTP={code}, attempt={attempt + 1}', flush=True)
            if not retryable or attempt == 2:
                raise
            delay = 30 * (attempt + 1)
            retry_after = getattr(exc, 'headers', {}).get('Retry-After')
            if retry_after:
                try:
                    delay = max(delay, float(retry_after))
                except ValueError:
                    pass
            if delay > 120:
                raise
            time.sleep(delay)

urllib.request.urlopen = patient_open
sys.argv = [str(ROOT / 'evals/run_evals.py'), *sys.argv[1:]]
runpy.run_path(sys.argv[0], run_name='__main__')
