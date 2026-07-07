"""
inventory-alert-trigger-skill: Client SDK
Monitors inventory rates and alerts operations teams when velocity risks out-of-stock scenarios.
"""
from __future__ import annotations
from typing import Optional


class InventoryAlertTriggerClient:
    """
    SDK for replenishment alerting logic.
    """

    def check_stock_level(
        self,
        current_stock: int,
        daily_sales_velocity: float,
        lead_time_days: int,
    ) -> dict:
        velocity = max(0.01, daily_sales_velocity)
        days_left = round(current_stock / velocity, 1)

        # Safety stock buffer calculation (adds 3 days buffer)
        safety_stock = int(velocity * 3)
        reorder_point = int(velocity * lead_time_days) + safety_stock
        
        alert = current_stock < reorder_point

        return {
            "days_of_stock_left": days_left,
            "reorder_point": reorder_point,
            "safety_stock_buffer": safety_stock,
            "alert_triggered": alert,
            "severity": "critical" if days_left < lead_time_days else "warning" if alert else "ok"
        }
