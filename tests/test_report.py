import os
import re
import pytest

REPORT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'report.md'))

def get_report_content():
    if not os.path.exists(REPORT_PATH):
        raise AssertionError(f"report.md was not found at {REPORT_PATH}")
    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def get_section_discussion_answer(question_keyword, content):
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if question_keyword in line and '**' in line:
            answer_lines = []
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line.startswith('-') or next_line.startswith('##') or next_line.startswith('---'):
                    break
                if next_line:
                    answer_lines.append(next_line)
            return '\n'.join(answer_lines)
    return None

@pytest.mark.weight(5)
@pytest.mark.number("2.1")
def test_student_information():
    """report.md: Student Information check"""
    content = get_report_content()
    name_match = re.search(r'-\s*\*\*Name:\*\*\s*(.*)', content)
    mmdt_id_match = re.search(r'-\s*\*\*MMDT ID:\*\*\s*(.*)', content)
    
    assert name_match is not None, "Name field not found under Student Information"
    assert mmdt_id_match is not None, "MMDT ID field not found under Student Information"
    
    name = name_match.group(1).strip()
    mmdt_id = mmdt_id_match.group(1).strip()
    
    assert name and name != "[Write your Name here]", "Student Name must be filled out"
    assert not (name.startswith("[") and name.endswith("]")), "Student Name cannot contain placeholder text"
    
    assert mmdt_id and mmdt_id != "[Write your MMDT ID here]", "MMDT ID must be filled out"
    assert not (mmdt_id.startswith("[") and mmdt_id.endswith("]")), "MMDT ID cannot contain placeholder text"

@pytest.mark.weight(5)
@pytest.mark.number("2.2")
def test_agent_configuration():
    """report.md: AI Agent Configuration check"""
    content = get_report_content()
    alg_match = re.search(r'-\s*\*\*Primary AI Algorithm:\*\*\s*(.*)', content)
    prune_match = re.search(r'-\s*\*\*Pruning Technique:\*\*\s*(.*)', content)
    heur_match = re.search(r'-\s*\*\*Heuristic Strategy:\*\*\s*(.*)', content)

    assert alg_match is not None, "Primary AI Algorithm field not found"
    assert prune_match is not None, "Pruning Technique field not found"
    assert heur_match is not None, "Heuristic Strategy field not found"

    alg = alg_match.group(1).strip()
    prune = prune_match.group(1).strip()
    heur = heur_match.group(1).strip()

    assert alg and not alg.startswith("["), "Primary AI Algorithm must be filled out"
    assert prune and not prune.startswith("["), "Pruning Technique must be filled out"
    assert heur and not heur.startswith("["), "Heuristic Strategy must be filled out"

@pytest.mark.weight(5)
@pytest.mark.number("2.3")
def test_game_tree_complexity():
    """report.md: Complexity & Search Tree Analysis check"""
    content = get_report_content()
    depth_match = re.search(r'-\s*\*\*Maximum Search Depth \(Empty 3x3 Board\):\*\*\s*(.*)', content)
    states_match = re.search(r'-\s*\*\*Total Possible Board States:\*\*\s*(.*)', content)
    unbeatable_match = re.search(r'-\s*\*\*Unbeatable Minimax Guarantee:\*\*\s*(.*)', content)

    assert depth_match is not None, "Maximum Search Depth field not found"
    assert states_match is not None, "Total Possible Board States field not found"
    assert unbeatable_match is not None, "Unbeatable Minimax Guarantee field not found"

    depth_raw = depth_match.group(1).strip()
    states_raw = states_match.group(1).strip()
    unbeatable_raw = unbeatable_match.group(1).strip()

    assert depth_raw and not depth_raw.startswith("["), "Maximum Search Depth must be filled out"
    assert states_raw and not states_raw.startswith("["), "Total Possible Board States must be filled out"
    assert unbeatable_raw and not unbeatable_raw.startswith("["), "Unbeatable Minimax Guarantee must be filled out"

    depth_val = re.search(r'\d+', depth_raw)
    assert depth_val is not None, "Maximum Search Depth must contain a numeric value"
    
    unbeatable = unbeatable_raw.lower()
    assert "yes" in unbeatable or "no" in unbeatable, "Unbeatable Minimax Guarantee must be answered with 'Yes' or 'No'"

@pytest.mark.weight(5)
@pytest.mark.number("2.4")
def test_local_verification_checked():
    """report.md: Verification checklist"""
    content = get_report_content()
    checked_algs = re.findall(r'-\s*\[[xX]\]\s*(.*)', content)
    assert len(checked_algs) >= 3, "At least 3 features/algorithms must be marked verified with [x]"

@pytest.mark.weight(5)
@pytest.mark.number("2.5")
def test_deployment_and_presentation():
    """report.md: Deployed and Presentation Information check"""
    content = get_report_content()
    platform_match = re.search(r'-\s*\*\*Deployment Platform:\*\*\s*(.*)', content)
    url_match = re.search(r'-\s*\*\*Live Deployment URL:\*\*\s*(.*)', content)
    video_match = re.search(r'-\s*\*\*Video Presentation Link:\*\*\s*(.*)', content)

    assert platform_match is not None, "Deployment Platform field not found"
    assert url_match is not None, "Live Deployment URL field not found"
    assert video_match is not None, "Video Presentation Link field not found"

    platform = platform_match.group(1).strip()
    url = url_match.group(1).strip()
    video = video_match.group(1).strip()

    assert platform and not platform.startswith("["), "Deployment Platform must be filled out"
    assert url and not url.startswith("["), "Live Deployment URL must be filled out"
    assert video and not video.startswith("["), "Video Presentation Link must be filled out"

@pytest.mark.weight(5)
@pytest.mark.number("2.6")
def test_discussion_answers():
    """report.md: Discussion answers check"""
    content = get_report_content()
    ans1 = get_section_discussion_answer("Alpha-Beta pruning", content)
    ans2 = get_section_discussion_answer("Generative AI", content)

    assert ans1 is not None and len(ans1.split()) >= 15, "Discussion Question 1 answer must be completed (at least 15 words)"
    assert ans2 is not None and len(ans2.split()) >= 15, "Discussion Question 2 answer must be completed (at least 15 words)"
