from flask_app.config.mysqlconnection import MySQLConnection
# create a regular expression object that we'll use later   
from flask_app.models import user_model
from flask import flash,session
import yfinance
import datetime

class Companies:
    def __init__(self,data):
        self.id = data["id"]
        self.Name = data["symbol"]
        self.Name = data["Name"]
        self.Market_Cap = data["Market_Cap"]
        self.PE_Ratio = data["PE_Ratio"]
        self.EPS = data["EPS"]
        self.Volume = data["Volume"]
        self.Volume = data["Avg_Volume"]
        self.Volume = data["dividendYield"]
        self.Avg_Volume = data["regularMarketPrice"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_class = None

    @classmethod
    def display_all_companies(cls,session):
        query = "select * from users_companies_table join companies_table  on users_companies_table.companies_t_id = companies_table.id where users_companies_table.user_t_id = %(id)s"
        results = MySQLConnection("Stocks_project").query_db(query,session)      
        return results
    
    @classmethod
    def get_company_info(cls,symbol):
        company = yfinance.Ticker(symbol)
        # get stock info
        company_info = company.info
        # this line to confirm if stock symbol exist
        if company_info["regularMarketPrice"] == None:
            return False
        PE_Ratio = company_info["regularMarketPrice"] / company_info["trailingEps"]
        company_data = {
            "Name" : company_info["longName"],
            "symbol" : symbol,
            "Market_Cap" : company_info["marketCap"],
            "PE_Ratio" :PE_Ratio,
            "EPS" :company_info["trailingEps"],
            "Volume" : company_info["volume"],
            "Avg_Volume" : company_info["averageVolume"],
            "dividendYield" : company_info["dividendYield"],
            "regularMarketPrice" :company_info["regularMarketPrice"],
            "fiftyTwoWeekLow": company_info["fiftyTwoWeekLow"],
            "fiftyTwoWeekHigh": company_info["fiftyTwoWeekHigh"],
            "revenuePerShare" :company_info["revenuePerShare"],
            "totalRevenue" :company_info["totalRevenue"],
            "totalDebt" :company_info["totalDebt"],
            "totalCash" :company_info["totalCash"],
            "currentRatio" : company_info['currentRatio'],
            "recommendationKey" :company_info["recommendationKey"],
            "longBusinessSummary":company_info["longBusinessSummary"],
            "user_t_id" : session["id"]
        }
        return company_data

    @classmethod
    def save_campany(cls, data):
        query = "insert into companies_table (symbol,Name, Market_Cap, PE_Ratio, EPS, Volume ,Avg_Volume,dividendYield,regularMarketPrice) values (%(symbol)s,%(Name)s, %(Market_Cap)s, %(PE_Ratio)s, %(EPS)s, %(Volume)s, %(Avg_Volume)s,%(dividendYield)s,%(regularMarketPrice)s);"
        results = MySQLConnection("Stocks_project").query_db(query, data)
        my_ids = {"user_t_id":data["user_t_id"], "companies_t_id":results}
        query = "insert into users_companies_table (user_t_id, companies_t_id) values(%(user_t_id)s, %(companies_t_id)s);"
        results_id = MySQLConnection("Stocks_project").query_db(query,my_ids)
        return results


    @classmethod
    def save_all_campanies(cls, data):
        query = "insert into company (symbol,Name, Market_Cap, PE_Ratio, EPS, Volume ,Avg_Volume,dividendYield,regularMarketPrice, fiftyTwoWeekLow, fiftyTwoWeekHigh, revenuePerShare, totalRevenue, totalDebt, totalCash ,currentRatio,recommendationKey,longBusinessSummary) values (%(symbol)s,%(Name)s, %(Market_Cap)s, %(PE_Ratio)s, %(EPS)s, %(Volume)s, %(Avg_Volume)s,%(dividendYield)s,%(regularMarketPrice)s, %(fiftyTwoWeekLow)s,%(fiftyTwoWeekHigh)s, %(revenuePerShare)s, %(totalRevenue)s, %(totalDebt)s, %(totalCash)s, %(currentRatio)s,%(recommendationKey)s,%(longBusinessSummary)s);"
        results = MySQLConnection("Stocks_project").query_db(query, data)
        return results

    @classmethod
    def show_all_companies(cls):
        query = "select * from company"
        results = MySQLConnection("Stocks_project").query_db(query)
        return results

    @classmethod
    def one_company(cls,data):
        query = "select * from company where symbol = %(symbol)s"
        results = MySQLConnection("Stocks_project").query_db(query,data)   
        return results
    
    @classmethod
    def update_companies(cls):
        currentTime = datetime.datetime.now()
        if (currentTime.hour == 21) or (currentTime.minute == 58):
            user_symbols = []
            users_query = "select * from companies_table"
            user_companies = MySQLConnection("Stocks_project").query_db(users_query)
            
            for user_company in user_companies:
                user_symbols.append(user_company["symbol"])
            
            all_companies = Companies.show_all_companies()
            for company in all_companies:
                symbol = company["symbol"]

                data = Companies.get_company_info(symbol)
                all_companies_query = "update company set Name = %(Name)s, Market_Cap = %(Market_Cap)s, PE_Ratio = %(PE_Ratio)s, EPS = %(EPS)s, Volume = %(Volume)s, Avg_Volume = %(Avg_Volume)s, dividendYield = %(dividendYield)s, regularMarketPrice = %(regularMarketPrice)s, fiftyTwoWeekLow = %(fiftyTwoWeekLow)s, fiftyTwoWeekHigh = %(fiftyTwoWeekHigh)s, revenuePerShare = %(revenuePerShare)s, totalRevenue = %(totalRevenue)s, totalDebt = %(totalDebt)s, totalCash = %(totalCash)s,currentRatio = %(currentRatio)s,recommendationKey = %(recommendationKey)s,longBusinessSummary = %(longBusinessSummary)s where symbol = %(symbol)s;"
                results = MySQLConnection("Stocks_project").query_db(all_companies_query, data)
                if symbol in user_symbols:
                    query = "update companies_table set Market_Cap = %(Market_Cap)s, PE_Ratio = %(PE_Ratio)s, EPS = %(EPS)s, Volume = %(Volume)s, Avg_Volume = %(Avg_Volume)s, dividendYield = %(dividendYield)s, regularMarketPrice =  %(regularMarketPrice)s where symbol = %(symbol)s;"
                    user_results = MySQLConnection("Stocks_project").query_db(query, data)
        

    @classmethod
    def delete_company(cls,data):
        queryp = "Delete from users_companies_table where users_companies_table.companies_t_id =%(id)s;"
        queryc = "delete from companies_table where companies_table.id =%(id)s;"
        resultp = MySQLConnection("Stocks_project").query_db(queryp, data)
        resultc = MySQLConnection("Stocks_project").query_db(queryc, data)

        return resultp

    @staticmethod
    def validate_company(data):
        is_valid = True
        if len(data["symbol"]) == 0:
            is_valid = False
            flash("please enter a valid symbol","company")
        return is_valid

    @classmethod
    def check_new_comapny(cls,symbol):
        is_valid = None
        is_user_has_it = None
        data = {"symbol" : symbol}
        data_id = {"id" : session["id"]}

# this section to find if a company in user companies
# to avoid duplicate add
        one_company_info = Companies.display_all_companies(data_id)
        print(one_company_info)
        # print("okay3")
        for company in one_company_info:
            if symbol == company["symbol"]:
                return True
        companies = Companies.show_all_companies()
# this section should work only if a company
#  in company table and not in user companies
        for company in companies:
            if symbol == company["symbol"]:
# this function to pull infor from comapny table
                results = Companies.one_company(data)
                company_info = results[0]
                print(company_info['Market_Cap'])
                company_data = {
                    "Name" : company_info["Name"],
                    "symbol" : company_info["symbol"],
                    "Market_Cap" : company_info["Market_Cap"],
                    "PE_Ratio" :company_info['PE_Ratio'],
                    "EPS" :company_info["EPS"],
                    "Volume" : company_info["Volume"],
                    "Avg_Volume" : company_info["Avg_Volume"],
                    "dividendYield" : company_info["dividendYield"],
                    "regularMarketPrice" :company_info["regularMarketPrice"],
                    "user_t_id" : session["id"]
                }
                is_valid = True
                if is_valid == True:
                    results = Companies.save_campany(company_data)
                return True
        return False
