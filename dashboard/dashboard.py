import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data 
all_df = pd.read_csv("https://raw.githubusercontent.com/ayuaprliia/Bike_Sharing_Analysis_Project/refs/heads/main/dashboard/main_data.csv")

# title
st.title("Dashboard Bike Sharing Dataset:bike:")
st.sidebar.image("../logo.jpg")


# Home
def show_home():
    st.subheader("Selamat Datang di Dashboard Analisis Bike Sharing Dataset!")
    st.write("Dashboard ini menyajikan analisis mendalam mengenai penyewaan sepeda berdasarkan berbagai faktor, "
             "seperti kondisi cuaca, hari kerja, dan waktu penyewaan. Pilih analisis yang ingin Anda lihat "
             "dari menu di sebelah kiri.")

# Sidebar
st.sidebar.header("Menu")
menu = st.sidebar.selectbox("Pilih analisis yang ingin ditampilkan", 
                             ['Home', 
                              'Jumlah Penyewaan Sepeda berdasarkan Hari', 
                              'Jumlah Penyewaan Sepeda per Jam', 
                              'Perbandingan Penyewaan antara Registered dan Casual Users', 
                              'Kondisi Cuaca dengan Penyewaan Paling Sedikit'])

# Tampilkan Beranda
if menu == 'Home':
    show_home()

# 1. Jumlah Penyewaan Sepeda berdasarkan Hari
elif menu == 'Jumlah Penyewaan Sepeda berdasarkan Hari':
    all_df['day_category'] = all_df.apply(lambda row: 'Holiday' if row['holiday'] == 1 else (
        'Weekend' if row['workingday'] == 0 else 'Working Day'), axis=1)
    
    user_type_day_category = all_df.groupby(['day_category'])[['registered', 'casual']].sum().reset_index()

    st.subheader("Jumlah Penyewaan Sepeda berdasarkan Hari")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    x = range(len(user_type_day_category['day_category']))

    ax.bar(x, user_type_day_category['registered'], width=bar_width, color='skyblue', label='Registered Users')
    ax.bar([p + bar_width for p in x], user_type_day_category['casual'], width=bar_width, color='orange', label='Casual Users')

    ax.set_title('Jumlah Penyewaan Sepeda berdasarkan Hari', fontsize=16)
    ax.set_xlabel('Kategori Hari', fontsize=14)
    ax.set_ylabel('Total Penyewaan', fontsize=14)
    ax.set_xticks([p + bar_width / 2 for p in x])
    ax.set_xticklabels(user_type_day_category['day_category'])
    ax.legend()

    st.pyplot(fig)

    rental_counts = all_df.groupby('day_category')['cnt'].sum().reset_index()

    weekday_mapping = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri'}
    working_day_rents = all_df[all_df['workingday'] == 1].groupby('weekday')['cnt'].sum().reset_index()
    working_day_rents['weekday'] = working_day_rents['weekday'].replace(weekday_mapping)

    plt.figure(figsize=(12, 8))

    # Total Rents Based on Day Category bar chart
    plt.subplot(2, 1, 1)
    plt.bar(rental_counts['day_category'], rental_counts['cnt'], color=['lightblue', 'lightblue', 'skyblue'], width=0.4)
    plt.title('Total Rents Based on Day Category', fontsize=16)
    plt.ylabel('Total Rents', fontsize=14)
    plt.xticks(rotation=0)

    for index, value in enumerate(rental_counts['cnt']):
        plt.text(index, value, f"{value}", ha='center', va='bottom')

    # Total Rents on Working Day (Mon-Fri)
    plt.subplot(2, 1, 2)
    plt.bar(working_day_rents['weekday'], working_day_rents['cnt'], color='skyblue', width=0.4)
    plt.title('Total Rents on Working Day (Mon-Fri)', fontsize=16)
    plt.ylabel('Total Rents', fontsize=14)
    plt.xticks(rotation=0)

    for index, value in enumerate(working_day_rents['cnt']):
        plt.text(index, value, f"{value}", ha='center', va='bottom')

    st.pyplot(plt)

    with st.expander("See Insight"):
        st.write(
            """Untuk pertanyaan pertama mengenai "Jumlah penyewaan sepeda berdasarkan kategori hari", 
            hasil analisis divisualisasikan dalam bentuk diagram batang. Pada diagram batang pertama, 
            terlihat bahwa penyewaan sepeda mencapai angka tertinggi pada hari kerja, dengan total 2.292.410 
            penyewaan selama tahun 2011-2012. Sebaliknya, jumlah penyewaan terendah terjadi pada hari libur. 
            Pada diagram batang kedua, terlihat bahwa penyewaan sepeda pada hari kerja menunjukkan pola yang stabil, 
            dengan puncak tertinggi terjadi pada hari Kamis.
            """
        )


# 2. Jumlah Penyewaan Sepeda per Jam
elif menu == 'Jumlah Penyewaan Sepeda per Jam':
    # Group by hour and sum rentals
    hourly_rentals = all_df.groupby('hr')[['registered', 'casual']].sum().reset_index()
    hourly_rentals['total_rents'] = hourly_rentals['registered'] + hourly_rentals['casual']  # Adding a new column for total rentals

    st.subheader("Jumlah Penyewaan Sepeda per Jam")
    
    plt.figure(figsize=(12, 6))
    plt.plot(hourly_rentals['hr'], hourly_rentals['total_rents'], marker='o', color='indianred', linestyle='-', linewidth=2)

    plt.title('Total Rents Based on Hours', fontsize=16)
    plt.xlabel('Hours', fontsize=14)
    plt.ylabel('Total Rents', fontsize=14)
    plt.xticks(hourly_rentals['hr'])   
    plt.xticks(rotation=0)     
    st.pyplot(plt)

    with st.expander("See Insight"):
        st.write(
            """Untuk pertanyaan kedua mengenai "jumlah penyewaan sepeda sepanjang hari berdasarkan 
            jam-jam tertentu", hasil analisis divisualisasikan dengan line chart agar dapat melihat
              tren serta dinamika jumlah penyewaan sepeda pada berbagai jam. Pada diagram garis, terlihat 
              bahwa penyewaan sepeda mengalami peningkatan yang signifikan dimulai pada pukul 6-8 pagi hari 
              dan mencapai puncak tertinggi pada pukul 5-6 sore.
            """
        )


# 3. Perbandingan Penyewaan antara Registered dan Casual Users
elif menu == 'Perbandingan Penyewaan antara Registered dan Casual Users':
    hourly_rentals = all_df.groupby('hr')[['registered', 'casual']].sum().reset_index()

    # Prepare data for comparison
    total_rentals = all_df[['registered', 'casual']].sum().reset_index()
    total_rentals.columns = ['User Type', 'Total Rentals']

    plt.figure(figsize=(12, 8))

    # Total Rentals Between Registered and Casual Users
    plt.subplot(3, 1, 1) 
    plt.bar(total_rentals['User Type'], total_rentals['Total Rentals'], color=['skyblue', 'orange'], width=0.10)
    plt.title('Total Rentals Between Registered and Casual Users', fontsize=16)
    plt.ylabel('Total Rentals', fontsize=14)
    plt.xticks(rotation=0)

    # Average Daily Rentals by Registered and Casual Users
    avg_daily_rentals = all_df[['registered', 'casual']].mean().reset_index()
    avg_daily_rentals.columns = ['User Type', 'Average Daily Rentals']
    plt.subplot(3, 1, 2) 
    plt.bar(avg_daily_rentals['User Type'], avg_daily_rentals['Average Daily Rentals'], color=['skyblue', 'orange'], width=0.10)
    plt.title('Average Daily Rentals by Registered and Casual Users', fontsize=16)
    plt.ylabel('Average Daily Rentals', fontsize=14)
    plt.xticks(rotation=0)

    # Rental Trends by Hour for Both Registered and Casual User
    plt.subplot(3, 1, 3) 
    plt.plot(hourly_rentals['hr'], hourly_rentals['registered'], label='Registered Users', marker='o')
    plt.plot(hourly_rentals['hr'], hourly_rentals['casual'], label='Casual Users', marker='o')
    plt.title('Rental Trends by Hour (Registered and Casual Users)', fontsize=16)
    plt.xlabel('Hour of the Day', fontsize=14)
    plt.ylabel('Total Rentals', fontsize=14)
    plt.xticks(hourly_rentals['hr'])
    plt.legend()
    plt.grid()

    plt.subplots_adjust(hspace=0.5)    
    st.pyplot(plt)

    with st.expander("See Insight"):
        st.write(
            """Untuk pertanyaan mengenai "Perbandingan registered and casual users 
            dalam jumlah penyewaan sepeda", jawabannya divisualisasikan dengan menggunakan 
            diagram batang dan juga diagram garis. Pada diagram batang pertama dan kedua, 
            registered users memiliki tingkat penyewaan sepeda jauh lebih tinggi dibandingkan 
            dengan casual users, dengan registered users memiliki rata-rata penyewaan sepeda harian 
            di angka 153. Pada diagram garis, registered users cenderung menyewa sepeda pada jam-jam 
            kerja untuk keperluan mobilitas, sedangkan pola sewa dari casual users lebih fluktuatif, 
            yang menunjukkan bahwa mereka memiliki lebih banyak waktu luang untuk beraktivitas.
            """
        )

# 4. Kondisi Cuaca dengan Penyewaan Paling Sedikit
elif menu == 'Kondisi Cuaca dengan Penyewaan Paling Sedikit':
    weathersit_rentals = all_df.groupby('weathersit')['cnt'].agg(['sum', 'mean']).reset_index()
    weathersit_rentals['weathersit'] = weathersit_rentals['weathersit'].replace({
        1: 'Clear, Few clouds',
        2: 'Mist+cloudy',
        3: 'Light Snow, light rain',
        4: 'Heavy Rain'
    })
    min_rentals = weathersit_rentals.loc[weathersit_rentals['sum'].idxmin()]
    st.subheader("Kondisi Cuaca dengan Penyewaan Paling Sedikit")
    st.write(f"Kondisi cuaca dengan penyewaan paling sedikit adalah: **{min_rentals['weathersit']}** "
             f"dengan total penyewaan sebanyak **{min_rentals['sum']}**.")

    plt.figure(figsize=(10, 6))
    plt.bar(weathersit_rentals['weathersit'], weathersit_rentals['sum'], color='skyblue')
    plt.title('Total Rentals by Weather Condition', fontsize=16)
    plt.ylabel('Total Rentals', fontsize=14)
    plt.xticks(rotation=45)

    for index, value in enumerate(weathersit_rentals['sum']):
        plt.text(index, value, f"{value}", ha='center', va='bottom')

    st.pyplot(plt)

    with st.expander("See Insight"):
        st.write(
            """Untuk pertanyaan keempat mengenai "Pada saat cuaca apa jumlah penyewaan sepeda 
            paling sedikit? ", jawabannya divisualisasikan dengan diagram batang. Pada diagram, 
            jumlah penyewaan sepeda yang paling sedikit jatuh pada saat cuaca ekstrim, yaitu hujan 
            lebat disertai badai atau bersalju disertai kabut. Tentunya hal ini masuk akal karena 
            pada cuaca ekstrim, orang-orang tidak bisa beraktivitas secara normal.
            """
        )

# Display data preview
st.sidebar.subheader("Data Preview")
if st.sidebar.checkbox("Show Data"):
    st.write(all_df.head())

st.caption('copyright (c) Bike Sharing Dataset 2024')
