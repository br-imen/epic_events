"""cascade events and contract for client delete

Revision ID: 14c0e67b6b0c
Revises: 0ac28d24d8cf
Create Date: 2024-08-18 17:13:32.667622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '14c0e67b6b0c'
down_revision: Union[str, None] = '0ac28d24d8cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # Drop existing foreign key constraints
    op.drop_constraint('events_client_id_fkey', 'events', type_='foreignkey')
    op.drop_constraint('contracts_client_id_fkey', 'contracts', type_='foreignkey')

    # Create new foreign key constraints with cascade on delete
    op.create_foreign_key(
        'events_client_id_fkey',
        'events', 
        'clients', 
        ['client_id'], 
        ['id'],
        ondelete='CASCADE'
    )

    op.create_foreign_key(
        'contracts_client_id_fkey',
        'contracts', 
        'clients', 
        ['client_id'], 
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    # Revert the foreign key constraints to original state
    op.drop_constraint('events_client_id_fkey', 'events', type_='foreignkey')
    op.drop_constraint('contracts_client_id_fkey', 'contracts', type_='foreignkey')

    # Recreate the original foreign key constraints without cascade on delete
    op.create_foreign_key(
        'events_client_id_fkey',
        'events', 
        'clients', 
        ['client_id'], 
        ['id']
    )

    op.create_foreign_key(
        'contracts_client_id_fkey',
        'contracts', 
        'clients', 
        ['client_id'], 
        ['id']
    )
    # ### end Alembic commands ###
