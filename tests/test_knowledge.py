from pathlib import Path

import pytest

from assistant_core.errors import DataError
from assistant_core.knowledge import Handbook, OfficeDirectory


def test_office_directory_success(tmp_path):

    csv_file = tmp_path / "offices.csv"
    csv_file.write_text("name,room,hours\nTraining,I.101,07:30-16:30\nLibrary,Floor 2,08:00-17:00\n", encoding="utf-8")
    
    directory = OfficeDirectory.from_csv(csv_file)
    
    assert len(directory.names) == 2
    assert "training" in directory.names
    
    # Test tìm thấy
    office = directory.find("where is training office?")
    assert office is not None
    assert office.room == "I.101"
    
    # Test không tìm thấy
    assert directory.find("canteen") is None

def test_office_directory_missing():
    with pytest.raises(DataError):
        OfficeDirectory.from_csv(Path("fake_offices.csv"))

def test_handbook_success(tmp_path):

    json_file = tmp_path / "handbook.json"
    json_data = '[{"id": "rule_1", "title": "Thesis", "text": "Register with 118 credits"}]'
    json_file.write_text(json_data, encoding="utf-8")
    
    handbook = Handbook.from_json(json_file)
    
    # Test search trúng từ khóa
    rule = handbook.search("I have 118 credits for thesis")
    assert rule is not None
    assert rule.id == "rule_1"
    
    # Test search trượt
    assert handbook.search("parking rules") is None

def test_handbook_missing():
    with pytest.raises(DataError):
        Handbook.from_json(Path("fake_handbook.json"))