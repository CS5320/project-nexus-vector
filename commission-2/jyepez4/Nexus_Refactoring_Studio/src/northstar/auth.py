class AuthClient:
    def can_manage_customers(self, actor_role: str) -> bool:
        return actor_role in {"admin", "manager"}

    def can_run_reports(self, actor_role: str) -> bool:
        return actor_role in {"admin", "manager", "analyst"}
