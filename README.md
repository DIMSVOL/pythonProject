# Project   
***Project consists of the following structural parts:***

- Table Scraper
- PostgreSQL Database
- API Tornado Application


## Installation
Python version 3.8+ are required.

Install requirements
```bash
pip install -r requirements.txt
```

## Table Scraper

Script **run_scraper.py** create ***TableScraper*** object and parse data
from [Summary of Python 3's built-in types](https://proglib.io/p/slozhnost-algoritmov-i-operaciy-na-primere-python-2020-11-03) table

### Launch
Run the scraper to print data in console:

```bash
python run_scraper.py --dry_run 
```

Run the scraper to add data into the table **Algorithms**:

```bash
python run_scraper.py 
```


## PostgreSQL Database

Script **db_init.py** Initialize database and create tables ***Algorithms*** and ***Users***

### Launch


```bash
python db_init.py 
```

## Description
Table **Algorithms** contains next columns:

- id (int, primary key, not null)
- operation (str), 
- complexity (str), 
- example (str), 
- type (int)

Table **Users** contains next columns:

- id (int, primary key, not null), 
- login (str, unique, not null), 
- password (str, not null), 
- created_at (datetime, not null), 
- last_request (datetime)


Database queries are implemented using ORM SqlAlchemy

### Security
User passwords storing in databases after using **bcrypt password-hashing function**


## API Tornado Application

### Launch

```bash
python run_api.py 
```
### Description

Tornado Application handle 2 requests:
+ POST /api/login (user authorization).

Example of request:
```json
{
    "login": "my_user",
    "password": "my_password"
}
```

+ GET /api/data  (Shows whole data contained in the **Algorithms** table)

Example of response:

```json
{
    "data": [
        {
            "id": 1,
            "operation": "Получение элемента",
            "example": "l[i]",
            "type": "list"
        },
        {
            "id": 2,
            "operation": "Сохранение элемента",
            "example": "l[i] = 0",
            "type": "list"
        },
        {
            "id": 3,
            "operation": "Размер списка",
            "example": "len(l)",
            "type": "list"
        }
    ],
    "total": 3
}
```
The request is processed only from authorized users.

### Swagger
After running api this service will be available on [http://localhost:8088/swagger](http://localhost:8088/swagger) with Swagger UI.