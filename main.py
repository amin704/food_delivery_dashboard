import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from bidi.algorithm import get_display
from arabic_reshaper import reshape

# Translation Dictionary
translations = {
    "fa": {
        "page_title": "داشبورد تحلیل داده‌های تحویل غذا",
        "lang_selector": "زبان را انتخاب کنید",
        "data_input_header": "انتخاب ورودی داده ها",
        "sample_data": "استفاده از داده نمونه ( 500 مورد )",
        "full_data": "استفاده از داده کامل",
        "map_options_header": "لطفاً یکی از گزینه‌های زیر را انتخاب کنید",
        "map_opt_restaurants": "رستوران ها",
        "map_opt_delivery_points": "نقاط تحویل",
        "map_opt_both_points": "رستوران ها و نقاط تحویل",
        "map_opt_connections": "اتصال رستوران ها و نقاط تحویل",
        "data_table_header": "ستون‌هایی که می‌خواهید نمایش داده شوند را انتخاب کنید",
        "num_rows_header": "تعداد سطرهایی که می‌خواهید نمایش داده شوند را انتخاب کنید",
        "show_data_btn": "نمایش {num_rows} سطر اول داده‌ها در ستون‌های انتخاب شده",
        "no_column_selected": "هیچ ستونی انتخاب نشده است.",
        "distribution_header": "ستون مورد نظر را انتخاب کنید",
        "distribution_of": "توزیع {selected_column}",
        "time_range_hour": "بازه زمانی (ساعت)",
        "delivery_person_rating": "امتیاز پیک",
        "delivery_person_age": "بازه سنی (سال)",
        "count_label": "تعداد",
        "rating_filter_header": "فیلتر بر اساس امتیاز پیک",
        "rating_slider_label": "محدوده امتیاز پیک را انتخاب کنید",
        "age_dist_by_rating": "توزیع سن پیک‌ها (امتیاز بین {min_rating} تا {max_rating})",
        "age_range": "بازه سنی",
        "no_data_for_rating": "هیچ داده‌ای برای محدوده امتیاز انتخابی وجود ندارد.",
        "order_time_filter_header": "فیلتر بر اساس ساعت سفارش",
        "order_time_slider_label": "محدوده ساعت سفارش را انتخاب کنید",
        "order_time_dist_by_hour": "توزیع ساعت سفارش‌ها (ساعت بین {min_hour} تا {max_hour})",
        "order_hour": "ساعت سفارش",
        "no_data_for_hour": "هیچ داده‌ای برای محدوده ساعت انتخابی وجود ندارد.",
        "correlation_header": "همبستگی بین دسته ها",
        "correlation_heatmap_title": "هیت‌مپ همبستگی بین ویژگی‌های انتخاب ‌شده",
        "comparison_header": "انتخاب ویژگی‌ها برای مقایسه",
        "feature1_select": "ویژگی اول را انتخاب کنید",
        "feature2_select": "ویژگی دوم را انتخاب کنید",
        "plot_type_select": "نوع نمودار را انتخاب کنید",
        "comparison_plot_title": "{feature1} و {feature2}",
        "final_text_header": "نظر شما چیست؟",
        "final_text_body": """این داشبورد اطلاعات مربوط به یک شرکت تحویل غذا و خوراکی را نشان می‌دهد که می‌توان با استفاده از چارت‌ها و روش‌های تحلیلی مختلف، نتایج متفاوتی را به دست آورد. مثلا می‌شود فهمید که سن تحویل‌دهندگان تا چه حد مرتبط با امتیاز دریافتی آن‌ها بوده یا شرایط آب و هوا تا چه مقدار روی ترافیک تأثیرگذار است. همچنین می‌توان بررسی کرد که در شرایط آب و هوایی مختلف یا در ساعات مختلف روز، مشتریان چه نوع سفارشی داشته‌اند. لیست این موارد می‌تواند ادامه پیدا کند و گزینه‌های زیادی را در بر بگیرد. شما فکر می‌کنید مقایسه و بررسی کدام گزینه‌ها می‌تواند به نتایج خوبی منجر شود؟ این داشبورد چه استفاده‌های دیگری می‌تواند داشته باشد؟""",
        "send_your_comment": "می‌توانید نظر خود را از طریق قسمت زیر ارسال کنید.",
        "comment_box_label": "نظر خود را بنویسید.",
        "send_button": "ارسال",
        "message_sent_success": "پیام شما دریافت شد.",
        "enter_message_warning": "لطفاً یک پیام وارد کنید!",
        
        # Column names
        "Delivery_person_Age": "سن پیک",
        "Delivery_person_Ratings": "امتیاز پیک",
        "Order_Date": "تاریخ سفارش",
        "Time_Orderd": "زمان سفارش",
        "Time_Order_picked": "زمان تحویل به پیک",
        "Weatherconditions": "شرایط آب‌وهوا",
        "Road_traffic_density": "ترافیک جاده",
        "Vehicle_condition": "وضعیت وسیله نقلیه",
        "Type_of_order": "نوع سفارش",
        "Type_of_vehicle": "نوع وسیله نقلیه",
        "multiple_deliveries": "تحویل‌های چندگانه",
        "Festival": "جشن",
        "City": "شهر",
        "Time_taken(min)": "زمان تحویل (دقیقه)"
    },
    "en": {
        "page_title": "Food Delivery Data Analysis Dashboard",
        "lang_selector": "Select Language",
        "data_input_header": "Select Data Input",
        "sample_data": "Use Sample Data (500 records)",
        "full_data": "Use Full Dataset",
        "map_options_header": "Please select one of the following options",
        "map_opt_restaurants": "Restaurants",
        "map_opt_delivery_points": "Delivery Points",
        "map_opt_both_points": "Restaurants and Delivery Points",
        "map_opt_connections": "Connect Restaurants and Delivery Points",
        "data_table_header": "Select columns to display",
        "num_rows_header": "Select the number of rows to display",
        "show_data_btn": "Showing first {num_rows} rows for selected columns",
        "no_column_selected": "No columns selected.",
        "distribution_header": "Select a column for distribution analysis",
        "distribution_of": "Distribution of {selected_column}",
        "time_range_hour": "Time Range (Hour)",
        "delivery_person_rating": "Delivery Person Rating",
        "delivery_person_age": "Age Range (Year)",
        "count_label": "Count",
        "rating_filter_header": "Filter by Delivery Person Rating",
        "rating_slider_label": "Select the rating range",
        "age_dist_by_rating": "Age Distribution for Ratings between {min_rating} and {max_rating}",
        "age_range": "Age Range",
        "no_data_for_rating": "No data available for the selected rating range.",
        "order_time_filter_header": "Filter by Order Hour",
        "order_time_slider_label": "Select the order hour range",
        "order_time_dist_by_hour": "Order Time Distribution between {min_hour}:00 and {max_hour}:00",
        "order_hour": "Order Hour",
        "no_data_for_hour": "No data available for the selected hour range.",
        "correlation_header": "Feature Correlation",
        "correlation_heatmap_title": "Correlation Heatmap of Selected Features",
        "comparison_header": "Feature Comparison",
        "feature1_select": "Select the first feature",
        "feature2_select": "Select the second feature",
        "plot_type_select": "Select the plot type",
        "comparison_plot_title": "{feature1} and {feature2}",
        "final_text_header": "What are your thoughts?",
        "final_text_body": """This dashboard displays data from a food delivery company, allowing for various analyses. For instance, we can explore the correlation between delivery person's age and their ratings, or how weather conditions affect traffic. We can also investigate order types under different weather conditions or at various times of the day. The possibilities are numerous. What other comparisons do you think could yield interesting results? What other uses could this dashboard have?""",
        "send_your_comment": "You can send your feedback using the form below.",
        "comment_box_label": "Write your comment.",
        "send_button": "Send",
        "message_sent_success": "Your message was received.",
        "enter_message_warning": "Please enter a message!",
        
        # Column names
        "Delivery_person_Age": "Delivery Person Age",
        "Delivery_person_Ratings": "Delivery Person Ratings",
        "Order_Date": "Order Date",
        "Time_Orderd": "Time Ordered",
        "Time_Order_picked": "Time Order Picked",
        "Weatherconditions": "Weather Conditions",
        "Road_traffic_density": "Road Traffic Density",
        "Vehicle_condition": "Vehicle Condition",
        "Type_of_order": "Type of Order",
        "Type_of_vehicle": "Type of Vehicle",
        "multiple_deliveries": "Multiple Deliveries",
        "Festival": "Festival",
        "City": "City",
        "Time_taken(min)": "Time Taken (min)"
    }
}





def t(key):
    return translations.get(st.session_state.lang, {}).get(key, key)

def make_farsi_text(text):
    if st.session_state.lang == 'fa':
        return get_display(reshape(str(text)))
    return str(text)

st.set_page_config(page_title="Food Delivery Dashboard", layout="centered")

def update_language():
    # This function reads the new value from the radio widget (using its key)
    # and updates the 'lang' in session_state immediately.
    st.session_state.lang = lang_options[st.session_state.language_selector]


# Global and Font Styles
st.markdown(
    """
    <style>
    /* Global styles applying to both languages */
    h1 { font-size: 24px !important; }
    h1, h2, h3, h4, h5, h6, p, label, div, span, .stButton>button {
        font-family: 'tahoma', sans-serif !important;
    }
    h2 { font-size: 24px; }
    p { font-size: 18px; }
    </style>
    """,
    unsafe_allow_html=True
)


lang_options = {"فارسی": "fa", "English": "en"}

if 'lang' not in st.session_state:
    st.session_state.lang = 'fa'
    st.session_state.language_selector = 'فارسی' 
    
    
# Language-specific Directional Styles

if st.session_state.lang == 'fa':
    st.markdown(
        """
        <style>
        .stApp { direction: rtl; text-align: right; }
        .stRadio > div { flex-direction: row-reverse; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp { direction: ltr; text-align: left; }
        </style>
        """,
        unsafe_allow_html=True
    )


#Title

with st.container():
    st.title(t("page_title"))

st.divider()



# Language Selection

with st.container(border=True):    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"**{t('lang_selector')}**")
    with col2:
        lang_options = {"فارسی": "fa", "English": "en"}
        current_lang_index = list(lang_options.values()).index(st.session_state.lang)
    selected_lang_name = st.radio(
    "",
    options=list(lang_options.keys()),
    label_visibility="collapsed",
    horizontal=True,
    # index=current_lang_index,
    key='language_selector',  #  This key is essential
    on_change=update_language  # This callback handles the update
)
    # st.session_state.lang = lang_options[selected_lang_name]

    


plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 8

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def toggle_data_view(data, full_data):
    return data if full_data else data.sample(n=500, random_state=42)

def display_map(data, option):
    view_state = pdk.ViewState(
        latitude=data["Restaurant_latitude"].mean(),
        longitude=data["Restaurant_longitude"].mean(),
        zoom=5, pitch=0
    )

    if option == t("map_opt_restaurants"):
        df_display = data.rename(columns={"Restaurant_latitude": "lat", "Restaurant_longitude": "lon"})
        st.map(df_display)

    elif option == t("map_opt_delivery_points"):
        df_display = data.rename(columns={"Delivery_location_latitude": "lat", "Delivery_location_longitude": "lon"})
        st.map(df_display)

    elif option == t("map_opt_both_points"):
        start_layer = pdk.Layer(
            "ScatterplotLayer", data,
            get_position=["Restaurant_longitude", "Restaurant_latitude"],
            get_color=[255, 0, 0], get_radius=100
        )
        end_layer = pdk.Layer(
            "ScatterplotLayer", data,
            get_position=["Delivery_location_longitude", "Delivery_location_latitude"],
            get_color=[0, 0, 255], get_radius=100
        )
        st.pydeck_chart(pdk.Deck(layers=[start_layer, end_layer], initial_view_state=view_state,
                                    map_style="mapbox://styles/mapbox/light-v9"))

    elif option == t("map_opt_connections"):
        start_layer = pdk.Layer(
            "ScatterplotLayer", data,
            get_position=["Restaurant_longitude", "Restaurant_latitude"],
            get_color=[255, 0, 0], get_radius=100
        )
        end_layer = pdk.Layer(
            "ScatterplotLayer", data,
            get_position=["Delivery_location_longitude", "Delivery_location_latitude"],
            get_color=[0, 0, 255], get_radius=100
        )

        arc_layer = pdk.Layer(
            "ArcLayer", data,
            get_source_position=["Restaurant_longitude", "Restaurant_latitude"],
            get_target_position=["Delivery_location_longitude", "Delivery_location_latitude"],
            get_width=5,
            get_tilt=15,
            get_source_color=[255, 0, 0],
            get_target_color=[0, 0, 255]
        )
        st.pydeck_chart(pdk.Deck(layers=[start_layer, end_layer, arc_layer], initial_view_state=view_state,
                                    map_style="mapbox://styles/mapbox/light-v9"))

# Load data
data = load_data("Cleaned_Food_Delivery_Dataset.csv")

# Data preprocessing
data["Time_taken(min)"] = pd.to_numeric(data["Time_taken(min)"].str.extract(r'(\d+)')[0], errors="coerce")

numeric_columns = ["Delivery_person_Age", "Delivery_person_Ratings", "Time_taken(min)"]
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=[col])
    data = data[~data[col].isin([np.inf, -np.inf])]

# Convert time columns
time_columns = ["Time_Orderd", "Time_Order_picked"]
for col in time_columns:
    if col in data.columns:
        data[col] = pd.to_datetime(data[col], format='%H:%M:%S', errors='coerce')

# Data selection
with st.container(border=True):
    data_option = st.selectbox(
        t("data_input_header"),
        [t("sample_data"), t("full_data")]
    )
    full_data_option = True if data_option == t("full_data") else False
    display_data = toggle_data_view(data, full_data_option)

st.divider()

# Map visualization
with st.container(border=True):
    map_options = [
        t("map_opt_restaurants"),
        t("map_opt_delivery_points"),
        t("map_opt_both_points"),
        t("map_opt_connections")
    ]
    option = st.radio(
        t("map_options_header"),
        map_options,
        horizontal=True
    )
    display_map(display_data, option)

st.divider()

# Data table
with st.container(border=True):
    allowed_columns = ['Delivery_person_Age', 'Delivery_person_Ratings', 'Order_Date', 'Time_Orderd',
                        'Time_Order_picked', 'Weatherconditions', 'Road_traffic_density', 'Vehicle_condition',
                        'Type_of_order', 'Type_of_vehicle', 'multiple_deliveries', 'Festival', 'City', 'Time_taken(min)']
    
    available_columns = [col for col in allowed_columns if col in data.columns]
    translated_columns = [t(col) for col in available_columns]
    
    selected_columns_translated = st.multiselect(
        t("data_table_header"),
        options=translated_columns
    )
    
    reverse_translation = {t(col): col for col in available_columns}
    selected_columns = [reverse_translation[col] for col in selected_columns_translated]
    
    num_rows = st.number_input(
        t("num_rows_header"),
        min_value=1,
        max_value=len(data),
        value=5
    )
    
    if selected_columns:
        st.write(t("show_data_btn").format(num_rows=num_rows))
        df_display = data[selected_columns].head(num_rows).reset_index(drop=True)
        df_display.index += 1
        
        df_display.columns = [t(col) for col in df_display.columns]
        st.table(df_display)
    else:
        st.write(t("no_column_selected"))

st.divider()

# Distribution analysis
with st.container(border=True):
    distribution_options = [t(col) for col in available_columns]
    selected_column_translated = st.selectbox(
        t("distribution_header"),
        options=distribution_options
    )
    
    selected_column = reverse_translation[selected_column_translated]
    
    st.markdown(f"###### {t('distribution_of').format(selected_column=t(selected_column))}")
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    if pd.api.types.is_datetime64_any_dtype(data[selected_column]):
        hours = data[selected_column].dt.hour.dropna()
        bins = range(0, 25, 2)
        labels = [f"{i}-{i + 2}" for i in range(0, 24, 2)]
        
        counts, bins, patches = ax.hist(hours, bins=bins, color='blue', alpha=0.7, rwidth=0.8, edgecolor='black')
        
        ax.set_xlabel(make_farsi_text(t("time_range_hour")))
        bin_centers = np.arange(1, 24, 2)
        ax.set_xticks(bin_centers)
        ax.set_xticklabels(labels, rotation=45)
        
        for patch in patches:
            patch.set_facecolor(np.random.rand(3, ))
    elif selected_column == "Delivery_person_Ratings":
        min_rating = float(data[selected_column].min())
        max_rating = float(data[selected_column].max())
        bins = np.arange(min_rating, max_rating + 0.5, 0.5)
        
        counts, bins, patches = ax.hist(data[selected_column].dropna(), bins=bins, color='blue', alpha=0.7,
                                        edgecolor='black')
        
        for patch in patches:
            patch.set_facecolor(np.random.rand(3, ))
        ax.set_xticks(bins)
        ax.set_xlabel(make_farsi_text(t("delivery_person_rating")))
        ax.set_xlim(min_rating, max_rating)
    
    elif selected_column == "Delivery_person_Age":
        min_age = int(data[selected_column].min())
        max_age = int(data[selected_column].max())
        bins = np.arange(min_age, max_age + 1, 3)
        
        counts, bins, patches = ax.hist(data[selected_column].dropna(), bins=bins, color='blue', alpha=0.7,
                                        edgecolor='black', rwidth=0.85)
        
        for patch in patches:
            patch.set_facecolor(np.random.rand(3, ))
        ax.set_xticks(bins)
        ax.set_xlabel(make_farsi_text(t("delivery_person_age")))
        ax.set_xlim(min_age, max_age)
    
    else:
        unique_values = data[selected_column].dropna().unique()
        counts, bins, patches = ax.hist(
            data[selected_column].dropna(),
            bins=len(unique_values),
            color='blue',
            alpha=0.7,
            rwidth=0.4,
            edgecolor='black',
        )
        
        bin_width = bins[1] - bins[0]
        bin_centers = bins[:-1] + bin_width / 2
        
        ax.set_xticks(bin_centers)
        ax.set_xticklabels(unique_values, rotation=90)
        ax.set_xlabel(make_farsi_text(t(selected_column) if selected_column in translations[st.session_state.lang] else selected_column))
        
        for patch in patches:
            patch.set_facecolor(np.random.rand(3, ))
    
    plt.tight_layout()
    ax.set_ylabel(make_farsi_text(t("count_label")))
    ax.set_title(make_farsi_text(f"{t('distribution_of').format(selected_column=t(selected_column))}"))
    st.pyplot(fig)

st.divider()

# Rating filter
with st.container(border=True):
    st.markdown(f"###### {t('rating_filter_header')}")
    min_rating, max_rating = st.slider(
        t("rating_slider_label"),
        min_value=float(data["Delivery_person_Ratings"].min()),
        max_value=float(data["Delivery_person_Ratings"].max()),
        value=(float(data["Delivery_person_Ratings"].min()), float(data["Delivery_person_Ratings"].max())),
        step=0.5
    )
    
    filtered_data_rating = data[(data["Delivery_person_Ratings"] >= min_rating) & (data["Delivery_person_Ratings"] <= max_rating)]
    
    if not filtered_data_rating.empty:
        st.markdown(f"###### {t('age_dist_by_rating').format(min_rating=min_rating, max_rating=max_rating)}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            
            min_age = int(filtered_data_rating["Delivery_person_Age"].min())
            max_age = int(filtered_data_rating["Delivery_person_Age"].max())
            age_bins = np.arange(min_age, max_age + 3, 3)
            
            sns.histplot(filtered_data_rating["Delivery_person_Age"].dropna(), bins=age_bins, kde=True, color='blue', ax=ax1)
            ax1.set_xlabel(make_farsi_text(t("Delivery_person_Age")))
            ax1.set_ylabel(make_farsi_text(t("count_label")))
            ax1.set_xticks(age_bins)
            ax1.set_xlim(min_age, max_age)
            st.pyplot(fig1)
        
        with col2:
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            
            age_groups = pd.cut(filtered_data_rating["Delivery_person_Age"], bins=age_bins)
            age_group_counts = age_groups.value_counts().sort_index()
            labels = [f"{int(bin.left)}-{int(bin.right)}" for bin in age_groups.cat.categories]
            colors = sns.color_palette("tab20", len(age_group_counts))
            
            wedges, texts, autotexts = ax2.pie(
                age_group_counts,
                labels=None,
                startangle=90,
                colors=colors,
                autopct=''
            )
            
            legend_labels = [f"{label} ({count})" for label, count in zip(labels, age_group_counts)]
            ax2.legend(wedges, legend_labels, title=make_farsi_text(t("age_range")), loc="center left",
                        bbox_to_anchor=(1, 0.5))
            
            plt.tight_layout()
            st.pyplot(fig2)
    else:
        st.write(t("no_data_for_rating"))

st.divider()

# Order time filter
with st.container(border=True):
    st.markdown(f"###### {t('order_time_filter_header')}")
    min_hour, max_hour = st.slider(
        t("order_time_slider_label"),
        min_value=0,
        max_value=23,
        value=(0, 23)
    )
    
    filtered_data_hour = data[
        (data["Time_Orderd"].dt.hour >= min_hour) & (data["Time_Orderd"].dt.hour <= max_hour)
    ]
    
    if not filtered_data_hour.empty:
        st.markdown(f"###### {t('order_time_dist_by_hour').format(min_hour=min_hour, max_hour=max_hour)}")
        col3, col4 = st.columns(2)
        
        with col3:
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            hour_bins = np.arange(0, 25, 1)
            sns.histplot(filtered_data_hour["Time_Orderd"].dt.hour.dropna(), bins=hour_bins, kde=True, color='green',
                            ax=ax3)
            ax3.set_xlabel(make_farsi_text(t("order_hour")))
            ax3.set_ylabel(make_farsi_text(t("count_label")))
            
            ax3.set_xticks(hour_bins)
            st.pyplot(fig3)
        
        with col4:
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            
            hour_counts = filtered_data_hour["Time_Orderd"].dt.hour.value_counts().sort_index()
            labels = [f"{hour}-{hour + 1}" for hour in hour_counts.index]
            colors = sns.color_palette("tab20", len(hour_counts))
            
            wedges, texts, autotexts = ax4.pie(
                hour_counts,
                labels=None,
                startangle=90,
                colors=colors,
                autopct=''
            )
            legend_labels = [f"{label} ({count})" for label, count in zip(labels, hour_counts)]
            ax4.legend(wedges, legend_labels, title=make_farsi_text(t("order_hour")), loc="center left",
                        bbox_to_anchor=(1, 0.5))
            
            plt.tight_layout()
            st.pyplot(fig4)
    else:
        st.write(t("no_data_for_hour"))

st.divider()

# Correlation heatmap
with st.container(border=True):
    corr_data = data[available_columns].copy()
    
    for col in corr_data.columns:
        if corr_data[col].dtype == 'object':
            corr_data[col] = pd.factorize(corr_data[col])[0]
    
    st.markdown(f"###### {t('correlation_header')}")
    
    correlation_matrix = corr_data.corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        annot_kws={"size": 8},
        fmt=".2f",
        cmap="Purples",
        linewidths=0.5,
        ax=ax
    )
    
    translated_labels = [make_farsi_text(t(col) if col in translations[st.session_state.lang] else col) for col in correlation_matrix.columns]
    
    ax.set_xticklabels(translated_labels, rotation=90, fontsize=10)
    ax.set_yticklabels(translated_labels, rotation=0, fontsize=10)
    ax.set_title(make_farsi_text(t("correlation_heatmap_title")))
    st.pyplot(fig)

st.divider()

# Feature comparison
with st.container(border=True):
    st.markdown(f"###### {t('comparison_header')}")
    
    comparison_columns = available_columns + ["Restaurant_latitude", "Restaurant_longitude", 
                                                "Delivery_location_latitude", "Delivery_location_longitude"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        feature1 = st.selectbox(
            t("feature1_select"),
            options=comparison_columns,
            index=0
        )
    
    with col2:
        feature2 = st.selectbox(
            t("feature2_select"),
            options=comparison_columns,
            index=1
        )
    
    plot_type = st.radio(
        t("plot_type_select"),
        ["Scatter Plot", "Jointplot"],
        horizontal=True
    )
    
    if plot_type == "Scatter Plot":
        st.markdown(f"###### {t('comparison_plot_title').format(feature1=t(feature1), feature2=t(feature2))}")
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(
            data=data,
            x=feature1,
            y=feature2,
            ax=ax
        )
        
        ax.set_xlabel(make_farsi_text(t(feature1) if feature1 in translations[st.session_state.lang] else feature1), fontsize=12)
        ax.set_ylabel(make_farsi_text(t(feature2) if feature2 in translations[st.session_state.lang] else feature2), fontsize=12)
        st.pyplot(fig)
    
    elif plot_type == "Jointplot":
        st.markdown(f"###### {t('comparison_plot_title').format(feature1=t(feature1), feature2=t(feature2))}")
        
        joint_plot = sns.jointplot(
            data=data,
            x=feature1,
            y=feature2,
            height=6,
            ratio=3,
            marginal_ticks=True,
        )
        joint_plot.set_axis_labels(
            make_farsi_text(t(feature1) if feature1 in translations[st.session_state.lang] else feature1), 
            make_farsi_text(t(feature2) if feature2 in translations[st.session_state.lang] else feature2), 
            fontsize=10
        )
        
        joint_plot.ax_joint.tick_params(axis='both', labelsize=8)
        joint_plot.ax_marg_x.tick_params(labelsize=8)
        joint_plot.ax_marg_y.tick_params(labelsize=8)
        st.pyplot(joint_plot)

st.divider()

# Feedback section
with st.container(border=True):
    st.markdown(f"###### {t('final_text_header')}")
    st.markdown(t("final_text_body"))
    
    st.markdown(f"**{t('send_your_comment')}**")
    user_message = st.text_area(t("comment_box_label"), height=150)
    
    if st.button(t("send_button"), use_container_width=True):
        if user_message.strip():
            st.success(t("message_sent_success"))
        else:
            st.warning(t("enter_message_warning"))
