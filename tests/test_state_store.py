from ollama_network.service import NetworkService
from ollama_network.state_store import LocalStateStore


def test_private_state_persists_issued_identity_and_balance(tmp_path) -> None:
    store = LocalStateStore(tmp_path / "private_state.json")

    service = NetworkService(state_store=store)
    issued = service.issue_user_identity(starting_credits=7.0)
    user_id = issued["user_id"]

    reloaded = NetworkService(state_store=store)
    loaded = reloaded.get_user(user_id)
    context = reloaded.get_identity_context()

    assert loaded["user_id"] == user_id
    assert loaded["balance"] == 7.0
    assert context["auto_selected_user_id"] == user_id
