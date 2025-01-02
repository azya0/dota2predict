## Problems with fix

```
File "...\dota2predict\database\config.py", line 55, in validate_sqlalchemy_url
    port=int(info.data["POSTGRES_PORT"]),
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

this problem occurs when you try to create a new migration version using the command:

```
alembic revision --autogenerate
```

## Solution

1. Check your env variables
2. Make sure that the **DEV_MODE** variable is undefined or set to True.

## Removing

Linux:

```
unset DEV_MODE
```

Powershell:

```
rm env:DEV_MODE
```