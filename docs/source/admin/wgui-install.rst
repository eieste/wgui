============
Install wgui
============

Docker Setup
============

comming Soon



Manual Setup
============

There should be python > 3.8 on the system

.. code-block::

   apt install python3 python3-virtualenv python3-pip

You should have an existing  :ref:`Wireguard Setup <admin/wg-install:Install Wireguard>>`.

For installation you can use pip.
Its nessesary to use an virtual environment

.. code-block:: python

   virtualenv venv/
   source venv/bin/activate
   pip install wgui

Create your base configuration folder at /etc

.. code-block:: bash

    mkdir /etc/wgui



Setup web-UI
============

Its possible to use wgui only for cli command usage.
But if you like the full experience you should setup the web-ui.

Its