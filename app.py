
from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "launches_dashboard.csv"
df = pd.read_csv(DATA, parse_dates=["Date"])

SITE_COORDS = {
    "CCAFS LC-40": (28.5623, -80.5774),
    "CCAFS SLC-40": (28.5619, -80.5774),
    "KSC LC-39A": (28.6084, -80.6043),
    "VAFB SLC-4E": (34.6321, -120.6108),
}

# Keep the dashboard deterministic and usable offline once the repository is cloned.
df["Launch Site"] = df["Launch Site"].str.strip()
df["Year"] = df["Date"].dt.year

app = Dash(__name__)
app.title = "Falcon 9 Analytics"

CARD = {
    "background": "#111827",
    "border": "1px solid #243044",
    "borderRadius": "14px",
    "padding": "18px",
    "boxShadow": "0 8px 24px rgba(0,0,0,.18)",
}

def kpi(label, value, sub=""):
    return html.Div([
        html.Div(label, style={"fontSize": "12px", "color": "#94a3b8", "textTransform": "uppercase",
                               "letterSpacing": "1px"}),
        html.Div(value, style={"fontSize": "28px", "fontWeight": "700", "marginTop": "6px"}),
        html.Div(sub, style={"fontSize": "12px", "color": "#64748b", "marginTop": "4px"}),
    ], style=CARD)

app.layout = html.Div([
    html.Div([
        html.Div("FALCON 9 • ANALYTICS", style={"fontSize": "13px", "letterSpacing": "2px", "color": "#60a5fa"}),
        html.H1("Launch & Landing Intelligence", style={"margin": "6px 0 4px", "fontSize": "38px"}),
        html.P("An end-to-end data analytics portfolio: collection, wrangling, SQL, EDA, visualization and predictive modeling.",
               style={"color": "#94a3b8", "maxWidth": "900px"}),
    ], style={"padding": "28px 0 18px"}),

    html.Div([
        html.Div([
            html.Label("Launch site"),
            dcc.Dropdown(id="site", options=[{"label":"All sites","value":"ALL"}] +
                         [{"label":x,"value":x} for x in sorted(df["Launch Site"].dropna().unique())],
                         value="ALL", clearable=False),
        ]),
        html.Div([
            html.Label("Orbit"),
            dcc.Dropdown(id="orbit", options=[{"label":"All orbits","value":"ALL"}] +
                         [{"label":x,"value":x} for x in sorted(df["Orbit"].dropna().unique())],
                         value="ALL", clearable=False),
        ]),
        html.Div([
            html.Label("Booster generation"),
            dcc.Dropdown(id="booster", options=[{"label":"All generations","value":"ALL"}] +
                         [{"label":x,"value":x} for x in sorted(df["Booster Version Category"].dropna().unique())],
                         value="ALL", clearable=False),
        ]),
        html.Div([
            html.Label("Payload range (kg)"),
            dcc.RangeSlider(id="payload", min=float(df["Payload Mass (kg)"].min()),
                            max=float(df["Payload Mass (kg)"].max()), step=250,
                            value=[float(df["Payload Mass (kg)"].min()), float(df["Payload Mass (kg)"].max())],
                            tooltip={"placement":"bottom","always_visible":False}),
        ], style={"padding": "0 8px 0 4px"}),
    ], style={**CARD, "display":"grid", "gridTemplateColumns":"1fr 1fr 1fr 2fr", "gap":"16px", "marginBottom":"18px"}),

    html.Div(id="kpis", style={"display":"grid","gridTemplateColumns":"repeat(4,1fr)","gap":"14px","marginBottom":"18px"}),

    html.Div([
        html.Div(dcc.Graph(id="trend"), style=CARD),
        html.Div(dcc.Graph(id="site-chart"), style=CARD),
    ], style={"display":"grid","gridTemplateColumns":"1.35fr 1fr","gap":"14px","marginBottom":"14px"}),

    html.Div([
        html.Div(dcc.Graph(id="orbit-chart"), style=CARD),
        html.Div(dcc.Graph(id="payload-chart"), style=CARD),
    ], style={"display":"grid","gridTemplateColumns":"1fr 1.35fr","gap":"14px","marginBottom":"14px"}),

    html.Div([
        html.Div(dcc.Graph(id="map"), style=CARD),
        html.Div(dcc.Graph(id="booster-chart"), style=CARD),
    ], style={"display":"grid","gridTemplateColumns":"1.35fr 1fr","gap":"14px"}),

], style={"background":"#0b1120","color":"#e5e7eb","minHeight":"100vh",
          "padding":"0 4vw 40px","fontFamily":"Inter,system-ui,-apple-system,Segoe UI,sans-serif"})

@app.callback(
    Output("kpis","children"),
    Output("trend","figure"),
    Output("site-chart","figure"),
    Output("orbit-chart","figure"),
    Output("payload-chart","figure"),
    Output("map","figure"),
    Output("booster-chart","figure"),
    Input("site","value"), Input("orbit","value"), Input("booster","value"), Input("payload","value")
)
def update(site, orbit, booster, payload):
    d = df[(df["Payload Mass (kg)"] >= payload[0]) & (df["Payload Mass (kg)"] <= payload[1])].copy()
    if site != "ALL":
        d = d[d["Launch Site"] == site]
    if orbit != "ALL":
        d = d[d["Orbit"] == orbit]
    if booster != "ALL":
        d = d[d["Booster Version Category"] == booster]

    launches = len(d)
    successes = int(d["Landing Success"].sum()) if launches else 0
    rate = successes / launches if launches else 0
    avg_payload = d["Payload Mass (kg)"].mean() if launches else 0

    cards = [
        kpi("Launches", f"{launches:,}", "Filtered observations"),
        kpi("Successful landings", f"{successes:,}", f"of {launches:,} launches"),
        kpi("Landing success rate", f"{rate:.1%}", "Success / filtered launches"),
        kpi("Average payload", f"{avg_payload:,.0f} kg", "Filtered payload mass"),
    ]

    def base(fig):
        fig.update_layout(template="plotly_dark", paper_bgcolor="#111827", plot_bgcolor="#111827",
                          margin=dict(l=45,r=20,t=55,b=45), font=dict(color="#e5e7eb"))
        return fig

    yr = d.groupby("Year", as_index=False).agg(launches=("Landing Success","size"),
                                                success_rate=("Landing Success","mean"))
    fig_trend = base(px.line(yr, x="Year", y="success_rate", markers=True,
                             title="Landing success rate over time"))
    fig_trend.update_yaxes(tickformat=".0%", range=[0,1])

    st = d.groupby("Launch Site", as_index=False).agg(launches=("Landing Success","size"),
                                                        success_rate=("Landing Success","mean")).sort_values("success_rate")
    fig_site = base(px.bar(st, x="success_rate", y="Launch Site", orientation="h",
                           text="launches", title="Launch-site performance"))
    fig_site.update_xaxes(tickformat=".0%", range=[0,1])
    fig_site.update_traces(texttemplate="%{text} launches", textposition="outside")

    ob = d.groupby("Orbit", as_index=False).agg(launches=("Landing Success","size"),
                                                 success_rate=("Landing Success","mean")).sort_values("success_rate")
    fig_orbit = base(px.bar(ob, x="Orbit", y="success_rate", title="Success rate by orbit"))
    fig_orbit.update_yaxes(tickformat=".0%", range=[0,1])

    fig_payload = base(px.scatter(d, x="Payload Mass (kg)", y="Landing Success",
                                  color="Booster Version Category", hover_data=["Flight Number","Launch Site","Orbit"],
                                  title="Payload mass vs landing outcome"))
    fig_payload.update_yaxes(tickvals=[0,1], ticktext=["Failure","Success"], range=[-0.15,1.15])

    mp = d.copy()
    mp["Lat"] = mp["Launch Site"].map(lambda x: SITE_COORDS.get(x, (None,None))[0])
    mp["Lon"] = mp["Launch Site"].map(lambda x: SITE_COORDS.get(x, (None,None))[1])
    mp = mp.dropna(subset=["Lat","Lon"])
    fig_map = base(px.scatter_geo(mp, lat="Lat", lon="Lon", color="Outcome Label",
                                  hover_name="Launch Site",
                                  hover_data=["Flight Number","Payload Mass (kg)","Orbit"],
                                  title="Launch-site geography"))
    fig_map.update_geos(scope="usa", showcountries=True, showland=True, showocean=True,
                        fitbounds="locations")

    bv = d.groupby("Booster Version Category", as_index=False).agg(
        launches=("Landing Success","size"), success_rate=("Landing Success","mean"))
    fig_booster = base(px.bar(bv, x="Booster Version Category", y="success_rate",
                              text="launches", title="Performance by booster generation"))
    fig_booster.update_yaxes(tickformat=".0%", range=[0,1])
    fig_booster.update_traces(texttemplate="%{text} launches", textposition="outside")

    return cards, fig_trend, fig_site, fig_orbit, fig_payload, fig_map, fig_booster

if __name__ == "__main__":
    app.run(debug=True)
