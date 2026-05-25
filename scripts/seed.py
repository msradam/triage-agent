"""Seed one triage-agent session for the demo recording."""

from __future__ import annotations

import asyncio

from fastmcp import Client

from theodosia import ServingMode, mount
from triage_agent.app import build_application


async def main() -> None:
    server = mount(build_application(), mode=ServingMode.STEP, name="triage-agent")
    async with Client(server) as client:

        async def step(action, **inputs):
            await client.call_tool("step", {"action": action, "inputs": inputs})

        await step("classify", category="billing", priority="high")
        await step("gather_context", note="customer charged twice on 2026-05-20")
        await step("gather_context", note="duplicate confirmed in ledger")
        await step("resolve", resolution="refunded the duplicate charge")


if __name__ == "__main__":
    asyncio.run(main())
