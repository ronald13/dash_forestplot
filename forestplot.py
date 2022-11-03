import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from const import COLOR_FOREST



class Forest():
    def __init__(self, data):
        self.data = data
        self.font_size = 10
        return

    def set_styling(self, font_family, font_size):
        self.font_family = font_family
        self.font_size = font_size


    def draw_forest_plot(self, df, inputheight=450, annotation_list=[]):




        # data preparation
        df['right_col'] = df['hazard_ratio'].astype(str) + ' ' + df['ci']
        df['num_arm1'] = df['num_arm1'].astype(int)
        df['num_arm2'] = df['num_arm2'].astype(int)

        def create_axis(df_column):
            label = df_column.to_list()[::-1]
            label = list(map(str, label))
            new_label = [label[i] + " " * label[:i].count(label[i]) for i in
                             range(len(label))]
            new_label = list(map(lambda x: x.replace('nan', ''), new_label))
            return new_label

        def bold_category(df):
            type = list(df['type'].unique())
            subtype = list(df['subtype'])
            categoty = []

            for el in subtype:
                if el in type:
                    bold = '<b>' + el + '</b>'
                    categoty.append(bold)
                else:
                    categoty.append(el)
            return categoty[::-1]

        labels_axis_2 = create_axis(df['num_arm1'])
        labels_axis_3 = create_axis(df['num_arm2'])
        labels_axis_4 = create_axis(df['right_col'])
        main_axis = bold_category(df)

        # drawing figure
        fig_forest = go.Figure()

        fig_forest.add_trace(
            go.Scatter(
                x=df['hazard_ratio'][::-1],
                y=main_axis,
                mode="markers",
                marker=dict(color='black', size=self.font_size - 2),
                customdata=df['type'],
                hoverlabel_bgcolor='#ffffff',
                yaxis="y5"
            ))


        fig_forest.add_trace(
            go.Scatter(
                x=df['hazard_ratio'][::-1],
                y=labels_axis_2,
                mode="markers",
                marker=dict(color='red', size=self.font_size - 2),
                customdata=df['type'],
                hovertemplate='<extra></extra>',
                yaxis='y2',
                hoverlabel_bgcolor='#ffffff'
            ))
        fig_forest.add_trace(
            go.Scatter(
                x=df['hazard_ratio'][::-1],
                y=labels_axis_3,
                mode="markers",
                marker=dict(color='red', size=self.font_size - 2),
                customdata=df['type'],
                hovertemplate='<extra></extra>',
                yaxis='y3',
                hoverlabel_bgcolor='#ffffff'
            ))




        fig_forest.add_trace(
            go.Scatter(
                x=df['hazard_ratio'][::-1],
                y=labels_axis_4,
                mode="markers",
                marker=dict(color='black', size=self.font_size - 2),
                customdata=df['type'],
                hovertemplate='%{text}<extra></extra>',
                text='<b>' + df['subtype'][::-1] + ':</b>' +
                     '<br>' + 'Hazard Ratio: ' + df['hazard_ratio'][::-1].astype('str') +
                     '<br>' + '95% CI: ' + df['ci_left'][::-1].astype('str') + ', ' + df['ci_right'][::-1].astype(
                    'str'),

                error_x=dict(
                    type='data',
                    symmetric=False,
                    array=df['ci_diff_right'][::-1],
                    arrayminus=df['ci_diff_left'][::-1]
                ),
                yaxis='y4',
            ))


        fig_forest.update_layout(
            autosize=True,
            margin=dict(l=0, r=0, t=30, pad=10),
            height=inputheight,
            template='plotly_white',
            showlegend=False,
            font=dict(
                # family=brand_font,
                size=self.font_size,
                color="black"
            ),
            yaxis5=dict(
                anchor="free",
                overlaying="y",
                side="left",
                position=0.0
            ),
            yaxis2=dict(
                anchor="free",
                overlaying="y",
                side="left",
                position=0.25
            ),
            yaxis3=dict(
                anchor="free",
                overlaying="y",
                side="left",
                position=0.33
            ),
            yaxis4=dict(
                anchor="free",
                overlaying="y",
                side="right",
                position=1
            ),
        )
        fig_forest.update_yaxes(ticklabelposition='inside', showgrid=False)  # align left
        fig_forest.update_xaxes(range=[-2, 2], tickvals=[0.01, 0.1, 1, 2, 10], type='log',  ticks="inside", tickwidth=0.1, ticklen=5, color='#000', showgrid=False, domain=[0.40, 1], showline=True, linewidth=1, linecolor='#757575')

        annotations = [{"text": "<b>"+annotation_list[0]+"</b>",
                        "position":[0, 1],
                        "color":"#000"},
                       {"text": "<b>"+annotation_list[1] +"             "+annotation_list[2]+"</b>",
                        "position": [0.23, 1],
                        "color": "#000"},
                       {"text": "<b>"+annotation_list[3]+"</b>",
                        "position": [0.68, 1],
                        "color": "#000"},
                       {"text": "<b>"+annotation_list[4]+"</b>",
                        "position": [0.92, 1],
                        "color": "#000"},

                       ]

        for annotation in annotations:
            fig_forest.add_annotation(dict(font=dict(color='#000', size=self.font_size),
                                           x=annotation["position"][0],
                                           y=annotation["position"][1],
                                           align="center",
                                           showarrow=False,
                                           text=annotation["text"],
                                           xanchor='left',
                                           yanchor='bottom',
                                           xref="paper",
                                           yref="paper"
                                           ))

        fig_forest.add_vline(x=1, y0=0, y1=0.96, line_width=1, line_dash="dash", line_color="grey")
        fig_forest.add_hline(x0=-1, x1=1,  y=35,  line_width=2, line_color="#000")

        # draw horizontal line
        y_height = -0.8
        while y_height < 32.5:
            fig_forest.add_hrect(x0=-1, x1=1, y0=y_height, y1=y_height+1.5, line_width=0, fillcolor=list(COLOR_FOREST.values())[1],
                             opacity=0.1)
            y_height = y_height + 3


        return fig_forest

def prepare_forest_data(data_file, addcategoty=False):
    df_forestdata = pd.read_csv(data_file, encoding='UTF-8')

    arm1 = df_forestdata['first'].unique()[0]
    arm2 = df_forestdata['second'].unique()[0]

    row_has_NaN = df_forestdata.isnull().any(axis=1)
    rows_with_NaN = df_forestdata[row_has_NaN]
    categoty_row = rows_with_NaN['type'].to_dict()

    df_forestdata.drop(categoty_row, inplace=True)

    df_forestdata['ci'] = df_forestdata['ci'].apply(lambda x: x.replace(' ', ''))
    df_forestdata['ci_left'] = df_forestdata['ci'].apply(lambda x: x.split(',')[0][1:])
    df_forestdata['ci_right'] = df_forestdata['ci'].apply(lambda x: x.split(',')[1][:-1])

    df_forestdata['ci_left'] = df_forestdata['ci_left'].astype('float')
    df_forestdata['ci_right'] = df_forestdata['ci_right'].astype('float')

    df_forestdata['ci_diff_left'] = df_forestdata['hazard_ratio'] - df_forestdata['ci_left']
    df_forestdata['ci_diff_right'] = df_forestdata['ci_right'] - df_forestdata['hazard_ratio']

    # Subgroups
    df_forestdata['group_subgroup'] = df_forestdata['type'] + ': ' + df_forestdata['subtype']

    # create list with Category rows
    if addcategoty:
        categoty = df_forestdata['type'].unique().tolist()[1:]
        list_cat_row = create_category_row(rows_with_NaN['type'].to_list(), arm1, arm2)
        number_cat_row = rows_with_NaN.index.to_list()  # row numbers in which to insert our Categories

        for row, n_r in zip(list_cat_row, number_cat_row):
            df_forestdata = insert_row(n_r, df_forestdata, row)

    return df_forestdata

def insert_row(row_number, df, row_value):
    start_upper = 0
    end_upper = row_number
    start_lower = row_number
    end_lower = df.shape[0]
    upper_half = [*range(start_upper, end_upper, 1)]
    lower_half = [*range(start_lower, end_lower, 1)]
    lower_half = [x.__add__(1) for x in lower_half]
    index_ = upper_half + lower_half
    df.index = index_
    df.loc[row_number] = row_value
    df = df.sort_index()
    return df
def create_category_row(list, arm1, arm2):
    list_dicts = []
    for el in list:
        temp = {'arm_first': arm1,
                'arm_second': arm2,
                'hazard_ratio': '',
                'ci': '',
                'type': '',
                'subtype': el,
                'ci_left': '',
                'ci_right': '',
                'ci_diff_left': '',
                'ci_diff_right': '',
                'group_subgroup': el}
        list_dicts.append(temp)
    return list_dicts