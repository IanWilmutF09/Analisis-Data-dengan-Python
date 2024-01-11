```markdown
# Proyek Analisis Data: Air Quality Dataset

## Navigasi
1. [Introduksi](#introduksi)
2. [Data Wrangling](#data-wrangling)
3. [Distribusi](#distribusi)
4. [Fluktuasi](#fluktuasi)
5. [Konklusi](#konklusi)

## Introduksi
Nama: Yosef Gomgom Handayani

Email: yosefgomgom2000@gmail.com

ID Dicoding: yosefgomgom_m7mc

Pertanyaan Bisnis:
- Bagaimana distribusi dari PM2.5, PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, wd, WSPM di setiap stasiun cuaca?
- Bagaimana pola fluktuasi dari PM2.5, PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, wd, WSPM di setiap stasiun cuaca?

## Data Wrangling
### Data Gathering
Dilakukan koleksi data dari 12 dataset yang masing-masing berasal dari setiap stasiun cuaca. Lalu kita memasukkan semua dataset pada suatu list. Namun, suatu kolom pada setiap dataset yaitu kolom wd (Wind Direction) merupakan tipe string. Untuk menyesuaikan tipe data, maka kita mengubah string ini ke float. Masing-masing dari setiap string memiliki nilai sudut tertentu sesuai arah mata angin.

### Assessing Data
Ada banyak nilai yang hilang pada beberapa kolom dalam dataset. Namun tidak ada duplikat pada setiap dataset. Lalu untuk mencari nilai outlier, dalam konteks ini adalah tidak mungkin untuk mencari nilai outlier dari wd karena nilai dari wd ada pada rentang 0 hingga 360 derajat. Dan dari hasil pengecekan, tidak ada outlier dari setiap dataset stasiun.

### Cleaning Data
Pembersihan data hanya untuk mengisi nilai-nilai kosong pada setiap kolom dengan nilai rata-ratanya.

## Exploratory Data Analysis (EDA)
Untuk masing-masing dataset kita ingin melihat grafik distribusi dan grafik fluktuasi pada setiap kolom untuk setiap stasiun. Ini bisa dilihat pada tab Distribusi dan Fluktuasi.

## Konklusi
### Kesimpulan
#### Konklusi pertanyaan 1:
- Karbonmonoksida: Jumlah CO (karbonmonoksida) dan persebarannya (standar deviasi) lebih besar secara signifikan. Hal ini menyebabkan karbonmonoksida masih rendah pada nilai 0-300 ppb dan terus meningkat jumlahnya di atas nilai 300 ppb.
- Dua puncak pada temperatur: Puncak pertama ada pada sekitar 20 derajat Celcius dan yang kedua sekitar 0 derajat Celcius. Namun lebih sering terjadi di sekitar 20 derajat Celcius. Dew Point Temperatur cenderung mirip dengan pola distribusi temperatur.
- Tekanan: Tekanan udara sekitar 1000 mb merupakan puncak dari distribusi tekanan udara di setiap stasiun.
- Curah hujan: Curah hujan selalu di antara 0.06 dan 0.07 mm.
- Angin: Distribui arah angin sangat bervariasi yang mungkin sangat tergantung pada lokasi di mana stasiun berada. Dan kecepatan angin memiliki puncak di sekita 1 m/s.

#### Konklusi pertanyaan 2:
- Temperatur, dew point temperatur dan tekanan udara: Ketiga hal ini memiliki fluktuasi periodik. Temperatur dan dew point temperatur memiliki hubungan atau korelasi yang positif. Sedangkan tekanan udaara memiliki korelasi yang jelas negatif. Saat temperatur meningkat begitu juga dew point temperatur dan di saat yang bersamaan tekanan udara menurun. Hal ini juga berlaki sebaliknya.
- Curah hujan: Curah hujan perlahan-lahan meningkat hingga melonjak naik di sekitar bulan Juli setiap tahunnya.
- Kecepatan angin: Kecepatan angin juga terlihat berupa periodik namun tidak memiliki pola perulangan yang jelas. Mungkin bisa dipecahkan dengan teknik statistik yang lebih advanced.
```

## Cara menjalankan dashboard

### Setup environment

pip install -r requirements.txt

### Run streamlit app
streamlit run dashboard\dashboard.py