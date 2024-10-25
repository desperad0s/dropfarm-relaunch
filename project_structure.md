// ./docker-compose.yml
services:
  postgres:
    container_name: dropfarm-relaunch-postgres
    image: postgres:14
    environment:
      POSTGRES_USER: dropfarm
      POSTGRES_PASSWORD: dropfarm
      POSTGRES_DB: dropfarm
    ports:
      - "5433:5432"  # Changed port
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    container_name: dropfarm-relaunch-redis
    image: redis:6
    ports:
      - "6380:6379"  # Changed port
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:----------------------------------------------------------------------------------
// ./project_structure.md
----------------------------------------------------------------------------------
// ./file_tracker.py
import os
import hashlib
import json
from typing import Dict, Set
from datetime import datetime

# Define directories to exclude
EXCLUDE_DIRS = {'node_modules', '.git', 'venv', '__pycache__', '.svelte-kit'}
EXCLUDE_FILES = {'package-lock.json', 'yarn.lock', '*.png', '*.jpg', '*.ico'}

def get_file_hash(file_path: str) -> str:
    """Calculate MD5 hash of a file."""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def load_previous_state() -> tuple[Dict[str, str], bool]:
    """Load previous file hashes from state file and determine if this is first run."""
    try:
        with open('.file_hashes.json', 'r') as f:
            data = json.load(f)
            return data.get('hashes', {}), False
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, True

def save_current_state(hashes: Dict[str, str]):
    """Save current file hashes to state file."""
    state = {
        'hashes': hashes,
        'last_updated': datetime.now().isoformat()
    }
    with open('.file_hashes.json', 'w') as f:
        json.dump(state, f, indent=2)

def get_all_files(directory: str) -> Set[str]:
    """Get all valid files in the directory."""
    valid_files = set()
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if any(file.endswith(ext.replace('*', '')) for ext in EXCLUDE_FILES):
                continue
            
            file_path = os.path.join(root, file)
            valid_files.add(file_path)
    
    return valid_files

def write_file_contents(output_file, files_to_write: Set[str]):
    """Write contents of specified files to output file."""
    for file_path in sorted(files_to_write):
        output_file.write(f"// {file_path}\n")
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                output_file.write(f.read())
        except Exception as e:
            output_file.write(f"Error reading {file_path}: {e}\n")
        output_file.write("\n" + "-" * 80 + "\n")

def list_files_and_contents(directory: str):
    """Generate both full content and changes-only files."""
    previous_hashes, is_first_run = load_previous_state()
    current_hashes = {}
    changed_files = set()
    
    # Get all valid files
    all_files = get_all_files(directory)
    
    # Calculate current hashes and identify changes
    for file_path in all_files:
        try:
            current_hash = get_file_hash(file_path)
            current_hashes[file_path] = current_hash
            
            if not is_first_run and (file_path not in previous_hashes or previous_hashes[file_path] != current_hash):
                changed_files.add(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Generate full content file
    with open('project_structure.md', 'w', encoding='utf-8') as full_file:
        full_file.write("# Full Project Structure\n\n")
        write_file_contents(full_file, all_files)
    
    # Generate changes-only file if not first run and there are changes
    if not is_first_run and changed_files:
        with open('project_changes.md', 'w', encoding='utf-8') as changes_file:
            changes_file.write("# Changed Files\n\n")
            write_file_contents(changes_file, changed_files)
    elif is_first_run:
        print("Initial run - establishing baseline state. No changes file generated.")
    else:
        print("No changes detected since last run.")
    
    # Save current state for next comparison
    save_current_state(current_hashes)
    
    # Print summary
    print(f"Full project structure written to: project_structure.md")
    if not is_first_run:
        if changed_files:
            print(f"Changes written to: project_changes.md")
            print(f"Number of changed files: {len(changed_files)}")
        else:
            print("No changes detected - project_changes.md not created")

if __name__ == "__main__":
    list_files_and_contents('.')----------------------------------------------------------------------------------
// ./project_changes.md
----------------------------------------------------------------------------------
// ./.gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
python_lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
venv/

# Node/Frontend
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.env
.output
.vercel
/.svelte-kit
/build

# Keep frontend lib folder
!frontend/src/lib/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Project specific
backend/.env
browser_data/

# Docker
docker/**/data

# OS
.DS_Store
Thumbs.db

# Vite
vite.config.js.timestamp-*
vite.config.ts.timestamp-*----------------------------------------------------------------------------------
// ./.file_hashes.json
{
  "hashes": {
    "./frontend/src/routes/+page.svelte": "3047456d6c9c3dd1151961f671e54b70",
    "./backend/migrations/README": "0d64fccd082782288b1dce1b4743bc9c",
    "./frontend/playwright.config.ts": "02a3faa04f251a61041ebcfe0b0e4058",
    "./backend/app/core/security.py": "4ee03887cbe3d49a7e711041ba8ba119",
    "./frontend/src/routes/dashboard/+layout.svelte": "463bb083fef54ee0f6933fec426cd808",
    "./frontend/src/lib/components/ui/card/card-header.svelte": "66d8c48dfe2ac7e2744c063d4fc64259",
    "./frontend/src/lib/utils.ts": "b0d53f8e204c51ae061cc574b0010147",
    "./frontend/components.json": "8a5efaf92be5898b9360519d78774b3d",
    "./backend/requirements.txt": "d15447ba3df3893b32e70c03b4b5ae10",
    "./backend/app/db/__init__.py": "d41d8cd98f00b204e9800998ecf8427e",
    "./frontend/.prettierrc": "f859616345c032dbebcf2fa8357f7d65",
    "./frontend/src/lib/components/ui/input/index.ts": "98c9ca1c15938faa5b1acf16c372f8bd",
    "./list_project_files.py": "a517e58b20f51cb6c17509b5186b38c9",
    "./frontend/src/routes/schedules/+page.svelte": "cfa33790748ca780456cb39bcbf62efd",
    "./backend/app/services/scheduler/job_manager.py": "01fa03a3c9ab89c26343638b753713eb",
    "./backend/alembic.ini": "b0f5a1dd005a9d6d85c5de80d2c9d6b6",
    "./frontend/src/lib/components/ui/card/card-content.svelte": "1b047b6b93ccaa65fd7ed2250813dae3",
    "./file_tracker.py": "51a3b5e2db67c4f230d606b37daa6976",
    "./frontend/src/routes/auth/login/+page.svelte": "7164256177a5364cb56337051aa92c1a",
    "./frontend/src/app.css": "822bf2a1004a7d0505e0f752ce57a834",
    "./frontend/src/lib/components/ui/button/index.ts": "51c4ce5cacfbdbbfd12d4705f54f4de6",
    "./backend/app/__init__.py": "d41d8cd98f00b204e9800998ecf8427e",
    "./frontend/src/lib/stores/routines.ts": "33a32c8dcd2e2f4c303f7869dcf3fc26",
    "./backend/.env": "db6e18aaaa7e9499e4011ade86f1cc4a",
    "./frontend/src/routes/+layout.svelte": "9a70ec9d831e22446881498550bfc2f5",
    "./frontend/src/lib/components/ui/card/card-title.svelte": "23b42ff5c70996ca68e7d7605533930b",
    "./.file_hashes.json": "463dceb225a7527f64eb1279d8070698",
    "./frontend/postcss.config.js": "cf9efb38a2607f99faa86f977c3c360d",
    "./backend/app/models/__init__.py": "d41d8cd98f00b204e9800998ecf8427e",
    "./backend/app/models/routine.py": "f8ba432181cb42a11e3e16623f4b78d0",
    "./backend/app/main.py": "9c334faf1eab4703b54d361c5b0c78ae",
    "./frontend/src/lib/stores/schedules.ts": "fa79878b65706116a325deaa356b5bb2",
    "./frontend/.prettierignore": "9a0c508eb7e6a3309f493a5463494dfc",
    "./frontend/src/lib/components/ui/card/card.svelte": "d622242f9c0ddd5ee72cf6a3329f7ece",
    "./backend/app/api/v1/schedules.py": "439c38ceb4b01d55f9324486c6431549",
    "./frontend/src/lib/components/Nav.svelte": "bcdda3c4c65cae751dab2640c77ae502",
    "./frontend/src/app.d.ts": "e7ca655ae323f4832078d94dc684990e",
    "./frontend/src/lib/index.ts": "ffcb0e97b69eb555d5739e9efe961ca0",
    "./backend/migrations/script.py.mako": "dbe2609632797d37d908ab6a957e5604",
    "./backend/migrations/versions/2dfe4ece6829_add_user_model.py": "ff18641a5cdf8b8b0a87d3634cf042e7",
    "./backend/app/db/session.py": "29a42a97ed5fdca41c9c47997ed1fb40",
    "./frontend/eslint.config.js": "95aea1b45486201193150b6a5322fd9b",
    "./backend/app/services/automation/__init__.py": "d41d8cd98f00b204e9800998ecf8427e",
    "./backend/app/models/user.py": "5e82cefb54fe158c35d268e2c18f17cf",
    "./frontend/src/lib/api.ts": "33ce674af71864c3fffb80d8a4b04046",
    "./frontend/src/lib/components/ui/label/index.ts": "18ee6b31bbe0c3a41b4b0d3be130ef30",
    "./frontend/src/lib/components/ui/label/label.svelte": "655e9466dc1921394099464487527c75",
    "./frontend/src/lib/components/ui/input/input.svelte": "5b8a8e55f3afd15983a91d3a41e1024c",
    "./frontend/src/lib/components/StatsWidget.svelte": "19c9d72145d462660061066ce031355e",
    "./frontend/src/lib/components/ui/card/index.ts": "585b4d8de9e933fa3c27175515531d30",
    "./backend/migrations/versions/de90cdbf7d8a_initial_migration.py": "8b0970a9a57c35a6f8a3ba676e265907",
    "./frontend/src/app.html": "1a40fcf49d7f0813d821764b0c5ff482",
    "./frontend/README.md": "ffdb618fb937b11736449e3ec63dc354",
    "./project_changes.md": "513c5c78779070b5ed0fad18b4445b80",
    "./backend/app/core/config.py": "5e6e2ea436dfba910b8b7058c43ca6e8",
    "./frontend/src/routes/dashboard/+page.svelte": "ae2c4977e12a4e9aef9b641e11773293",
    "./frontend/src/routes/routines/+page.svelte": "3af36d9b71a9067bbaef4425d28d8ec8",
    "./frontend/.npmrc": "e780ac33d3d13827a73886735c3a368b",
    "./backend/app/schemas/__init__.py": "d41d8cd98f00b204e9800998ecf8427e",
    "./backend/app/api/v1/auth.py": "9ef4dc3f8aae1c6dd3dfb6c61c499ef9",
    "./frontend/src/routes/auth/register/+page.svelte": "336b51022e9597833652fec8f2cdd867",
    "./frontend/svelte.config.js": "9f7646f4d93442c9196b6d56048b6b4f",
    "./docker-compose.yml": "4f6b8784448ad514266c7b044961bf92",
    "./frontend/tsconfig.json": "7dea0cc2fb98e87d0df3173e0658e68f",
    "./frontend/src/routes/schedules/[id]/+page.svelte": "e0b9730879a4c4a0252e400de9cdfd52",
    "./backend/app/core/auth.py": "60d602ce9d82019c49f44a3599364f9f",
    "./backend/app/api/v1/routines.py": "900c98e89c68ce3c030409cdb6c4a5c0",
    "./backend/app/models/schedule.py": "51e22c9566972aeb95a3a527e3e3a2c7",
    "./frontend/src/demo.spec.ts": "e8d47f6fa44c60b24db052eac57f714c",
    "./frontend/src/lib/components/ui/button/button.svelte": "d2114dfda0ed72afe2bab8ba98c4a3a3",
    "./backend/migrations/env.py": "40f309bcfedba4a697e84f42674b4aa8",
    "./project_structure.md": "8f459800ca46d07fa88c7366b6644312",
    "./frontend/src/lib/components/ui/card/card-footer.svelte": "d2ddd90c9bf60dcf32acb7c4f36b378c",
    "./frontend/vite.config.ts": "7a9908641523f1624bc2696d5d85dd8a",
    "./frontend/src/routes/routines/[id]/+page.svelte": "1b309dd9bc3919a0fd5ff9bc66c07eeb",
    "./frontend/src/lib/stores/auth.ts": "7b6c2c08964dcabb5cc5bf96130d1b32",
    "./.gitignore": "8fc9dfa844cc1a5271a57e95f12558dd",
    "./backend/app/db/base_class.py": "25437479c51ea4fa8cff594460024939",
    "./backend/app/schemas/schedule.py": "1ff8f3a8e0f0ce22bbdb062e1d7b7f07",
    "./backend/app/schemas/user.py": "5d8ba7fbf4c3fc73ef7a300b1e5adfd9",
    "./frontend/src/lib/components/NotificationToast.svelte": "7389515693a0ba5e60ffeca22e75a3e0",
    "./frontend/package.json": "2f19db9850c8958bcf85ba0235479364",
    "./frontend/src/lib/components/ui/card/card-description.svelte": "048749a472886e146210247db376f61b",
    "./frontend/tailwind.config.ts": "18d37402bcdc0703c5fe500ad8edd051",
    "./frontend/e2e/demo.test.ts": "eef62f9ac8ad9798de68604be11ae9a3",
    "./backend/app/services/automation/player.py": "d42b0c5d027a5e207cccac74bbfb69e2",
    "./backend/app/db/base.py": "75e23d274e761a96afcd7ad3e63a2d47"
  },
  "last_updated": "2024-10-26T00:08:11.272335"
}----------------------------------------------------------------------------------
// ./list_project_files.py
import os

# Define directories to exclude
EXCLUDE_DIRS = {'node_modules', '.git', 'venv', '__pycache__', '.svelte-kit'}

def list_files_and_contents(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for root, dirs, files in os.walk(directory):
            # Exclude specified directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                file_path = os.path.join(root, file)
                out_file.write(f"// {file_path}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        out_file.write(f.read())
                except Exception as e:
                    out_file.write(f"Error reading {file_path}: {e}\n")
                out_file.write("----------------------------------------------------------------------------------\n")

# Specify the output file
output_file = 'project_structure.md'

# Start from the current directory
list_files_and_contents('.', output_file)

print(f"Project structure and contents have been logged to {output_file}")----------------------------------------------------------------------------------
// ./backend/alembic.ini
[alembic]
script_location = migrations
sqlalchemy.url = postgresql://dropfarm_user:testing123@localhost:5433/dropfarm

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
----------------------------------------------------------------------------------
// ./backend/requirements.txt
alembic==1.13.1
annotated-types==0.7.0
anyio==4.6.2.post1
asyncpg==0.29.0
bcrypt==4.2.0
certifi==2024.8.30
cffi==1.17.1
click==8.1.7
cryptography==43.0.3
dnspython==2.7.0
ecdsa==0.19.0
email-validator==2.1.0
fastapi==0.109.0
greenlet==3.0.3
h11==0.14.0
httpcore==1.0.6
httpx==0.26.0
idna==3.10
iniconfig==2.0.0
Mako==1.3.6
MarkupSafe==3.0.2
packaging==24.1
passlib==1.7.4
playwright==1.41.1
pluggy==1.5.0
psycopg2-binary==2.9.9
pyasn1==0.6.1
pycparser==2.22
pydantic==2.5.3
pydantic-settings==2.1.0
pydantic_core==2.14.6
pyee==11.0.1
pytest==7.4.4
pytest-asyncio==0.23.3
python-dotenv==1.0.0
python-jose==3.3.0
python-multipart==0.0.6
redis==5.0.1
rsa==4.9
six==1.16.0
sniffio==1.3.1
SQLAlchemy==2.0.25
starlette==0.35.1
types-passlib==1.7.7
types-python-jose==3.3.0
typing_extensions==4.12.2
uvicorn==0.27.0
----------------------------------------------------------------------------------
// ./backend/.env
DATABASE_URL=postgresql+asyncpg://dropfarm:dropfarm@localhost:5433/dropfarm
REDIS_URL=redis://localhost:6380
SECRET_KEY=fe65b6a100765032dbc59c224bf478048e3a3ca241afa2dddaa2d510976a2432----------------------------------------------------------------------------------
// ./backend/migrations/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parents[1]))

# Import your models
from app.db.base_class import Base
from app.models.user import User  # noqa
from app.models.routine import Routine  # noqa
from app.models.schedule import Schedule  # noqa

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()----------------------------------------------------------------------------------
// ./backend/migrations/script.py.mako
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
----------------------------------------------------------------------------------
// ./backend/migrations/README
Generic single-database configuration.----------------------------------------------------------------------------------
// ./backend/migrations/versions/2dfe4ece6829_add_user_model.py
"""add user model

Revision ID: 2dfe4ece6829
Revises: de90cdbf7d8a
Create Date: 2024-10-25 18:43:38.426389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dfe4ece6829'
down_revision: Union[str, None] = 'de90cdbf7d8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
----------------------------------------------------------------------------------
// ./backend/migrations/versions/de90cdbf7d8a_initial_migration.py
"""Initial migration

Revision ID: de90cdbf7d8a
Revises: 
Create Date: 2024-10-25 00:14:40.618461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de90cdbf7d8a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('routines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('steps', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_routines_id'), 'routines', ['id'], unique=False)
    op.create_table('schedules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('routine_id', sa.Integer(), nullable=True),
    sa.Column('interval_seconds', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_run', sa.DateTime(), nullable=True),
    sa.Column('next_run', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['routine_id'], ['routines.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schedules_id'), 'schedules', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_schedules_id'), table_name='schedules')
    op.drop_table('schedules')
    op.drop_index(op.f('ix_routines_id'), table_name='routines')
    op.drop_table('routines')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
----------------------------------------------------------------------------------
// ./backend/app/main.py
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, routines, schedules

app = FastAPI(title="Dropfarm API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(routines.router, prefix="/api/v1")
app.include_router(schedules.router, prefix="/api/v1")
# TO-DO: Implement main application logic
----------------------------------------------------------------------------------
// ./backend/app/__init__.py
----------------------------------------------------------------------------------
// ./backend/app/schemas/__init__.py
----------------------------------------------------------------------------------
// ./backend/app/schemas/schedule.py
# app/schemas/schedule.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScheduleBase(BaseModel):
    routine_id: int
    interval_seconds: int
    is_active: bool = True

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    interval_seconds: Optional[int] = None
    is_active: Optional[bool] = None

class ScheduleResponse(ScheduleBase):
    id: int
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ScheduleInDB(ScheduleResponse):
    pass----------------------------------------------------------------------------------
// ./backend/app/schemas/user.py
# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

# We had an incorrect reference to UserInDBBase, let's fix that
class User(UserResponse):
    pass

class UserInDB(UserResponse):
    hashed_password: str----------------------------------------------------------------------------------
// ./backend/app/api/v1/schedules.py
# backend/app/api/v1/schedules.py
"""
Schedule management endpoints
filepath: backend/app/api/v1/schedules.py
"""
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.schemas.schedule import ScheduleCreate, ScheduleResponse

router = APIRouter()

@router.post("/schedules")
async def create_schedule(schedule: ScheduleCreate):
    """Create a new schedule."""
    # TODO: Implement schedule creation
    pass

@router.get("/schedules")
async def list_schedules():
    """List user's schedules."""
    # TODO: Implement schedules listing
    pass

# TO-DO: Implement schedules endpoints----------------------------------------------------------------------------------
// ./backend/app/api/v1/routines.py
# app/api/v1/routines.py
from fastapi import APIRouter, Depends
from app.services.automation.player import AutomationService  # Changed this line
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/routines/start-recording")
async def start_recording(user = Depends(get_current_user)):
    # Create user-specific automation service
    user_data_dir = f"browser_data/{user.id}"
    automation = AutomationService(user_data_dir)
    await automation.start_browser()
    await automation.start_recording()
    return {"status": "recording_started"}

@router.post("/routines/stop-recording")
async def stop_recording(user = Depends(get_current_user)):
    # Get user's automation service
    automation = AutomationService(f"browser_data/{user.id}")
    recorded_steps = await automation.stop_recording()
    await automation.close()
    return {"recorded_steps": recorded_steps}

@router.post("/routines/{routine_id}/play")
async def play_routine(routine_id: int, user = Depends(get_current_user)):
    # Get routine from database
    routine = await get_routine(routine_id)  # TO-DO: Implement this
    # Play back the routine
    automation = AutomationService(f"browser_data/{user.id}")
    await automation.start_browser()
    await automation.playback_routine(routine.steps)
    await automation.close()
    return {"status": "playback_completed"}----------------------------------------------------------------------------------
// ./backend/app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from app.core import security
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/auth/register")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Check if user already exists
        result = await db.execute(select(User).where(User.email == user_data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = security.get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        print(f"User registered successfully: {user_data.email}")  # Add logging
        return db_user
    except Exception as e:
        print(f"Error during registration: {str(e)}")  # Add logging
        raise

@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Find user
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active
        }
    }----------------------------------------------------------------------------------
// ./backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dropfarm"
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BROWSER_DATA_DIR: str = "browser_data"

    class Config:
        env_file = ".env"

settings = Settings()----------------------------------------------------------------------------------
// ./backend/app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "your-secret-key-here"  # Replace with your secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt----------------------------------------------------------------------------------
// ./backend/app/core/auth.py
# app/core/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
        
    return user----------------------------------------------------------------------------------
// ./backend/app/models/__init__.py
----------------------------------------------------------------------------------
// ./backend/app/models/schedule.py
# app/models/schedule.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from app.db.base_class import Base
from datetime import datetime

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey("routines.id"))
    interval_seconds = Column(Integer)  # Simple interval in seconds
    is_active = Column(Boolean, default=True)
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# TO-DO: Implement database models and functions for schedules
----------------------------------------------------------------------------------
// ./backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)----------------------------------------------------------------------------------
// ./backend/app/models/routine.py
# app/models/routine.py
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from app.db.base_class import Base
from datetime import datetime

class Routine(Base):
    __tablename__ = "routines"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    description = Column(String, nullable=True)
    steps = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# TO-DO: Implement database models and functions for routines
----------------------------------------------------------------------------------
// ./backend/app/db/base.py
# backend/app/db/base.py
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.routine import Routine  # noqa
from app.models.schedule import Schedule  # noqa----------------------------------------------------------------------------------
// ./backend/app/db/base_class.py
# backend/app/db/base_class.py
from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()----------------------------------------------------------------------------------
// ./backend/app/db/__init__.py
----------------------------------------------------------------------------------
// ./backend/app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# TO-DO: Implement database models and functions for routines, users, schedules, etc.----------------------------------------------------------------------------------
// ./backend/app/services/scheduler/job_manager.py
# backend/app/services/scheduler/job_manager.py
"""
Schedule manager for automation routines
filepath: backend/app/services/scheduler/job_manager.py
"""
from redis import Redis
from typing import List
from ...models.schedule import Schedule

class JobManager:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def schedule_routine(self, schedule: Schedule) -> bool:
        """Create a new scheduled job."""
        # TODO: Implement job scheduling
        pass

    async def cancel_schedule(self, schedule_id: int) -> bool:
        """Cancel an existing scheduled job."""
        # TODO: Implement job cancellation
        pass

    async def list_active_jobs(self, user_id: int) -> List[Dict]:
        """List all active jobs for a user."""
        # TODO: Implement active jobs listing
        pass

# TO-DO: Implement job manager
----------------------------------------------------------------------------------
// ./backend/app/services/automation/player.py
# app/services/automation/player.py
from playwright.async_api import async_playwright, Browser, Page
from typing import List, Dict, Any, Optional
import json
import os
import asyncio
from datetime import datetime

class AutomationService:
    def __init__(self, user_data_dir: str):
        self.user_data_dir = user_data_dir
        self.recording: List[Dict[str, Any]] = []
        self.is_recording = False
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None

    async def start_browser(self) -> None:
        """Start browser with persistent context for Telegram session."""
        playwright = await async_playwright().start()
        self._browser = await playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=False,  # Set to True for production headless mode
            viewport={'width': 1280, 'height': 720}
        )
        self._page = await self._browser.new_page()

    async def start_recording(self) -> None:
        """Start recording user interactions."""
        if not self._page:
            raise RuntimeError("Browser not started")
        
        self.recording = []
        self.is_recording = True
        
        # Setup event listeners
        async def handle_click(event):
            if not self.is_recording:
                return
            
            element = await self._page.evaluate("""
                (element) => {
                    return {
                        selector: element.id || element.className,
                        innerText: element.innerText,
                        tag: element.tagName.toLowerCase()
                    }
                }
            """, event)
            
            self.recording.append({
                'type': 'click',
                'timestamp': datetime.now().isoformat(),
                'x': event['x'],
                'y': event['y'],
                'element': element,
                'url': self._page.url
            })

        async def handle_navigation(response):
            if not self.is_recording:
                return
            
            self.recording.append({
                'type': 'navigation',
                'timestamp': datetime.now().isoformat(),
                'url': response.url,
                'status': response.status
            })

        # Register event listeners
        await self._page.evaluate("""
            window.addEventListener('click', event => {
                window.__recordClick(event);
            });
        """)
        
        self._page.on('click', handle_click)
        self._page.on('response', handle_navigation)

    async def stop_recording(self) -> List[Dict[str, Any]]:
        """Stop recording and return the recorded steps."""
        self.is_recording = False
        return self.recording

    async def verify_routine(self, routine: List[Dict[str, Any]]) -> bool:
        """Verify a recorded routine can be played back."""
        try:
            await self.playback_routine(routine, verify_mode=True)
            return True
        except Exception as e:
            print(f"Verification failed: {str(e)}")
            return False

    async def playback_routine(self, routine: List[Dict[str, Any]], verify_mode: bool = False) -> None:
        """Play back a recorded routine."""
        if not self._page:
            raise RuntimeError("Browser not started")

        for step in routine:
            try:
                if step['type'] == 'click':
                    # Wait for navigation or network idle if this is a critical click
                    await self._page.wait_for_load_state('networkidle')
                    
                    # Try to find element by multiple strategies
                    element = None
                    if 'element' in step:
                        try:
                            # Try by ID
                            if step['element'].get('selector'):
                                element = await self._page.wait_for_selector(
                                    f"#{step['element']['selector']}", 
                                    timeout=5000
                                )
                            # Try by text content
                            if not element and step['element'].get('innerText'):
                                element = await self._page.wait_for_selector(
                                    f"text={step['element']['innerText']}", 
                                    timeout=5000
                                )
                        except:
                            pass

                    # Fallback to coordinates if element not found
                    if element:
                        await element.click()
                    else:
                        await self._page.mouse.click(step['x'], step['y'])
                    
                    # Add wait time after click (configurable)
                    await asyncio.sleep(1)

                elif step['type'] == 'navigation':
                    await self._page.wait_for_load_state('networkidle')
                    
                    # If URL doesn't match, try to navigate
                    if self._page.url != step['url']:
                        await self._page.goto(step['url'])

                # Handle special cases like waiting for video
                if 'wait_time' in step:
                    await asyncio.sleep(step['wait_time'])

            except Exception as e:
                if verify_mode:
                    raise
                print(f"Error during playback: {str(e)}")

    async def close(self) -> None:
        """Close the browser and cleanup."""
        if self._browser:
            await self._browser.close()
            self._browser = None
            self._page = None----------------------------------------------------------------------------------
// ./backend/app/services/automation/__init__.py
----------------------------------------------------------------------------------
// ./frontend/package.json
{
	"name": "frontend",
	"version": "0.0.1",
	"type": "module",
	"scripts": {
		"dev": "vite dev",
		"build": "vite build",
		"preview": "vite preview",
		"check": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json",
		"check:watch": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json --watch",
		"test:e2e": "playwright test",
		"test": "npm run test:e2e && npm run test:unit -- --run",
		"test:unit": "vitest",
		"lint": "eslint . && prettier --check .",
		"format": "prettier --write ."
	},
	"devDependencies": {
		"@playwright/test": "^1.45.3",
		"@sveltejs/adapter-auto": "^3.3.0",
		"@sveltejs/kit": "^2.0.0",
		"@sveltejs/vite-plugin-svelte": "^4.0.0",
		"@tailwindcss/aspect-ratio": "^0.4.2",
		"@tailwindcss/container-queries": "^0.1.1",
		"@tailwindcss/forms": "^0.5.9",
		"@tailwindcss/typography": "^0.5.15",
		"@types/eslint": "^9.6.0",
		"autoprefixer": "^10.4.20",
		"bits-ui": "^0.21.16",
		"clsx": "^2.1.1",
		"eslint": "^9.7.0",
		"eslint-config-prettier": "^9.1.0",
		"eslint-plugin-svelte": "^2.36.0",
		"globals": "^15.0.0",
		"lucide-svelte": "^0.453.0",
		"postcss": "^8.4.47",
		"prettier": "^3.3.2",
		"prettier-plugin-svelte": "^3.2.6",
		"shadcn-svelte": "^0.14.0",
		"svelte": "^5.0.0",
		"svelte-check": "^4.0.0",
		"tailwind-merge": "^2.5.4",
		"tailwind-variants": "^0.2.1",
		"tailwindcss": "^3.4.14",
		"typescript": "^5.0.0",
		"typescript-eslint": "^8.0.0",
		"vite": "^5.0.3",
		"vitest": "^2.1.3"
	}
}
----------------------------------------------------------------------------------
// ./frontend/svelte.config.js
import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations#preprocessors
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		// adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
		// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
		// See https://svelte.dev/docs/kit/adapters for more information about adapters.
		adapter: adapter()
	}
};

export default config;
----------------------------------------------------------------------------------
// ./frontend/tailwind.config.ts
import { fontFamily } from "tailwindcss/defaultTheme";
import type { Config } from "tailwindcss";

const config: Config = {
	darkMode: ["class"],
	content: ["./src/**/*.{html,js,svelte,ts}"],
	safelist: ["dark"],
	theme: {
		container: {
			center: true,
			padding: "2rem",
			screens: {
				"2xl": "1400px"
			}
		},
		extend: {
			colors: {
				border: "hsl(var(--border) / <alpha-value>)",
				input: "hsl(var(--input) / <alpha-value>)",
				ring: "hsl(var(--ring) / <alpha-value>)",
				background: "hsl(var(--background) / <alpha-value>)",
				foreground: "hsl(var(--foreground) / <alpha-value>)",
				primary: {
					DEFAULT: "hsl(var(--primary) / <alpha-value>)",
					foreground: "hsl(var(--primary-foreground) / <alpha-value>)"
				},
				secondary: {
					DEFAULT: "hsl(var(--secondary) / <alpha-value>)",
					foreground: "hsl(var(--secondary-foreground) / <alpha-value>)"
				},
				destructive: {
					DEFAULT: "hsl(var(--destructive) / <alpha-value>)",
					foreground: "hsl(var(--destructive-foreground) / <alpha-value>)"
				},
				muted: {
					DEFAULT: "hsl(var(--muted) / <alpha-value>)",
					foreground: "hsl(var(--muted-foreground) / <alpha-value>)"
				},
				accent: {
					DEFAULT: "hsl(var(--accent) / <alpha-value>)",
					foreground: "hsl(var(--accent-foreground) / <alpha-value>)"
				},
				popover: {
					DEFAULT: "hsl(var(--popover) / <alpha-value>)",
					foreground: "hsl(var(--popover-foreground) / <alpha-value>)"
				},
				card: {
					DEFAULT: "hsl(var(--card) / <alpha-value>)",
					foreground: "hsl(var(--card-foreground) / <alpha-value>)"
				}
			},
			borderRadius: {
				lg: "var(--radius)",
				md: "calc(var(--radius) - 2px)",
				sm: "calc(var(--radius) - 4px)"
			},
			fontFamily: {
				sans: [...fontFamily.sans]
			}
		}
	},
};

export default config;
----------------------------------------------------------------------------------
// ./frontend/vite.config.ts
import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
	plugins: [sveltekit()],

	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	}
});
----------------------------------------------------------------------------------
// ./frontend/README.md
# create-svelte

Everything you need to build a Svelte project, powered by [`create-svelte`](https://github.com/sveltejs/kit/tree/main/packages/create-svelte).

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```bash
# create a new project in the current directory
npx sv create

# create a new project in my-app
npx sv create my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.
----------------------------------------------------------------------------------
// ./frontend/.prettierignore
# Package Managers
package-lock.json
pnpm-lock.yaml
yarn.lock
----------------------------------------------------------------------------------
// ./frontend/playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
	webServer: {
		command: 'npm run build && npm run preview',
		port: 4173
	},

	testDir: 'e2e'
});
----------------------------------------------------------------------------------
// ./frontend/eslint.config.js
import prettier from 'eslint-config-prettier';
import js from '@eslint/js';
import svelte from 'eslint-plugin-svelte';
import globals from 'globals';
import ts from 'typescript-eslint';

export default ts.config(
	js.configs.recommended,
	...ts.configs.recommended,
	...svelte.configs['flat/recommended'],
	prettier,
	...svelte.configs['flat/prettier'],
	{
		languageOptions: {
			globals: {
				...globals.browser,
				...globals.node
			}
		}
	},
	{
		files: ['**/*.svelte'],

		languageOptions: {
			parserOptions: {
				parser: ts.parser
			}
		}
	},
	{
		ignores: ['build/', '.svelte-kit/', 'dist/']
	}
);
----------------------------------------------------------------------------------
// ./frontend/postcss.config.js
export default {
	plugins: {
	  tailwindcss: {},
	  autoprefixer: {},
	},
  }----------------------------------------------------------------------------------
// ./frontend/components.json
{
	"$schema": "https://shadcn-svelte.com/schema.json",
	"style": "default",
	"tailwind": {
		"config": "tailwind.config.ts",
		"css": "src/app.css",
		"baseColor": "zinc"
	},
	"aliases": {
		"components": "$lib/components",
		"utils": "$lib/utils"
	},
	"typescript": true
}----------------------------------------------------------------------------------
// ./frontend/.prettierrc
{
	"useTabs": true,
	"singleQuote": true,
	"trailingComma": "none",
	"printWidth": 100,
	"plugins": ["prettier-plugin-svelte"],
	"overrides": [
		{
			"files": "*.svelte",
			"options": {
				"parser": "svelte"
			}
		}
	]
}
----------------------------------------------------------------------------------
// ./frontend/.npmrc
engine-strict=true
----------------------------------------------------------------------------------
// ./frontend/tsconfig.json
{
	"extends": "./.svelte-kit/tsconfig.json",
	"compilerOptions": {
		"allowJs": true,
		"checkJs": true,
		"esModuleInterop": true,
		"forceConsistentCasingInFileNames": true,
		"resolveJsonModule": true,
		"skipLibCheck": true,
		"sourceMap": true,
		"strict": true,
		"moduleResolution": "bundler"
	}
	// Path aliases are handled by https://svelte.dev/docs/kit/configuration#alias
	// except $lib which is handled by https://svelte.dev/docs/kit/configuration#files
	//
	// If you want to overwrite includes/excludes, make sure to copy over the relevant includes/excludes
	// from the referenced tsconfig.json - TypeScript does not merge them in
}
----------------------------------------------------------------------------------
// ./frontend/static/favicon.png
PNG

   
IHDR         i7@   sRGB   IDATx]m8U	.%\BJp	.!%b !A8ܛuƤ&gCr<;H`l6.fk6.]lg(.ۙSDNA"|؅و.?8N.V	`qf\l
f\
ҕy3P$~E3В9rf0zj
ߤ
ݤ
~M`*Y+5
0sK<%pq
Z0";Gq^0<
ɗrtŀ
漼q^a|6"$zLCl ,UwIxpqE GIx%F̅VV2:;b^3\G@Nk6:KO}6	GK0-`@%th,M0qeMHx]WٗQ|!-$6!ht:nԏ?OxGC 
kO#j"00+;L
)/f0HA_NT\VWf+H;;b8	%  vɇa y
ƈ^7-f%P愲gA^tIP*vY	/)/AS*{%<]P =lktO 
(!"
=6,T@B;{`TBPު*PD(*rv1S%`*d@FQ
 |6h8Z"/H} mP_Üa9+ålҵ~E~wMK?s3Wӕg#
<jY-{-
O1ˤxC;9X;v /hjẃXtV#̗ ~FOPb, wsbxT@eTh/D#E}8Oew>s(rkq=׸֍y2uD(Б{["@R ŗr݌P(%Kj6|Q4C5=+''GLm'r8t
ء$5!	`?\UPOgȽl]qKgYXCh30> ;rG<Ul5h0L$:V |ZB<킊b~KLG
.8=?`6{Aт 1M*K䲼yxӤн#KyM>]͟<^ݜE.NcT!E'+cr@&^
I|'ϧsn:/_=v dw̞A}:	FY\gv&5˛.x}>]jwqo6v֗    IENDB`----------------------------------------------------------------------------------
// ./frontend/e2e/demo.test.ts
import { expect, test } from '@playwright/test';

test('home page has expected h1', async ({ page }) => {
	await page.goto('/');
	await expect(page.locator('h1')).toBeVisible();
});
----------------------------------------------------------------------------------
// ./frontend/src/app.d.ts
// See https://svelte.dev/docs/kit/types#app
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
----------------------------------------------------------------------------------
// ./frontend/src/app.css
@tailwind base;
@tailwind components;
@tailwind utilities;
 
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
 
    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;
 
    --popover: 0 0% 100%;
    --popover-foreground: 240 10% 3.9%;
 
    --card: 0 0% 100%;
    --card-foreground: 240 10% 3.9%;
 
    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
 
    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;
 
    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;
 
    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;
 
    --destructive: 0 72.2% 50.6%;
    --destructive-foreground: 0 0% 98%;
 
    --ring: 240 10% 3.9%;
 
    --radius: 0.5rem;
  }
 
  .dark {
    --background: 240 10% 3.9%;
    --foreground: 0 0% 98%;
 
    --muted: 240 3.7% 15.9%;
    --muted-foreground: 240 5% 64.9%;
 
    --popover: 240 10% 3.9%;
    --popover-foreground: 0 0% 98%;
 
    --card: 240 10% 3.9%;
    --card-foreground: 0 0% 98%;
 
    --border: 240 3.7% 15.9%;
    --input: 240 3.7% 15.9%;
 
    --primary: 0 0% 98%;
    --primary-foreground: 240 5.9% 10%;
 
    --secondary: 240 3.7% 15.9%;
    --secondary-foreground: 0 0% 98%;
 
    --accent: 240 3.7% 15.9%;
    --accent-foreground: 0 0% 98%;
 
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
 
    --ring: 240 4.9% 83.9%;
  }
}
 
@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}----------------------------------------------------------------------------------
// ./frontend/src/demo.spec.ts
import { describe, it, expect } from 'vitest';

describe('sum test', () => {
	it('adds 1 + 2 to equal 3', () => {
		expect(1 + 2).toBe(3);
	});
});
----------------------------------------------------------------------------------
// ./frontend/src/app.html
<!doctype html>
<html lang="en">
	<head>
		<meta charset="utf-8" />
		<link rel="icon" href="%sveltekit.assets%/favicon.png" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		%sveltekit.head%
	</head>
	<body data-sveltekit-preload-data="hover">
		<div style="display: contents">%sveltekit.body%</div>
	</body>
</html>
----------------------------------------------------------------------------------
// ./frontend/src/routes/+layout.svelte
<script lang="ts">
    import { onMount } from 'svelte';
    import Nav from '$lib/components/Nav.svelte';
    import { isAuthenticated } from '$lib/stores/auth';
    
    onMount(async () => {
        // TODO: Check authentication status
    });
</script>

<Nav />
<main>
    <slot />
</main>----------------------------------------------------------------------------------
// ./frontend/src/routes/+page.svelte
<script lang="ts">
    import { isAuthenticated } from '$lib/stores/auth';
</script>

<div class="landing">
    <!-- TODO: Implement landing page content -->
</div>----------------------------------------------------------------------------------
// ./frontend/src/routes/dashboard/+layout.svelte
<script lang="ts">
    import { onMount } from 'svelte';
    import { isAuthenticated } from '$lib/stores/auth';
    import { goto } from '$app/navigation';

    onMount(async () => {
        // TODO: Check authentication status
        // TODO: Redirect to login if not authenticated
    });
</script>

<div class="min-h-screen bg-background">
    <div class="container mx-auto px-4 py-8">
        <slot />
    </div>
</div>----------------------------------------------------------------------------------
// ./frontend/src/routes/dashboard/+page.svelte
<script lang="ts">
    import { onMount } from 'svelte';
    import { routines, currentRoutine } from '$lib/stores/routines';
    import { schedules } from '$lib/stores/schedules';
    import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
    import { Button } from '$lib/components/ui/button';
    import StatsWidget from '$lib/components/StatsWidget.svelte';

    let stats = {
        activeRoutines: 0,
        scheduledTasks: 0,
        successRate: 0,
    };

    onMount(async () => {
        // TODO: Load dashboard data
        // TODO: Initialize stats
    });
</script>

<div class="space-y-6">
    <h1 class="text-3xl font-bold">Dashboard</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsWidget {stats} />
        
        <Card>
            <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
                <div class="space-y-2">
                    <Button class="w-full" href="/routines/new">Create New Routine</Button>
                    <Button class="w-full" href="/schedules">Manage Schedules</Button>
                </div>
            </CardContent>
        </Card>
    </div>
    
    <!-- TODO: Add recent activity list -->
    <!-- TODO: Add active routines overview -->
</div>
----------------------------------------------------------------------------------
// ./frontend/src/routes/routines/+page.svelte
<script lang="ts">
    import { onMount } from 'svelte';
    import { routines } from '$lib/stores/routines';
    import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
    import { Button } from '$lib/components/ui/button';
    import { api } from '$lib/api';

    let loading = true;
    let error = '';

    onMount(async () => {
        try {
            // TODO: Load routines list
            // TODO: Update routines store
        } catch (err) {
            error = 'Failed to load routines';
        } finally {
            loading = false;
        }
    });
</script>

<div class="space-y-6">
    <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold">Routines</h1>
        <Button href="/routines/new">Create New Routine</Button>
    </div>

    {#if loading}
        <p>Loading routines...</p>
    {:else if error}
        <p class="text-red-500">{error}</p>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- TODO: Implement routine cards list -->
        </div>
    {/if}
</div>----------------------------------------------------------------------------------
// ./frontend/src/routes/routines/[id]/+page.svelte
<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { currentRoutine } from '$lib/stores/routines';
    import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
    import { Button } from '$lib/components/ui/button';
    import { api } from '$lib/api';

    let loading = true;
    let error = '';
    let routineId = $page.params.id;

    onMount(async () => {
        try {
            // TODO: Load routine details
            // TODO: Update currentRoutine store
        } catch (err) {
            error = 'Failed to load routine';
        } finally {
            loading = false;
        }
    });

    async function startRoutine() {
        try {
            // TODO: Implement routine start logic
        } catch (err) {
            error = 'Failed to start routine';
        }
    }
</script>

<div class="space-y-6">
    {#if loading}
        <p>Loading routine...</p>
    {:else if error}
        <p class="text-red-500">{error}</p>
    {:else}
        <div class="flex justify-between items-center">
            <h1 class="text-3xl font-bold">{$currentRoutine?.name || 'Routine Details'}</h1>
            <Button on:click={startRoutine}>Start Routine</Button>
        </div>

        <Card>
            <CardHeader>
                <CardTitle>Routine Steps</CardTitle>
            </CardHeader>
            <CardContent>
                <!-- TODO: Implement routine steps visualization -->
            </CardContent>
        </Card>

        <!-- TODO: Add execution history -->
        <!-- TODO: Add schedule management -->
    {/if}
</div>----------------------------------------------------------------------------------
// ./frontend/src/routes/auth/register/+page.svelte
<script lang="ts">
    import { api } from '$lib/api';
    import { goto } from '$app/navigation';
    import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '$lib/components/ui/card';
    import { Input } from '$lib/components/ui/input';
    import { Button } from '$lib/components/ui/button';
    import { Label } from '$lib/components/ui/label';

    let email = '';
    let password = '';
    let confirmPassword = '';
    let error = '';

    async function handleRegister() {
        try {
            if (password !== confirmPassword) {
                error = 'Passwords do not match';
                return;
            }

            await api.auth.register(email, password);
            await goto('/auth/login');
        } catch (err) {
            error = err instanceof Error ? err.message : 'Registration failed. Please try again.';
        }
    }
</script>

<div class="container mx-auto flex items-center justify-center min-h-screen">
    <Card class="w-full max-w-md">
        <CardHeader>
            <CardTitle>Create an Account</CardTitle>
            <CardDescription>Sign up for Dropfarm</CardDescription>
        </CardHeader>
        <CardContent>
            <form on:submit|preventDefault={handleRegister} class="space-y-4">
                <div class="space-y-2">
                    <Label for="email">Email</Label>
                    <Input type="email" id="email" bind:value={email} required />
                </div>
                <div class="space-y-2">
                    <Label for="password">Password</Label>
                    <Input type="password" id="password" bind:value={password} required />
                </div>
                <div class="space-y-2">
                    <Label for="confirmPassword">Confirm Password</Label>
                    <Input type="password" id="confirmPassword" bind:value={confirmPassword} required />
                </div>
                {#if error}
                    <p class="text-red-500 text-sm">{error}</p>
                {/if}
                <Button type="submit" class="w-full">Register</Button>
            </form>
        </CardContent>
        <CardFooter class="flex justify-center">
            <a href="/auth/login" class="text-sm text-blue-600 hover:underline">
                Already have an account? Login
            </a>
        </CardFooter>
    </Card>
</div>----------------------------------------------------------------------------------
// ./frontend/src/routes/auth/login/+page.svelte
<script lang="ts">
    import { api } from '$lib/api';
    import { goto } from '$app/navigation';
    import { auth } from '$lib/stores/auth';
    import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '$lib/components/ui/card';
    import { Input } from '$lib/components/ui/input';
    import { Button } from '$lib/components/ui/button';
    import { Label } from '$lib/components/ui/label';

    let email = '';
    let password = '';
    let error = '';

    async function handleLogin() {
        try {
            const response = await api.auth.login(email, password);
            auth.setUser(response.user);
            await goto('/dashboard');
        } catch (err) {
            error = err instanceof Error ? err.message : 'Login failed. Please check your credentials.';
        }
    }
</script>

<div class="container mx-auto flex items-center justify-center min-h-screen">
    <Card class="w-full max-w-md">
        <CardHeader>
            <CardTitle>Login to Dropfarm</CardTitle>
            <CardDescription>Enter your credentials to access your account</CardDescription>
        </CardHeader>
        <CardContent>
            <form on:submit|preventDefault={handleLogin} class="space-y-4">
                <div class="space-y-2">
                    <Label for="email">Email</Label>
                    <Input type="email" id="email" bind:value={email} required />
                </div>
                <div class="space-y-2">
                    <Label for="password">Password</Label>
                    <Input type="password" id="password" bind:value={password} required />
                </div>
                {#if error}
                    <p class="text-red-500 text-sm">{error}</p>
                {/if}
                <Button type="submit" class="w-full">Login</Button>
            </form>
        </CardContent>
        <CardFooter class="flex justify-center">
            <a href="/auth/register" class="text-sm text-blue-600 hover:underline">
                Don't have an account? Register
            </a>
        </CardFooter>
    </Card>
</div>----------------------------------------------------------------------------------
// ./frontend/src/routes/schedules/+page.svelte
<script lang="ts">
    import { onMount } from 'svelte';
    import { schedules } from '$lib/stores/schedules';
    import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
    import { Button } from '$lib/components/ui/button';
    import { api } from '$lib/api';

    let loading = true;
    let error = '';

    onMount(async () => {
        try {
            // TODO: Load schedules list
            // TODO: Update schedules store
        } catch (err) {
            error = 'Failed to load schedules';
        } finally {
            loading = false;
        }
    });
</script>

<div class="space-y-6">
    <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold">Schedules</h1>
        <Button href="/schedules/new">Create New Schedule</Button>
    </div>

    {#if loading}
        <p>Loading schedules...</p>
    {:else if error}
        <p class="text-red-500">{error}</p>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- TODO: Implement schedule cards list -->
        </div>
    {/if}
</div>----------------------------------------------------------------------------------
// ./frontend/src/routes/schedules/[id]/+page.svelte
<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { currentSchedule } from '$lib/stores/schedules';
    import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
    import { Button } from '$lib/components/ui/button';
    import { api } from '$lib/api';

    let loading = true;
    let error = '';
    let scheduleId = $page.params.id;

    onMount(async () => {
        try {
            // TODO: Load schedule details
            // TODO: Update currentSchedule store
        } catch (err) {
            error = 'Failed to load schedule';
        } finally {
            loading = false;
        }
    });

    async function toggleSchedule() {
        try {
            // TODO: Implement schedule toggle logic
        } catch (err) {
            error = 'Failed to update schedule';
        }
    }
</script>

<div class="space-y-6">
    {#if loading}
        <p>Loading schedule...</p>
    {:else if error}
        <p class="text-red-500">{error}</p>
    {:else}
        <div class="flex justify-between items-center">
            <h1 class="text-3xl font-bold">Schedule Details</h1>
            <Button on:click={toggleSchedule}>
                {$currentSchedule?.is_active ? 'Disable' : 'Enable'} Schedule
            </Button>
        </div>

        <Card>
            <CardHeader>
                <CardTitle>Schedule Configuration</CardTitle>
            </CardHeader>
            <CardContent>
                <!-- TODO: Implement schedule configuration form -->
            </CardContent>
        </Card>

        <!-- TODO: Add execution history -->
        <!-- TODO: Add routine details reference -->
    {/if}
</div>----------------------------------------------------------------------------------
// ./frontend/src/lib/index.ts
// place files you want to import through the `$lib` alias in this folder.
----------------------------------------------------------------------------------
// ./frontend/src/lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { cubicOut } from "svelte/easing";
import type { TransitionConfig } from "svelte/transition";

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

type FlyAndScaleParams = {
	y?: number;
	x?: number;
	start?: number;
	duration?: number;
};

export const flyAndScale = (
	node: Element,
	params: FlyAndScaleParams = { y: -8, x: 0, start: 0.95, duration: 150 }
): TransitionConfig => {
	const style = getComputedStyle(node);
	const transform = style.transform === "none" ? "" : style.transform;

	const scaleConversion = (
		valueA: number,
		scaleA: [number, number],
		scaleB: [number, number]
	) => {
		const [minA, maxA] = scaleA;
		const [minB, maxB] = scaleB;

		const percentage = (valueA - minA) / (maxA - minA);
		const valueB = percentage * (maxB - minB) + minB;

		return valueB;
	};

	const styleToString = (
		style: Record<string, number | string | undefined>
	): string => {
		return Object.keys(style).reduce((str, key) => {
			if (style[key] === undefined) return str;
			return str + `${key}:${style[key]};`;
		}, "");
	};

	return {
		duration: params.duration ?? 200,
		delay: 0,
		css: (t) => {
			const y = scaleConversion(t, [0, 1], [params.y ?? 5, 0]);
			const x = scaleConversion(t, [0, 1], [params.x ?? 0, 0]);
			const scale = scaleConversion(t, [0, 1], [params.start ?? 0.95, 1]);

			return styleToString({
				transform: `${transform} translate3d(${x}px, ${y}px, 0) scale(${scale})`,
				opacity: t
			});
		},
		easing: cubicOut
	};
};----------------------------------------------------------------------------------
// ./frontend/src/lib/api.ts
// src/lib/api.ts
const BASE_URL = 'http://localhost:8000/api/v1'; // Add this line

interface LoginResponse {
    access_token: string;
    token_type: string;
    user: {
        id: number;
        email: string;
        is_active: boolean;
    };
}

export const api = {
    auth: {
        login: async (email: string, password: string): Promise<LoginResponse> => {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);
            
            const response = await fetch(`${BASE_URL}/auth/login`, {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Login failed');
            }
            
            return await response.json();
        },
        
        register: async (email: string, password: string) => {
            const response = await fetch(`${BASE_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Registration failed');
            }
            
            return response.json();
        }
    }
};----------------------------------------------------------------------------------
// ./frontend/src/lib/stores/routines.ts
import { writable } from 'svelte/store';

export const routines = writable([]);
export const currentRoutine = writable(null);

// TO-DO: Implement routines store
----------------------------------------------------------------------------------
// ./frontend/src/lib/stores/schedules.ts
import { writable } from 'svelte/store';

export const schedules = writable([]);
export const currentSchedule = writable(null);

// TO-DO: Implement schedules store----------------------------------------------------------------------------------
// ./frontend/src/lib/stores/auth.ts
// src/lib/stores/auth.ts
import { writable } from 'svelte/store';

interface User {
    id: number;
    email: string;
    is_active: boolean;
}

function createAuthStore() {
    const { subscribe, set } = writable<User | null>(null);
    const { subscribe: subscribeAuth, set: setAuth } = writable(false);

    return {
        subscribe,
        subscribeAuth,
        setUser: (user: User | null) => {
            set(user);
            setAuth(!!user);
        },
        logout: () => {
            set(null);
            setAuth(false);
        }
    };
}

export const auth = createAuthStore();
export const user = { subscribe: auth.subscribe }; // Add this line
export const isAuthenticated = { subscribe: auth.subscribeAuth };----------------------------------------------------------------------------------
// ./frontend/src/lib/components/NotificationToast.svelte
<script lang="ts">
    export let message: string;
    export let type: 'success' | 'error' | 'info' = 'info';
</script>

<div class="toast" class:success={type === 'success'} class:error={type === 'error'}>
    {message}
</div>

<style>
    .toast {
        /* TODO: Add toast styles */
    }----------------------------------------------------------------------------------
// ./frontend/src/lib/components/StatsWidget.svelte
<script lang="ts">
    export let stats: any;
</script>

<div class="stats-widget">
    <!-- TODO: Implement stats display -->
</div>----------------------------------------------------------------------------------
// ./frontend/src/lib/components/Nav.svelte
<script lang="ts">
    import { routines } from '$lib/stores/routines';
    import { schedules } from '$lib/stores/schedules';
    import { isAuthenticated } from '$lib/stores/auth';
</script>

<nav class="bg-white shadow">
    <div class="container mx-auto px-4">
        <div class="flex justify-between h-16">
            <div class="flex">
                <a href="/" class="flex items-center">Dropfarm</a>
                
                {#if $isAuthenticated}
                    <a href="/dashboard" class="ml-8">Dashboard</a>
                    <a href="/routines" class="ml-4">Routines</a>
                    <a href="/schedules" class="ml-4">Schedules</a>
                {/if}
            </div>
            
            <div class="flex items-center">
                {#if $isAuthenticated}
                    <button class="ml-4">Logout</button>
                {:else}
                    <a href="/auth/login">Login</a>
                    <a href="/auth/register" class="ml-4">Register</a>
                {/if}
            </div>
        </div>
    </div>
</nav>----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/label/index.ts
import Root from "./label.svelte";

export {
	Root,
	//
	Root as Label,
};
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/label/label.svelte
<script lang="ts">
	import { Label as LabelPrimitive } from "bits-ui";
	import { cn } from "$lib/utils.js";

	type $$Props = LabelPrimitive.Props;
	type $$Events = LabelPrimitive.Events;

	let className: $$Props["class"] = undefined;
	export { className as class };
</script>

<LabelPrimitive.Root
	class={cn(
		"text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
		className
	)}
	{...$$restProps}
	on:mousedown
>
	<slot />
</LabelPrimitive.Root>
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/card/index.ts
import Root from "./card.svelte";
import Content from "./card-content.svelte";
import Description from "./card-description.svelte";
import Footer from "./card-footer.svelte";
import Header from "./card-header.svelte";
import Title from "./card-title.svelte";

export {
	Root,
	Content,
	Description,
	Footer,
	Header,
	Title,
	//
	Root as Card,
	Content as CardContent,
	Description as CardDescription,
	Footer as CardFooter,
	Header as CardHeader,
	Title as CardTitle,
};

export type HeadingLevel = "h1" | "h2" | "h3" | "h4" | "h5" | "h6";
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/card/card-description.svelte
<script lang="ts">
	import type { HTMLAttributes } from "svelte/elements";
	import { cn } from "$lib/utils.js";

	type $$Props = HTMLAttributes<HTMLParagraphElement>;

	let className: $$Props["class"] = undefined;
	export { className as class };
</script>

<p class={cn("text-muted-foreground text-sm", className)} {...$$restProps}>
	<slot />
</p>
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/card/card.svelte
<script lang="ts">
	import type { HTMLAttributes } from "svelte/elements";
	import { cn } from "$lib/utils.js";

	type $$Props = HTMLAttributes<HTMLDivElement>;

	let className: $$Props["class"] = undefined;
	export { className as class };
</script>

<div
	class={cn("bg-card text-card-foreground rounded-lg border shadow-sm", className)}
	{...$$restProps}
>
	<slot />
</div>
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/card/card-header.svelte
<script lang="ts">
	import type { HTMLAttributes } from "svelte/elements";
	import { cn } from "$lib/utils.js";

	type $$Props = HTMLAttributes<HTMLDivElement>;

	let className: $$Props["class"] = undefined;
	export { className as class };
</script>

<div class={cn("flex flex-col space-y-1.5 p-6 pb-0", className)} {...$$restProps}>
	<slot />
</div>
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/card/card-content.svelte
<script lang="ts">
	import type { HTMLAttributes } from "svelte/elements";
	import { cn } from "$lib/utils.js";

	type $$Props = HTMLAttributes<HTMLDivElement>;

	let className: $$Props["class"] = undefined;
	export { className as class };
</script>

<div class={cn("p-6", className)} {...$$restProps}>
	<slot />
</div>
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/card/card-title.svelte
<script lang="ts">
	import type { HTMLAttributes } from "svelte/elements";
	import type { HeadingLevel } from "./index.js";
	import { cn } from "$lib/utils.js";

	type $$Props = HTMLAttributes<HTMLHeadingElement> & {
		tag?: HeadingLevel;
	};

	let className: $$Props["class"] = undefined;
	export let tag: $$Props["tag"] = "h3";
	export { className as class };
</script>

<svelte:element
	this={tag}
	class={cn("text-lg font-semibold leading-none tracking-tight", className)}
	{...$$restProps}
>
	<slot />
</svelte:element>
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/card/card-footer.svelte
<script lang="ts">
	import type { HTMLAttributes } from "svelte/elements";
	import { cn } from "$lib/utils.js";

	type $$Props = HTMLAttributes<HTMLDivElement>;

	let className: $$Props["class"] = undefined;
	export { className as class };
</script>

<div class={cn("flex items-center p-6 pt-0", className)} {...$$restProps}>
	<slot />
</div>
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/button/index.ts
import { type VariantProps, tv } from "tailwind-variants";
import type { Button as ButtonPrimitive } from "bits-ui";
import Root from "./button.svelte";

const buttonVariants = tv({
	base: "ring-offset-background focus-visible:ring-ring inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
	variants: {
		variant: {
			default: "bg-primary text-primary-foreground hover:bg-primary/90",
			destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
			outline:
				"border-input bg-background hover:bg-accent hover:text-accent-foreground border",
			secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
			ghost: "hover:bg-accent hover:text-accent-foreground",
			link: "text-primary underline-offset-4 hover:underline",
		},
		size: {
			default: "h-10 px-4 py-2",
			sm: "h-9 rounded-md px-3",
			lg: "h-11 rounded-md px-8",
			icon: "h-10 w-10",
		},
	},
	defaultVariants: {
		variant: "default",
		size: "default",
	},
});

type Variant = VariantProps<typeof buttonVariants>["variant"];
type Size = VariantProps<typeof buttonVariants>["size"];

type Props = ButtonPrimitive.Props & {
	variant?: Variant;
	size?: Size;
};

type Events = ButtonPrimitive.Events;

export {
	Root,
	type Props,
	type Events,
	//
	Root as Button,
	type Props as ButtonProps,
	type Events as ButtonEvents,
	buttonVariants,
};
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/button/button.svelte
<script lang="ts">
	import { Button as ButtonPrimitive } from "bits-ui";
	import { type Events, type Props, buttonVariants } from "./index.js";
	import { cn } from "$lib/utils.js";

	type $$Props = Props;
	type $$Events = Events;

	let className: $$Props["class"] = undefined;
	export let variant: $$Props["variant"] = "default";
	export let size: $$Props["size"] = "default";
	export let builders: $$Props["builders"] = [];
	export { className as class };
</script>

<ButtonPrimitive.Root
	{builders}
	class={cn(buttonVariants({ variant, size, className }))}
	type="button"
	{...$$restProps}
	on:click
	on:keydown
>
	<slot />
</ButtonPrimitive.Root>
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/input/index.ts
import Root from "./input.svelte";

export type FormInputEvent<T extends Event = Event> = T & {
	currentTarget: EventTarget & HTMLInputElement;
};
export type InputEvents = {
	blur: FormInputEvent<FocusEvent>;
	change: FormInputEvent<Event>;
	click: FormInputEvent<MouseEvent>;
	focus: FormInputEvent<FocusEvent>;
	focusin: FormInputEvent<FocusEvent>;
	focusout: FormInputEvent<FocusEvent>;
	keydown: FormInputEvent<KeyboardEvent>;
	keypress: FormInputEvent<KeyboardEvent>;
	keyup: FormInputEvent<KeyboardEvent>;
	mouseover: FormInputEvent<MouseEvent>;
	mouseenter: FormInputEvent<MouseEvent>;
	mouseleave: FormInputEvent<MouseEvent>;
	mousemove: FormInputEvent<MouseEvent>;
	paste: FormInputEvent<ClipboardEvent>;
	input: FormInputEvent<InputEvent>;
	wheel: FormInputEvent<WheelEvent>;
};

export {
	Root,
	//
	Root as Input,
};
----------------------------------------------------------------------------------
// ./frontend/src/lib/components/ui/input/input.svelte
<script lang="ts">
	import type { HTMLInputAttributes } from "svelte/elements";
	import type { InputEvents } from "./index.js";
	import { cn } from "$lib/utils.js";

	type $$Props = HTMLInputAttributes;
	type $$Events = InputEvents;

	let className: $$Props["class"] = undefined;
	export let value: $$Props["value"] = undefined;
	export { className as class };

	// Workaround for https://github.com/sveltejs/svelte/issues/9305
	// Fixed in Svelte 5, but not backported to 4.x.
	export let readonly: $$Props["readonly"] = undefined;
</script>

<input
	class={cn(
		"border-input bg-background ring-offset-background placeholder:text-muted-foreground focus-visible:ring-ring flex h-10 w-full rounded-md border px-3 py-2 text-sm file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
		className
	)}
	bind:value
	{readonly}
	on:blur
	on:change
	on:click
	on:focus
	on:focusin
	on:focusout
	on:keydown
	on:keypress
	on:keyup
	on:mouseover
	on:mouseenter
	on:mouseleave
	on:mousemove
	on:paste
	on:input
	on:wheel|passive
	{...$$restProps}
/>
----------------------------------------------------------------------------------
