import streamlit as st
import time
import datetime
import arrow

tz = datetime.timezone(
    datetime.timedelta(hours=8),
    name='Asia/Shanghai',
)

help_text = """
春有百花秋有月，夏有凉风冬有雪。\n
若无闲事挂心头，便是人间好时节。\n
"""

random_image = "https://source.unsplash.com/1600x900/?background"

st.set_page_config(page_title="快乐时间倒计时", page_icon="🧸")
st.header(f"🧸 快乐时间倒计时")

params = st.experimental_get_query_params()


def initialize_default_datetime():
    value = params.get('datetime', [])

    if value and isinstance(value, list):
        return arrow.get(value[0])
    
    return arrow.now(tz=tz).shift(days=1)


date_col, time_col = st.columns(2)

with date_col:
    dest_date = st.date_input(
        "日期",
        value=initialize_default_datetime().date(),
        min_value=datetime.datetime.now(tz=tz)
    )

with time_col:
    dest_time = st.time_input(
        "时间",
        value=initialize_default_datetime().time(),
    )

st.image(random_image, caption="来自 unsplash")

# st.subheader("", divider="rainbow")

container = st.empty()

while True:
    now = datetime.datetime.now(tz=tz)

    dest_day = datetime.datetime(
        year=dest_date.year,
        month=dest_date.month,
        day=dest_date.day,
        hour=dest_time.hour,
        minute=dest_time.minute,
        second=dest_time.second,
        tzinfo=tz
    )

    if dest_day < now:
        container.success(help_text, icon="🧸")
        st.stop()

    seconds = int((dest_day - now).total_seconds())
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    d_col, h_col, m_col, s_col = container.columns(4)

    with d_col:
        st.metric(label=":blue[天]", value=f"{days}")

    with h_col:
        st.metric(label=":yellow[小时]", value=f"{hours}")

    with m_col:
        st.metric(label=":green[分钟]", value=f"{minutes}")

    with s_col:
        st.metric(label=":red[秒]", value=f"{seconds}")

    time.sleep(1)
