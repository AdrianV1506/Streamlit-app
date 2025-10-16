import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mini-Dashboard Activity", layout="wide")

# 0) Title & Intro
st.title("🎯 Mini-Dashboard: KPIs + Filters + Chart")

st.markdown(
    """
    **Goal:** Build a tiny, interactive dashboard using Streamlit + pandas + Plotly.
    
    **Dataset:** Synthetic "Course Enrollments" across Departments.
    """
)

# 1) Data (pre-loaded)
df = pd.DataFrame({
    "Department": [
        "Finance","Finance","Finance",
        "Marketing","Marketing","Marketing",
        "Engineering","Engineering","Engineering"
    ],
    "Course": [
        "Intro Analytics", "Risk Models", "Financial Viz",
        "Marketing Basics", "Segmentation", "Campaigns",
        "Intro Robotics", "ML for Sensors", "Control Systems"
    ],
    "Students": [55, 38, 44, 60, 35, 42, 48, 51, 39],
    "Satisfaction": [4.2, 3.9, 4.1, 4.5, 4.0, 3.8, 4.3, 4.4, 4.1],  # 1–5
    "Semester": ["A","A","B","A","B","B","A","A","B"]
})

# 2) Sidebar filters
st.sidebar.header("Filters")
dept = st.sidebar.multiselect(
    "Department", options=sorted(df["Department"].unique()), default=None
)
sem = st.sidebar.multiselect(
    "Semester", options=sorted(df["Semester"].unique()), default=None
)

# Radio button para elegir tipo de gráfico principal
chart_type = st.sidebar.radio(
    "Chart Type for Students per Course:",
    ["Bar Chart", "Line Chart"],
    index=0
)

fdf = df.copy()
if dept:
    fdf = fdf[fdf["Department"].isin(dept)]
if sem:
    fdf = fdf[fdf["Semester"].isin(sem)]

# 3) KPIs (top row)
c1, c2, c3, c4, c5 = st.columns(5)

total_students = int(fdf["Students"].sum())
avg_class = float(fdf["Students"].mean()) if not fdf.empty else 0.0
avg_sat = float(fdf["Satisfaction"].mean()) if not fdf.empty else 0.0
num_courses = int(fdf["Course"].nunique())
max_sat = float(fdf["Satisfaction"].max()) if not fdf.empty else 0.0  # Nuevo KPI

c1.metric("Total Students", f"{total_students:,}")
c2.metric("Avg. Students / Course", f"{avg_class:.1f}")
c3.metric("Avg. Satisfaction", f"{avg_sat:.2f} / 5")
c4.metric("Courses", f"{num_courses}")
c5.metric("Max Satisfaction", f"{max_sat:.2f} / 5")  # Mostrar KPI nuevo

# 4) Table + Chart (second row)
tcol, gcol = st.columns([1,2])

with tcol:
    st.subheader("Filtered Data")
    st.dataframe(fdf, use_container_width=True, hide_index=True)

with gcol:
    st.subheader("Students by Course")
    # Chart principal: color por Semester (antes era Department)
    if chart_type == "Bar Chart":
        fig = px.bar(
            fdf,
            x="Course", y="Students",
            color="Semester",
            title="Students per Course (filtered)",
            text="Students"
        )
    else:  # Line Chart
        fig = px.line(
            fdf,
            x="Course", y="Students",
            color="Semester",
            title="Students per Course (filtered)",
            markers=True
        )
    fig.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

# 5) Second Chart
st.subheader("Comparison Chart")
comp_option = st.radio("Choose comparison:", ["Satisfaction by Department", "Students by Semester"])

if comp_option == "Satisfaction by Department":
    fig2 = px.box(
        fdf,
        x="Department", y="Satisfaction",
        color="Department",
        title="Satisfaction by Department"
    )
else:
    fig2 = px.bar(
        fdf.groupby("Semester", as_index=False)["Students"].sum(),
        x="Semester", y="Students",
        color="Semester",
        title="Total Students by Semester",
        text="Students"
    )
st.plotly_chart(fig2, use_container_width=True)

# 6) mini-questions
with st.expander("✅ Bonus: answer these directly in Streamlit text inputs"):
    q1 = st.text_input("Q1) Which department has the highest total enrollment under your current filter?")
    q2 = st.text_input("Q2) Which single course is the most popular?")
    q3 = st.text_area("Q3) Propose one actionable insight based on the chart/KPIs:")

    st.caption("Tip: adjust filters and read the KPIs + chart to justify your answers.")

# 7) Explanation of grouping difference
st.markdown(
    """
    ---
    ### 🔎 Observation:
    - **Color by Department**: lets you compare how each department’s courses perform against each other.  
    - **Color by Semester**: instead highlights when (A or B) students are enrolled, showing patterns across time rather than organizational units.  
    """
)

st.toast("App ready — complete the TODOs in the code and refresh!", icon="✅")
