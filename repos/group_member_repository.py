from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.group_members import GroupMember

class GroupMemberRepository:
      def __init__(self, session: AsyncSession):
            self.session = session

      async def add(
                  self,
                  user_id: str,
                  group_id: str
      ) -> GroupMember:
            
            member = GroupMember(group_id = group_id, user_id = user_id)

            await self.session.add(member)
            await self.session.commit()
            await self.session.refresh(member)

            return member
      
      async def get(
                  self,
                  user_id: str,
                  group_id: str
      ) -> GroupMember:
            
            return await self.session.execute(select(GroupMember).where(GroupMember.user_id == user_id, GroupMember.group_id == group_id))
      
      async def list(
                  self,
                  group_id: str
      ):
            return await self.session.execute(select(GroupMember).where(GroupMember.group_id == group_id))
      
      async def remove(
                  self,
                  member: GroupMember
      ):    
            await self.session.delete(member)
            await self.session.commit()