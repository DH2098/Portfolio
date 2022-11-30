import os
from dash import html, dcc
import dash_bootstrap_components as dbc
import feffery_antd_components as fac

from app import app
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app_name = os.getenv("DASH_APP_PATH", "/movie-recommender")

table = pd.read_csv("data/table.csv")

genre_ani_df = pd.read_csv("data/genre_ani_df.csv")

genres_df = pd.read_csv("data/genres_df.csv").set_index('genre')

titles_df = pd.read_csv('data/titles_df.csv')
cast_title_df = pd.read_csv("data/cast_title_df.csv")
director_title_df = pd.read_csv("data/director_title_df.csv")

keyword_df = pd.read_csv("data/keyword_df.csv")

keyword_top20_df = pd.read_csv("data/keyword_top20_df.csv")
keyword_top20_df['sum'] = keyword_top20_df['sum'].apply(lambda x:int(x))

def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

title_dict = []
for i in range(len(titles_df)):
    title_dict.append({'label' : sorted(titles_df.title)[i], 'value' : sorted(titles_df.title)[i]})

cast_dict = []
for i in range(len(cast_title_df)):
    cast_dict.append({'label' : sorted(cast_title_df.cast)[i], 'value' : sorted(cast_title_df.cast)[i]})

director_dict = []
for i in range(len(director_title_df.index)):
    director_dict.append({'label' : sorted(director_title_df.director)[i], 'value' : sorted(director_title_df.director)[i]})

def Navbar():
    navbar = fac.AntdSider(
        [
            html.Div(
                fac.AntdMenu(
                    menuItems=[
                        {
                            'component': 'Item',
                            'props': {
                                'key': 'main-page',
                                'title': '메인 페이지',
                                'icon': 'antd-home',
                                'href': f'{app_name}/main'                            
                            },
                        },
                        {
                            'component': 'SubMenu',
                            'props': {
                                'key': 'eda',
                                'title': 'EDA',
                                'icon': 'antd-bar-chart'
                            },
                            'children' : [
                                {
                                    'component' : 'SubMenu',
                                    'props' : {
                                        'key': 'trend',
                                        'title': '추세 분석',
                                        'icon': 'antd-menu'
                                    },
                                    'children' : [
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'trend-year',
                                                'title': '1년 단위 추세',
                                                'href': f'{app_name}/trend'
                                            }
                                        },
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'trend-decade',
                                                'title': '10년 단위 추세',
                                                'href': f'{app_name}/trend'
                                            }
                                        },
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'trend-animation',
                                                'title': '애니메이션',
                                                'href': f'{app_name}/trend'
                                            }
                                        },
                                    ]
                                },
                                {
                                    'component' : 'SubMenu',
                                    'props' : {
                                        'key': 'revenue',
                                        'title': '흥행 분석',
                                        'icon': 'antd-menu'
                                    },
                                    'children' : [
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'revenue-genre',
                                                'title': '장르별',
                                                'href': f'{app_name}/revenue'
                                            }
                                        },
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'revenue-title',
                                                'title': '영화별',
                                                'href': f'{app_name}/revenue'
                                            }
                                        },
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'revenue-director',
                                                'title': '감독별',
                                                'href': f'{app_name}/revenue#director_revenue_fig'
                                            }
                                        },
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'revenue-cast',
                                                'title': '배우별',
                                                'href': f'{app_name}/revenue'
                                            }
                                        },
                                    ]
                                },
                                {
                                    'component' : 'SubMenu',
                                    'props' : {
                                        'key': 'keyword',
                                        'title': '키워드 분석',
                                        'icon': 'antd-menu'
                                    },
                                    'children' : [
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'keyword-revenue',
                                                'title': '수익별 키워드',
                                                'href': f'{app_name}/keyword'
                                            }
                                        },
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'keyword-vote-average',
                                                'title': '장르별 키워드',
                                                'href': f'{app_name}/keyword'
                                            }
                                        },
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'keyword-popularity',
                                                'title': '인기도별 키워드',
                                                'href': f'{app_name}/keyword'
                                            }
                                        },
                                    ]
                                },
                                {
                                    'component' : 'SubMenu',
                                    'props' : {
                                        'key': 'corr',
                                        'title': '상관관계 분석',
                                        'icon': 'antd-menu'
                                    },
                                    'children' : [
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'corr-revenue',
                                                'title': '장르 - 흥행지표',
                                                'href': f'{app_name}/corr'
                                            }
                                        },
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'corr-genre',
                                                'title': '배우 - 흥행지표',
                                                'href': f'{app_name}/corr'
                                            }
                                        },
                                        {
                                            'component' : 'Item',
                                            'props' : {
                                                'key': 'corr-popularity',
                                                'title': '감독 - 흥행지표',
                                                'href': f'{app_name}/corr'
                                            }
                                        },
                                    ]
                                },
                            ]
                        },
                        {
                            'component': 'SubMenu',
                            'props': {
                                'key': 'recommender',
                                'title': '영화 추천',
                                'icon': 'antd-dot-chart'
                            },
                            'children' : [
                                {
                                    'component' : 'Item',
                                    'props' : {
                                        'key': 'genre-recommend',
                                        'title': '장르별 영화 추천',
                                        'href': f'{app_name}/recommender'
                                    }
                                },
                                {
                                    'component' : 'Item',
                                    'props' : {
                                        'key': 'director-recommend',
                                        'title': '감독별 영화 추천',
                                        'href': f'{app_name}/recommender'
                                    }
                                },
                                {
                                    'component' : 'Item',
                                    'props' : {
                                        'key': 'cast-recommend',
                                        'title': '배우별 영화 추천',
                                        'href': f'{app_name}/recommender'
                                    }
                                },
                                {
                                    'component' : 'Item',
                                    'props' : {
                                        'key': 'title-recommend',
                                        'title': '제목별 영화 추천',
                                        'href': f'{app_name}/recommender'
                                    }
                                }
                            ]
                        },
                        {
                            'component': 'Item',
                            'props': {
                                'key': 'github',
                                'title': 'GitHub',
                                'icon': 'antd-github',
                                'href': 'https://github.com/DH2098'
                            },
                        },
                    ],
                    mode='inline'
                ),
                style={
                    'height': '100%',
                    'overflowY': 'scroll' 
                }
            )
        ],
        collapsible=True,
        style={
            'backgroundColor': 'rgb(240, 242, 245)'
        }
    )
    return navbar

trend_animation_fig = px.bar(
    genre_ani_df, 
    x='genres', 
    y='count', 
    color='genres',
    animation_frame='year', 
    animation_group='genres', 
    range_y=[0,130]
)
trend_animation_fig.update_traces(hovertemplate=None)
trend_animation_fig.update_layout(
    hovermode='x unified',
    plot_bgcolor = 'rgb(240, 242, 245)'
    )

genre_revenue_fig = go.Figure()
genre_revenue_fig.add_trace(go.Bar(
    x = genres_df.index,
    y = genres_df['revenue'].sort_values(ascending=False),
    hovertemplate="<b>장르 : %{x}</b>" +
    "<br>흥행 수익 : %{y}<extra></extra>",
    marker_color='peachpuff'
))
genre_revenue_fig.update_layout(
    hoverlabel=dict(
        bgcolor='white',
        font_size=16,
    ),
    plot_bgcolor = 'rgb(240, 242, 245)'
)

keywords_fig = px.treemap(keyword_df[keyword_df.idx=='수익별'], 
                 path = [px.Constant('키워드'), 'idx', '키워드'], 
                 values = 'count',
                 color = 'count',
                 color_continuous_scale = 'Blues',
                 )
keywords_fig.update_traces(hovertemplate='<b>%{label}</b> <br> Count : %{value}')                 
keywords_fig.update_layout(margin = dict(t=25, l=25, r=25, b=25))

keywords_top20_fig = px.bar(
    x = keyword_top20_df['sum'],
    y = keyword_top20_df['index'],
    orientation = 'h',
    title='Top 20'
)

keywords_top20_fig.update_traces(hovertemplate=None)
keywords_top20_fig.update_layout(
    yaxis=dict(autorange="reversed"),
    xaxis_title=None,
    yaxis_title=None,
    hovermode='y'
)

main_layout = html.Div(
    html.Div(
        [
        html.H1('변동현의 프로젝트입니다.',
        style={
                'textAlign': 'center',
                'color': '#000000',
                'margin' : '5rem 5rem',
                }
        ),

        dbc.Table.from_dataframe(table, striped=True, bordered=True, hover=True),

        html.Div([

            html.Img(src=app.get_asset_url('flask-logo.png'), style={'height':'300px', 'width':'300px', 'textAlign': 'center'}),
            html.Img(src=app.get_asset_url('plotly-dash-logo.png'), style={'height':'300px', 'width':'300px', 'textAlign': 'center'}),

            html.P('kaggle의 TMDB 5000 Movie Dataset을 기반으로 영화 추천 시스템을 구현했습니다.', className='mt-5')
            ], 
            style={'textAlign': 'center',
                    'margin-top' : '2rem',}
        ),
        html.Div(
            [
                dbc.Button('파일 다운로드', color="secondary", external_link=False, id="btn-download", n_clicks=0),
                dcc.Download(id="download-df")
            ],
            style={'textAlign': 'center', 'margin-bottom': '5rem'}
        )
        ]
    ),
    id="page-content"
)

trend_layout = html.Div(
    [ 
        fac.AntdAnchor(
            linkDict= [
                {'title': '1년 단위', 'href': '#trend-year-graph'},
                {'title': '10년 단위', 'href': '#trend-decade-graph'},
                {'title': '애니메이션', 'href': '#trend-animation'},
            ],
            align='right',
            targetOffset=100,
            offsetTop=50
        ),
        html.Div(
            [
                html.H4("1년 단위 장르 추세"),
                dcc.Loading(dcc.Graph(id="trend-year-graph"), type="graph"),
                html.P("연도: "),
                dcc.RangeSlider(
                    id = "trend-year-RS",
                    min = 1916,
                    max = 2017,
                    step = None,
                    marks = {
                        1916: "1916년", 
                        1920: "1920년",
                        1930: "1930년",
                        1940: "1940년",
                        1950: "1950년",
                        1960: "1960년",
                        1970: "1970년",
                        1980: "1980년",
                        1990: "1990년",
                        2000: "2000년",
                        2010: "2010년",                
                        2017: "2017년"},
                    value = [1916, 2017],
                    allowCross=False
                )
            ],
            className='mt-5 mr-7'
        ),
        html.Div(
            [
                html.H4("10년 단위 장르 추세"),
                dcc.Loading(dcc.Graph(id="trend-decade-graph"), type="graph"),
                html.P("연도: "),
                dcc.RangeSlider(
                    id = "trend-decade-RS",
                    min = 1910,
                    max = 2010,
                    step = None,
                    marks = {
                        1910: "1910년", 
                        1920: "1920년",
                        1930: "1930년",
                        1940: "1940년",
                        1950: "1950년",
                        1960: "1960년",
                        1970: "1970년",
                        1980: "1980년",
                        1990: "1990년",
                        2000: "2000년",
                        2010: "2010년"},
                    value = [1910, 2010],
                    allowCross=False
                )
            ],
            className='mt-5 mr-7'
        ),
        html.Div(
            [
                html.H4("추세 애니메이션"),
                dcc.Loading(dcc.Graph(figure=trend_animation_fig, id="trend-animation"), type="cube"),
            ],
            className='mt-5 mr-7'    
        )   
    ],
    className='pd-2 mb-15'
)

revenue_layout = html.Div(
    [
        fac.AntdAnchor(
            linkDict= [
                {'title': '장르별 흥행', 'href': '#genre_revenue_fig'},
                {'title': '제목별 흥행', 'href': '#title_revenue_fig'},
                {'title': '배우별 흥행', 'href': '#cast_revenue_fig'},
                {'title': '감독별 흥행', 'href': '#director_revenue_fig'},
            ],
            align='right',
            targetOffset=100,
            offsetTop=50
        ),
        html.Div(
            [
                html.H4("장르별 흥행 수익"),
                dcc.Loading(dcc.Graph(figure=genre_revenue_fig), type="graph"),
            ],
            className='mt-5 mr-7',
            id='genre_revenue_fig'
        ),
        html.Div(
            [
                html.H4("제목별 흥행 수익"),
                dbc.Row(
                    [
                        dbc.Label("영화 제목 :", width="auto"),
                        dbc.Col(dcc.Dropdown(
                            title_dict,
                            id="title-select",
                            placeholder='제목을 선택하세요.',
                            multi=True
                            ),
                            className= 'custom-dropdown',
                        ),
                        dbc.Col(dbc.Button("검색", id='submit-title', color="secondary"), width="auto", className='mt-2')
                     ]
                ),
                dcc.Loading(dcc.Graph(id='title_revenue_fig'), type="graph"),
            ],
            className='mt-5 mr-7',
            id='title_revenue_fig'    
        ),
        html.Div(
            [
                html.H4("배우별 흥행 수익"),
                html.P('10편 이상 촬영한 배우 기준', className='text-gray'),
                dbc.Row(
                    [
                        dbc.Label("배우 이름 :", width="auto"),
                        dbc.Col(dcc.Dropdown(
                            cast_dict,
                            id="cast-select",
                            placeholder='배우를 선택하세요.',
                            multi=True
                            ),
                            className= 'custom-dropdown',
                        ),
                        dbc.Col(dbc.Button("검색", id='submit-cast', color="secondary"), width="auto", className='mt-2')
                     ]
                ),
                dcc.Loading(dcc.Graph(id='cast_revenue_fig'), type="graph"),
            ],
            className='mt-5 mr-7',
            id='cast_revenue_fig'    
        ),
        html.Div(
            [
                html.H4("감독별 흥행"),
                html.P('5편 이상 촬영한 감독 기준', className='text-gray'),
                dbc.Row(
                    [
                        dbc.Label("감독 이름 :", width="auto"),
                        dbc.Col(dcc.Dropdown(
                            director_dict,
                            id="director-select",
                            placeholder='감독을 선택하세요.',
                            multi=True
                            ),
                            className= 'custom-dropdown',
                        ),
                        dbc.Col(dbc.Button("검색", id='submit-director', color="secondary"), width="auto", className='mt-2')
                     ]
                ),
                dcc.Loading(dcc.Graph(id='director_revenue_fig'), type="graph"),
            ],
            className='mt-5 mr-7',
            id='director_revenue_fig'
        )
    ],
    className='pd-2 mb-15'
)

keyword_layout = html.Div(
    [
        html.H2("키워드 분석"),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Label("키워드 :", width="auto"),
                        dbc.Col(dcc.Dropdown(
                            ['수익별', '평점별', '인기도별'],
                            id='keyword-select',
                            placeholder='키워드를 선택하세요',
                            ),
                            width='20px'
                        ),
                        dbc.Col(dbc.Button("검색", id='submit-keyword', color="secondary"), width="auto", className='mt-2')
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(figure=keywords_top20_fig, className='mg-0')], className='mw-30'),
                        dbc.Col([dcc.Graph(id='keyword-fig')], className='mw-70')
                    ]
                )
            ]
        )
    ],
    className='pd-2 mb-15'
)

corr_dict = [
    {'label':'장르 - 흥행 지표', 'value':'corr_genre'},
    {'label':'배우 - 흥행 지표', 'value':'corr_cast'},
    {'label':'감독 - 흥행 지표', 'value':'corr_director'}
]

corr_layout = html.Div(
    [
        html.H2("상관관계 분석"),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Label("키워드 :", width="auto"),
                        dbc.Col(dcc.Dropdown(
                            corr_dict,
                            id='corr-select',
                            placeholder='주제를 선택하세요',
                            ),
                            width='20px'
                        ),
                        dbc.Col(dbc.Button("검색", id='submit-corr', color="secondary"), width="auto", className='mt-2')
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(id='corr-fig1', className='mg-0')], className='mw-50'),
                        dbc.Col([dcc.Graph(id='corr-fig2')], className='mw-50')
                    ]
                )
            ]
        )
    ],
    className='pd-2 mb-15'
)

recommender_dict = {
    '장르별 영화 추천' : [],
    '감독별 영화 추천' : sorted([i for i in director_title_df.director]),
    '배우별 영화 추천' : sorted([i for i in cast_title_df.cast]),
    '제목별 영화 추천' : sorted([i for i in titles_df.title])
    }

recommender_layout = html.Div(
    [
        html.H2("영화 추천"),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Label("주제 :", width="auto"),
                        dbc.Col(dcc.Dropdown(
                            list(recommender_dict.keys()),
                            list(recommender_dict.keys())[0],
                            placeholder='주제를 선택하세요',
                            id='recommender-select',
                            searchable=False,
                            clearable=False
                            ),
                            width='20px'
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Dropdown(
                            id="recommender-dropdown",
                            multi=True
                            ),
                            id='recommender-dropdown-row',
                            className= 'custom-dropdown',
                            width='20px'
                        )
                     ]
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(id='recommender-fig', className='mg-0')]),
                    ]
                )
            ]
        )
    ],
    className='pd-2 mb-15'
)
