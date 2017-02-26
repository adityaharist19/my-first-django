from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from karyawan.models import Karyawan
from kehadiran.models import Kehadiran, Izin
from kehadiran.forms import IzinForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors

import json, time

# Create your views here.

# harus login dahulu sebelum menampilkan daftar kehadiran
@login_required(login_url=settings.LOGIN_URL)
def daftar_hadir(request):
    daftar_hadir = None

    # tambahin ini agar tidak error pada render, karena pada render dia perlu variabel bulan & tahun,yang akan tambil adalah januari dan tahun terawal yg teregistrasi
    bulan = 0
    tahun = 0

    # cek requestnya POST, akan proses query utk ambil data kehadiran karyawan bulan & tahun tertentu, ini jika form submit diklik;karena table akan memanggil tiap data maka views juga akan dipanggil satu-persatu
    if request.method == 'POST':
       bulan = request.POST['bulan']
       tahun = request.POST['tahun']
       daftar_hadir = Kehadiran.objects.filter(waktu__year=tahun, waktu__month=bulan, karyawan__id=request.session['karyawan_id'])

    return render(request, 'new/daftar_hadir.html', {'daftar_hadir':daftar_hadir, 'bulan':bulan, 'tahun':tahun})


@login_required(login_url=settings.LOGIN_URL)
def pengajuan_izin(request):
    if request.method == 'POST':
        # Jika yang datang adalah request berupa POST, maka data POST akan dikumpulkan
        # ke variabel form_data kemudian diperiksa oleh IzinForm untuk dicari validitasnya,
        form_data = request.POST
        form = IzinForm(form_data)

        # jika nilai - nilai yang dimasukkan valid, maka proses selanjutnya
        # yang akan dilakukan yaitu penyimpanan data pengajuan izin kerja.
        if form.is_valid():
            izin = Izin(
                    karyawan = Karyawan.objects.get(id=request.session['karyawan_id']),
                    jenis_kehadiran = request.POST['jenis_kehadiran'],
                    waktu_mulai = request.POST['waktu_mulai'],
                    waktu_berhenti = request.POST['waktu_berhenti'],
                    alasan = request.POST['alasan'],
                    disetujui = False,
                )
            # Kita membuat sebuah instance baru dari model Izin yang dilewatkan beberapa nilai dari form yang
            # dikirimkan (izin), kemudian kita simpan (save), dan melakukan redirect ke halaman root (return).
            izin.save()
            return redirect('/')

    # Ketika yang datang adalah request berupa GET, maka Anda akan dibuatkan
    # IzinForm kosong dan menampilkannya di template tambah_izin.html
    else:
        form = IzinForm()

    return render(request, 'new/tambah_izin.html', {'form':form})


@login_required(login_url=settings.LOGIN_URL)
def daftar_izin(request):
    daftar_izin = Izin.objects.filter(karyawan__id=request.session['karyawan_id'])

    paginator = Paginator(daftar_izin, 5)
    page = request.GET.get('page')
    try:
        daftar_izin = paginator.page(page)
    except PageNotAnInteger:
        daftar_izin = paginator.page(1)
    except EmptyPage:
        daftar_izin = paginator.page(paginator.num_pages)

    return render(request, 'new/daftar_izin.html', {'daftar_izin':daftar_izin})


@login_required(login_url=settings.LOGIN_URL)
def tampil_grafik(request, bulan, tahun):
    temp_chart_data = []
    # ambil data daftar_hadir dari karyawan
    daftar_hadir = Kehadiran.objects.filter(waktu__year=tahun, waktu__month=bulan, karyawan__id=request.session['karyawan_id'])

    temp_chart_data.append({ "x":"hadir", "a":daftar_hadir.filter(jenis_kehadiran='hadir').count() })
    temp_chart_data.append({ "x":"izin", "a":daftar_hadir.filter(jenis_kehadiran='izin').count() })
    temp_chart_data.append({ "x":"alpa", "a":daftar_hadir.filter(jenis_kehadiran='alpa').count() })
    temp_chart_data.append({ "x":"cuti", "a":daftar_hadir.filter(jenis_kehadiran='cuti').count() })

    chart_data = json.dumps({"data":temp_chart_data})

    return render(request, 'new/tampil_grafik.html', {'chart_data':chart_data, 'bulan':bulan, 'tahun':tahun})


@login_required(login_url=settings.LOGIN_URL)
def cetak_daftar_hadir(request, bulan, tahun):
    # pengaturan respon berformat pdf
    filename = "daftar_hadir_" + str(bulan) + "_" + str(tahun)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.pdf"'

    # isi data tabel
    data = Kehadiran.objects.filter(waktu__year=tahun, waktu__month=bulan, karyawan__id=request.session['karyawan_id'])
    table_data = []
    table_data.append([ "Tanggal","Status" ])
    for x in data:
        table_data.append([ x.waktu, x.jenis_kehadiran])


    # termasuk dg, cara format pdf dicetak, dari ukuran halaman pdf, margin
    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()

    # khusus utk format penyajian tabel agar rapi
    table_style = TableStyle([
        ('ALIGN',(1,1),(-2,-2),'RIGHT'),
        ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
        ('VALIGN',(0,0),(0,-1),'TOP'),
        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
        ('BOX',(0,0),(-1,-1), 0.25, colors.black),
    ])
    kehadiran_table = Table(table_data, colWidths=[doc.width/4.0]*2)
    kehadiran_table.setStyle(table_style)

    # format file yang dicetak
    content = []
    content.append(Paragraph('Daftar Kehadiran %s/%s' % (bulan, tahun), styles['Title']))
    content.append(Spacer(1,12))
    content.append(Paragraph('Berikut ini adalah hasil rekam jejak kehadiran Anda selama bulan %s tahun %s:' % (bulan, tahun), styles['Normal']))
    content.append(Spacer(1,12))
    content.append(kehadiran_table)
    content.append(Spacer(1,36))
    content.append(Paragraph('Mengetahui, ', styles['Normal']))
    content.append(Spacer(1,48))
    content.append(Paragraph('Annasikhatussalavi, Head of Department PT. Impian Sejahtera.', styles['Normal']))

    doc.build(content)
    return response

