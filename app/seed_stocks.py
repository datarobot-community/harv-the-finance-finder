import csv
from app.models import User, Portfolio, Stock, StockQuote, StockEsg
from app import db

# GET CSV
# Feed CSV into stocks model
# Add Risk category for stock model
# Make sure we can select stocks based on user ratings and risk

def seed_stock_quotes():
    
    if StockQuote.query.count() <= 0:
        print("Quotes database is emtpy - loading data for the first time.")
        with open('data/stock_quotes_all.csv', newline='') as csvfile:
            print('Opened Seed stocks')
            
            csvReader = csv.reader(csvfile)    
            next(csvReader, None)  # skip the headers

            for row in csvReader:    
                # print(row)
                newQuote = StockQuote(
                    symbol=row[0],
                    companyName=row[1],
                    openPrice = row[2] if row[2] else None,
                    closePrice = row[3] if row[3] else None,
                    high = row[4] if row[4] else None,
                    low = row[5] if row[5] else None,
                    latestPrice = row[6] if row[6] else None,
                    latestVolume = row[7] if row[7] else None,
                    previousClose = row[8] if row[8] else None,
                    change = row[9] if row[9] else None,
                    changePercent = row[10] if row[10] else None,
                    avgTotalVolume = row[11] if row[11] else None,
                    marketCap = row[12] if row[12] else None,
                    week52High = row[13] if row[13] else None,
                    week52Low = row[14] if row[14] else None,
                    ytdChange = row[15] if row[15] else None,
                    primaryExchange = row[16] if row[16] else None,
                    previousVolume = row[17] if row[17] else None,
                    volume = row[18] if row[18] else None,
                    peRatio = row[19] if row[19] else None,
                    sector = row[20] if row[20] else None
                )
                print(newQuote)
                db.session.add(newQuote)
                db.session.commit()
            print("Seed stocks complete")

    else:
        print("Quotes DB not empty - going ahead")
        return

def seed_esgs():
    if StockEsg.query.count() <= 0:
        print("Esgs database is emtpy - loading data for the first time.")
        with open('data/stocks_sustainability.csv', newline='') as csvfile:
            print('Opened Seed sustainability data')
            
            csvReader = csv.reader(csvfile)    
            next(csvReader, None)  # skip the headers

            for row in csvReader:    
                # print(row)
                newEsg = StockEsg(
                    symbol = row[0],
                    esg_risk_category = row[1]
                )

                print(newEsg)
                db.session.add(newEsg)
                db.session.commit()
            print("Seed Esgs complete")

    else:
        print("Esgs DB not empty - skipping")
        return
