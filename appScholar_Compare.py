from flask import Flask, render_template, request, Blueprint
import pymysql
import wordsExtra_zsf
import json
app = Blueprint("appScholar_Comapre", __name__)
@app.route("/compare")
def compare():
    partner_list = request.args.get('partner')
    partner_list = eval(partner_list)
    conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                           charset="utf8")
    cls = conn.cursor()
    all_name = []
    achivement_list = []
    achivement_list2 = []
    cited_list = []
    paper_search_list = []
    need_part = '`name`,`scholarid`,`achievement_list`,`achievement_list2`,`cited_list`,`paper_search_list`'
    achiveminiyear, cited_minyear = 10000, 10000;
    achivemaxyear, cited_maxyear = 0, 0
    results = []
    for scholar in partner_list:
        name = scholar['name']
        id = scholar['id']
        school = str(scholar['in']).split('学')
        if len(school) > 1:
            realschool = school[0] + '学'
        else:
            realschool = school[0]
        sql = "select %s from %s where id between 1 and 2500 and scholarid='%s'" % (need_part, realschool, id)
        # print(sql)
        try:
            cls.execute(sql);
            conn.commit()
            result = cls.fetchone()
            if result[4]:  # 代表整条数据都有
                all_name.append(result[0])
                achivement_list.append(eval(result[2]))
                achivement_list2.append(eval(result[4]))
                cited_list.append(eval(result[3]))
                paper_search_list.append(eval(result[5]))
                citede_year = eval(result[3])
                achivement_year = eval(result[4])
                if int(citede_year[0]['year']) < cited_minyear:
                    cited_minyear = int(citede_year[0]['year'])
                if int(citede_year[len(citede_year) - 1]['year']) > cited_maxyear:
                    cited_maxyear = int(citede_year[len(citede_year) - 1]['year'])
                if int(achivement_year[0]['year']) < achiveminiyear:
                    achiveminiyear = int(achivement_year[0]['year'])
                if int(achivement_year[len(achivement_year) - 1]['year']) > achivemaxyear:
                    achivemaxyear = int(achivement_year[len(achivement_year) - 1]['year'])
        except:
            pass
    compare_ans = {
        'all_name': all_name,
        'achivement_list': achivement_list,
        'achivement_list2': achivement_list2,
        'cited_list': cited_list,
        'paper_search_list': paper_search_list,
        'achive_minyear': achiveminiyear,
        'achive_maxyear': achivemaxyear,
        'cited_minyear': cited_minyear,
        'cited_maxyear': cited_maxyear,
    }
    compare_ans = json.dumps(compare_ans, ensure_ascii=False)
    return compare_ans

def compare1(ScholarInfoIncluedeCollege):
    conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                           charset="utf8")
    cls = conn.cursor()
    all_name = []
    achivement_list = []
    achivement_list2 = []
    cited_list =[]
    paper_search_list =[]
    need_part = '`name`,`scholarid`,`achievement_list`,`achievement_list2`,`cited_list`,`paper_search_list`'
    achiveminiyear,cited_minyear = 10000,10000;
    achivemaxyear ,cited_maxyear= 0,0
    results = []
    for scholar in ScholarInfoIncluedeCollege:
        name = scholar['name']
        school = scholar['school']
        college = scholar['college']
        if college:
            sql = "select * from %s where id between 1 and 2500 and name='%s' and colleg = '%s' " % (
            school, name, college)
        else:
            sql = "select * from %s where id between 1 and 2500 and name='%s'" % (school, name)
        print(sql)
        try:
            cls.execute(sql);
            conn.commit()
            result = cls.fetchone()
            results.append(result)
        except:
            results.append("")
           #  print('查询出错,无该学者所在学校或者表')
    print(results)
    # 对results进行处理
    listresult = []
    for reone in results:
        if reone:#表示能查到该条数据
            # 如果reone[4]存在表示整条数据存在
            if reone[4]:
                # 去掉研究领域的[]
                if reone[5]:
                    filed = (reone[5].replace('[\'', ' ').replace('\']', ' ').replace('\', \'', ', '))
                try:  # 期刊会议
                    meeting = eval(reone[10])
                except:
                    meeting = []
                try:  # 引用
                    cited = eval(reone[11])
                except:
                    cited = []
                try:  # 成果
                    achive = eval(reone[12])
                except:
                    achive = []
                try:  # 合作学者
                    partner = eval(reone[13])
                except:
                    partner = []
                try:  # paper_name
                    paper_name = eval(reone[14])
                except:
                    paper_name = []
                try:  # 论文关键信息
                    paper_info = eval(reone[15])
                except:
                    paper_info = []
                try:  # 论文搜索信息
                    paper_search = eval(reone[16])
                except:
                    paper_search = []
                try:  # 合作机构
                    cooperate = eval(reone[17])
                except:
                    cooperate = []
                try:
                    dict_word = wordsExtra_zsf.deal_srchp2(reone[14], reone[16])
                    paper_search_key1 = list(dict_word.keys())
                    paper_search_num1 = list(dict_word.values())
                except:
                    dict_word = {}

                if len(paper_search_key1) > 30:
                    paper_search_key = paper_search_key1[:30]
                    paper_search_num = paper_search_num1[:30]
                else:
                    paper_search_key = paper_search_key1
                    paper_search_num = paper_search_num1
                newtuple = (
                    reone[0], reone[1], reone[2], reone[3], reone[4], filed, reone[6], reone[7], reone[8], reone[9],
                    meeting, achive, cited,partner, paper_name, paper_info, paper_search, cooperate, len(paper_name), paper_search_key,
                    paper_search_num);
                listresult.append(newtuple)
                all_name.append(reone[0]);
                achivement_list.append(meeting);
                achivement_list2.append(achive)
                cited_list.append(cited)
                if int(cited[0]['year']) < cited_minyear:
                    cited_minyear = int(cited[0]['year'])
                if int(cited[len(cited) - 1]['year']) > cited_maxyear:
                    cited_maxyear = int(cited[len(cited) - 1]['year'])
                if int(achive[0]['year']) < achiveminiyear:
                    achiveminiyear = int(achive[0]['year'])
                if int(achive[len(achive) - 1]['year']) > achivemaxyear:
                    achivemaxyear = int(achive[len(achive) - 1]['year'])
            else:
                newtuple = (reone[0], reone[1], reone[2], reone[3], reone[4], reone[5], reone[6], reone[7], reone[8],
                reone[9], reone[10], reone[11], reone[12],
                reone[13], reone[14], reone[15], reone[16], reone[17], 0)
                listresult.append(newtuple)
        else:#表示无该条学者数据
            listresult.append(reone)
    compare_ans = {
        'all_name': all_name,
        'achivement_list': achivement_list,
        'achivement_list2': achivement_list2,
        'cited_list': cited_list,
        'achive_minyear': achiveminiyear,
        'achive_maxyear': achivemaxyear,
        'cited_minyear': cited_minyear,
        'cited_maxyear': cited_maxyear,
    }
    return listresult,compare_ans
