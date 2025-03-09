"""Migrate legacy data to new schema

Revision ID: 002_migrate_legacy_data
Create Date: 2025-03-09 21:20:16.000000
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

# revision identifiers
revision = '002_migrate_legacy_data'
down_revision = '001_simplified_schema'
branch_labels = None
depends_on = None

def upgrade():
    connection = op.get_bind()
    
    # Create temporary tables to store old data
    connection.execute("""
        CREATE TEMPORARY TABLE temp_school_info AS 
        SELECT * FROM School_info
    """)
    
    connection.execute("""
        CREATE TEMPORARY TABLE temp_assoc_info AS 
        SELECT * FROM Assoc_info
    """)
    
    connection.execute("""
        CREATE TEMPORARY TABLE temp_personal_info AS 
        SELECT * FROM Personal_info
    """)
    
    # Migrate user data
    connection.execute("""
        INSERT INTO users (
            id, 
            email, 
            username, 
            rfid_uid,
            is_active,
            role,
            created_at
        )
        SELECT 
            s.Std_ID,
            p.eMail,
            CONCAT(p.FirstName, '.', p.LastName),
            s.UID,
            a.Assoc_Actv,
            CASE 
                WHEN a.Assoc_Affil = 1 THEN 'member'
                ELSE 'guest'
            END,
            CURRENT_TIMESTAMP
        FROM temp_school_info s
        JOIN temp_personal_info p ON s.UID = p.UID
        JOIN temp_assoc_info a ON s.UID = a.UID
    """)
    
    # Create default memberships for active association members
    connection.execute("""
        INSERT INTO memberships (
            user_id,
            type,
            start_date,
            end_date,
            is_active
        )
        SELECT 
            s.Std_ID,
            'regular',
            CURRENT_DATE,
            DATE_ADD(CURRENT_DATE, INTERVAL 1 YEAR),
            a.Assoc_Actv
        FROM temp_school_info s
        JOIN temp_assoc_info a ON s.UID = a.UID
        WHERE a.Assoc_Affil = 1
    """)
    
    # Drop temporary tables
    connection.execute("DROP TEMPORARY TABLE IF EXISTS temp_school_info")
    connection.execute("DROP TEMPORARY TABLE IF EXISTS temp_assoc_info")
    connection.execute("DROP TEMPORARY TABLE IF EXISTS temp_personal_info")
    
    # Drop old tables
    op.drop_table('Personal_info')
    op.drop_table('Assoc_info')
    op.drop_table('School_info')

def downgrade():
    # Cannot restore old data after migration
    pass
