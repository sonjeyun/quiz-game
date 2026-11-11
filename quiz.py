def show_menu():
    while True:
        print("\n===== 퀴즈 게임 =====")
        print("1. 퀴즈 시작")
        print("2. 종료")

        choice = get_number("선택: ", 1, 2)   # ✅ 함수 재사용!

        if choice == 1:
            quiz_list = load_quiz()
            play_quiz(quiz_list)
        elif choice == 2:
            print("게임을 종료합니다. 안녕히 가세요! 👋")
            break
        else:                      # ④ 그 외 → 잘못된 입력
            print("⚠️ 잘못된 입력이에요. 1 또는 2를 입력해주세요!")
def get_number(prompt, min_val, max_val):
    while True:                          # 올바른 입력까지 반복
        value = input(prompt).strip()    # 앞뒤 공백 제거

        if value == "":                  # 빈 입력(그냥 Enter)
            print("⚠️ 입력이 비어있어요. 다시 입력해주세요.")
            continue

        if not value.isdigit():          # abc 같은 숫자 아님
            print("⚠️ 숫자만 입력해주세요.")
            continue

        number = int(value)              # 숫자로 변환
        if number < min_val or number > max_val:   # 범위 밖
            print(f"⚠️ {min_val}~{max_val} 사이로 입력해주세요.")
            continue

        return number                    # 모든 검사 통과!
import json  # 파일 읽기용 (맨 윗줄에 둬도 됨)
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self):
        print(f"\n{self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def check(self, user_number):
        return user_number == self.answer
# 기본 퀴즈 데이터 (파일 없을 때 사용)
DEFAULT_QUIZ = [
    Quiz("대한민국의 수도는?", ["서울", "부산", "대구", "인천"], 1),
    Quiz("1 + 1 = ?", ["1", "2", "3", "4"], 2),
    Quiz("무지개는 몇 가지 색?", ["5", "6", "7", "8"], 3),
]

def load_quiz():
    try:
        with open("quiz_data.json", "r", encoding="utf-8") as f:
            return json.load(f)          # 파일 읽기 성공
    except FileNotFoundError:             # 파일이 없을 때
        print("📂 파일이 없어 기본 퀴즈를 사용합니다.")
        return DEFAULT_QUIZ
    except json.JSONDecodeError:          # 파일이 손상됐을 때
        print("⚠️ 파일이 손상되어 기본 퀴즈로 복구합니다.")
        return DEFAULT_QUIZ

def play_quiz(quiz_list):
    score = 0
    total = len(quiz_list)

    print("\n===== 퀴즈 시작! =====")
    for i, quiz in enumerate(quiz_list, 1):   # quiz는 Quiz 객체!
        print(f"\n[{i}번 문제]")
        quiz.show()                            # 👈 show() 메서드 사용!

        user_number = get_number("답(번호): ", 1, 4)   # 👈 번호로 입력받기!

        if quiz.check(user_number):            # 👈 check() 메서드 사용!
            print("⭕ 정답입니다!")
            score += 1
        else:
            print(f"❌ 틀렸어요. 정답은 {quiz.answer}번")

    print(f"\n===== 결과: {total}문제 중 {score}개 정답! =====")
    return score
if __name__ == "__main__":
    try:
        show_menu()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 프로그램을 안전하게 종료합니다. 👋")          # ✅ 메뉴부터 시작!