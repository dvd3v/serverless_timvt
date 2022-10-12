from timvt.db import close_db_connection, connect_to_db, register_table_catalog
from timvt.factory import VectorTilerFactory
from timvt.layer import FunctionRegistry
from fastapi import FastAPI

from settings import ApiSettings, PostgresSettings

settings = ApiSettings()
postgres_settings = PostgresSettings()

# Create Application.
app = FastAPI()

# Add Function registry to the application state
app.state.timvt_function_catalog = FunctionRegistry()


# Register Start/Stop application event handler to setup/stop the database connection
# and populate `app.state.table_catalog`
@app.on_event("startup")
async def startup_event():
    """Application startup: register the database connection and create table list."""
    await connect_to_db(app)
    await register_table_catalog(
        app
    )


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown: de-register the database connection."""
    await close_db_connection(app)

# Register endpoints.
mvt_tiler = VectorTilerFactory(
    with_tables_metadata=True,
    with_functions_metadata=True,  # add Functions metadata endpoints (/functions.json, /{function_name}.json)
    with_viewer=True,
)
app.include_router(mvt_tiler.router, tags=["Tiles"])
