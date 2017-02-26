from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages

from karyawan.models import Akun, Karyawan

# Create your views here.
def login_view(request):
    # proses pengecekan apakah request yang datang adalah POST atau bukan. Bila bukan POST maka akan ditampilkan langsung halaman login yang berisi form login.
    if request.POST:
        # request.POST utk mendapat input POST form seperti $_GET[] nya php
        # Secara teknis, authenticate akan memeriksa identitas yang dikirimkan dari form login untuk diperiksa keberadaannya di tabel User.
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        # Bila POST maka akan masuk ke proses selanjutnya yaitu proses autentikasi user.
        if user is not None:
            # Bila user terdaftar maka akan masuk ke proses berikutnya yaitu pengecekan apakah user merupakan user aktif atau bukan.
            if user.is_active:
                try:
                    akun = Akun.objects.get(akun=user.id)
                    login(request, user)

                    # bila user sudah aktif maka akan terjadi proses pencatatan session dengan mengambil data Karyawan yang terhubung ke akun yang akan diakses.
                    request.session['karyawan_id'] = akun.karyawan.id
                    request.session['jenis_akun'] = akun.jenis_akun
                    request.session['username'] = request.POST['username']
                except:
                    messages.add_message(request, messages.INFO, 'Akun ini belum terhubung dengan data karyawan, silahkan hubungi administrator')
                return redirect('/')

            # Bila user belum diaktifkan maka akan tampil halaman login dengan pesan "User belum terverifikasi"
            else:
                messages.add_message(request, messages.INFO, 'User belum terverifikasi')

        # Jika user tidak terdaftar maka akan akan ditampilkan halaman login dengan pesan "Username atau password Anda salah".
        else:
            messages.add_message(request, messages.INFO, "Username atau password anda salah")

    return render(request, 'new/login.html')

# kita hanya melakukan pembersihan request dari session dan menghilangkan objek user yang sudah tercatat sewaktu login.
def logout_view(request):
    logout(request)
    # sebelum masuk ke inti, masuk dahulu ke url login
    return redirect('/login/')