FROM python:3.9-slim-buster
ENV TZ="America/Chicago"
RUN apt-get -y update && apt-get install -y --no-install-recommends ca-certificates curl firefox-esr wget bzip2 xz-utils

ADD requirements.txt .
RUN python -m pip install -r requirements.txt

#Install geckodriver for Firefox (HARD-CODED. NEED TO GET LATEST)
RUN GECKODRIVER_VERSION=v0.34.0 && wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

#Install firefox
RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && apt-get purge firefox && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xvf $FIREFOX_SETUP -C /opt/ && \
    #ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP

WORKDIR /app
ADD . /app

CMD ["python", "app.py"]
