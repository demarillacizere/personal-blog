"""new Migration

Revision ID: ef518a2edf60
Revises: d7abd8f73d6c
Create Date: 2020-12-05 17:01:37.505552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef518a2edf60'
down_revision = 'd7abd8f73d6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mail_email'), 'mail', ['email'], unique=True)
    op.create_index(op.f('ix_mail_name'), 'mail', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_mail_name'), table_name='mail')
    op.drop_index(op.f('ix_mail_email'), table_name='mail')
    op.drop_table('mail')
    # ### end Alembic commands ###
