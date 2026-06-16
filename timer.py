import time
import asyncio
import patch
import processjson

class Timer:
    def __init__(self):
        self.currentTime = None
        self._reset = False
        self._currentJson = None
        self._cid = None

    def updateTime(self):
        if self._currentJson != None and self._cid != None and self.currentTime != None:
            j = processjson.generateStatus(self._currentJson, self._cid, self.getSeconds())
            asyncio.run(patch.setStatus(j))


    def getSeconds(self):
        if self.currentTime == None:
            return None
        ct = self.currentTime
        while len(str(ct)) > 10:
            ct = round(ct / 1000)
        return round(time.time()-ct)

    def setTime(self,timee):
        self.currentTime = timee

    def setCurrentJsonAndCid(self,j:dict,cid):
        self.currentTime = j.get("args").get("activity").get("timestamps").get("start")
        self._currentJson = j
        self._cid = cid

    def stop(self):
        self._reset = True

    def timeLoop(self):
        while self._reset == False:
            if self.currentTime != None:
                self.updateTime()
            time.sleep(5)
