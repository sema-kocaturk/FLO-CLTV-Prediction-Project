

##############################################################
# BG-NBD ve Gamma-Gamma ile CLTV Prediction
##############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO satış ve pazarlama faaliyetleri için roadmap belirlemek istemektedir.
# Şirketin orta uzun vadeli plan yapabilmesi için var olan müşterilerin gelecekte şirkete sağlayacakları potansiyel değerin tahmin edilmesi gerekmektedir.


###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi


###############################################################
# GÖREVLER
###############################################################
# GÖREV 1: Veriyi Hazırlama

# GÖREV 2: CLTV Veri Yapısının Oluşturulması

# GÖREV 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması, CLTV'nin hesaplanması

# GÖREV 4: CLTV'ye Göre Segmentlerin Oluşturulması


###############################################################
# GÖREV 1: Veriyi Hazırlama
###############################################################

import datetime as dt
import pandas as pd
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)


df_ = pd.read_csv(r"C:\Users\user\Desktop\Datas\flo_data_20k.csv")
df = df_.copy()


def outlier_thresholds(dataframe,variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    upper_limit = quartile3 + 1.5 * interquantile_range
    lower_limit = quartile1 - 1.5 * interquantile_range

    return lower_limit, upper_limit



def replace_with_thresholds(dataframe, variable):
    lower_limit, upper_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] > upper_limit), variable] = upper_limit

replace_with_thresholds(df,"order_num_total_ever_online")
replace_with_thresholds(df, "order_num_total_ever_offline")
replace_with_thresholds(df,"customer_value_total_ever_offline")
replace_with_thresholds(df,"customer_value_total_ever_online")


df.info()

df["first_order_date"] = df["first_order_date"].apply(pd.to_datetime)
df["last_order_date"] = df["last_order_date"].apply(pd.to_datetime)
df["last_order_date_online"] = df["last_order_date_online"].apply(pd.to_datetime)
df["last_order_date_offline"] = df["last_order_date_offline"].apply(pd.to_datetime)


df["total_num_order"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["total_value_order"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]


###############################################################
# GÖREV 2: CLTV Veri Yapısının Oluşturulması
###############################################################


df["last_order_date"].max()

today_date = dt.datetime(2021, 6, 1)

cltv_df = pd.DataFrame()
cltv_df["customer_id"] = df["master_id"]
cltv_df["recency_cltv_weekly"] = ((df["last_order_date"] - df["first_order_date"])/7).astype('timedelta64[D]')
cltv_df["frequency"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
cltv_df["frequency"] = cltv_df["frequency"].astype(int)
cltv_df["T_weekly"] = ((today_date - df["first_order_date"])/7).astype('timedelta64[D]')
cltv_df["monetary_cltv_avg"] = (df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]) / (df["order_num_total_ever_online"] + df["order_num_total_ever_offline"])



###############################################################
# GÖREV 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması, 3 ve 6 aylık CLTV'nin hesaplanması
###############################################################


bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(cltv_df['frequency'],
        cltv_df['recency_cltv_weekly'],
        cltv_df['T_weekly'])



cltv_df["expected_purc_3_month"] = bgf.predict(4*3,
                                              cltv_df['frequency'],
                                              cltv_df['recency_cltv_weekly'],
                                              cltv_df['T_weekly'])



cltv_df["expected_purc_6_month"] = bgf.predict(4*6,
                                              cltv_df['frequency'],
                                              cltv_df['recency_cltv_weekly'],
                                              cltv_df['T_weekly'])


cltv_df["expected_purc_3_month"].sort_values(ascending=False).head(10)
cltv_df["expected_purc_6_month"].sort_values(ascending = False).head(10)


ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])

cltv_df["expected_average_value"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                                 cltv_df['monetary_cltv_avg'])


cltv_df["CLTV"] = ggf.customer_lifetime_value(bgf,
                                              cltv_df["frequency"],
                                              cltv_df["monetary_cltv_avg"],
                                              cltv_df["T_weekly"],
                                              cltv_df["recency_cltv_weekly"],
                                              time = 6,
                                              freq = "W",
                                              discount_rate=0.01)

cltv_df["CLTV"].sort_values(ascending=False).head(20)
###############################################################
# GÖREV 4: CLTV'ye Göre Segmentlerin Oluşturulması
###############################################################


cltv_df["segment"]= pd.qcut(cltv_df["CLTV"],4 , labels=("D","B","C","A"))

cltv_df.groupby("segment").agg({"recency_cltv_weekly": "mean", "frequency":"mean","monetary_cltv_avg": "mean"})

cltv_df.head()





