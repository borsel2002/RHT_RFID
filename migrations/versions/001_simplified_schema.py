"""Initial simplified schema

Revision ID: 001_simplified_schema
Create Date: 2025-03-09 21:19:43.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001_simplified_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create tables
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('username', sa.String(64), nullable=False),
        sa.Column('password_hash', sa.String(128)),
        sa.Column('rfid_uid', sa.String(128)),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('role', sa.String(20), default='member'),
        sa.Column('created_at', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('last_login', sa.DateTime()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('rfid_uid')
    )
    
    op.create_table(
        'memberships',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )
    
    op.create_table(
        'events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(128), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('start_datetime', sa.DateTime(), nullable=False),
        sa.Column('end_datetime', sa.DateTime(), nullable=False),
        sa.Column('capacity', sa.Integer()),
        sa.Column('location', sa.String(256)),
        sa.Column('event_type', sa.String(20)),
        sa.Column('created_at', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'event_registrations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('registration_time', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('status', sa.String(20), default='registered'),
        sa.Column('check_in_time', sa.DateTime()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['event_id'], ['events.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )
    
    op.create_table(
        'volunteer_shifts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('volunteer_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('status', sa.String(20), default='scheduled'),
        sa.Column('priority_score', sa.Float(), default=0.0),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['event_id'], ['events.id']),
        sa.ForeignKeyConstraint(['volunteer_id'], ['users.id'])
    )
    
    op.create_table(
        'volunteer_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('volunteer_id', sa.Integer(), nullable=False),
        sa.Column('total_hours', sa.Float(), default=0.0),
        sa.Column('reliability_score', sa.Float(), default=1.0),
        sa.Column('seniority_score', sa.Float(), default=0.0),
        sa.Column('last_updated', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['volunteer_id'], ['users.id']),
        sa.UniqueConstraint('volunteer_id')
    )
    
    # Create indexes
    op.create_index('idx_user_auth', 'users', ['email', 'is_active'])
    op.create_index('idx_user_role', 'users', ['role', 'is_active'])
    op.create_index('idx_membership_validation', 'memberships', ['user_id', 'start_date', 'end_date', 'is_active'])
    op.create_index('idx_membership_active', 'memberships', ['is_active', 'end_date'])
    op.create_index('idx_event_date_type', 'events', ['start_datetime', 'event_type'])
    op.create_index('idx_event_date_range', 'events', ['start_datetime', 'end_datetime'])
    op.create_index('idx_registration_lookup', 'event_registrations', ['event_id', 'user_id', 'status'])
    op.create_index('idx_registration_status', 'event_registrations', ['status', 'registration_time'])
    op.create_index('idx_shift_scheduling', 'volunteer_shifts', ['volunteer_id', 'start_time', 'status', 'priority_score'])
    op.create_index('idx_shift_time_range', 'volunteer_shifts', ['start_time', 'end_time', 'status'])
    op.create_index('idx_metrics_scores', 'volunteer_metrics', ['reliability_score', 'seniority_score'])

def downgrade():
    # Drop indexes
    op.drop_index('idx_metrics_scores', 'volunteer_metrics')
    op.drop_index('idx_shift_time_range', 'volunteer_shifts')
    op.drop_index('idx_shift_scheduling', 'volunteer_shifts')
    op.drop_index('idx_registration_status', 'event_registrations')
    op.drop_index('idx_registration_lookup', 'event_registrations')
    op.drop_index('idx_event_date_range', 'events')
    op.drop_index('idx_event_date_type', 'events')
    op.drop_index('idx_membership_active', 'memberships')
    op.drop_index('idx_membership_validation', 'memberships')
    op.drop_index('idx_user_role', 'users')
    op.drop_index('idx_user_auth', 'users')
    
    # Drop tables
    op.drop_table('volunteer_metrics')
    op.drop_table('volunteer_shifts')
    op.drop_table('event_registrations')
    op.drop_table('events')
    op.drop_table('memberships')
    op.drop_table('users')
