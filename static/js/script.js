// 图书管理系统 JavaScript

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    initTooltips();

    // 初始化确认对话框
    initConfirmDialogs();

    // 初始化搜索功能
    initSearchFunctionality();

    // 初始化表单验证
    initFormValidation();

    // 初始化自动刷新
    initAutoRefresh();

    // 初始化键盘快捷键
    initKeyboardShortcuts();
});

// 初始化Bootstrap工具提示
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// 初始化确认对话框
function initConfirmDialogs() {
    // 为所有删除按钮添加确认
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.dataset.confirm || '确定要执行此操作吗？';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
}

// 初始化搜索功能
function initSearchFunctionality() {
    // 实时搜索
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        let searchTimeout;

        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const searchTerm = this.value.trim();
            const searchContainer = this.closest('.search-container');

            if (searchTerm.length < 2) {
                hideSearchResults(searchContainer);
                return;
            }

            searchTimeout = setTimeout(() => {
                performSearch(searchTerm, searchContainer);
            }, 300);
        });

        // 点击其他地方关闭搜索结果
        document.addEventListener('click', function(e) {
            if (!input.contains(e.target) && !searchContainer.contains(e.target)) {
                hideSearchResults(searchContainer);
            }
        });
    });
}

// 执行搜索
function performSearch(searchTerm, container) {
    // 这里可以调用后端API进行搜索
    // 为了演示，我们显示一个加载状态

    const resultsContainer = container.querySelector('.search-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = '<div class="search-loading"><div class="loading"></div> 搜索中...</div>';
        resultsContainer.style.display = 'block';

        // 模拟API调用
        setTimeout(() => {
            resultsContainer.innerHTML = `
                <div class="search-no-results">
                    <i class="bi bi-search"></i>
                    <p>没有找到相关结果</p>
                </div>
            `;
        }, 1000);
    }
}

// 隐藏搜索结果
function hideSearchResults(container) {
    const resultsContainer = container.querySelector('.search-results');
    if (resultsContainer) {
        resultsContainer.style.display = 'none';
    }
}

// 初始化表单验证
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // 密码强度检测
    const passwordInputs = document.querySelectorAll('input[type="password"][id*="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            checkPasswordStrength(this);
        });
    });
}

// 检查密码强度
function checkPasswordStrength(passwordInput) {
    const password = passwordInput.value;
    const strengthIndicator = passwordInput.parentElement.querySelector('.password-strength');

    if (!strengthIndicator) return;

    let strength = 0;

    if (password.length >= 8) strength++;
    if (password.match(/[a-z]+/)) strength++;
    if (password.match(/[A-Z]+/)) strength++;
    if (password.match(/[0-9]+/)) strength++;
    if (password.match(/[$@#&!]+/)) strength++;

    const strengthLevels = ['', '弱', '一般', '中等', '强', '很强'];
    const strengthColors = ['', 'danger', 'warning', 'info', 'primary', 'success'];

    strengthIndicator.className = `password-strength badge bg-${strengthColors[strength]}`;
    strengthIndicator.textContent = strengthLevels[strength];
}

// 初始化自动刷新
function initAutoRefresh() {
    // 自动刷新借阅状态
    const autoRefreshElements = document.querySelectorAll('[data-auto-refresh]');
    autoRefreshElements.forEach(element => {
        const interval = element.dataset.autoRefresh || 30000; // 默认30秒
        setInterval(() => {
            refreshElementData(element);
        }, interval);
    });
}

// 刷新元素数据
function refreshElementData(element) {
    const url = element.dataset.refreshUrl;
    if (url) {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                updateElementContent(element, data);
            })
            .catch(error => {
                console.error('刷新数据失败:', error);
            });
    }
}

// 更新元素内容
function updateElementContent(element, data) {
    // 根据数据更新元素内容
    if (data.html) {
        element.innerHTML = data.html;
    } else if (data.text) {
        element.textContent = data.text;
    } else if (data.value !== undefined) {
        element.value = data.value;
    }
}

// 初始化键盘快捷键
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl+K 打开搜索
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('.search-input');
            if (searchInput) {
                searchInput.focus();
            }
        }

        // ESC 关闭模态框
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                bootstrap.Modal.getInstance(modal).hide();
            });
        }
    });
}

// 通用工具函数

// 显示成功消息
function showSuccessMessage(message) {
    showAlert(message, 'success');
}

// 显示错误消息
function showErrorMessage(message) {
    showAlert(message, 'danger');
}

// 显示警告消息
function showWarningMessage(message) {
    showAlert(message, 'warning');
}

// 显示信息消息
function showInfoMessage(message) {
    showAlert(message, 'info');
}

// 显示警告框
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    alertContainer.insertBefore(alert, alertContainer.firstChild);

    // 5秒后自动关闭
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 计算天数差
function daysBetween(date1, date2) {
    const firstDate = new Date(date1);
    const secondDate = new Date(date2);
    const timeDiff = Math.abs(secondDate.getTime() - firstDate.getTime());
    return Math.ceil(timeDiff / (1000 * 3600 * 24));
}

// 复制到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showSuccessMessage('已复制到剪贴板');
    }).catch(() => {
        showErrorMessage('复制失败，请手动复制');
    });
}

// 导出数据
function exportData(format, data) {
    let content, filename, type;

    switch(format) {
        case 'csv':
            content = convertToCSV(data);
            filename = 'export.csv';
            type = 'text/csv';
            break;
        case 'json':
            content = JSON.stringify(data, null, 2);
            filename = 'export.json';
            type = 'application/json';
            break;
        default:
            showErrorMessage('不支持的导出格式');
            return;
    }

    downloadFile(content, filename, type);
}

// 转换为CSV格式
function convertToCSV(data) {
    if (!data || !data.length) return '';

    const headers = Object.keys(data[0]);
    const csvHeaders = headers.join(',');
    const csvData = data.map(row => headers.map(header => row[header]).join(','));

    return [csvHeaders, ...csvData].join('\n');
}

// 下载文件
function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// 图片预览
function previewImage(input, previewElement) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewElement.src = e.target.result;
            previewElement.style.display = 'block';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// 表格排序
function sortTable(table, column, direction) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const aValue = a.children[column].textContent.trim();
        const bValue = b.children[column].textContent.trim();

        if (direction === 'asc') {
            return aValue.localeCompare(bValue);
        } else {
            return bValue.localeCompare(aValue);
        }
    });

    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
}

// 打印功能
function printElement(elementId) {
    const element = document.getElementById(elementId);
    const printWindow = window.open('', '_blank');

    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
            <head>
                <title>打印预览</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    .no-print { display: none; }
                    @media print { .no-print { display: none; } }
                </style>
            </head>
            <body>
                ${element.innerHTML}
            </body>
        </html>
    `);

    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 懒加载图片
function initLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    lazyImages.forEach(img => imageObserver.observe(img));
}

// 页面可见性变化处理
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // 页面隐藏时停止自动刷新
        console.log('页面隐藏，停止自动刷新');
    } else {
        // 页面显示时恢复自动刷新
        console.log('页面显示，恢复自动刷新');
    }
});

// 网络状态监听
window.addEventListener('online', function() {
    showSuccessMessage('网络连接已恢复');
});

window.addEventListener('offline', function() {
    showWarningMessage('网络连接已断开');
});

console.log('图书管理系统 JavaScript 已加载完成');