from typing import Any

from app.integrations.webhook_client import WebhookClient


class WorkflowEngine:

    def __init__(
        self,
        webhook_client: WebhookClient | None = None,
    ):
        self.webhook_client = (
            webhook_client
            if webhook_client is not None
            else WebhookClient()
        )

    def execute(
        self,
        steps: list[dict],
        input_data: dict[str, Any],
    ) -> tuple[str, list[dict]]:

        results = []

        for step in steps:

            step_type = step["type"]

            step_name = (
                step.get("name")
                or step_type
            )

            config = step.get(
                "config",
                {},
            )

            if step_type == "condition":

                result = self._execute_condition(
                    config,
                    input_data,
                )

                results.append(
                    {
                        "step_name": step_name,
                        "step_type": step_type,
                        "status": (
                            "completed"
                            if result
                            else "skipped"
                        ),
                        "result": result,
                    }
                )

                if not result:
                    return "completed", results

            elif step_type == "approval":

                result = self._execute_approval(
                    config,
                )

                results.append(
                    {
                        "step_name": step_name,
                        "step_type": step_type,
                        "status": "completed",
                        "result": result,
                    }
                )

            elif step_type == "notification":

                result = self._execute_notification(
                    config,
                )

                results.append(
                    {
                        "step_name": step_name,
                        "step_type": step_type,
                        "status": "completed",
                        "result": result,
                    }
                )

            elif step_type == "webhook":

                result = self._execute_webhook(
                    config,
                    input_data,
                )

                success = result.get(
                    "success",
                    False,
                )

                results.append(
                    {
                        "step_name": step_name,
                        "step_type": step_type,
                        "status": (
                            "completed"
                            if success
                            else "failed"
                        ),
                        "result": result,
                    }
                )

                if not success:
                    return "failed", results

            else:

                results.append(
                    {
                        "step_name": step_name,
                        "step_type": step_type,
                        "status": "failed",
                        "result": (
                            f"Unsupported step type: "
                            f"{step_type}"
                        ),
                    }
                )

                return "failed", results

        return "completed", results

    def _execute_condition(
        self,
        config: dict,
        input_data: dict,
    ) -> bool:

        field = config.get("field")
        operator = config.get("operator")
        expected = config.get("value")

        actual = input_data.get(field)

        if operator == "==":
            return actual == expected

        if operator == "!=":
            return actual != expected

        if operator == ">":
            return (
                actual is not None
                and actual > expected
            )

        if operator == ">=":
            return (
                actual is not None
                and actual >= expected
            )

        if operator == "<":
            return (
                actual is not None
                and actual < expected
            )

        if operator == "<=":
            return (
                actual is not None
                and actual <= expected
            )

        return False

    def _execute_approval(
        self,
        config: dict,
    ) -> bool:

        return True

    def _execute_notification(
        self,
        config: dict,
    ) -> dict:

        return {
            "sent": True,
            "channel": config.get(
                "channel",
                "unknown",
            ),
        }

    def _execute_webhook(
        self,
        config: dict,
        input_data: dict,
    ) -> dict:

        url = config.get("url")

        method = config.get(
            "method",
            "POST",
        )

        headers = config.get(
            "headers",
            {},
        )

        if not url:
            return {
                "success": False,
                "error": "Webhook URL is required",
            }

        return self.webhook_client.send(
            url=url,
            method=method,
            payload=input_data,
            headers=headers,
        )