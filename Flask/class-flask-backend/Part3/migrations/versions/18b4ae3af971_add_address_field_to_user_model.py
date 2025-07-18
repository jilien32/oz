"""Add address field to User Model

Revision ID: 18b4ae3af971
Revises: 
Create Date: 2025-07-16 15:28:18.842380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18b4ae3af971'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(length=200), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('address')

    # ### end Alembic commands ###
