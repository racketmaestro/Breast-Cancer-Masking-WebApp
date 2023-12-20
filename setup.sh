mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
\n\
[theme]\n\
base = 'light'\n\
primaryColor = '#96ead7'\n\
secondaryBackgroundColor = '#b8dbd3'\n\
font = 'sans serif'\n\
\n\
" > ~/.streamlit/config.toml
