# main_css = """
#     <style>
#     .main {
#         max-width: 800px;
#         margin: 0 auto;
#     }
#     .stChatMessage {
#         padding: 1rem;
#         margin-bottom: 1rem;
#     }
#     .stChatInputContainer {
#         padding: 1rem 0;
#     }
#     h1 {
#         font-size: 1.5rem;
#         font-weight: 600;
#         margin-bottom: 2rem;
#     }
#     </style>
# """


main_css = """
<style>
/* DataFrame styling */
.stDataFrame {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stDataFrame thead tr th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white !important;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
    padding: 14px 12px !important;
    border: none !important;
}

.stDataFrame tbody tr:nth-child(even) {
    background-color: #f8f9fa;
}

.stDataFrame tbody tr:hover {
    background-color: #e3f2fd;
    transition: background-color 0.2s ease;
}

.stDataFrame td {
    padding: 12px !important;
    font-size: 0.9rem;
    border-bottom: 1px solid #e0e0e0 !important;
}

/* Download button styling */
.stDownloadButton button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 500;
    transition: transform 0.2s ease;
}

.stDownloadButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: #f0f2f6;
    border-radius: 6px;
    font-weight: 500;
}

/* Code block styling */
.stCodeBlock {
    border-radius: 8px;
    border: 1px solid #e0e0e0;
}
</style>
"""