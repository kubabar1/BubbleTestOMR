import argparse
import cv2
import os

from test_grader import grade_test
from test_grader_utils import get_answer_key_default, get_answer_key_csv, get_answer_key_excel


def get_input_data():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--answers", required=True, help="Path to file with correct answers")
    ap.add_argument("-i", "--image", required=True, help="Path to the input image")
    args = vars(ap.parse_args())

    answers_file_path = args['answers']
    input_img = cv2.imread(args["image"])

    _, file_extension = os.path.splitext(answers_file_path)
    if file_extension == "" or file_extension == ".txt":
        answer_key = get_answer_key_default(answers_file_path)
    elif file_extension == ".csv":
        answer_key = get_answer_key_csv(answers_file_path)
    elif file_extension == ".xlsx":
        answer_key = get_answer_key_excel(answers_file_path)
    else:
        raise Exception("Specified file with correct answers has unsupported file format")

    return input_img, answer_key


def show_results(input_img, paper_img, correct):
    score = (correct / 5.0) * 100
    print("[INFO] score: {:.2f}%".format(score))
    cv2.putText(paper_img, "{:.2f}%".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    cv2.imshow("Original", input_img)
    cv2.imshow("Exam", paper_img)


def main():
    input_img, answer_key = get_input_data()
    correct, paper = grade_test(input_img, answer_key)
    show_results(input_img, paper, correct)

    while True:
        k = cv2.waitKey(25) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
