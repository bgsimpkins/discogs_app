docker run -d --network=host --env-file .env --restart always discogs
#docker run -d -p 5001:5001 --env-file .env --restart always discogs
#docker run -d --publish 5001:5001 --env-file .env -e DB_HOST=`hostname -I | awk '{print $1}'` --restart always discogs
