#After rebooting error was solved. literally restarting is sometimes best solutions.

import streamlit as st
import requests
import re
import base64
from bs4 import BeautifulSoup
from st_btn_select import st_btn_select


def main():
  regular_ended=False
  student_type='REGULAR'
  for i in range(st.session_state['starting_range'],st.session_state['ending_range']):
    
    i_th_url= url_maker(year_no,student_type, str(int(roll_no) + i), course_name)
    #print(i_th_url)
    
    # Make a request
    page = requests.get(i_th_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # print the result
    text=soup.get_text()
    #LOGIC FOR PRIVATE STUDENTS.
    if "Result Not Found" in text:
      regular_ended = True
      student_type = 'Non Col'
      st.write("Now Private students")
      #i=i-1
      i_th_url= url_maker(year_no,student_type, str(int(roll_no) + i), course_name)
      page = requests.get(i_th_url)
      soup = BeautifulSoup(page.content, 'html.parser')
      text=soup.get_text()
      
      
    #Using only useful information and deleting rest  
    start_text_index=text.find('Roll')
    end_text_index=text.find('Note')
    end_word='Note'

    # Adjust indices to include the starting and ending words
    start_text_index = max(0, start_text_index)  # Avoid negative index
    end_text_index += len(end_word)  # Include the ending word itself

    text=text[start_text_index:end_text_index]
    #st.write(text)

    #print(new_text)
    #word_list=text.split()

    
      
    pass_status="Supply"
    percentage=0
    #Searching for name
    start_text_index=text.find('(SHRI/SMT./KU.)')
    end_text_index=text.find('Father\'s')

    if start_text_index == -1 or end_text_index == -1:
      name='No words found'  # Words not found
    
    name=text[start_text_index+18:end_text_index-3]
    isPass=text.find("PASS")
    isFail=text.find("FAIL")
    #isSupply=text.find("SUPPLY 1ST")
    
    #Pass_Status
    if isPass!=-1:
      pass_status="PASS"
    if isFail!=-1:
      pass_status="FAIL"
    

    #NOW SEARCH FOR PERCENTAGE
    percentage=str(percentage_finder(text))+"%"
    
    subjects=subject_finder(text)
    result=[name,pass_status,percentage,subjects,i_th_url]  
    results.append(result)


def next_page():
    st.session_state['starting_range'] += 25
    st.session_state['ending_range'] += 25

def previous_page():
    if st.session_state['starting_range'] == 0:
        pass  # Nothing to do if already at the beginning
    else:
        st.session_state['starting_range'] -= 25
        st.session_state['ending_range'] -= 25
    return None  # Optional return statement


def subject_finder(text):
  subjects = ["BOTANY", "ZOOLOGY", "CHEMISTRY", "MATHEMATICS", "PHYSICS", "INFORMATION TECHNOLOGY","SOCIOLOGY","HISTORY","POLITICAL SCIENCE","PSYCHOLOGY","HINDI LITERATURE","ENGLISH LITERATURE","GEOGRAPHY","ECONOMICS","GROUP - I","GROUP - II","GROUP - III","GROUP - B MARKETING AREA"]
  found_subjects = []
  for subject in subjects:
    if (text.find(subject)!=-1):
        found_subjects.append(subject)
  return found_subjects

def percentage_finder(text):
  pattern = r"\b(\d{3})/600\b"
  match = re.search(pattern, text)
  if match:
    percentage=int(match.group(1))/6
    percentage=round(percentage, 2)
  else:
    percentage="percentage not found"
  return percentage

def percentage_finder_all_three_year(text):
  # Regular expression pattern
  pattern = r"PERCENTAGE(\d+\.\d+)"
  # Search for all matches
  matches = re.findall(pattern, text)

  if matches:
    for match in matches:
      # Access the captured percentage value
      percentage = match
      return percentage
  else:
    return "No percentages found"

def url_maker(year="Mw==",student_type="UkVHVUxBUg==",roll_no="ODk2NDI0NDAxMzUwMDdAQDE3NTY=",course="YmNh"):
  url="http://result.prsuuniv.in/rsuniv/home/student/result19annual/"
  year=encrypt(year)
  student_type=encrypt(student_type)
  roll_no="8964"+roll_no+"@@1756"
  roll_no=encrypt(roll_no)
  course=encrypt(course)
  #print(url+'/'+year+'/'+student_type+'/'+roll_no+'/'+course)
  url=url+'/'+year+'/'+student_type+'/'+roll_no+'/'+course
  return url

def encrypt(value):
  encoded_string = base64.b64encode(value.encode('utf-8')).decode('utf-8')
  return encoded_string

if 'starting_range' not in st.session_state:
    st.session_state['starting_range'] = 0
if 'ending_range' not in st.session_state:
    st.session_state['ending_range'] = 25

starting_range=st.session_state['starting_range']
ending_range=st.session_state['starting_range']

## streamlit app
st.title("PRSU RESULT FINDER")

results=[]
college_num=st.number_input("Enter college code",1,999,401)
#Values
Course={'BSc':5,'BCom':3,'BA':0,'BCA':7}
Year={'First_Year':1,'Second_Year':2,'Final_Year':3}

 
course = st_btn_select(('BSc', 'BCom', 'BA'), index=0)
year = st_btn_select(('First_Year', 'Second_Year', 'Final_Year'), index=2)
# both REGULAR and Private IS AVAILABLE
st.write("Both Regular and Private student results are available. After Regular students the Private student roll number starts.")
student_type='REGULAR'

year_no=str(Year[str(year)])
course_no=str(Course[str(course)])
course_list={'BSc':'bca', 'BCom':'B.COM.', 'BA':'B.A.','BCA':'B.C.A.'}
course_name=course_list[course]
roll_no='24'+str(college_num)+year_no+course_no+'001'

if 0<=st.session_state['starting_range']<=9:
  display_roll_no=roll_no='24'+str(college_num)+year_no+course_no+'001'
elif 10<=st.session_state['starting_range']<=99:
   display_roll_no=roll_no='24'+str(college_num)+year_no+course_no+'0'+str(st.session_state['starting_range'])
else: 
   display_roll_no=roll_no='24'+str(college_num)+year_no+course_no+str(st.session_state['starting_range'])
   
st.write("Your roll number will be :",display_roll_no)

next_page=st.button("next page",on_click=next_page)
previous_page=st.button("previous page",on_click=previous_page)
 
st.write("searching between roll numbers: ",st.session_state['starting_range'],"to",st.session_state['ending_range'])

button_clicked = st.button("Click here to get RESULTS")


if button_clicked:
  main()
  st.write(results)
  
st.write("Please consider leaving feedback in our telegram group.")
st.write("https://t.me/prsu_results_feedback")

