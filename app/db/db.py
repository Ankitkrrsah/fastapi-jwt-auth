from psycopg2 import connect 
 
conn = connect("dbname=user_login user=ankitkumar")


cur = conn.cursor()

