"""make contract-event cascade when delete

Revision ID: 0ac28d24d8cf
Revises: a20ad62bab85
Create Date: 2024-08-17 15:32:13.926997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0ac28d24d8cf'
down_revision: Union[str, None] = 'a20ad62bab85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add cascade delete to contract_id foreign key in events table
    op.drop_constraint('events_contract_id_fkey', 'events', type_='foreignkey')
    op.create_foreign_key(
        'events_contract_id_fkey',
        'events', 
        'contracts', 
        ['contract_id'], 
        ['id'],
        ondelete='CASCADE'
    )

def downgrade() -> None:
    # Remove cascade delete from contract_id foreign key in events table
    op.drop_constraint('events_contract_id_fkey', 'events', type_='foreignkey')
    op.create_foreign_key(
        'events_contract_id_fkey',
        'events', 
        'contracts', 
        ['contract_id'], 
        ['id']
    )

    # ### end Alembic commands ###
