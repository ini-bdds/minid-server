.. image:: https://raw.githubusercontent.com/ini-bdds/minid-server/master/minid_server/static/images/minid-logo.png

Minids (Minimal Viable Identifiers) are identifiers that are sufficiently simple to make creation and use trivial, while still having enough substance to make data easily findable, accessible, interoperable, and reusable (FAIR).

This repository contains the minid server. Minid client code is avaialble at https://github.com/fair-research/minid.


Installation
------------

The minid server is a Python Flask application.  The following steps outline how to install the server in a development setting. 

Download the source code::

  $ git clone git@github.com:ini-bdds/minid-server.git
  
Create a local configuration for development (an example configuration is included below)::

  $ vim local_config.cfg

Run the server::

  $ python main.py


Note: you will need to edit your minid client configuration to point to your local development server. 

For production deployments we suggest using Apache and uWSGI. An example WSGI configuration script is avaialble `here <https://github.com/ini-bdds/minid-server/blob/master/minid_server/minid.wsgi>`_.


Configuration
-------------

Here is an example configuration file that uses a local SQLite database and the EZID test shoulder for minting ARKs.

.. code-block:: python

  class Config(object):
      DEBUG = True
      TESTING = True

      SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/minid.db"
      SQLALCHEMY_TRACK_MODIFICATIONS = True

      HOSTNAME = "http://localhost:5000/minid"
      PORT = 5000
      LANDING_PAGE = "http://localhost:5000/minid/landingpage"

      GLOBUS_CLIENT_ID = "a5cdede9-567f-4ae5-aba5-cb997d08693a"
      GLOBUS_CLIENT_SECRET = ""

      EZID_SERVER = "https://ezid.cdlib.org"
      EZID_SCHEME = "ark:/"
      EZID_SHOULDER = "99999/fk4"
      EZID_USERNAME = "apitest"
      EZID_PASSWORD = "apitest"

      TEST_EZID_SERVER = "https://ezid.cdlib.org"
      TEST_EZID_SCHEME = "ark:/"
      TEST_EZID_SHOULDER = "99999/fk4"
      TEST_EZID_USERNAME = "apitest"
      TEST_EZID_PASSWORD = "apitest"

      # AWS account used for sending email
      AWS_ACCESS_KEY_ID = ""
      AWS_SECRET_ACCESS_KEY = ""
      AWS_EMAIL_SENDER = ""


Globus Auth
-----------

The Minid Server needs to register two items:

* A Globus App at https://developers.globus.org/
* A Resource Server Scope at https://docs.globus.org/api/auth/reference/#create_scope

Clients can then add the following scope to their login flow:

.. code-block:: python

  scopes = ["https://auth.globus.org/scopes/a5cdede9-567f-4ae5-aba5-cb997d08693a/minid"]

