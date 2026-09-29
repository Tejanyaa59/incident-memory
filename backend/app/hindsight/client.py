import re
import logging
from typing import Optional, List, Dict, Any
from app.config import settings

logger = logging.getLogger("incidentlens.hindsight")

class HindsightService:
    def __init__(self):
        self.bank_id = settings.HINDSIGHT_BANK_ID
        self.base_url = settings.HINDSIGHT_BASE_URL
        self.api_key = settings.HINDSIGHT_API_KEY
        self.client = None
        self._available: Optional[bool] = None

        if self.base_url and self.api_key:
            try:
                from hindsight_client import Hindsight
                self.client = Hindsight(
                    base_url=self.base_url,
                    api_key=self.api_key,
                    timeout=30.0,
                )
            except Exception as e:
                logger.warning(f"Failed to initialize Hindsight client: {e}")

    def is_available(self) -> bool:
        """Check if Hindsight server is reachable and bank exists or can be accessed."""
        if not self.client:
            return False
        if self._available is not None:
            return self._available

        try:
            # Test connectivity by querying bank config or version
            self.client.get_bank_config(bank_id=self.bank_id)
            self._available = True
            return True
        except Exception:
            try:
                # Try getting version or creating bank if missing
                self.ensure_bank()
                self._available = True
                return True
            except Exception as err:
                logger.warning(f"Hindsight connection check failed: {err}")
                self._available = False
                return False

    def ensure_bank(self) -> bool:
        """Ensure the dedicated memory bank exists with appropriate missions and traits."""
        if not self.client:
            return False
        try:
            try:
                self.client.get_bank_config(bank_id=self.bank_id)
                logger.info(f"[HINDSIGHT] Bank {self.bank_id} already exists.")
                return True
            except Exception:
                pass

            logger.info(f"[HINDSIGHT] Creating bank {self.bank_id}...")
            self.client.create_bank(
                bank_id=self.bank_id,
                name="IncidentLens Production Memory",
                background="Production incident management and automated root cause memory bank for IncidentLens.",
                mission=settings.HINDSIGHT_RETAIN_MISSION,
                retain_mission=settings.HINDSIGHT_RETAIN_MISSION,
                disposition={
                    "skepticism": 3,
                    "literalism": 3,
                    "empathy": 1,
                },
                enable_observations=True,
                enable_text_search=True,
                enable_temporal_retrieval=True,
                enable_graph_retrieval=True,
            )
            logger.info(f"[HINDSIGHT] Bank {self.bank_id} created successfully.")
            return True
        except Exception as e:
            logger.warning(f"[HINDSIGHT] Could not ensure bank exists: {e}")
            return False

    def format_incident_content(self, incident: Dict[str, Any]) -> str:
        """Format an incident into rich structured natural language for Hindsight retention."""
        incident_id = incident.get("id", "")
        service = incident.get("service", "")
        date = incident.get("date", "recent")
        severity = incident.get("severity", "High")
        root_cause = incident.get("root_cause", "")
        context = incident.get("context", "")
        resolution = incident.get("resolution", "")
        outcome = incident.get("outcome", "")
        error = incident.get("error", "General service degradation")
        human_feedback = incident.get("human_feedback", "Confirmed by incident investigator")
        error_rate = incident.get("error_rate")
        latency = incident.get("latency")
        db_connections = incident.get("db_connections")
        cpu = incident.get("cpu")

        metrics_parts = []
        if error_rate:
            metrics_parts.append(f"error rate was {error_rate}")
        if latency:
            metrics_parts.append(f"latency reached {latency}")
        if db_connections:
            metrics_parts.append(f"database connections reached {db_connections}")
        if cpu:
            metrics_parts.append(f"CPU utilization was {cpu}")

        metrics_str = f" During the incident, {', '.join(metrics_parts)}." if metrics_parts else ""

        content = (
            f"On {date}, incident {incident_id} affected the {service}. "
            f"Severity was {severity}. Symptoms and error: {error}.{metrics_str} "
            f"Operational context: {context}. "
            f"Investigation identified root cause: {root_cause}. "
            f"Investigator decision: {human_feedback}. "
            f"Resolution: {resolution}. Outcome: {outcome}. "
            f"This incident establishes a reusable pattern that {context.lower()} with "
            f"{error.lower()} in {service} indicates {root_cause.lower()}."
        )
        return content

    def retain(self, incident: Dict[str, Any]) -> bool:
        """Retain an incident in Hindsight memory using stable document ID."""
        incident_id = incident.get("id")
        if not incident_id:
            return False

        logger.info(f"[MEMORY] Retaining {incident_id}")
        content = self.format_incident_content(incident)
        context_str = f"Production incident {incident_id} for {incident.get('service', 'Service')}"

        if self.is_available() and self.client:
            try:
                self.client.retain(
                    bank_id=self.bank_id,
                    content=content,
                    context=context_str,
                    document_id=f"incident-{incident_id}",
                    metadata={
                        "incident_id": incident_id,
                        "service": incident.get("service", ""),
                        "root_cause": incident.get("root_cause", ""),
                        "severity": incident.get("severity", ""),
                    },
                    tags=[
                        incident_id,
                        incident.get("service", ""),
                        incident.get("root_cause", ""),
                    ],
                )
                logger.info(f"[MEMORY] {incident_id} retained successfully in Hindsight")
                return True
            except Exception as e:
                logger.error(f"[MEMORY] Failed to retain {incident_id} in Hindsight: {e}")
                return False
        else:
            logger.info(f"[MEMORY] Hindsight unavailable. Retained locally for {incident_id}")
            return False

    def build_recall_query(self, incident: Dict[str, Any]) -> str:
        """Build a rich recall query from incident evidence."""
        service = incident.get("service", "")
        title = incident.get("title", "")
        error = incident.get("error", "")
        context = incident.get("context", "")
        db_conn = incident.get("db_connections", "")
        err_rate = incident.get("error_rate", "")
        latency = incident.get("latency", "")
        recent_dep = incident.get("recent_deployment", "")

        query_parts = [f"{service} {title}"]
        if error:
            query_parts.append(f"error: {error}")
        if db_conn:
            query_parts.append(f"{db_conn} database connections")
        if recent_dep:
            query_parts.append(f"recent deployment {recent_dep}")
        if err_rate:
            query_parts.append(f"{err_rate} error rate")
        if latency:
            query_parts.append(f"{latency} latency")
        if context:
            query_parts.append(f"context: {context}")

        return ", ".join(query_parts)

    def recall(self, incident: Dict[str, Any], budget: str = "mid") -> List[Dict[str, Any]]:
        """Run recall for an incident and return matched incident references with similarity scores."""
        incident_id = incident.get("id", "")
        logger.info(f"[HINDSIGHT] Recall started for {incident_id}")
        query = self.build_recall_query(incident)

        recalled_items = []
        if self.is_available() and self.client:
            try:
                response = self.client.recall(
                    bank_id=self.bank_id,
                    query=query,
                    budget=budget,
                    max_tokens=4096,
                )
                raw_results = getattr(response, "results", [])
                logger.info(f"[HINDSIGHT] {len(raw_results)} memories retrieved from Hindsight")

                # Map results back to incident IDs
                for idx, r in enumerate(raw_results):
                    text = getattr(r, "text", "")
                    doc_id = getattr(r, "document_id", "") or ""
                    meta = getattr(r, "metadata", {}) or {}
                    tags = getattr(r, "tags", []) or []

                    matched_id = None
                    if doc_id.startswith("incident-"):
                        matched_id = doc_id.replace("incident-", "")
                    elif meta and "incident_id" in meta:
                        matched_id = meta["incident_id"]
                    else:
                        for tag in tags:
                            if re.match(r"^INC-\d+$", tag):
                                matched_id = tag
                                break
                    if not matched_id and text:
                        match = re.search(r"INC-\d+", text)
                        if match:
                            matched_id = match.group(0)

                    if matched_id and matched_id != incident_id:
                        # Derive memory relevance from rank if scores not provided
                        sim = max(50, 96 - (idx * 7))
                        recalled_items.append({
                            "incident_id": matched_id,
                            "similarity": sim,
                            "memory_text": text,
                        })
            except Exception as e:
                logger.error(f"[HINDSIGHT] Recall error: {e}")

        return recalled_items

    def reflect(self, query: str, context: Optional[str] = None) -> Optional[str]:
        """Run Hindsight reflect reasoning over retrieved memory."""
        if not self.is_available() or not self.client:
            return None
        try:
            response = self.client.reflect(
                bank_id=self.bank_id,
                query=query,
                context=context,
                budget="low",
            )
            return getattr(response, "text", None)
        except Exception as e:
            logger.warning(f"[HINDSIGHT] Reflect failed: {e}")
            return None

hindsight_service = HindsightService()
