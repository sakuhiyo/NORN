import streamlit as st
import os
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
import os
os.environ["STREAMLIT_UI_HIDE_TOP_BAR"] = "true"
from darts_shooting_game import darts_shooting
from gravity_roulette_game import gravity_roulette
from hologram_slot_game import hologram_slot
from plasma_dice_game import plasma_dice

st.markdown("""
    <style>
    body {
        font-family: 'Yu Gothic', '游ゴシック', sans-serif; /* 游ゴシックを指定 */
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Yu Gothic', '游ゴシック', sans-serif; /* 見出しも游ゴシックに変更 */
    }
    </style>
""", unsafe_allow_html=True)

# GitHubの画像URL（変換後）
background_image_url = "https://raw.githubusercontent.com/sakuhiyo/my-images/main/casino_test3.png"
image_url = "https://raw.githubusercontent.com/sakuhiyo/my-images/main/logo.png"

# 背景画像をCSSで適用
st.markdown(f"""
    <style>
    .stApp {{
        background: url({background_image_url});
        background-size: cover; /* 背景画像を画面全体に表示 */
        background-position: center; /* 背景画像を中央に配置 */
        background-repeat: no-repeat; /* 背景画像を繰り返さない */
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <style>
    .title-image {{
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 400px; /* 画像の幅を調整 */
        margin-top: -10px; /* 上部の余白を削減 */
        margin-bottom: -50px;   /* 下方向の余白 */
    }}
    </style>
    <img src="{image_url}" class="title-image">
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* タブのスタイル */
    .stTabs button {
        font-weight: bold;
        border: 2px solid #4e454a; /* ノブの枠線色 */
        background-color: rgba(255, 255, 255, 0.5); /* 半透明の白 */
        color: #573528;
        # background-color: #2E8B57;
        border-radius: 5px;
        padding: 5px 10px;
    }
    .stTabs button:hover {
        color: #FFD700;
        background-color: #b35e3c;
    }
    .stTabs button[data-selected="true"] {
        color: #FFD700;
        background-color: #1E5631;
    }
    <style>
    /* スライダー全体の背景色変更 */
    .stSlider > div[data-baseweb="slider"] > div {
        background: linear-gradient(to right, #4CAF50, #8BC34A); /* 動いている部分の色 */
    }
    /* スライダーのノブ（つまみ）の色 */
    .stSlider > div[data-baseweb="slider"] > div > div {
        background-color: #ede4c7; /* ノブの色 */
        border: 2px solid #4e454a; /* ノブの枠線色 */
        padding:2px;
        border-radius: 10px;
    }
""", unsafe_allow_html=True)

def main():

    st.markdown("""
    <style>
        .sidebar .slider-label {
            color: #FFD700;
            font-size: 18px;
            font-weight: bold;
        }
        .stTabs > div {
            background-color: rgba(255, 255, 255, 0.8); /* 半透明の白 */
            color: #573528;
            # background-color: #192f60; /* プルシャンブルー */
            # color: #e6cf8a; /* 金 */
            
            padding:30px;
            border-radius: 20px;
        }
    </style>
""", unsafe_allow_html=True)
    
    # ステータス入力セクション
    st.sidebar.markdown(
        """
        <div style="
        background-color: #ede4c7;
        color: #573528;
        padding: 2px 10px 0px 10px;
        margin-bottom: 30px;
        border: 2px solid #4e454a;
        border-radius: 40px; /*丸くする*/
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);">
        <h3 style="text-align: center; font-size: 15px; margin: 0;">ステータス入力</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            color: #573528;
            background-color: #b5b5ae; /*プルシャンブルー*/
            padding: 0px; /* サイドバー内の余白を調整 */
            border-right: 3px solid #4e454a; /* サイドバーの右側にチャコールグレイの枠線を追加 */
            box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1); /* サイドバーに影を追加 */
        }
        </style>
    """, unsafe_allow_html=True)

    # ステータス入力欄
    with st.sidebar:
        st.markdown(
            """
            <style>
            .slider-label {
                background-color: #ede4c7; /* クリーム */
                border-radius: 20px; /*丸くする*/
                border: 2px solid #4e454a; /* ノブの枠線色 */
                font-size: 16px; /* フォントを大きくする */
                font-weight: bold;
                margin-bottom: 3px; /* スライダー上の余白を縮める */
            }
            .stSlider {
                margin-top: -20px; /* スライダー上部の余白を削減 */
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="slider-label"> 　　　　　　💪 STR 💪</div>', unsafe_allow_html=True)
        str_value = st.slider("", min_value=3, max_value=18, value=10, key="str_slider")
        
        st.markdown('<div class="slider-label"> 　　　　　　🛡 CON 🛡</div>', unsafe_allow_html=True)
        con_value = st.slider("", min_value=3, max_value=18, value=10, key="con_slider")
        
        st.markdown('<div class="slider-label"> 　　　　　　⚡ SPD ⚡</div>', unsafe_allow_html=True)
        spd_value = st.slider("", min_value=3, max_value=18, value=10, key="spd_slider")
        
        st.markdown('<div class="slider-label"> 　　　　　　🎯 DEX 🎯</div>', unsafe_allow_html=True)
        dex_value = st.slider("", min_value=3, max_value=18, value=10, key="dex_slider")
        
        st.markdown('<div class="slider-label"> 　　　　　　🔥 POW 🔥</div>', unsafe_allow_html=True)
        pow_value = st.slider("", min_value=3, max_value=18, value=10, key="pow_slider")
        
        st.markdown('<div class="slider-label"> 　　　　　　🧠 INT 🧠</div>', unsafe_allow_html=True)
        int_value = st.slider("", min_value=3, max_value=18, value=10, key="int_slider")

    # ゲームのタブ切り替え
    tabs = st.tabs([
        "ダーツシューティング",
        "グラビティルーレット",
        "ホログラムスロット",
        "プラズマダイス",
    ])

    with tabs[0]:
        darts_shooting(dex_value, spd_value)

    with tabs[1]:
        gravity_roulette(str_value, con_value)

    with tabs[2]:
        hologram_slot(dex_value, pow_value)

    with tabs[3]:
        plasma_dice(pow_value, int_value)

if __name__ == "__main__":
    main()
