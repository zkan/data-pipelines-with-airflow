# Project Instruction

ในโปรเจคนี้เราจะมาสร้าง Cryptocurrency Data Pipeline ด้วย Airflow กัน โดยจะดึงข้อมูล crypto exchange market data เป็นรายวัน โดยช่วงของข้อมูลที่ดึงมาจะเป็นข้อมูลในแต่ละชั่วโมงของวันนั้นๆ

1. เราจะใช้ `PythonOperator` เพื่อเรียกฟังก์ชั่นดึงข้อมูล OHLCV ของเหรียญ SHIB/USDT จาก Binance โดยผ่าน CCXT API และเราจะเก็บข้อมูลที่เราดึงมาไว้ที่ MinIO หรือที่ data lake เพื่อที่เราจะได้สามารถนำข้อมูลตรงนี้ไปวิเคราะห์ต่อยอด หรือแชร์ให้กับทีมอื่นๆ ได้โดยไม่จำเป็นต้องไปดึงข้อมูลจาก API อีก

   ```py
   fetch_ohlcv = PythonOperator(
       task_id="fetch_ohlcv",
       python_callable=_fetch_ohlcv,
   )
   ```

   ในข้อนี้เราต้องสร้าง connection สำหรับ MinIO ด้วย

2. ต่อไปเราจะโหลดข้อมูลมาจาก data lake เพื่อที่จะนำไปโหลดเข้า data warehouse ของเราต่อ ในที่นี้เราจะใช้ `PythonOperator` เพื่อเรียกฟังก์ชั่นสำหรับดาวน์โหลดข้อมูลมาจาก data lake

   ```py
   download_file = PythonOperator(
       task_id="download_file",
       python_callable=_download_file,
   )
   ```

3. ต่อไปเราอยากจะโหลดข้อมูลขึ้นมาไว้ที่ data warehouse ของเรา (ซึ่งในโปรเจคนี้เราจะใช้ Postgres) เพื่อที่จะสามารถวิเคราะห์ข้อมูลได้ แต่เราจะยังไม่โหลดข้อมูลของเราเข้าไปที่ table ที่ใช้วิเคราะห์ข้อมูลของเราตรงๆ เผื่อว่าเราอยากที่จะปรับปรุง หรือเปลี่ยนแปลงข้อมูลเราก่อน ดังนั้นเราจะเก็บไว้ที่ table ที่เสมือนเป็นที่ๆ เราพักข้อมูล

   การที่จะโหลดข้อมูลเข้า table ได้ เราจำเป็นต้องสร้าง table นั้นๆ ไว้ก่อน เราจะใช้ `PostgresOperator` เพื่อรัน SQL ในการสร้าง table

   ```py
   create_import_table = PostgresOperator(
       task_id="create_import_table",
       postgres_conn_id="postgres",
       sql="""
           CREATE TABLE IF NOT EXISTS cryptocurrency_import (
               timestamp BIGINT,
               open FLOAT,
               highest FLOAT,
               lowest FLOAT,
               closing FLOAT,
               volume FLOAT
           )
       """,
   )
   ```

   ในข้อนี้เราต้องสร้าง connection สำหรับ Postgres ด้วย

4. หลังจากที่เรามี table พร้อมแล้ว เราจะโหลดข้อมูลของเราจากไฟล์เข้าไป โดยใช้ `PythonOperator` เรียกฟังก์ชั่นที่เตรียมไว้ให้

   ```py
   load_data_into_database = PythonOperator(
       task_id="load_data_into_database",
       python_callable=_load_data_into_database,
   )
   ```

5. พอเรามีข้อมูลเก็บอยู่ใน table ที่เราเตรียมไว้พักข้อมูลแล้ว เราก็จะสร้าง table ที่เราจะเอาไว้สำหรับวิเคราะห์ข้อมูลกัน โดยจะใช้ `PostgresOperator` เพื่อรันคำสั่ง SQL ในการสร้าง table

   ```py
   create_final_table = PostgresOperator(
       task_id="create_final_table",
       postgres_conn_id="postgres",
       sql="""
           CREATE TABLE IF NOT EXISTS cryptocurrency (
               timestamp BIGINT PRIMARY KEY,
               open FLOAT,
               highest FLOAT,
               lowest FLOAT,
               closing FLOAT,
               volume FLOAT
           )
       """,
   )
   ```

6. ในข้อนี้เราจะ merge ข้อมูลจาก table ที่เราใช้พักข้อมูลไว้ เข้ามาที่ table ที่เราจะใช้วิเคราะห์จริงๆ โดยใช้ `PostgresOperator` ในการรัน SQL เช่นกัน ตรงนี้มีสิ่งที่เราต้องคิดถึงก็คือเรื่อง idempotent ซึ่งหมายความว่าในตอนที่เรา merge ข้อมูลเข้าไปแล้ว จะไม่เกิดข้อมูลซ้ำขึ้นใน table ที่เราจะนำไปวิเคราะห์ ดังนั้นใน SQL เราจะต้องมีการตรวจสอบข้อมูลซ้ำด้วย ใน Postgres เราจะใช้ `ON CONFLICT ... DO` และถ้าเจอข้อมูลซ้ำเราจะอัพเดททับข้อมูลเก่าโดยใช้คำสั่ง `UPDATE`

   ```py
   merge_import_into_final_table = PostgresOperator(
       task_id="merge_import_into_final_table",
       postgres_conn_id="postgres",
       sql="""
           INSERT INTO cryptocurrency (
               timestamp,
               open,
               highest,
               lowest,
               closing,
               volume
           )
           SELECT
               timestamp,
               open,
               highest,
               lowest,
               closing,
               volume
           FROM
               cryptocurrency_import
           ON CONFLICT (timestamp)
           DO UPDATE SET
               open = EXCLUDED.open,
               highest = EXCLUDED.highest,
               lowest = EXCLUDED.lowest,
               closing = EXCLUDED.closing,
               volume = EXCLUDED.volume
       """,
   )
   ```

7. หลังจากที่เรา merge ข้อมูลไปแล้ว เราอาจจะไม่มีความจำเป็นที่จะต้องเก็บข้อมูลใน table ที่เราใช้พักข้อมูล เราสามารถลบข้อมูลออกได้

   ```py
   clear_import_table = PostgresOperator(
       task_id="clear_import_table",
       postgres_conn_id="postgres",
       sql="""
           DELETE FROM cryptocurrency_import
       """,
   )
   ```

8. หลังจากที่ data pipeline ของเราทำงานเสร็จ ก็ควรที่จะต้องมี notification อย่างเช่น ส่งอีเมลแจ้งเราด้วย ในทีนี้เราสามารถใช้ `EmailOperator` ได้

   ```py
   notify = EmailOperator(
       task_id="notify",
       to=["kan@dataengineercafe.io"],
       subject="Loaded data into database successfully on {{ ds }}",
       html_content="Your pipeline has loaded data into database successfully",
   )
   ```

9. ลำดับของงานต่างๆ หรือ task dependencies สุดท้ายควรจะมีหน้าตาประมาณนี้

   ```py
   fetch_ohlcv >> download_file >> create_import_table >> load_data_into_database >> create_final_table >> merge_import_into_final_table >> clear_import_table >> notify
   ```

10. สุดท้ายเพื่อให้ data pipeline ของเรารันตาม schedule ที่เราต้องการ คือ ดึงข้อมูลรายวัน และถ้ามี failure อะไรเกิดขึ้น เราก็ต้องการที่จะให้ Airflow แจ้งผ่านอีเมลเรามา ตรงนี้เราสามารถตั้งค่า `email` ใน `default_args` ได้ และในกรณีที่ CCXT API เกิด unavailable ในช่วงที่เราดึงข้อมูล เราก็อยากที่จะให้เกิดการ retry ขึ้นด้วย เราก็สามารถตั้งแค่ `retries` และ `retry_delay` ใน `default_args` ได้เช่นกัน

    ```py
    default_args = {
        "owner": "zkan",
        "email": ["kan@dataengineercafe.io"],
        "start_date": timezone.datetime(2022, 2, 1),
        "retries": 3,
        "retry_delay": timedelta(minutes=3),
    }
    ```
