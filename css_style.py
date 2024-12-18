# css_style.py


def get_css_styles(text_color="#000000"):
    return f"""
    <style>
    /* 入力フィールドのスタイル */
    .stTextInput > div > div > input {{
        min-height: 40px !important;
        width: 40px !important;
        padding: 0 !important;
        text-align: center !important;
        font-size: 20px !important;
        margin: 1px !important;
        color: {text_color} !important;
    }}
    
    /* 固定数字のスタイル */
    .fixed-number {{
        background-color: #f0f0f0;
        min-height: 40px;
        width: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        margin: 1px;
        border: 1px solid #ddd;
        border-radius: 4px;
        color: #000000;
    }}

    /* 3x3ブロックの区切り線用のスペース */
    .block-divider {{
        margin: 3px 0;
    }}

    .vertical-divider {{
        margin: 0 3px;
    }}

    /* コントロールパネル */
    .control-panel {{
        margin-bottom: 1rem;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
    }}

    /* コンテナの余白調整 */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }}

    /* Streamlitのデフォルトの余白を調整 */
    .stTextInput > div {{
        padding: 0 !important;
    }}
    </style>
    """
