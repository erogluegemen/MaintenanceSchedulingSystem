import sqlite3
from datetime import datetime


def insert_sample_data():
    conn = sqlite3.connect('maintenance.db')
    cursor = conn.cursor()

    # Türkçe Makine Verileri
    machines = [
        ('Torna Tezgahı', 'Atölye A', 'Ağır Makine', 'Çalışıyor'),
        ('Kaynak Makinesi', 'Atölye B', 'Üretim', 'Bakım Gerekli'),
        ('Pres Makinesi', 'Atölye C', 'Montaj Hattı', 'Çevrim Dışı'),
        ('CNC Makinesi', 'Atölye D', 'Hassas Araçlar', 'Çalışıyor')
    ]

    cursor.executemany('''
    INSERT INTO machines (name, location, type, status)
    VALUES (?, ?, ?, ?)
    ''', machines)

    # Türkçe Bakım Görevleri
    tasks = [
        (1, 'Denetim', '2024-12-10 10:00:00', 'Ahmet Yılmaz', 'Planlandı'),
        (2, 'Onarım', '2024-12-12 15:00:00', 'Fatma Demir', 'Bekliyor'),
        (3, 'Kalibrasyon', '2024-12-15 09:00:00', 'Mehmet Kaya', 'Planlandı')
    ]

    cursor.executemany('''
    INSERT INTO maintenance_tasks (machine_id, maintenance_type, date_scheduled, technician_name, status)
    VALUES (?, ?, ?, ?, ?)
    ''', tasks)

    # Türkçe Bakım Geçmişi
    history = [
        (1, '2024-12-05 14:00:00', 'Rutin Denetim Tamamlandı.'),
        (2, '2024-12-06 12:00:00', 'Parça bulunamadığı için onarım gecikti.')
    ]

    cursor.executemany('''
    INSERT INTO maintenance_history (task_id, completion_date, remarks)
    VALUES (?, ?, ?)
    ''', history)

    conn.commit()
    conn.close()

    print("Örnek veriler başarıyla eklendi!")

if __name__ == '__main__':
    insert_sample_data()
