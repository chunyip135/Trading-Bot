# buy and hold SPY (tracking index of S&P500)
# close position if either loss more than 10% or profit more than 10% ( take profit or cut loss )
# stop for predetermined period of time (e.g. 1 month)
# repeat again

class Name(QCAlgorithm):

    def Initialize(self):

        # start and end dates for backtesting
        self.SetStartDate(2021,4,11) # set start date
        self.SetEndDate() # if not then most recent date is chosen

        self.SetCash(100000) # for backtesting / except for real trading

        # specify ticker 
        spy = self.AddEquity("SPY", Resolution.Daily) # lowest resolution is tick per miliseconds ( not efficient )
        # self.AddForex, self.AddFuture ... 

        # set data normalization mode (default = adjusted, raw , SplitAdjusted ...)
        spy.SetDataNormalizationMode(DataNormalizationMode.Raw)

        self.spy = spy.Symbol # more information than ticker object

        self.SetBenchmark("SPY") # choose suitable market indices to compare performance

        # brokerage or acount type: margin or cash account
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)
        # if cash account, can't use leverage and settlement of 3 days for Equities

        self.entryPrice = 0
        self.period = timedelta(31) # 31 days
        self.nextEntryTime = self.Time # start right away

    def OnData(self, data):
        # called everytime algorithm receive new data (bar reaches its end time)
        
        # check if data exists or not
        if not self.spy in data:
            return  "No Data"

        # alternatives
        #price = data.Bars[self.spy].Close # current price (closest price which is the closing prie for the day before)
        price = data[self.spy].Close
        #price = self.Securities[self.spy].Close

        # trade logit of the bot

        # check if invested in the securities
        if not self.Portfolio.Invested:
            # if aren't invested
            if self.nextEntryTime <= self.Time: # check current time is less than or equal to the next entry time
                # mannually calculating holding size
                self.SetHoldings(self.spy, 1) # if 1 = 100% of our portfolio
                self.MarketOrder(self.spy, int(self.Portfolio.Cash / price)) # negative size will be selling ( buy as much as possible )
                self.Log("BUY SPY @" + str(price))
                # self.Debug()
                self.entryPrice = price # should be the exact current market price as some deviations when the order is send but ignore for now
        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price:
            # exit
            self.Liquidate() # liquidate all positions in portfolio or specify self.spy to only liquify particular holdings
            self.Log("SELL SPY @" + str(price))
            self.nextEntryTime = self.Time + self.period
