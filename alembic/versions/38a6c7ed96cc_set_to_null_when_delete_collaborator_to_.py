"""set to null when delete collaborator to event, client and contract

Revision ID: 38a6c7ed96cc
Revises: 2b3337f181fd
Create Date: 2024-08-18 17:31:14.532963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '38a6c7ed96cc'
down_revision: Union[str, None] = '2b3337f181fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing foreign key constraints
    op.drop_constraint('contracts_commercial_collaborator_id_fkey', 'contracts', type_='foreignkey')
    op.drop_constraint('events_collaborator_support_id_fkey', 'events', type_='foreignkey')
    op.drop_constraint('clients_commercial_collaborator_id_fkey', 'clients', type_='foreignkey')

    # Recreate the foreign key constraints with ondelete="SET NULL"
    op.create_foreign_key(
        'contracts_commercial_collaborator_id_fkey',
        'contracts', 
        'collaborators', 
        ['commercial_collaborator_id'], 
        ['id'],
        ondelete='SET NULL'
    )

    op.create_foreign_key(
        'events_collaborator_support_id_fkey',
        'events', 
        'collaborators', 
        ['collaborator_support_id'], 
        ['id'],
        ondelete='SET NULL'
    )

    op.create_foreign_key(
        'clients_commercial_collaborator_id_fkey',
        'clients', 
        'collaborators', 
        ['commercial_collaborator_id'], 
        ['id'],
        ondelete='SET NULL'
    )

def downgrade() -> None:
    # Revert the changes made in the upgrade
    op.drop_constraint('contracts_commercial_collaborator_id_fkey', 'contracts', type_='foreignkey')
    op.drop_constraint('events_collaborator_support_id_fkey', 'events', type_='foreignkey')
    op.drop_constraint('clients_commercial_collaborator_id_fkey', 'clients', type_='foreignkey')

    # Recreate the original foreign key constraints without ondelete="SET NULL"
    op.create_foreign_key(
        'contracts_commercial_collaborator_id_fkey',
        'contracts', 
        'collaborators', 
        ['commercial_collaborator_id'], 
        ['id']
    )

    op.create_foreign_key(
        'events_collaborator_support_id_fkey',
        'events', 
        'collaborators', 
        ['collaborator_support_id'], 
        ['id']
    )

    op.create_foreign_key(
        'clients_commercial_collaborator_id_fkey',
        'clients', 
        'collaborators', 
        ['commercial_collaborator_id'], 
        ['id']
    )
