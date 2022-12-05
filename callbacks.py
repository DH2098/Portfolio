from dash import dcc, Input, Output, State 

from app import app

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
 
df = pd.read_csv("data/df.csv")

genre_df = pd.read_csv("data/genre_df.csv")
genre_df.set_index('year',inplace=True)
genre_df_10 = pd.read_csv("data/genre_df_10.csv")
genre_df_10.set_index('year',inplace=True)

genre_ani_df = pd.read_csv("data/genre_ani_df.csv")
genre_ani_10_df = pd.read_csv("data/genre_ani_10_df.csv")

titles_df = pd.read_csv("data/titles_df.csv")
cast_title_df = pd.read_csv("data/cast_title_df.csv")
director_title_df = pd.read_csv("data/director_title_df.csv")

genre_corr_df = pd.read_csv("data/genre_cor_df.csv")
cast_corr_df = pd.read_csv("data/cast_cor_df.csv")
director_corr_df = pd.read_csv("data/director_cor_df.csv")

keyword_df = pd.read_csv("data/keyword_df.csv").fillna('')

genre_recommender_df = pd.read_csv("data/genre_recommender.csv")
director_recommender_df = pd.read_csv("data/director_recommender.csv")
cast_recommender_df = pd.read_csv("data/cast_recommender.csv")
title_recommender_df = pd.read_csv("data/title_recommender.csv")

recommender_dict = {
    '장르별 영화 추천' : [],
    '감독별 영화 추천' : sorted([i for i in director_title_df.director]),
    '배우별 영화 추천' : sorted([i for i in cast_title_df.cast]),
    '제목별 영화 추천' : sorted([i for i in titles_df.title.map(lambda x:x.replace("'",""))])
    }

# 메인 페이지
@app.callback(
    Output("download-df", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, "TMDB_5000_Movie_Dataset.csv")

## 1년 단위 추세
@app.callback(
    Output("trend-year-graph", "figure"),
    Input("trend-year-RS", "value"),
)
def update_chart(slider_range):
    low, high = slider_range
    mask = (genre_ani_df.year >= low) & (genre_ani_df.year <= high) 

    fig = px.bar(        
        genre_ani_df[mask],
        x = 'year',
        y = 'count',
        color='genres'        
    )
    fig.update_traces(hovertemplate=None)
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor = 'rgb(240, 242, 245)',
        height = 600,
        )
    return fig

## 10년 단위 추세
@app.callback(
    Output("trend-decade-graph", "figure"),
    Input("trend-decade-RS", "value"),
)
def update_chart(slider_range):
    low, high = slider_range
    mask = (genre_ani_10_df.year >= low) & (genre_ani_10_df.year <= high) 

    fig = px.bar(        
        genre_ani_10_df[mask],
        x = 'year',
        y = 'count',
        color='genres'
    )
    fig.update_traces(hovertemplate=None)
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor = 'rgb(240, 242, 245)',
        height = 600,
        )
    return fig

# 제목 흥행
@app.callback(
    Output("title_revenue_fig", "figure"),
    Input("submit-title","n_clicks"),
    State('title-select', 'value')
)
def updatde_title_revenue_fig(n_clicks, value):

    if (value is None) or (n_clicks is None):
        df = titles_df
    else:
        df = titles_df[titles_df['title'].isin(value)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x = df['title'],
        y = df['revenue'],
        customdata=np.stack((df['director'], df['cast'], df['genres'], df['revenue'], df['vote_average'], df['popularity']), axis=-1),
        hovertemplate="<b>제목 : %{x}</b>" +
        "<br>흥행 수익 : %{customdata[3]}" +
        "<br><br><b> *** 정보 *** </b><br>" +
        "<br>감독 : %{customdata[0]}" +
        "<br>배우 : %{customdata[1]}" +
        "<br>장르 : %{customdata[2]}" +     
        "<br>평점 : %{customdata[4]}" +    
        "<br>인기도 : %{customdata[5]}<extra></extra>",
        marker_color='lightcoral'
        ))
    fig.update_layout(
        hoverlabel=dict(
            bgcolor='white',
            font_size=16,
        ),
        plot_bgcolor = 'rgb(240, 242, 245)',
    )

    return fig

# 배우 흥행
@app.callback(
    Output("cast_revenue_fig", "figure"),
    Input("submit-cast","n_clicks"),
    State('cast-select', 'value')
)
def updatde_cast_revenue_fig(n_clicks, value):

    if (value is None) or (n_clicks is None):
        df = cast_title_df
    else:
        df = cast_title_df[cast_title_df['cast'].isin(value)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x = df['cast'],
        y = df['revenue'],
        customdata = df['top5'],
        hovertemplate="<b>배우 : %{x}</b>" +
        "<br>흥행 수익 : %{y}<br>" +
        "<br><b> *** 대표작 *** </b>  <br>%{customdata}<extra></extra>",
        marker_color='teal'
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor='white',
            font_size=16,
        ),
        plot_bgcolor = 'rgb(240, 242, 245)',
    )

    return fig

# 감독 흥행
@app.callback(
    Output("director_revenue_fig", "figure"),
    Input("submit-director","n_clicks"),
    State('director-select', 'value')
)
def updatde_director_revenue_fig(n_clicks, value):

    if (value is None) or (n_clicks is None):
        df = director_title_df
    else:
        df = director_title_df[director_title_df['director'].isin(value)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x = df['director'],
        y = df['revenue'],
        customdata = df['top5'],
        hovertemplate="<b>감독 : %{x}</b>" +
        "<br>흥행 수익 : %{y}<br>" +
        "<br><b> *** 대표작 *** </b>  <br>%{customdata}<extra></extra>",
        marker_color='thistle'
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor='white',
            font_size=16,
        ),
        plot_bgcolor = 'rgb(240, 242, 245)',
    )

    return fig

@app.callback(
    Output("keyword-fig", "figure"),
    Input("submit-keyword","n_clicks"),
    State('keyword-select', 'value')
)
def updatde_keyword_fig(n_clicks, value):
    
    if (n_clicks is None) or (value is None):
        fig = go.Figure()
    
    else:
        fig = px.treemap(keyword_df[keyword_df.idx==value], 
                    path = [px.Constant('키워드'), 'idx', '키워드'], 
                    values = 'count',
                    color = 'count',
                    color_continuous_scale = 'Blues'
                    )
        fig.update_traces(hovertemplate='<b>%{label}</b> <br> Count : %{value}')
        fig.update_layout(margin = dict(t=25, l=25, r=25, b=25))
        
    return fig

@app.callback(
    Output("corr-fig1", "figure"),
    Input("submit-corr","n_clicks"),
    State('corr-select', 'value')
)
def updatde_corr_fig(n_clicks, value):

    if (n_clicks is None) or (value is None):
        fig = go.Figure()
    
    elif value == 'corr_genre':
        df = genre_corr_df
        
        fig = go.Figure(data=go.Splom(
                        dimensions=[dict(label='장르',
                                        values=df['name']),
                                    dict(label='수익',
                                        values=df['revenue']),
                                    dict(label='인기도',
                                        values=df['popularity']),
                                    dict(label='평점',
                                        values=df['vote_average'])],
                        diagonal_visible=False,
                        hovertemplate='%{xaxis.title.text}=%{x}<br>%{yaxis.title.text}=%{y}<extra></extra>',
                        marker=dict(color=df['genres'],
                                    showscale=False,
                                    line_color='white', line_width=0.5)
                        ))

        fig.update_layout(plot_bgcolor = 'rgb(240, 242, 245)')

    elif value == 'corr_cast':
        df = cast_corr_df

        fig = go.Figure(data=go.Splom(
                        dimensions=[dict(label='배우',
                                        values=df['name']),
                                    dict(label='수익',
                                        values=df['revenue']),
                                    dict(label='인기도',
                                        values=df['popularity']),
                                    dict(label='평점',
                                        values=df['vote_average'])],
                        diagonal_visible=False,
                        hovertemplate='%{xaxis.title.text}=%{x}<br>%{yaxis.title.text}=%{y}<extra></extra>',
                        marker=dict(color=df['cast'],
                                    showscale=False,
                                    line_color='white', line_width=0.5)
                        ))

        fig.update_layout(plot_bgcolor = 'rgb(240, 242, 245)')

    else:
        df = director_corr_df

        fig = go.Figure(data=go.Splom(
                        dimensions=[dict(label='감독',
                                        values=df['name']),
                                    dict(label='수익',
                                        values=df['revenue']),
                                    dict(label='인기도',
                                        values=df['popularity']),
                                    dict(label='평점',
                                        values=df['vote_average'])],
                        diagonal_visible=False,
                        hovertemplate='%{xaxis.title.text}=%{x}<br>%{yaxis.title.text}=%{y}<extra></extra>',
                        marker=dict(color=df['director'],
                                    showscale=False,
                                    line_color='white', line_width=0.5)
                        ))

        fig.update_layout(plot_bgcolor = 'rgb(240, 242, 245)')

    return fig

@app.callback(
    Output("corr-fig2", "figure"),
    Input("submit-corr","n_clicks"),
    State('corr-select', 'value')
)
def updatde_corr_fig(n_clicks, value):
    palette_blue = ['#BFBFFF', '#0000FF']   

    if (n_clicks is None) or (value is None):   
        fig = go.Figure() 
    
    elif value == 'corr_genre':
        label = ['장르', '수익', '인기도', '평점']
        df = genre_corr_df
        fig = px.imshow(df.corr(), x=label, y=label, text_auto=True, color_continuous_scale=palette_blue)
        fig.update_traces(hovertemplate='<b>%{x}</b> <> <b>%{y}</b><extra></extra>')
    elif value == 'corr_cast':
        df = cast_corr_df
        label = ['배우', '수익', '인기도', '평점']
        fig = px.imshow(df.corr(), x=label, y=label, text_auto=True, color_continuous_scale=palette_blue)
        fig.update_traces(hovertemplate='<b>%{x}</b> <> <b>%{y}</b><extra></extra>')
    else:
        df = director_corr_df
        label = ['감독', '수익', '인기도', '평점']
        fig = px.imshow(df.corr(), x=label, y=label, text_auto=True, color_continuous_scale=palette_blue)
        fig.update_traces(hovertemplate='<b>%{x}</b> <> <b>%{y}</b><extra></extra>')

    return fig

@app.callback(
    Output('recommender-dropdown','options'),
    Output('recommender-dropdown','placeholder'),
    Output('recommender-dropdown-row','style'),
    Input('recommender-select','value')
)
def update_recommender_value(selected):

    if selected == list(recommender_dict.keys())[0]:
        placeholder = '감독을 선택하세요'
        style = {'display': 'none'}
    if selected == list(recommender_dict.keys())[1]:
        placeholder = '감독을 선택하세요'
        style = {'display': 'block'}
    if selected == list(recommender_dict.keys())[2]:
        placeholder = '배우를 선택하세요'
        style = {'display': 'block'}
    if selected == list(recommender_dict.keys())[3]:
        placeholder = '제목을 선택하세요'
        style = {'display': 'block'}
    return [{'label': i, 'value': i} for i in recommender_dict[selected]], placeholder, style

@app.callback(
    Output("recommender-fig", "figure"),
    Input("recommender-dropdown","value"),
    Input('recommender-select', 'value')
)
def update_recommender_fig(dropdown_value, value):
    
    if value == list(recommender_dict.keys())[0]:

        df = genre_recommender_df
        color = ['red','blue','violet','aqua','orange','gold','green','yellow','crimson','gray','navy','lime','khaki','black','bisque','tan','teal','slateblue','indigo']
        d = []
        for i,c in enumerate(color):
            d.extend([go.Scatter3d(
                            x = df[df['top_genre']==df['top_genre'].value_counts().index[i]]['component 0'],
                            y = df[df['top_genre']==df['top_genre'].value_counts().index[i]]['component 1'],
                            z = df[df['top_genre']==df['top_genre'].value_counts().index[i]]['component 2'],
                            hovertemplate = df[df['top_genre']==df['top_genre'].value_counts().index[i]]['hover'],
                            hovertext = df[df['top_genre']==df['top_genre'].value_counts().index[i]]['movie_name'],
                            name=df['top_genre'].value_counts().index[i],
                            mode='markers',
                            marker=dict(
                                color=c,
                                size=df[df['top_genre']==df['top_genre'].value_counts().index[i]]['revenue'],
                            )
                        )])


        fig = go.Figure(
            data=d
        )

        fig.update_layout(
            autosize=False,
            width=1000,
            height=500,

            margin=go.layout.Margin(
                l=50,
                r=50,
                b=50,
                t=50,
                pad = 4
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            scene=dict(xaxis_visible=False,
                       yaxis_visible=False,
                       zaxis_visible=False),
                       
            plot_bgcolor = 'rgb(240, 242, 245)',
        )

    elif value == list(recommender_dict.keys())[1]:

        if dropdown_value is None:
            fig = go.Figure()
        else:
            director_data = {d:director_recommender_df[director_recommender_df['director'].isin(dropdown_value)].query("director == '%s'" % d) for d in dropdown_value}

            fig = go.Figure()
            for d, director in director_data.items():
                fig.add_trace(go.Scatter3d(
                    x = director['component 0'],
                    y = director['component 1'],
                    z = director['component 2'],
                    name=d,
                    text=director['director'],
                    hovertemplate=director['hover'],
                    mode='markers',
                    marker_size=director['revenue']
                    )
                )

            fig.update_layout(
                autosize=False,
                width=1000,
                height=500,

                margin=go.layout.Margin(
                    l=50,
                    r=50,
                    b=50,   
                    t=50,
                    pad = 4
                ),
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                ),
                scene=dict(xaxis_visible=False,
                        yaxis_visible=False,
                        zaxis_visible=False),
                        
                plot_bgcolor = 'rgb(240, 242, 245)',
            )

    elif value == list(recommender_dict.keys())[2]:

        if dropdown_value is None:
            fig = go.Figure()
        else:
            cast_data = {c:cast_recommender_df[cast_recommender_df['cast'].isin(dropdown_value)].query("cast == '%s'" % c) for c in dropdown_value}

            fig = go.Figure()
            for c, cast in cast_data.items():
                fig.add_trace(go.Scatter3d(
                    x = cast['component 0'],
                    y = cast['component 1'],
                    z = cast['component 2'],
                    name = c,
                    text = cast['cast'],
                    hovertemplate=cast['hover'],
                    mode='markers',
                    marker_size=cast['revenue']
                    )
                )

            fig.update_layout(
                autosize=False,
                width=1000,
                height=500,

                margin=go.layout.Margin(
                    l=50,
                    r=50,
                    b=50,   
                    t=50,
                    pad = 4
                ),
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                ),
                scene=dict(xaxis_visible=False,
                        yaxis_visible=False,
                        zaxis_visible=False),
                        
                plot_bgcolor = 'rgb(240, 242, 245)',
            )

    elif value == list(recommender_dict.keys())[3]:

        if dropdown_value is None:
            fig = go.Figure()
        else:
            title_recommender_df['movie_name'] = title_recommender_df['movie_name'].apply(lambda x:x.replace("'",""))
            title_data = {t:title_recommender_df[title_recommender_df['movie_name'].isin(dropdown_value)].query("movie_name == '%s'" % t) for t in dropdown_value}

            fig = go.Figure()
            for t, title in title_data.items():
                fig.add_trace(go.Scatter3d(
                    x = title['component 0'],
                    y = title['component 1'],
                    z = title['component 2'],
                    name = t,
                    text = title['movie_name'],
                    hovertemplate=title['hover'],
                    mode='markers',
                    marker_size=title['revenue']
                    )
                )

            fig.update_layout(
                autosize=False,
                width=1000,
                height=500,

                margin=go.layout.Margin(
                    l=50,
                    r=50,
                    b=50,   
                    t=50,
                    pad = 4
                ),
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                ),
                scene=dict(xaxis_visible=False,
                        yaxis_visible=False,
                        zaxis_visible=False),
                        
                plot_bgcolor = 'rgb(240, 242, 245)',
            )

    return fig
