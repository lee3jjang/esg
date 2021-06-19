from altair.vegalite.v4.schema.core import FontWeight
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from esg.models import SmithWilson, HullWhite, DynamicNelsonSiegel

def main():
    with st.sidebar:
        st.title("경제적 시나리오 생성기")
        menu = st.selectbox('메뉴', ['무위험금리', '유동성프리미엄', '기업부도율', '개인부도율', '물가상승률', '조기상환율', 'TVOG시나리오', '내부모형시나리오'], index=6)

    
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
        compounding_kr = st.selectbox('복리계산', ['연복리', '연속복리'])
        compounding = {'연복리': 'annually', '연속복리': 'continuously'}.get(compounding_kr)
        # if st.selectbox('현물/선도', ['현물', '선도']) == '선도':
        fwd_mat = st.slider('선도만기(월)', min_value=0, max_value=12, value=1, step=1)

        
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

        # SW 모델 생성 및 α 학습
        sw = SmithWilson(np.log(1+ltfr), cp, tol)
        sw.train(X_train, y_train)
        t = np.arange(0, 100+1e-8, 1/12)
        spot = sw.spot(t, compounding=compounding)
        forward = sw.forward(t, x=fwd_mat, compounding=compounding)

        # 시각화
        fig = make_subplots(rows=1, cols=1, shared_xaxes=False)

        ## 현물(연복리)
        fig.add_trace(go.Scatter(
            x=X_train, y=y_train if compounding=="annually" else np.log(1+y_train),
            marker=dict(color='black', symbol='x', size=10),
            name='관측값',
            mode='markers',
            showlegend=False,
        ))
        
        fig.add_trace(go.Scatter(
            x=t, y=spot,
            line=dict(width=2, color='#009473'),
            name=f'현물({compounding_kr})',
        ))

        ## 1개월선도(연복리)
        fig.add_trace(go.Scatter(
            x=t, y=forward,
            line=dict(width=2, color='#dd4124'),
            name=f'{str(fwd_mat)+"개월" if fwd_mat != 0 else "순간":}선도({compounding_kr})',
        ))

        fig.add_hline(y=ltfr if compounding=='annually' else np.log(1+ltfr), line=dict(width=2, color='black', dash='dash'))

        fig.add_annotation(
            x=100, y=ltfr if compounding=='annually' else np.log(1+ltfr),
            text="<b>LTFR</b>",
            showarrow=False,
            yshift=1,
            font_color='white',
            font_size=15,
            # bordercolor="black",
            borderwidth=2,
            borderpad=4,
            bgcolor="#dd4124",
            opacity=1,
        )

        fig.update_xaxes(
            title=dict(text='<b>만기(년)</b>', font_color='#323232', font_size=18, standoff=0),
            tickfont=dict(size=15, family='Malgun Gothic', color='#323232'),
            tickformat='.0f',
            tickangle=0,
            dtick=20,
            showline=True, linecolor='#323232', linewidth=2,
            zeroline=False, #zerolinewidth=2, zerolinecolor='black',
            showgrid=False, #gridcolor='black', gridwidth=1,
            range=[0, 100],
        )

        fig.update_yaxes(
            title=dict(text=r'<b>금리</b>', font_color='#323232', font_size=18, standoff=0),
            tickfont=dict(size=15, family='Malgun Gothic', color='#323232'),
            tickformat=',.1%',
            dtick=0.01,
            showline=True, #linecolor='#323232', linewidth=2,
            zeroline=False, #zerolinewidth=2, zerolinecolor='black',
            showgrid=False, #gridcolor='black', gridwidth=1,
            # range=[0, 100],
        )

        fig.update_layout(
            title=dict(text='<b>금리기간구조                      2020.12.31</b>', font_size=20, font_color='#323232', xanchor='left', yanchor='top', x=0.43, y=0.97),
            margin=dict(l=40, r=40, b=40, t=60),
            width=697,
            height=400,
            font_family='Malgun Gothic',
            font_color='black',
            plot_bgcolor='#fcfcfc',
            paper_bgcolor='#fcfcfc',
            # legend_title='<b>구분</b>',
            legend_title_font_size=17,
            legend_font_size=15,
            # hovermode='x unified',
            showlegend=True,
            legend=dict(x=0.7, y=0.2),
            hoverlabel_align='left',
        )

        st.plotly_chart(fig)
      
    
        if st.button('다운로드'):
            #TODO: 결과 다운로드 구현
            pass

    elif menu == "TVOG시나리오":
        st.title(menu)
        
        st.subheader('**Ⅱ. 산출결과**')
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
        ltfr, cp = 0.052, 60
        # alpha = [0.0001, 0.02082]
        alpha = [0.0001, 0.001]
        sigma = [0.00457, 0.00490, 0.00651, 0.00631, 0.00465, 0.00562, 0.00405]
        sw = SmithWilson(np.log(1+ltfr), cp)
        sw.train(X_train, y_train)
        hw = HullWhite(sw, alpha, sigma)
        
        t = np.arange(0, 100+1e-8, 1/12)
        alpha_t = np.array([hw.alpha(x) for x in t])
        sigma_t = np.array([hw.sigma(x) for x in t])
        N = 1000
        all_scen = hw.generate_scenario(t=100, n=N).T
        scen_mean = all_scen.mean(axis=0)
        scen_vol = all_scen.std(axis=0)
        fwd = hw.curve.forward(t)

        all_ts = np.array([t for _ in range(N)])
        all_ts_with_nan = [np.concatenate((ts, [np.nan])) for ts in all_ts]
        all_scen_with_nan = [np.concatenate((s, [np.nan])) for s in all_scen]
        ts = np.concatenate(all_ts_with_nan)
        scen = np.concatenate(all_scen_with_nan)

        # 시각화(1)
        fig = make_subplots(rows=1, cols=1, shared_xaxes=False)

        ## 모수
        fig.add_trace(go.Scatter(
            x=t, y=alpha_t,
            line=dict(width=2, color='#009473'),
            name='α(t)'
        ))
        fig.add_trace(go.Scatter(
            x=t, y=sigma_t,
            line=dict(width=2, color='#dd4124'),
            name='σ(t)'
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
            range=[0, 100],
        )

        fig.update_yaxes(
            # title=dict(text=r'<b>금리</b>', font_color='#323232', font_size=18, standoff=0),
            tickfont=dict(size=15, family='Malgun Gothic', color='#323232'),
            tickformat=',.2f',
            dtick=0.005,
            showline=False, #linecolor='#323232', linewidth=2,
            zeroline=False, #zerolinewidth=2, zerolinecolor='black',
            showgrid=False, #gridcolor='black', gridwidth=1,
            # range=[0, 100],
        )

        fig.update_layout(
            title=dict(text='<b>    모수                           2020.12.31</b>', font_size=20, font_color='#323232', xanchor='left', yanchor='top', x=0.43, y=0.97),
            margin=dict(l=40, r=40, b=40, t=60),
            width=697,
            height=400,
            font_family='Malgun Gothic',
            font_color='black',
            plot_bgcolor='#fcfcfc',
            paper_bgcolor='#fcfcfc',
            # legend_title='<b>구분</b>',
            legend_title_font_size=17,
            legend_font_size=15,
            # hovermode='x unified',
            showlegend=True,
            legend=dict(x=0.85, y=0.95),
            hoverlabel_align='left',
        )

        st.plotly_chart(fig)

        # 시각화(2)
        fig2 = make_subplots(rows=1, cols=1, shared_xaxes=False)

        fig2.add_trace(go.Scattergl(
            x=ts, y=scen,
            mode='lines', opacity=0.025,
            line={'color': 'darkblue'},
            name='r(t)',
        ))

        fig2.add_trace(go.Scatter(
            x=t, y=scen_mean,
            line=dict(width=2, color='#009473'),
            name='E[r(t)]',
        ))

        fig2.add_trace(go.Scatter(
            x=t, y=scen_mean+1.96*scen_vol,
            line=dict(width=2, color='#009473', dash='dash'),
            showlegend=False,
        ))
        fig2.add_trace(go.Scatter(
            x=t, y=scen_mean-1.96*scen_vol,
            line=dict(width=2, color='#009473', dash='dash'),
            showlegend=False,
        ))

        fig2.add_trace(go.Scatter(
            x=t, y=fwd,
            line=dict(width=2, color='black'),
            name='f(t)'
        ))

        fig2.update_xaxes(
            title=dict(text='<b>만기(년)</b>', font_color='#323232', font_size=18, standoff=0),
            tickfont=dict(size=15, family='Malgun Gothic', color='#323232'),
            tickformat='.0f',
            tickangle=0,
            dtick=20,
            showline=True, linecolor='#323232', linewidth=2,
            zeroline=False, #zerolinewidth=2, zerolinecolor='black',
            showgrid=False, #gridcolor='black', gridwidth=1,
            range=[0, 100],
        )

        fig2.update_yaxes(
            # title=dict(text=r'<b>금리</b>', font_color='#323232', font_size=18, standoff=0),
            tickfont=dict(size=15, family='Malgun Gothic', color='#323232'),
            tickformat=',.1%',
            dtick=0.05,
            showline=False, #linecolor='#323232', linewidth=2,
            zeroline=False, #zerolinewidth=2, zerolinecolor='black',
            showgrid=False, #gridcolor='black', gridwidth=1,
            # range=[0, 100],
        )

        fig2.update_layout(
            title=dict(text='<b>TVOG 시나리오                2020.12.31</b>', font_size=20, font_color='#323232', xanchor='left', yanchor='top', x=0.43, y=0.97),
            margin=dict(l=40, r=40, b=40, t=60),
            width=697,
            height=400,
            font_family='Malgun Gothic',
            font_color='black',
            plot_bgcolor='#fcfcfc',
            paper_bgcolor='#fcfcfc',
            # legend_title='<b>구분</b>',
            legend_title_font_size=17,
            legend_font_size=15,
            # hovermode='x unified',
            showlegend=False,
            legend=dict(x=0.85, y=0.7),
            hoverlabel_align='left',
        )

        st.plotly_chart(fig2)

if __name__ == '__main__':
    main()