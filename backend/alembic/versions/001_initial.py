"""Initial tables

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'urls',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('short_code', sa.String(10), unique=True, nullable=False),
        sa.Column('original_url', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('click_count', sa.Integer(), default=0),
    )
    op.create_index('ix_urls_short_code', 'urls', ['short_code'])

    op.create_table(
        'clicks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('short_code', sa.String(10), nullable=False),
        sa.Column('clicked_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('user_agent', sa.Text()),
        sa.Column('ip_address', sa.String(50)),
    )
    op.create_index('ix_clicks_short_code', 'clicks', ['short_code'])


def downgrade():
    op.drop_index('ix_clicks_short_code')
    op.drop_table('clicks')
    op.drop_index('ix_urls_short_code')
    op.drop_table('urls')
