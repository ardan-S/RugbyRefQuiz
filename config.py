import os
import tempfile

from cachelib.file import FileSystemCache


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # Server-side sessions: quiz state (question IDs, score, missed answers)
    # is too large for the 4KB cookie limit.
    SESSION_TYPE = 'cachelib'
    SESSION_CACHELIB = FileSystemCache(
        cache_dir=os.path.join(tempfile.gettempdir(), 'rugbyrefquiz-sessions'),
        threshold=500,
    )
    SESSION_PERMANENT = False
