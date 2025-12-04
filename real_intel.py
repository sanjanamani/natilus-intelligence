# real_intel.py - REAL DATA for immediate impact
from datetime import datetime
from simple_db import SimpleSupabase


class RealIntelligence:
    def __init__(self):
        self.db = SimpleSupabase()

    def add_real_talent(self):
        """Add ACTUAL Boeing / Spirit style talent pools"""

        real_talent = [
            {
                "name": "Boeing 787 Composite Team",
                "current_company": "Boeing",
                "location": "Charleston, SC",
                "title": "Composite Engineers - 787 Program",
                "years_experience": 12,
                "is_open_to_work": True,
                "priority_score": 95,
                "skills": "787 composite fuselage, autoclave, carbon fiber",
                "notes": "Charleston facility downsizing",
                "risk_of_poaching": "HIGH",
            },
            {
                "name": "Boeing Cert Specialists",
                "current_company": "Boeing",
                "location": "Seattle, WA",
                "title": "FAA DER Certification Engineers",
                "years_experience": 15,
                "is_open_to_work": True,
                "priority_score": 98,
                "skills": "Part 23/25 certification, FAA liaison",
                "notes": "CRITICAL HIRE - These people know FAA process",
                "risk_of_poaching": "HIGH",
            },
            {
                "name": "Spirit Quality Team",
                "current_company": "Spirit AeroSystems",
                "location": "Wichita, KS",
                "title": "Quality & Manufacturing Engineers",
                "years_experience": 8,
                "is_open_to_work": True,
                "priority_score": 85,
                "skills": "AS9100, composite manufacturing, lean",
                "notes": "Spirit bankruptcy risk - immediate availability",
                "risk_of_poaching": "HIGH",
            },
        ]

        self.db.insert_talent(real_talent)
        print(f"✅ Added {len(real_talent)} REAL talent pools")
        return real_talent

    def add_real_competition(self):
        """Add MANUAL competitor moves into competitor_news table.

        competitor_news columns:
        - company
        - news_type
        - details
        - impact_on_natilus
        - date_detected
        """

        now = datetime.utcnow().isoformat()

        moves = [
            {
                "company": "JetZero",
                "news_type": "Strategic Partnership",
                "details": "JetZero expanding BWB partnerships with USAF-facing stakeholders.",
                "impact_on_natilus": "HIGH - Direct blended wing competitor with USAF interest.",
                "date_detected": now,
            },
            {
                "company": "JetZero",
                "news_type": "Talent Move",
                "details": "JetZero rumored to be hiring ex-Boeing aerodynamic / structures engineers.",
                "impact_on_natilus": "MEDIUM - Signals talent flow out of Boeing into BWB ecosystem.",
                "date_detected": now,
            },
            {
                "company": "Archer Aviation",
                "news_type": "Funding / Certification",
                "details": "Archer continues to de-risk type certification for eVTOL; investors more comfortable with hardware + certification risk.",
                "impact_on_natilus": "MEDIUM - Helpful proof-point that investors will back complex cert programs.",
                "date_detected": now,
            },
            {
                "company": "Joby Aviation",
                "news_type": "Manufacturing",
                "details": "Joby scaling advanced composites manufacturing for high-rate production.",
                "impact_on_natilus": "LOW - Indirect signal that large-scale composite production is fundable.",
                "date_detected": now,
            },
        ]

        self.db.insert_competitor_news(moves)
        print(f"✅ Added {len(moves)} REAL competitor moves")
        return moves

    def add_critical_insights(self):
        """Local-only insights object (not stored in DB yet)."""

        insights = {
            "series_a_intel": [
                {
                    "insight": "Deep tech / defense investors are aggressively backing hardware with clear wedge (Anduril, Shield AI, Hadrian).",
                    "action": "Position Natilus as the BWB logistics infra layer with both defense and cargo upside.",
                    "urgency": "HIGH",
                },
                {
                    "insight": "USAF and DoD are increasingly open to non-traditional primes for experimentation.",
                    "action": "Shape narrative around Natilus as the BWB cargo demonstrator partner of choice.",
                    "urgency": "MEDIUM",
                },
            ],
            "talent_intel": [
                {
                    "insight": "Boeing / Spirit uncertainty is pushing senior engineers to quietly explore options.",
                    "action": "Host invite-only Natilus deep-dive in Seattle and Wichita aimed at systems, cert, and composites talent.",
                    "urgency": "CRITICAL",
                }
            ],
            "supply_chain": [
                {
                    "insight": "Single-source fuselage / large-structure risk is no longer acceptable to investors.",
                    "action": "Show a clear dual-sourcing / backup plan for major composite and systems suppliers.",
                    "urgency": "HIGH",
                }
            ],
        }

        return insights


if __name__ == "__main__":
    intel = RealIntelligence()

    print("Adding REAL intelligence...")
    intel.add_real_talent()
    intel.add_real_competition()
    insights = intel.add_critical_insights()

    print("\n🎯 CRITICAL INSIGHTS ADDED (local object, not in DB):")
    for category, items in insights.items():
        print(f"\n{category.upper()}:")
        for item in items:
            print(f"  - {item['insight']}")
            print(f"    ACTION: {item['action']}")
