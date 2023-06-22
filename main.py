'''
모듈 불러오기
'''
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random as rand
import tkinter.messagebox
'''
변수 선언
'''
year = 2023
month = 3
day = 2
money = 5000000
goal = 10000000
count = 0
now_stock = 0
start_money = 5000000
goal = 0
who = 0
what = {"신기술 개발을 시도(실패)" : (0,-5), "신기술 개발을 시도(성공)" : (5,15), "ceo 교체(실패)" : (-3,-8), "ceo 교체(성공)" : (8,18), "주식 가격이 내려가(개미)" : (0, 0),"주식 가격이 내려가(진짜)" : (-10,-20)}
'''
함수 선언
'''
def monthCheck(month):
        thirtyone = [1,3,5,7,8,10,12]
        twentysix = 26
        if month in thirtyone:
            return 31
        elif month == twentysix:
            return 26
        else:
            return 30
def update_date():
        global count, day, month, year
        day += 1
        if monthCheck(month) < day:
            month += 1
            day = 1
            if month > 12:
                year += 1
                month = 1
'''
프레임 만들기
'''
# 시작 페이지
class StartPage(tk.Frame):
    def __init__(self, master):
        super(StartPage, self).__init__(master)
        self.label = tk.Label(self, text="목표 금액을 입력하세요")
        self.label.pack()
        self.input_goal = tk.Entry(self)
        self.input_goal.pack()
        self.button = tk.Button(self, text="시작하기", command=self.start)
        self.button.pack()
    def start(self):
        global goal
        try:
            goal = int(self.input_goal.get())
            if goal <= 5000000:
                tkinter.messagebox.showinfo("경고", "5000000 초과 금액만 입력해 주세요")
                return
        except:
            tkinter.messagebox.showinfo("경고", "숫자만 입력하세요")
            return
        self.pack_forget()
        stock[now_stock].pack()
        button_bar.pack()

#목표 달성 페이지
class GoalPage(tk.Frame):
    def __init__(self, master):
        super(GoalPage, self).__init__(master)
        self.label = tk.Label(self, text="축하드립니다. 목표에 달성 하셨습니다")
        self.money_label = tk.Label(self, text=f"최종 금액{money} {count}일")
        self.button = tk.Button(self, text="나가기", command=app.quit)
        self.label.pack()
        self.money_label.pack()
        self.button.pack()
    def update_label(self):
        self.money_label.config(text=f"최종 금액{money} {count}일")
        self.update()

#주식 프레임
class Stock(tk.Frame):
    def __init__(self,master, name, stock_price, low, high):
        super(Stock, self).__init__(master)
        #변수 선언 부분
        self.low = low
        self.high = high
        self.number = 0
        self.price = [['2023-3-1','2023-3-2'],[stock_price,stock_price]]
        #위젯 선언
        self.name = name[:-4]
        self.stock_name = tk.Label(self, text=name)
        self.rise_fall = tk.Label(self, text=f"{low}% ~ {high - 1}%")
        self.price_label = tk.Label(self, text=f"현재 주식 금액 : {self.price[1][-1]}")
        self.money_label = tk.Label(self, text=f"보유금액 : {money}")
        self.number_label = tk.Label(self, text=f"주식 보유 개수 : {self.number}")
        self.buy_input = tk.Entry(self)
        self.buy_input.insert(0, money//self.price[1][-1])
        self.sell_input = tk.Entry(self)
        self.sell_input.insert(0, str(self.number))
        self.buy_button = tk.Button(self,text="BUY", command=self.buy)
        self.sell_button = tk.Button(self,text="SELL", command=self.sell)


        #주식 그래프 선언
        self.figure = Figure(figsize=(5,4), dpi=100)
        self.plot = self.figure.add_subplot(1,1,1)
        self.plot.plot(self.price[0],self.price[1])
        self.plot.set_xticks([])
        self.plot.set_xticklabels([])
        self.plot.set_xlabel('')
        self.grape = FigureCanvasTkAgg(self.figure, master=self)
        self.grape.draw()


        #위젯 배치하기
        self.stock_name.pack()
        self.rise_fall.pack()
        self.grape.get_tk_widget().pack()
        self.price_label.pack()
        self.money_label.pack()
        self.number_label.pack()
        self.buy_input.pack(side="left")
        self.sell_input.pack(side="right")
        self.buy_button.pack(side="left")
        self.sell_button.pack(side="right")

    #함수 선언 부분
    def update_grape(self):
        def update_price():
            plus_minus = rand.randrange(self.low,self.high) if self.price[1][-1] > self.price[1][0]//5 else rand.randrange(self.low//2,self.high*2)
            self.price[0].append(f"{year}-{month}-{day}")
            self.price[1].append(int(self.price[1][-1]*((100 + plus_minus) / 100)))
            self.price_label.config(text=f"현재 주식 금액 : {self.price[1][-1]}")
            self.price_label.pack()
        def draw_grape():
            if len(self.price[1]) > 30:
                self.price[1].pop(0)
                self.price[0].pop(0)
            self.plot.clear()
            self.plot.plot(self.price[0],self.price[1])
            self.plot.set_xticks([])
            self.plot.set_xticklabels([])
            self.plot.set_xlabel('')
            self.grape.draw()
        update_price()
        draw_grape()
        self.price_label.config()
        app.update()



    def buy(self):
        global money
        #입력 데이터 검사
        if self.buy_input.get() == "": n = 1
        else:
            try:
                n = int(self.buy_input.get())
            except:
                tkinter.messagebox.showinfo("경고","숫자만 입력해 주세요")
                return
        if n <= 0:
            tkinter.messagebox.showinfo("경고","1이상만 입력해 주세요")
            return
        if self.price[1][-1] * n > money: 
            tkinter.messagebox.showinfo("겅고","돈이 부족합니다")
            return
        
        #구매 기능
        money -= self.price[1][-1] * n
        self.number += n
        self.number_label.config(text=f"주식 보유 개수 : {self.number}")
        self.money_label.config(text=f"보유금액 : {money}")

        #입력창 업데이트
        for i in range(len(stock)):
            stock[i].updateInput()

        app.update()
    def sell(self):
        global money
        try:
            n = int(self.sell_input.get())
            if n <= 0:
                tkinter.messagebox.showinfo("경고","숫자만 입력해주세요")
                return
        except:
            tkinter.messagebox.showinfo("경고","숫자만 입력해주세요")
            return
        if self.number < n:
            tkinter.messagebox.showinfo("경고","보유 개수가 부족합니다")
            return
        money += self.price[1][-1] * n
        self.number -= n
        for i in range(len(stock)):
            stock[i].number_label.config(text=f"주식 보유 개수 : {self.number}")
            stock[i].money_label.config(text=f"보유금액 : {money}")
        for i in range(len(stock)):
            stock[i].updateInput()
        app.update()
    def updateInput(self):
        self.buy_input.delete(0, tk.END)
        self.sell_input.delete(0, tk.END)
        self.buy_input.insert(0, money//self.price[1][-1])
        self.sell_input.insert(0, self.number)
        app.update()

#버튼 바 프레임
class ButtonBar(tk.Frame):
    def __init__(self, master):
        super(ButtonBar, self).__init__(master)
        #위젯 설정
        self.behind_stock = tk.Button(self, text="뒷 주식", command=self.behindStock)
        self.front_stock = tk.Button(self, text="앞 주식", command=self.frontStock)
        self.next_day = tk.Button(self, text="다음 날", command=self.changeBill)

        #위젯 배치
        if now_stock == 0:
            self.behind_stock.pack_forget()
        else:
            self.behind_stock.pack(side="left")
        if now_stock == 3:
            self.front_stock.pack_forget()
        else:
            self.front_stock.pack(side="right")
        self.next_day.pack(side="bottom")

    #함수 선언
    def frontStock(self):
        global now_stock
        stock[now_stock].pack_forget()
        button_bar.pack_forget()
        now_stock += 1
        stock[now_stock].pack()
        button_bar.pack()
        if now_stock == len(stock) - 1:
            self.front_stock.pack_forget()
        else:
            self.behind_stock.pack_forget()
            self.front_stock.pack_forget()
            self.next_day.pack_forget()
            self.behind_stock.pack(side="left")
            self.front_stock.pack(side="right")
            self.next_day.pack()
        app.update()

    def behindStock(self):
        global now_stock
        stock[now_stock].pack_forget()
        button_bar.pack_forget()
        now_stock -= 1
        stock[now_stock].pack()
        button_bar.pack()
        if now_stock == 0:
            self.behind_stock.pack_forget()
        else:
            self.behind_stock.pack_forget()
            self.front_stock.pack_forget()
            self.next_day.pack_forget()
            self.behind_stock.pack(side="left")
            self.front_stock.pack(side="right")
            self.next_day.pack()
        app.update()

    def changeBill(self):
        global count,who,what
        update_date()
        for i in range(len(stock)):
            stock[i].updateInput()
        if goal <= money:
            goal_page.update_label();goal_page.pack();stock[now_stock].pack_forget();button_bar.pack_forget()
        if count % 7 == 0 and count != 0:
            bill.updateNews(1,rand.choice(stock),rand.choice(list(what.keys()))) if rand.randrange(0,2) == 1 else bill.updateNews(0)
            for i in range(len(stock)):
                stock[i].update_grape()
            stock[now_stock].pack_forget();button_bar.pack_forget();bill.updateRealMoney();bill.pack()
        else:
            for i in range(len(stock)):
                stock[i].update_grape()
        count += 1
        app.update()
    
#영수증 페이지
class Bill(tk.Frame):
    def __init__(self, master):
        global start_money, money
        self.real_money = haman.number * haman.price[1][-1] + jungman.number * jungman.price[1][-1] + sangman.number * sangman.price[1][-1] + money
        super(Bill, self).__init__(master)
        #위젯 설정
        self.rate_label = tk.Label(self, text=f"수익 {self.real_money - start_money}, 수익율 {(self.real_money - start_money)/start_money * 100}%")
        self.next_day_button = tk.Button(self, text="다음 날", command=self.nextDay)
        self.news = tk.Label(self, text="")
        self.real_news = tk.Label(self, text="")
        #위젯 배치
        self.rate_label.pack()
        self.next_day_button.pack()
        self.updateLabel()
    #함수 선언
    def updateLabel(self):
        self.rate_label.config(text=f"수익 {self.real_money - start_money}, 수익율 {(self.real_money - start_money)/start_money * 100}%")
        app.update()
        self.after(10, self.updateLabel)
        self.update()
    def nextDay(self):
        global start_money, stock, now_stock, count
        start_money = haman.number * haman.price[1][-1] + jungman.number * jungman.price[1][-1] + sangman.number * sangman.price[1][-1] + money
        count += 1
        self.pack_forget()
        start_money = start_money = haman.number * haman.price[1][-1] + jungman.number * jungman.price[1][-1] + sangman.number * sangman.price[1][-1] + money
        stock[now_stock].pack()
        button_bar.pack()
        self.updateRealNews()
    def updateRealMoney(self):
        self.real_money = haman.number * haman.price[1][-1] + jungman.number * jungman.price[1][-1] + sangman.number * sangman.price[1][-1] + money
    def updateNews(self, do, who = "",news = ""):
        haman.low = -5;haman.high = 6
        jungman.low = -25;jungman.high = 26
        sangman.low = -50;sangman.high = 51
        self.do = do
        if do == 0:
            self.news.pack_forget()
        else:
            self.what_news = news
            self.who_news = who
            self.news.config(text=f"속보 - {who.name}기업이 {news[:-4]}")
            who.low += what[news][0]
            who.high += what[news][1]
            self.news.pack()
        app.update()
    def updateRealNews(self):
        self.real_news.config(text=f"속보 - {self.who_news.name}기업이 {self.what_news}")
        self.real_news.pack()
        app.update()
            
'''
메인 코드
'''
#기본 설정
app = tk.Tk()
app.title("주식게임")
app.geometry("600x600")

#프레임 생성
haman = Stock(app, "유리심장의 주식", 50000, -5, 6)
jungman = Stock(app, "고무심장의 주식", 25000, -25, 26)
sangman = Stock(app, "강철심장의 주식", 5000, -50, 51)
# bitcoin = Stock(app, "비트코인", 100, -99, 100)
button_bar = ButtonBar(app)
bill = Bill(app)
start_page = StartPage(app)
stock = [haman, jungman, sangman]
goal_page = GoalPage(app)

#시작페이지 실행
start_page.pack()

#실행
app.mainloop()