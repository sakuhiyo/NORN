def gravity_roulette(str, con):
    import streamlit as st
    from datetime import datetime, timezone, timedelta
    import random

    # 日付システム
    JST = timezone(timedelta(hours=9))
    today = datetime.now(JST).date()

    # セッション状態で日付とプレイ回数を保持
    if "last_play_date" not in st.session_state:
        st.session_state["last_play_date"] = None
        st.session_state["play_count"] = 0

    # 日付が変わった場合にリセット
    if st.session_state["last_play_date"] != today:
        st.session_state["last_play_date"] = today
        st.session_state["play_count"] = 0

    # ゲームルールの表示
    st.markdown("""
        <div style="text-align: center;">
        <h3 style="font-size:20px;">⚙ グラビティルーレット ⚙</h3>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<h4 style="font-size:16px;">ゲームルール</h4>', unsafe_allow_html=True)
    st.write("""
    1. **基本得点**: ダイス（3d6）を振り、合計が基本得点になります。  
    2. **重力フィールドボーナス**: ランダムに決定されるフィールド効果に応じて得点を修正。  
       - 無重力: 基本得点に +10点  
       - 高重力: ボーナスなし  
    3. **パワーコントロール（STR判定）**: 【STR】+1d10で判定し、基本得点に加点します。  
       - 難易度15: +5点  
       - 難易度20: +10点  
       - 難易度25: +20点  
    4. **重力耐性（CON判定）**: 【CON】+1d10で判定し、得点倍率を決定します。  
       - 難易度15: ×2  
       - 難易度20: ×3  
       - 難易度25: ×4  
    """)

    # プレイ回数の表示
    st.write(f"本日プレイ済み回数: {st.session_state['play_count']}回")
    st.write("各ゲーム1日に1回のみプレイ可能です。")

    # プレイ処理
    if st.session_state["play_count"] < 4 and st.button("プレイする", key="gravity_roulette_play_button"):
        # 重力フィールドボーナスの決定
        gravity_state = random.randint(1, 2)  # 1: 無重力, 2: 高重力
        if gravity_state == 1:
            gravity_bonus = 10  # 無重力ボーナス
            gravity_message = "無重力フィールド: 基本得点に +10点 のボーナスを適用。"
        else:
            gravity_bonus = 0  # 高重力ではボーナスなし
            gravity_message = "高重力フィールド: 特別なボーナスはありません。"

        st.write(f"重力フィールド: {'無重力' if gravity_state == 1 else '高重力'}")
        st.write(gravity_message)

        # 基本得点の計算
        # 修正後
        dice_rolls = [random.randint(1, 6) for _ in range(3)]
        dice_total = sum(dice_rolls)
        base_score = dice_total + gravity_bonus
        st.subheader("⚙️ 結果")
        st.write(f"3d6の出目: {dice_rolls} → 合計: {dice_total}点")
        if gravity_bonus > 0:
            st.write(f"無重力ボーナス: +{gravity_bonus}点")
        st.write(f"基本得点（ボーナス込み）: {base_score}点")

        # STR判定
        str_random = random.randint(1, 10)  # 1d10の結果
        str_roll = str + str_random
        st.write(f"パワーコントロール（STR判定）: {str} + 1d10({str_random}) → {str_roll}")
        if str_roll >= 15 and str_roll < 20:
            base_score += 5
        elif str_roll >= 20 and str_roll < 25:
            base_score += 10
        elif str_roll >= 25:
            base_score += 20

        st.write(f"STR判定後の得点: {base_score}点")

        # CON判定
        con_random = random.randint(1, 10)  # 1d10の結果
        con_roll = con + con_random
        multiplier = 1
        if con_roll >= 15:
            multiplier = 2
        if con_roll >= 20:
            multiplier = 3
        if con_roll >= 25:
            multiplier = 4
        st.write(f"重力耐性（CON判定）: {con} + 1d10({con_random}) → {con_roll} → 倍率: ×{multiplier}")

        # 最終得点計算
        final_score = base_score * multiplier
        st.write(f"最終得点: **{final_score}点**")

        # モノルンのコメント
        if final_score <= 20:
            st.write("赤い警告灯が画面を点滅させ、ルーレット盤が異常な低速で停止した。")
            st.write("『深刻なエラー。ルーレットは回転しましたが、あなたのスコアは一向に上昇しませんでした。重力の責任ではなく、プレイヤーの責任です。』")
        elif final_score <= 40:
            st.write("青い光が画面を横切り、無重力モードのルーレットが規則的に停止する。")
            st.write("『状況分析: プレイヤーの動きは確認されましたが、結果は微妙です。次回、ルーレットにお祈りするのはいかがですか？』")
        elif final_score <= 60:
            st.write("淡い緑色のライトが画面を包み、高重力モードでの安定した停止が映し出された。")
            st.write("『平均評価。重力制御は基準値内に収まっています。統計データ: 中位50%。安定したパフォーマンスを確認。』")
        elif final_score <= 90:
            st.write("金色の光がルーレット盤を照らし、盤面のスピンが優雅に減速して停止する。")
            st.write("『優秀なあなたへ。重力フィールドの操作に成功しました。次の挑戦では、“この程度”を超える結果を期待しています。』")
        else:
            st.write("虹色の光が画面全体を彩り、無重力モードでの完璧な停止を強調する演出が加わった。")
            st.write("『計算終了。あなたは重力そのものを凌駕しました。モノルンは祝賀パレードの準備を開始しましたが、あいにくカジノの設定にはその機能がありません。残念ですね？』")

        # プレイ回数を増やす
        st.session_state["play_count"] += 1
        st.success("プレイしました！次の日までお待ちください。")
    elif st.session_state["play_count"] >= 4:
        st.error("本日のプレイ回数を超えました。")