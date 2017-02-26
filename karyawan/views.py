from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from karyawan.models import Karyawan
# Create your views here.

@login_required(login_url=settings.LOGIN_URL)
def profil(request):
    # dapat diartikan sebagai "SELECT * FROM karyawan WHERE id='10'"
    karyawan = Karyawan.objects.get(id=request.session['karyawan_id'])
    # Setelah mengambil data karyawan yang terkait dengan akun yang berhasil login, kita melakukan rendering template profil.html dengan melewatkan data karyawan ke dalam template tersebut.
    return render(request, 'new/profil.html', {'karyawan':karyawan})

@login_required(login_url=settings.LOGIN_URL)
def ganti_foto(request):
    karyawan = Karyawan.objects.get(id=request.session['karyawan_id'])
    karyawan.foto = request.FILES['files']
    karyawan.save()

    return redirect('/')


