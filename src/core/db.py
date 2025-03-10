import asyncio
import re
import asyncpg
import pandas as pd
import psycopg2
from src.constants.messages import UNKNOWN_ERROR
from src.core.load_config import config
from fastapi import Request as FastAPIRequest
from src.core.logger import log_async, logger


db_conn_details = config["DBConnection"]

db_host = 'localhost' if (db_conn_details["IsDBOnLocalhostForProduction"] and not config["IsDevelopment"]) else db_conn_details["Host"]
DATABASE_URL = f"postgresql://{db_conn_details['User']}@{db_host}:{db_conn_details['Port']}/{db_conn_details['DBName']}"

DB_POOL = None

MAX_RETRIES = 5  # Set max retries to avoid infinite loops


async def init_db_pool():
    """Initialize the async database connection pool"""
    global DB_POOL
    DB_POOL = await asyncpg.create_pool(DATABASE_URL, password=db_conn_details["Password"],
        min_size=1,  # Minimum number of connections in the pool
        max_size=10,  # Maximum number of connections in the pool
        timeout=5,
        statement_cache_size=0
    )

async def get_valid_connection():
    """Acquire a valid connection from the pool, retrying if needed."""
    global DB_POOL

    for attempt in range(1, MAX_RETRIES + 1):
        conn = await DB_POOL.acquire()
        if await is_connection_alive(conn):
            return conn  # ✅ Connection is valid
        else:
            await conn.close()  # Close the bad connection

    raise asyncpg.exceptions.InterfaceError(" All retries failed. No valid connection available.")


async def is_connection_alive(conn):
    """Checks if the connection is alive by running a simple SELECT 1 query."""
    try:
        await conn.execute("SELECT 1")
        return True
    except asyncpg.exceptions.PostgresError:
        return False
    

async def execute_query_async(query, params=None) -> dict[str, pd.DataFrame]:
    """
    Executes an async query using asyncpg and returns results as Pandas DataFrames.
    """
    global DB_POOL
    if DB_POOL is None or DB_POOL._closed:
        await init_db_pool()  # Ensure the pool is initialized

    result = {}
    query = convert_psycopg2_to_asyncpg(query=query)
    # conn = await asyncpg.connect(DATABASE_URL, password=db_conn_details["Password"])

    # conn = await get_valid_connection()

    try:
        async with DB_POOL.acquire() as conn:
            # await conn.execute("DISCARD ALL")
            # txn = conn.transaction()
            async with conn.transaction(): 
                # await txn.start()
                cur = await conn.fetch(query, *params if params else ())

                if not cur:
                    return result  # No cursors returned

                cursor_names = cur[0]  # Extract cursor names

                for _cursor in cursor_names:
                    try:
                        fetch_query = f'FETCH ALL IN "{_cursor}"'  # Use double quotes for safe execution
                        d = await conn.fetch(fetch_query)

                        if d:
                            df = await asyncio.to_thread(pd.DataFrame, d, columns=d[0].keys())  # pd.DataFrame(d, columns=d[0].keys())
                            result[_cursor] = df

                        else:
                            result[_cursor] = pd.DataFrame([])

                    except Exception as e:
                        await log_async(logger.error, f"Error fetching cursor {_cursor}: {e}")
                        await log_error(e, extra_info='execute_query',
                                extra_data=f'Query => {query}, Params => {params}, Cursor => {_cursor}')
            # await txn.commit()
            try:
                await conn.execute("DISCARD ALL")
            except asyncpg.exceptions.PostgresError as discard_error:
                await log_async(logger.error, f"DISCARD ALL failed: {discard_error}")

    except Exception as error:
        await log_async(logger.error, f"Database error: {error}")
        # await txn.rollback()
        await log_error(error, extra_info='execute_query', extra_data=f'Query => {query}, Params => {params}')

    finally:
        pass
        # await conn.close()

    return result



def execute_query(query, params=None) -> dict[str, pd.DataFrame]:
    # conn = psycopg2.connect(conn_string)
    conn = psycopg2.connect(dbname=db_conn_details["DBName"],
                            user=db_conn_details["User"],
                            password=db_conn_details["Password"],
                            host='localhost' if (db_conn_details["IsDBOnLocalhostForProduction"] and not config["IsDevelopment"]) else db_conn_details["Host"],
                            port=db_conn_details["Port"])

    result = {}
    try:
        cur = conn.cursor()
        cur.execute(query, params)

        cursor_names = cur.fetchall()

        if len(cursor_names)>0:

            cursor_names = cursor_names[0]

            for _cursor in cursor_names:
                try:

                    cur.execute(f'fetch all in {_cursor}')
                    d = cur.fetchall()
                    df = pd.DataFrame(d, columns=[i[0] for i in cur.description])

                    result[_cursor] = df
                except Exception as e:
                    asyncio.run(log_async(logger.error, e.__str__()))
                    asyncio.run(log_error(e, extra_info='execute_query', extra_data='Query => '+ query+', Params => '+(','.join(params))+', Cursor => '+_cursor))
        else:
            pass

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        asyncio.run(log_async(logger.error, e.__str__()))
        asyncio.run(log_error(error, extra_info='execute_query', extra_data='Query => '+ query+', Params => '+(','.join(params))))
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()

    return result


def convert_psycopg2_to_asyncpg(query: str) -> str:
    """
    Converts a SQL query using %s placeholders (psycopg2 style)
    into $1, $2, $3... placeholders for asyncpg.
    
    If the query already contains $1, $2, etc., it is not modified.
    
    Args:
        query (str): The SQL query using %s placeholders.

    Returns:
        str: The modified query using $1, $2, ... placeholders.
    """
    if re.search(r"\$\d+", query):  
        return query
    
    count = 0
    def replacer(match):
        nonlocal count
        count += 1
        return f"${count}"

    return re.sub(r"%s", replacer, query)


async def close_db_pool():
    if DB_POOL:
        await log_async(logger.info, "Closing DBPool")
        await DB_POOL.close()


async def log_global_error(exc, request: FastAPIRequest, request_body = None):
    error_message = await log_error(e=exc,
                                    route_path=request.url.path,
                                    request_method=request.method,
                                    request_query_params=str(request.query_params),
                                    request_client_host=request.headers.get("X-Forwarded-For", request.client.host if request.client else None),
                                    request_body=request_body)
    return error_message


async def log_error(e,
                route_path: str='',
                request_method: str='',
                request_query_params: str='',
                request_client_host: str='',
                request_body=None,
                extra_info: str='',
                extra_data: str=''):
    if e is not None:
        await execute_query_async("call usp_save_api_error_log(_error_msg => $1, _route => $2, _method => $3, _params => $4, _client => $5, _body => $6, _extra_info => $7, _extra_data => $8)",
                      (e.__str__(), route_path, request_method, request_query_params, request_client_host, request_body if request_body != '' else '{}', extra_info, extra_data))
        if config['IsDevelopment']:
            return 'Error : '+e.__str__()

    return UNKNOWN_ERROR
