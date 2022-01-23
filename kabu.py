import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('株価アプリ テスト')
st.sidebar.write("""
# LLL株価
こちらは株価可視化ツール。以下から表示日付を指定してください。
""")
st.sidebar.write("""
## 表示日数選択
""")
days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去 **{days}**日の株価
""")


@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        appl = yf.Ticker(tickers[company])
        his = appl.history(period=f'{days}d')
        his.reset_index()
        his.index = his.index.strftime('%d %B %Y')
        his = his[['Close']]
        his.columns = [company]
        his = his.T
        his.index.name = 'Name'
        df = pd.concat([df, his])
    return df


try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定ください。',
        0.0, 3500.0, (0.0, 3500.0)
    )
    tickers = {
        'apple': 'AAPL',
        'google': 'GOOGL',
        'netflix': 'NFLX'
    }
    df = get_data(days, tickers)
    sel = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['google', 'apple']
    )

    if not sel:
        st.error('会社を選択してください！')
    else:
        data = df.loc[sel]
        st.write("### 株価(USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'USD'}
        )
    chart = (
        alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
            x="Date:T",
            y=alt.Y("USD:Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N'
        )
    )

    st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "505 error!"
    )
