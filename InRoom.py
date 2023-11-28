from Enum import *
from Man import _man, _pocardsstyle
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.label import Label
import numpy as np
import random
import pyautogui
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.image import Image
#-----------------------------------------size-----------------------------
# W,H=800,600 
W,H=pyautogui.size() 
CX,CY=W/2,H/2
rateW=W/1366
rateH=H/768
card_maxsize=[100*rateH,150*rateH]
card_minsize=[50*rateH,75*rateH]
# card_minsize=[100*rateH,120*rateH]

#-----------------------------------------whidget------------------------
class ManWidget(Button):
    pass
class CardBoard(Button):
    pass
class ButWidget(Button):
    def ClickAnimation(self):
        Animation.cancel_all(self)
        target_x = self.pos[0]
        target_y = self.pos[1]
        anim = Animation(x = target_x, y = target_y, duration = 0.3,t ='out_quad')
        anim.start(self)
    def ClickHelpWndAnimation(self,state):
        Animation.cancel_all(self)
        if state:
            anim = Animation(x = 0, y = 0, duration = 0.3,t ='out_quad')
        else:
            anim = Animation(x = -W-10, y = 0, duration = 0.5,t ='out_quad')
        anim.start(self)        
class CardWidget(Button):
    ID=9999
    def SelectAnimation(self, selected):
        Animation.cancel_all(self)
        target_x = self.pos[0]
        if selected==CS_SELECT: target_y = self.pos[1]-20*rateH
        else: target_y = self.pos[1]+20*rateH
        anim = Animation(x = target_x, y = target_y, duration = 0.3,t ='out_quad')
        anim.start(self)
    def PutoutAnimation(self,target_pos):
        Animation.cancel_all(self)
        anim = Animation(x = target_pos[0], y = target_pos[1], size=(150*rateH,150*rateH), duration = 0.3,t ='out_quad')
        anim.start(self)
class GameRoom(Widget):
#-----------------------------------------init----------------------------
    def __init__(self, **kwargs):
        super(GameRoom, self).__init__(**kwargs)
        self.initPrice=100
        self.whoIsTurn=random.randint(0,2)
        self.man=_man()
        self.cpu1=_man()
        self.cpu2=_man()
        self.Init()
        self.BuildingUI()
    def BuildingUI(self):      
        self.ManWidget1=ButWidget(pos=[W/20,H/10],size=(150*rateH,150*rateH),background_normal='data/mans/man1n.png',background_down='data/mans/man1d.png')
        self.add_widget(self.ManWidget1)
        self.ManWidget2=ButWidget(pos=[W/10,7*H/9],size=(150*rateH,150*rateH),background_normal='data/mans/man2n.png',background_down='data/mans/man2d.png')
        self.add_widget(self.ManWidget2)
        self.ManWidget3=ButWidget(pos=[9*W/10-150*rateH,7*H/9],size=(150*rateH,150*rateH),background_normal='data/mans/man3n.png',background_down='data/mans/man3d.png')
        self.add_widget(self.ManWidget3)
        self.PlayWidget=ButWidget(pos=[W-100*rateH,H/22],size=(60*rateH,60*rateH),on_release=self.OnPlay,background_normal='data/buttons/but_playn.png',background_down='data/buttons/but_playd.png')
        self.add_widget(self.PlayWidget)
        self.CloseWidget=ButWidget(pos=[W-100*rateH,H*10/11],size=(60*rateH,60*rateH),on_release=self.OnClose,background_normal='data/buttons/but_closen.png',background_down='data/buttons/but_closed.png')
        self.add_widget(self.CloseWidget)
        self.ManSpeakWidget1=Label(pos=[W/8.5,H/5],size=(150*rateH,150*rateH),text='')
        self.add_widget(self.ManSpeakWidget1)
        self.ManSpeakWidget2=Label(pos=[W/5.5,7.5*H/9],size=(150*rateH,150*rateH),text='')
        self.add_widget(self.ManSpeakWidget2)
        self.ManSpeakWidget3=Label(pos=[8*W/10-150*rateH,7.5*H/9],size=(150*rateH,150*rateH),text='')
        self.add_widget(self.ManSpeakWidget3)    
        self.ManName1=Label(pos=[W/12,H/5],size=(150*rateH,150*rateH),text='annop:')
        self.add_widget(self.ManName1)
        self.ManName2=Label(pos=[W/7,7.5*H/9],size=(150*rateH,150*rateH),text='marsh:')
        self.add_widget(self.ManName2)
        self.ManName3=Label(pos=[8.5*W/10-150*rateH,7.5*H/9],size=(150*rateH,150*rateH),text=':lena')
        self.add_widget(self.ManName3)     
        self.DoWidget1=Label(pos=[W/12,H/7],size=(150*rateH,150*rateH),text='')
        self.add_widget(self.DoWidget1)
        self.DoWidget2=Label(pos=[W/7,7*H/9],size=(150*rateH,150*rateH),text='')
        self.add_widget(self.DoWidget2)
        self.DoWidget3=Label(pos=[8.5*W/10-150*rateH,7*H/9],size=(150*rateH,150*rateH),text='')
        self.add_widget(self.DoWidget3)
        self.PriceWidget=ButWidget(pos=[W/2-200*rateH,8*H/9],size=(400*rateH,45*rateH),text="price:"+str(self.initPrice),background_normal='data/buttons/but_pricen.png',background_down='data/buttons/but_priced.png')
        self.add_widget(self.PriceWidget)
        self.butSuggest=ButWidget(pos=[2*W/3-100*rateH,H/3],size=(100*rateH,45*rateH),on_release=self.OnSuggest,background_normal='data/buttons/but_suggestn.png',background_down='data/buttons/but_suggestd.png')
        self.add_widget(self.butSuggest)
        self.butPass=ButWidget(pos=[W/3,H/3],size=(100*rateH,50*rateH),on_release=self.OnPass,background_normal='data/buttons/but_passn.png',background_down='data/buttons/but_passd.png')
        self.add_widget(self.butPass)
        self.CardBoard=ButWidget(pos=[CX-250*rateH,CY-85*rateH],size=(500*rateH,200*rateH),background_normal='data/backgrounds/cardboard.png',background_down='data/backgrounds/cardboard.png')
        self.add_widget(self.CardBoard)
        self.HelpButWidget=ButWidget(pos=[10,10*H/11],size=(60*rateH,60*rateH),on_release=self.OnClickHelpBut,background_normal='data/buttons/but_helpn.png',background_down='data/buttons/but_helpd.png')
        self.add_widget(self.HelpButWidget)
        self.manCardWidgets=[]
        self.cpu1CardWidgets=[]
        self.cpu2CardWidgets=[]
        self.cpu1CardBKWidgets=[]
        self.cpu2CardBKWidgets=[]
        for i in range(self.man.cardN):
            file='data/card_set/card'+str(self.man.cards[i].cardId)+'.png'
            card=CardWidget(pos=[W/4+40*rateW*i,H/9],size=card_maxsize,on_release=self.OnClickCard,background_normal=file,background_down=file)
            card.ID=i
            self.manCardWidgets.append(card)
            self.add_widget(card)
        for i in range(self.cpu1.cardN):
            file='data/card_set/card'+str(self.cpu1.cards[i].cardId)+'.png'
            card=CardWidget(pos=[W/10+20*rateW*i,6*H/9],size=card_minsize,background_normal=file,background_down=file)            
            self.cpu1CardWidgets.append(card)
            self.add_widget(card)
        for i in range(self.cpu2.cardN):
            file='data/card_set/card'+str(self.cpu2.cards[i].cardId)+'.png'
            card=CardWidget(pos=[4.4*W/7+20*rateW*i,6*H/9],size=card_minsize,background_normal=file,background_down=file)            
            self.cpu2CardWidgets.append(card)
            self.add_widget(card)
        for i in range(self.cpu1.cardN):
            file='data/card_set/card54.png'
            card=CardWidget(pos=[W/10+20*rateW*i,6*H/9],size=card_minsize,background_normal=file,background_down=file)            
            self.cpu1CardBKWidgets.append(card)
            self.add_widget(card)
        for i in range(self.cpu2.cardN):
            file='data/card_set/card54.png'
            card=CardWidget(pos=[4.4*W/7+20*rateW*i,6*H/9],size=card_minsize,background_normal=file,background_down=file)            
            self.cpu2CardBKWidgets.append(card)
            self.add_widget(card)
        self.HelpWndWidget=ButWidget(pos=[-W-10,0],size=(W,H),on_release=self.OnClickHelpWnd,background_normal='data/backgrounds/helpwnd.png',background_down='data/backgrounds/helpwnd.png')
        self.add_widget(self.HelpWndWidget) 
    def RemveCardsWidget(self):    
        self.remove_widget(self.ManWidget1)
        self.remove_widget(self.ManWidget2)
        self.remove_widget(self.ManWidget3)
        self.remove_widget(self.PlayWidget)
        self.remove_widget(self.CloseWidget)
        self.remove_widget(self.ManSpeakWidget1)
        self.remove_widget(self.ManSpeakWidget2)
        self.remove_widget(self.ManSpeakWidget3)    
        self.remove_widget(self.ManName1)
        self.remove_widget(self.ManName2)
        self.remove_widget(self.ManName3)     
        self.remove_widget(self.DoWidget1)
        self.remove_widget(self.DoWidget2)
        self.remove_widget(self.DoWidget3)
        self.remove_widget(self.PriceWidget)
        self.remove_widget(self.butSuggest)
        self.remove_widget(self.butPass)
        self.remove_widget(self.CardBoard)
        self.remove_widget(self.HelpButWidget)
        for it in self.manCardWidgets:
            self.remove_widget(it)  
        for it in self.cpu1CardWidgets:
            self.remove_widget(it) 
        for it in self.cpu2CardWidgets:
            self.remove_widget(it) 
        for it in self.cpu1CardBKWidgets:
            self.remove_widget(it) 
        for it in self.cpu2CardBKWidgets:
            self.remove_widget(it) 
        self.remove_widget(self.HelpWndWidget) 
    def Init(self):
        self.Price=self.initPrice
        self.isBetting=False
        self.isBeginOrEndOrPlaying=GS_BEGIN
        self.prevPOCardStyle=_pocardsstyle()
        self.whoIsMain=0
        self.whoIsTurn+=1
        self.whoIsTurn%=3
        self.whoIsStrong=0
        self.man.IsMain=True
        self.firstRest3Cards=[]
        self.cardsState=np.ones(54)
        self.DistributeCardsToMans()
        self.man.SetCardsState(CS_UNSELECT)
        self.cpu1.SetCardsState(CS_UNSELECT)
        self.cpu2.SetCardsState(CS_UNSELECT)
    def DistributeCardsToMans(self):
        self.man.InitCards()
        self.cpu1.InitCards()
        self.cpu2.InitCards()
        fl=list(range(0,54))
        lst=random.sample(fl,17)
        # lst=[17,13,26,39,1,14,27,40,2,15,28,41,3,16,29,42,4]
        self.man.SetCardsId(lst)
        sl=[i for i in fl if i not in lst]
        lst=random.sample(sl,17)
        # lst=[34,9,43,5,18,31,44,6,19,32,45,7,20,33,46,8,21]
        self.cpu1.SetCardsId(lst)
        tl=[i for i in sl if i not in lst]
        lst=random.sample(tl,17)
        # lst=[0,47,30,22,35,48,10,23,36,49,11,24,37,50,12,25,38]
        self.cpu2.SetCardsId(lst)
        self.Rest3Cards=[i for i in tl if i not in lst]
        rnd=random.randint(0,2)
        match rnd:
            case 0:
                self.man.AddRest3CardsId(self.Rest3Cards)
                self.man.cardN=20
            case 1:
                self.cpu1.AddRest3CardsId(self.Rest3Cards)
                self.cpu1.cardN=20
            case 2:
                self.cpu2.AddRest3CardsId(self.Rest3Cards)
                self.cpu2.cardN=20
        self.man.SortCard()
        self.cpu1.SortCard()
        self.cpu2.SortCard()
#---------------------------------------event-----------------------------
    def OnClickHelpWnd(self,instance):
        self.HelpWndWidget.ClickHelpWndAnimation(0)
    def OnClickHelpBut(self,instance):
        self.HelpWndWidget.ClickHelpWndAnimation(1)
    def OnPlay(self,instance):
        if self.isBeginOrEndOrPlaying==GS_BEGIN:
            self.isBeginOrEndOrPlaying=GS_PLAYING
            Clock.schedule_interval(self.MainProccess,1)
    def OnClose(self,instance):
        App.get_running_app().stop()
        # App.get_running_app().root.OnPlay()
    def OnClickCard(self,instance):
        card=self.man.cards[instance.ID]
        state=card.state
        if state==CS_UNSELECT:
            instance.SelectAnimation(CS_UNSELECT)
            card.state=CS_SELECT
        elif state==CS_SELECT:
            instance.SelectAnimation(CS_SELECT)
            card.state=CS_UNSELECT  
    def OnPass(self,instance):
        # self.ManWidget1.source='data/mans/man2n.png'
        # self.ManWidget1.source=Image(source='data/mans/man2n.png')
        whoIsWin=self.IsEnd()
        if whoIsWin!=-1:
            self.End(whoIsWin)
            return
        self.FreeSelectedCardsAnimation(self.man,self.manCardWidgets)
        if self.whoIsTurn!=0: 
            return
        self.whoIsTurn=1
        self.man.noPOCards=False
        self.ManSpeakWidget1.text="pass"
    def OnSuggest(self,instance):
        if self.whoIsTurn>0: return
        self.butSuggest.ClickAnimation()
        self.ManProceed()
    def PutoutCardsAnimation(self,obj,cardWidgets,cardBKWidgets):
        lst=[]
        for i in range(obj.cardN):
            if obj.cards[i].state==CS_SELECT:
                obj.cards[i].state=CS_PUTOUT
                lst.append(i)
        L=CX-len(lst)/2*40*rateW-50*rateH
        it=0
        for i in lst:
            target_pos=[L+40*rateW*it,CY-60*rateH]
            it+=1
            cardWidgets[i].PutoutAnimation(target_pos)
        Clock.schedule_once(lambda dt:self.RemovePOCards(lst,cardWidgets,cardBKWidgets),2)
    def RemovePOCards(self,lst,cardWidgets,cardBKWidgets):
        for i in lst:
            self.remove_widget(cardWidgets[i])
            if len(cardBKWidgets)!=0: self.remove_widget(cardBKWidgets[i])
        self.POCards=[]
    def FreeSelectedCardsAnimation(self,obj,cardWidgets):
        for i in range(obj.cardN):            
            if obj.cards[i].state==CS_SELECT:
                cardWidgets[i].SelectAnimation(CS_SELECT)
                obj.cards[i].state=CS_UNSELECT
#---------------------------------------game manage-----------------------
    def MainProccess(self, *largs):
        whoIsWin=self.IsEnd()
        if whoIsWin!=-1:
            self.End(whoIsWin)
            return
        match self.whoIsTurn:
            case 0:
                self.cpu1.noPOCards=True
                self.cpu2.noPOCards=True
            case 1:
                self.CpuProceed() 
                self.man.noPOCards=True
                self.cpu2.noPOCards=True
            case 2:
                self.CpuProceed()
                self.man.noPOCards=True
                self.cpu1.noPOCards=True
        if self.man.noPOCards==True:
            self.ManSpeakWidget1.text=""
        else:
            self.ManSpeakWidget1.text="pass"
        if self.cpu1.noPOCards==True:
            self.ManSpeakWidget2.text=""
        else:
            self.ManSpeakWidget2.text="pass"
        if self.cpu2.noPOCards==True:
            self.ManSpeakWidget3.text=""
        else:
            self.ManSpeakWidget3.text="pass"
        self.PriceWidget.text="price:"+str(self.Price)
        self.DoWidget1.text=str(self.man.DoNums)
        self.DoWidget2.text=str(self.cpu1.DoNums)
        self.DoWidget3.text=str(self.cpu2.DoNums)
    def ManProceed(self):
        if self.whoIsTurn==self.whoIsStrong:
            self.prevPOCardStyle=_pocardsstyle()
        chStyle=self.man.ManPOCards(self.prevPOCardStyle)
        if chStyle.T==-1: 
            self.FreeSelectedCardsAnimation(self.man,self.manCardWidgets)
            return False
        if chStyle.T==CST_4 or chStyle.T==CST_SW:
            self.Price*=2
            self.PriceWidget.text="price:"+str(self.Price)
        self.whoIsStrong=self.whoIsTurn
        self.whoIsTurn=self.WhoIsNext() 
        self.prevPOCardStyle=chStyle
        self.PutoutCardsAnimation(self.man,self.manCardWidgets,[])
        return True
    def CpuProceed(self):
        self.POCards=[]
        obj=_man()
        cardWidgets=[]
        cardBKWidgets=[]
        if self.whoIsTurn==1:
            obj=self.cpu1
            cardWidgets=self.cpu1CardWidgets
            cardBKWidgets=self.cpu1CardBKWidgets
        else:
            obj=self.cpu2
            cardWidgets=self.cpu2CardWidgets
            cardBKWidgets=self.cpu2CardBKWidgets
        if self.whoIsTurn==self.whoIsStrong:
            self.prevPOCardStyle=_pocardsstyle() 
        chStyle=obj.CpuPOCards(self.prevPOCardStyle)
        if chStyle.T==-1: 
            obj.FreeSelectedCards()  
            if self.whoIsTurn==1:
                self.cpu1.noPOCards=False 
            if self.whoIsTurn==2:
                self.cpu2.noPOCards=False
            self.whoIsTurn=self.WhoIsNext()
            return        
        if chStyle.T==CST_4 or chStyle.T==CST_SW:
            self.Price*=2
            self.PriceWidget.text="price:"+str(self.Price)
        self.whoIsStrong=self.whoIsTurn
        self.whoIsTurn=self.WhoIsNext() 
        self.prevPOCardStyle=chStyle
        self.PutoutCardsAnimation(obj,cardWidgets,cardBKWidgets)
    def WhoIsPrev(self):
        match self.whoIsTurn:
            case 0:
                return 2
            case 1:
                return 0
            case 2:
                return 1
    def WhoIsNext(self):
        match self.whoIsTurn:
            case 0:
                return 1
            case 1:
                return 2
            case 2:
                return 0
    def End(self,whoIsWin):
        self.isBeginOrEndOrPlaying=GS_END
        print('Game is over!')
        match whoIsWin:
            case 0:
                self.man.DoNums+=int(self.Price*0.8)
            case 1:
                self.cpu1.DoNums+=int(self.Price*0.8)
            case 2:
                self.cpu2.DoNums+=int(self.Price*0.8)
        self.Init()
        self.RemveCardsWidget() 
        self.BuildingUI()  
        self.PriceWidget.text=str(self.Price)
        self.DoWidget1.text=str(self.man.DoNums)
        self.DoWidget2.text=str(self.cpu1.DoNums)
        self.DoWidget3.text=str(self.cpu2.DoNums)
    def IsEnd(self):
        if self.man.HowMuchCards()==0: 
            return 0
        if self.cpu1.HowMuchCards()==0: 
            return 1
        if self.cpu2.HowMuchCards()==0: 
            return 2
        return -1        

class InRoomApp(App):
    def build(self):         
        return GameRoom()

Window.fullscreen = 'auto'
if __name__=="__main__":
    game=InRoomApp()
    game.run() 