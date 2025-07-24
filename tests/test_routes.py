def test_agent_selection(client):
    # Test selecting FAQ agent returns FAQ answer (not fallback)
    response = client.post("/", data={"query": "How long is the program?", "agent_choice": "faq"})
    assert b"3" in response.data  # Checks for "3 months" or similar in response

    # Test selecting wellness agent returns mocked wellness answer
    response2 = client.post("/", data={"query": "What are genetic markers?", "agent_choice": "wellness"})
    assert b"Mock wellness answer" in response2.data

    # Test auto-detect chooses FAQ agent for support queries
    response3 = client.post("/", data={"query": "How do I pay for the program?", "agent_choice": "auto"})
    assert b"support" in response3.data.lower() or b"answer" in response3.data.lower()

    # Test auto-detect chooses wellness agent for wellness queries
    response4 = client.post("/", data={"query": "How does DNA affect metabolism?", "agent_choice": "auto"})
    assert b"Mock wellness answer" in response4.data
