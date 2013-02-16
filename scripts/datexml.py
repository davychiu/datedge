import xml.etree.cElementTree as ET
import json

f_test = open('../datedge/sql/test.sql', 'w')
f_question = open('../datedge/sql/question.sql', 'w')
f_scaling = open('../datedge/sql/scaling.sql', 'w')

scaled_scores = [[1,0,5],[2,2,6],[5,3,7],[8,6,9],[11,9,11],[14,12,12],[17,15,13],[20,18,14],[23,21,15],[26,24,16],[30,27,16],[35,31,18],[38,36,19],[41,39,20],[44,42,21],[47,45,22],[49,48,25],[50,50,29]]
questions_out = ""
tests_out = ""
scalings_out = ""

for idx, score in enumerate(scaled_scores):
    min_score = score[1]
    max_score = score[0]
    scaling = score[2]
    score = ", ".join([str(idx+1), str(min_score), str(max_score), str(scaling)])
    scalings_out += "INSERT INTO datedge_scaling (id, min_score, max_score, scaled) VALUES (" + score + ");\n"

for n in range(1,6):
    test = ET.parse('testdata/' + str(n) + 'testdata.xml')
    text1 = "\"" + open('testdata/' + str(n) + 'text_1.txt','r').read().replace('"',"'").replace("\n","").replace("\r","").replace("\t"," ").replace("<html>","").replace("</html>","") + "\""
    text2 = "\"" + open('testdata/' + str(n) + 'text_2.txt','r').read().replace('"',"'").replace("\n","").replace("\r","").replace("\t"," ").replace("<html>","").replace("</html>","") + "\""
    text3 = "\"" + open('testdata/' + str(n) + 'text_3.txt','r').read().replace('"',"'").replace("\n","").replace("\r","").replace("\t"," ").replace("<html>","").replace("</html>","") + "\""
    test_id = "1"
    questions =  test.findall('.//question')

    tests_out += "INSERT INTO datedge_test (id, text1, text2, text3) VALUES (" + str(n) + ", " + text1 + ", " + text2 + ", " + text3 + ");\n"

    for q_id, q in enumerate(questions):
        answers = q.findall('.//option')
        answer_id = "";
        for i, a in enumerate(answers):
            if a.get('correct') == "true":
                answer_id = str(i)
        opt1 = "\"" + " ".join(answers[0][0].text.replace('\n','').split()).replace("<html>","").replace("</html>","") + "\""
        opt2 = "\"" + " ".join(answers[1][0].text.replace('\n','').split()).replace("<html>","").replace("</html>","") + "\""
        opt3 = "\"" + " ".join(answers[2][0].text.replace('\n','').split()).replace("<html>","").replace("</html>","") + "\""
        try:
            opt4 = "\"" + " ".join(answers[3][0].text.replace('\n','').split()).replace("<html>","").replace("</html>","") + "\""
        except IndexError:
            opt4 = "\"\""
        try:
            opt5 = "\"" + " ".join(answers[4][0].text.replace('\n','').split()).replace("<html>","").replace("</html>","") + "\""
        except IndexError:
            opt5 = "\"\""
        description = "\"" + " ".join(q.find('text').text.replace('\n','').replace('"',"'").replace("<html>","").replace("</html>","").split()) + "\""
        text_id = q.find('additionalTextPath').text[11]

        values = ", ".join([str(q_id+(n-1)*50+1), str(n), text_id, answer_id, opt1, opt2, opt3, opt4, opt5, description])
        questions_out += "INSERT INTO datedge_question (id, test_id, text_idx, answer_idx, option1, option2, option3, option4, option5, description) VALUES (" + values.encode('utf-8', 'ignore') + ");\n"

f_test.write(tests_out.decode('windows-1252').encode('utf-8', 'ignore'))
f_test.close()
f_question.write(questions_out)
f_question.close()
f_scaling.write(scalings_out)
f_scaling.close()
