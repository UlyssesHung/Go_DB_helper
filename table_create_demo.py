#!/usr/bin/env Python2.7
# coding=UTF-8
import psycopg2
import math
import random
import datetime
import pytz
import golang_migrate_generator as gmg
import golang_struct_generator_new as gsgn

"Open SSH tunnel for PostgresQL"
"ssh -i ~/.ssh/id_rsa -L 5433:ciao.cofpkzxoslpm.ap-northeast-1.rds.amazonaws.com:5432 -p 50022 chenwei@52.68.87.176"
conn = psycopg2.connect(database="postgres",
                        user="ciao", password="Kir0#alpha",
                        host="localhost", port="5433")
cur = conn.cursor()
# Create area table
query = ("""
CREATE TABLE table_create_demo (
  id SERIAL PRIMARY KEY,
  int_demo int NOT NULL,
  text_demo text NOT NULL DEFAULT '',
  bool_demo bool NOT NULL,
  float_demo FLOAT4 NOT NULL,
  timestamp_demo timestamp NOT NULL,
  timestamp_demo_null timestamp NOT NULL
);
""")
gsgn.create(query, appendshopinfo=False)
cur.execute(query)
queryall = query
conn.commit()
gmg.create(queryall)
nameList = ["赤羽信之介", "青木ひかり", "相沢雅", "藤井りな", "逢沢莉奈"]
for k, v in enumerate(nameList):
    cur.execute("""
        INSERT INTO table_create_demo(
        int_demo,
        text_demo,
        bool_demo,
        float_demo,
        timestamp_demo,
        timestamp_demo_null
        ) VALUES (%s,%s,%s,%s,%s,%s)
        """, (k, v, False, 10.1, datetime.datetime.now(),  datetime.datetime.now()))
    conn.commit()
cur.close()
conn.close()
