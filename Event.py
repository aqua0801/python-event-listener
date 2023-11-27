class Event():
    def __init__(self):
        self.__warning=True
        self.eventListeners={}
        self.wrappers={}
        self.thread=None

    def display(self,string):
        if(not self.__warning):
            return
        print(string)

    def enableWarning(self):
        self.__warning=True
    def disableWarning(self):
        self.__warning=False
        
    def lstFuncWrapper(self,lstFunc:callable):
        def wrapper(*args,**kwargs):
            lstFunc(*args,**kwargs)
            self.triggerEventListener(self.wrappers[lstFunc],*args,**kwargs)
            return lstFunc
        self.wrappers[lstFunc]=wrapper
        return wrapper
    
    def decoratorAdd(self,lstFunc:callable):
        def add(objFunc:callable):
            self.addEventListener(lstFunc,objFunc)
            return objFunc
        return add

    
    def setThread(self,objFunc,*args,**kwargs):
        import threading
        self.thread=threading.Thread(target=objFunc,*args,**kwargs)
        self.thread.name=objFunc.__name__
    def singleThreadExecute(self,objFunc:callable):
        import threading     
        def wrapper(*args,**kwargs):
            if(self.thread==None): self.setThread(objFunc,*args,**kwargs)
            if(self.thread.is_alive()):
                self.display(f"[singleThd]{str(self.__class__)} is already running function({self.thread.name})")
                return
            self.setThread(objFunc,*args,**kwargs)
            self.thread.start()
            return objFunc
        return wrapper
    @staticmethod
    def inputInt(string:str)->int:
        while(True):
            inputTemp=input(string)
            try:
                return int(inputTemp)
            except:
                print("[Input]Invalid input !")
    @staticmethod
    def tryFunc(objFunc:callable):
        def wrapper(*args,**kwargs):
            try:
                objFunc(*args,**kwargs)
            except Exception as ex:
                print(f"[TryFunc]{objFunc.__name__} encounters ({ex}) exception !")
            return objFunc
        return wrapper
    
    @staticmethod
    def threadExecute(objFunc:callable):
        import threading
        def wrapper(*args,**kwargs):
            thread=threading.Thread(target=objFunc,args=args,kwargs=kwargs)
            thread.start()
            return objFunc
        return wrapper
    @staticmethod
    def funcTimer(objFunc:callable):
        import time
        def wrapper(*args,**kwargs):
            START=time.time()
            objFunc(*args,**kwargs)
            END=time.time()
            print(f'[Timer]Function {objFunc.__name__!r} executed in {(END-START):.4f}s') 
            return objFunc
        return wrapper
    def showEventListeners(self,lstFunc:callable):
        if(lstFunc not in self.eventListeners):
            if(lstFunc not in self.wrappers):
                self.display(f"[Show]Cannot find {lstFunc.__name__} in event listeners !")
                return
            lstFunc=self.wrappers[lstFunc]
        for func in self.eventListeners[lstFunc]:
            print(func,end="  ")
        print()
    def changeOrder(self,lstFunc:callable):
        if(lstFunc not in self.eventListeners):
            if(lstFunc not in self.wrappers):
                self.display(f"[Change]Cannot find {lstFunc.__name__} in event listeners !")
                return
            lstFunc=self.wrappers[lstFunc]
            
        if(len(self.eventListeners[lstFunc])<=1):
            self.display(f"[Change]Event listener of function {lstFunc.__name__} is less than 1 , cannot be ordered !")
            return
        
        self.showEventListeners(lstFunc)
        sortedTemp=[]
        for index in range(0,len(self.eventListeners[lstFunc])):
            sortedTemp.append([])
            sortedTemp[index].append(self.eventListeners[lstFunc][index])
            sortedTemp[index].append(self.inputInt(">"))

        sortedTemp.sort(key=lambda x:x[1])
        self.eventListeners[lstFunc]=[func for func , index in sortedTemp]
        
        self.showEventListeners(lstFunc)
        
    def addEventListener(self,lstFunc:callable,objFunc:callable):
        if(lstFunc==objFunc):
            self.display(f"[Add]Cannot bind function itself to its listener !")
            return
        if(lstFunc not in self.eventListeners):
            self.eventListeners[lstFunc]=[]
        if(objFunc in self.eventListeners[lstFunc]):
            self.display(f"[Add]{objFunc.__name__} already exists in {lstFunc.__name__} listener !")
            return
        if(self.checkListenerPath(lstFunc,objFunc)):
            self.display(f"[Add]Make {objFunc.__name__} listener to {lstFunc.__name__} will lead to infinite loop !")
            return
        self.eventListeners[lstFunc].append(objFunc)
        
    def deleteEventListener(self,lstFunc:callable,objFunc:callable):

        if(lstFunc not in self.eventListeners):
            self.display(f"[Delete]{lstFunc.__name__} does not exist in event listeners !")
            return
        if(objFunc not in self.eventListeners[lstFunc]):
            self.display(f"[Delete]{objFunc.__name__} does not exist in {lstFunc.__name__} listener !")
            return
        self.eventListeners[lstFunc].remove(objFunc)

    def triggerEventListener(self,lstFunc,*args,**kwargs):
        if(lstFunc not in self.eventListeners):
            self.display(f"[TriggerEvn]{lstFunc.__name__} does not exist in event listeners !")
            return
        for func in self.eventListeners[lstFunc]:
            #rint(func.__name__)
            func(*args,**kwargs)
            self.triggerEventListener(func,*args,**kwargs)
    
    def triggerlstFunc(self,lstFunc:callable,*args,**kwargs):
        lstFunc(*args,**kwargs)
        print(lstFunc, self.eventListeners)
        if(lstFunc not in self.eventListeners):
            self.display(f"[TriggerFunc]{lstFunc.__name__} does not exist in event listeners !")
            return
        for objFunc in self.eventListeners[lstFunc]:
            objFunc(*args,**kwargs)
    

    def checkListenerPath(self, startFunc, currentFunc, visited=None): #depth-first
        if visited is None:
            visited = set()

        visited.add(currentFunc)
        listeners = self.eventListeners.get(currentFunc, [])

        for lstFunc in listeners:
            if lstFunc == startFunc:
                return True  # Loop detected
            if lstFunc not in visited:
                if self.checkListenerPath(startFunc, lstFunc, visited):
                    return True  # Loop detected

        return False  # No loop detected

