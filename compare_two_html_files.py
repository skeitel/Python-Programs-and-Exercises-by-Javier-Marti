'''We use the difflib library to compare two different HMTL files and see what has changed. JavierMarti.co.uk'''

#import library
import difflib
#define variables containing files
first_file = 'html_diff_exercise/temperase_file1.html'
second_file = 'html_diff_exercise/temperase_file2.html'
first_file_lines = open(first_file).readlines()
second_file_lines = open(second_file).readlines()

#perform the comparison operation
difference = difflib.HtmlDiff().make_file(first_file_lines, second_file_lines, first_file, second_file)

#produce report
destination_file = 'html_diff_difference_report.html'
difference_report = open(destination_file, 'w')
difference_report.write(difference)
difference_report.close()

#print outcome
print('The file ' + destination_file + ' has been produced and can be viewed now')