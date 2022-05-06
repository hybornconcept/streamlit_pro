
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime
from streamlit_option_menu import option_menu


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

mainstyle = """
    <style>
    # root{
primaryColor:'#E84C29';
Background-color:'#273346';
font-color:'#FFFFFF';
font-family: "sans serif";
}
.css-2ykyy6 .egzxvld0 {visibility: hiddden;}
header {visibility: hiddden;}
    </style>
    """
st.markdown(mainstyle, unsafe_allow_html=True)

with open("style.css") as f:
    st.markdown('<style>{f.read()}<style>', unsafe_allow_html=True)

conn = sqlite3.connect('data.db', check_same_thread=False)
cur = conn.cursor()
bigcollector = []
collector = []
entrysection = st.container()
mainsection = st.container()
loginsection = st.container()
df_selection = 1

facilityoptions = ["Select the Facility",
                   "Akamkpa General Hospital",
                   "Calabar General Hospital",
                   "Ugep General Hospital",
                   "Sankwala General Hospital",
                   "Initiative Of People Good Health (Ipgh) Youth Center",
                   "Calabar Municipal Youth Resource Center",
                   "Youth Hub Unical"]

LGAoptions = ["Select the LGA",
              "Calabar",
              "Akamkpa",
              "Yakurr",
              "Obanliku"
              ]

stateoptions = ["Select the State",
                "Cross river",
                "Akwa ibom",
                ]

YearOptions = ["Select the Year", "2021", "2022"]
Monthoptions = ["Select the Month",
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"]

list = ["", "10-14yrs", "15-19yrs", "20-24yrs", "25-35yrs",
        "10-14yrs", "15-19yrs", "20-24yrs", "25-35yrs", ""]
listed = ["10-14yrs_male", "15-19yrs_male", "20-24yrs_male", "25-35yrs_male",
          "10-14yrs_female", "15-19yrs_female", "20-24yrs_female", "25-35yrs_female"]
# questions = ["Safe Sex", "STI Prevention", "Contraceptive Use",
#              "Drug Abuse", "Sexual Violence", "Unplanned Pregnancy", "Others (specify)"]

body = {
    "Total  Attendance":     ["Old Clients", "New Clients"],
    "Counseling on":            ["Safe Sex", "STI Prevention", "Contraceptive Use",
                                 "Drug Abuse", "Sexual Violence", "Unplanned Pregnancy", "Others (specify)"],
    " HIV Testing and Couseling": ["HIV Result negative (-ve)", "HIV Result positive (+ve)"],

    "Family Planning": ["Total no of clients receiving condom",
                        "Total no of condoms dispensed (in pieces)",
                        "Total no clients receiving Oral Contraceptive Pills (OPC)",
                        "Total no of clients receiving injectables",
                        "Total no of clients that had Implants inserted"],

    "HIV Care and Treatment": ["Enrolment into Care",
                               "HIV Treatment (ART)",
                               "PMTCT"],
    "Other Services": ["Post Abortion Care",
                       "Sydromic Management of STIs",
                       "Antenatal Care",
                       "Others"],
    "Treatment of Minor Ailments": ["Treatment of Minor Ailments"],
    "Group Contact Activities": ["Number of Adolescents and Young People reached through health talks held at the centre",
                                 "Number of School Visits Conducted",
                                 "Number of Adolescents and Young People reached through school visits",
                                 "Number of Outreaches /Group health talk conducted",
                                 "Number of Adolescents and Young People reached through outreaches/group health talks conducted"
                                 ],

    "Status": ["Number of  In School Youth (ISY) that accessed the centre",
               "Number of  Out School Youth (OSY) that accessed the centre",
               "Number of Clients referred",
               ]
}
keysList = [key for key in body]
# # print(keysList[1])
# questions = [body[i] for i in body]
# # print(questions[1][1])
if 'header' not in st.session_state:
    st.session_state['header'] = False


def authen(username, password):
    users = ['admin', 'CRSO', 'Bedet', 'Orose', 'Nchigbu',
             'Ionyekuru', 'Aapinega', 'Cthompson']
    passwods = ['admin', 'admin1', 'admin2', 'admin3',
                'admin4', 'admin5', 'admin6' 'admin7']

    koler1, col2, col3 = st.columns(3)
    with col2:
        try:
            users.index(username) == passwods.index(password)

        except ValueError:
            st.session_state['loggedin'] = False
            st.error('Invalid Username or Password')

        else:
            st.session_state['loggedin'] = True
            if username == 'admin' and password == 'admin':
                st.session_state['header'] = True

            else:
                st.session_state['header'] = False


def showLogin():
    with loginsection:
        col1, col2, col3 = st.columns(3)

        with col2:
            st.write("## ASRH Monthly Data Collector")
            username = st.text_input("Enter your Username")
            password = st.text_input("Enter your Password", type="password")

            st.button("Login", on_click=authen, args=(username, password))


def spacer(order, number):
    for i in range(number):
        order.markdown(
            '<br/>', unsafe_allow_html=True)


def liner(order, number):
    for i in range(number):
        order.markdown(
            '<hr/>', unsafe_allow_html=True)


def spiller(title, questions):
    x = 0
    count = 0

    with st.expander(title):
        male, Female = st.columns(2)
        linemale, lineFemale = st.columns(2)
        male.write(
            '<h4 class="small-font" style="text-align: center;">Male</h4>', unsafe_allow_html=True)
        liner(linemale, 1)
        Female.write(
            '<h4 class="small-font" style="text-align: center;">Female</h4>', unsafe_allow_html=True)
        liner(lineFemale, 1)
        cols = st.columns(10)
        count = 0

        for j in questions:

            for (i, col, e) in zip(list, cols, range(1, 11)):

                index = questions.index(j)+1

                e += index*10
                keys = j + str(e)
                if e == 1 or e % 10 == 1:

                    if (title in keysList[2:6] or title in keysList[0]):

                        col.markdown(
                            '<h6 class="small-font" style=" margin-top:25%;  ">{questions}</h6>'.format(questions=j), unsafe_allow_html=True)
                        spacer(col, 2)
                    elif (title == keysList[1]):
                        col.markdown(
                            '<h6 class="small-font" style=" margin-top:25%;  ">{questions}</h6>'.format(questions=j), unsafe_allow_html=True)

                        spacer(col, 3)
                    else:
                        col.markdown(
                            '<h6 class="small-font" style=" margin-top:26%;  ">{questions}</h6>'.format(questions=j), unsafe_allow_html=True)
                        # liner(col, 1)
                elif e % 10 == 0:

                    if questions.index(j) == count:
                        submitted1 = col.form_submit_button('sum', help=j)

                        if submitted1 == False:

                            col.write(
                                '<h5 class="vertical-center small-font" style="margin-left: 2.5%;">{fname}</h5>'.format(fname=0), unsafe_allow_html=True)
                        else:
                            hh = [sum(collector[i:i+len(questions)+1])
                                  for i in range(0, len(collector), len(questions)+1)]
                            col.write(
                                '<h5 class=" vertical-center small-font" style="margin-left: 2.5%;">{fname}</h5>'.format(fname=hh[questions.index(j)]), unsafe_allow_html=True)

                    else:
                        continue

                else:
                    x = col.number_input(i, min_value=0, key=keys)
                    collector.append(x)
                    liner(col, 1)
            liner(col, 1)
            count += 1


def addData(holder):
    holder = []
    linelist = [body[i] for i in body]
    flat_list = [item for sublist in linelist for item in sublist]
    for y in listed:
        for x in flat_list:
            holder.append(x+"_"+y)

    header_columns_commands = []
    query = ""
    for h in holder:

        if h == holder[0]:

            header_columns_commands += "\"%s\"" % h.replace(" ", "_")
            header_columns_commands += " TEXT(4) "

        else:
            header_columns_commands += " , "
            header_columns_commands += "\"%s\"" % h.replace(" ", "_")
            header_columns_commands += " TEXT(4)"
    query += "CREATE TABLE IF NOT EXISTS ASRHMSF (\"Timestamp\" TEXT(50), \"State\" TEXT(50),\"LGA\" TEXT(50)  ,\"Facility\" TEXT(50), \"Year\" TEXT(50) ,\"Month\" TEXT(50)  , "
    query += "".join(header_columns_commands)
    query += ");"

    #########

    mark = []
    newquery = ""
    newcollector = [str(int(i)) for i in collector]
    bigcollector.extend(newcollector)
    for v in bigcollector[:6]:
        if v == bigcollector[0]:
            mark += "\"%s\"" % v
        else:
            mark += " , "
            mark += "\"%s\"" % v

    for v in bigcollector[6:]:
        if v == bigcollector[0]:
            mark += v

        else:
            mark += " , "
            mark += v

    newquery += "insert into ASRHMSF  values ( "
    newquery += "".join(mark)
    newquery += " );"
    bad = """DROP TABLE ASRHMSF;"""
    # st.write(newquery)
    try:

        cur.execute(query)
        cur.execute(newquery)
        # cur.execute(bad)

    except sqlite3.Error as error:
        st.write("Failed to insert data into sqlite table", error)
    finally:
        if conn:
            st.success("succesfully inserted")
            st.success("The SQLite connection is closed")
            conn.commit()
            conn.close()


def retrieve():
    # body
    dlist = [(key, i) for key, value in body.items() for i in value]
    beta = pd.DataFrame(dlist, columns=['dataset', 'Beta_indicator'])
    # database
    cnx = sqlite3.connect('data.db')
    df = pd.read_sql_query("SELECT * FROM ASRHMSF", cnx)
    # main
    melt = df.melt(id_vars=df.columns[:6])
    main = melt['variable'].str.rsplit('_', 2, expand=True).join(melt)
    main.rename(columns={0: 'indicators', 1: 'Age', 2: 'Sex'}, inplace=True)
    main.replace(r"_", "", regex=True)
    main['indicators'] = main['indicators'].replace(
        '_', ' ', regex=True).str.strip()
    beta['Beta_indicator'].str.strip()
    # merge
    main = main.merge(beta, left_on="indicators", right_on='Beta_indicator')
    main.drop(columns=['variable',
              'Beta_indicator'], inplace=True)
    main = main.reindex(columns=['Timestamp', 'Facility', 'State', 'LGA', 'Year',
                        'Month', 'Age', 'Sex', 'dataset', 'indicators',  'value'])
    main['value'] = pd.to_numeric(main['value'])
    return main


def show_database():
    st.markdown("### ASRHMSF Monthly Reported data")
    st.dataframe(retrieve())


def navbar():
    selected = option_menu(
        menu_title=None,
        options=['Home', 'Database', 'Dashboard'],
        icons=['house', 'wallet2', 'bar-chart'],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "5!important", "background-color": "black", "width": "50%"},
            "icon": {"color": "red", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#2C3845"},
        }
    )
    if selected == "Home":
        showmainpage()

    elif selected == "Database":
        show_database()

    else:
        show_dashboard()


# def metrics(list1):
#     cols = st.columns(len(list1))
#     for (x, i) in zip(cols, list1):
#         x.metric(i, "70 °F", "1.2 °F")

def metrics(list1, df):
    cols = st.columns(len(list1))
    for (x, i) in zip(cols, list1):
        x.metric(i, df[i].sum())


def show_dashboard():
    st.sidebar.header("Please Filter Here:")
    df = retrieve()
    State = st.sidebar.multiselect(
        "Select the State:",
        options=df["State"].unique(),
        default=df["State"].unique()

    )

    LGA = st.sidebar.multiselect(
        "Select the LGA:",
        options=df["LGA"].unique(),
        default=df["LGA"].unique(),
    )

    Facility = st.sidebar.multiselect(
        "Select the Facility:",
        options=df["Facility"].unique(),
        default=df["Facility"].unique()
    )

    Year = st.sidebar.multiselect(
        "Select the Year:",
        options=df["Year"].unique(),
        default=df["Year"].unique()
    )

    Month = st.sidebar.multiselect(
        "Select the Month:",
        options=df["Month"].unique(),
        default=df["Month"].unique()
    )
    dataset = st.sidebar.multiselect(
        "Select the dataset:",
        options=df["dataset"].unique(),
        default=df["dataset"].unique().tolist()[1:2]
    )

    indicators = st.sidebar.multiselect(
        "Select the indicators:",
        options=df["indicators"].unique(),
        default=df["indicators"].unique().tolist()[2:9]

    )

    Age = st.sidebar.multiselect(
        "Select the Age:",
        options=df["Age"].unique(),
        default=df["Age"].unique()
    )

    Sex = st.sidebar.multiselect(
        "Select the Sex:",
        options=df["Sex"].unique(),
        default=df["Sex"].unique()

    )

    filtered_df = df[(df['State'].isin(State)) & (df["LGA"].isin(LGA)) & (df["Facility"].isin(Facility))
                     & (df["Year"].isin(Year)) & (df["Month"].isin(Month)) & (df["dataset"].isin(dataset))
                     & (df["indicators"].isin(indicators)) & (df["Age"].isin(Age)) &
                     (df["Sex"].isin(Sex))]

    df1 = filtered_df.pivot(
        index=filtered_df.columns[:9], columns='indicators', values='value')
    liner(st, 1)
    metrics(df1.columns, df1)
    liner(st, 1)
    # st.dataframe(filtered_df)
    hcol, vcol = st.columns(2)
    # SALES BY PRODUCT LINE [BAR CHART]
    sales_by_product_line = (
        filtered_df.groupby(by=["indicators"]).sum()[
            ["value"]].sort_values(by="value")
    )
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="value",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>Sales by Product Line</b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
        text="value"
    )
    fig_product_sales.update_layout(
        height=600,
        plot_bgcolor="#0E1117",
        yaxis=(dict(showgrid=False)),
        xaxis=(dict(showgrid=False))
    )

    second = filtered_df.groupby(
        by=["indicators", "Sex"]).sum().reset_index()

    fig = px.bar(second,  x='indicators', y="value",
                 color="Sex",
                 text="value",
                 barmode='group')

    fig.update_layout(
        height=600,
        width=800,
        plot_bgcolor="#0E1117",
        yaxis=(dict(showgrid=False)),
        xaxis=(dict(showgrid=False))
    )

    hcol.write(fig_product_sales)
    vcol.write(fig)

    # scol, ecol = st.columns(2)

    third = filtered_df.groupby(
        by=["indicators", "Age"]).sum().reset_index()

    fig2 = px.bar(third,  x='indicators', y="value",
                  color="Age",
                  text="value",
                  barmode='group')

    fig2.update_layout(
        height=600,
        width=1300,
        plot_bgcolor="#0E1117",
        yaxis=(dict(showgrid=False)),
        xaxis=(dict(showgrid=False))
    )

    st.write(fig2)


def showmainpage():

    with mainsection:

        st.header("ASRH Monthly Data Collector")
        st.write(
            "Adolescents And Young People Reproductive Health Services Monthly Data Summary Form")
        spacer(st, 1)

        with st.form(key='columns_in_form'):
            kol1, kol2, kol3, kol4, kol5 = st.columns(5)
            with kol1:
                state = st.selectbox(
                    'State',
                    stateoptions)
            with kol2:
                LGA = st.selectbox(
                    'LGA',
                    LGAoptions)
            with kol3:
                facility = st.selectbox(
                    'Facility',
                    facilityoptions)
            with kol4:
                year = st.selectbox(
                    'Reporting Year',
                    YearOptions)
            with kol5:
                month = st.selectbox(
                    'Reporting Month',
                    Monthoptions)

            liner(st, 1)
            spacer(st, 3)
            # datetime object containing current date and time
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            bigcollector.append(dt_string)
            bigcollector.append(state)
            bigcollector.append(LGA)
            bigcollector.append(facility)
            bigcollector.append(year)
            bigcollector.append(month)

            spacer(st, 1)

            for key, value in body.items():
                spiller(key, value)

            submitted = st.form_submit_button('Submit')
            if submitted:
                addData(collector)


with entrysection:
    # st.title("ASRH Monthly Data Collector")
    if 'loggedin' not in st.session_state:
        st.session_state['loggedin'] = False
        showLogin()
    else:
        if st.session_state['loggedin']:
            with st.spinner("Loading..."):
                time.sleep(1)
                if st.session_state['header'] == True:
                    navbar()
                    # showmainpage()

        else:
            showLogin()
