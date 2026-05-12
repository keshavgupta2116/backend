from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.group_expenses import GroupExpense
from models.expense_splits import ExpenseSplit

class ExoenseRepository:
      def __init__(self, session: AsyncSession):
            self.session = session

      async def create(
                  self,
                  data: dict,
                  split: dict
      ) -> GroupExpense:
            
            expense = GroupExpense(**data)

            await self.session.add(expense)
            await self.session.flush()

            for user_id, amount in split.items():
                  split = ExpenseSplit(expense_id = expense.id, user_id = user_id, amount = amount)
                  await self.session.add(split)

            await self.session.commit()
            await self.session.refresh(expense)

            return expense
      
      async def get_by_id(
                  self,
                  expense_id: str
      ) -> GroupExpense:
            
            return await self.session.execute(select(GroupExpense).where(GroupExpense.id == expense_id))
      
      async def list_by_group(
                  self,
                  group_id: str
      ):
            return await self.session.execute(select(GroupExpense).where(GroupExpense.group_id == group_id))
      
      async def update(
                  self,
                  expense: GroupExpense,
                  data: dict
      ) -> GroupExpense:
            
            for key, val in data.items():
                  setattr(expense, key, val)

            await self.session.commit()
            await self.session.refresh(expense)

            return expense
      
      async def delete(
                  self,
                  expense: GroupExpense
      ):
            await self.session.delete(expense)
            await self.session.commit()