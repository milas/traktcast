# traktcast
[![Build Status](https://travis-ci.org/milas/traktcast.svg?branch=master)](https://travis-ci.org/milas/traktcast)

Automatically scrobble what's playing on Chromecast to Trakt

# Requirements
* Python 3.5 (other versions may work, but have not been tested)


# Installation
1. Clone the repo: `git clone https://github.com/milas/traktcast`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`


# Authentication
When Traktcast starts, it will generate a device code using the
Trakt.tv API and provide you with a link to enter the code at.


You should only have to do this once and Traktcast will save the
result. See the `TRAKT_AUTH` environment variable if you want to
customize where it is saved/loaded from.


# Configuration
## `TRAKT_STAGING`
If defined and set to a truthy value (e.g. 1), this will cause
Traktcast to connect to and use the Trakt.tv staging API. If you
specify your own custom application OAuth client ID, make sure
it is for a staging application.


## `TRAKT_AUTH`
Path to a JSON file with Trakt credentials. By default, this will
be `~/.traktcast/auth.json` (or `~/.traktcast/auth.staging.json` if
staging mode is enabled). If this file exists and contains valid
credentials, they will be used. If it does not exist, Traktcast will
create it after authentication for future use.


## `TRAKT_CLIENT_ID`
Traktcast has a registered application on production Trakt.tv as well
as the staging version. It will automatically use the client ID for
these applications for authentication, but if you want to override this
for some reason, you can do so by specifying a different OAuth client
ID.


# Supported Services
In theory, this will work with any application that makes appropriate
use of the Chromecast media metadata. Only TV shows are supported
currently, movies will be added soon.


## Hulu Plus
Hulu does not provide the Chromecast with metadata about the currently
playing show. Hulu custom messages are watched and an attempt is made
to resolve their metadata. This is pretty fragile, and is likely to
break if they change something with their app or website.


# Limitations
Currently, only media status change events are monitored, so things
might not get scrobbled properly on disconnection, for example.
