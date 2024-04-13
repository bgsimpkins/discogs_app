import os
import mysql.connector
import pandas as pd

from discogs_data_classes import RecordItem, RecordMaster

def connect_to_db():

    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_DB')
    )
    print(conn)
    return conn


def execute_sql(conn, sql, vals):
    mycursor = conn.cursor()
    mycursor.execute(sql, vals)
    id = mycursor.lastrowid
    conn.commit()
    return id


def get_current_token(conn):
    sql = 'select * from token;'

    res = pd.read_sql(sql, conn)
    if res.shape[0] > 0:
        return res.iloc[0]
    else:
        a = {'token':'', 'token_date':''}
        return pd.Series(a, copy=False)


def set_token(conn, token: str):
    sql = 'TRUNCATE TABLE token;'
    execute_sql(conn, sql, None)

    sql = """
        INSERT INTO token VALUES( 
            %s,
            CURRENT_TIMESTAMP
        );
    """
    token = token.strip()
    execute_sql(conn, sql, [token])


def delete_release(conn, release_id):
    sql = 'DELETE FROM RecordItem WHERE release_id = %s;'
    execute_sql(conn, sql, [release_id])


def insert_record_item(conn, ri:RecordItem):

    #sql = 'SELECT 1 FROM RecordItem WHERE release_id = %s;'
    #res = pd.read_sql(sql, conn, params=[ri.release_id])

    #if res.shape[0] == 0:
    sql = """
        INSERT INTO RecordItem 
        (
            release_id,
            item_id,
            available,
            url,
            adjusted_price,
            media_condition,
            sleeve_condition,
            details,
            avg_rating,
            num_ratings,
            country,
            date_created,
            date_updated
        )
        VALUES
        (
            %(release_id)s,
            %(item_id)s,
            %(available)s,
            %(url)s,
            %(adjusted_price)s,
            %(media_condition)s,
            %(sleeve_condition)s,
            %(details)s,
            %(avg_rating)s,
            %(num_ratings)s,
            %(country)s,
            %(date_created)s,
            %(date_updated)s
        );
    """
    execute_sql(conn, sql, ri.__dict__)
    #else:
    #    print('Update')


def add_master_to_watchlist(conn, rm: RecordMaster):

    # TODO: We should probably keep track of history here.
    sql = 'DELETE FROM WatchList WHERE master_id = %s;'
    execute_sql(conn, sql, [rm.master_id])

    sql = """
        INSERT INTO WatchList
        (
            master_id,
            master_url, 
            artist,
            title,    
            formats,
            year,   
            country,
            date_created,
            date_updated
        )
        VALUES
        (
            %(master_id)s,
            %(master_url)s,
            %(artist)s,
            %(title)s, 
            %(formats)s,
            %(year)s,
            %(country)s,
            %(date_created)s,
            %(date_updated)s
        );

    """
    execute_sql(conn, sql, rm.__dict__)


def get_watchlist(conn):
    sql = """
        SELECT
            wl.*
            ,COALESCE(dtl.num_items,0) as num_items
            ,dtl.min_price
            ,dtl.last_scrape_date
        
        FROM WatchList wl
            LEFT OUTER JOIN(
                -- Summary item data
                SELECT
                    release_id as master_id
                    ,count(*) as num_items
                    ,min(adjusted_price) as min_price
                    ,max(date_created) as last_scrape_date
                FROM RecordItem
                WHERE available = 1
                GROUP BY release_id
                
            ) as dtl
            ON wl.master_id = dtl.master_id
        ORDER BY wl.artist, wl.year
        ;
    """
    res = pd.read_sql(sql, conn)

    watchlist = []
    for index, row in res.iterrows():
        watchlist.append(RecordMaster(
            master_id=row['master_id'],
            master_url=row['master_url'],
            artist=row['artist'],
            title=row['title'],
            formats=row['formats'],
            year=row['year'],
            country=row['country'],
            date_created=row['date_created'],
            date_updated=row['date_updated'],
            num_items=row['num_items'],
            min_price=row['min_price'],
            desired_price=row['desired_price'] if row['desired_price'] is not None else 100,
            last_scrape_date=row['date_scraped']

        ))
    return watchlist


def get_watchlist_item(conn, master_id):
    sql = """
            SELECT *
            FROM WatchList
            WHERE master_id = %s
            ;
        """
    res: pd.DataFrame = pd.read_sql(sql, conn, params=[master_id])
    if res.shape[0] > 0:
        return res.iloc[0]
    else:
        return None


def delete_from_watchlist(conn, id):
    sql = """
        DELETE FROM WatchList
        WHERE master_id = %s
        ;
    """
    execute_sql(conn, sql, [id])


def get_record_items_for_master(conn, master_id):
    sql = """
        SELECT *
        FROM RecordItem
        WHERE release_id = %s
        ORDER BY adjusted_price
        ;
    """
    res: pd.DataFrame = pd.read_sql(sql, conn, params=[master_id])

    item_list = []
    for index, row in res.iterrows():
        item_list.append(RecordItem(
            release_id=row['release_id'],
            item_id=row['item_id'],
            available=row['available'],
            url=row['url'],
            adjusted_price=row['adjusted_price'],
            media_condition=row['media_condition'],
            sleeve_condition=row['sleeve_condition'],
            details=row['details'],
            avg_rating=row['avg_rating'],
            num_ratings=row['num_ratings'],
            country=row['country'],
            date_created=row['date_created'],
            date_updated=row['date_updated']

        ))
    return item_list


def update_desired_price_for_master(conn, master_id, desired_price):
    sql = """
        UPDATE WatchList
            SET desired_price= %s
        WHERE master_id = %s;
    """
    execute_sql(conn, sql, [desired_price, master_id])


def update_scrape_date_for_master(conn, master_id, date_scraped):
    sql = """
            UPDATE WatchList
                SET date_scraped= %s
            WHERE master_id = %s;
        """
    execute_sql(conn, sql, [date_scraped, master_id])