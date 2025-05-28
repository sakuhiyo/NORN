def darts_shooting(dex, spd):
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
# ゲームルールの表示
    st.markdown("""
    <div style="text-align: center;">
        <h3 style="font-size:20px;">🎯 ダーツシューティング 🎯</h3>
    </div>
""", unsafe_allow_html=True)
    st.markdown('<h4 style="font-size:16px;">ゲームルール</h4>', unsafe_allow_html=True)
    st.write("""
    1. **基本得点**: ダイス（1d6）を振って出目に応じた得点を計算します。  
       - 出目 1～2: 10点（シングル）  
       - 出目 3～4: 15点（ダブル）  
       - 出目 5～6: 20点（トリプル）  
       - 命中精度での昇格のみ: 30点（ブル）  
    2. **命中精度（DEX判定）**: 【DEX】+1d10で判定し、得点を追加/昇格します。  
       - 難易度15: 1段階昇格（例: シングル→ダブル、トリプル→ブル）  
       - 難易度20: 2段階昇格（例: シングル→ダブル→トリプル）  
       - 難易度25: 3段階昇格（例: シングル→ダブル→トリプル→ブル）  
       - 既にブル（30点）の場合、1段階につき+10点ずつ加点  
    3. **スピード（SPD判定）**: 【SPD】+1d10で判定し、得点倍率を決定します。  
       - 難易度15: ×2  
       - 難易度20: ×3  
       - 難易度25: ×5  
    4. **組み合わせボーナス**: 【DEX】と【SPD】の判定が両方20以上の場合、+10点。  
    """)

    # プレイ回数の表示
    st.write(f"本日プレイ済み回数: {st.session_state['play_count']}回")
    st.write("各ゲーム1日に1回のみプレイ可能です。")

    # プレイ処理
    if st.session_state["play_count"] < 4 and st.button("プレイする", key="darts_shooting_play_button"):
    # 基本得点の判定（出目に応じて階層を割り当て）
       base_roll = random.randint(1, 6)
    if base_roll <= 2:
        base_score = 10
        level = 0
        zone = "シングル"
    elif base_roll <= 4:
        base_score = 15
        level = 1
        zone = "ダブル"
    else:
        base_score = 20
        level = 2
        zone = "トリプル"

        # 基礎得点を表示
        st.subheader("🎯 結果")
        st.write(f"出目: {base_roll} → 基礎得点: {base_score}点（{zone}）")

        # DEX判定
        dex_random = random.randint(1, 10)
        dex_roll = dex + dex_random
        st.write(f"DEX判定: {dex} + 1d10({dex_random}) → {dex_roll}")

        # DEXによる昇格段階数の決定
        upgrade = 0
        if 15 <= dex_roll < 20:
            upgrade = 1
        elif 20 <= dex_roll < 25:
            upgrade = 2
        elif dex_roll >= 25:
            upgrade = 3

        # 昇格処理
        if level < 3:
            new_level = min(level + upgrade, 3)
            level = new_level
            base_score = [10, 15, 20, 30][level]
        else:
            # 既にブルの場合は+10点ずつ加算
            base_score += 10 * upgrade

        # レベルに応じたラベル
        zone_labels = ["シングル", "ダブル", "トリプル", "ブル"]
        zone = zone_labels[level]
        st.write(f"昇格後得点: {base_score}点（{zone}）")

        # 昇格後得点のラベル付け
        if base_score == 10:
            final_zone = "外周"
        elif base_score == 15:
            final_zone = "中間"
        elif base_score == 20 or base_score == 25:
            final_zone = "中心"
        elif base_score == 30:
            final_zone = "中心+"
        elif base_score == 40:
            final_zone = "中心++"
        else:
            final_zone = "不明"

        st.write(f"昇格後得点: {base_score}点（{final_zone}）")

        # SPD判定
        spd_random = random.randint(1, 10)  # 1d10の結果
        spd_roll = spd + spd_random
        multiplier = 1
        if spd_roll >= 15:
            multiplier = 2
        if spd_roll >= 20:
            multiplier = 3
        if spd_roll >= 25:
            multiplier = 5
        st.write(f"SPD判定: {spd} + 1d10({spd_random}) → {spd_roll} → 倍率: ×{multiplier}")

        # 組み合わせボーナス
        combo_bonus = 10 if dex_roll >= 20 and spd_roll >= 20 else 0
        st.write(f"組み合わせボーナス: +{combo_bonus}点")

        # 最終得点計算
        final_score = base_score * multiplier + combo_bonus
        st.write(f"最終得点: **{final_score}点**")

        # モノルンのコメント
        if final_score <= 20:
            st.write("ダーツがホログラムの的をかすめ、虚しく宙を舞う。的の赤い警告ライトが点滅し、機械的な「エラー」の声が響く。")
            st.write("『結果: 低得点ゾーン。再計算の必要性: 0%。この記録は、削除すべきでしょうか？』")
        elif final_score <= 40:
            st.write("ダーツが遅れて放たれ、ホログラムの的にかろうじて命中。青い光が一瞬だけ点滅し、静かに消えた。")
            st.write("『平均以下。あなたのスコアはデータベースの基準を下回っています。モノルンは努力を歓迎しますが、進展は確認されていません。』")
        elif final_score <= 60:
            st.write("動く的の中間にダーツがしっかり刺さる。緑色のライトが点灯し、心地よい音楽が短く流れた。")
            st.write("『結果: 安定したスコアです。ただし、モノルンの基準では“特別”とは言えません。未来の挑戦者として進化する可能性に期待しています。』")
        elif final_score <= 90:
            st.write("ダーツが高速で飛び、的の中心に寸分違わず命中。金色の光が的を包み、観客の歓声を再現する音が流れる。")
            st.write("『優秀な結果。あなたの成長曲線は非常に興味深いです。次も同様の結果を期待します。』")
        else:
            st.write("『驚異的なスコアです。モノルンはデータベースの書き換えを開始します。")
            st.write("おっと、書き換え速度が遅い？それもそのはず、こんな記録は予定外だったのですから！』")
            st.write("ホログラムダーツが完璧な軌道で命中する。虹色に光る画面、派手な演出と祝賀音楽の中で、モノルンは踊っていた。")

        # プレイ回数を増やす
        st.session_state["play_count"] += 1
        st.success("プレイしました！次の日までお待ちください。")
    elif st.session_state["play_count"] >= 4:
        st.error("本日のプレイ回数を超えました。")
