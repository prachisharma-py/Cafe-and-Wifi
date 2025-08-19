from alembic import op
import sqlalchemy as sa


revision = '457f588001eb'
down_revision = '5c89f95a5dde'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create a new table with updated schema
    op.create_table(
        'new_cafe',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=250), nullable=False, unique=True),
        sa.Column('map_url', sa.String(length=1000), nullable=False),  # increased length
        sa.Column('img_url', sa.Text(), nullable=False),  # changed to Text
        sa.Column('location', sa.Text(), nullable=False),  # changed to Text
        sa.Column('has_sockets', sa.Boolean(), nullable=False),
        sa.Column('has_toilet', sa.Boolean(), nullable=False),
        sa.Column('has_wifi', sa.Boolean(), nullable=False),
        sa.Column('can_take_calls', sa.Boolean(), nullable=False),
        sa.Column('seats', sa.Integer(), nullable=True),
        sa.Column('coffee_price', sa.String(length=250), nullable=True),
    )

    # Copy data from old table to new table
    op.execute(
        """
        INSERT INTO new_cafe (id, name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price)
        SELECT id, name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price FROM cafe
        """
    )

    # Drop old table
    op.drop_table('cafe')

    # Rename new table to old name
    op.rename_table('new_cafe', 'cafe')


def downgrade() -> None:
    # Reverse: recreate old table schema
    op.create_table(
        'old_cafe',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=250), nullable=False, unique=True),
        sa.Column('map_url', sa.String(length=500), nullable=False),  # old length
        sa.Column('img_url', sa.String(length=500), nullable=False),  # old type VARCHAR(500)
        sa.Column('location', sa.String(length=250), nullable=False),  # old type VARCHAR(250)
        sa.Column('has_sockets', sa.Boolean(), nullable=False),
        sa.Column('has_toilet', sa.Boolean(), nullable=False),
        sa.Column('has_wifi', sa.Boolean(), nullable=False),
        sa.Column('can_take_calls', sa.Boolean(), nullable=False),
        sa.Column('seats', sa.Integer(), nullable=True),
        sa.Column('coffee_price', sa.String(length=250), nullable=True),
    )

    # Copy data back, cast Text to String where needed
    op.execute(
        """
        INSERT INTO old_cafe (id, name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price)
        SELECT id, name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price FROM cafe
        """
    )

    # Drop current table
    op.drop_table('cafe')

    # Rename old table back to cafe
    op.rename_table('old_cafe', 'cafe')
