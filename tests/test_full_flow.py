import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.anyio
async def test_full_group_expense_flow():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        register_a = await client.post(
            "/auth/register",
            json={
                "name": "Jagdeep",
                "email": "jagdeep@test.com",
                "password": "test123",
            },
        )
        assert register_a.status_code == 201

        user_a_data = register_a.json()
        access_token_a = user_a_data["tokens"]["access_token"]
        user_a_id = user_a_data["user"]["id"]

        register_b = await client.post(
            "/auth/register",
            json={"name": "Rohit", "email": "rohit@test.com", "password": "test123"},
        )
        assert register_b.status_code == 201

        user_b_data = register_b.json()
        user_b_id = user_b_data["user"]["id"]
        user_b_code = user_b_data["user"]["user_code"]

        headers_a = {"Authorization": f"Bearer {access_token_a}"}

        create_group = await client.post(
            "/groups/",
            json={"name": "Goa Trip"},
            headers=headers_a,
        )
        assert create_group.status_code == 201

        group_id = create_group.json()["id"]

        add_member = await client.post(
            f"/groups/{group_id}/members",
            json={"user_code": user_b_code},
            headers=headers_a,
        )
        assert add_member.status_code == 200

        create_expense = await client.post(
            f"/groups/{group_id}/expenses",
            json={
                "title": "Dinner",
                "amount": 1000,
                "split_type": "equal",
                "equal_member_ids": [user_a_id, user_b_id],
            },
            headers=headers_a,
        )
        assert create_expense.status_code == 201

        expense_data = create_expense.json()
        assert expense_data["title"] == "Dinner"
        assert float(expense_data["amount"]) == 1000

        expenses = await client.get(f"/groups/{group_id}/expenses", headers=headers_a)
        assert expenses.status_code == 200
        assert len(expenses.json()) > 0
