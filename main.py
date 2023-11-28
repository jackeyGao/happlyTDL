import streamlit as st
import time
import datetime
import arrow
import random

tz = datetime.timezone(
    datetime.timedelta(hours=8),
    name='Asia/Shanghai',
)

colors = ['blue', 'green', 'orange', 'red', 'violet', 'gray', 'rainbow']
emojis = ['🧸', '🎊', '🎉', '🎎', '🪭', '🏮', '🏮']

page_icon = "🧸"
page_title = "快乐时间倒计时"


def rc():
    return random.choice(colors)

def re(k: int=1):
    if k > 1:
        return random.sample(emojis, k=k)
    else:
        return random.sample(emojis, k=1)[0]

def rsc(input: str, ignores: list=None):
    if not ignores:
        ignores = []

    output = ""

    for i in input:
        if i.strip() and i.strip() not in ignores:
            output += f':{rc()}[{i}]'
        else:
            output += i
    return output

help_text = """
**珍惜当下**

春有百花秋有月，夏有凉风冬有雪。

若无闲事挂心头，便是人间好时节。
"""

real_help_text = rsc(help_text, ['*'])


random_image = "https://source.unsplash.com/1600x900/?background"
img_ref = "https://unsplash.com/"

st.set_page_config(page_title=page_title, page_icon=page_icon)
st.header(f":rainbow[{page_icon}]" + rsc(f" _{page_title}_", ignores=['_']))
st.markdown("""
<style>
.st-b9 .st-dk {
  height: 1px!important;     
}
</style>""",unsafe_allow_html=True)

params = st.experimental_get_query_params()


@st.cache_resource
def initialize_now():
    return arrow.now(tz=tz).shift(days=1).replace(hour=0, minute=0)


def initialize_default_datetime():
    # if 'dest_datetime' in st.session_state:
    #     return arrow.get(st.session_state.dest_datetime)

    value = params.get('datetime', [])

    if value and isinstance(value, list):
        return arrow.get(value[0])
    
    return initialize_now()


date_col, time_col = st.columns(2)

dest_date = date_col.date_input(
    "日期",
    value=initialize_default_datetime().date(),
    min_value=datetime.datetime.now(tz=tz)
)

dest_time = time_col.time_input(
    "时间",
    value=initialize_default_datetime().time(),
    step=datetime.timedelta(minutes=5),
)

dest_day = datetime.datetime(
    year=dest_date.year,
    month=dest_date.month,
    day=dest_date.day,
    hour=dest_time.hour,
    minute=dest_time.minute,
    second=dest_time.second,
    tzinfo=tz
)

# st.subheader("", divider="rainbow")

image = st.image(random_image + f'&_m={str(datetime.datetime.now(tz=tz).minute)}')
st.caption(rsc("图片来自 [unsplash]", ignores=['[', ']']) + f'({img_ref})')

container = st.empty()

n = 0
while True:
    now = datetime.datetime.now(tz=tz)

    if dest_day < now:
        container.success(real_help_text, icon=f"{re()}")
        st.stop()

    seconds = int((dest_day - now).total_seconds())
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    colors_sample = [ f":rainbow[{i}]" for i in re(k=4) ]

    d_col, h_col, m_col, s_col = container.columns(4)

    d_col.metric(label=f"{colors_sample.pop()} :{rc()}[天]", value=f"{days}")
    h_col.metric(label=f"{colors_sample.pop()} :{rc()}[小时]", value=f"{hours}")
    h_col.progress(value=1 - hours / 24)
    m_col.metric(label=f"{colors_sample.pop()} :{rc()}[分钟]", value=f"{minutes}")
    m_col.progress(value=1 - minutes / 60)
    s_col.metric(label=f"{colors_sample.pop()} :{rc()}[秒]", value=f"{seconds}")
    s_col.progress(value=1 - seconds / 60)

    n += 1; time.sleep(1)

    if n % 60 == 0:
        st.rerun()
