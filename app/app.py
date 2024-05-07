from flask import Flask, render_template, request, session
import datetime
import numpy as np
from numpy.linalg import eig


app = Flask(__name__)

data_tugas = []
prioritas = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mata_kuliah = request.form['mata_kuliah']
        tenggat_waktu = request.form['tenggat_waktu']
        tenggat_waktu = datetime.datetime.strptime(tenggat_waktu, "%Y-%m-%dT%H:%M")
        partisipan = request.form['partisipan']
        sks = int(request.form['sks'])
        tingkat_kesulitan = request.form['tingkat_kesulitan']
        jenis_tugas = request.form['jenis_tugas']

        tugas_baru = {
            "mata_kuliah": mata_kuliah,
            "tenggat_waktu": tenggat_waktu,
            "partisipan": partisipan,
            "sks": sks,
            "tingkat_kesulitan": tingkat_kesulitan,
            "jenis_tugas": jenis_tugas
        }

        data_tugas.append(tugas_baru)

    return render_template('index.html', data_tugas=data_tugas, prioritas=prioritas, )

@app.route('/hitung_prioritas', methods=['POST'])
def hitung_prioritas():
    # Waktu awal yang ditentukan
    waktu_awal = datetime.datetime.now()

    # Konversi ke satuan waktu universal (detik)
    for tugas in data_tugas:
        tugas["waktu_detik"] = (tugas["tenggat_waktu"] - waktu_awal).total_seconds()
        tugas["waktu_menit"] = (tugas["waktu_detik"] / 60)

    # Mengurutkan waktu detik secara menaik
    data_tugas.sort(key=lambda x: x["waktu_menit"])

    # Inisialisasi bobot
    bobot = len(data_tugas)
    waktu_diberi_bobot = {}

    # Memberikan nilai bobot setiap waktunya
    for tugas in data_tugas:
        waktu = tugas["waktu_menit"]
        if waktu not in waktu_diberi_bobot:
            waktu_diberi_bobot[waktu] = bobot
            bobot -= 1
        tugas["bobot_waktu"] = waktu_diberi_bobot[waktu]
        print(f"{tugas['mata_kuliah']}, {round(tugas['waktu_menit'], 0)} menit | bobot: {tugas['bobot_waktu']}")

    def map_jenis_tugas(jenis_tugas):
        if jenis_tugas == "projek":
            return 5
        elif jenis_tugas in ["jurnal", "paper"]:
            return 4
        elif jenis_tugas == "esai":
            return 3
        elif jenis_tugas == "quizz":
            return 2
        elif jenis_tugas == "rangkuman":
            return 1
        else:
            return 0

    # Matriks hasil
    result_matrix = np.column_stack((
        np.array([tugas["bobot_waktu"] for tugas in data_tugas]),
        np.where(np.array([tugas["partisipan"] for tugas in data_tugas]) == "individu", 2, 1),
        np.where(np.array([tugas["sks"] for tugas in data_tugas]) == 3, 3, np.where(np.array([tugas["sks"] for tugas in data_tugas]) == 2, 2, 1)),
        np.where(np.array([tugas["tingkat_kesulitan"] for tugas in data_tugas]) == "sulit", 3, np.where(np.array([tugas["tingkat_kesulitan"] for tugas in data_tugas]) == "sedang", 2, 1)),
        np.array([map_jenis_tugas(tugas["jenis_tugas"]) for tugas in data_tugas]),
    ))

    print("Matriks bobot:")
    print(f"{'BOBOT':<14} : waktu, ps,  sks,  ks,  jt")
    for i, data in enumerate(data_tugas):
        print(f"{data['mata_kuliah']:<15}: ", end="")
        for nilai in result_matrix[i]:
            print("{:4d}".format(nilai), end=" ")
        total_nilai_per_baris = np.sum(result_matrix[i])
        print(f"  Total: {total_nilai_per_baris}")

    kriteria = {
        "Waktu": 0,
        "Partisipan": 1,
        "SKS": 2,
        "Kesulitan": 3,
        "Jenis Tugas": 4
    }

    # Loop untuk menampilkan matriks berdasarkan kriteria
    for kriteria_nama, kriteria_index in kriteria.items():
        print(f"Kriteria {kriteria_nama}: \n")

        max_width = 13
        for i, data in enumerate(data_tugas):
            # Mencetak nama mata kuliah dengan lebar yang tetap
            print(f"{data['mata_kuliah']:{max_width}}", end="")

        nilai_kriteria = result_matrix[:, kriteria_index]
        print("\n")
        # Menampilkan nilai-nilai kriteria setelah mencetak semua mata kuliah
        for nilai in nilai_kriteria:
            print(f"{nilai: <15}", end="")
        print("\n")
        print("="*40)

    # Menghitung jumlah elemen pada matriks bobot
    n = len(result_matrix)

    # Inisialisasi matriks perbandingan untuk semua kriteria
    matriks_perbandingan = {k: np.zeros((n, n)) for k in kriteria}

    # Loop untuk menghitung rasio perbandingan untuk setiap kriteria
    for kriteria_nama, kriteria_index in kriteria.items():
        # Mendapatkan nilai kriteria yang sesuai dari result_matrix
        nilai_kriteria = result_matrix[:, kriteria_index]

        # Loop untuk menghitung rasio perbandingan
        for i in range(n):
            for j in range(n):
                # Menghindari pembagian dengan nol
                if nilai_kriteria[j] != 0:
                    matriks_perbandingan[kriteria_nama][i][j] = nilai_kriteria[i] / nilai_kriteria[j]
                else:
                    matriks_perbandingan[kriteria_nama][i][j] = float('inf') if nilai_kriteria[i] != 0 else 1.0

    combined_eigenvectors = np.empty((n, 0))

    for kriteria_nama, matriks in matriks_perbandingan.items():
        #matriks perbandingan per Kreteria
        print("=" * 50)
        print(f"Matriks Perbandingan Kriteria {kriteria_nama}:")
        for i in range(n):
            for j in range(n):
                print(f"{matriks[i][j]:.2f}", end=" ")
            print()
        print()

        # Operasi dot produk dari setiap matriks perbandingan dengan dirinya sendiri
        print(f"Matriks dot Perbandingan Kriteria {kriteria_nama}:")
        hasil_dot = np.dot(matriks, matriks)
        for i in range(n):
            for j in range(n):
                print(f"{hasil_dot[i][j]:.2f}", end=" ")
            print()
        print()

        sum_each_row = np.sum(hasil_dot, axis=1)
        print("Jumlah setiap baris: ", sum_each_row)

        sum_each_row_A = np.sum(sum_each_row)
        print("Jumlah setiap baris yang telah dinormalisasi: ", sum_each_row_A)

        eigenvektor = sum_each_row / sum_each_row_A
        rounded_eigenvektor = np.round(eigenvektor, 2)

        print("Vektor Eigen Kriteria: ", rounded_eigenvektor)
        print("=" * 50, "\n")

        rounded_eigenvektor = eigenvektor.reshape((-1, 1))
        combined_eigenvectors = np.hstack((combined_eigenvectors, rounded_eigenvektor))


    print("Matriks Gabungan Eigen Vektor:")
    print(f"{'KATAGERORI':<15}: ", "W     P   SKS   K   JT")
    print("_" * 50)
    for i, data in enumerate(data_tugas):
        print(f"{data['mata_kuliah']:<15}: ", end="")
        for vec in combined_eigenvectors[i]:
            print("{:.2f}".format(vec), end=" ")
        print()

    # Data bobot kriteria
    data_bobot_max = [{
        "tenggat_waktu": len(data_tugas),
        "partisipan": 2,
        "sks": 3,
        "tingkat_kesulitan": 3,
        "jenis_tugas": 5
    }]

    A = []
    lambda_max =[]

    # Membuat result_matri_max berdasarkan bobot yang ada dalam data_bobot_max
    result_matri_max = np.array([
        [
            tugas["tenggat_waktu"],
            2 if tugas["partisipan"] == 2 else 1,
            3 if tugas["sks"] == 3 else (2 if tugas["sks"] == 2 else 1),
            3 if tugas["tingkat_kesulitan"] == 3 else (2 if tugas["tingkat_kesulitan"] == 2 else 1),
            5 if tugas["jenis_tugas"] == 5 else (4 if tugas["jenis_tugas"] == 4 else (3 if tugas["jenis_tugas"] == 3 else (2 if tugas["jenis_tugas"] == 2 else 1)))
        ] for tugas in data_bobot_max
    ])


    # Menghitung jumlah elemen pada matriks bobot
    n = len(result_matri_max[0])

    # Inisialisasi nilai konsistensi dan nilai bobot relatif

    for i in range(len(data_bobot_max)):
        # Mengambil baris ke-i dari matriks bobot sebagai matriks A
        A = result_matri_max[i]

        # Membuat matriks perbandingan B dengan ukuran n x n
        B = np.zeros((n, n))

        # Mengisi elemen-elemen pada matriks B dengan hasil pembagian elemen-elemen pada matriks A
        for j in range(n):
            for k in range(n):
                B[k][j] = A[k] / A[j] if A[j] != 0 else 0

        # Menampilkan nama mata kuliah, matriks perbandingan B, dan hasil perkalian dot
        print("Matriks Perbandingan Bobot Max:\n", B, "\n")
        dot_result = np.dot(B, B)
        print("Matriks Perkalian dot Bobot Max:\n", dot_result, "\n")

        # Menambahkan setiap baris dari hasil perkalian dot
        sum_each_row = np.sum(dot_result, axis=1)
        print("Jumlah setiap baris:\n", sum_each_row, "\n")

        #menambahkan
        sum_each_row_A = np.sum(sum_each_row)
        print("Jumlah setiap baris yang telah di normalisais:\n", sum_each_row_A, "\n")

        #eginvector kriteria
        eigenvektor_max = sum_each_row/sum_each_row_A
        print("Vektor Eigen Kriteria max:\n", eigenvektor_max, "\n")

        # Menghitung CI
        A = (np.dot(B, eigenvektor_max))
        lambda_max = (np.sum(A/eigenvektor_max))/5
        CI = ((lambda_max - n)/(n-1))
        RI = 1.12

        #Menghitung CR
        CR = CI/RI


    #Menetukan Hasil Matriks Gabungan yang kalikan dengan Matriks Bobot Maksimal
    hasil = []
    for i, data in enumerate(data_tugas):
        vec_result = []
        for vec in combined_eigenvectors[i]:
            formatted_vec = "{:.2f}".format(vec)
            #print(formatted_vec, end=" ")
            vec_result.append(float(formatted_vec))
        hasil.append(vec_result)

    hasil_akhir = np.dot(np.array(hasil), eigenvektor_max)
    print(hasil_akhir)

    # Inisialisasi dictionary untuk menyimpan hasil akhir dengan urutan mata kuliah
    hasil_dict = {}

    for i, data in enumerate(data_tugas):
        # Menghitung hasil akhir untuk setiap mata kuliah
        hasil_mata_kuliah = np.dot(np.array(hasil[i]), eigenvektor_max)
        # Menyimpan hasil akhir dengan urutan mata kuliah ke dalam dictionary
        hasil_dict[data['mata_kuliah']] = hasil_mata_kuliah

    # Mengurutkan hasil akhir berdasarkan nilai terbesar ke terkecil
    sorted_hasil = sorted(hasil_dict.items(), key=lambda x: x[1], reverse=True)

    # Menampilkan hasil urutan prioritas
    prioritas = 1
    for mata_kuliah, hasil in sorted_hasil:
        print(f"Prioritas {prioritas}: {mata_kuliah} - Hasil: {hasil}")
        prioritas += 1

        sorted_hasil = sorted(hasil_dict.items(), key=lambda x: x[1], reverse=True)
        
        return render_template('index.html', data_tugas=data_tugas, sorted_hasil=sorted_hasil)

@app.route('/tentukan_prioritas', methods=['GET'])
def tentukan_prioritas():
    hitung_prioritas()
    return render_template('index.html', data_tugas=data_tugas, prioritas=prioritas)

if __name__ == '__main__':
    app.run(debug=True)
