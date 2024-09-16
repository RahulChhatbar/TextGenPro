import pytest
from app import local_generate_completion, append_completion, clear_fields, update_prompt


@pytest.mark.timeout(10)
def test_append_completion():
    prompt = "  Test prompt      "
    completion = "       generated result "
    new_prompt, new_completion = append_completion(prompt, completion)

    assert new_prompt != ""
    assert new_prompt == "Test prompt generated result"
    assert new_completion == ""
    print("Completed test_append_completion")


@pytest.mark.timeout(10)
def test_clear_fields():
    new_prompt, new_completion = clear_fields()

    assert new_prompt == ""
    assert new_completion == ""
    print("Completed test_clear_fields")


@pytest.mark.timeout(10)
def test_update_prompt():
    selected_example = "This is an example prompt"
    new_prompt, new_completion = update_prompt(selected_example)

    assert new_prompt == selected_example
    assert new_completion == ""
    print("Completed test_update_prompt")


@pytest.mark.timeout(10)
def test_local_generate_completion():
    prompt = "Test prompt"
    max_tokens = 100
    temperature = 0.7
    repetition_penalty = 1.5
    top_p = 0.9
    result = local_generate_completion(prompt, max_tokens, temperature, repetition_penalty, top_p)

    assert result != ""
    print("Completed test_local_generate_completion")
