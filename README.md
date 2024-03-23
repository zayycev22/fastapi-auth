[![PyPI version](https://badge.fury.io/py/auth_fastapi.svg)](https://badge.fury.io/py/auth_fastapi)
[![Downloads](https://static.pepy.tech/badge/auth_fastapi)](https://pepy.tech/project/auth_fastapi)

# FastAPI-Auth

FastAPI-Auth is an authentication library built upon the principles of Django and fastapi-users frameworks, designed for
seamless migration from Django to FastAPI.

It supports multiple ORMs including SQL Alchemy and Tortoise ORM, with plans for SQL model support in the future.

## Features

* [X] Pagination
* [X] Filtering
* [X] JWT Token-based Authentication
* [X] Endpoint Permissions
* [X] Serializers
* [X] Signals
* [X] Secret Key Generation

## Installation

For SQL Alchemy ORM:

```bash
pip install auth_fastapi[sqlalchemy]
```

For Tortoise ORM:

```bash
pip install auth_fastapi[tortoise]
```

Note: The package is named auth_fastapi because fastapi-auth already exists.

## Examples
FastAPI-auth with Tortoise ORM
https://github.com/zayycev22/fastapi_auth_tortoise_example

FastAPI-auth with SqlAlchemy ORM https://github.com/zayycev22/fastapi_auth_sqlalchemy_example

## Contributors

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/zayycev22"><img src="https://avatars.githubusercontent.com/zayycev22?v=4?s=100" width="100px;" alt="zayycev22"/><br /><sub><b>zayycev22</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/BednyYorik"><img src="https://avatars.githubusercontent.com/BednyYorik?v=4?s=100" width="100px;" alt="BednyYorik"/><br /><sub><b>BednyYorik</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ck1999"><img src="https://avatars.githubusercontent.com/ck1999?v=4?s=100" width="100px;" alt="ck1999"/><br><sub><b>ck1999</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Dragonfl1ght"><img src="https://avatars.githubusercontent.com/Dragonfl1ght?s=4?s=100" width="100px;" alt="Dragonfl1ght"/><br /><sub><b>Dragonfl1ght</b></sub></a><br /></td>
    </tr>
    </tbody>
</table>