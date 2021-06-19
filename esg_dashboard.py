import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from esg.models import SmithWilson, HullWhite, DynamicNelsonSiegel

def main():
    with st.sidebar:
        st.title("경제적 시나리오 생성기")
        menu = st.selectbox('메뉴', ['무위험금리', '유동성프리미엄', '기업부도율', '개인부도율', '물가상승률', '조기상환율', 'TVOG시나리오', '내부모형시나리오'])

    
    if menu == "무위험금리":
        st.title(menu)
        
        st.subheader('**Ⅰ. 데이터 및 설정**')

        input_type = st.radio('입력방법', ['자동수집', '수기입력'])

        if input_type == '수기입력':
            data = st.file_uploader('파일업로드')
        elif input_type == '자동수집':
            base_date = st.date_input('기준일자')
            agency = st.selectbox('기관명', ['금융투자협회', '민평평균', '나이스피앤아이', '한국자산평가', 'KIS채권평가', '에프엔자산평가'])
            maturity = st.multiselect('만기', ['3월','6월','9월','1년','1년6월','2년','2년6월','3년','4년','5년','7년','10년','15년','20년','30년','50년'], default=['1년', '2년', '3년', '5년', '10년', '20년'])
            st.button('수집')

        ltfr = st.number_input('장기선도금리', min_value=0., max_value=1., value=0.052, format='%.3f', step=0.001)
        cp = st.number_input('수렴시점(년)', min_value=20, max_value=100, value=60, step=1)
        tol = st.number_input('수렴오차', min_value=0.0001, max_value=0.001+1e-15, value=0.0001, step=0.0001, format='%.4f')

        if st.button('모델링'):
            #TODO: 연산 구현
            pass

        st.subheader('**Ⅱ. 산출결과**')
        compounding = st.selectbox('복리계산', ['연복리', '연속복리'])
        if st.selectbox('현물/선도', ['현물', '선도']) == '선도':
            st.slider('선도만기(월)', min_value=0, max_value=12, value=1, step=1)

        
        # 데이터 입력
        data = np.array([
            [0.25, 0.0041],
            [0.5, 0.0055],
            [0.75, 0.0061],
            [1, 0.0068],
            [2, 0.0090],
            [3, 0.0099],
            [5, 0.0140],
            [7, 0.0155],
            [10, 0.0174],
            [20, 0.0184]
        ])

        X_train = data[:, 0]
        y_train = data[:, 1]
        ltfr, terminal = 0.052, 60

        # SW 모델 생성 및 α 학습
        sw = SmithWilson(np.log(1+ltfr), terminal)
        sw.train(X_train, y_train)
        t = np.arange(0, 120+1e-8, 1/12)
        spot = sw.spot(t)

        fig = make_subplots(rows=1, cols=1, shared_xaxes=False)
        fig.add_trace(go.Scatter(
            x=t, y=spot,
            line=dict(width=2, color='#009473'),
            name='현물(연복리)',
        ))

        fig.update_xaxes(
            title=dict(text='<b>만기(년)</b>', font_color='#323232', font_size=18, standoff=0),
            tickfont=dict(size=15, family='Malgun Gothic', color='#323232'),
            tickformat='.0f',
            tickangle=0,
            dtick=20,
            showline=True, linecolor='#323232', linewidth=2,
            zeroline=False, #zerolinewidth=2, zerolinecolor='black',
            showgrid=False, #gridcolor='black', gridwidth=1,
        )

        fig.update_yaxes(
            title=dict(text=r'<b>금리</b>', font_color='#323232', font_size=18, standoff=0),
            tickfont=dict(size=15, family='Malgun Gothic', color='#323232'),
            tickformat='.1f',
            dtick=0.5,
            showline=False, #linecolor='#323232', linewidth=2,
            zeroline=False, #zerolinewidth=2, zerolinecolor='black',
            showgrid=False, #gridcolor='black', gridwidth=1,
        )

        fig.update_layout(
            title=dict(text='<b>금리기간구조</b>', font_size=20, font_color='#323232', xanchor='center', yanchor='top', x=0.475, y=0.97),
            margin=dict(l=40, r=40, b=40, t=60),
            width=697,
            height=400,
            font_family='Malgun Gothic',
            font_color='black',
            plot_bgcolor='#fcfcfc',
            paper_bgcolor='#fcfcfc',
            legend_title='<b>구분</b>',
            legend_title_font_size=17,
            legend_font_size=15,
            # hovermode='x unified',
            showlegend=True,
            hoverlabel_align='left',
        )

        st.plotly_chart(fig)

      
        

        if st.button('다운로드'):
            #TODO: 결과 다운로드 구현
            pass


if __name__ == '__main__':
    main()