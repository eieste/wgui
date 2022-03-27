FROM alpine:3.15.2 as tailwind

COPY ./ build/

ADD https://github.com/tailwindlabs/tailwindcss/releases/download/v3.0.23/tailwindcss-linux-x64 /usr/local/bin/tailwindcss

RUN apk add make

RUN chmod +x /usr/local/bin/tailwindcss; \
    cd /build/; \
    make build


FROM python:3.9-buster

RUN pip install --upgrade pip

COPY ./ build/

COPY --from=tailwind build/wgui/static/css/tailwind.css build/wgui/static/css/tailwind.css

RUN apt install -y libxml2 libxslt libxml2-dev libxslt-dev gcc libxml2-dev libxslt1-dev; \
    pip install lxml

RUN cd build; \
    python3 setup.py build; \
    python3 setup.py install
