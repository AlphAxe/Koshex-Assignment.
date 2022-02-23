# Koshex-Assignment.

1. Before running the Flask app ,make sure to have a database table whose schema is given as follows:

    database table name - url
    table content :
        column name        datatype

        url                 varchar(500)
        short_url           varchar(100)
        date_created        datetime
        count               int unsigned
        hourly_count        int unsigned

2. In database.py file,change the name of your own database name where you have created a table as mentioned in point 1 as below:
            create_engine("mysql://root@localhost/<your database>")

3. After creating above table run wsgi.py file.
3. For testing the first api you can use any tool(I used postman) ,in the body use json in the following format :
    {
        "url": "url whose shorter version is required"
    }
    and hit send and it will give all the required details.

5. For testing the second api which will return the original url just copy the api rout to postman and hit send.
