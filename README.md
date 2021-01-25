# BubbleTestOMR
Program basis on this tutorial: https://www.pyimagesearch.com/2016/10/03/bubble-sheet-multiple-choice-scanner-and-test-grader-using-omr-python-and-opencv/


## How to run?
```
python console_script.py -i test_data/test_exam/sheets/test2.png -a test_data/test_exam/correct_answers.txt
python console_script.py -i test_data/test_16_answ/sheets -a test_data/test_16_answ/answers.txt
```

Second example command process all images in directory. File with answers may have txt, csv or xlsx format. Output file contating results and selected answers for each input file is generated in report.xlsx file in script directory or inside directory pointed by '-o' param.

Close by "ESC" key

## Additional params
```
  -a ANSWERS, --answers ANSWERS
                        Path to file with correct answers
  -i IMAGE, --image IMAGE
                        Path to the input image or directory containing multiple test images
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Path to the output directory for generated report
  -s SHOW_RESULT_IMAGES, --show_result_images SHOW_RESULT_IMAGES
                        Are result images should be displayed
  -ac ANSWERS_COUNT, --answers_count ANSWERS_COUNT
                        Count of possible answers
```

##  Files dscription
<b>console_script</b> - script to run program from console </br>
<b>test_grader</b> - test grader backend code, main method is grade_test, which is used in console_script </br>
<b>test_grader_utils</b> - additional utils, used mainly to research purpose or by console script </br>
