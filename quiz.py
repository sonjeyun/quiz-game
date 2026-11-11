def play_quiz(quiz_list):
    # ⚠️ 퀴즈가 없는 경우 처리
    if not quiz_list:
        print("\n⚠️ 출제할 퀴즈가 없어요! 😢")
        return 0

    score = 0
    total = len(quiz_list)
def show_menu():
    while True:
        print("\n===== 퀴즈 게임 =====")
        print("1. 퀴즈 시작")
        print("2. 퀴즈 추가")          # 👈 추가!
        print("3. 종료")               # 👈 번호 변경!

        choice = get_number("선택: ", 1, 3)   # 👈 2를 3으로!

        if choice == 1:
            quiz_list = load_quiz()
            play_quiz(quiz_list)
        elif choice == 2:              # 👈 추가!
            add_quiz()
        elif choice == 3:              # 👈 번호 변경!
            print("게임을 종료합니다. 안녕히 가세요! 👋")
            break
        else:
            print("⚠️ 잘못된 입력이에요.")
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
    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @staticmethod
    def from_dict(data):
        return Quiz(data["question"], data["choices"], data["answer"])
    
# 기본 퀴즈 데이터 (파일 없을 때 사용)
# 기본 퀴즈 데이터 (파일 없을 때 사용)
DEFAULT_QUIZ = [
    Quiz("대한민국의 수도는?", ["부산", "서울", "인천", "대구"], 2),
    Quiz("지구에서 가장 큰 대양은?", ["대서양", "인도양", "태평양", "북극해"], 3),
    Quiz("1년은 며칠인가요?", ["360일", "365일", "366일", "370일"], 2),
    Quiz("물의 화학 기호는?", ["CO2", "O2", "H2O", "NaCl"], 3),
    Quiz("무지개 색깔은 몇 가지인가요?", ["5개", "6개", "7개", "8개"], 3),
]

def load_quiz():
    try:
        with open("quiz_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Quiz.from_dict(d) for d in data]   # 👈 변경!
            return [Quiz.from_dict(item) for item in data]  # 파일 읽기 성공
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
def save_quiz(quiz_list):
    data = [quiz.to_dict() for quiz in quiz_list]
    with open("quiz_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_quiz():
    print("\n===== 새 퀴즈 추가 =====")
    while True:
        question = input("문제를 입력하세요: ").strip()
        if question == "":
            print("⚠️ 문제가 비어있어요. 다시 입력해주세요.")
            continue
        break
    choices = []
    for i in range(1, 5):
        while True:
            choice = input(f"{i}번 선택지: ").strip()
            if choice == "":
                print("⚠️ 선택지가 비어있어요. 다시 입력해주세요.")
                continue
            break
        choices.append(choice)
    answer = get_number("정답 번호(1~4): ", 1, 4)
    new_quiz = Quiz(question, choices, answer)
    quiz_list = load_quiz()
    quiz_list.append(new_quiz)
    save_quiz(quiz_list)
    print("✅ 퀴즈가 추가되었어요! 😄")
if __name__ == "__main__":
    try:
        show_menu()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 프로그램을 안전하게 종료합니다. 👋")          # ✅ 메뉴부터 시작!