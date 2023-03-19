from cgitb import text
import tkinter
import tkinter.ttk

class Logic:
    def __init__(self):
        ########: dicts for weight, bag value and coin vlaue for each coin type
        self.coinValue = {"£2":2, "£1":1, "50p":0.5, "20p":0.2, "10p":0.1, "5p":0.5, "2p":0.2, "1p":0.1}
        self.weightPerCoin = {"£2":12, "£1":8.75, "50p":8, "20p":5, "10p":6.5, "5p":2.35, "2p":7.12, "1p":3.56}
        self.bagValue = {"£2":20, "£1":20, "50p":10, "20p":10, "10p":5, "5p":5, "2p":1, "1p":1}



    ########: checks if the inputed weight is the same as the target weight
    ########: if true, the total correct bags is updated in both the totals dict and the volenteers dict
    ########: other wise the the same is done without incrementing the correct totals
    def Validate_Data(self, coinType, coinWeight, name):

        try:
            targetWeight = int((self.bagValue[coinType] / self.coinValue[coinType]) * self.weightPerCoin[coinType])
        except(ValueError):
            return "The coin type of the bag is incorect or there is a mismatched coin."

        try:
            if(int(coinWeight) == targetWeight):
                self.update_Totals(True, name, coinType)
                return "Correct Bag"
            else:
                self.update_Totals(False, name, coinType)
                return "Incorect Bag. {}".format(self.how_many_out(coinWeight, coinType))

        ########: input sanitation thangs        
        except(ValueError):
            return "Invalid, please only use a Number"
        except(KeyError):
            return "Please select a coin type"
    
    

    ########: when reading the file, the first line is a dictionary for the totals for every inputed data
    ########: the second line, a list of dictionarys for each volenteer entered
    ########: the two lines are each assigned to a variable to be eddited and writen back into the text file
    ########: this specific func updates the totals dict  ===> {'Total': int, 'TotalBags': int, 'TotalCorrect': int, 'Accuracy': int}
    def update_Totals(self, correct, name, coinType):
        with open("CoinCount.txt", 'r') as coinCount:
            total = eval(coinCount.readline())
            volenteers = eval(coinCount.readline())

        ########: updates the total dict incrementing each item -if needed
        total["Total"] += self.bagValue[coinType]
        total["TotalBags"] += 1
        total["Accuracy"] = round((total["TotalCorrect"] / total["TotalBags"]) * 100)
        if(correct):
            total["TotalCorrect"] +=1

        ########: func updates the volenteers list
        self.update_Volenteers(volenteers, name, correct)
        
        with open("./CoinCount.txt", 'w') as coinCount:
            coinCount.write(str(total) + "\n")
            coinCount.write(str(volenteers))



    ########: this specific func updates the volenteers dict ===> [{'name': str, 'TotalBags': int, 'TotalCorrect': int, 'Accuracy': int}]
    ########: if there is already a volenteer by the same name, the dict will be updated
    ########: otherwise, a new dict will be appended
    def update_Volenteers(self, volenteers, name, correct):
        if(correct):
            totalCorect = 1
            accuracy = 100
        else:
            totalCorect = 0
            accuracy  = 0

        for i in range(len(volenteers)):
            if(volenteers[i]["name"] == name):
                volenteers[i]["TotalBags"] += 1
                volenteers[i]["TotalCorrect"] += totalCorect
                volenteers[i]["Accuracy"] = round((int(volenteers[i]["TotalCorrect"]) / int(volenteers[i]["TotalBags"])) * 100, 2)
                return None
        
        volenteers.append(dict({"name":name, "TotalBags":1, "TotalCorrect":totalCorect, "Accuracy":accuracy}))



    ########: calculates the diffrence between the number of expected coins and inputed coins
    ########: then changes the output depending of if the answer is positive or negative, indicating coins needing to be added or taken away
    def how_many_out(self, coinWeight, coinType):
        out = int((int(coinWeight) / self.weightPerCoin[coinType]) - (self.bagValue[coinType] / self.coinValue[coinType]))

        if(out > 0):
            msg = "{} coins to be removed.".format(out)
        else:
            sout = str(out)
            msg = "{} coins to be added.".format(sout[1:len(sout)])

        return msg



    ########: makes a list of sorted accuracys from the volenteer list of dicts
    ########: using the sorted list it searches through the volenteer list to find the dict with a matching accuracy
    ########: if found, the dict will be apended to a new list that will be ordered
    def order_by_accuracy(self, volenteer):
        accuracys = []
        for i in range(len(volenteer)):
            accuracys.append(volenteer[i]["Accuracy"])
        
        accuracys.sort(reverse=True)
        newDict = []
        for i in range(len(accuracys)):
            for j in range(len(volenteer)):
                if(accuracys[i] == volenteer[j]["Accuracy"]):
                    newDict.append(volenteer[j])
        
        return newDict



        





class Help_Page(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)

        info ="""
 - input the volenteers name, the weight of the coin bag and the
    type of coin in the bag
 - only use one type of coin per bag
 - dont delete the CoinCount.txt file"""

        infoLabel = tkinter.Text(self, width=70, height=5)
        infoLabel.insert(tkinter.END,info)
        infoLabel.pack()







class TotalBags_Page(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)
        
        nameLabel = tkinter.Label(self, text="Name")
        totalBagsLabel = tkinter.Label(self, text="Total Bags")
        acccuracyLabel = tkinter.Label(self, text="Accuracy")

        nameLabel.grid(column=0, row=0)
        totalBagsLabel.grid(column=1, row=0)
        acccuracyLabel.grid(column=2, row=0)

        self.make_table()
    
    def make_table(self):
        with open("./CoinCount.txt") as coin:
            coin.readline()
            volenteers = eval(coin.readline())

        logic = Logic()
        newVolenteer = logic.order_by_accuracy(volenteer=volenteers)
        
        for i in range(len(volenteers)):
            name = tkinter.Label(self, text=newVolenteer[i]["name"])
            totalBags = tkinter.Label(self, text=newVolenteer[i]["TotalBags"])
            accuracy = tkinter.Label(self, text=newVolenteer[i]["Accuracy"])

            name.grid(column=0, row=i + 1)
            totalBags.grid(column=1, row=i + 1)
            accuracy.grid(column=2, row=i + 1)








class Total_Page(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)

        with open("./CoinCount.txt", 'r') as coin:
            total = eval(coin.readline())

        totalFrame = tkinter.Frame(self, padx=10, pady=10)
        totalMoneyLabel = tkinter.Label(totalFrame, text="TotalMoney: {}".format(total["Total"]))
        totalBagsLabel = tkinter.Label(totalFrame, text="TotalBags: {}".format(total["TotalBags"]))

        totalFrame.grid(column=0, row=0)
        totalMoneyLabel.grid(column=0, row=0)
        totalBagsLabel.grid(column=0, row=1)


        bagsFrame = tkinter.Frame(self, padx=10, pady= 10)
        bagsCorrect = tkinter.Label(bagsFrame, text="Correct bags: {}".format(total["TotalCorrect"]))
        bagsAccuracy = tkinter.Label(bagsFrame, text="Accuracy: {}".format(total["Accuracy"]))

        bagsFrame.grid(column=1, row=0)
        bagsCorrect.grid(column=0, row=0)
        bagsAccuracy.grid(column=0, row=1)








class Home_Page(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)

        nameLabel = tkinter.Label(self, text="Name: ")
        coinTypeLabel = tkinter.Label(self, text="Coin Type: ")
        weightLabel = tkinter.Label(self, text="Weight(g): ")
        self.outputLabel = tkinter.Label(self)

        self.nameSVar = tkinter.StringVar()
        self.weightSVar = tkinter.StringVar()
        coinTypeSVar = tkinter.StringVar()
        nameEntry = tkinter.Entry(self, textvariable=self.nameSVar)
        weightEntry = tkinter.Entry(self, textvariable=self.weightSVar)

        self.coinTypeCB = tkinter.ttk.Combobox(self, textvariable=coinTypeSVar)
        self.coinTypeCB['values'] = ["£2", "£1", "50p", "20p", "10p", "5p", "2p", "1p"]
        self.coinTypeCB['state'] = 'readonly'

        submitButton = tkinter.Button(self, text="Submit", command=lambda: self.submitButton_Pressed())

        nameLabel.grid(column=0,row=0)
        coinTypeLabel.grid(column=0, row=2)
        weightLabel.grid(column=0, row=1)
        nameEntry.grid(column=1, row=0)
        weightEntry.grid(column=1, row=1)
        self.outputLabel.grid(column=0, row=4, columnspan=2)
        self.coinTypeCB.grid(column=1, row=2)
        submitButton.grid(column=0, row=3, columnspan=2)


    
    def submitButton_Pressed(self):
        logic = Logic()
        outText = logic.Validate_Data(coinType=self.coinTypeCB.get(), coinWeight=self.weightSVar.get(), name=self.nameSVar.get())
        self.outputLabel.config(text=outText)
        







class gui(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.title("Coin Count")
        self.currentFrame = None
        self.switch_frame(Home_Page)

        menuBar = tkinter.Menu(self)
        self.config(menu=menuBar)

        fmenu = tkinter.Menu(menuBar, tearoff=False)
        fmenu.add_command(label="Home", command=lambda: self.switch_frame(Home_Page))
        fmenu.add_command(label="Total", command=lambda: self.switch_frame(Total_Page))
        fmenu.add_command(label="All Bags", command=lambda: self.switch_frame(TotalBags_Page))
        fmenu.add_separator()
        fmenu.add_command(label="Help", command=lambda: self.switch_frame(Help_Page))
        fmenu.add_command(label="Quit", command=lambda: self.quit())
        menuBar.add_cascade(label="Options", menu=fmenu)



    ########: changes the curent frame
    ########: when called a new frame is given (nFrame), which is initialised as a child to the gui class
    ########: old frame is destroyed and new frame is packed
    def switch_frame(self, nFrame):
        newFrame = nFrame(self)
        if(self.currentFrame is not None):
            self.currentFrame.destroy()
        self.currentFrame = newFrame
        self.currentFrame.pack(padx=5, pady=5)








if(__name__ == "__main__"):
    gui = gui()
    gui.mainloop()