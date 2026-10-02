import os
import pytest

@pytest.mark.weight(10)
@pytest.mark.number("1.1")
def test_submitted_files(request):
    """Check that all required files and directories under project directory exist"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    expected_files = [
        'app.py',
        'game.py',
        'agent.py',
        'templates/index.html',
        'requirements.txt',
        'report.md',
        'AI_declaration.png'
    ]
    
    missing_files = []
    existing_files = []
    for relative_path in expected_files:
        full_path = os.path.join(project_root, relative_path)
        if not os.path.exists(full_path):
            missing_files.append(relative_path)
        else:
            existing_files.append(relative_path)
            
    earned = int(round(10.0 * len(existing_files) / len(expected_files)))
    request.node._earned_points = earned
    
    assert len(missing_files) == 0, f"Missing required files/directories under project directory: {missing_files}"
    print("All required files present!")
