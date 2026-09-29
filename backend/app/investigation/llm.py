import logging
import httpx
from typing import Optional, Dict, Any, List
from app.config import settings

logger = logging.getLogger("incidentlens.llm")

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower() if settings.LLM_PROVIDER else ""
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL or ("llama-3.3-70b-versatile" if self.provider == "groq" else "gpt-4o-mini")

    def is_configured(self) -> bool:
        return bool(self.api_key and self.provider)

    def synthesize_investigation(
        self,
        incident: Dict[str, Any],
        recalled_memories: List[Dict[str, Any]],
        structured_evidence: List[str],
        base_root_cause: str,
        base_confidence: int,
    ) -> Optional[Dict[str, Any]]:
        """Optional LLM synthesis of the final investigation summary and recommendations."""
        if not self.is_configured():
            return None

        prompt = (
            f"You are IncidentLens, an AI incident investigator. Investigate incident {incident.get('id')} ({incident.get('title')}) "
            f"for service {incident.get('service')}.\n\n"
            f"Evidence:\n"
            f"- Error: {incident.get('error')}\n"
            f"- DB Connections: {incident.get('db_connections')}\n"
            f"- Error Rate: {incident.get('error_rate')}\n"
            f"- Latency: {incident.get('latency')}\n"
            f"- Recent Deployment: {incident.get('recent_deployment')}\n\n"
            f"Recalled Historical Memories from Hindsight:\n"
            + "\n".join([f"- Incident {m.get('incident_id')}: {m.get('title')} ({m.get('root_cause')}) -> {m.get('resolution')}" for m in recalled_memories])
            + f"\n\nBaseline Diagnosis: {base_root_cause} with {base_confidence}% confidence.\n"
            f"Provide a grounded explanation without claiming 100% certainty. Use phrasing like 'likely', 'evidence suggests'."
        )

        try:
            if self.provider == "groq":
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a professional SRE incident investigator."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 500,
                }
                with httpx.Client(timeout=10.0) as client:
                    resp = client.post(url, headers=headers, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        explanation = data["choices"][0]["message"]["content"]
                        return {"explanation": explanation}
            elif self.provider in ["openai", "open_ai"]:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a professional SRE incident investigator."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 500,
                }
                with httpx.Client(timeout=10.0) as client:
                    resp = client.post(url, headers=headers, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        explanation = data["choices"][0]["message"]["content"]
                        return {"explanation": explanation}
        except Exception as e:
            logger.warning(f"LLM synthesis call failed: {e}")

        return None

llm_service = LLMService()
