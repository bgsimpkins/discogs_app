import os
import mysql.connector
import pandas as pd

from discogs_data_classes import RecordItem, RecordMaster, ScrapeQueue

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


def update_scrape_date_in_watchlist(conn, master_id, date_scraped):
    sql = """
            UPDATE WatchList
                SET date_updated= CURRENT_TIMESTAMP(),
                    date_scraped = %(date_scraped)s
            WHERE master_id = %(master_id)s;
        """
    execute_sql(conn, sql, {"date_scraped":date_scraped, "master_id":master_id})


def get_scrape_queue(conn, batch_id):
    sql = """
            SELECT
                SQ.row_id,
                SQ.batch_id,
                SQ.master_id,
                WL.artist,
                WL.title,
                WL.formats,
                COALESCE(SQ.status,"") as status,
                SQ.date_updated
            FROM ScrapeQueue SQ
                INNER JOIN WatchList WL
                    ON SQ.master_id = WL.master_id
            WHERE batch_id = %s
            ORDER BY date_updated DESC
            ;
        """
    res: pd.DataFrame = pd.read_sql(sql, conn, params=[batch_id])

    current_queue = res.loc[(res["status"] != "COMPLETE") | (res["status"].isna()),]
    current_queue_list = []

    for index, row in current_queue.iterrows():
        current_queue_list.append(ScrapeQueue(
            row_id=row['row_id'],
            batch_id=row['batch_id'],
            master_id=row['master_id'],
            artist=row['artist'],
            title=row['title'],
            formats=row['formats'],
            status=row['status'],
            date_updated=row['date_updated']
        ))

    ## TODO: Should we catch and handle FAILED here?
    historical_queue = res.loc[(res["status"] == "COMPLETE"),]
    historical_queue_list = []

    for index, row in historical_queue.iterrows():
        historical_queue_list.append(ScrapeQueue(
            row_id=row['row_id'],
            batch_id=row['batch_id'],
            master_id=row['master_id'],
            artist=row['artist'],
            title=row['title'],
            formats=row['formats'],
            status=row['status'],
            date_updated=row['date_updated']
        ))

    return current_queue_list, historical_queue_list


def update_scrape_status(conn, row_id, status):

        sql = """
            UPDATE ScrapeQueue
                SET status= %s,
                    date_updated=CURRENT_TIMESTAMP()
            WHERE row_id = %s;
        """
        execute_sql(conn, sql, [status, row_id])


def add_to_scrape_queue(conn, batch_id, master_list):
    df = pd.DataFrame(columns=['batch_id','master_id'])

    i = 1
    for master_id in master_list:
        ## Upsert. Unnecesary because UI will prevent inserting while scraping. Okay to scrape something in history again
        # sql = """
        #     INSERT INTO `ScrapeQueue` (`batch_id`, `master_id`, `date_updated`)
        #         SELECT %(batch_id)s, %(master_id)s, CURRENT_TIMESTAMP() FROM DUAL
        #         WHERE NOT EXISTS (SELECT * FROM `ScrapeQueue`
        #               WHERE `batch_id`=%(batch_id)s AND `master_id`= %(master_id)s LIMIT 1);
        # """

        sql = """
            INSERT INTO `ScrapeQueue` (`batch_id`, `master_id`, `date_updated`) VALUES(
                %(batch_id)s, %(master_id)s, CURRENT_TIMESTAMP()
            );
        """
        execute_sql(conn, sql, {"batch_id": batch_id, "master_id": master_id})


def is_scrape_active(conn, batch_id):
    sql = """
            SELECT row_id
            FROM ScrapeQueue
            WHERE batch_id = %s
                AND status = "RUNNING"
            ;
            """
    res: pd.DataFrame = pd.read_sql(sql, conn, params=[batch_id])

    return res.shape[0] > 0
