import random
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def run_simulation(n_iters):
    old_stones_list = np.zeros(n_iters, dtype=int)
    new_stones_list = np.zeros(n_iters, dtype=int)
    old_first_stones_list = np.zeros(n_iters, dtype=int)
    new_first_stones_list = np.zeros(n_iters, dtype=int)

    for i in range(n_iters):
        stones = 0
        points = 0
        got_A = False
        got_B = False
        first_recorded_old = False

        while not (got_A and got_B):
            stones += 1200
            target_A_this_pull = not got_A
            
            for _ in range(10):
                points += 1
                if random.random() < 0.007:
                    if target_A_this_pull:
                        got_A = True
                    else:
                        got_B = True

            while points >= 200:
                if not got_A:
                    got_A = True
                    points -= 200
                elif not got_B:
                    got_B = True
                    points -= 200
                else:
                    break

            if (got_A or got_B) and not first_recorded_old:
                old_first_stones_list[i] = stones
                first_recorded_old = True

        old_stones_list[i] = stones

        stones_new = 0
        charge = 0
        total_pulls = 0
        tickets = 0
        got_A_new = False
        got_B_new = False
        first_recorded_new = False
        claimed_tickets = set()

        while not (got_A_new and got_B_new):
            if tickets > 0:
                tickets -= 1
            else:
                stones_new += 1200

            target_A_this_pull = not got_A_new

            for _ in range(10):
                total_pulls += 1
                charge += 1
                is_target = False

                if random.random() < 0.007:
                    is_target = True
                elif not is_target:
                    if charge == 200:
                        is_target = True
                    elif charge == 100:
                        if random.random() < 0.5:
                            is_target = True

                if is_target:
                    if target_A_this_pull:
                        got_A_new = True
                    else:
                        got_B_new = True
                    charge = 0

                if (got_A_new or got_B_new) and not first_recorded_new:
                    new_first_stones_list[i] = stones_new
                    first_recorded_new = True

            if total_pulls in (70, 130, 150, 170, 270, 330, 350, 370) and total_pulls not in claimed_tickets:
                tickets += 1
                claimed_tickets.add(total_pulls)

        new_stones_list[i] = stones_new

    return old_stones_list, new_stones_list, old_first_stones_list, new_first_stones_list

st.title("ガチャ必要石シミュレーション")
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)
n_iters = st.number_input("試行回数を入力してください", min_value=1, max_value=1000000, value=10000, step=1)

if st.button("シミュレーションを実行する"):
    with st.spinner("アロナが一生懸命計算しています...！"):
        old_data, new_data, old_first_stones, new_first_stones = run_simulation(n_iters)

        st.header("【2人目お迎え（コンプリート）までの消費石】")
        st.subheader("統計データ")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("--- 旧仕様 ---")
            st.write(f"平均: {np.mean(old_data):.1f} 個")
            st.write(f"中央値: {np.percentile(old_data, 50):.0f} 個")
            st.write(f"95%ile: {np.percentile(old_data, 95):.0f} 個")
            st.write(f"最大値: {np.max(old_data):.0f} 個")

        with col2:
            st.write("--- 新仕様 ---")
            st.write(f"平均: {np.mean(new_data):.1f} 個")
            st.write(f"中央値: {np.percentile(new_data, 50):.0f} 個")
            st.write(f"95%ile: {np.percentile(new_data, 95):.0f} 個")
            st.write(f"最大値: {np.max(new_data):.0f} 個")

        st.subheader("分布 (ヒストグラム)")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.hist(old_data, bins=50, alpha=0.5, label='Old Specs', color='cornflowerblue', density=True)
        ax1.hist(new_data, bins=50, alpha=0.5, label='New Specs', color='lightpink', density=True)
        ax1.set_xlabel('Consumed Pyroxenes (Stones)')
        ax1.set_ylabel('Probability Density')
        ax1.legend()
        ax1.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig1)

        st.subheader("散らばり (箱ひげ図)")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        bplot = ax2.boxplot([old_data, new_data], tick_labels=['Old Specs', 'New Specs'], patch_artist=True, medianprops=dict(color='red', linewidth=2))
        colors = ['cornflowerblue', 'lightpink']
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)
        ax2.set_ylabel('Consumed Pyroxenes (Stones)')
        ax2.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig2)

        st.subheader("累積分布 (CDF)")
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        x_old = np.sort(old_data)
        y_old = np.arange(1, len(x_old) + 1) / len(x_old)
        x_new = np.sort(new_data)
        y_new = np.arange(1, len(x_new) + 1) / len(x_new)
        ax3.plot(x_old, y_old, label='Old Specs', color='cornflowerblue', linewidth=2)
        ax3.plot(x_new, y_new, label='New Specs', color='lightpink', linewidth=2)
        ax3.set_xlabel('Consumed Pyroxenes (Stones)')
        ax3.set_ylabel('Cumulative Probability')
        ax3.legend()
        ax3.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig3)

        st.markdown("---")
        st.header("【1人目お迎え vs 2人目コンプリートの消費石関係】")
        
        diff_stones_old = old_data - old_first_stones
        diff_stones_new = new_data - new_first_stones
        
        st.subheader("1人目お迎えからの追加消費石")
        col3, col4 = st.columns(2)
        with col3:
            st.write("--- 旧仕様 ---")
            st.write(f"追加消費石 (平均): {np.mean(diff_stones_old):.1f} 個")
        with col4:
            st.write("--- 新仕様 ---")
            st.write(f"追加消費石 (平均): {np.mean(diff_stones_new):.1f} 個")

        # 試行回数に応じてドットの濃さと大きさを自動調整
        alpha_val = max(0.1, min(0.8, 500 / n_iters))
        size_val = max(10, min(50, 50000 / n_iters))

        st.subheader("1人目と合計の消費石分布 (散布図)")
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        ax5.scatter(old_first_stones, old_data, alpha=alpha_val, s=size_val, label='Old Specs', color='cornflowerblue')
        ax5.scatter(new_first_stones, new_data, alpha=alpha_val, s=size_val, label='New Specs', color='lightpink')
        
        # 先生ご指定の仮天井ライン（約10,800石）に赤色の「縦破線」を追加！
        ax5.axvline(x=10800, color='red', linestyle='--', linewidth=1.5, label='仮天井ライン (約10,800石)')

        ax5.set_xlabel('Consumed Pyroxenes for 1st Pickup (Stones)')
        ax5.set_ylabel('Total Consumed Pyroxenes for Both (Stones)')
        ax5.legend()
        ax5.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig5)

st.markdown("---")
st.markdown(
    """
    ### 💡 試行回数と計算方法について

    **試行回数とは？**
    ここで入力する試行回数は、「このガチャに挑戦するプレイヤーの人数」を意味します。例えば「10,000」と入力した場合、1万人分のシミュレーションを一気に行い、その結果の平均やバラつきをグラフにしています。試行回数が多いほど現実に近い正確なデータになりますが、計算には少し時間がかかります。

    **計算方法（シミュレーションのルール）**
    *   **目的:** ピックアップ生徒2人（生徒Aと生徒B）を両方お迎えするまでに「消費した青輝石の数」を計算しています。
    *   **旧仕様:** 1回0.7%の確率で抽選。200連（24,000石）ごとに、まだお迎えしていない生徒を確定で交換できます。
    *   **新仕様:** 1回0.7%の確率で抽選。100連到達時に50%の確率でピックアップ生徒を獲得（すり抜けあり）、200連到達時は確定で獲得。さらに、道中の特定の募集回数に到達すると、無料の10連チケットがもらえ、その分消費石を節約できます。
    """
)
