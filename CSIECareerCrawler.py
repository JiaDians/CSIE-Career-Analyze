from selenium import webdriver
import time,re
from bs4 import BeautifulSoup
from tqdm import tqdm
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']

test = {'前端工程師': 'https://www.104.com.tw/jobs/search/?keyword=%E5%89%8D%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%AB&order=1&jobsource=2018indexpoc&ro=0',
        '後端工程師': 'https://www.104.com.tw/jobs/search/?keyword=%E5%BE%8C%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%AB&order=1&jobsource=2018indexpoc&ro=0',
        '網路工程師': 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E7%B6%B2%E8%B7%AF%E5%B7%A5%E7%A8%8B%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1',
        '韌體設計工程師': 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E9%9F%8C%E9%AB%94%E8%A8%AD%E8%A8%88%E5%B7%A5%E7%A8%8B%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1',
        '電腦系統分析師': 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E9%9B%BB%E8%85%A6%E7%B3%BB%E7%B5%B1%E5%88%86%E6%9E%90%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1',
        '區塊鏈工程師': 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E5%8D%80%E5%A1%8A%E9%8F%88%E5%B7%A5%E7%A8%8B%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1',
        '資料科學家': 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E8%B3%87%E6%96%99%E7%A7%91%E5%AD%B8%E5%AE%B6&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1',
        '資安工程師': 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E8%B3%87%E5%AE%89%E5%B7%A5%E7%A8%8B%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1',
        '電腦視覺工程師': 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E9%9B%BB%E8%85%A6%E8%A6%96%E8%A6%BA%E5%B7%A5%E7%A8%8B%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'}

search_page_count = 100
education_experience_lists = []
work_experience_lists = []
skill_count_lists = []
salary_month_lists = []
salary_year_lists = []
average_salary_month_list = []
median_salary_month_list = []


def getData():
    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(3)
    soup = []
    # for i in range(2):
    for i in range(len(test)):
        print('正在取得', list(test.keys())[i], '的資料')
        driver.get(list(test.values())[i])
        
        # 取得 search_page_count
        soup_temp = BeautifulSoup(driver.page_source, "html5lib")
        regex = re.compile('\s*b-clear-border\s*page-select\s*js-paging-select\s*gtm-paging-bottom\s*')
        page_number_tag = soup_temp.find("select",{'class': regex})
        m = re.search('第.+?頁', page_number_tag.text)
        if m != None:   
           # print(m.group(0))
           m2 = re.search('/.+?頁', m.group(0))
           search_page_count = int(m2.group(0)[1:-1].strip())
           if search_page_count > 100:
               search_page_count = 100
                   
        # 開爬
        btn_count = 0
        progress = tqdm(total=search_page_count)
        for j in range(search_page_count):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            soup_temp = BeautifulSoup(driver.page_source, "html5lib")
            regex = re.compile('\s*b-btn\s*b-btn--link\s*js-more-page\s*')
            btn = soup_temp.findAll("button",{'class': regex})
            # print(btn)
            if len(btn) != btn_count:
                btn_count += 1
                btn_list = driver.find_elements_by_xpath("//button[@class='b-btn b-btn--link js-more-page']")
                btn_list[len(btn_list)-1].click()
            progress.update(1)
            time.sleep(3.5)
        
        soup.append(BeautifulSoup(driver.page_source, "html5lib"))
        progress.close()
        print()
    driver.close()
    return soup

def main(soup):
    for i in range(len(soup)):
        print(list(test.keys())[i])
        # salary
        regex = re.compile('b-tag--default')
        salary_info_list1 = soup[i].findAll("span",{'class': regex}, string=re.compile("月薪.+~.+元"))
        salary_info_list2 = soup[i].findAll("span",{'class': regex}, string=re.compile("月薪.+元以上"))
        salary_info_list3 = soup[i].findAll("span",{'class': regex}, string=re.compile("年薪.+~.+元"))
        salary_info_list4 = soup[i].findAll("span",{'class': regex}, string=re.compile("年薪.+元以上"))
        
        
        salary_month_list = []
        salary_year_list = []
        # salary_info_list1
        for salary in salary_info_list1:
            salary_temp = re.search('[0-9,]+~[0-9,]+', salary.text) 
            salary_temp = salary_temp.group(0).replace(',', '')
            salary_range = salary_temp.split('~')
            salary_month_list.append((int(salary_range[0]) + int(salary_range[1]))//2)
        # salary_info_list2
        for salary in salary_info_list2:
            salary_temp = re.search('[0-9,]+', salary.text) 
            salary_temp = salary_temp.group(0).replace(',', '')
            salary_month_list.append(int(salary_temp))
        # salary_info_list3
        for salary in salary_info_list3:
            salary_temp = re.search('[0-9,]+~[0-9,]+', salary.text) 
            salary_temp = salary_temp.group(0).replace(',', '')
            salary_range = salary_temp.split('~')
            salary_year_list.append((int(salary_range[0]) + int(salary_range[1]))//2)
        # salary_info_list4
        for salary in salary_info_list4:
            salary_temp = re.search('[0-9,]+', salary.text) 
            salary_temp = salary_temp.group(0).replace(',', '')
            salary_year_list.append(int(salary_temp))
        
        salary_month_lists.append(salary_month_list)
        salary_year_lists.append(salary_year_list)
        
        if len(salary_month_list) > 0:
            print('月薪平均:', sum(salary_month_list)//len(salary_month_list), '月薪中位數:', sorted(salary_month_list)[len(salary_month_list)//2])
            average_salary_month_list.append(sum(salary_month_list)//len(salary_month_list))
            median_salary_month_list.append(sorted(salary_month_list)[len(salary_month_list)//2])
        if len(salary_year_list) > 0:
            print('年薪平均:', sum(salary_year_list)//len(salary_year_list), '年薪中位數:', sorted(salary_year_list)[len(salary_year_list)//2])
        
        # experience
        regex = re.compile('\s*b-list-inline\s*b-clearfix\s*job-list-intro\s*b-content')
        experience_list = soup[i].findAll("ul",{'class': regex})
        
        education_experience_dict = {}
        work_experience_dict = {}
        for experience in experience_list:
            # education_experience_lists
            if '高中' in experience.text:
                education_experience_dict['高中'] = education_experience_dict.get('高中', 0) + 1
            elif '專科' in experience.text:
                education_experience_dict['專科'] = education_experience_dict.get('專科', 0) + 1
            elif '大學' in experience.text:
                education_experience_dict['大學'] = education_experience_dict.get('大學', 0) + 1
            elif '碩士' in experience.text:
                education_experience_dict['碩士'] = education_experience_dict.get('碩士', 0) + 1
              
            # work_experience_lists
            if '經歷不拘' in experience.text:
                work_experience_dict['經歷不拘'] = work_experience_dict.get('經歷不拘', 0) + 1
            m = re.search('.年以上', experience.text)
            if m != None:   
                work_experience_dict[m.group(0)] = work_experience_dict.get(m.group(0), 0) + 1
            
        education_experience_lists.append(education_experience_dict)    
        work_experience_lists.append(work_experience_dict)
        
        
        # skill info
        regex = re.compile('\s*job-list-item__info\s*b-clearfix\s*b-content\s*')
        article_info_list = soup[i].findAll("p",{'class': regex})
        
        article_skill_source_data = []
        for article_info in article_info_list:
            article_skill_list = re.findall('[a-zA-Z][a-zA-Z0-9-]*', article_info.text)
            # print('----------------------------------------------')
            # print(article_skill_list)
            if len(article_skill_list) < 30:
                article_skill_source_data += article_skill_list
            
        skill_count_dict = {}
        for data in article_skill_source_data:
            skill_count_dict[data] = skill_count_dict.get(data, 0) + 1
        
        skill_count_dict = sorted(skill_count_dict.items(), key=lambda x: x[1], reverse = True)  
        skill_count_lists.append(skill_count_dict)
        
        print('Skill: ', end='')
        for skill in skill_count_dict[:20]:
            print(skill[0], end=',')
        print()
        print('---------------------------------------')
    
def GraphAnalyze(salary_month_lists, salary_year_lists, education_experience_lists, work_experience_lists, average_salary_month_list, median_salary_month_list):
    # salary
    min_salary_month = min(salary_month_lists[0])
    for salary_month_list in salary_month_lists:
        min_salary_month = min(min_salary_month, min(salary_month_list))
    max_salary_month = 0
    for salary_month_list in salary_month_lists:
        max_salary_month = max(max_salary_month, max(salary_month_list))
    
    if len(str(min_salary_month)) >= 5:
        min_salary_month = ((min_salary_month // 10000)) * 10000
    else:
        print('error')
    if len(str(max_salary_month)) >= 5:
        max_salary_month = ((max_salary_month // 10000)+1) * 10000
    else:
        print('error')
    
    # print(min_salary_month, max_salary_month)
    
    # 建立 salary_range_list
    salary_range_list = [min_salary_month + 10000 * i for i in range((max_salary_month // 10000) - (min_salary_month // 10000))]
    
    # 建立 salary_range_dict
    salary_range_dict = {}
    for test_name in list(test.keys()):
        salary_range_dict[test_name] = {}
        for salary in salary_range_list:
            salary_range_dict[test_name][str(salary) + '_' + str(salary + 10000)] = 0
    # print(salary_range_dict)
    
    test_name_list = list(test.keys())
    for i in range(len(test_name_list)):
        for salary in salary_month_lists[i]:
            salary = (salary // 10000) * 10000
            salary_range_dict[test_name_list[i]][str(salary) + '_' + str(salary + 10000)] = salary_range_dict[test_name_list[i]][str(salary) + '_' + str(salary + 10000)] + 1
    # print(salary_range_dict)
    
    company_count = []
    for test_name in list(test.keys()):
        company_count.append([salary_range_dict[test_name][str(salary) + '_' + str(salary + 10000)] for salary in salary_range_list])
    # print(company_count)
    
    salary_xticks = salary_range_list.copy()
    salary_xticks.append(salary_range_list[len(salary_range_list)-1] + 10000)
    
    # ------------------------------------------------------------
    # main 
    plt.figure(1, figsize=(8,5))
    plt.subplot(111) 
    plt.grid()
    for i in range(len(test_name_list)):
        plt.bar([salary + 5000 for salary in salary_range_list], 
        	company_count[i],
        	10000, 
        	edgecolor=(0, 0, 0),
            label = test_name_list[i],
            alpha = 0.8) 
    salary_xtick_temp = [salary_xtick // 1000 for salary_xtick in salary_xticks]
    plt.xticks(salary_xticks, salary_xtick_temp, rotation=-90) 
    plt.xlabel("Monthly salary (k)")
    plt.ylabel("Number of companies")
    plt.title('資工「各領域」開出薪資範圍內之公司數對比圖')
    plt.legend(loc = 'upper right')     
    plt.tight_layout()
    plt.savefig('1.png')
    
    # main 2
    plt.figure(2, figsize=(8,5))
    plt.subplot(111) 
    plt.grid()
    for i in range(2):
        plt.bar([salary + 5000 for salary in salary_range_list], 
        	company_count[i],
        	10000, 
        	edgecolor=(0, 0, 0),
            label = test_name_list[i],
            alpha = 0.4) 
    salary_xtick_temp = [salary_xtick // 1000 for salary_xtick in salary_xticks]
    plt.xticks(salary_xticks, salary_xtick_temp, rotation=-90) 
    plt.xlabel("Monthly salary (k)")
    plt.ylabel("Number of companies")
    plt.title('「' + test_name_list[0] + '」 與 「'+ test_name_list[1] + '」 開出薪資範圍內之公司數對比圖')
    plt.legend(loc = 'upper right')     
    plt.tight_layout()
    plt.savefig('2.png')
    
    # ------------------------------------------------------------
    # sub
    plt.figure(3, figsize=(10,7))
    for i in range(len(test_name_list)):
        plt.subplot(int(str(3)+str(3)+str(i+1))) 
        plt.grid()
        plt.bar([salary + 5000 for salary in salary_range_list], 
        	company_count[i],
        	10000, 
        	edgecolor=(0, 0, 0),
            alpha = 0.8) 
        salary_xtick_temp = [salary_xtick // 1000 for salary_xtick in salary_xticks]
        plt.xticks(salary_xticks, salary_xtick_temp, rotation=-90) 
        plt.xlabel("Monthly salary (k)")
        plt.ylabel("Number of companies")
        plt.title(test_name_list[i] + ' (開出月薪範圍內之公司數統計)')
    plt.tight_layout()
    plt.savefig('3.png')
    
    # ------------------------------------------------------------
    # average_salary_month_list
    average_salary_month_dict = {}
    average_salary_month_dict = dict(zip(test_name_list, average_salary_month_list))
    sorted_average_salary_month_list = sorted(average_salary_month_dict.items(), key=lambda x: x[1])
    plt.figure(4, figsize=(10,7))
    plt.subplot(111) 
    plt.grid()
    plt.barh([a for a,b in sorted_average_salary_month_list], [b for a,b in sorted_average_salary_month_list]) 
    plt.xlabel("平均 月薪")
    plt.ylabel("領域")
    plt.title('資工各領域「平均」薪資對照')
    for i in range(len(test_name_list)):
        plt.text(sorted_average_salary_month_list[i][1] + 1000, 
                 i,
                 str(sorted_average_salary_month_list[i][1]),
                 color='red',
                 fontweight='bold',
                 va= 'center')
    plt.tight_layout()
    
    plt.savefig('4.png')
    
    
    # ------------------------------------------------------------
    # median_salary_month_list
    
    median_salary_month_dict = {}
    median_salary_month_dict = dict(zip(test_name_list, median_salary_month_list))
    sorted_median_salary_month_list = sorted(median_salary_month_dict.items(), key=lambda x: x[1])
    plt.figure(5, figsize=(10,7))
    plt.subplot(111) 
    plt.grid()
    plt.barh([a for a,b in sorted_median_salary_month_list], [b for a,b in sorted_median_salary_month_list]) 
    plt.xlabel("中位數 月薪")
    plt.ylabel("領域")
    plt.title('資工各領域「中位數」薪資對照')
    for i in range(len(test_name_list)):
        plt.text(sorted_median_salary_month_list[i][1] + 1000,
                 i,
                 str(sorted_median_salary_month_list[i][1]),
                 color='red',
                 fontweight='bold',
                 va= 'center') 
    plt.tight_layout()
    
    plt.savefig('5.png')
    
    # ------------------------------------------------------------
    # education_experience
    plt.figure(6, figsize=(10,7))
    for i in range(len(test_name_list)):
        plt.subplot(int(str(3)+str(3)+str(i+1))) 
        plt.title(test_name_list[i] + ' (學歷要求)')
        dict_temp = dict(sorted(education_experience_lists[i].items(), key=lambda item: item[1]))
        mylabels = dict_temp.keys()
        mylabels = [mylabel + '以上' for mylabel in mylabels]
        plt.pie(dict_temp.values(), labels=(mylabels), autopct='%1.1f%%', radius=1, explode = [0.05 for i in range(len(dict_temp))])
    plt.tight_layout()
    plt.savefig('6.png')
    
    # ------------------------------------------------------------
    # work_experience
    plt.figure(7, figsize=(10,7))
    for i in range(len(test_name_list)):
        plt.subplot(int(str(3)+str(3)+str(i+1))) 
        plt.title(test_name_list[i] + ' (工作經歷)')
        dict_temp = dict(sorted(work_experience_lists[i].items(), key=lambda item: item[1]))
        # print(dict_temp)
        mylabels = list(dict_temp.keys())
        plt.pie(list(dict_temp.values()),labels=(mylabels),autopct='%1.1f%%', radius=1, explode= [0.05 for i in range(len(dict_temp))])
    plt.tight_layout()
    plt.savefig('7.png')
    
    plt.show()

if __name__ == '__main__':
    soup = getData()
    main(soup)
    GraphAnalyze(salary_month_lists, salary_year_lists, 
                 education_experience_lists, 
                 work_experience_lists,
                 average_salary_month_list,
                 median_salary_month_list)
