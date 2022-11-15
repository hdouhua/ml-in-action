import os

#import pytest
from app.config import MODEL_FILE


def test_model_file_existent():
    assert os.path.exists(MODEL_FILE)
