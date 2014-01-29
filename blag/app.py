from flask import Flask, g, url_for, request, flash, redirect, session, json, render_template, current_app
from .default_settings import Settings
from flask.ext.flatpages import FlatPages, pygments_style_defs
from datetime import datetime
from feedgenerator import DefaultFeed


pages = FlatPages()


def create_app(conf_obj=Settings, conf_file='/etc/blag.cfg'):
    app = Flask(__name__)
    app.config.from_object(conf_obj)
    app.config.from_pyfile(conf_file, silent=True)

    pages.init_app(app)

    articles_ = [p for p in pages if 'published' in p.meta]
    articles = sorted(articles_, reverse=True,
                        key=lambda p: p.meta['published'])

    @app.route('/.htaccess')
    def htaccess_one():
        return '''<Files rss.xml>
<IfModule mod_headers.c>
Header set Content-Type application/rss+xml
</IfModule>
</Files>''', 200, {'Content-Type': 'application/octet-stream'}

    @app.route('/pygments.css')
    def pygments_css():
        return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}

    @app.route('/rss.xml')
    def rss():
        c = current_app.config
        f = DefaultFeed(title=c['BLAG_TITLE'], link=url_for('index', _external=True),
            author_name=c['BLAG_AUTHOR'], feed_url=url_for('rss', _external=True),
            description=c['BLAG_DESCRIPTION'], language='en')
        latest = sorted(articles, reverse=True,
                        key=lambda p: p.meta['published'])
        for late in latest[:3]:
            d = datetime.strptime(late.meta['published'], '%Y-%m-%d %H:%M:%S %Z')
            f.add_item(late.meta['title'], url_for('page', path=late.path, _external=True), late.html, unique_id=url_for('page', path=late.path, _external=True), pubdate=d)
        return f.writeString('UTF-8'), 200, {'Content-Type': 'application/rss+xml'}

    @app.route('/favicon.ico')
    def favicon():
        return redirect(url_for('static', filename='favicon.ico'))

    @app.route('/')
    def index():
        latest = sorted(articles, reverse=True,
                        key=lambda p: p.meta['published'])
        for article in latest:
            article.year = article.meta['published'].split('-')[0]
            d = datetime.strptime(article.meta['published'], '%Y-%m-%d %H:%M:%S %Z')
            nice_date = d.strftime('%A, %d %B %Y')
            article.nice_date = nice_date
        return render_template('posts.html', articles=latest[:3], other_articles=latest[3:])

    @app.route('/post/<path:path>.html')
    def page(path):
        page = pages.get(path)
        d = datetime.strptime(page.meta['published'], '%Y-%m-%d %H:%M:%S %Z')
        nice_date = d.strftime('%A, %d %B %Y')
        page.nice_date = nice_date
        nr = prev = next_ = None
        try:
            nr = articles.index(page)
            prev = articles[nr - 1] if nr > 0 else None
            next_ = articles[nr + 1] if (nr+1) < len(articles) else None
        except:
            pass
        template = page.meta.get('template', 'post.html')
        return render_template(template, article=page, nr=nr, next_=next_, prev=prev)

    return app
