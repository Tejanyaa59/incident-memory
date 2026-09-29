import pytest
from app.models.models import Incident, MemoryRecord

def test_hindsight_persistence_pipeline(client, db_session):
    """
    Demonstrate that memory persists and is retrievable:
    1. Seed 10 incidents
    2. Recall query for INC-104 returns INC-031, INC-052, INC-083
    3. Save INC-104 to memory
    4. Run recall query for a new incident or future query
    5. INC-104 is now part of retrievable organizational memory
    """
    # 1. 10 historical incidents seeded
    initial_memories = db_session.query(MemoryRecord).count()
    assert initial_memories == 10

    # 2. Recall query for INC-104
    inv_resp = client.post("/api/investigations/run", json={"incident_id": "INC-104"})
    assert inv_resp.status_code == 200
    recalled_ids = [m.get("incidentId") or m.get("incident_id") for m in inv_resp.json()["recalled_memories"]]
    assert "INC-031" in recalled_ids
    assert "INC-104" not in recalled_ids

    # 3. Save INC-104
    save_resp = client.post("/api/incidents/INC-104/memory", json={"decision": "confirm"})
    assert save_resp.status_code == 200
    assert db_session.query(MemoryRecord).count() == 11

    # 4. Check memory list endpoint
    mem_resp = client.get("/api/memory")
    assert mem_resp.status_code == 200
    memories = mem_resp.json()["memories"]
    all_memory_ids = [m["id"] for m in memories]
    assert "INC-104" in all_memory_ids

    # 5. Verify INC-104 is stored with rich organizational context
    inc_104_mem = db_session.query(MemoryRecord).filter(MemoryRecord.incident_id == "INC-104").first()
    assert inc_104_mem is not None
    assert "Database connection leak" in inc_104_mem.content
    assert "Payment API" in inc_104_mem.content
    assert "Rollback deployment" in inc_104_mem.content
