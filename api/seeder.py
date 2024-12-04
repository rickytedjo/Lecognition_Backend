from api.models import User, Disease, Scan, Bookmark
import time

disease1 = Disease.objects.create(name='Healthy', desc='Kondisi tanaman yang normal dan sehat')
disease2 = Disease.objects.create(name='Sooty Mould', desc='Infeksi jamur yang menyebabkan jamur hitam pada daun')
disease3 = Disease.objects.create(name='Anthracnose', desc='Penyakit jamur yang menyebabkan lesi gelap pada jaringan tanaman')
disease4 = Disease.objects.create(name='Bacterial Canker', desc='Infeksi bakteri yang menyebabkan luka terbuka pada tanaman')
disease5 = Disease.objects.create(name='Cutting Weevil', desc='Infestasi serangga yang merusak jaringan tanaman')
disease6 = Disease.objects.create(name='Die Back', desc='Kematian bertahap cabang tanaman dari ujung ke bawah')
disease7 = Disease.objects.create(name='Gall Midge', desc='Larva serangga yang menyebabkan pembengkakan atau pertumbuhan abnormal pada tanaman')
disease8 = Disease.objects.create(name='Powdery Mildew', desc='Infeksi jamur yang menyebabkan lapisan putih seperti tepung pada permukaan tanaman')

print("Seeding selesai!")