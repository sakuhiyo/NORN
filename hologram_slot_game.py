def hologram_slot(dex, pow_stat):
    import streamlit as st
    from datetime import datetime, timezone, timedelta
    import random

        # 日付システム（日本時間）
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

        # スロット出目に対応する絵文字
    slot_emojis = {
            1: "🪐",  # 惑星
            2: "🚀",  # ロケット
            3: "🌟",  # 星
            4: "🛸",  # UFO
            5: "💎",  # ダイヤモンド
            6: "🌌",  # 銀河
    }

    # ゲームルールの表示
    st.markdown("""
        <div style="text-align: center;">
        <h3 style="font-size:20px;">🔮 ホログラムスロット 🔮</h3>
        </div>
	""", unsafe_allow_html=True)
    st.markdown('<h4 style="font-size:16px;">ゲームルール</h4>', unsafe_allow_html=True)
    st.write("""
    1. **スロット出目**: スロット（3d6）を止めて出目（絵柄）に応じた得点を計算します。  
       - 出目の絵柄に応じて初期合計が計算されます
       - （例: 出目 🪐(1) | 🌟(3) | 🌌(6) → 合計 10点）。
    2. **目押し判定（DEX）**  
       - 【DEX】+1d10で目押しを判定し、成功に応じて出目を変更できます。  
       - 難易度15: 出目1つを変更（ゾロ目優先）。  
       - 難易度20: 出目2つを変更（ゾロ目優先）。  
       - 難易度25: 出目3つを変更（ゾロ目確定）。
    3. **ゾロ目ボーナス**  
        - すべて同じ出目（ゾロ目）の場合、合計得点が**2倍**になり+10点のボーナスが加算されます。
    4. **精神集中判定（POW）**  
       - 【POW】+1d10で判定を行い、最終得点に倍率を適用します。  
       - 難易度20: 最終得点×2  
       - 難易度25: 最終得点×3
        5. **得点計算式**  
       - 最終得点 = (ゾロ目ボーナス適用後の得点) × POW判定倍率
        """)

        # プレイ回数の表示
    st.write(f"本日プレイ済み回数: {st.session_state['play_count']}回")
    st.write("各ゲーム1日に1回のみプレイ可能です。")

        # プレイ処理
    if st.session_state["play_count"] < 4 and st.button("プレイする", key="hologram_slot_play_button"):
            # スロットの初期出目を決定
            slot_rolls = [random.randint(1, 6) for _ in range(3)]  # スロット出目
            
            # 絵文字で出目を表示
            st.subheader("スロットの結果")
            slot_emoji_display = " | ".join([slot_emojis[roll] for roll in slot_rolls])
            st.write(f"結果: {slot_emoji_display}")
            st.write(f"初期合計: {sum(slot_rolls)}")
            
            # 目押し（DEX判定）
            dex_roll = random.randint(1, 10)
            dex_total = dex + dex_roll
            st.write(f"目押し判定（DEX判定）: {dex} + 1d10({dex_roll}) → {dex_total}")
            
            # 目押しによる出目変更（ゾロ目優先＋高得点優先）
            changeable = 0
            if dex_total >= 15 and dex_total < 20:
                changeable = 1
            elif dex_total >= 20 and dex_total < 25:
                changeable = 2
            elif dex_total >= 25:
                # 強制最大ゾロ目
                slot_rolls = [6, 6, 6]
                st.write(f"目押し反映後: {' | '.join([slot_emojis[roll] for roll in slot_rolls])} → 合計: {sum(slot_rolls)}")
            if 0 < changeable < 3:
                candidates = []
                for t in range(1, 7):
                    count = slot_rolls.count(t)
                    needed = 3 - count
                    if needed <= changeable:
                        candidates.append((t, needed))
                if candidates:
                    best_target = max(candidates, key=lambda x: x[0])  # 値の大きいゾロ目を優先
                    slot_rolls = [best_target[0]] * 3
                st.write(f"目押し反映後: {' | '.join([slot_emojis[roll] for roll in slot_rolls])} → 合計: {sum(slot_rolls)}")
                        
            # ゾロ目ボーナス判定
            if len(set(slot_rolls)) == 1:
                base_score = sum(slot_rolls) * 2 + 10
                st.write("✨ ゾロ目ボーナス適用！得点が倍増し +10 点加算！ ✨")
            else:
                base_score = sum(slot_rolls)
            
            # 【POW】判定: 精神集中
            pow_roll = random.randint(1, 10)
            pow_total = pow_stat + pow_roll
            st.write(f"精神集中判定（POW判定）: {pow_stat} + 1d10({pow_roll}) → {pow_total}")
            
            # POW判定による倍率適用
            multiplier = 1
            if pow_total >= 20 and pow_total < 25:
                multiplier = 2
            elif pow_total >= 25:
                multiplier = 3
            final_score = base_score * multiplier
            
            st.write(f"得点計算式: {' + '.join(map(str, slot_rolls))} → {base_score}点 → ×{multiplier}倍")
            
            st.subheader("🎰 最終結果 🎰")
            st.write(f"最終得点: **{final_score}点**")
            
            # モノルンのコメント
            if final_score <= 20:
                st.write("スロットが停止し、全絵柄が消え画面が暗転。赤いエラーメッセージが点滅し、遠くで警告音が鳴り響く。")
                st.write("『モノルンは冷静にお伝えします。この結果は統計データに残す価値がありません。お疲れさまでした。』")
            elif final_score <= 40:
                st.write("スロットがゆっくり止まる。散らばった惑星と破損した宇宙船。青い光が微かに揺れ、失敗を示す電子音が響いた。")
                st.write("『結果確認完了。スコアは低空飛行、宇宙船は墜落、惑星は崩壊。モノルンとしては期待値未満の結果に軽く失望しています。』")
            elif final_score <= 60:
                st.write("スロットが回転を止めると、ホログラムに輝く惑星と宇宙船が並び現れる。穏やかな背景音楽が流れ始めた。")
                st.write("『スロットの停止を確認。統計的には無難なスコアですが、銀河の片隅でひっそりと輝く星のような控えめな結果です。』")
            elif final_score <= 90:
                st.write("スロットが停止と同時に、クリスタルが爆発的な輝きを放つ。画面は金色に染まり、華やかな音楽が高鳴る。")
                st.write("『金色の光、華やかな音楽、そして高得点。あなたのスコアは立派ですが、モノルンのデータベースはまだ上位の空席を確認しています。』")
            else:
                st.write("絵柄が宇宙船の大艦隊に変化し、艦隊が一斉に発光する。虹色のオーロラが背景を包み込み、壮麗な光景が広がった。")
                st.write("『艦隊の輝きは美しいですが、あなたのスコアはさらにそれを超える壮麗さです。モノルンはこれ以上の言葉を見つけられません……珍しいことです。』")
            
            # プレイ回数を増やす
            st.session_state["play_count"] += 1
            st.success("プレイしました！次の日までお待ちください。")
    elif st.session_state["play_count"] >= 4:
            st.error("本日のプレイ回数を超えました。")

    # Streamlitアプリとして実行
    if __name__ == "__main__":
        hologram_slot()
