from tkinter import *
import datetime as dt
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkcalendar as tkc
from datetime import timedelta 
import os as os
import json

## root=main root2=mng root3=password root4=사람 추가 root5=사람 삭제

cnt=0
cnt2=0
tottime=0

#재시작 이벤트
def closing():
    root.destroy()
    main() ##파일경로 손봐야됨

#파일이 없으면 만들어주는 함수
def mkfile():
    if os.path.isfile("출석로그.txt")==0:
         f=open("출석로그.txt",'a')
    if os.path.isfile("출석_로그.json")==0:
         g=open("출석_로그.json",'a')
    if os.path.isfile("알바인원.txt")==0:
        k=open("알바인원.txt",'a')

#출근시간 기록    
def startlog():
    global cnt
    cnt=cnt+1
    if cnt>1:
        msgbox.showinfo("알림","버튼은 한 번만 누르세요")
        cnt-=1#나중에 중복 시간 지우는 로직 짜기
    else:
        now=dt.datetime.now()  #현재시간 부르기
        dt_str=(now.strftime('%y-%m-%d %H:%M')) #타임스탬프 기록
        global st_time
        global stjson_time
        put_name=combox.get()
        st_time=(now.strftime('%y-%m-%d %H:%M')) ##시작 시간 킵
        stjson_time=(now.strftime('%H:%M')) ## 날짜 재낀 json 시작시간, 문자형임.
        global cnt_stjsontime
        cnt_stjsontime=(dt.datetime.strptime(stjson_time,'%H:%M'))

        
       
        f = open("출석로그.txt", 'a')
        f.write(put_name+": "+dt_str+"  -  ")
        f.close()
   
 
#퇴근시간 기록 #이름없이 눌리면 안되도록 수정해야함
def endlog():
    #cnt 초깃값 봐야됨
    global cnt
    global cnt2
    cnt=cnt-1
    if cnt<0:
        msgbox.showinfo("알림","출근 먼저 누르세요")
        cnt+=1
   
    else:
        now=dt.datetime.now()
        dt_str=(now.strftime('%H:%M'))
        global ed_time
        ed_time=(now.strftime('%H:%M')) ##종료 시간 킵, 문자형임.
        global cnt_edtime
        cnt_edtime=(dt.datetime.strptime(ed_time,'%H:%M'))
        f = open("출석로그.txt", 'a')
        f.write(dt_str)
        f.write("\n")
        f.close()
        realjson()
            

#json 파일 수정? -->> 참고용 실패 함수, 신경 쓰지 x
def modifyjson(new_data, filename='출석_로그.json'):
    with open(filename,'r+') as g:
        # First we load existing data into a dict.
        file_data = json.load(g)
        # Join new_data with file_data inside emp_details
        
        
        file_data.append(new_data)
        # Sets file's current position at offset.
        g.seek(0)
        # convert back to json.
        json.dump(file_data, g, indent = 2)

def realjson():
    now=dt.datetime.now()
    global dt_time
    dt_time=now.strftime("%y-%m-%d")
    global diff
    global diff_min
    diff=(cnt_edtime)-(cnt_stjsontime)
    diff_min=int(diff.seconds/60)  #분으로만 표시해줌

    
    try: 
        with open('출석_로그.json','r+') as g:
            file_data = json.load(g)
            if combox.get() not in file_data:
                        file_data[combox.get()] = {}
                    
                    # 현재 날짜가 이미 있는지 확인하고 없으면 초기화합니다.
            if dt_time not in file_data[combox.get()]:
                file_data[combox.get()][dt_time] = {
                    "출근시간": stjson_time,
                    "퇴근시간": ed_time,
                    "근무시간": diff_min
                }
                g.seek(0)
                json.dump(file_data, g, indent=2, ensure_ascii=False)
                g.truncate()  # 파일의 끝을 자릅니다.
            else:
                with open('출석_로그.json', 'r', encoding='utf-8') as m:
                    get_data = json.load(m)
                    new_sttime=get_data[combox.get()][dt_time]["출근시간"] #기존에 이름이 없으면 이 코드에서 오류가 남
                    cnt_newsttime=dt.datetime.strptime(new_sttime,"%H:%M")
                    new_diff=(cnt_edtime)-(cnt_newsttime) #시간:분 형식으로 표시
                    new_diffmin=int(new_diff.seconds/60) #분으로만 표시
                # 날짜가 이미 존재할 경우, 퇴근 시간만 업데이트합니다.
                file_data[combox.get()][dt_time]["퇴근시간"] = ed_time 
                #아래서부터 추가했음
                file_data[combox.get()][dt_time]["근무시간"] = new_diffmin #출근시간이 다시 눌리면서 마이너스가 근무시간 계산이 업데이트가 안됨.->해결
                    # 파일의 시작 부분으로 이동하여 기존 내용을 덮어씁니다.
                g.seek(0)
                json.dump(file_data,g,default=str,indent=2, ensure_ascii=False)
                g.truncate()  # 파일의 끝을 자릅니다.

    except FileNotFoundError:
        # 파일이 없으면 초기화된 데이터를 작성합니다.
        with open('출석_로그.json', 'w') as g:
            file_data = {
                combox.get(): {
                    dt_time: {
                        "출근시간": stjson_time,
                        "퇴근시간": ed_time,
                        "근무시간": diff_min
                    }
                }
            }
            json.dump(file_data, g, indent=2, ensure_ascii=False)  
    
    except json.decoder.JSONDecodeError:
        # 파일이 비어있거나 잘못된 형식인 경우, 기본 구조 반환
       with open('출석_로그.json', 'w') as g:
            file_data = {
                combox.get(): {
                    dt_time: {
                        "출근시간": stjson_time,
                        "퇴근시간": ed_time,
                        "근무시간": diff_min
                    }
                }
            }
            json.dump(file_data, g, indent=2, ensure_ascii=False)  
       


#json 파일 작성
def jsonlog():
    now=dt.datetime.now()
    global dt_time
    dt_time=str(now.date())
   ## time=(now.strftime('%H:%M'))
    g=open("출석_로그.json",'a',encoding='utf-8')
    '''data={
        combox.get():{ # 이름
            dt_time:[stjson_time,ed_time]
        }
    }'''
    ddata={}
    ddata[combox.get()]={}
    ddata[combox.get()][dt_time]=[]
    ddata[combox.get()][dt_time].append(stjson_time)
    ddata[combox.get()][dt_time].append(ed_time)
    json.dump(ddata,g,indent=2,ensure_ascii=False)

    g.close()
    ##이걸 그럼 퇴근시간을 눌렀을떄 발동되게끔?->로그랑, json 둘 다 기록되게끔


#비번 체크하는 함수
def pwcheck():

    def getpw(): #비번 가져오기
        global Rpw
        Rpw=1234
        pw=int(float(ent.get()))
        if (Rpw==pw):
            mng()
            root3.destroy()
            #비번 입력 창 한 번만 뜨게끔 해보기, 필요없을 수도
        else:
            msgbox.showwarning("경고","올바르지 않은 암호입니다.")

    global root3
    root3=tk.Tk() #비번 페이지
    root3.geometry("200x100")
    root3.title("관리자암호")
    root3.option_add("*Font","맑은고딕 17")
    root3.resizable(False,False)
    lbl=Label(root3,text="PW:")
    lbl.place(x=10,y=14)
    ent=Entry(root3,bd=2.5,width=10)
    root3.bind('<Return>',getpw) ##수정작업중
    ent.place(x=50,y=10)
    ck=Button(root3,width=7,text="확인")
    ck.place(x=60,y=60)
    ck.config(command=getpw)

'''#비번 변경 창
def pw_ch():
    Rpw=#엔트리에서 받아오기'''

#이름추가
def name_add():
    global name
    add_NM=peradd_ent.get()
    k = open("알바인원.txt", 'a')
    k.write(add_NM+"\n")
    k.close()

    with open('알바인원.txt','r',encoding='utf-8') as p:
        new_p=p.readlines()
        p.seek(0)
        for i in new_p:
            name.append(i)
    
    msgbox.showinfo("알림","추가되었습니다, 프로그램을 재시작하세요.")
    root2.destroy()
    root4.destroy()
    closing()

#이름 삭제
def name_del():
    global name
    NM=perdel_combox.get()
    with open('알바인원.txt','r+',encoding='utf-8')as n:
        new_n=n.readlines()
        n.seek(0)
        for line in new_n:
            if NM not in line:
                n.write(line)
        n.truncate()
    ##name.remove(NM)
    
    msgbox.showinfo("알림","삭제되었습니다")
    root2.destroy()
    root5.destroy()
    closing()

#날짜 조회
def date_range(start,stop):
    global dates
    global boxjson
    tottime=0

    dates = []
    diff = (stop-start).days
    for i in range(diff+1):
        day = start + timedelta(days=i)
        dates.append(day)
    if dates: 
        mngbox = mngcombox.get()  # 콤보박스에서 선택된 이름 가져오기
        with open('출석_로그.json', 'r', encoding='utf-8') as g:
            get_data = json.load(g)

            
            for widget in scrollable_frame.winfo_children(): ## 프레임에서 내용 안겹치게끔
                widget.destroy()

        for k in dates:
            date_str = k.strftime("%y-%m-%d")
            
            if mngbox in get_data and date_str in get_data[mngbox]:
                date_json = {
                            date_str: get_data[mngbox][date_str],

                        }

                global time_money,tottime_lbl,ex_tottime
                time_money=0
                #time_money += get_data[mngbox][date_str]["근무시간"]
                #cc=dt.datetime.strptime(get_data[mngbox][date_str]["근무시간"],"%H:%M")
                ccn=int(get_data[mngbox][date_str]["근무시간"])
                tottime+=ccn

                boxjson = json.dumps(date_json, indent=2, ensure_ascii=False)
                ex_tottime=json.dumps(tottime,indent=2,ensure_ascii=False)
                tottime_lbl.configure(text=f"근무시간:{ex_tottime}분")
                
                
            else:
                #boxjson=""
                continue
                #boxjson = f"날짜 {date_str}에 해당하는 기록이 없습니다." #날짜별로 내용이 없음을 알릴때
            ttk.Label(scrollable_frame, text=boxjson).pack() # 여기서 내용을 쏴주는 것임
            


    
    else:
        msgbox.showwarning('경고','시작날짜는 마지막 날짜보다 늦을 수 없으며, 마지막 날짜는 시작날짜보다 이를 수 없습니다.')

#비밀번호 변경 페이지
###def change_pw():
'''  global root7
    root7=tk.Tk()
    root7.geometry("300x100")
    root7.title("비밀번호 변경")
    root7.option_add("*Font","맑은고딕 17")
    root7.resizable(False,False)
    root7.configure(bg="lightgray")

    pw_ent=Entry(root7,bd=2.5,width=8,text="비번입력")
    pw_ent.place(x=20,y=30)
    ch_but=Button(root7,text="변경",width=7,command=)'''




#인원 추가 페이지  ## 결국 메모장에 넣고 불러와야 됨
def per_add():
    global root4
    root4=tk.Tk()
    root4.geometry("300x100")
    root4.title("인원 추가")
    root4.option_add("*Font","맑은고딕 17")
    root4.resizable(False,False)
    root4.configure(bg="lightgray")
    
    global peradd_ent
    
    peradd_ent=Entry(root4,bd=2.5,width=8,text="이름추가")
    peradd_ent.place(x=20,y=30)
    addbut=Button(root4,text="추가",width=7,command=name_add)
    addbut.place(x=200,y=30)


#인원 삭제 페이지
def per_del():
    global root5
    root5=tk.Tk()
    root5.geometry("300x100")
    root5.title("인원 삭제")
    root5.option_add("*Font","맑은고딕 17")
    root5.resizable(False,False)
    root5.configure(bg="lightgray")
    
    global perdel_combox

    perdel_combox=ttk.Combobox(root5)

            
    perdel_combox.config(height=6,width=8,values=name,state="readonly")
    perdel_combox.set("이름")
    perdel_combox.place(x=20,y=30)
    delbut=tk.Button(root5,text="삭제",width=7,command=name_del)
    delbut.place(x=200,y=30)
    
##->알바비 계산
def calc_money():
    global root6
    root6=tk.Tk()
    root6.geometry("300x100")
    root6.title("근무시간 확인")
    root6.option_add("*Font","맑은고딕 17")
    root6.resizable(False,False)
    root6.configure(bg="lightgray")


'''### 총 근무시간 표시
def work_time():
    tottime_lbl=tk.Label(root2,text="총 xx분",bg="lightgray")
    tottime_lbl.place(x=50,y=650)'''
    

#관리자 페이지
def mng(): 
    global root2
    root2=tk.Tk() 
    root2.geometry("1200x700")
    root2.title("관리자 페이지")
    root2.option_add("*Font","맑은고딕 17")
    root2.resizable(False,False)
    root2.configure(bg="lightgray")
    
    
    #이름 콤보박스
    global mngcombox
    mngcombox=ttk.Combobox(root2)
    mngcombox.config(height=5,width=10,values=name,state="readonly")
    mngcombox.set("이름")
    mngcombox.place(x=50,y=40)

    #시작날짜, 종료날짜
   
    #띄어쓰기 말고 사용할 방법은 없을까?
    lbl=tk.Label(root2,text="     시작날짜:",bg="lightgray")
    lbl.place(x=280,y=40)

    lbl2=tk.Label(root2,text="     종료날짜:",bg="lightgray")
    lbl2.place(x=600,y=40)

    lbl3=tk.Label(root2,text="~",width=2,bg="lightgray")
    lbl3.place(x=580,y=40)

    date1 = tkc.DateEntry(root2)
    date1.place(x=380,y=40)

    date2 = tkc.DateEntry(root2)
    date2.place(x=700,y=40)

    #조회버튼
    ckbtn=tk.Button(root2,text='조회',width=8,command=lambda: date_range(date1.get_date(),date2.get_date()))
    ckbtn.place(x=910,y=40)


    #출석 로그 표시
    log=tk.LabelFrame(root2,text="출석 로그",font=("맑은고딕",20) ,width=800, height=500, border=10)
    log.place(x=200,y=105)
    #showjson() #log 보여주려고 키는 함수

    container = ttk.Frame(log)
    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    global scrollable_frame
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    #스크롤 창 크기 조절
    canvas.configure(yscrollcommand=scrollbar.set,width=770, height=490)


    
    #ttk.Label(scrollable_frame, text=boxjson).pack()

    container.place(x=0,y=0)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    ##---총 근무시간 표시
    global tottime, ex_tottime, tottime_lbl
    
    tottime_lbl=tk.Label(root2,text=f"근무시간:{tottime}",bg="white")
    tottime_lbl.place(x=200,y=630)

    '''#비밀번호 변경 페이지 열기
    chpw_btn=tk.Button(root2,text='비밀번호 변경',width=7,command=ch_pw)
    chpw_btn.place(x=810,y=650)'''
    
    
    #사람 추가 페이지 열기
    per_addbtn=tk.Button(root2,text="사람추가",width=7,command=per_add)
    per_addbtn.place(x=910,y=650)
    #사람 삭제 페이지 열기
    per_delbtn=tk.Button(root2,text="사람삭제",width=7,command=per_del)
    per_delbtn.place(x=1010,y=650)

def main():
    #메인 창
    global root
    root=tk.Tk() 
    root.geometry("600x400")
    root.title("더모어 출결관리")
    root.option_add("*Font","맑은고딕 17")
    root.resizable(False,False)
    root.configure(bg="lightgray")

    #파일 없을시 생성
    mkfile()

    global name
    name=[] # 리스트화 해서 하나씩 추가할 수 있게끔 기능만들기 
    with open('알바인원.txt','r',encoding='utf-8') as p:
            new_p=p.readlines()
            p.seek(0)
            for i in new_p:
                name.append(i)

    global combox
    combox=ttk.Combobox(root)
    combox.config(height=5,width=10,values=name,state="readonly")
    combox.set("이름")
    combox.place(x=40,y=50)
    toss=combox.get() #임시

    btns=Button(root,width=8,text="출근", overrelief="solid")
    btns.place(x=370, y=50)
    btns.config(command=startlog)

    btne=Button(root,width=8,text="퇴근", overrelief="solid")
    btne.place(x=470, y=50)
    btne.config(command=endlog)

    manage=Button(root,width=8,text="관리자",overrelief="solid")
    manage.place(x=450, y=350)
    manage.config(command=pwcheck)


        
    root.mainloop()

main()