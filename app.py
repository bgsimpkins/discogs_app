import os
import time
from flask import Flask, render_template, request, url_for

import dbUtils
import discogs_api_utils as apiUtils
from dotenv import load_dotenv

import scrape

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def search_page():
    conn = dbUtils.connect_to_db()
    token = dbUtils.get_current_token(conn)

    posted_form_id = None

    # 2-element array (0=artist, 1=album)
    searched_data = None

    search_results = None
    alert_text = None

    if request.method == 'POST':
        posted_form_id = request.form['form_id']
        print('Form={form_id}'.format(form_id=posted_form_id))

        # Use hidden input to differentiate forms
        # If click 'Save Token', write token to DB and refresh token object
        if posted_form_id == 'token_saved':
            print('Saving token')
            token_value = request.form['save_token']
            dbUtils.set_token(conn, token_value)
            token = dbUtils.get_current_token(conn)

        elif posted_form_id == 'do_search_album':
            dq = apiUtils.DiscogsQueryer(token['token'])

            print('Searching for album {}'.format(request.form['search_album']))
            searched_data = [request.form['search_artist'], request.form['search_album']]
            search_results = dq.search_by_artist_and_album(searched_data[0], searched_data[1], int(request.form['max_results']))
            print(search_results)

        elif posted_form_id == 'save_to_watchlist':
            dq = apiUtils.DiscogsQueryer(token['token'])
            master_id = request.form['selected_master_id']
            print('Saving to watchlist: {id}'.format(id=master_id))
            record_master = dq.get_master(master_id)
            record_master.formats = request.form.get('format_select')
            dbUtils.add_master_to_watchlist(conn, record_master)
            alert_text = 'Album saved to watchlist!!'

    return render_template(
        'search.html',
        token=token,
        form_id=posted_form_id,
        searched_data=searched_data,
        search_results=search_results,
        alert_text=alert_text
    )


@app.route('/watch', methods=['GET', 'POST'])
def market_watch_page():

    conn = dbUtils.connect_to_db()
    watchlist = dbUtils.get_watchlist(conn)

    selected_master_id = None
    item_list = None

    alert_text = None

    if request.method == 'POST':
        if 'update_price' in request.form:
            for x in request.form.items():
                if x[0][0:3] != 'des': continue

                master_id = int(x[0][4:len(x[0])])
                desired_price = float(x[1])
                print('Updating desired price for master_id={master_id} to {price}'.format(master_id=master_id, price=desired_price))
                dbUtils.update_desired_price_for_master(conn, master_id, desired_price)

        elif 'delete_items' in request.form:
            for x in request.form.items():
                if x[0][0:4] != 'sel_': continue

                print('Deleting: {x}'.format(x=x))
                dbUtils.delete_from_watchlist(conn, x[1])

        elif 'add_to_scrape_queue' in request.form:
            # Previously handled with JQuery/AJAX call. Was sucky and inefficient
            print('Scraping Watchlist!')
            master_list = []
            for x in request.form.items():
                if x[0][0:4] != 'sel_': continue
                master_list.append(x[1])

            dbUtils.add_to_scrape_queue(conn,1,master_list)
            alert_text = """Items added to <a href="/scrape_queue">Scrape Queue</a>"""

        elif 'selected_master_id' in request.form:
            selected_master_id = request.form['selected_master_id']
            item_list = dbUtils.get_record_items_for_master(conn, selected_master_id)

        # Watchlist has changed. Reload
        watchlist = dbUtils.get_watchlist(conn)


    return render_template(
        'marketWatch.html',
        watchlist=watchlist,
        selected_master_id=int(selected_master_id) if selected_master_id is not None else None,
        item_list=item_list,
        alert_text=alert_text
    )

@app.route('/scrape_queue', methods=['GET', 'POST'])
def scrape_queue_page():
    conn = dbUtils.connect_to_db()

    alert_text = None
    scrape_running = False

    if dbUtils.is_scrape_active(conn,1):
        alert_text = """Scrape running! <a href="/scrape_queue">Refresh</a>"""
        scrape_running = True

    if request.method == 'POST':
        if 'scrape_queue' in request.form:
            print("scraping!")
            #scrape.scrape_queue(conn)


            # Need to reload scrape queue to update status
            #scrape_queue = dbUtils.get_scrape_queue(conn, 1)

    current_queue, historical_queue = dbUtils.get_scrape_queue(conn, 1)

    return render_template(
        'scrapeQueue.html',
        scrape_queue=current_queue,
        historical_queue=historical_queue,
        alert_text=alert_text,
        scrape_running=scrape_running
    )

@app.route('/do_scrape_queue', methods=['GET'])
def scrape_queue():
    conn = dbUtils.connect_to_db()
    scrape.scrape_queue(conn)

    return 0

@app.route('/scrape_service', methods=['GET'])
def scrape_for_master():
    master_id = request.args.get('master_id')

    conn = dbUtils.connect_to_db()
    res = dbUtils.get_watchlist_item(conn, master_id)

    driver = scrape.create_driver(True)

    try:
        scrape.scrape_for_master(driver, conn, master_id, res['formats'])
        return '0'
    except Exception as e:
        return str(e)

    driver.close()
    driver.quit()


@app.route('/test', methods=['GET'])
def test_stuff():
    return render_template(
        'test.html'
    )

@app.route('/test_service', methods=['GET'])
def test_service():
    return "The shit worked!"


if __name__ == '__main__':
    load_dotenv(override=False)
    APP_MODE = os.getenv('APP_MODE')
    print(f'APP_MODE={APP_MODE}')
    if APP_MODE == 'WEB_APP':
        print('Starting web app..')
        app.run(
            host="0.0.0.0",
            port=5001,
            debug=True,
            use_reloader=False
        )
    elif APP_MODE == 'SCRAPE':
        scrape.scrape_watchlist(dbUtils.connect_to_db())
    elif APP_MODE == 'SCRAPE_AND_REPORT':
        scrape.scrape_watchlist()
        #TODO: send email with report
    else:
        print('APP_MODE {APP_MODE} not supported!')
