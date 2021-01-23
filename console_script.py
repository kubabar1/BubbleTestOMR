import argparse
import cv2

from test_grader import grade_test
from test_grader_utils import get_answer_key_from_txt


def get_input_data():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--answers", required=True, help="Path to file with correct answers")
    ap.add_argument("-i", "--image", required=True, help="Path to the input image")
    args = vars(ap.parse_args())

    # get answers keys from txt file
    answer_key = get_answer_key_from_txt(args['answers'])
    input_img = cv2.imread(args["image"])
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
