import pytest
from app.models.models import Incident, LearnedPattern, MemoryRecord, InvestigatorFeedback

def test_1_health_endpoint(client):
    """1. Health endpoint returns valid status."""
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "database" in data
    assert data["database"] == "connected"

def test_2_seed_creates_10_historical_incidents(client, db_session):
    """2. Seed creates exactly 10 historical incidents."""
    resolved = db_session.query(Incident).filter(Incident.status == "Resolved").all()
    assert len(resolved) == 10

def test_3_seed_creates_1_active_incident(client, db_session):
    """3. Seed creates exactly 1 active incident."""
    active = db_session.query(Incident).filter(Incident.status == "Active").all()
    assert len(active) == 1
    assert active[0].id == "INC-104"

def test_4_no_duplicate_incident_ids(client, db_session):
    """4. No duplicate incident IDs exist."""
    all_incidents = db_session.query(Incident).all()
    ids = [inc.id for inc in all_incidents]
    assert len(ids) == len(set(ids))
    assert len(ids) == 11

def test_5_inc_104_exists(client, db_session):
    """5. INC-104 exists with expected attributes."""
    inc = db_session.query(Incident).filter(Incident.id == "INC-104").first()
    assert inc is not None
    assert inc.service == "Payment API"
    assert inc.severity == "Critical"
    assert inc.status == "Active"

def test_6_investigation_endpoint_works(client):
    """6. Investigation endpoint works."""
    resp = client.post("/api/investigations/run", json={"incident_id": "INC-104"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["incident"]["id"] == "INC-104"
    assert "likely_root_cause" in data["investigation"] or "likelyRootCause" in data["investigation"]
    assert data["confidence"] == 89

def test_7_8_hindsight_recall_and_three_memories(client):
    """7 & 8. Hindsight recall is invoked and returns 3 relevant memories for INC-104."""
    resp = client.post("/api/investigations/run", json={"incident_id": "INC-104"})
    assert resp.status_code == 200
    data = resp.json()
    recalled = data["recalled_memories"]
    assert len(recalled) == 3
    recalled_ids = [m.get("incidentId") or m.get("incident_id") for m in recalled]
    assert "INC-031" in recalled_ids
    assert "INC-052" in recalled_ids
    assert "INC-083" in recalled_ids

def test_9_confirm_feedback_works(client, db_session):
    """9. Confirm feedback works."""
    resp = client.post(
        "/api/incidents/INC-104/feedback",
        json={"decision": "confirm", "notes": "Confirmed by SRE on duty"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["decision"] == "confirm"
    inc = db_session.query(Incident).filter(Incident.id == "INC-104").first()
    assert "Confirmed" in inc.human_feedback

def test_10_save_memory_works(client, db_session):
    """10. Save memory works."""
    resp = client.post(
        "/api/incidents/INC-104/memory",
        json={"decision": "confirm", "notes": "Deployment rolled back"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["incident"]["status"] == "Resolved"

def test_11_save_twice_idempotency_no_duplicate(client, db_session):
    """11. Saving INC-104 twice does not create duplicate memory."""
    resp1 = client.post("/api/incidents/INC-104/memory", json={"decision": "confirm"})
    assert resp1.status_code == 200
    resp2 = client.post("/api/incidents/INC-104/memory", json={"decision": "confirm"})
    assert resp2.status_code == 200
    assert resp2.json()["already_exists"] is True

    # Check database memory records count
    mem_records = db_session.query(MemoryRecord).filter(MemoryRecord.incident_id == "INC-104").all()
    assert len(mem_records) == 1

def test_12_13_14_stats_change_10_to_11_and_corrections_zero(client):
    """12, 13, 14. Memory count: 10->11, Confirmed: 10->11, Corrections: 0."""
    stats_before = client.get("/api/dashboard/stats").json()
    assert stats_before["hindsight_memories"] == 10
    assert stats_before["confirmed_outcomes"] == 10
    assert stats_before["investigator_corrections"] == 0
    assert stats_before["active_incidents"] == 1

    # Save INC-104
    client.post("/api/incidents/INC-104/memory", json={"decision": "confirm"})

    stats_after = client.get("/api/dashboard/stats").json()
    assert stats_after["hindsight_memories"] == 11
    assert stats_after["confirmed_outcomes"] == 11
    assert stats_after["investigator_corrections"] == 0
    assert stats_after["active_incidents"] == 0

def test_15_correction_flow_increments_corrections(client, db_session):
    """15. Correction flow increments corrections."""
    # Reset/seed for fresh state is done per fixture
    resp = client.post(
        "/api/incidents/INC-104/feedback",
        json={
            "decision": "correct",
            "rootCause": "Configuration regression",
            "notes": "Was actually bad pool config",
        },
    )
    assert resp.status_code == 200
    fb_count = db_session.query(InvestigatorFeedback).filter(InvestigatorFeedback.decision == "correct").count()
    assert fb_count == 1
    stats = client.get("/api/dashboard/stats").json()
    assert stats["investigator_corrections"] == 1

def test_16_history_changes_correctly(client):
    """16. History returns 10 initially, and 11 after INC-104 is resolved."""
    hist_before = client.get("/api/history").json()
    assert len(hist_before) == 10

    client.post("/api/incidents/INC-104/memory", json={"decision": "confirm"})

    hist_after = client.get("/api/history").json()
    assert len(hist_after) == 11
    ids = [h["id"] for h in hist_after]
    assert "INC-104" in ids

def test_17_learned_pattern_reinforced(client, db_session):
    """17. Learned pattern PAT-01 is reinforced after confirming INC-104."""
    pat_before = db_session.query(LearnedPattern).filter(LearnedPattern.id == "PAT-01").first()
    assert pat_before.confirmed == 3
    assert pat_before.successful == 3

    client.post("/api/incidents/INC-104/memory", json={"decision": "confirm"})

    db_session.expire_all()
    pat_after = db_session.query(LearnedPattern).filter(LearnedPattern.id == "PAT-01").first()
    assert pat_after.confirmed == 4
    assert pat_after.successful == 4
