from __future__ import annotations
from datetime import date

class ReadinessService:
    def summarize(self, controls:list[dict], poams:list[dict], artifacts:list[dict], hardware:list[dict], software:list[dict], test_results:list[dict], workflows:list[dict]) -> list[dict]:
        overdue = sum(1 for p in poams if p.get('scheduledCompletion') and p.get('scheduledCompletion') < date.today().isoformat() and p.get('status','').lower() != 'completed')
        not_satisfied = sum(1 for c in controls if 'not' in str(c.get('complianceStatus','')).lower())
        return [
            {'report':'open_poams','description':str(sum(1 for p in poams if p.get('status','').lower() not in {'completed','closed'}))},
            {'report':'overdue_poams','description':str(overdue)},
            {'report':'controls_not_satisfied','description':str(not_satisfied)},
            {'report':'missing_artifacts_placeholder','description':'Advisory placeholder'},
            {'report':'stale_test_results_placeholder','description':'Advisory placeholder'},
            {'report':'empty_hardware_baseline','description':str(not bool(hardware))},
            {'report':'empty_software_baseline','description':str(not bool(software))},
            {'report':'active_workflow_status','description':workflows[0].get('status','None') if workflows else 'None'},
        ]
