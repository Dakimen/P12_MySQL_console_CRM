## Database Setup

This project uses MySQL. A schema-only SQL dump is provided so you can create the required tables locally.

### Prerequisites

- MySQL 8.x installed

- Access to a MySQL user with permission to create tables

1. Create a database

Log into MySQL:

```
mysql -u your_user -p
```

Then create the database:

```
CREATE DATABASE epicevents;
EXIT;
```

2. Import the schema

From your system terminal (not inside mysql>), run:

```
mysql -u your_user -p epicevents < schema_backup.sql
```

You will be prompted for your MySQL password.

This will create all required tables, indexes, and constraints without importing any data.

3. Verify the tables

Log back into MySQL:

```
mysql -u your_user -p epicevents
```

Then run:

```
SHOW TABLES;
```

You should see the full list of tables used by the application.
