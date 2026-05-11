"""update users table

Revision ID: 76a6c11c917e
Revises: 258f5a8b91db
Create Date: 2026-05-11 16:24:38.557737

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76a6c11c917e'
down_revision: Union[str, Sequence[str], None] = '258f5a8b91db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    auth_provider_enum = sa.Enum(
        'LOCAL',
        'GOOGLE',
        name='authprovider'
    )

    auth_provider_enum.create(
        op.get_bind(),
        checkfirst=True
    )

    op.add_column(
        'users',
        sa.Column('google_id', sa.String(), nullable=True)
    )

    op.add_column(
        'users',
        sa.Column(
            'auth_provider',
            auth_provider_enum,
            nullable=False,
            server_default='LOCAL'
        )
    )

    op.add_column(
        'users',
        sa.Column('profile_picture', sa.String(), nullable=True)
    )

    op.add_column(
        'users',
        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true')
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        )
    )

    op.alter_column(
        'users',
        'password_hash',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    op.create_unique_constraint(
        'uq_users_google_id',
        'users',
        ['google_id']
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        'uq_users_google_id',
        'users',
        type_='unique'
    )

    op.alter_column(
        'users',
        'password_hash',
        existing_type=sa.VARCHAR(),
        nullable=False
    )

    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'profile_picture')
    op.drop_column('users', 'auth_provider')
    op.drop_column('users', 'google_id')

    auth_provider_enum = sa.Enum(
        'LOCAL',
        'GOOGLE',
        name='authprovider'
    )

    auth_provider_enum.drop(
        op.get_bind(),
        checkfirst=True
    )