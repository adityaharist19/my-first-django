from django.forms import ModelForm
from django import forms
from kehadiran.models import Izin

# Kita akan mencoba bagaimana django dapat mempermudah kita membuat sebuah form yang sesuai dengan
# model yang kita definisikan plus dengan validasi yang tidak perlu kita tangani terlalu banyak.
# Yap, dengan ModelAdmin, Anda dapat menggunakan form yang sama persi di halaman admin Django untuk ditampilkan di halaman HTML yang Anda buat.

class IzinForm(ModelForm):
    # Kita harus menggunakan class Meta untuk mulai mendefinisikan ModelForm.
    class Meta:
        model = Izin
        fields = ['jenis_kehadiran', 'waktu_mulai', 'waktu_berhenti', 'alasan']
        # exclude = ['disetujui']
        # kita memperbaharui labels setiap field yang akan ditampilkan menjadi bahasa Indonesia.
        labels = {
            'jenis_kehadiran': "Jenis Izin",
            'waktu_mulai': 'Waktu Mulai Izin',
            'waktu_berhenti': 'Waktu Berhenti Izin',
            'alasan': 'Alasan Izin',
        }
        # Kemudian kita ubah juga pesan error yang akan dimunculkan ketika user salah memberikan masukan pada form.
        error_messages = {
            'jenis_kehadiran': {
                'required': 'Anda harus memilih jenis izin'
            },
            'waktu_mulai': {
                'required': "Anda harus menentukan tanggal izin dimulai"
            },
            'waktu_berhenti': {
                'required': "Anda harus menentukan tanggal izin berakhir"
            },
            'alasan': {
                'required': "Alasan harus diisi agar dapat disetujui oleh HRD"
            }
        }
        # Dan khusus untuk field "alasan", kita harus mengubah jenis tampilan field-nya menjadi TextArea ketimbang TextInput.
        widgets = {
            # 'alasan': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
            'alasan': forms.Textarea(attrs={'class':'form-control'}),
            'jenis_kehadiran': forms.Select(attrs={'class':'form-control'}),
            'waktu_mulai': forms.TextInput(attrs={'class':'form-control'}),
            'waktu_berhenti': forms.TextInput(attrs={'class':'form-control'}),
        }