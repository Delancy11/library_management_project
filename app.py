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

    # 获取搜索和分页参数
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    status = request.args.get('status', '')  # all, active, inactive
    sort_by = request.args.get('sort', 'created_date')  # created_date, username, email

    # 构建基础查询
    query = User.query

    # 搜索功能
    if search:
        search_filter = f'%{search}%'
        query = query.filter(
            db.or_(
                User.username.like(search_filter),
                User.email.like(search_filter),
                User.full_name.like(search_filter),
                User.phone.like(search_filter)
            )
        )

    # 状态筛选
    if status == 'active':
        # 可以根据实际业务逻辑定义活跃用户
        query = query.filter(User.is_active == True)
    elif status == 'inactive':
        query = query.filter(User.is_active == False)

    # 排序
    if sort_by == 'username':
        query = query.order_by(User.username)
    elif sort_by == 'email':
        query = query.order_by(User.email)
    elif sort_by == 'created_date':
        query = query.order_by(User.created_at.asc())
    else:
        query = query.order_by(User.id)

    # 分页查询
    users = query.paginate(
        page=page, per_page=10, error_out=False
    )

    # 保存搜索参数用于模板显示
    return render_template('admin/users.html',
                         users=users,
                         search=search,
                         status=status,
                         sort_by=sort_by)

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
    sort_by = request.args.get('sort', 'id')  # id, title, author, added_date

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
    if category_id and category_id != '':
        try:
            category_id = int(category_id)
            query = query.filter(Book.category_id == category_id)
        except (ValueError, TypeError):
            pass

    # 应用状态筛选
    if status == 'available':
        query = query.filter(Book.available_quantity > 0)
    elif status == 'borrowed':
        query = query.filter(Book.quantity > Book.available_quantity)

    # 应用排序
    if sort_by == 'id':
        query = query.order_by(Book.id)
    elif sort_by == 'title':
        query = query.order_by(Book.title)
    elif sort_by == 'author':
        query = query.order_by(Book.author)
    elif sort_by == 'added_date':
        query = query.order_by(Book.id.desc())
    elif sort_by == 'isbn':
        query = query.order_by(Book.isbn)
    else:
        query = query.order_by(Book.id)

    # 执行分页查询
    books = query.paginate(
        page=page, per_page=10, error_out=False
    )

    # 获取所有分类用于筛选器（排除Ubuntu和Ubuntu-22.04分类）
    categories = Category.query.filter(Category.name.notin_(['Ubuntu', 'Ubuntu-22.04'])).order_by(Category.name).all()

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
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter(Category.name.notin_(['Ubuntu', 'Ubuntu-22.04'])).all()]

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
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter(Category.name.notin_(['Ubuntu', 'Ubuntu-22.04'])).all()]

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

    # 获取搜索参数
    search = request.args.get('search', '').strip()

    # 构建基础查询
    query = Category.query

    # 搜索功能
    if search:
        search_filter = f'%{search}%'
        query = query.filter(
            db.or_(
                Category.name.like(search_filter),
                Category.description.like(search_filter)
            )
        )

    # 执行查询
    categories = query.all()

    # 过滤后的分类（用于搜索结果显示）
    filtered_categories = categories if search else None

    return render_template('admin/categories.html',
                         categories=Category.query.all(),  # 所有分类用于统计
                         filtered_categories=filtered_categories if search else None,
                         search=search)

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

    # 获取搜索和筛选参数
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    status = request.args.get('status', '')
    search_type = request.args.get('search_type', 'all')
    days = request.args.get('days', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    sort_by = request.args.get('sort_by', 'borrow_date')
    due_filter = request.args.get('due_filter', '')  # 新增：到期日期筛选参数

    # 构建基础查询
    query = BorrowRecord.query

    # 应用搜索筛选
    if search:
        search_term = f"%{search}%"
        if search_type == 'book':
            query = query.join(Book).filter(Book.title.like(search_term))
        elif search_type == 'user':
            query = query.join(User).filter(
                db.or_(
                    User.username.like(search_term),
                    User.full_name.like(search_term),
                    User.email.like(search_term)
                )
            )
        elif search_type == 'isbn':
            query = query.join(Book).filter(Book.isbn.like(search_term))
        elif search_type == 'id':
            try:
                record_id = int(search)
                query = query.filter(BorrowRecord.id == record_id)
            except ValueError:
                pass
        else:  # all
            query = query.join(Book, User).filter(
                db.or_(
                    Book.title.like(search_term),
                    Book.author.like(search_term),
                    Book.isbn.like(search_term),
                    User.username.like(search_term),
                    User.full_name.like(search_term),
                    User.email.like(search_term)
                )
            )

    # 应用状态筛选
    if status == 'borrowed':
        query = query.filter(BorrowRecord.status == 'borrowed')
    elif status == 'returned':
        query = query.filter(BorrowRecord.status == 'returned')
    elif status == 'overdue':
        query = query.filter(
            BorrowRecord.status == 'borrowed',
            BorrowRecord.due_date < datetime.utcnow()
        )

    # 应用时间筛选
    if days:
        try:
            days_num = int(days)
            start_date = datetime.utcnow() - timedelta(days=days_num)
            query = query.filter(BorrowRecord.borrow_date >= start_date)
        except ValueError:
            pass
    elif date_from:
        try:
            start_date = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(BorrowRecord.borrow_date >= start_date)
        except ValueError:
            pass

    if date_to:
        try:
            end_date = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(BorrowRecord.borrow_date < end_date)
        except ValueError:
            pass

    # 应用到期日期筛选
    if due_filter == 'today':
        # 今日到期：从今天开始到明天结束
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        query = query.filter(
            BorrowRecord.status == 'borrowed',
            BorrowRecord.due_date >= today_start,
            BorrowRecord.due_date < today_end
        )
    elif due_filter == 'this_week':
        # 本周到期：从本周一开始到本周日结束
        now = datetime.utcnow()
        days_since_monday = now.weekday()
        week_start = (now - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = week_start + timedelta(days=7)
        query = query.filter(
            BorrowRecord.status == 'borrowed',
            BorrowRecord.due_date >= week_start,
            BorrowRecord.due_date < week_end
        )

    # 应用排序
    if sort_by == 'borrow_date':
        query = query.order_by(BorrowRecord.borrow_date.desc())
    elif sort_by == 'due_date':
        query = query.order_by(BorrowRecord.due_date.desc())
    elif sort_by == 'return_date':
        query = query.order_by(BorrowRecord.return_date.desc())
    elif sort_by == 'user_name':
        query = query.join(User).order_by(User.full_name)
    else:
        query = query.order_by(BorrowRecord.borrow_date.desc())

    # 执行分页查询
    records = query.paginate(page=page, per_page=10, error_out=False)

    # 计算统计数据
    all_records = records.items

    # 统计逾期记录（只计算当前页）
    overdue_count = 0
    for record in all_records:
        if record.is_overdue():
            overdue_count += 1

    # 统计当前借阅数量
    borrowed_count = 0
    returned_count = 0
    for record in all_records:
        if record.status == 'borrowed':
            borrowed_count += 1
        elif record.status == 'returned':
            returned_count += 1

    return render_template('admin/borrow_records.html',
                         records=records,
                         datetime=datetime,
                         overdue_count=overdue_count,
                         borrowed_count=borrowed_count,
                         returned_count=returned_count)

@app.route('/admin/records/return/<int:record_id>', methods=['POST'])
@login_required
def admin_return_book(record_id):
    """管理员标记图书归还"""
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': '权限不足'}), 403

    try:
        # 获取借阅记录
        record = BorrowRecord.query.get_or_404(record_id)

        # 检查是否已经归还
        if record.return_date is not None:
            return jsonify({
                'success': False,
                'message': f'该图书已于{record.return_date.strftime("%Y-%m-%d %H:%M")}归还'
            }), 400

        # 获取图书并更新可借数量
        book = record.book
        if book.available_quantity < book.quantity:
            book.available_quantity += 1

        # 更新借阅记录
        record.return_date = datetime.utcnow()
        record.status = 'returned'

        # 提交到数据库
        db.session.commit()

        # 记录操作日志
        app.logger.info(f'管理员 {current_user.username} 标记归还：用户 {record.user.username} 归还图书 {book.title}')

        return jsonify({
            'success': True,
            'message': f'《{book.title}》已成功标记为归还',
            'return_date': record.return_date.strftime('%Y-%m-%d %H:%M'),
            'new_status': 'returned',
            'book_available': book.available_quantity
        })

    except Exception as e:
        db.session.rollback()
        app.logger.error(f'标记归还失败: {str(e)}')
        return jsonify({'success': False, 'message': '操作失败，请重试'}), 500

@app.route('/admin/records/batch-return', methods=['POST'])
@login_required
def admin_batch_return_books():
    """管理员批量标记图书归还"""
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': '权限不足'}), 403

    try:
        data = request.get_json()
        record_ids = data.get('record_ids', [])

        if not record_ids:
            return jsonify({'success': False, 'message': '请选择要归还的记录'}), 400

        success_count = 0
        error_messages = []

        for record_id in record_ids:
            try:
                record = BorrowRecord.query.get(record_id)
                if not record:
                    error_messages.append(f'记录ID {record_id} 不存在')
                    continue

                if record.return_date is not None:
                    error_messages.append(f'《{record.book.title}》已归还，跳过')
                    continue

                # 更新图书数量
                if record.book.available_quantity < record.book.quantity:
                    record.book.available_quantity += 1

                # 更新借阅记录
                record.return_date = datetime.utcnow()
                record.status = 'returned'

                success_count += 1

            except Exception as e:
                error_messages.append(f'处理记录ID {record_id} 时出错: {str(e)}')

        # 提交所有更改
        db.session.commit()

        # 记录批量操作日志
        app.logger.info(f'管理员 {current_user.username} 批量归还：成功 {success_count} 条记录')

        return jsonify({
            'success': True,
            'message': f'成功标记 {success_count} 条记录为归还',
            'success_count': success_count,
            'errors': error_messages
        })

    except Exception as e:
        db.session.rollback()
        app.logger.error(f'批量归还失败: {str(e)}')
        return jsonify({'success': False, 'message': '批量操作失败，请重试'}), 500

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
        search_filter = f'%{search}%'
        query = query.join(Book).filter(
            db.or_(
                Book.title.like(search_filter),
                Book.author.like(search_filter),
                Book.isbn.like(search_filter)
            )
        )

    # 状态筛选
    if status == 'borrowed':
        query = query.filter(BorrowRecord.status == 'borrowed')
    elif status == 'returned':
        query = query.filter(BorrowRecord.status == 'returned')
    elif status == 'overdue':
        # 查询状态为借阅中且已逾期的记录
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