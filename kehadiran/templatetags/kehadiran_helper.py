# file ini hanya menambah nilai pada halaman pagination agar indexnya masih nyambung dengan yang sebelumnya

# kita memanggil modul template dari Django,
from django import template

# kemudian membuat sebuah variabel yang berisi sebuah objek template.Library()
register = template.Library()

ROW_PER_PAGE = 5

# Kemudian kita panggil decorator @register.filter untuk menandai function get_table_number sebagai function yang dapat dipanggil di suatu template.
@register.filter
# Di dalam function tersebut terdapat sebuah rumus yang akan menghitung penomoran di setiap halaman yang telah di beri pagination.
def get_table_number(value, arg):
    # Parameter value adalah baris data yang akan diproses, kemudian arg adalah halaman dimana Anda berada saat ini.
    return value + ( (arg-1) * ROW_PER_PAGE)
