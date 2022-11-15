import os

#import pytest
from app.config import MODEL_FILE


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4


def test_model_file_existent():
    assert os.path.exists(MODEL_FILE)
