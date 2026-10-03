# add_activity_css.py - Ku dar CSS-ka activity list

with open("public/index.html", "r") as f:
    content = f.read()

css = '''
.activity-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    border-radius: 10px;
    transition: 0.2s;
    margin-bottom: 5px;
}
.activity-item:hover { background: var(--card-hover); }
.activity-info div:first-child { font-size: 14px; font-weight: 600; margin-bottom: 2px; }
.activity-badge {
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}
.panel-header a {
    color: var(--primary);
    font-size: 13px;
    text-decoration: none;
    font-weight: 600;
}
'''

# Ku dar ka hor </style>
style_end = content.find("</style>")
if style_end != -1:
    content = content[:style_end] + css + content[style_end:]
    print("✅ CSS-ka activity waa lagu daray!")

with open("public/index.html", "w") as f:
    f.write(content)
