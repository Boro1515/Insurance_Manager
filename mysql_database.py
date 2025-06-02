# mysql.database.py
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

def get_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

def get_all_insured():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, jmeno, prijmeni, vek, telefon FROM pojisteni")
    results = cursor.fetchall()
    conn.close()
    return results

def add_insured(jmeno, prijmeni, vek, telefon):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pojisteni (jmeno, prijmeni, vek, telefon) VALUES (%s, %s, %s, %s)",
                   (jmeno, prijmeni, vek, telefon))
    conn.commit()
    conn.close()

def delete_insured(insured_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pojisteni WHERE id = %s", (insured_id,))
    conn.commit()
    conn.close()

def update_insured(insured_id, jmeno, prijmeni, vek, telefon):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pojisteni
        SET jmeno = %s, prijmeni = %s, vek = %s, telefon = %s
        WHERE id = %s
    """, (jmeno, prijmeni, vek, telefon, insured_id))
    conn.commit()
    conn.close()

def get_insured_by_id(insured_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pojisteni WHERE id = %s", (insured_id,))
    result = cursor.fetchone()
    conn.close()
    return result
