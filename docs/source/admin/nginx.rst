=====
Nginx
=====

Setup uwsgi with nginx


Create a uwsgi.ini file
( You can create it in /etc/wgui/ )


.. code-block::

    [uwsgi]
    wsgi-file = /usr/local/lib/python3.7/site-packages/wgui/wsgi.py
    pyargv = -c /etc/wgui/wgui.yml server
    callable = app
    socket = /var/run/wgui.sock
    chmod-socket = 666
    chown-socket = nginx:nginx

Create a systemd service file:
/etc/systemd/system/system/wgui.service

.. code-block::

    [Unit]
    Description=uWSGI wgui
    After=syslog.target

    [Service]
    ExecStart=/usr/local/bin/uwsgi --ini /etc/wgui/uwsgi.ini
    RuntimeDirectory=uwsgi
    Restart=always
    KillSignal=SIGQUIT
    Type=notify
    StandardError=syslog
    NotifyAccess=all
    User=nginx
    Group=nginx


    [Install]
    WantedBy=multi-user.target


Configure your nginx:

.. code-block::

    error_log memory:32m debug;

    upstream uwsgiwgui {
      server unix://var/run/wgui.sock;
    }

    server {
        server_name <YOURDOMAIN>>;

        location / {
            uwsgi_pass uwsgiwgui;
            include uwsgi_params;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        listen 443 ssl; # managed by Certbot
    }

