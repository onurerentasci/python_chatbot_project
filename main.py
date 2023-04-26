import json
from difflib import get_close_matches


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


def chatbot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    username = input("Merhaba! Sana nasıl seslenmemi istersin? \n")
    while True:
        user_input: str = input(f'{username}: ')

        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print("Bot: {0}".format(answer))
        else:
            print("Bot: Bunun ne anlama geldiğini bilmiyorum. \n"
                  "Bana bu soruya ne cevap vermem gerektiğini öğretebilir misin? \n")
            new_answer: str = input('İstiyorsan cevabı yazabilirsin. Eğer geçmek istersen "pas" yazman yeterli \n')

            if new_answer.lower() != 'pas':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Yeni bir şey öğrenmemde yardımcı olduğun için teşekkür ederim!")


if __name__ == '__main__':
    chatbot()
