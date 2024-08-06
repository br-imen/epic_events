from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '90403ac4bc06'
down_revision = None
branch_labels = None
depends_on = None

def column_exists(table_name, column_name):
    """Check if the column exists in the table."""
    conn = op.get_bind()
    query = f"""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name='{table_name}' AND column_name='{column_name}';
    """
    result = conn.execute(query)
    return result.fetchone() is not None

def upgrade():
    # Check if the 'role_id' column already exists
    if not column_exists('collaborators', 'role_id'):
        op.add_column('collaborators', sa.Column('role_id', sa.Integer(), nullable=True))
        op.create_foreign_key(None, 'collaborators', 'roles', ['role_id'], ['id'])

def downgrade():
    if column_exists('collaborators', 'role_id'):
        op.drop_constraint(None, 'collaborators', type_='foreignkey')
        op.drop_column('collaborators', 'role_id')
