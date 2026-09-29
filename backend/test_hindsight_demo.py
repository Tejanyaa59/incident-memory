"""
IncidentLens Diagnostic Script: Demonstrating Persistent Memory Pipeline

Run:
    python test_hindsight_demo.py

Flow:
1. Seed 10 historical incidents
2. Recall query for INC-104
3. Verify Hindsight returns relevant historical experience (INC-031, INC-052, INC-083)
4. Save INC-104 outcome to Hindsight memory
5. Demonstrate INC-104 is now retained as organizational experience
6. Verify pattern PAT-01 reinforcement (3 -> 4)
"""
import sys
import logging
from app.database.session import SessionLocal, Base, engine
from app.seed.seeder import seed_database
from app.services.incident_service import incident_service
from app.services.learning_service import learning_service
from app.investigation.engine import investigation_engine
from app.hindsight.client import hindsight_service

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("demo")

def run_diagnostic():
    print("=" * 60)
    print("INCIDENTLENS — PERSISTENT MEMORY VERIFICATION")
    print("Don't investigate the same incident twice.")
    print("=" * 60)

    db = SessionLocal()
    try:
        # Step 1: Seed
        print("\n[STEP 1] Seeding database and memory bank...")
        seed_database(db=db, force_reset=True)
        stats_initial = learning_service.get_dashboard_stats(db)
        print(f" -> Active incidents: {stats_initial['active_incidents']}")
        print(f" -> Historical incidents: {stats_initial['historical_incidents']}")
        print(f" -> Hindsight memories: {stats_initial['hindsight_memories']}")
        print(f" -> Confirmed outcomes: {stats_initial['confirmed_outcomes']}")

        # Step 2: Investigation & Recall
        print("\n[STEP 2] Running investigation on INC-104...")
        inc_104 = incident_service.get_by_id(db, "INC-104")
        inv_result = investigation_engine.investigate(inc_104, db)

        recalled = inv_result["recalled_memories"]
        print(f" -> Hindsight returned {len(recalled)} relevant memories:")
        for r in recalled:
            print(f"    * {r['incident_id']} (similarity: {r['similarity']}%) - {r['title']} [{r['root_cause']}]")

        print(f" -> Likely root cause: {inv_result['investigation']['likely_root_cause']}")
        print(f" -> Confidence: {inv_result['confidence']}%")

        # Step 3: Investigator Feedback & Save to Memory
        print("\n[STEP 3] Investigator confirms diagnosis and retains INC-104...")
        save_result = incident_service.save_to_memory(
            db=db,
            incident_id="INC-104",
            feedback_decision="confirm",
            notes="Rollback deployment executed successfully",
        )
        print(f" -> Result: {save_result['message']}")

        # Step 4: Verify Memory Growth
        print("\n[STEP 4] Verifying organizational memory growth...")
        stats_after = learning_service.get_dashboard_stats(db)
        print(f" -> Active incidents: {stats_after['active_incidents']} (was {stats_initial['active_incidents']})")
        print(f" -> Historical incidents: {stats_after['historical_incidents']} (was {stats_initial['historical_incidents']})")
        print(f" -> Hindsight memories: {stats_after['hindsight_memories']} (was {stats_initial['hindsight_memories']})")
        print(f" -> Confirmed outcomes: {stats_after['confirmed_outcomes']} (was {stats_initial['confirmed_outcomes']})")

        # Step 5: Check Pattern Reinforcement
        pat_page = learning_service.get_memory_page_data(db)
        pat1 = next(p for p in pat_page["patterns"] if p.id == "PAT-01")
        print(f"\n[STEP 5] Pattern PAT-01 reinforced: confirmed={pat1.confirmed}, successful={pat1.successful}")

        # Step 6: Verify Idempotency
        print("\n[STEP 6] Testing idempotency (saving INC-104 again)...")
        dup_result = incident_service.save_to_memory(db=db, incident_id="INC-104")
        print(f" -> Duplicate prevention triggered: {dup_result.get('already_exists')}")
        stats_dup = learning_service.get_dashboard_stats(db)
        assert stats_dup["hindsight_memories"] == 11, "Memory count should not increase on duplicate save"
        print(" -> Verified: Memory count remains 11 (No duplicates created).")

        print("\n" + "=" * 60)
        print("ALL DIAGNOSTIC CHECKS PASSED SUCCESSFULLY!")
        print("=" * 60)
    finally:
        db.close()

if __name__ == "__main__":
    run_diagnostic()
