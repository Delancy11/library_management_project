from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField, DateField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from datetime import datetime, timedelta
import os

from config import Config
from models import db, Admin, User, Category, Book, BorrowRecord

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 用户加载器
@login_manager.user_loader
def load_user(user_id):
    try:
        user_id = int(user_id)
        # 首先在管理员表中查找
        admin = Admin.query.get(user_id)
        if admin:
            return admin

        # 如果管理员表中没有，则在普通用户表中查找
        user = User.query.get(user_id)
        return user
    except (ValueError, TypeError):
        return None

# 表单类定义
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember = BooleanField('记住我')

class UserRegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('邮箱', validators=[DataRequired(), Email()])
    full_name = StringField('姓名', validators=[DataRequired(), Length(max=100)])
    phone = StringField('手机号', validators=[Length(max=20)])
    address = TextAreaField('地址')
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])

class BookForm(FlaskForm):
    title = StringField('书名', validators=[DataRequired(), Length(max=200)])
    author = StringField('作者', validators=[DataRequired(), Length(max=100)])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(max=20)])
    publisher = StringField('出版社', validators=[Length(max=100)])
    publication_date = DateField('出版日期')
    quantity = IntegerField('数量', validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField('描述')
    category_id = SelectField('分类', coerce=int, validators=[DataRequired()])

class CategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('描述')

# 初始化数据库
def initialize_database():
    with app.app_context():
        try:
            db.create_all()
            print("数据库表创建成功")

            # 创建默认管理员账户（ID为1）
            if not Admin.query.filter_by(username='admin').first():
                admin = Admin(username='admin', email='admin@library.com')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("创建默认管理员: admin/admin123")

            return True
        except Exception as e:
            print(f"数据库初始化失败: {e}")
            return False

# 路由定义
@app.route('/')
def index():
    return render_template('index.html')

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # 尝试以管理员身份登录
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin, remember=form.remember.data)
            flash('管理员登录成功！', 'success')
            return redirect(url_for('admin_dashboard'))

        # 尝试以用户身份登录
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=form.remember.data)
            flash('登录成功！', 'success')
            return redirect(url_for('user_dashboard'))

        flash('用户名或密码错误！', 'danger')

    return render_template('login.html', form=form)

# 用户注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('用户名已存在！', 'danger')
            return render_template('register.html', form=form)

        if User.query.filter_by(email=form.email.data).first():
            flash('邮箱已存在！', 'danger')
            return render_template('register.html', form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('注册成功！请登录。', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# 登出路由
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已安全退出登录！', 'info')
    return redirect(url_for('index'))

# 管理员仪表板
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        abort(403)

    stats = {
        'total_users': User.query.count(),
        'total_books': Book.query.count(),
        'total_categories': Category.query.count(),
        'active_borrows': BorrowRecord.query.filter_by(status='borrowed').count(),
        'overdue_records': BorrowRecord.query.filter(BorrowRecord.status == 'borrowed').filter(BorrowRecord.due_date < datetime.utcnow()).count()
    }

    return render_template('admin/dashboard.html', stats=stats)

# 用户仪表板
@app.route('/user/dashboard')
@login_required
def user_dashboard():
    # 如果是管理员但访问了用户仪表板，重定向到管理员仪表板
    if current_user.__class__.__name__ == 'Admin':
        flash('您是管理员，已跳转到管理员页面', 'info')
        return redirect(url_for('admin_dashboard'))

    user_borrows = BorrowRecord.query.filter_by(user_id=current_user.id, status='borrowed').limit(5).all()
    overdue_records = BorrowRecord.query.filter_by(user_id=current_user.id, status='borrowed').filter(BorrowRecord.due_date < datetime.utcnow()).count()
    total_borrows = BorrowRecord.query.filter_by(user_id=current_user.id, status='borrowed').count()

    return render_template('user/dashboard.html',
                         user_borrows=user_borrows,
                         overdue_count=overdue_records,
                         total_borrows=total_borrows)

# 管理员路由 - 用户管理
@app.route('/admin/users')
@login_required
def admin_users():
    if not isinstance(current_user, Admin):
        abort(403)

    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    if not isinstance(current_user, Admin):
        abort(403)

    user = User.query.get_or_404(user_id)
    # 删除用户相关的借阅记录
    BorrowRecord.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功！', 'success')
    return redirect(url_for('admin_users'))

# 图书管理路由
@app.route('/admin/books')
@login_required
def admin_books():
    if not isinstance(current_user, Admin):
        abort(403)

    # 获取搜索和筛选参数
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    category_id = request.args.get('category', '', type=int)
    status = request.args.get('status', '')  # all, available, borrowed
    sort_by = request.args.get('sort', 'title')  # title, author, added_date

    # 构建基础查询
    query = Book.query

    # 应用搜索筛选
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Book.title.like(search_term),
                Book.author.like(search_term),
                Book.isbn.like(search_term),
                Book.description.like(search_term)
            )
        )

    # 应用分类筛选
    if category_id:
        query = query.filter(Book.category_id == category_id)

    # 应用状态筛选
    if status == 'available':
        query = query.filter(Book.available_copies > 0)
    elif status == 'borrowed':
        query = query.filter(Book.total_copies > Book.available_copies)

    # 应用排序
    if sort_by == 'title':
        query = query.order_by(Book.title)
    elif sort_by == 'author':
        query = query.order_by(Book.author)
    elif sort_by == 'added_date':
        query = query.order_by(Book.id.desc())
    elif sort_by == 'isbn':
        query = query.order_by(Book.isbn)
    else:
        query = query.order_by(Book.title)

    # 执行分页查询
    books = query.paginate(
        page=page, per_page=10, error_out=False
    )

    # 获取所有分类用于筛选器
    categories = Category.query.order_by(Category.name).all()

    return render_template('admin/books.html',
                         books=books,
                         categories=categories,
                         current_search=search,
                         current_category=category_id,
                         current_status=status,
                         current_sort=sort_by)

@app.route('/admin/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if not isinstance(current_user, Admin):
        abort(403)

    form = BookForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        if Book.query.filter_by(isbn=form.isbn.data).first():
            flash('ISBN已存在！', 'danger')
            return render_template('admin/add_book.html', form=form)

        book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            publisher=form.publisher.data,
            publication_date=form.publication_date.data,
            quantity=form.quantity.data,
            available_quantity=form.quantity.data,
            description=form.description.data,
            category_id=form.category_id.data
        )
        db.session.add(book)
        db.session.commit()
        flash('图书添加成功！', 'success')
        return redirect(url_for('admin_books'))

    return render_template('admin/add_book.html', form=form)

@app.route('/admin/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if not isinstance(current_user, Admin):
        abort(403)

    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        form.populate_obj(book)
        book.available_quantity = book.quantity - (book.quantity - book.available_quantity)
        db.session.commit()
        flash('图书更新成功！', 'success')
        return redirect(url_for('admin_books'))

    return render_template('admin/edit_book.html', form=form, book=book)

@app.route('/admin/books/delete/<int:book_id>')
@login_required
def delete_book(book_id):
    if not isinstance(current_user, Admin):
        abort(403)

    book = Book.query.get_or_404(book_id)
    # 删除相关的借阅记录
    BorrowRecord.query.filter_by(book_id=book_id).delete()
    db.session.delete(book)
    db.session.commit()
    flash('图书删除成功！', 'success')
    return redirect(url_for('admin_books'))

# 分类管理路由
@app.route('/admin/categories')
@login_required
def admin_categories():
    if not isinstance(current_user, Admin):
        abort(403)

    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if not isinstance(current_user, Admin):
        abort(403)

    form = CategoryForm()
    if form.validate_on_submit():
        if Category.query.filter_by(name=form.name.data).first():
            flash('分类名称已存在！', 'danger')
            return render_template('admin/add_category.html', form=form)

        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        flash('分类添加成功！', 'success')
        return redirect(url_for('admin_categories'))

    return render_template('admin/add_category.html', form=form)

@app.route('/admin/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if not isinstance(current_user, Admin):
        abort(403)

    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        form.populate_obj(category)
        db.session.commit()
        flash('分类更新成功！', 'success')
        return redirect(url_for('admin_categories'))

    return render_template('admin/edit_category.html', form=form, category=category)

@app.route('/admin/categories/delete/<int:category_id>')
@login_required
def delete_category(category_id):
    if not isinstance(current_user, Admin):
        abort(403)

    category = Category.query.get_or_404(category_id)
    # 检查是否有关联的图书
    if category.books:
        book_count = len(category.books)
        flash(f'该分类下还有 {book_count} 本图书，无法删除！请先删除或移动这些图书。', 'danger')
        return redirect(url_for('admin_categories'))

    db.session.delete(category)
    db.session.commit()
    flash('分类删除成功！', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/force-delete/<int:category_id>')
@login_required
def force_delete_category(category_id):
    if not isinstance(current_user, Admin):
        abort(403)

    category = Category.query.get_or_404(category_id)

    if category.books:
        # 找一个默认分类（通常是第一个分类）
        default_category = Category.query.filter(Category.id != category_id).first()
        if not default_category:
            flash('没有其他分类可以接收这些图书，请先创建一个新分类！', 'danger')
            return redirect(url_for('admin_categories'))

        # 将所有关联的图书移动到默认分类
        book_count = len(category.books)
        for book in category.books:
            book.category_id = default_category.id

        flash(f'已将 {book_count} 本图书移动到分类 "{default_category.name}"。', 'warning')

    # 删除分类
    db.session.delete(category)
    db.session.commit()
    flash('分类删除成功！', 'success')
    return redirect(url_for('admin_categories'))

# 借阅记录管理路由
@app.route('/admin/records')
@login_required
def admin_borrow_records():
    if not isinstance(current_user, Admin):
        abort(403)

    page = request.args.get('page', 1, type=int)
    records = BorrowRecord.query.order_by(BorrowRecord.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('admin/borrow_records.html', records=records, datetime=datetime)

# 用户图书浏览
@app.route('/books')
@login_required
def browse_books():
    category_id = request.args.get('category_id', type=int)
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = Book.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Book.title.contains(search) | Book.author.contains(search))

    books = query.filter(Book.available_quantity > 0).paginate(
        page=page, per_page=10, error_out=False
    )
    categories = Category.query.all()

    return render_template('user/browse_books.html',
                         books=books,
                         categories=categories,
                         selected_category=category_id,
                         search=search)

# 用户借阅图书
@app.route('/books/borrow/<int:book_id>')
@login_required
def borrow_book(book_id):
    if isinstance(current_user, Admin):
        abort(403)

    book = Book.query.get_or_404(book_id)

    if book.available_quantity <= 0:
        flash('该图书暂无库存！', 'danger')
        return redirect(url_for('browse_books'))

    # 检查用户是否已经借阅了这本书且还未归还
    existing_record = BorrowRecord.query.filter_by(
        user_id=current_user.id,
        book_id=book_id,
        status='borrowed'
    ).first()

    if existing_record:
        flash('您已经借阅了这本书！', 'warning')
        return redirect(url_for('browse_books'))

    # 创建借阅记录
    borrow_record = BorrowRecord(
        user_id=current_user.id,
        book_id=book_id,
        due_date=datetime.utcnow() + timedelta(days=30)  # 30天归还期限
    )

    book.available_quantity -= 1
    db.session.add(borrow_record)
    db.session.commit()

    flash('图书借阅成功！请按时归还。', 'success')
    return redirect(url_for('user_dashboard'))

# 用户归还图书
@app.route('/books/return/<int:record_id>')
@login_required
def return_book(record_id):
    if isinstance(current_user, Admin):
        abort(403)

    record = BorrowRecord.query.get_or_404(record_id)

    if record.user_id != current_user.id:
        abort(403)

    if record.status == 'returned':
        flash('该图书已经归还！', 'warning')
        return redirect(url_for('user_dashboard'))

    # 更新借阅记录
    record.return_date = datetime.utcnow()
    record.status = 'returned'

    # 增加图书库存
    record.book.available_quantity += 1
    db.session.commit()

    flash('图书归还成功！', 'success')
    return redirect(url_for('user_dashboard'))

# 用户借阅历史
@app.route('/user/borrow-history')
@login_required
def borrow_history():
    if isinstance(current_user, Admin):
        abort(403)

    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')

    # 构建查询
    query = BorrowRecord.query.filter_by(user_id=current_user.id)

    # 搜索条件
    if search:
        query = query.join(Book).filter(
            Book.title.contains(search) | Book.author.contains(search)
        )

    # 状态筛选
    if status == 'borrowed':
        query = query.filter_by(status='borrowed')
    elif status == 'returned':
        query = query.filter_by(status='returned')
    elif status == 'overdue':
        query = query.filter(
            BorrowRecord.status == 'borrowed',
            BorrowRecord.due_date < datetime.utcnow()
        )

    # 分页查询
    records = query.order_by(BorrowRecord.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('user/borrow_history.html',
                         records=records,
                         search=search,
                         status=status)

# 用户个人资料
@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if isinstance(current_user, Admin):
        abort(403)

    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')

        if request.form.get('password'):
            current_user.set_password(request.form.get('password'))

        db.session.commit()
        flash('个人资料更新成功！', 'success')
        return redirect(url_for('user_profile'))

    return render_template('user/profile.html')

if __name__ == '__main__':
    app.run(debug=True)