#docker run --rm --env-file .env -e APP_MODE=SCRAPE --network=host discogs
docker run --rm --env-file .env -e APP_MODE=SCRAPE -e DB_HOST=`hostname -I | awk '{print $1}'` discogs