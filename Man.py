from Enum import *
import numpy as np

class _card:
    def __init__(self, cardId=9999, state=CS_UNSELECT, src=''):
        self.cardId=cardId
        self.state=state
        self.src=src
    def get(self, cardId=9999, state=CS_UNSELECT, src=''):
        self.cardId=cardId
        self.state=state
        self.src=src
    def type(self):
        if self.cardId == 9999:
            return -1;
        elif self.cardId == 53:
            return CT_W;
        elif self.cardId == 52:
            return CT_S;
        else:
            return self.cardId//13
    def val(self):
        if self.cardId == 9999:
            return 9999;
        elif self.cardId == 53:
            return CV_W;
        elif self.cardId == 52:
            return CV_S;
        else:
            if self.cardId%13==12: return CV_2
            return self.cardId%13;
class _pocardsstyle:
    def __init__(self, T=-1, F=-1, S=-1, R=-1):
        self.T=T;
        self.F=F;
        self.S=S;
        self.R=R;
    def get(self, T, F, S, R):
        self.T=T;
        self.F=F;
        self.S=S;
        self.R=R;
class _man:
    def __init__(self):
        self.IsMain=False
        self.cards=[]
        self.DoNums=1000
        self.noPOCards=True
        self.InitCards()
    def InitCards(self):
        self.cardN=17
        self.cards=[]
        for i in range(20):
            card=_card()
            self.cards.append(card)
    def HowMuchCards(self):
        cardsN=0
        for i in range(self.cardN):
            if self.cards[i].state!=CS_PUTOUT:
                cardsN+=1
        return cardsN
    def SetCardsState(self,state):
        n=17
        if self.IsMain==True:n=20        
        for i in range(n):
            self.cards[i].state=state
    def SetCardsId(self, idList):
        it=0
        for i in idList:
            self.cards[it].cardId=i
            it+=1
    def AddRest3CardsId(self, idList):
        it=17
        for i in idList:
            self.cards[it].cardId=i
            it+=1
    def GetStrongerStyle(self,prevPOCardStyle):
        blst=[CST_4, CST_SW]
        if prevPOCardStyle.T==-1: return [CST_1, CST_2, CST_3, CST_31, CST_32, CST_4, CST_41, CST_411, CST_42, CST_422, CST_SEQ, CST_SW]
        elif prevPOCardStyle.T==CST_SW: return []
        elif prevPOCardStyle.T==CST_4: return blst
        else: return [prevPOCardStyle.T]+blst
    def GetLstOfVals(self,vec_val):
        lst=[]
        for v in vec_val:
            for i in range(self.cardN):
                it=self.cards[i]
                if it.state==CS_UNSELECT and it.val()==v:
                    lst.append(it)
        return lst
    def SelectStyle(self,vec_val,res_lst,prevPOCardStyle):
        non=_pocardsstyle()
        for v in vec_val:
            lst=self.GetLstOfVals([v])
            chStyle=self.ClassifyCards(lst+res_lst)
            res=self.CompareCards(prevPOCardStyle,chStyle)
            if res==1:
                for it in lst+res_lst:
                    it.state=CS_SELECT
                return chStyle
        return non
    def CpuPOCards(self,prevPOCardStyle):
        non=_pocardsstyle()
        vec_card=[]
        for i in range(self.cardN):
            if self.cards[i].state==CS_UNSELECT:
                vec_card.append(self.cards[i])
        vec_val_CST_1=self.GetValsOfType(vec_card, CST_1)
        vec_val_CST_2=self.GetValsOfType(vec_card, CST_2)
        vec_val_CST_3=self.GetValsOfType(vec_card, CST_3)
        vec_val_CST_4=self.GetValsOfType(vec_card, CST_4)
        vec_val_CST_SW=self.GetValsOfType(vec_card, CST_SW)
        n_CST_1 = len(vec_val_CST_1)
        n_CST_2 = len(vec_val_CST_2)
        n_CST_3 = len(vec_val_CST_3)
        n_CST_4 = len(vec_val_CST_4)
        n_CST_SW = len(vec_val_CST_SW)
        lstStyle=self.GetStrongerStyle(prevPOCardStyle)
        if len(lstStyle)==0: return non
        for style in lstStyle:            
            res=_pocardsstyle()
            res_lst=[]
            match style:
                case 0:#CST_1
                    if n_CST_1>0: 
                        res=self.SelectStyle(vec_val_CST_1,[],prevPOCardStyle)
                        if n_CST_SW==2:
                            if res.T==CST_1 and (res.F==CV_S or res.F==CV_W): continue
                        if res.T!=-1: return res
                    continue
                case 1:#CST_2
                    if n_CST_2>0: 
                        res=self.SelectStyle(vec_val_CST_2,[],prevPOCardStyle)
                        if res.T!=-1: return res
                    continue
                case 2:#CST_3
                    if n_CST_3>0: 
                        res=self.SelectStyle(vec_val_CST_3,[],prevPOCardStyle)
                        if res.T!=-1: return res
                    continue
                case 3:#CST_31
                    if n_CST_3>0: 
                        if n_CST_1>0: 
                            res_lst=self.GetLstOfVals(vec_val_CST_1)
                        elif n_CST_2>0: 
                            res_lst=self.GetLstOfVals(vec_val_CST_2)
                        elif n_CST_3>0: 
                            res_lst=self.GetLstOfVals(vec_val_CST_3)
                        if len(res_lst)>0:
                            res=self.SelectStyle(vec_val_CST_3,[res_lst[0]],prevPOCardStyle)
                        if res.T!=-1: return res
                    continue
                case 4:#CST_32
                    if n_CST_3>0: 
                        if n_CST_2>0: 
                            res_lst=self.GetLstOfVals([vec_val_CST_2[0]])
                        elif n_CST_3>0: 
                            res_lst=self.GetLstOfVals([vec_val_CST_3[0]])                            
                        if len(res_lst)>1:
                            res=self.SelectStyle(vec_val_CST_3,[res_lst[0],res_lst[1]],prevPOCardStyle)
                        if res.T!=-1: return res
                    continue
                case 5:#CST_4
                    if n_CST_4>0: 
                        res=self.SelectStyle(vec_val_CST_4,[],prevPOCardStyle)
                        if res.T!=-1: return res
                    continue
                case 6:#CST_41
                    if n_CST_4>0: 
                        if n_CST_1>0: 
                            res_lst=self.GetLstOfVals(vec_val_CST_1)
                        elif n_CST_2>0: 
                            res_lst=self.GetLstOfVals(vec_val_CST_2)
                        elif n_CST_3>0: 
                            res_lst=self.GetLstOfVals(vec_val_CST_3)
                        if len(res_lst)>0:
                            res=self.SelectStyle(vec_val_CST_4,[res_lst[0]],prevPOCardStyle)
                        if res.T!=-1: return res
                    continue
                case 7:#CST_411
                    if n_CST_4>0: 
                        if n_CST_1>1: 
                            res_lst=self.GetLstOfVals(vec_val_CST_1)
                            if len(res_lst)>1:
                                res=self.SelectStyle(vec_val_CST_4,[res_lst[0],res_lst[1]],prevPOCardStyle)
                        if res.T!=-1: return res
                    continue
                case 8:#CST_42
                    if n_CST_4>0: 
                        if n_CST_2>0: 
                            res_lst=self.GetLstOfVals([vec_val_CST_2[0]])
                        elif n_CST_3>0: 
                            res_lst=self.GetLstOfVals([vec_val_CST_3[0]])                            
                        if len(res_lst)>1:
                            res=self.SelectStyle(vec_val_CST_4,[res_lst[0],res_lst[1]],prevPOCardStyle)
                        if res.T!=-1: return res
                    continue
                case 9:#CST_422
                    if n_CST_4>0: 
                        if n_CST_2>1: 
                            res_lst=self.GetLstOfVals([vec_val_CST_2[0],vec_val_CST_2[1]])
                        res=self.SelectStyle(vec_val_CST_4,res_lst,prevPOCardStyle)
                        if res.T!=-1: return res
                    continue
                case 10:#CST_SEQ
                    continue
                case 11:#CST_SW
                    if n_CST_SW==2: return _pocardsstyle(CST_SW,CV_S,CV_W,-1)
                    continue
        return non
    def ManPOCards(self,prevPOCardStyle):
        vec_card=[]
        for i in range(self.cardN):
            state=self.cards[i].state
            if state==CS_SELECT:
                vec_card.append(self.cards[i])
        chStyle=self.ClassifyCards(vec_card)
        non=_pocardsstyle()
        if chStyle.T==-1:return non
        if self.CompareCards(prevPOCardStyle,chStyle)!=1:return non
        return chStyle
    def FreeSelectedCards(self):
        for i in range(self.cardN):
            if self.cards[i].state==CS_SELECT:
                self.cards[i].state=CS_UNSELECT
    #------------------------------------card manage----------------------------    
    def SortCard(self):
        self.cards.sort(key=lambda x: x.val())
        return self.cards
    def GetValsOfType(self, vec_card, type):
        arr=np.zeros(16)
        for it in vec_card:
            arr[it.val()] += 1            
        vec_val=[]
        vec_val1=[]
        vec_val2=[]
        vec_val3=[]
        vec_val4=[]
        vec_SW=[]
        for i in range(16):
            if arr[i] == 1:
                vec_val1.append(i)
        for i in range(16):
            if arr[i] == 2:
                vec_val2.append(i)
        for i in range(16):
            if arr[i] == 3:
                vec_val3.append(i)
        for i in range(16):
            if arr[i] == 4:
                vec_val4.append(i)   
        if arr[14] == 1 and arr[15] == 1:
            vec_SW=[14,15]   
        n1=len(vec_val1)      
        n2=len(vec_val2)      
        n3=len(vec_val3)      
        n4=len(vec_val4)      
        nSW=len(vec_SW)   
        match type:    
            case 0:#CST_1=0
                if n1>0:
                    vec_val=vec_val1
            case 1:#CST_2=1
                if n2>0:
                    vec_val=vec_val2
            case 2:#CST_3=2
                if n3>0:
                    vec_val=vec_val3
            case 3:#CST_31=3
                if n3>0:
                    vec_val=vec_val3
                    if n1>0:
                        vec_val.append(vec_val1[0])
                    elif n2>0:
                        vec_val.append(vec_val2[0])
                    elif n3>0:
                        vec_val.append(vec_val3[0])
            case 4:#CST_32=4
                if n3>0:
                    vec_val=vec_val3
                    if n2>0:
                        vec_val.append(vec_val2[0])
                    elif n3>0:
                        vec_val.append(vec_val3[0])
            case 5:#CST_4=5
                if n4>0:
                    vec_val=vec_val4
            case 6:#CST_41=6
                if n4>0:
                    vec_val=vec_val4
                    if n1>0:
                        vec_val.append(vec_val1[0])
                    elif n2>0:
                        vec_val.append(vec_val2[0])
                    elif n3>0:
                        vec_val.append(vec_val3[0])
            case 7:#CST_411=7
                if n4>0:
                    vec_val=vec_val4
                    if n1>1:
                        vec_val.append(vec_val1[0])
                        vec_val.append(vec_val1[1])
                    elif n2>1:
                        vec_val.append(vec_val2[0])
                        vec_val.append(vec_val2[1])
                    elif n3>1:
                        vec_val.append(vec_val3[0])
                        vec_val.append(vec_val3[0])
            case 8:#CST_42=8
                if n4>0:
                    vec_val=vec_val4
                    if n1>0:
                        vec_val.append(vec_val1[0])
                    elif n2>0:
                        vec_val.append(vec_val2[0])
                    elif n3>0:
                        vec_val.append(vec_val3[0])
            case 9:#CST_422=9
                if n4>0:
                    vec_val=vec_val4
                    if n2>1:
                        vec_val.append(vec_val2[0])
                        vec_val.append(vec_val2[1])
                    elif n3>1:
                        vec_val.append(vec_val3[0])
                        vec_val.append(vec_val3[1])
            case 10:#CST_SEQ=9
                if n1>4:
                    for i in range(n1):
                        vec_val.append(vec_val1[i])
                elif n2>4:
                    for i in range(n2):
                        vec_val.append(vec_val2[i])
                elif n3>4:
                    for i in range(n3):
                        vec_val.append(vec_val3[i])
            case 11:#CST_SW=9
                if nSW==2:  
                    vec_val=vec_SW
        return vec_val
    def GetStyle(self, n1, n2, n3, n4):
        if n1 == 1 and n2 == 0 and n3 == 0 and n4 == 0: return CST_1
        elif n1 == 0 and n2 == 1 and n3 == 0 and n4 == 0: return CST_2
        elif n1 == 0 and n2 == 0 and n3 == 1 and n4 == 0: return CST_3
        elif n1 == 1 and n2 == 0 and n3 == 1 and n4 == 0: return CST_31
        elif n1 == 0 and n2 == 1 and n3 == 1 and n4 == 0: return CST_32
        elif n1 == 0 and n2 == 0 and n3 == 0 and n4 == 1: return CST_4
        elif n1 == 1 and n2 == 0 and n3 == 0 and n4 == 1: return CST_41
        elif n1 == 0 and n2 == 1 and n3 == 0 and n4 == 1: return CST_42
        elif n1 == 2 and n2 == 0 and n3 == 0 and n4 == 1: return CST_411
        elif n1 == 0 and n2 == 2 and n3 == 0 and n4 == 1: return CST_422
        else: return -1
    def ClassifyCards(self, vec_card):
        non=cards=_pocardsstyle()
        n = len(vec_card)
        if n == 0 or n > 20: return non
        if n == 2:
            if (vec_card[0].type() == CT_S and vec_card[0].type() == CT_S) or (vec_card[0].type() == CT_S and vec_card[0].type() == CT_S):
                cards.T = CST_SW
                return cards
        vec_val1=self.GetValsOfType(vec_card, CST_1)
        vec_val2=self.GetValsOfType(vec_card, CST_2)
        vec_val3=self.GetValsOfType(vec_card, CST_3)
        vec_val4=self.GetValsOfType(vec_card, CST_4)
        n1 = len(vec_val1)
        n2 = len(vec_val2)
        n3 = len(vec_val3)
        n4 = len(vec_val4)
        type = self.GetStyle(n1, n2, n3, n4)
        cards.T = type
        match type:    
            case 0:#CST_1=0
                cards.F = vec_val1[0]
                return cards
            case 1:#CST_2=1
                cards.F = vec_val2[0]
                return cards
            case 2:#CST_3=2
                cards.F = vec_val3[0]
                return cards
            case 3:#CST_31=3
                cards.F = vec_val3[0]
                cards.S = vec_val1[0]
                return cards
            case 4:#CST_32=4
                cards.F = vec_val3[0]
                cards.S = vec_val2[0]
                return cards
            case 5:#CST_4=5
                cards.F = vec_val4[0]
                return cards
            case 6:#CST_41=6
                cards.F = vec_val4[0]
                cards.S = vec_val1[0]
                return cards
            case 7:#CST_411=7
                cards.F = vec_val4[0]
                cards.S = vec_val1[0]
                cards.R = vec_val1[1]
                return cards
            case 8:#CST_42=8
                cards.F = vec_val4[0]
                cards.S = vec_val2[0]
                return cards
            case 9:#CST_422=9
                cards.F = vec_val4[0]
                cards.S = vec_val2[0]
                cards.R = vec_val2[1]
                return cards
        if n1<5 or n2>0 or n3>0 or n4>0: return non
        for it in range(len(vec_val1)-1):
            if vec_val1[it]+1 != vec_val1[it+1]:
                return non            
        cards.T= CST_SEQ         
        cards.F = vec_val1[0]
        cards.S = len(vec_val1)
        return cards
    def CompareCards(self, cards1, cards2):
        if cards1.T==-1:return 1
        if cards1.T == CST_SW: return -1
        if cards2.T == CST_SW: return 1
        if cards2.T == CST_4 and cards1.T != CST_4: return 1
        if cards1.T == CST_4 and cards2.T != CST_4: return -1
        if cards1.T == CST_4 and cards2.T == CST_4:
            if cards1.F < cards2.F: return 1
            if cards2.F < cards1.F: return -1 
        if cards1.T != cards2.T: return 0
        if cards1.T == CST_SEQ:
            if cards1.S != cards2.S: return 0
            if cards1.F < cards2.F: return 1
            if cards1.F > cards2.F: return -1
            return 0;
        if cards1.F < cards2.F:return 1
        if cards1.F > cards2.F:return -1
        return 0    