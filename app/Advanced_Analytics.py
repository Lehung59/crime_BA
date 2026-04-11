import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import folium
from folium import plugins
from streamlit_folium import st_folium
import os

# Cấu hình đường dẫn
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@st.cache_data
def load_advanced_data():
    profile_path = os.path.join(root_dir, 'data', 'processed', 'Criminal_Profiling_cleaned.csv')
    outcome_path = os.path.join(root_dir, 'data', 'processed', 'Case_Outcome_Cleaned.csv')
    pattern_path = os.path.join(root_dir, 'data', 'processed', 'Crime_Pattern_Analysis_Cleaned.csv')
    
    profile_df = pd.read_csv(profile_path)
    outcome_df = pd.read_csv(outcome_path)
    pattern_df = pd.read_csv(pattern_path)
    return profile_df, outcome_df, pattern_df

def advanced_analytics():
    st.title("Phân tích Nâng cao & Mô hình Dự báo")
    st.markdown("""
        Module này tập trung vào các mô hình học máy có tính diễn giải cao (Interpretable AI) 
        để giải mã các mối tương quan giữa con người, địa điểm và mức độ nghiêm trọng của tội phạm.
    """)

    profile_df, outcome_df, pattern_df = load_advanced_data()

    tab1, tab2 = st.tabs([
        "📊 Tương quan Nhân khẩu học", 
        "🌳 Dự báo Mức độ Nghiêm trọng"
    ])

    # ------------------------------------------------------------------
    # TAB 1: TƯƠNG QUAN NHÂN KHẨU HỌC
    # ------------------------------------------------------------------
    with tab1:
        st.subheader("Mối liên hệ giữa Nghề nghiệp, Đẳng cấp và Loại tội phạm")
        st.write("Phân tích tỷ trọng các nhóm tội danh dựa trên đặc điểm nhân thân.")

        feature = st.selectbox("Chọn đặc điểm nhân thân:", ["Caste", "Occupation", "Sex"])
        
        # Chỉ lấy top 15 để heatmap không bị quá dày
        top_categories = profile_df[feature].value_counts().nlargest(15).index
        filtered_df = profile_df[profile_df[feature].isin(top_categories)]
        
        # Tạo bảng chéo (cross-tabulation)
        ct = pd.crosstab(filtered_df[feature], filtered_df['Crime_Group1'], normalize='index') * 100
        
        fig = px.imshow(
            ct,
            labels=dict(x="Nhóm tội phạm", y=feature, color="Tỷ lệ (%)"),
            x=ct.columns,
            y=ct.index,
            aspect="auto",
            color_continuous_scale="Viridis",
            title=f"Heatmap Tương quan: {feature} vs Nhóm tội phạm"
        )
        st.plotly_chart(fig, width='stretch')
        
    # ------------------------------------------------------------------
    # TAB 2: DỰ BÁO MỨC ĐỘ NGHIÊM TRỌNG (DECISION TREE)
    # ------------------------------------------------------------------
    with tab2:
        st.subheader("Dự báo mức độ nghiêm trọng (Heinous vs Non-Heinous)")
        st.write("Sử dụng Cây quyết định (Decision Tree) để hiểu các yếu tố dẫn đến một vụ án nghiêm trọng.")

        # Chuẩn bị dữ liệu cho mô hình (Interpretable)
        model_data = outcome_df[['Month', 'District_Name', 'Crime_Category', 'FIR_Type']].dropna()
        
        le_dist = LabelEncoder()
        le_cat = LabelEncoder()
        
        model_data['District_Encoded'] = le_dist.fit_transform(model_data['District_Name'])
        model_data['Category_Encoded'] = le_cat.fit_transform(model_data['Crime_Category'])
        model_data['Target'] = (model_data['FIR_Type'] == 'Heinous').astype(int)
        
        X = model_data[['Month', 'District_Encoded', 'Category_Encoded']]
        y = model_data['Target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        clf = DecisionTreeClassifier(max_depth=3) 
        clf.fit(X_train, y_train)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.write("**Công cụ thử nghiệm:**")
            test_month = st.slider("Tháng", 1, 12, 6)
            test_dist = st.selectbox("Chọn Quận", le_dist.classes_)
            test_cat = st.selectbox("Chọn Danh mục", le_cat.classes_)
            
            input_d = pd.DataFrame([[
                test_month, 
                le_dist.transform([test_dist])[0], 
                le_cat.transform([test_cat])[0]
            ]], columns=['Month', 'District_Encoded', 'Category_Encoded'])
            
            prob = clf.predict_proba(input_d)[0][1]
            st.metric("Tỷ lệ án Heinous", f"{prob*100:.1f}%")
        
        with c2:
            st.write("**Logic đưa ra quyết định:**")
            fig_tree, ax = plt.subplots(figsize=(10, 6))
            plot_tree(clf, feature_names=['Tháng', 'Quận', 'Loại tội'], class_names=['BT', 'Nghiêm trọng'], filled=True, ax=ax)
            st.pyplot(fig_tree)

    # ------------------------------------------------------------------
    # TAB 3: PHÂN CỤM ĐỊA LÝ (DBSCAN) - Tạm ẩn để sửa lỗi
    # ------------------------------------------------------------------
    # with tab3:
    #     st.subheader("Phân tích Cụm tội phạm Không gian (DBSCAN)")
    #     ...
        st.info("💡 **Giải thích:** Các điểm cùng màu thuộc về cùng một cụm mật độ. Các điểm màu xám là các vụ án đơn lẻ (nhiễu). Bản đồ này giúp xác định các 'ổ nhóm' tội phạm thực tế ngoài đời thực.")

if __name__ == "__main__":
    advanced_analytics()
