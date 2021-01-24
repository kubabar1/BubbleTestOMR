from imutils import contours
from imutils.perspective import four_point_transform
import numpy as np
import imutils
import cv2


def obtain_silhouette(input_image):
    """Obtain silhouette of the document by converting it to greyscale, blurring and finding edges

    :param input_image: image to obtain silhouette
    :return: tuple containing silhouette of the input image and grayscale image
    """
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    return edged, gray


def get_paper_contour(edged_img):
    """Find contour in edge map, initialize contour corresponding to the document and if at least one contour was found,
        sort all contours according to their size in descending order, loop over them, approximate the contours, and if
        approximated contour has 4 points it is treated as paper contour;

        :param edged_img: image containing edge map
        :return: document contour, or None if it wasn't found
        """
    cnts = cv2.findContours(edged_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # show_contours_cvtColor(input_img, cnts)
    cnts = imutils.grab_contours(cnts)
    doc_cnt = None
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                doc_cnt = approx
                break
    return doc_cnt


def perspective_transform(input_img, edged_img, gray_img):
    """Find paper contours and apply four point perspective transform to original and grayscale image;
    as a result return top-down birds eye view of the paper and grayscale image if its contour was found,
    otherwise it return tuple containing input_img and gray_img
    
    :param input_img: input image of the doc
    :param edged_img: image containing edge map
    :param gray_img: grayscale image
    :return: tuple containing top-down birds eye view of the paper and grayscale image if its contour was found,
    otherwise it return tuple containing input_img and gray_img
    """
    doc_cnt = get_paper_contour(edged_img)
    # show_contours_doc_cnt(input_img, doc_cnt)
    if doc_cnt is not None:
        paper = four_point_transform(input_img, doc_cnt.reshape(4, 2))
        warped = four_point_transform(gray_img, doc_cnt.reshape(4, 2))
    else:
        paper = input_img
        warped = gray_img

    return paper, warped


def get_all_questions_contours(thresh_img):
    """Find contours in the thresholded image, then initialize the list of contours that correspond to questions

    :param thresh_img: thresholded input image
    :return: contours of all questions
    """
    cnts = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    question_cnts = []
    for contour in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        # check if detected contour is a question contour
        if w >= 20 and h >= 20 and 0.9 <= aspect_ratio <= 1.1:
            question_cnts.append(contour)
    return question_cnts


def get_marked_answer(question_cnts, thresh_img):
    """

    :param question_cnts: contours of answers
    :param thresh_img: thresholded input image
    :return:
    """
    bubbled = None
    # loop over the sorted contours
    for (j, c) in enumerate(question_cnts):
        # construct a mask that reveals only the current "bubble" for the question
        mask = np.zeros(thresh_img.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)

        # apply the mask to the thresholded image, then count the number of non-zero pixels in the bubble area
        mask = cv2.bitwise_and(thresh_img, thresh_img, mask=mask)
        total = cv2.countNonZero(mask)

        # if the current total has a larger number of total non-zero pixels, then we are examining the currently
        # bubbled-in answer
        if bubbled is None or total > bubbled[0]:
            bubbled = (total, j)
    return bubbled


def check_answers(question_cnts, answer_key, thresh_img, paper):
    """For each exam question contour, determine the bubbles are marked as answers and compare with the answer key to
    make sure that the user gave the correct answer, then draw result on paper

    :param question_cnts: contours of answers
    :param answer_key: correct answers
    :param thresh_img: thresholded input image
    :param paper: input image paper, after perspective transformation
    :return: count of correct answers checked by user
    """
    correct = 0
    checked_answers = []
    wrong_answer_color = (0, 0, 255)
    correct_answer_color = (0, 255, 0)
    for (q, i) in enumerate(np.arange(0, len(question_cnts), 5)):
        # sort the contours for the current question from left to right, then initialize the index of the bubbled answer
        cnts = contours.sort_contours(question_cnts[i:i + 5])[0]
        bubbled = get_marked_answer(cnts, thresh_img)

        color = wrong_answer_color
        correct_answer_key = answer_key[q]

        # check to see if the bubbled answer is correct
        if correct_answer_key == bubbled[1]:
            color = correct_answer_color
            correct += 1

        # draw the outline of the correct answer on the test
        cv2.drawContours(paper, [cnts[correct_answer_key]], -1, color, 3)
        checked_answers.append(bubbled[1])
    return correct, checked_answers


def grade_test(input_img, answer_key):
    """Grade entire test

    :param input_img: input image containing test with marked answers
    :param answer_key: answers
    :return: tuple containing points count, detected document with checked correct answers and answers checked by user
    """
    # (1) Detect exam silhouette on given input image
    edged, gray = obtain_silhouette(input_img)

    # (2) Transform perspective of detected document and its grayscale image to bird-eye-view
    paper, warped = perspective_transform(input_img, edged, gray)

    # apply Otsu's thresholding method to binarize the warped piece of paper
    thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # (3) Get contours of all possible questions answers
    question_cnts = get_all_questions_contours(thresh)

    # (4) sort the question contours top-to-bottom
    question_cnts = contours.sort_contours(question_cnts, method="top-to-bottom")[0]

    # (5) (6) (7) for each exam question, determine the bubbles are marked as answers and compare with the key to
    # make sure that the user gave the correct answer
    correct, checked_answers = check_answers(question_cnts, answer_key, thresh, paper)
    return correct, paper, checked_answers
