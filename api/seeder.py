from api.models import User, Disease, Scan, Bookmark
import time

# Create Users
user1 = User.objects.create(username='john_doe', email='john@example.com', password='password123')
user2 = User.objects.create(username='jane_doe', email='jane@example.com', password='password123')

# Buat Penyakit
disease1 = Disease.objects.create(name='Healthy', desc='Kondisi tanaman yang normal dan sehat')
disease2 = Disease.objects.create(name='Sooty Mould', desc='Infeksi jamur yang menyebabkan jamur hitam pada daun')
disease3 = Disease.objects.create(name='Anthracnose', desc='Penyakit jamur yang menyebabkan lesi gelap pada jaringan tanaman')
disease4 = Disease.objects.create(name='Bacterial Canker', desc='Infeksi bakteri yang menyebabkan luka terbuka pada tanaman')
disease5 = Disease.objects.create(name='Cutting Weevil', desc='Infestasi serangga yang merusak jaringan tanaman')
disease6 = Disease.objects.create(name='Die Back', desc='Kematian bertahap cabang tanaman dari ujung ke bawah')
disease7 = Disease.objects.create(name='Gall Midge', desc='Larva serangga yang menyebabkan pembengkakan atau pertumbuhan abnormal pada tanaman')
disease8 = Disease.objects.create(name='Powdery Mildew', desc='Infeksi jamur yang menyebabkan lapisan putih seperti tepung pada permukaan tanaman')

# Buat Pemindaian
scan1 = Scan.objects.create(user=user1, datetime=int(time.time()), img='path_to_image_1.jpg', diagnosis=disease1, accuracy=99.0, desc='Tidak ada tanda-tanda penyakit')
scan2 = Scan.objects.create(user=user2, datetime=int(time.time()), img='path_to_image_2.jpg', diagnosis=disease2, accuracy=90.5, desc='Jamur hitam terlihat jelas')
scan3 = Scan.objects.create(user=user1, datetime=int(time.time()), img='path_to_image_3.jpg', diagnosis=disease3, accuracy=85.2, desc='Bercak gelap pada daun')
scan4 = Scan.objects.create(user=user1, datetime=int(time.time()), img='path_to_image_4.jpg', diagnosis=disease4, accuracy=88.0, desc='Luka terbuka pada batang')
scan5 = Scan.objects.create(user=user1, datetime=int(time.time()), img='path_to_image_5.jpg', diagnosis=disease5, accuracy=92.4, desc='Gigitan serangga pada daun')
scan6 = Scan.objects.create(user=user2, datetime=int(time.time()), img='path_to_image_6.jpg', diagnosis=disease6, accuracy=87.6, desc='Cabang yang mati')
scan7 = Scan.objects.create(user=user2, datetime=int(time.time()), img='path_to_image_7.jpg', diagnosis=disease7, accuracy=91.8, desc='Pembengkakan pada cabang tanaman')
scan8 = Scan.objects.create(user=user2, datetime=int(time.time()), img='path_to_image_8.jpg', diagnosis=disease8, accuracy=93.5, desc='Lapisan putih seperti tepung pada daun')

# Buat Bookmark
bookmark1 = Bookmark.objects.create(user=user1, disease=disease1, date=int(time.time()), status=True)
bookmark2 = Bookmark.objects.create(user=user2, disease=disease2, date=int(time.time()), status=False)
bookmark3 = Bookmark.objects.create(user=user1, disease=disease3, date=int(time.time()), status=True)
bookmark4 = Bookmark.objects.create(user=user1, disease=disease4, date=int(time.time()), status=False)
bookmark5 = Bookmark.objects.create(user=user1, disease=disease5, date=int(time.time()), status=True)
bookmark6 = Bookmark.objects.create(user=user2, disease=disease6, date=int(time.time()), status=False)
bookmark7 = Bookmark.objects.create(user=user2, disease=disease7, date=int(time.time()), status=True)
bookmark8 = Bookmark.objects.create(user=user2, disease=disease8, date=int(time.time()), status=False)

print("Seeding selesai!")