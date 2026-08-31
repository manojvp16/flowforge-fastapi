import httpx


class WebhookClient:

    def send(
        self,
        url: str,
        method: str,
        payload: dict,
        headers: dict | None = None,
    ) -> dict:

        method = method.upper()

        if method not in {"GET", "POST", "PUT", "PATCH"}:
            raise ValueError(
                f"Unsupported HTTP method: {method}"
            )

        request_headers = headers or {}

        try:
            with httpx.Client(
                timeout=5.0
            ) as client:

                response = client.request(
                    method=method,
                    url=url,
                    json=payload,
                    headers=request_headers,
                )

            return {
                "success": response.is_success,
                "status_code": response.status_code,
                "response": response.text[:1000],
            }

        except httpx.TimeoutException:

            return {
                "success": False,
                "error": "Webhook request timed out",
            }

        except httpx.RequestError as exc:

            return {
                "success": False,
                "error": (
                    f"Webhook request failed: {exc}"
                ),
            }