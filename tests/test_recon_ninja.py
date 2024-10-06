import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path to import recon_ninja
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import recon_ninja

@pytest.fixture
def app():
    recon_ninja.app.config['TESTING'] = True
    return recon_ninja.app.test_client()

def test_index_route(app):
    response = app.get('/')
    assert response.status_code == 200
    assert b"Welcome to ReconNINJ@" in response.data

def test_is_windows_route(app):
    response = app.get('/api/is_windows')
    assert response.status_code == 200
    assert "is_windows" in response.json

@patch('recon_ninja.get_registry_key_value')
def test_registry_key_route(mock_get_registry, app):
    mock_get_registry.return_value = "test_value"
    response = app.post('/api/registry_key', json={
        "key": "TEST_KEY",
        "value_name": "TEST_VALUE"
    })
    assert response.status_code == 200
    assert response.json["result"] == "test_value"

    # Test missing parameters
    response = app.post('/api/registry_key', json={})
    assert response.status_code == 400
    assert "error" in response.json

@patch('recon_ninja.compare_version')
def test_compare_version_route(mock_compare, app):
    mock_compare.return_value = "Versions are equal"
    response = app.post('/api/compare_version', json={
        "current_version": "1.0.0",
        "target_version": "1.0.0"
    })
    assert response.status_code == 200
    assert response.json["result"] == "Versions are equal"

    # Test missing parameters
    response = app.post('/api/compare_version', json={})
    assert response.status_code == 400
    assert "error" in response.json

@patch('recon_ninja.read_xml_file')
def test_read_xml_route(mock_read_xml, app):
    mock_read_xml.return_value = ("XML read successfully", "<root></root>")
    response = app.post('/api/read_xml', json={
        "file_path": "test.xml"
    })
    assert response.status_code == 200
    assert response.json["result"] == "XML read successfully"
    assert response.json["content"] == "<root></root>"

    # Test missing parameters
    response = app.post('/api/read_xml', json={})
    assert response.status_code == 400
    assert "error" in response.json

@patch('recon_ninja.write_xml_file')
def test_write_xml_route(mock_write_xml, app):
    mock_write_xml.return_value = "XML written successfully"
    response = app.post('/api/write_xml', json={
        "file_path": "test.xml",
        "xml_content": "<root></root>"
    })
    assert response.status_code == 200
    assert response.json["result"] == "XML written successfully"

    # Test missing parameters
    response = app.post('/api/write_xml', json={})
    assert response.status_code == 400
    assert "error" in response.json

@patch('recon_ninja.modify_xml_file')
def test_modify_xml_route(mock_modify_xml, app):
    mock_modify_xml.return_value = "XML modified successfully"
    response = app.post('/api/modify_xml', json={
        "file_path": "test.xml",
        "xpath": "/root/element",
        "new_value": "new_value"
    })
    assert response.status_code == 200
    assert response.json["result"] == "XML modified successfully"

    # Test missing parameters
    response = app.post('/api/modify_xml', json={})
    assert response.status_code == 400
    assert "error" in response.json

@patch('recon_ninja.manage_admin_permissions')
def test_admin_permissions_route(mock_manage_permissions, app):
    mock_manage_permissions.return_value = "Admin permissions granted to test_user"
    response = app.post('/api/admin_permissions', json={
        "username": "test_user",
        "action": "grant"
    })
    assert response.status_code == 200
    assert response.json["result"] == "Admin permissions granted to test_user"

    # Test missing parameters
    response = app.post('/api/admin_permissions', json={})
    assert response.status_code == 400
    assert "error" in response.json

@patch('recon_ninja.execute_program')
def test_execute_program_route(mock_execute, app):
    mock_execute.return_value = "Program executed successfully"
    response = app.post('/api/execute_program', json={
        "program_name": "test_program",
        "args": ["arg1", "arg2"]
    })
    assert response.status_code == 200
    assert response.json["result"] == "Program executed successfully"

    # Test missing parameters
    response = app.post('/api/execute_program', json={})
    assert response.status_code == 400
    assert "error" in response.json

def test_regenerate_structure():
    with patch('os.path.exists', return_value=False), \
         patch('os.makedirs') as mock_makedirs, \
         patch('builtins.open', MagicMock()) as mock_open:
        recon_ninja.regenerate_structure()
        assert mock_makedirs.called
        assert mock_open.called

@patch('time.sleep')
def test_start_random_delay(mock_sleep):
    recon_ninja.start_random_delay()
    assert mock_sleep.called

@patch('platform.system', return_value='Linux')
@patch('builtins.open', MagicMock())
def test_check_uptime_linux(mock_system):
    uptime = recon_ninja.check_uptime()
    assert isinstance(uptime, float)

@patch('requests.get')
def test_self_regenerate(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "new script content"
    with patch('builtins.open', MagicMock()), \
         patch('os.execv') as mock_execv:
        recon_ninja.SCRIPT_URL = "http://example.com/script"
        recon_ninja.self_regenerate()
        assert mock_execv.called

def test_find_free_port():
    port = recon_ninja.find_free_port()
    assert isinstance(port, int)
    assert port > 0

if __name__ == '__main__':
    pytest.main()
