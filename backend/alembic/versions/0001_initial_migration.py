"""Initial migration

Revision ID: 0001_initial_migration
Revises: 
Create flights table

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001_initial_migration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'flights',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('flight_number', sa.String(), nullable=False),
        sa.Column('departure_airport', sa.String(), nullable=False),
        sa.Column('arrival_airport', sa.String(), nullable=False),
        sa.Column('scheduled_departure', sa.DateTime(), nullable=False),
        sa.Column('actual_departure', sa.DateTime(), nullable=True),
        sa.Column('scheduled_arrival', sa.DateTime(), nullable=False),
        sa.Column('actual_arrival', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=True, server_default='scheduled'),
        sa.Column('aircraft_type', sa.String(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('altitude', sa.Float(), nullable=True),
        sa.Column('heading', sa.Float(), nullable=True),
        sa.Column('speed', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.utcnow()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.utcnow()),
    )


def downgrade():
    op.drop_table('flights')
