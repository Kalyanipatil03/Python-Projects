import json, os, re, secrets, sqlite3, hashlib, csv, io
from datetime import date, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

BASE=os.path.dirname(os.path.abspath(__file__)); DB=os.path.join(BASE,'expense_tracker.db')
SESSIONS={}

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.executescript('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT UNIQUE NOT NULL,password_hash TEXT NOT NULL,created_at TEXT NOT NULL); CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,type TEXT NOT NULL CHECK(type IN ('income','expense')),amount REAL NOT NULL CHECK(amount>0),category TEXT NOT NULL,source TEXT,description TEXT,date TEXT NOT NULL,payment_method TEXT,created_at TEXT NOT NULL,FOREIGN KEY(user_id) REFERENCES users(id)); CREATE TABLE IF NOT EXISTS budgets(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,month TEXT NOT NULL,category TEXT NOT NULL,amount REAL NOT NULL CHECK(amount>=0),UNIQUE(user_id,month,category),FOREIGN KEY(user_id) REFERENCES users(id));''')
    return c

def hashpw(p,salt=None):
    salt=salt or secrets.token_hex(16); return salt+'$'+hashlib.pbkdf2_hmac('sha256',p.encode(),bytes.fromhex(salt),120000).hex()
def checkpw(p,h):
    salt,d=h.split('$',1); return secrets.compare_digest(hashpw(p,salt).split('$',1)[1],d)
def clean(s,maxlen=300): return str(s or '').strip()[:maxlen]
def current_user(h):
    sid=h.headers.get('Cookie','').replace('session=','').split(';')[0]
    return SESSIONS.get(sid)
def send(h,code,obj):
    b=json.dumps(obj).encode(); h.send_response(code); h.send_header('Content-Type','application/json'); h.send_header('Content-Length',str(len(b))); h.end_headers(); h.wfile.write(b)
def body(h):
    n=int(h.headers.get('Content-Length','0')); return json.loads(h.rfile.read(n) or '{}')
def require(h):
    u=current_user(h)
    if not u: send(h,401,{'error':'Please log in'}); return None
    return u

def summary(c,uid):
    r=c.execute("SELECT COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END),0) income,COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END),0) expense FROM transactions WHERE user_id=?",(uid,)).fetchone(); return {'income':r['income'],'expense':r['expense'],'balance':r['income']-r['expense']}

class H(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def do_GET(self):
        p=urlparse(self.path).path
        if p=='/': return self.file('index.html','text/html')
        if p.startswith('/static/'): return self.file(p[8:],'text/plain' if p.endswith('.js') else 'text/css')
        u=current_user(self)
        if p=='/api/me': return send(self,200,{'user':dict(u) if u else None})
        if p=='/api/dashboard':
            if not u:return send(self,401,{'error':'Please log in'})
            c=db(); s=summary(c,u['id']); month=date.today().strftime('%Y-%m'); budget=c.execute("SELECT COALESCE(SUM(amount),0) x FROM budgets WHERE user_id=? AND month=?",(u['id'],month)).fetchone()['x']; cats=c.execute("SELECT category,SUM(amount) total FROM transactions WHERE user_id=? AND type='expense' GROUP BY category ORDER BY total DESC",(u['id'],)).fetchall(); recent=c.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY date DESC,id DESC LIMIT 8",(u['id'],)).fetchall(); c.close(); return send(self,200,{'summary':s,'budget':budget,'categories':[dict(x) for x in cats],'recent':[dict(x) for x in recent]})
        if p=='/api/transactions':
            if not u:return send(self,401,{'error':'Please log in'})
            q=parse_qs(urlparse(self.path).query); term=clean(q.get('search',[''])[0],100); typ=q.get('type',['all'])[0]; cat=q.get('category',['all'])[0]
            c=db(); sql='SELECT * FROM transactions WHERE user_id=?'; args=[u['id']]
            if term: sql+=' AND (description LIKE ? OR category LIKE ? OR source LIKE ?)'; args += [f'%{term}%']*3
            if typ in ('income','expense'): sql+=' AND type=?'; args.append(typ)
            if cat!='all': sql+=' AND category=?'; args.append(cat)
            sql+=' ORDER BY date DESC,id DESC'; rows=c.execute(sql,args).fetchall(); c.close(); return send(self,200,{'transactions':[dict(x) for x in rows]})
        if p=='/api/analytics':
            if not u:return send(self,401,{'error':'Please log in'})
            c=db(); cats=c.execute("SELECT category,SUM(amount) total FROM transactions WHERE user_id=? AND type='expense' GROUP BY category ORDER BY total DESC",(u['id'],)).fetchall(); monthly=c.execute("SELECT substr(date,1,7) month,COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END),0) income,COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END),0) expense FROM transactions WHERE user_id=? GROUP BY month ORDER BY month DESC LIMIT 6",(u['id'],)).fetchall(); c.close(); return send(self,200,{'categories':[dict(x) for x in cats],'monthly':[dict(x) for x in reversed(monthly)]})
        if p=='/api/budget':
            if not u:return send(self,401,{'error':'Please log in'})
            month=parse_qs(urlparse(self.path).query).get('month',[date.today().strftime('%Y-%m')])[0]; c=db(); rows=c.execute('SELECT * FROM budgets WHERE user_id=? AND month=? ORDER BY category',(u['id'],month)).fetchall(); spent=c.execute("SELECT category,SUM(amount) total FROM transactions WHERE user_id=? AND type='expense' AND substr(date,1,7)=? GROUP BY category",(u['id'],month)).fetchall(); c.close(); sm={x['category']:x['total'] for x in spent}; return send(self,200,{'month':month,'budgets':[dict(x,spent=sm.get(x['category'],0),remaining=x['amount']-sm.get(x['category'],0)) for x in rows]})
        if p=='/api/export':
            if not u:return send(self,401,{'error':'Please log in'})
            c=db(); rows=c.execute('SELECT date,type,amount,category,source,description,payment_method FROM transactions WHERE user_id=? ORDER BY date DESC,id DESC',(u['id'],)).fetchall(); c.close(); out=io.StringIO(); w=csv.writer(out); w.writerow(['Date','Type','Amount','Category','Source','Description','Payment Method']); [w.writerow([x[k] for k in ('date','type','amount','category','source','description','payment_method')]) for x in rows]; b=out.getvalue().encode(); self.send_response(200); self.send_header('Content-Type','text/csv'); self.send_header('Content-Disposition','attachment; filename="expense_tracker_export.csv"'); self.send_header('Content-Length',str(len(b))); self.end_headers(); return self.wfile.write(b)
        return self.file('index.html','text/html')
    def file(self,name,ctype):
        path=os.path.join(BASE,'static',name) if name!='index.html' else os.path.join(BASE,'templates','index.html')
        try:b=open(path,'rb').read()
        except:return send(self,404,{'error':'Not found'})
        self.send_response(200); self.send_header('Content-Type',ctype); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        p=urlparse(self.path).path; d=body(self)
        if p=='/api/register':
            name=clean(d.get('name'),80); email=clean(d.get('email'),120).lower(); pw=str(d.get('password',''))
            if not name or not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$',email) or len(pw)<6:return send(self,400,{'error':'Enter a valid name, email and password (6+ characters).'})
            c=db()
            try:c.execute('INSERT INTO users(name,email,password_hash,created_at) VALUES(?,?,?,?)',(name,email,hashpw(pw),datetime.now().isoformat())); c.commit(); uid=c.execute('SELECT id FROM users WHERE email=?',(email,)).fetchone()['id'];
            except sqlite3.IntegrityError:c.close(); return send(self,409,{'error':'An account with this email already exists.'})
            c.close(); sid=secrets.token_urlsafe(32); SESSIONS[sid]={'id':uid,'name':name,'email':email}; self.send_response(200); self.send_header('Set-Cookie',f'session={sid}; HttpOnly; SameSite=Lax; Path=/'); self.send_header('Content-Type','application/json'); b=json.dumps({'ok':True}).encode(); self.send_header('Content-Length',str(len(b))); self.end_headers(); return self.wfile.write(b)
        if p=='/api/login':
            email=clean(d.get('email'),120).lower(); pw=str(d.get('password','')); c=db(); u=c.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone(); c.close()
            if not u or not checkpw(pw,u['password_hash']):return send(self,401,{'error':'Invalid email or password.'})
            sid=secrets.token_urlsafe(32); SESSIONS[sid]={'id':u['id'],'name':u['name'],'email':u['email']}; self.send_response(200); self.send_header('Set-Cookie',f'session={sid}; HttpOnly; SameSite=Lax; Path=/'); self.send_header('Content-Type','application/json'); b=b'{}'; self.send_header('Content-Length','2'); self.end_headers(); self.wfile.write(b); return
        if p=='/api/logout':
            sid=self.headers.get('Cookie','').replace('session=','').split(';')[0]; SESSIONS.pop(sid,None); self.send_response(200); self.send_header('Set-Cookie','session=; Max-Age=0; Path=/'); self.send_header('Content-Length','2'); self.end_headers(); return self.wfile.write(b'{}')
        u=require(self)
        if not u:return
        c=db()
        if p=='/api/transactions':
            typ=d.get('type'); amt=float(d.get('amount',0)); cat=clean(d.get('category'),60); dt=clean(d.get('date'),20) or str(date.today());
            if typ not in ('income','expense') or amt<=0 or not cat:return c.close() or send(self,400,{'error':'Type, positive amount and category are required.'})
            c.execute('INSERT INTO transactions(user_id,type,amount,category,source,description,date,payment_method,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(u['id'],typ,amt,cat,clean(d.get('source'),100),clean(d.get('description'),300),dt,clean(d.get('payment_method'),60),datetime.now().isoformat())); c.commit(); c.close(); return send(self,200,{'ok':True})
        if p.startswith('/api/transactions/'):
            tid=int(p.rsplit('/',1)[1]);
            c.execute('DELETE FROM transactions WHERE id=? AND user_id=?',(tid,u['id'])); c.commit(); c.close(); return send(self,200,{'ok':True})
        if p=='/api/budget':
            month=clean(d.get('month'),7); cat=clean(d.get('category'),60); amt=float(d.get('amount',0));
            if not re.match(r'^\d{4}-\d{2}$',month) or not cat or amt<0:c.close(); return send(self,400,{'error':'Invalid budget data.'})
            c.execute('INSERT INTO budgets(user_id,month,category,amount) VALUES(?,?,?,?) ON CONFLICT(user_id,month,category) DO UPDATE SET amount=excluded.amount',(u['id'],month,cat,amt)); c.commit(); c.close(); return send(self,200,{'ok':True})
        c.close(); return send(self,404,{'error':'Not found'})

if __name__=='__main__':
    db().close(); port=8000; print(f'Expense Tracker Pro running at http://127.0.0.1:{port}'); ThreadingHTTPServer(('127.0.0.1',port),H).serve_forever()
