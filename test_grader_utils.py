import cv2


def show_contours_cvtColor(image, contours):
    """Show contours detected by cv2.cvtColor

    :param image: image where edges have been detected
    :param contours: contours detected by cv2.cvtColor
    """
    tmp_image = image.copy()
    for contour in contours[0][0]:
        cv2.circle(tmp_image, tuple(contour[0]), radius=3, color=(0, 0, 255), thickness=-1)
    cv2.imshow('cvtColor_contours', tmp_image)
    pass


def show_contours_doc_cnt(image, doc_contour_points):
    """Show contours basis on 4 document contour points

    :param image: image where edges have been detected
    :param doc_contour_points: 4 document contour points
    """
    tmp_image = image.copy()
    a, b, c, d = doc_contour_points[0][0], doc_contour_points[1][0], doc_contour_points[2][0], doc_contour_points[3][0]
    cv2.line(tmp_image, tuple(a), tuple(b), (0, 255, 0), thickness=3, lineType=8)
    cv2.line(tmp_image, tuple(b), tuple(c), (0, 255, 0), thickness=3, lineType=8)
    cv2.line(tmp_image, tuple(c), tuple(d), (0, 255, 0), thickness=3, lineType=8)
    cv2.line(tmp_image, tuple(d), tuple(a), (0, 255, 0), thickness=3, lineType=8)
    cv2.imshow('doc_cnt_contours', tmp_image)
    pass


def get_answer_key_from_txt(answers_txt_file_path):
    answer_key = {}
    with open(answers_txt_file_path, 'r') as f:
        for idx, line in enumerate(f.readlines()):
            answer_key[idx] = ord(line.replace("\n", "").upper()) - 65
    return answer_key