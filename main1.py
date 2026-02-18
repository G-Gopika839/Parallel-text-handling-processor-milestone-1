import sqlite3

with open("sample.txt", "w") as f:
    for i in range(1, 1001):
        f.write(f"This is line number {i}\n")

with open("sample.txt", "r") as f:
    lines = f.readlines()

chunks = [lines[i:i+100] for i in range(0, len(lines), 100)]

for index, chunk in enumerate(chunks):
    with open(f"chunk_{index+1}.txt", "w") as cf:
        cf.writelines(chunk)

conn = sqlite3.connect("results.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS wordcount (
    chunk_name TEXT,
    word_count INTEGER
)
""")

for index in range(10):
    with open(f"chunk_{index+1}.txt", "r") as cf:
        text = cf.read()
        count = len(text.split())
        cursor.execute("INSERT INTO wordcount VALUES (?, ?)",
                       (f"chunk_{index+1}", count))

conn.commit()
conn.close()


