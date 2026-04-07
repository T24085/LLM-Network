from __future__ import annotations

from collections import defaultdict

from .models import CreditHold, CreditTransaction


class CreditLedger:
    """Tracks balances and job reservations for reciprocal compute credits."""

    def __init__(self) -> None:
        self._balances: dict[str, float] = defaultdict(float)
        self._holds: dict[str, CreditHold] = {}
        self._transactions: list[CreditTransaction] = []

    def register_user(self, user_id: str, starting_credits: float = 0.0) -> None:
        if user_id not in self._balances:
            self._balances[user_id] = 0.0
        if starting_credits:
            self.deposit(
                user_id=user_id,
                amount=starting_credits,
                reason="bootstrap credits",
                reference_id=user_id,
            )

    def balance_of(self, user_id: str) -> float:
        return round(self._balances[user_id], 4)

    def has_user(self, user_id: str) -> bool:
        return user_id in self._balances

    def hold_amount(self, job_id: str) -> float:
        return self._holds[job_id].amount

    def reserve(self, user_id: str, job_id: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Reservation amount must be positive.")
        if self._balances[user_id] < amount:
            raise ValueError(
                f"User '{user_id}' has {self._balances[user_id]:.4f} credits, which is not enough to reserve {amount:.4f}."
            )
        self._balances[user_id] -= amount
        self._holds[job_id] = CreditHold(job_id=job_id, user_id=user_id, amount=amount)
        self._transactions.append(
            CreditTransaction(
                user_id=user_id,
                delta=-amount,
                reason="job reservation",
                reference_id=job_id,
            )
        )

    def deposit(self, user_id: str, amount: float, reason: str, reference_id: str) -> None:
        if amount < 0:
            raise ValueError("Deposit amount must be non-negative.")
        self._balances[user_id] += amount
        self._transactions.append(
            CreditTransaction(
                user_id=user_id,
                delta=amount,
                reason=reason,
                reference_id=reference_id,
            )
        )

    def release(self, job_id: str, reason: str) -> float:
        hold = self._holds.pop(job_id)
        self._balances[hold.user_id] += hold.amount
        self._transactions.append(
            CreditTransaction(
                user_id=hold.user_id,
                delta=hold.amount,
                reason=reason,
                reference_id=job_id,
            )
        )
        return hold.amount

    def settle(self, job_id: str, worker_user_id: str, amount_to_worker: float) -> tuple[float, float]:
        hold = self._holds.pop(job_id)
        if amount_to_worker < 0 or amount_to_worker > hold.amount:
            raise ValueError("Settlement amount must be between zero and the held credits.")
        refund = round(hold.amount - amount_to_worker, 4)
        if amount_to_worker:
            self.deposit(
                user_id=worker_user_id,
                amount=amount_to_worker,
                reason="served public Ollama job",
                reference_id=job_id,
            )
        if refund:
            self.deposit(
                user_id=hold.user_id,
                amount=refund,
                reason="unused reserved credits",
                reference_id=job_id,
            )
        return round(amount_to_worker, 4), refund

    @property
    def transactions(self) -> list[CreditTransaction]:
        return list(self._transactions)

    def export_state(self) -> dict[str, object]:
        return {
            "balances": dict(self._balances),
            "holds": {
                job_id: {
                    "job_id": hold.job_id,
                    "user_id": hold.user_id,
                    "amount": hold.amount,
                }
                for job_id, hold in self._holds.items()
            },
            "transactions": [
                {
                    "user_id": transaction.user_id,
                    "delta": transaction.delta,
                    "reason": transaction.reason,
                    "reference_id": transaction.reference_id,
                }
                for transaction in self._transactions
            ],
        }

    def import_state(self, payload: dict[str, object]) -> None:
        self._balances = defaultdict(float, {
            str(user_id): float(balance)
            for user_id, balance in dict(payload.get("balances", {})).items()
            if str(user_id).strip()
        })
        self._holds = {
            str(job_id): CreditHold(
                job_id=str(hold["job_id"]),
                user_id=str(hold["user_id"]),
                amount=float(hold["amount"]),
            )
            for job_id, hold in dict(payload.get("holds", {})).items()
            if str(hold.get("user_id", "")).strip()
        }
        self._transactions = [
            CreditTransaction(
                user_id=str(item["user_id"]),
                delta=float(item["delta"]),
                reason=str(item["reason"]),
                reference_id=str(item["reference_id"]),
            )
            for item in list(payload.get("transactions", []))
            if str(item.get("user_id", "")).strip()
        ]
