from scripts.page_generator import render_page

def test_render_page(mock_llm_client, mock_affiliate_manager):
    # Simple smoke test
    content = render_page("Test Topic", "Test content")
    assert content is not None
    assert "Test Topic" in content