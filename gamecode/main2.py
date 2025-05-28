import streamlit as st
from darts_shooting_game import darts_shooting
from gravity_roulette_game import gravity_roulette
from hologram_slot_game import hologram_slot
from plasma_dice_game import plasma_dice

def main():
    st.title("🌃 カジノゲーム集 🌃")
    
    # ステータス入力
    st.sidebar.header("ステータス入力")
    str_value = st.sidebar.number_input("【STR】", min_value=3, max_value=18, value=10)
    con_value = st.sidebar.number_input("【CON】", min_value=3, max_value=18, value=10)
    spd_value = st.sidebar.number_input("【SPD】", min_value=3, max_value=18, value=10)
    dex_value = st.sidebar.number_input("【DEX】", min_value=3, max_value=18, value=10)
    pow_value = st.sidebar.number_input("【POW】", min_value=3, max_value=18, value=10)
    int_value = st.sidebar.number_input("【INT】", min_value=3, max_value=18, value=10)

    # ゲームのタブ切り替え
    tabs = st.tabs(["ダーツシューティング", "グラビティルーレット", "ホログラムスロット", "プラズマダイス"])
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
