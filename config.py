import os

DB_URL = os.getenv(
    "NPS_DB_URL",
    "postgresql://neondb_owner:npg_C4ghxK1yUcfw@ep-billowing-fog-agxbr2fc-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

APP_TITLE = "NPS Accounting System"

