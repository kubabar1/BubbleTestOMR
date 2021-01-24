import argparse
import cv2
import os
from os import listdir
from os.path import isfile, join
from test_grader import grade_test
from test_grader_utils import get_answer_key_default, get_answer_key_csv, get_answer_key_excel, save_results


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_input_data():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--answers", required=True, help="Path to file with correct answers")
    ap.add_argument("-i", "--image", required=True,
                    help="Path to the input image or directory containing multiple test images")
    ap.add_argument("-o", "--output_dir", required=False, default='.',
                    help="Path to the output directory for generated report")
    ap.add_argument("-s", "--show_result_images", required=False, default=True, type=str2bool,
                    help="Are result images should be displayed")
    args = vars(ap.parse_args())

    input_path = args["image"]
    answers_file_path = args["answers"]
    output_report_dir = args["output_dir"]
    show_result_images = args["show_result_images"]

    if os.path.isfile(input_path):
        input_images_paths = [input_path]
        input_images = [cv2.imread(input_images_paths[0])]
    else:
        input_images_paths = [join(input_path, f) for f in listdir(input_path) if isfile(join(input_path, f))]
        input_images = [cv2.imread(f) for f in input_images_paths]

    _, file_extension = os.path.splitext(answers_file_path)
    if file_extension == "" or file_extension == ".txt":
        answer_key = get_answer_key_default(answers_file_path)
    elif file_extension == ".csv":
        answer_key = get_answer_key_csv(answers_file_path)
    elif file_extension == ".xlsx":
        answer_key = get_answer_key_excel(answers_file_path)
    else:
        raise Exception("Specified file with correct answers has unsupported file format")

    return input_images, answer_key, input_images_paths, output_report_dir, show_result_images


def show_results(input_img, paper_img, score, input_img_path, show_result_images):
    input_image_name = os.path.splitext(os.path.basename(input_img_path))[0]
    print("[INFO] {:s} - score: {:.2f}%".format(input_image_name, score))
    if show_result_images:
        cv2.putText(paper_img, "{:.2f}%".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        cv2.imshow("Original_" + str(input_image_name), input_img)
        cv2.imshow("Exam_" + str(input_image_name), paper_img)


def main():
    input_images, answer_key, input_images_paths, output_report_dir, show_result_images = get_input_data()
    scores_array = []
    checked_answers_array = []
    for idx, input_img in enumerate(input_images):
        correct, paper, checked_answers = grade_test(input_img, answer_key)
        score = (correct / 5.0) * 100
        show_results(input_img, paper, score, input_images_paths[idx], show_result_images)
        scores_array.append(score)
        checked_answers_array.append(checked_answers)
    save_results(input_images_paths, output_report_dir, scores_array, checked_answers_array)

    if show_result_images:
        while True:
            k = cv2.waitKey(25) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
