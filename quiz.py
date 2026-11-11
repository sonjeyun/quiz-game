class QuizGame:
    def __init__(self):
        # 👇 한 번에 불러오기! (두 개를 동시에 받아요)
        self.quiz_list, self.best_score = load_state()

    def show_menu(self):
        print("\n===== 퀴즈 게임 =====")
        print("1. 퀴즈 시작")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 삭제") 
        print("4. 퀴즈 목록")
        print("5. 최고 점수")
        print("6. 종료")
    def show_list(self):                    # 👈 self 추가!
        if not self.quiz_list:              # 👈 self.quiz_list 사용!
            print("\n⚠️ 저장된 퀴즈가 없어요! 😢")
            return

        print("\n===== 퀴즈 목록 =====")
        print(f"총 {len(self.quiz_list)}개의 퀴즈가 있어요!\n")
        for i, quiz in enumerate(self.quiz_list, 1):   # 👈 self.quiz_list!
            print(f"{i}. {quiz.question}")
        print("====================")
    def add(self):                                  # 👈 self 추가!
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

        self.quiz_list.append(new_quiz)
        save_state(self.quiz_list, self.best_score)   # 👈 변경!
        print("✅ 퀴즈가 추가되었어요! 😄")
    def play(self):                              # 👈 self 추가!
        if not self.quiz_list:                   # 👈 빈 퀴즈 체크!
            print("\n⚠️ 출제할 퀴즈가 없어요! 😢")
            return

        score = 0
        print("\n===== 퀴즈 시작! =====")
        for i, quiz in enumerate(self.quiz_list, 1):   # 👈 self.quiz_list!
            print(f"\n[{i}번 문제]")
            quiz.show()

            user_number = get_number("답(번호): ", 1, 4)

            if quiz.check(user_number):
                print("⭕ 정답입니다!")
                score += 1
            else:
                print(f"❌ 틀렸어요. 정답은 {quiz.answer}번")

        # 👇 최고 점수와 비교! (self.best_score 사용!)
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            save_state(self.quiz_list, self.best_score)   # 👈 변경!
            print(f"\n🎉 새로운 최고 점수 달성! ({score}점)")
        else:
            print(f"\n현재 최고 점수: {self.best_score}점") 
    def delete_quiz(self):
        if not self.quiz_list:
            print("🗑️ 삭제할 퀴즈가 없습니다.")
            return

        print("\n===== 🗑️ 퀴즈 삭제 =====")
        for i, quiz in enumerate(self.quiz_list, 1):
            print(f"{i}. {quiz.question}")

        choice = get_number(
            f"삭제할 번호 (1~{len(self.quiz_list)}, 0=취소): ",
            0,
            len(self.quiz_list),
        )

        if choice == 0:
            print("↩️ 삭제를 취소했습니다.")
            return

        removed = self.quiz_list.pop(choice - 1)
        print(f"✅ '{removed.question}' 퀴즈를 삭제했습니다.")

        save_state(self.quiz_list, self.best_score)
    def run(self):                                   # 👈 게임 시작 메서드!
        while True:
            self.show_menu()                         # 👈 self. 붙여서 메뉴 출력!
            choice = get_number("선택: ", 1, 6)

            if choice == 1:
                self.play()                          
            elif choice == 2:
                self.add()
            elif choice == 3:
                self.delete_quiz()                            
            elif choice == 4:
                self.show_list()                     
            elif choice == 5:
                if self.best_score is None:         
                    print("\n⚠️ 아직 푼 퀴즈가 없어요! 먼저 풀어보세요! 😄")
                else:
                    print(f"\n🏆 최고 점수: {self.best_score}점")
            elif choice == 6:
                print("게임을 종료합니다. 안녕히 가세요! 👋")
                break       


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
    except FileNotFoundError:             # 파일이 없을 때
        print("📂 파일이 없어 기본 퀴즈를 사용합니다.")
        return DEFAULT_QUIZ
    except json.JSONDecodeError:          # 파일이 손상됐을 때
        print("⚠️ 파일이 손상되어 기본 퀴즈로 복구합니다.")
        return DEFAULT_QUIZ
def load_best_score():
    try:
        with open("best_score.txt", "r") as f:
            return int(f.read())    # 👈 파일에서 숫자 읽기
    except (FileNotFoundError, ValueError):
        return None                 # 👈 파일 없음 = 아직 안 풂!


def save_best_score(score):
    with open("best_score.txt", "w") as f:
        f.write(str(score))         # 👈 숫자를 글자로 바꿔서 저장

def save_quiz(quiz_list):
    data = [quiz.to_dict() for quiz in quiz_list]
    with open("quiz_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def save_state(quizzes, best_score):
    data = {
        "quizzes": [q.to_dict() for q in quizzes],  # 퀴즈를 dict로 변환
        "best_score": best_score
    }
    try:
        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:                        # 👈 파일 쓰기 오류 잡기
        print("저장에 실패했어요. 😢")      # 👈 사용자에게 안내
# 👇 state.json에서 퀴즈 + 점수를 한 번에 불러오기
def load_state():
    try:
        with open("state.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            quizzes = [Quiz.from_dict(d) for d in data["quizzes"]]
            best_score = data["best_score"]
            return quizzes, best_score
    except FileNotFoundError:
        print("📂 저장된 파일이 없어 기본 퀴즈로 시작해요!")
        return DEFAULT_QUIZ, None
    except (json.JSONDecodeError, KeyError):
        print("⚠️ 파일이 손상되어 기본 퀴즈로 복구해요!")
        return DEFAULT_QUIZ, None
if __name__ == "__main__":
    try:
        game = QuizGame()      # 👈 게임 객체 만들기!
        game.run()             # 👈 run()으로 시작!
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 프로그램을 안전하게 종료합니다. 👋")