import mysql.connector
from prettytable import PrettyTable

# Pewarna
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pendidikan_bermutu"
)
mycursor = mydb.cursor()

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def tampilan_admin(self):
        current = self.head
        x = PrettyTable()
        x.field_names = ["id_admin", "username", "password", "nim", "email"]
        while current:
            x.add_row(current.data)
            current = current.next
        print(x)

    def tampilan_beasiswa(self):
        current = self.head
        x = PrettyTable()
        x.field_names = ["id_beasiswa", "kategori_beasiswa", "nama_beasiswa"]
        while current:
            x.add_row(current.data)
            current = current.next
        print(x)
    
    def tampilan_mahasiswa(self):
        current = self.head
        x = PrettyTable()
        x.field_names = ["nim", "nama", "alamat", "tanggal_lahir", "email","id_universitas","id_beasiswa","nomor_hp"]
        while current:
            x.add_row(current.data)
            current = current.next
        print(x)

    def tampilan_pemerintah(self):
        current = self.head
        x = PrettyTable()
        x.field_names = ["id_pemerintah", "nama_pemerintah", "id_beasiswa"]
        while current:
            x.add_row(current.data)
            current = current.next
        print(x)

    def tampilan_universitas(self):
        current = self.head
        x = PrettyTable()
        x.field_names = ["id_universitas", "nama_universitas", "nama_fakultas", "nama_prodi", "alamat_universitas"]
        while current:
            x.add_row(current.data)
            current = current.next
        print(x)
        
def sorting_cepat(arr, ascending=True):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2][0]
    left = [x for x in arr if x[0] < pivot]
    middle = [x for x in arr if x[0] == pivot]
    right = [x for x in arr if x[0] > pivot]
    if ascending:
        return sorting_cepat(left, ascending) + middle + sorting_cepat(right, ascending)
    else:
        return sorting_cepat(right, ascending) + middle + sorting_cepat(left, ascending)

def jump_search(arr, x):
    n = len(arr)
    step = int(n ** 0.5)
    prev = 0
    while arr[min(step, n)-1][0] < x:
        prev = step
        step += int(n ** 0.5)
        if prev >= n:
            return -1
    while arr[prev][0] < x:
        prev += 1
        if prev == min(step, n):
            return -1
    if arr[prev][0] == x:
        return prev
    return -1

def data_admin():
    mycursor.execute("SELECT * FROM admin")
    myresult = mycursor.fetchall()
    ll = LinkedList()
    for data in myresult:
        ll.append(data)
    ll.tampilan_admin()

def tambah_data_admin():
    id_admin = int(input("MASUKKAN ID admin : "))
    username = input("MASUKKAN USERNAME ADMIN : ")
    password = input("MASUKKAN PASSWORD ADMIN : ")
    nim = input("MASUKKAN NIM ADMIN : ")
    email = input("MASUKKAN EMAIL ADMIN : ")
    query = f"""
    INSERT INTO admin (id_admin, username, password, nim, email)
    VALUES ({id_admin}, '{username}', '{password.replace("'", "''")}', '{nim}', '{email}')
    """

    mycursor.execute(query)
    mydb.commit()
    print("DATA ADMIN BERHASIL DITAMBAHKAN!")

def hapus_data_admin():
    data_admin()
    id_admin = int(input("MASUKKAN ID ADMIN YANG INGIN DIHAPUS : "))

    query = f"DELETE FROM admin WHERE id_admin = {id_admin}"

    mycursor.execute(query)
    mydb.commit()
    print("DATA ADMIN BERHASIL DIHAPUS !")

def perbarui_data_admin():
    data_admin()
    id_admin = int(input("MASUKKAN ID ADMIN YANG INGIN DIPERBARUI : "))
    username = input("MASUKKAN USERNAME ADMIN BARU : ")
    password = input("MASUKKAN PASSWORD ADMIN BARU : ")
    nim = input("MASUKKAN NIM ADMIN BARU : ")
    email = input("MASUKKAN EMAIL ADMIN BARU : ")
    query = f"""
    UPDATE admin
    SET username = %s, password = %s, nim = %s, email = %s
    WHERE id_admin = %s
    """

    val = (username, password, nim, email, id_admin)
    mycursor.execute(query, val)
    mydb.commit()
    print("DATA ADMIN BERHASIL DIPERBARUI!")

def data_beasiswa():
    mycursor.execute("SELECT * FROM beasiswa")
    myresult = mycursor.fetchall()
    data_list = []
    for data in myresult:
        data_list.append(data)

    while True:
        print("")
        print("                  TAMPILKAN DATA BEASISWA                ")
        print("")
        print("   1. URUTKAN DATA BERDASARKAN ID - ASCENDING             ")
        print("   2. URUTKAN DATA BERDASARKAN ID - DESCENDING            ")
        print("   3. CARI DATA BERDASARKAN ID                            ")
        print("   4. KEMBALI KE MENU DATABASE BEASISWA                   ")
        print("")

        pilihan = input("MASUKKAN PILIHAN ANDA : ")

        if pilihan == "1":
            sorted_data = sorting_cepat(data_list, ascending=True)
            ll = LinkedList()
            for data in sorted_data:
                ll.append(data)
            ll.tampilan_beasiswa()
        elif pilihan == "2":
            sorted_data = sorting_cepat(data_list, ascending=False)
            ll = LinkedList()
            for data in sorted_data:
                ll.append(data)
            ll.tampilan_beasiswa()
        elif pilihan == "3":
            id_to_search = int(input("MASUKKAN ID YANG INGIN DICARI : "))
            result_index = jump_search(data_list, id_to_search)
            if result_index != -1:
                print("DATA DITEMUKAN :")
                x = PrettyTable()
                x.field_names = ["id_beasiswa", "nama_beasiswa", "kategori_beasiswa"]
                x.add_row(data_list[result_index])
                print(x)
            else:
                print("DATA TIDAK DITEMUKAN")
        elif pilihan == "4":
            break
        else:
            print("PILIHAN TIDAK VALID !")
            
def tambah_data_beasiswa():
    id_beasiswa = int(input("MASUKKAN ID BEASISWA : "))
    nama_beasiswa = input("MASUKKAN NAMA BEASISWA : ")
    kategori_beasiswa = input("MASUKKAN KATEGORI BEASISWA : ")
    query = f"""
    INSERT INTO beasiswa (id_beasiswa, nama_beasiswa, kategori_beasiswa)
    VALUES ({id_beasiswa}, '{nama_beasiswa}', '{kategori_beasiswa}')
    """

    mycursor.execute(query)
    mydb.commit()
    print("DATA BERHASIL DITAMBAHKAN")

def hapus_data_beasiswa():
    mycursor.execute("SELECT * FROM beasiswa")
    myresult = mycursor.fetchall()
    x = PrettyTable()
    x.field_names = ["id_beasiswa", "nama_beasiswa", "kategori_beasiswa"]
    for data in myresult:
        x.add_row(data)
    print(x)

    id_beasiswa = int(input("MASUKKAN ID BEASISWA YANG INGIN DIHAPUS : "))

    query = f"DELETE FROM beasiswa WHERE id_beasiswa = {id_beasiswa}"

    mycursor.execute(query)
    mydb.commit()
    print("DATA BERHASIL DIHAPUS !")

def perbarui_data_beasiswa():
    mycursor.execute("SELECT * FROM beasiswa")
    myresult = mycursor.fetchall()
    x = PrettyTable()
    x.field_names = ["id_beasiswa", "nama_beasiswa", "kategori_beasiswa"]
    for data in myresult:
        x.add_row(data)
    print(x)

    id_beasiswa = int(input("MASUKKAN ID BEASISWA YANG INGIN DIPERBARUI : "))
    kategori_beasiswa = input("MASUKKAN KATEGORI BEASISWA BARU : ")
    nama_beasiswa = input("MASUKKAN NAMA BEASISWA BARU : ")
    query = f"""
    UPDATE beasiswa
    SET nama_beasiswa = %s, kategori_beasiswa = %s
    WHERE id_beasiswa = %s
    """

    val = (nama_beasiswa, kategori_beasiswa, id_beasiswa)
    mycursor.execute(query, val)
    mydb.commit()
    print("DATA BERHASIL DIPERBARUI!")

def data_mahasiswa():
    mycursor.execute("SELECT * FROM mahasiswa")
    myresult = mycursor.fetchall()
    data_list = []
    for data in myresult:
        data_list.append(data)

    while True:
        print("")
        print("                  TAMPILKAN DATA mahasiswa               ")
        print("")
        print("   1. URUTKAN DATA BERDASARKAN ID - ASCENDING            ")
        print("   2. URUTKAN DATA BERDASARKAN ID - DESCENDING            ")
        print("   3. CARI DATA BERDASARKAN ID                            ")
        print("   4. KEMBALI                  ")
        print("")

        pilihan = input("MASUKKAN PILIHAN ANDA : ")

        if pilihan == "1":
            sorted_data = sorting_cepat(data_list, ascending=True)
            ll = LinkedList()
            for data in sorted_data:
                ll.append(data)
            ll.tampilan_mahasiswa()
        elif pilihan == "2":
            sorted_data = sorting_cepat(data_list, ascending=False)
            ll = LinkedList()
            for data in sorted_data:
                ll.append(data)
            ll.tampilan_mahasiswa()
        elif pilihan == "3":
            id_to_search = int(input("MASUKKAN ID YANG INGIN DICARI : "))
            result_index = jump_search(data_list, id_to_search)
            if result_index != -1:
                print("DATA DATABASE DITEMUKAN :")
                x = PrettyTable()
                x.field_names = ["nim", "nama", "alamat", "tanggal_lahir", "email", "id_universitas", "id_beasiswa", "nomor_hp"]
                x.add_row(data_list[result_index])
                print(x)
            else:
                print("DATA DATABASE TIDAK DITEMUKAN")
        elif pilihan == "4":
            break
        else:
            print("COBA LAGI !")

def tambah_data_mahasiswa():
    nim = int(input("MASUKKAN ID mahasiswa : "))
    nama = input("MASUKAN NAMA mahasiswa BARU : ")
    alamat = input("MASUKAN alamat BARU : ")
    tanggal_lahir = input("MASUKAN tanggal lahir BARU : ")
    email = input("MASUKAN email BARU : ")
    id_universitas = int(input("masukkan id universitas yang sudah ada :"))
    id_beasiswa = int(input("masukkan id beasiswa yang sudah ada :"))
    nomor_hp = input(" masukkan nomor hp baru :")

    # Check if the id_universitas value exists in the universitas table
    mycursor.execute("SELECT COUNT(*) FROM universitas WHERE id_universitas = %s", (id_universitas,))
    if mycursor.fetchone()[0] == 0:
        print("id universitas tidak ada di tabel beasiswa")
        return

    # Check if the id_beasiswa value exists in the beasiswa table
    mycursor.execute("SELECT COUNT(*) FROM beasiswa WHERE id_beasiswa = %s", (id_beasiswa,))
    if mycursor.fetchone()[0] == 0:
        print("id beasiswa tidak di ada tabel beasiswa")
        return

    query = f"""
    INSERT INTO mahasiswa (nim, nama, alamat, tanggal_lahir, email, id_universitas, id_beasiswa, nomor_hp)
    VALUES ({nim}, '{nama}', '{alamat}', '{tanggal_lahir}', '{email}', {id_universitas}, {id_beasiswa}, '{nomor_hp}')
    """

    mycursor.execute(query)
    mydb.commit()
    print("DATA DATABASE BERHASIL DITAMBAHKAN")

def hapus_data_mahasiswa():
    mycursor.execute("SELECT * FROM mahasiswa")
    myresult = mycursor.fetchall()
    x = PrettyTable()
    x.field_names = ["nim", "nama", "alamat", "tanggal_lahir", "email", "id_universitas", "id_beasiswa", "nomor_hp"]
    for data in myresult:
        x.add_row(data)
    print(x)

    nim = int(input("MASUKKAN ID mahasiswa YANG INGIN DIHAPUS : "))

    query = f"DELETE FROM mahasiswa WHERE nim = {nim}"

    mycursor.execute(query)
    mydb.commit()
    print("DATA DATABASE BERHASIL DIHAPUS !")

def perbarui_data_mahasiswa():
    mycursor.execute("SELECT * FROM mahasiswa")
    myresult = mycursor.fetchall()
    x = PrettyTable()
    x.field_names = ["nim", "nama", "alamat", "tanggal_lahir", "email", "id_universitas", "id_beasiswa", "nomor_hp"]
    for data in myresult:
        x.add_row(data)
    print(x)

    nim = int(input("MASUKKAN NIM mahasiswa YANG INGIN DIPERBARUI : "))
    nama = input("MASUKAN NAMA mahasiswa BARU : ")
    alamat = input("MASUKAN alamat BARU : ")
    tanggal_lahir = input("MASUKAN tanggal lahir BARU : ")
    email = input("MASUKAN email BARU : ")
    id_universitas = int(input("masukkan id universitas yang sudah ada :"))
    id_beasiswa = int(input("masukkan id beasiswa yang sudah ada :"))

    # Check if the id_universitas value exists in the universitas table
    mycursor.execute("SELECT COUNT(*) FROM universitas WHERE id_universitas = %s", (id_universitas,))
    if mycursor.fetchone()[0] == 0:
        print("The id_universitas value does not exist in the universitas table.")
        return

    # Check if the id_beasiswa value exists in the beasiswa table
    mycursor.execute("SELECT COUNT(*) FROM beasiswa WHERE id_beasiswa = %s", (id_beasiswa,))
    if mycursor.fetchone()[0] == 0:
        print("The id_beasiswa value does not exist in the beasiswa table.")
        return

    query = f"""
    UPDATE mahasiswa
    SET nama = %s, alamat = %s, tanggal_lahir = %s, email = %s, id_universitas = %s, id_beasiswa = %s
    WHERE nim = %s
    """

    val = (nama, alamat, tanggal_lahir, email, id_universitas, id_beasiswa, nim)
    mycursor.execute(query, val)
    mydb.commit()
    print("DATA BERHASIL DIPERBARUI!")

def data_pemerintah():
    mycursor.execute("SELECT * FROM pemerintah")
    myresult = mycursor.fetchall()
    data_list = []
    for data in myresult:
        data_list.append(data)

    while True:
        print("")
        print("                  TAMPILKAN DATA pemerintah               ")
        print("")
        print("   1. URUTKAN DATA BERDASARKAN ID - ASCENDING             ")
        print("   2. URUTKAN DATA BERDASARKAN ID - DESCENDING            ")
        print("   3. CARI DATA BERDASARKAN ID                            ")
        print("   4. KEMBALI                     ")
        print("")
        pilihan = input("MASUKKAN PILIHAN ANDA : ")

        if pilihan == "1":
            sorted_data = sorting_cepat(data_list, ascending=True)
            ll = LinkedList()
            for data in sorted_data:
                ll.append(data)
            ll.tampilan_pemerintah()
        elif pilihan == "2":
            sorted_data = sorting_cepat(data_list, ascending=False)
            ll = LinkedList()
            for data in sorted_data:
                ll.append(data)
            ll.tampilan_pemerintah()
        elif pilihan == "3":
            id_to_search = int(input("MASUKKAN ID YANG DICARI : "))
            result_index = jump_search(data_list, id_to_search)
            if result_index != -1:
                print("DATA DATABASE TIDAK DITEMUKAN :")
                x = PrettyTable()
                x.field_names = ["id_pemerintah", "nama_pemerintah", "id_beasiswa"]
                x.add_row(data_list[result_index])
                print(x)
            else:
                print("DATA DATABASE TIDAK DITEMUKAN")
        elif pilihan == "4":
            break
        else:
            print("COBA LAGI !")

def tambah_data_pemerintah():
    id_pemerintah = int(input("MASUKKAN ID pemerintah : "))
    nama_pemerintah = input("MASUKAN NAMA pemerintah : ")
    id_beasiswa = int(input("MASUKAN id beasiswa : "))

    mycursor.execute("SELECT COUNT(*) FROM beasiswa WHERE id_beasiswa = %s", (id_beasiswa,))
    if mycursor.fetchone()[0] == 0:
        print("id beasiswa tidak di database beasiswa")
        return

    query = f"""
    INSERT INTO pemerintah (id_pemerintah, nama_pemerintah, id_beasiswa)
    VALUES ({id_pemerintah}, '{nama_pemerintah}', {id_beasiswa})
    """

    mycursor.execute(query)
    mydb.commit()
    print("DATA BERHASIL DITAMBAHKAN")

def hapus_data_pemerintah():
    mycursor.execute("SELECT * FROM pemerintah")
    myresult = mycursor.fetchall()
    x = PrettyTable()
    x.field_names = ["id_pemerintah", "nama_pemerintah", "id_beasiswa"]
    for data in myresult:
        x.add_row(data)
    print(x)

    id_pemerintah = int(input("MASUKKAN ID pemerintah YANG INGIN DIHAPUS : "))

    query = f"DELETE FROM pemerintah WHERE id_pemerintah = {id_pemerintah}"

    mycursor.execute(query)
    mydb.commit()
    print("DATA DATABASE BERHASIL DIHAPUS !")

def perbarui_data_pemerintah():
    mycursor.execute("SELECT * FROM pemerintah")
    myresult = mycursor.fetchall()
    x = PrettyTable()
    x.field_names = ["id_pemerintah", "nama_pemerintah", "id_beasiswa"]
    for data in myresult:
        x.add_row(data)
    print(x)

    id_pemerintah = int(input("MASUKKAN ID pemerintah YANG INGIN DIPERBARUI : "))
    nama_pemerintah = input("MASUKAN NAMA pemerintah BARU : ")
    id_beasiswa = int(input("MASUKAN id beasiswa yang sudah ada  : "))

    mycursor.execute("SELECT COUNT(*) FROM beasiswa WHERE id_beasiswa = %s", (id_beasiswa,))
    if mycursor.fetchone()[0] == 0:
        print("id beasiswa tidak ada di database beasiswa")
        return

    query = f"""
    UPDATE pemerintah
    SET nama_pemerintah = %s, id_beasiswa = %s
    WHERE id_pemerintah = %s
    """

    val = (nama_pemerintah, id_beasiswa, id_pemerintah)
    mycursor.execute(query, val)
    mydb.commit()
    print("DATA BERHASIL DIPERBARUI!")

def data_universitas():
    mycursor.execute("SELECT * FROM universitas")
    myresult = mycursor.fetchall()
    data_list = []
    for data in myresult:
        data_list.append(data)

    while True:
        print("")
        print("                  TAMPILKAN DATA universitas              ")
        print("")
        print("   1. URUTKAN DATA BERDASARKAN ID - ASCENDING             ")
        print("   2. URUTKAN DATA BERDASARKAN ID - DESCENDING            ")
        print("   3. CARI DATA BERDASARKAN ID                            ")
        print("   4. KEMBALI KE MENU DATABASE universitas                ")
        print("")

        pilihan = input("MASUKKAN PILIHAN ANDA : ")

        if pilihan == "1":
            sorted_data = sorting_cepat(data_list, ascending=True)
            ll = LinkedList()
            for data in sorted_data:
                ll.append(data)
            ll.tampilan_universitas()
        elif pilihan == "2":
            sorted_data = sorting_cepat(data_list, ascending=False)
            ll = LinkedList()
            for data in sorted_data:
                ll.append(data)
            ll.tampilan_universitas()
        elif pilihan == "3":
            id_to_search = int(input("MASUKKAN ID YANG INGIN DICARI : "))
            result_index = jump_search(data_list, id_to_search)
            if result_index != -1:
                print("DATA DITEMUKAN :")
                x = PrettyTable()
                x.field_names = ["id_universitas", "nama_universitas", "nama_fakultas", "nama_prodi", "alamat_universitas"]
                x.add_row(data_list[result_index])
                print(x)
            else:
                print("DATA TIDAK DITEMUKAN")
        elif pilihan == "4":
            break
        else:
            print("PILIHAN TIDAK VALID !")
            
def tambah_data_universitas():
    id_universitas = int(input("MASUKKAN ID universitas : "))
    nama_universitas = input("MASUKKAN NAMA universitas : ")
    nama_fakultas = input("MASUKKAN nama fakultas : ")
    nama_prodi = input("masukkan nama prodi :")
    alamat_universitas = input("MASUKKAN ALAMAT universitas : ")
    query = f"""
    INSERT INTO universitas (id_universitas, nama_universitas, nama_fakultas, nama_prodi, alamat_universitas)
    VALUES ({id_universitas}, '{nama_universitas}', '{nama_fakultas}', '{nama_prodi}', '{alamat_universitas}')
    """

    mycursor.execute(query)
    mydb.commit()
    print("DATA BERHASIL DITAMBAHKAN")

def hapus_data_universitas():
    mycursor.execute("SELECT * FROM universitas")
    myresult = mycursor.fetchall()
    x = PrettyTable()
    x.field_names = ["id_universitas", "nama_universitas", "nama_fakultas", "nama_prodi", "alamat_universitas"]
    for data in myresult:
        x.add_row(data)
    print(x)

    id_universitas = int(input("MASUKKAN ID universitas YANG INGIN DIHAPUS : "))

    query = f"DELETE FROM universitas WHERE id_universitas = {id_universitas}"

    mycursor.execute(query)
    mydb.commit()
    print("DATA BERHASIL DIHAPUS !")

def perbarui_data_universitas():
    mycursor.execute("SELECT * FROM universitas")
    myresult = mycursor.fetchall()
    x = PrettyTable()
    x.field_names = ["id_universitas", "nama_universitas", "nama_fakultas", "nama_prodi", "alamat_universitas"]
    for data in myresult:
        x.add_row(data)
    print(x)

    id_universitas = int(input("MASUKKAN ID universitas YANG INGIN DIPERBARUI : "))
    nama_universitas = input("MASUKAN NAMA universitas BARU : ")
    nama_fakultas = input("MASUKAN nama fakultas BARU : ")
    nama_prodi = input("masukkan nama prodi BARU :")
    alamat_universitas = input("MASUKKAN ALAMAT universitas BARU : ")

    query = f"""
    UPDATE universitas
    SET nama_universitas = '{nama_universitas}', nama_fakultas = '{nama_fakultas}', nama_prodi = '{nama_prodi}', alamat_universitas = '{alamat_universitas}'
    WHERE id_universitas = {id_universitas}
    """

    mycursor.execute(query)
    mydb.commit()
    print("DATA BERHASIL DIPERBARUI!")

def menu_utama_admin():
    while True:
        print("")
        print("                   DATABASE ADMIN                         ")
        print("")
        print("                1. TAMBAH DATA ADMIN                      ")
        print("                2. HAPUS DATA ADMIN                       ")
        print("                3. PERBARUI DATA ADMIN                    ")
        print("                4. TAMPILKAN DATA ADMIN                   ")
        print("                5. KELUAR DARI DATABASE ADMIN             ")
        print("")
        pilihan = input("MASUKKAN PILIHAN ANDA : ")

        if pilihan == "1":
            tambah_data_admin()
        elif pilihan == "2":
            hapus_data_admin()
        elif pilihan == "3":
            perbarui_data_admin()
        elif pilihan == "4":
            data_admin()
        elif pilihan == "5":
            print("BERHASIL KELUAR !")
            break
        else:
            print("COBA LAGI !")

def menu_utama_beasiswa():
    while True:
        print("")
        print("                   DATABASE beasiswa                     ")
        print("")
        print("                1. TAMBAH DATA beasiswa                  ")
        print("                2. HAPUS DATA beasiswa                   ")
        print("                3. PERBARUI DATA beasiswa                ")
        print("                4. TAMPILKAN DATA beasiswa               ")
        print("                5. KELUAR DARI DATABASE beasiswa         ")
        print("")
        pilihan = input("MASUKKAN PILIHAN ANDA : ")

        if pilihan == "1":
            tambah_data_beasiswa()
        elif pilihan == "2":
            hapus_data_beasiswa()
        elif pilihan == "3":
            perbarui_data_beasiswa()
        elif pilihan == "4":
            data_beasiswa()
        elif pilihan == "5":
            print("BERHASIL KELUAR !")
            break
        else:
            print("COBA LAGI !")

def menu_utama_mahasiswa():
    while True:
        print("")
        print("                   DATABASE mahasiswa                    ")
        print("")
        print("                1. TAMBAH DATA mahasiswa                 ")
        print("                2. HAPUS DATA mahasiswa                  ")
        print("                3. PERBARUI DATA mahasiswa               ")
        print("                4. TAMPILKAN DATA mahasiswa              ")
        print("                5. KELUAR        ")
        print("")
        pilihan = input("MASUKKAN PILIHAN ANDA : ")

        if pilihan == "1":
            tambah_data_mahasiswa()
        elif pilihan == "2":
            hapus_data_mahasiswa()
        elif pilihan == "3":
            perbarui_data_mahasiswa()
        elif pilihan == "4":
            data_mahasiswa()
        elif pilihan == "5":
            print("BERHASIL KELUAR !")
            break
        else:
            print("COBA LAGI !")


def menu_utama_pemerintah():
    while True:
        print("")
        print("                   DATABASE pemerintah                       ")
        print("")
        print("                1. TAMBAH DATA pemerintah                    ")
        print("                2. HAPUS DATA pemerintah                     ")
        print("                3. PERBARUI DATA pemerintah                  ")
        print("                4. TAMPILKAN DATA pemerintah                 ")
        print("                5. KELUAR            ")
        print("")
        pilihan = input("MASUKKAN PILIHAN ANDA : ")

        if pilihan == "1":
            tambah_data_pemerintah()
        elif pilihan == "2":
            hapus_data_pemerintah()
        elif pilihan == "3":
            perbarui_data_pemerintah()
        elif pilihan == "4":
            data_pemerintah()
        elif pilihan == "5":
            print("BERHASIL KELUAR !")
            print
            break
        else:
            print("SALAH PILIH !")

def menu_utama_universitas():
    while True:
        print("")
        print("                   DATABASE universitas                   ")
        print("")
        print("                1. TAMBAH DATA universitas                ")
        print("                2. HAPUS DATA universitas                 ")
        print("                3. PERBARUI DATA universitas              ")
        print("                4. TAMPILKAN DATA universitas             ")
        print("                5. KELUAR                                 ")
        print("")
        pilihan = input("MASUKKAN PILIHAN ANDA : ")

        if pilihan == "1":
            tambah_data_universitas()
        elif pilihan == "2":
            hapus_data_universitas()
        elif pilihan == "3":
            perbarui_data_universitas()
        elif pilihan == "4":
            data_universitas()
        elif pilihan == "5":
            print("BERHASIL KELUAR !")
            break
        else:
            print("COBA LAGI !")

def menu_utama_superuser():
    while True:
        print("")
        print("                  USERNAME :",username, "BERHASIL MASUK !   ")
        print("")
        print("                1. DATABASE ADMIN                  ")
        print("                2. DATABASE beasiswa               ")
        print("                3. DATABASE mahasiswa              ")
        print("                4. DATABASE pemerintah             ")
        print("                5. database universitas            ")
        print("                6. KELUAR                          ")
        print("")
        pilihan = input("MASUKKAN PILIHAN ANDA : ")

        if pilihan == "1":
            menu_utama_admin()
        elif pilihan == "2":
            menu_utama_beasiswa()
        elif pilihan == "3":
            menu_utama_mahasiswa()
        elif pilihan == "4":
            menu_utama_pemerintah()
        elif pilihan == "5":
            menu_utama_universitas()
        elif pilihan == "6":
            print("BERHASIL KELUAR !")
            break
        else:
            print("SALAH KETIK")

class LoginSystem:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.db_cursor = db_connection.cursor()

    def get_user_info(self, username):
        query = f"SELECT * FROM admin WHERE username = '{username}'"
        self.db_cursor.execute(query)
        user_data = self.db_cursor.fetchone()
        return user_data

    def login(self, username, password):
        user_data = self.get_user_info(username)
        if user_data:
            if user_data[2] == password:  
                menu_utama_superuser()
            else:
                print("PASSWORD SALAH !, COBA LAGI") 
        else:
            print("USERNAME TIDAK DITEMUKAN")
            

login_system = LoginSystem(mydb)

while True:
    print("                     PENDIDIKAN BERMUTU                   ")
    print("                                                          ")
    print("                      1. LOGIN ADMIN                      ")
    print("                      2. LOGIN USER                       ")
    print("                      2. KELUAR                           ")
    print("                                                          ")
    print("                      KELOMPOK 7                          ")
    print("")
    choice = input("PILIH MENU DI ATAS : ")

    if choice == "1":
        username = input("MASUKKAN USERNAME : ")
        password = input("MASUKKAN PASSWORD : ")
        login_system.login(username, password)
    elif choice == "2":
        print("terima kasih")

    else:
        print("SALAH KETIK")

