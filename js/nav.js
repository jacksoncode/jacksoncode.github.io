document.addEventListener('DOMContentLoaded', function() {
    var navContainer = document.getElementById('nav-container');
    
    if (!navContainer) {
        console.error('导航容器未找到');
        return;
    }

    fetch('data/nav.json')
        .then(function(response) {
            if (!response.ok) {
                throw new Error('加载导航配置失败: ' + response.status);
            }
            return response.json();
        })
        .then(function(data) {
            renderNav(data.categories);
        })
        .catch(function(error) {
            console.error('加载导航数据出错:', error);
            navContainer.innerHTML = '<p class="text-danger">导航数据加载失败，请刷新页面重试</p>';
        });

    function renderNav(categories) {
        var html = '<div class="row"><div class="col-12">';
        
        categories.forEach(function(category) {
            html += '<dl class="sitelist_1">';
            html += '<dt>' + escapeHtml(category.name) + '</dt>';
            html += '<dd><ul class="list-inline">';
            
            category.links.forEach(function(link) {
                html += '<li class="list-inline-item">';
                html += '<a target="_blank" href="' + escapeHtml(link.url) + '">' + escapeHtml(link.name) + '</a>';
                html += '</li>';
            });
            
            html += '</ul></dd></dl>';
        });
        
        html += '</div></div>';
        navContainer.innerHTML = html;
    }

    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
