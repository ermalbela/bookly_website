=================================================================
==============================ROLES==============================
=================================================================

===================CAPABLE OF=======================
        ||   CHANGE ROLES     ||
        ||   CRUD ON USERS    ||
ADMIN   ||   BOOK SUBMISSIONS ||
        ||   CRUD ON REVIEWS  ||
        ||   REVOKING ACCESS  ||


===================CAPABLE OF=======================
        ||   CRUD ON THEIR OWN SUBMISSIONS   ||
USER    ||   CRUD ON THEIR OWN REVIEWS       ||
        ||   CRUD ON THEIR OWN ACCOUNTS      ||




=================================================================
==========================AUTHENTICATION=========================
=================================================================

MECHANISM       : JWT
TOKEN TYPE      : Bearer Tokens
ACCESS TOKEN    : Short-lived  (expiry: 1 hour)
REFRESH TOKEN   : Long-lived   (expiry: 7 days)
SIGNING ALG     : HS256
TOKEN STORAGE   : Redis blocklist (for revoked/logged-out tokens)




=================================================================
===========================TECH STACK============================
=================================================================

==============================BACKEND============================

FRAMEWORK       : FastAPI
DATABASE        : PostgreSQL
ORM             : SQLModel + SQLAlchemy
MIGRATIONS      : Alembic
VALIDATION      : Pydantic
AUTH            : PyJWT
CACHE/BLOCKLIST : Redis (port:6379)
EMAIL           : fastapi-mail
IMAGES          : Cloudinary
TASK QUEUE      : Celery
TASK MONITOR    : Flower
MESSAGE BROKER  : Redis
TESTING         : pytest + schemathesis + hypothesis

==============================FRONTEND===========================

FRAMEWORK       : Vue 3 (Composition API)
LANGUAGE        : TypeScript
STYLING         : Tailwind CSS
STATE           : Pinia
ROUTING         : Vue Router
HTTP CLIENT     : Axios
BUILD TOOL      : Vite
TESTING         : Vitest + Vue Test Utils




=================================================================
======================COMMANDS TO RUN APP========================
=================================================================

==============================BACKEND============================

RUN FASTAPI     : fastapi dev src/
RUN CELERY      : celery -A src.celery_tasks.c_app worker --pool=solo -l info
FLOWER PORT     : http://localhost:5555/

==============================FRONTEND===========================

INSTALL         : npm install
RUN DEV         : npm run dev
RUN TESTS       : npm run test:run
DEV PORT        : http://localhost:5173/
