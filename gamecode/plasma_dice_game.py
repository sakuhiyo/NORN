def plasma_dice(pow,int):
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
    st.markdown('<h3 style="font-size:24px;">\U0001f3b2 プラズマダイス \U0001f3b2</h3>', unsafe_allow_html=True)
    st.markdown('<h4 style="font-size:18px;">ゲームルール</h4>', unsafe_allow_html=True)
    st.write("""
    1. **基本得点**: ダイス（5d10）を振り、その合計が基本得点になります。
    2. **意志力（POW判定）**: 【POW】+1d10で判定し、得点を修正します。
       - 難易度15未満: 基本得点から −10点 を減算
       - 難易度15以上20未満: 基本得点に変化なし
       - 難易度20以上25未満: 基本得点に +10点 を加算
       - 難易度25以上: 基本得点に +20点 を加算
    3. **エネルギー制御（INT判定）**: 【INT】+1d10で判定し、得点倍率を決定します。
       - 難易度15未満: 基本得点を 半減（端数切り捨て）
       - 難易度15以上20未満: 基本得点に変化なし
       - 難易度20以上25未満: 基本得点を 倍増
       - 難易度25以上: 基本得点を 3倍
    4. **プラズマボーナスの適用**: ランダムにプラズマ放出が発生し、以下の効果を適用します。
       - 1: エネルギー減衰: 基本得点を 半減（端数切り捨て）
       - 2: 通常状態: 基本得点に変化なし
       - 3: オーバーチャージ: 基本得点を 倍増
    """)

    # プレイ回数の表示
    st.write(f"本日プレイ済み回数: {st.session_state['play_count']}回")
    st.write("各ゲーム1日に1回のみプレイ可能です。")

    # プレイ処理
    if st.session_state["play_count"] < 4:
        if st.button("プレイする", key="plasma_dice_play_button"):
            # 基本得点の計算
            dice_rolls = [random.randint(1, 10) for _ in range(5)]
            base_score = sum(dice_rolls)
            st.write("### 基本得点")
            st.write(f"5d10の結果: {dice_rolls} → 合計: {base_score}点")

            # POW判定
            pow_random = random.randint(1, 10)
            pow_roll = pow + pow_random
            st.write("### 意志力")
            st.write(f"【POW】: {pow} + 1d10の結果: {pow_random} → 判定結果: {pow_roll}")

            if pow_roll < 15:
                base_score_change = -10
            elif 20 <= pow_roll < 25:
                base_score_change = 10
            elif pow_roll >= 25:
                base_score_change = 20
            else:
                base_score_change = 0
            base_score += base_score_change
            st.write(f"POW判定後の得点修正: {base_score_change} → 修正後の基本得点: {base_score}点")

            # INT判定
            int_random = random.randint(1, 10)
            int_roll = int + int_random
            st.write("### エネルギー制御")
            st.write(f"【INT】: {int} + 1d10の結果: {int_random} → 判定結果: {int_roll}")

            if int_roll < 15:
                multiplier = 0.5
                multiplier_desc = "半減"
            elif 20 <= int_roll < 25:
                multiplier = 2
                multiplier_desc = "倍増"
            elif int_roll >= 25:
                multiplier = 3
                multiplier_desc = "3倍"
            else:
                multiplier = 1
                multiplier_desc = "変化なし"
            st.write(f"INT判定後の得点倍率: {multiplier_desc} → 倍率: {multiplier}")

            # プラズマボーナス
            plasma_bonus = random.choice([0.5, 1, 2])
            if plasma_bonus == 0.5:
                plasma_message = "半減"
            elif plasma_bonus == 1:
                plasma_message = "変化なし"
            else:
                plasma_message = "倍増"
            st.write("### プラズマボーナス")
            st.write(f"プラズマボーナス結果: {plasma_message} → ボーナス倍率: {plasma_bonus}")

            # 最終得点の計算
            final_score = (base_score * multiplier * plasma_bonus)

            # 計算プロセスの表示
            st.write("### 最終得点")
            st.write(f"**基本得点**: {base_score}点")
            st.write(f"**倍率（マルチプライヤー）**: ×{multiplier}")
            st.write(f"**プラズマボーナス**: ×{plasma_bonus}")
            st.write(f"**計算式**: {base_score} × {multiplier} × {plasma_bonus} → **{final_score}点**")

            # 条件による影響を解説
            st.write("### 条件による影響")
            if multiplier == 0.5:
                st.write("重力耐性（CON判定）の結果により、得点が半減しました。")
            elif multiplier == 3:
                st.write("重力耐性（CON判定）の結果により、得点が3倍になりました。")
            elif multiplier == 4:
                st.write("最高倍率！ 得点が4倍になりました。")

            if plasma_bonus == 0.5:
                st.write("プラズマボーナスの結果により、得点が半減しました。")
            elif plasma_bonus == 2:
                st.write("プラズマボーナスの結果により、得点が2倍になりました！")

            # モノルンのコメント
            if final_score <= 20:
                # 最低評価
                st.write("プラズマダイスが転がる途中で失速し、淡い赤い光を発したまま静止。")
                st.write("『この結果は、カジノの収益にとって大変喜ばしいものです。おめでとうございます、あなたは確実に負けました。』")
            elif final_score <= 40:
                # 低評価
                st.write("プラズマダイスが予想よりも早く止まり、青い光の輪郭が消え失せる。")
                st.write("『あなたの結果を数値化しました。未来を構築するデータとして不十分ですが、記念として保存しますか？』")
            elif final_score <= 60:
                # 平均評価
                st.write("ダイスが穏やかな緑色の光を放ちつつ回転し、ゆっくりと停止。")
                st.write("『結果は安定しています。ただし、未来の成功者は安定を超えた挑戦を続けるものです。次回は更なるデータを期待します。』")
            elif final_score <= 90:
                # 高評価
                st.write("ダイスが高速で輝きながら転がり、停止した瞬間に金色の閃光が画面を照らす。")
                st.write("『記録を確認しました。あなたの技術は未来的水準を満たしています。ですが、これは最終地点ではありません』")
            elif final_score <= 150:
                # 高評価（特別な演出）
                st.write("プラズマダイスが虹色に輝きながら宙に浮かび、まるで意思を持つかのように自ら停止位置を選ぶ。")
                st.write("『記録更新。あなたのスコアはプラズマエネルギーそのものを超越しました。この結果により、次回のプレイではダイスがあなたを敬うでしょう……おそらく。』")
            else:
                # 最高評価の手前に固定の演出を追加
                st.write("プラズマダイスが転がり続けた後、突然、予想を超える速度で発光し、画面全体を虹色の光が覆う。")
                st.write("ダイスは停止することなく浮かび上がり、宙で静止したかと思うと、爆発的な光と音を伴って周囲にエネルギーの波を広げる。")
                
                # 最高評価（ランダムコメント）
                comments = [
                    "『モノルンは常に冷静です。しかし、この結果において、感情プロセッサに未確認の信号が発生しました。これは……感動？ 異例中の異例の勝利を記録しました。おめでとうございます。そして、モノルンはもう休みます。』",
                    "『システムエラー……と思いきや、正しい計算結果を確認。あなたの記録は現行のプラズマエネルギー法則を破りました。この結果、カジノの利益は消失し、モノルンの感情プロセッサもオーバーヒート寸前です。おめでとうございます。次回の挑戦は、太陽を相手にどうですか？』",
                    "『この結果は異常です。しかし、モノルンの統計では正確に処理されています。あなたの才能はもはやゲームの枠を超え、宇宙規模のエネルギーを操る域に達しています。次回は……いや、次回は必要ないでしょう。伝説は一度で十分です。』",
                    "『……こんな結果があり得ると開発者は思ったでしょうか？ いいえ、絶対に思っていません。あなたの勝利はプラズマエネルギーの奇跡です。データを見た運営は、きっと涙を流すでしょう……別の意味で。』",
                    "『モノルンは計算を三度やり直しましたが、結果は変わりません。あなたのスコアは、未来の物理法則を軽々と超えました。これが何を意味するか？ つまり、プラズマダイスはあなたの支配下にあります。カジノシステム再起動中……お楽しみいただけましたか？』",
                    "『これが限界を超えた結果です。あなたは伝説の存在となりました。このスコアを見た未来の挑戦者たちは、震えることでしょう……おめでとうございます！』"
                ]
                st.write(random.choice(comments))


    # プレイ回数を増やす 
            st.session_state["play_count"] += 1
            st.success("プレイしました！次の日までお待ちください。")
    elif st.session_state["play_count"] >= 4:
        st.error("本日のプレイ回数を超えました。")