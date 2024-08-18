"""make commercial_collaborator_id and collaborator_support_id nullable in client event and contract

Revision ID: 2b3337f181fd
Revises: 14c0e67b6b0c
Create Date: 2024-08-18 17:26:00.094221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2b3337f181fd'
down_revision: Union[str, None] = '14c0e67b6b0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alter the columns to be nullable
    op.alter_column('contracts', 'commercial_collaborator_id',
                    existing_type=sa.Integer(),
                    nullable=True)
    
    op.alter_column('events', 'collaborator_support_id',
                    existing_type=sa.Integer(),
                    nullable=True)


def downgrade() -> None:
    # Revert the columns to be non-nullable
    op.alter_column('contracts', 'commercial_collaborator_id',
                    existing_type=sa.Integer(),
                    nullable=False)
    
    op.alter_column('events', 'collaborator_support_id',
                    existing_type=sa.Integer(),
                    nullable=False)
