import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# create_monthly_trend_df() bertanggung jawab untuk menyiapkan monthly_trend_df.
def create_monthly_trend_df(df):
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
        ]
    df["month"] = pd.Categorical(df["month"], categories=month_order, ordered=True)
    monthly_trend_df = df.groupby(["year", "month"])["cnt"].sum().reset_index()
    monthly_trend_df["my_label"] = monthly_trend_df["month"].astype(str) + " " + monthly_trend_df["year"].astype(str)
    monthly_trend_df = monthly_trend_df.sort_values(["year", "month"])
    
    return monthly_trend_df

# create_season_summary_df() digunakan untuk menyiapkan season_summary_df.
def create_season_summary_df(df):
    season_order = [
    "Spring", 
    "Summer", 
    "Fall", 
    "Winter"
    ]
    df["season_label"] = pd.Categorical(df["season_label"], categories=season_order, ordered=True)
    season_summary_df = df.groupby("season_label")["cnt"].agg([
        "mean", "sum", "count"
    ])
    season_summary_df = season_summary_df.reset_index()
    
    return season_summary_df

# create_weather_summary_df() digunakan untuk menyiapkan weather_summary_df.
def create_weather_summary_df(df):
    weather_summary_df = df.groupby("weather_label")["cnt"].agg([
        "mean", "sum", "count"
    ])
    weather_summary_df = weather_summary_df.reset_index()
    
    return weather_summary_df

# Mengambil file 
all_df = pd.read_csv("main_data.csv")

# Mengurutkan DataFrame berdasarkan dteday serta memastikan kolom tersebut bertipe datetime. 
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Membuat Komponen Filter
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    #st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#start_date dan end_date di atas akan digunakan untuk memfilter all_df.
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

monthly_trend_df = create_monthly_trend_df(all_df)
season_summary_df = create_season_summary_df(all_df)
weather_summary_df = create_weather_summary_df(all_df)

st.header('Dicoding Bike Sharing Dashboard :sparkles:')

# menampilkan informasi tren bulanan peminjaman sepeda.
st.subheader('Monthly Trends')
 
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(
    x="my_label", 
    y="cnt",
    data=monthly_trend_df,
    marker="o",
    ax=ax
)
ax.set_title("Performa/tren Jumlah Peminjaman Sepeda per Bulan (2011–2012)", loc="center", fontsize=30)
ax.set_ylabel("Total Peminjaman")
ax.set_xlabel("Bulan")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

st.info("""
        Kesimpulan:
        
        - Performa peminjaman sepeda pada bulan Januari 2011 terus meningkat sampai pada bulan Mei 2011, dan konsisten sampai pada bulan September 2011 dan kembali menurun sedikit sampai pada bulan Desember.
        - Performa/tren peminjaman sepeda pada tahun 2012 juga sama pada performa peminjaman sepeda di tahun 2011 yang menandakan adanya pola musiman yang konsisten.
        - Peminjaman sepeda tertinggi pada setiap tahun berada pada bulan Mei, Juni, Juli, dan Agustus (Musim Panas dan Gugur). Peminjaman sepeda terendah berada pada musim dingin.
        - Total peminjaman sepeda pada tahun 2012 lebih tinggi daripada tahun 2011 hampir di seluruh bulan yang menandakan adanya pertumbuhan penggunaan layanan peminjaman sepeda dari tahun ke tahun.
        """)

# informasi tentang Pengaruh Musim Terhadap Peminjaman Sepeda
st.subheader("Pengaruh Musim Terhadap Peminjaman Sepeda")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
sns.boxplot(
    x="season_label", 
    y="cnt", 
    data=all_df, 
    palette="Set3", 
    ax=ax[0]
    )
ax[0].set_ylabel("Jumlah Peminjaman", fontsize=30)
ax[0].set_xlabel("Musim", fontsize=30)
ax[0].set_title("Distribusi Peminjaman Sepeda per Musim", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(
    x="season_label", 
    y="mean", 
    data=season_summary_df, 
    palette="Set3", 
    ax=ax[1]
    )
ax[1].set_ylabel("Rata-rata Jumlah Peminjaman", fontsize=30)
ax[1].set_xlabel("Musim", fontsize=30)
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Rata-rata Peminjaman Sepeda per Musim", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
plt.tight_layout()
st.pyplot(fig)

st.info("""
        Kesimpulan:
        
        - Aktivitas peminjaman sepeda tertinggi dan stabil berada pada saat Musim Gugur (Fall).
        - Peminjaman sepeda pada saat musim Spring dan Winter cenderung lebih sepi, yang kemungkinan besar dipengaruhi oleh cuaca yang kurang ideal.
        - Peminjaman sepeda pada musim Summer memiliki aktivitas yang tinggi, namun dengan fluktuasi besar yang kemungkinan karena faktor libur atau cuaca yang ekstrim.
        """)

# informasi tentang Pengaruh Cuaca Terhadap Peminjaman Sepeda
st.subheader("Pengaruh Cuaca Terhadap Peminjaman Sepeda")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.boxplot(
    x="weather_label", 
    y="cnt", 
    data=all_df, 
    palette="Set3", 
    ax=ax[0]
    )
ax[0].set_ylabel("Jumlah Peminjaman", fontsize=30)
ax[0].set_xlabel("Cuaca", fontsize=30)
ax[0].set_title("Distribusi Peminjaman Sepeda per Cuaca", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(
    x="weather_label", 
    y="mean", 
    data=weather_summary_df, 
    palette="Set2", 
    ax=ax[1]
    )
ax[1].set_ylabel("Rata-rata Jumlah Peminjaman", fontsize=30)
ax[1].set_xlabel("Cuaca", fontsize=30)
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Rata-rata Peminjaman Sepeda per Cuaca", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

st.info("""
        Kesimpulan:
        
        Rata-rata peminjaman sepeda tertinggi berada pada saat musim Fall dan Summer, dan cenderung lebih rendah pada saat musim Spring dan Winter.
        """)

# menampilkan perbedaan pola peminjaman sepeda pada kategori ramai, sedang, dan sepi berdasarkan musim dan cuaca.
st.subheader("perbedaan pola peminjaman sepeda pada kategori ramai, sedang, dan sepi berdasarkan musim dan cuaca")
 
fig, ax = plt.subplots(figsize=(35, 15))

sns.scatterplot(
    y="cnt", 
    x="dteday", 
    data=all_df, 
    hue="volume_cluster", 
    palette="tab10",
    s=80,
    alpha=0.6,
    ax=ax
    )
ax.set_ylabel("Jumlah Peminjaman", fontsize=30)
ax.set_xlabel("Tanggal", fontsize=30)
ax.set_title("Pola Jumlah Peminjaman Sepeda Harian Berdasarkan Clustering Manual", loc="center", fontsize=50)
legend = ax.legend(title="Cluster Volume", title_fontsize=25, fontsize=20)
legend.set_frame_on(True)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=35)

st.pyplot(fig)

st.info("""
        Kesimpulan:
        
        - Terlihat tren peningkatan jumlah peminjaman sepeda dari ala tahun 2011 hingga akhir tahun 2012.
        - Pada awal tahun 2011, sebagian besar titik berada pada cluster "sepi", cluster "sedang" berada pada pertengahan tahun 2011 sampai 2012, dan pada saat memasuki tahun 2012 cluster "ramai" mulai mendominasi dengan jumlah peminjaman harian yang tinggi mencapai lebih dari 8000 peminjaman sepeda per hari.
        """)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
sns.countplot(
    x="season_label", 
    data=all_df, 
    hue="volume_cluster", 
    palette="Set2", 
    ax=ax[0]
    )
ax[0].set_ylabel("Jumlah Hari", fontsize=30)
ax[0].set_xlabel("Musim", fontsize=30)
ax[0].set_title("Jumlah Hari dalam Setiap Cluster Volume per Musim", loc="center", fontsize=40)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
ax[0].legend_.remove()

handles, labels = ax[0].get_legend_handles_labels()
fig.legend(handles, labels, title="Cluster Volume", loc="center", bbox_to_anchor=(0.5, 0.8), ncol=1, fontsize=20, title_fontsize=25)
 
sns.countplot(
    x="weather_label", 
    data=all_df, 
    hue="volume_cluster", 
    palette="Set2", 
    ax=ax[1]
    )
ax[1].set_ylabel("Jumlah Hari", fontsize=30)
ax[1].set_xlabel("Kondisi Cuaca", fontsize=30)
ax[1].set_title("Jumlah Hari dalam Setiap Cluster Volume per Cuaca", loc="center", fontsize=40)
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
ax[1].legend_.remove()

plt.tight_layout()
st.pyplot(fig)

st.info("""
        Kesimpulan:
        
        - Jumlah hari pada saat Spring (Musim Semi) Kebanyakan sepi, namun ada beberapa hari dimana permintaan peminjaman sepeda sedang dan ramai.
        - Hari-hari pada saat Summer (musim panas), Fall (musim gugur), dan winter (musim Dingin) kebanyakan permintaan sepeda berada pada kategori sedang dan ramai.
        - Permintaan sepeda tinggi pada saat cuaca Clear dan jarang orang meminjam sepeda pada saat cuaca Light Snow/rain.
        """)