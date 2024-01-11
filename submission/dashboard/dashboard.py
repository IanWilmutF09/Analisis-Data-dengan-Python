import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.dates as mdates
import datetime

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Pergi ke", ['Introduksi', 'Data Wrangling', 'Distribusi', 'Fluktuasi', 'Konklusi'])

    if selection == 'Introduksi':
        st.title('Introduksi')
        introduksi()

    if selection == 'Data Wrangling':
        st.title('Data Wrangling')
        data_wrangling_text()

    elif selection == 'Distribusi':
        st.title('Distribusi Data')
        plot_graphs_distribution()

    elif selection == 'Fluktuasi':
        st.title('Fluktuasi Data')
        plot_graphs_fluctuation()

    elif selection == 'Konklusi':
        st.title('Konklusi')
        konklusi()

def introduksi():
        st.title('Proyek Analisis Data: Air Quality Dataset')
        st.write('**Nama:** Yosef Gomgom Handayani')
        st.write('**Email:** yosefgomgom2000@gmail.com')
        st.write('**ID Dicoding:** yosefgomgom_m7mc')
        st.header('Menentukan Pertanyaan Bisnis')
        st.write('- Bagaimana distribusi dari PM2.5, PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, wd, WSPM di setiap stasiun cuaca?')
        st.write('- Bagaimana pola fluktuasi dari PM2.5, PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, wd, WSPM di setiap stasiun cuaca?')

def data_wrangling():
        # from google.colab import drive
        # drive.mount('/content/drive')

        # !cp -r "/content/drive/MyDrive/Bangkit Academy/Air-quality-dataset" .

        # tentukan path folder
        folder_path = 'Air-quality-dataset/PRSA_Data_20130301-20170228/'

        # buat daftar nama-nama direktori pada folder tersebut
        files = os.listdir(folder_path)
        print(files)
        # buat daftar kosong untuk menyimpan direktori
        dfs = []
        # lakukan loop pada setiap direktori dalam folder
        for file in files:
            # rangkai path folder dan direktori
            file_path = os.path.join(folder_path, file)
            # baca file csv dan konversi ke dataframe
            df = pd.read_csv(file_path)
            # masukkan dataframe ke daftar kosong
            dfs.append(df)
        # buat kamus yang memetakan notasi mata angin ke sudut angin
        directions = {
            'N': 0,
            'NNE': 22.5,
            'NE': 45,
            'ENE': 67.5,
            'E': 90,
            'ESE': 112.5,
            'SE': 135,
            'SSE': 157.5,
            'S': 180,
            'SSW': 202.5,
            'SW': 225,
            'WSW': 247.5,
            'W': 270,
            'WNW': 292.5,
            'NW': 315,
            'NNW': 337.5
        }

        # loop melalui setiap DataFrame dalam dfs
        for df in dfs:
            # ubah notasi mata angin menjadi sudut angin
            df['wd'] = df['wd'].replace(directions)
        
        #Cek nilai yang hilang
        for i in range(len(dfs)):
            print(dfs[i].isnull().sum())

        for i in range(len(dfs)):
            print("Jumlah duplikasi: ", dfs[i].duplicated().sum())

        #Cek nilai outlier
        for i in range(len(dfs)):
            q25, q75 = np.percentile(dfs[i].drop(['No', 'year', 'month', 'day', 'hour', 'wd', 'station'], axis=1), 25), np.percentile(dfs[i].drop(['No', 'year', 'month', 'day', 'hour', 'wd', 'station'], axis=1), 75)
            iqr = q75 - q25
            cut_off = iqr * 1.5
            minimum, maximum = q25 - cut_off, q75 + cut_off

            outliers = [x for col in dfs[i].drop(['No', 'year', 'month', 'day', 'hour', 'wd', 'station'], axis=1).columns for x in dfs[i][col] if x < minimum or x > maximum]
            # cetak jumlah total outliers
            print(len(outliers))

            # cetak 10 outliers pertama
            print(outliers[:10])

        for df in dfs:
            for column in df.columns:
                if column not in ['station', 'No.']:
                    df[column] = df[column].fillna(df[column].mean())
        return files, dfs

files, dfs = data_wrangling()

def data_wrangling_text():
        st.subheader("Data Gathering")
        st.markdown("Dilakukan koleksi data dari 12 dataset yang masing-masing berasal dari setiap stasiun cuaca.")
        st.markdown("Lalu kita memasukkan semua dataset pada suatu list.")
        st.markdown("Namun, suatu kolom pada setiap dataset yaitu kolom wd (Wind Direction) merupakan tipe string. Untuk menyesuaikan tipe data, maka kita mengubah string ini ke float. Masing-masing dari setiap string memiliki nilai sudut tertentu sesuai arah mata angin.")
        st.subheader("Assessing Data")
        st.markdown("Ada banyak nilai yang hilang pada beberapa kolom dalam dataset.")
        st.markdown("Namun tidak ada duplikat pada setiap dataset. Lalu untuk mencari nilai outlier, dalam konteks ini adalah tidak mungkin untuk mencari nilai outlier dari wd karena nilai dari wd ada pada rentang 0 hingga 360 derajat.")
        st.markdown("Dan dari hasil pengecekan, tidak ada outlier dari setiap dataset stasiun.")
        st.subheader("Cleaning Data")
        st.markdown("Pembersihan data hanya untuk mengisi nilai-nilai kosong pada setiap kolom dengan nilai rata-ratanya.")
        st.header("Exploratory Data Analysis (EDA)")
        st.subheader("Explore")
        st.markdown("Untuk masing-masing dataset kita ingin melihat grafik distribusi dan grafik fluktuasi pada setiap kolom untuk setiap stasiun. Ini bisa dilihat pada tab **Distribusi** dan **Fluktuasi**")

nama_stasiun = [file.split('_')[2] for file in files]

# buat sebutan dari setiap kolom
sebutan = {
    'PM2.5': 'Partikulat <2.5 mikro',
    'PM10': 'Partikulat <10 mikro',
    'SO2': 'SO2',
    'NO2': 'NO2',
    'CO': 'CO',
    'O3': 'Ozon',
    'TEMP': 'Temperatur Udara',
    'PRES': 'Tekanan Udara',
    'RAIN': 'Curah Hujan',
    'DEWP': 'Dew Point',
    'wd': 'Arah Angin',
    'WSPM': 'Kecepatan Angin'
}
# buat kamus yang memetakan nama kolom ke unitnya
unit = {
    'PM2.5': 'ppb',
    'PM10': 'ppb',
    'SO2': 'ppb',
    'NO2': 'ppb',
    'CO': 'ppb',
    'O3': 'ppb',
    'TEMP': '°C',
    'PRES': 'mb',
    'RAIN': 'mm',
    'DEWP': '°C',
    'wd': '°',
    'WSPM': 'm/s'
}

### Pertanyaan 1:

def plot_loop_distribution(dfs, exclude_columns, same_plot_columns):
    # create a select box for the user to choose a station
    selected_station = st.selectbox('', options=nama_stasiun)
    
    # find the index of the selected station
    i = nama_stasiun.index(selected_station)
    
    # get the DataFrame for the selected station
    df = dfs[i]
    
    fig, ax = plt.subplots(figsize=(12, 5))
    st.subheader(f'Stasiun {selected_station}')
    for col in same_plot_columns:
        # Plot each column and assign a label for the legend
        sns.histplot(df[col].dropna(), bins=15, kde=True, label=col, ax=ax)

    ax.set_xlim(0, 300)
    ax.set_title(f'Distribusi {", ".join(same_plot_columns)} di stasiun {selected_station}', size=20)
    ax.set_xlabel('Partikel/Senyawa', size=15)
    ax.set_ylabel('Frekuensi', size=15)

    # Add a legend based on the labels assigned above
    ax.legend()

    # show the plot in Streamlit
    st.pyplot(fig)

    for col in df.columns:
        if col not in exclude_columns and col not in same_plot_columns:
            fig, ax = plt.subplots(figsize=(12, 5))
            sns.histplot(df[col].dropna(), bins=15, kde=True, ax=ax)
            ax.set_title(f'Distribusi {sebutan[col]} di stasiun {selected_station}', size=20)
            ax.set_xlabel(f'{sebutan[col]} ({unit[col]})', size=15)
            ax.set_ylabel('Frekuensi', size=15)
            st.pyplot(fig)

def plot_graphs_distribution():
    exclude_columns = ['year', 'month', 'day', 'hour', 'No', 'station', 'datetime']
    same_plot_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    plot_loop_distribution(dfs, exclude_columns, same_plot_columns)


### Pertanyaan 2:

def plot_loop_fluctuation(dfs, exclude_columns):
    # loop through each DataFrame in dfs
    for i, df in enumerate(dfs):
        # create a new 'datetime' column from the 'year', 'month', 'day', and 'hour' columns
        df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
        
        # create a select box for each station
        exclude_columns_fluctuation = ['No', 'station', 'year', 'month', 'day', 'hour', 'datetime']
        options = df.columns.drop(exclude_columns_fluctuation)
        st.subheader(f'Stasiun {nama_stasiun[i]}')
        station = st.selectbox(f'', options, key=f'StationSelectBox{i}', format_func=lambda x: sebutan[x] if x not in exclude_columns else x)

        # create a new figure for the selected column
        fig, ax = plt.subplots(figsize=(12, 5))

        # create a line plot for the selected column
        ax.plot(df['datetime'], df[station], color='blue')

        # set the title and axis labels
        ax.set_title(f'Fluktuasi {sebutan[station]} di stasiun {nama_stasiun[i]}', size=20)
        ax.set_xlabel('Waktu', size=15)
        ax.set_ylabel(f'{sebutan[station]} ({unit[station]})', size=15)  # add units to the y-axis label

        # show the plot in Streamlit
        st.pyplot(fig)

def plot_graphs_fluctuation():
    exclude_columns = ['year', 'month', 'day', 'hour', 'No', 'station', 'datetime']
    plot_loop_fluctuation(dfs, exclude_columns)

def konklusi():

        st.header('Kesimpulan')

        st.subheader('Konklusi pertanyaan 1:')
        st.markdown("""
        ## Karbonmonoksida
        Jumlah CO (karbonmonoksida) dan persebarannya (standar deviasi) lebih besar secara signifikan. Hal ini menyebabkan karbonmonoksida masih rendah pada nilai 0-300 ppb dan terus meningkat jumlahnya di atas nilai 300 ppb.

        ## Dua puncak pada temperatur
        Puncak pertama ada pada sekitar 20 derajat Celcius dan yang kedua sekitar 0 derajat Celcius. Namun lebih sering terjadi di sekitar 20 derajat Celcius. Dew Point Temperatur cenderung mirip dengan pola distribusi temperatur.

        ## Tekanan
        Tekanan udara sekitar 1000 mb merupakan puncak dari distribusi tekanan udara di setiap stasiun

        ## Curah hujan
        Curah hujan selalu di antara 0.06 dan 0.07 mm

        ## Angin
        Distribui arah angin sangat bervariasi yang mungkin sangat tergantung pada lokasi di mana stasiun berada. Dan kecepatan angin memiliki puncak di sekita 1 m/s.
        """)

        st.subheader('Konklusi pertanyaan 2:')
        st.markdown("""
        ## Temperatur, dew point temperatur dan tekanan udara
        Ketiga hal ini memiliki fluktuasi periodik. Temperatur dan dew point temperatur memiliki hubungan atau korelasi yang positif. Sedangkan tekanan udaara memiliki korelasi yang jelas negatif. Saat temperatur meningkat begitu juga dew point temperatur dan di saat yang bersamaan tekanan udara menurun. Hal ini juga berlaki sebaliknya.

        ## Curah hujan
        Curah hujan perlahan-lahan meningkat hingga melonjak naik di sekitar bulan Juli setiap tahunnya.

        ## Kecepatan angin
        Kecepatan angin juga terlihat berupa periodik namun tidak memiliki pola perulangan yang jelas. Mungkin bisa dipecahkan dengan teknik statistik yang lebih advanced.
        """)

if __name__ == "__main__":
    main()