import json
from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="운동 성향 테스트 & 루틴 추천",
    page_icon="🏋️",
    layout="centered"
)

print(f"[SERVER LOG] App rerun at {datetime.now()}", flush=True)

@st.cache_data
def load_quiz_data():
    """퀴즈 문항 데이터 불러오기"""
    with open("quiz_data.json", "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_routine_data():
    """추천 루틴 데이터 불러오기"""
    with open("routine_data.json", "r", encoding="utf-8") as f:
        return json.load(f)


def try_login(user_id, password):
    """간단한 로그인 검증"""
    valid_users = {
        "student": "1234",
        "admin": "2020"
    }
    return user_id in valid_users and valid_users[user_id] == password


def determine_result(scores):
    """
    점수 비교 후 결과 유형 결정
    동점이거나 balance가 가장 높으면 균형 발달형으로 처리
    """
    upper = scores["upper"]
    lower = scores["lower"]
    balance = scores["balance"]

    max_score = max(upper, lower, balance)

    # 동점이 있으면 균형 발달형으로 처리
    max_count = sum(1 for value in scores.values() if value == max_score)
    if max_count >= 2:
        return "balance"

    if upper == max_score:
        return "upper"
    elif lower == max_score:
        return "lower"
    else:
        return "balance"


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🏋️ 운동 성향 테스트 & 간단 루틴 추천")
st.write("학번: **2020204044**")
st.write("이름: **배지운**")
st.markdown("---")

st.write("이 앱은 간단한 퀴즈를 통해 사용자의 운동 성향을 파악하고, 그에 맞는 간단한 루틴을 추천하는 Streamlit 기반 웹 애플리케이션입니다.")

if not st.session_state.logged_in:
    st.subheader("로그인")

    user_id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
    print(f"[SERVER LOG] Login button clicked. user_id={user_id}", flush=True)

    if try_login(user_id, password):
        print(f"[SERVER LOG] Login success. user_id={user_id}", flush=True)
        st.session_state.logged_in = True
        st.session_state.username = user_id
        st.success("로그인에 성공했습니다.")
        st.rerun()
    else:
        print(f"[SERVER LOG] Login failed. user_id={user_id}", flush=True)
        st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    st.info("테스트용 로그인 정보: 아이디 `student` / 비밀번호 `1234`")

else:
    st.success(f"{st.session_state.username}님, 로그인 상태입니다.")

    if st.button("로그아웃"):
    print(f"[SERVER LOG] Logout button clicked. user={st.session_state.username}", flush=True)
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

    st.markdown("---")

    quiz_data = load_quiz_data()
    routine_data = load_routine_data()

    st.subheader("운동 성향 퀴즈")
    st.caption("각 문항에서 가장 자신에게 가까운 답을 선택한 뒤, 아래의 결과 보기 버튼을 눌러 주세요.")

    scores = {
        "upper": 0,
        "lower": 0,
        "balance": 0
    }

    for idx, q in enumerate(quiz_data):
        st.markdown(f"### Q{idx + 1}. {q['question']}")

        option_texts = [option["text"] for option in q["options"]]

        selected = st.radio(
            "선택하세요.",
            options=option_texts,
            key=f"question_{idx}"
        )

        for option in q["options"]:
            if option["text"] == selected:
                scores[option["category"]] += 1

    if st.button("결과 보기"):
    print(f"[SERVER LOG] Result button clicked. scores={scores}", flush=True)

    result_key = determine_result(scores)
    result = routine_data[result_key]

    print(f"[SERVER LOG] Result determined. result_key={result_key}", flush=True)

        st.markdown("---")
        st.subheader("테스트 결과")
        st.success(f"당신의 운동 성향은 **{result['title']}** 입니다.")
        st.write(result["description"])

        st.markdown("### 추천 루틴")
        for idx, exercise in enumerate(result["routine"], start=1):
            st.write(f"{idx}. {exercise}")

        st.markdown("### 운동 팁")
        st.info(result["tip"])

        st.markdown("### 성향 점수")
        st.write(f"- 상체 집중형 점수: **{scores['upper']}**")
        st.write(f"- 하체 집중형 점수: **{scores['lower']}**")
        st.write(f"- 균형 발달형 점수: **{scores['balance']}**")

    st.markdown("---")
    st.caption("※ 퀴즈 문항과 추천 루틴 데이터는 JSON 파일에서 불러오며, Streamlit의 캐싱 기능(@st.cache_data)을 적용했습니다.")
